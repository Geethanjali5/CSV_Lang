import argparse
import sys

from parser import Token, Parser
from scanner import scanner


import_flag = False

aggr_methods = {
    "average": "mean",
    "sum": "sum",
    "max": "max",
    "min": "min",
    "count": "nunique"
}

operator_map = {
    '<>': '!=',
    '=': '==',
}

path_map = {}
active_path = ""
active_tag = "a0"
declared_tags = []
declared_paths = {}

def convert_to_shift(expr):
    num1, num2 = map(int, expr.split('*'))

    shifts = []
    position = 0
    while num2 > 0:
        if num2 & 1:
            shifts.append(f"({num1} << {position})")
        num2 >>= 1
        position += 1

    shift_expr = " + ".join(shifts)
    return shift_expr

def generate_filter_expression(node, tag):
    res = []
    for i, child in enumerate(node.children):
        if child.node_type == 'CONDITION':
            res.append(generate_filter_expression(child, tag))
        elif child.node_type == 'COLUMN':
            if i > 0 and node.children[i - 1].node_type == 'OPERATOR':
                res.append(child.value)
            else:
                res.append(f'{tag}[{child.value}]')
        elif child.node_type == 'OPERATOR':
            res.append(operator_map[child.value]
               if operator_map.keys().__contains__(child.value)
               else child.value)
        elif child.node_type == 'NUMBER':
            res.append(child.value)

    return process_sub_expression(res)

def process_sub_expression(sub_expression):
    if isinstance(sub_expression, str):
        return sub_expression

    if isinstance(sub_expression, list):
        if len(sub_expression) == 3 and sub_expression[1] in '+-/%*':
            if sub_expression[1] == '*':
                return str(convert_to_shift(f"{sub_expression[0]} {sub_expression[1]} {sub_expression[2]}"))
            else:
                return str(eval(f"{sub_expression[0]} {sub_expression[1]} {sub_expression[2]}"))
        elif len(sub_expression) == 3 and isinstance(sub_expression[1], str) and sub_expression[1] in ['&', '|']:
            left_expr = process_sub_expression(sub_expression[0])
            operator = sub_expression[1]
            right_expr = process_sub_expression(sub_expression[2])
            return f"({left_expr} {operator} {right_expr})"
        else:
            sub_expressions = [process_sub_expression(item) for item in sub_expression]
            return f"({' '.join(sub_expressions)})"

def generate_python_code(node):
    global import_flag
    global active_path
    global active_tag
    code = ""

    if node.node_type == "PROGRAM":
        for child in node.children:
            code += generate_python_code(child) + "\n"

    elif node.node_type == "LOAD-STMT":
        path = ""
        header = ""
        tag = "a0"

        if not import_flag:
            code += f"from pathlib import Path\n"
            code += f"import pandas as pd\n\n"
            import_flag = True

        for child in node.children:
            if child is None: continue
            if child.node_type == "PATH":
                path = child.value
            elif child.node_type == "HEADER-ATTR":
                header = f"{child.children[2].value}"
            elif child.node_type == "TAG-ATTR":
                tag = f"{child.children[2].value[1:-1]}"
                path_map[tag] = path

        active_path = path
        active_tag = tag
        declared_tags.append(tag)

        if declared_paths.keys().__contains__(path) and declared_paths[path]['header'] == header:
            code += f"{tag} = {declared_paths[path]['tag']}"
        else:
            declared_paths[path] = {'header': header, 'tag': tag}
            code += f"{tag} = pd.read_csv({path}, header={'[0]' if header == 'true' else 'None'})"

    elif node.node_type == "DISPLAY-STMT":
        columns = []
        num = None
        sort_columns = []
        filter_cond = None
        tag = active_tag
        col_index_flag = False
        sort_col_index_flag = False

        for child in node.children:
            if child is None: continue
            if child.node_type == "COLUMN-LIST" or child.node_type == "COL-INDEX-LIST":
                if child.node_type == "COL-INDEX-LIST": col_index_flag = True
                for val in child.children:
                    if val.node_type == "COLUMN-EXPR" or val.node_type == "COL-INDEX-EXPR":
                        code += f'a1 = {active_tag if tag != "a1" else tag}.copy()'
                        code += (f'\na1[{val.children[0].value if val.node_type == "COLUMN-EXPR" else int(val.children[0].value) - 1}] = '
                                 f'a1[{val.children[0].value if val.node_type == "COLUMN-EXPR" else int(val.children[0].value) - 1}] {val.children[1].value} {val.children[2].value}\n')
                        tag = 'a1'
                columns = [col.value.strip('"') if col.node_type == 'COLUMN' or col.node_type == 'COL-INDEX' else
                        col.children[0].value.strip('"')for col in child.children]
            elif child.node_type == "NUM-ATTR":
                num = child.children[2].value
            elif child.node_type == "SORT-ATTR":
                if child.children[2].node_type == 'COL-INDEX-LIST':
                    sort_col_index_flag = True
                    sort_columns = [int(col.value)-1 for col in child.children[2].children]
                else:
                    sort_columns = [col.value.strip('"') for col in child.children[2].children]
            elif child.node_type == "FILTER-ATTR":
                filter_cond = child.children[2]
            elif child.node_type == "TAG-ATTR":
                tag = f"{child.children[2].value[1:-1]}" if tag != 'a1' else 'a1'

        if sort_col_index_flag:
            sort_columns = f'[{tag}.columns[i] for i in {sort_columns}]'

        if filter_cond is None:
            if num is None:
                code += f'a4 = ({tag}.sort_values(by={sort_columns}))'
            else:
                code += f'a4 = ({tag}.sort_values(by={sort_columns}).head({num}))'
        else:
            if num is None:
                code += (f'a4 = ({tag}.sort_values(by={sort_columns}).loc['
                         f'{generate_filter_expression(filter_cond, tag)}])')
            else:
                code += (f'a4 = ({tag}.sort_values(by={sort_columns}).loc['
                         f'{generate_filter_expression(filter_cond, tag)}].head'
                         f'({num}))')

        code += f'\nprint(a4.loc[:, {columns}])' if col_index_flag == False\
            else f'\nprint(a4.iloc[:, {[int(col)-1 for col in columns]}])'
        code += "\nprint("")"

    elif node.node_type == "STORE-STMT":
        columns = []
        num = None
        sort_columns = []
        filter_cond = None
        tag = active_tag
        col_index_flag = False
        path = ""

        for child in node.children:
            if child is None: continue
            if child.node_type == "COLUMN-LIST" or child.node_type == "COL-INDEX-LIST":
                if child.node_type == "COL-INDEX-LIST": col_index_flag = True
                for val in child.children:
                    if val.node_type == "COLUMN-EXPR" or val.node_type == "COL-INDEX-EXPR":
                        code += f'a1 = {active_tag if tag != "a1" else tag}.copy()'
                        code += (
                            f'\na1[{val.children[0].value if val.node_type == "COLUMN-EXPR" else int(val.children[0].value) - 1}] = '
                            f'a1[{val.children[0].value if val.node_type == "COLUMN-EXPR" else int(val.children[0].value) - 1}] {val.children[1].value} {val.children[2].value}\n')
                        tag = 'a1'
                columns = [
                    col.value.strip('"') if col.node_type == 'COLUMN' or col.node_type == 'COL-INDEX' else col.children[
                        0].value.strip('"') for col in child.children]
            elif child.node_type == "NUM-ATTR":
                num = child.children[2].value
            elif child.node_type == "SORT-ATTR":
                sort_columns = [col.value.strip('"') for col in child.children[2].children]
            elif child.node_type == "FILTER-ATTR":
                filter_cond = child.children[2]
            elif child.node_type == "TAG-ATTR":
                tag = f"{child.children[2].value[1:-1]}" if tag != 'a1' else 'a1'
            elif child.node_type == "PATH-ATTR":
                path = child.children[2].value

        if filter_cond is None:
            if num is None:
                code += f'a4 = ({tag}.sort_values(by={sort_columns}))'
            else:
                code += f'a4 = ({tag}.sort_values(by={sort_columns}).head({num}))'
        else:
            if num is None:
                code += (f'a4 = ({tag}.sort_values(by={sort_columns}).loc['
                         f'{generate_filter_expression(filter_cond, tag)}])')
            else:
                code += (f'a4 = ({tag}.sort_values(by={sort_columns}).loc['
                         f'{generate_filter_expression(filter_cond, tag)}].head'
                         f'({num}))')

        code += f'\na4.loc[:, {columns}].to_csv({path}, index=False)' if col_index_flag == False else f'\na4.iloc[:, {[int(col) - 1 for col in columns]}].to_csv({path}, index=False)'
        code += '\nprint("")'

    elif node.node_type == "PRINT-STMT":
        message = ""
        tag = active_tag
        column = ""
        aggr_method = ""

        for child in node.children:
            if child is None: continue
            if child.node_type == "MESSAGE":
                message = child.value
            elif child.node_type == "AGGR-FUNC":
                aggr_func = child.value
                column = child.children[0]
                aggr_method = aggr_methods[str(aggr_func).lower()]
            elif child.node_type == "TAG-ATTR":
                tag = f"{child.children[2].value[1:-1]}"

        column = column.value if column.node_type == 'COLUMN' else f'{tag}.columns[{column.value}]'
        code += f"print({message}, {tag}[{column}].{aggr_method}())" if aggr_method else f"print({message})"

    elif node.node_type == "MERGE-STMT":
        csv_list = []
        path = ""
        save = "false"

        for child in node.children:
            if child is None: continue
            if child.node_type == "PATH-ATTR":
                path = child.children[2].value
            elif child.node_type == "SAVE-ATTR":
                save = child.children[2].value
            elif child.node_type == "TAG-LIST":
                csv_list = [node.value[1:-1] for node in child.children]

        code += f"print(pd.concat([{', '.join(csv_list)}]))\nprint("")" \
            if save == "false" else f"pd.concat([{', '.join(csv_list)}]).to_csv({path}, index=False)"

    elif node.node_type == "DELETE-STMT":
        tag = ""

        for child in node.children:
            if child.node_type == "TAG-ATTR":
                tag = f"{child.children[2].value[1:-1]}"

        code += f'file_path = Path({path_map[tag]})'
        code += f'\nfile_path.unlink()'

    elif node.node_type == "CREATE-STMT":
        path = ""

        for child in node.children:
            if child.node_type == "PATH":
                path = child.value

        active_path = path
        active_tag = 'a0'
        code += f'open({path}, "w").close()'

    elif node.node_type == "ADD-STMT":
        cols = []

        for child in node.children[0].children:
            if child.node_type == "TUPLE":
                cols.append([child.value for child in child.children])

        code += f'with open({active_path}, "a") as file:'
        for col in cols:
            code += f'\n\tfile.write("{",".join([val[1:-1] for val in col])}\\n")'

        code += f"\n{active_tag} = pd.read_csv({active_path}, header=[0])"

    elif node.node_type == "REMOVE-STMT":
        cols = []

        for child in node.children[0].children:
            if child.node_type == "TUPLE":
                cols.append([child.value for child in child.children])

        formatted_cols = [
            tuple(
                float(val.strip('"')) if val.strip('"').replace('.', '', 1).isdigit() else val.strip('"')
                for val in col
            )
            for col in cols
        ]

        code += f'''
a2 = {active_tag}.apply(lambda row: tuple(row.dropna().values) in {formatted_cols}, axis=1)
{active_tag} = {active_tag}[~a2]
{active_tag}.to_csv({active_path}, index=False, header=False)
        '''

    return code

def optimize_code(code: str):
    tags_to_be_removed = []
    for tag in declared_tags:
        if not(code.__contains__(f'{tag}.') or code.__contains__(f'{tag}[')):
            tags_to_be_removed.append(tag)

    filtered_code = "\n".join(
        line for line in code.splitlines()
        if not any(unwanted_substring in line for unwanted_substring in tags_to_be_removed)
    )
    return filtered_code + '\n'

def main():
    arg_parser = argparse.ArgumentParser(description = "Code Generator for CSV Lang")
    arg_parser.add_argument("file", help = "Path to the CSV Lang source code")

    args = arg_parser.parse_args()

    # Read the file
    try:
        with open(args.file, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"\nError: File {args.file} not found.\n")
        sys.exit(1)

    global path_map
    global declared_tags
    global active_path
    global active_tag
    global declared_paths

    path_map= {}
    active_path = ""
    active_tag = "a0"
    declared_tags = []
    declared_paths = {}

    tokens, errors = scanner(source_code)

    if errors is None or len(errors) == 0:
        scanned_tokens = []
        for token in tokens:
            scanned_tokens.append(Token(token[0], token[1]))

        parser = Parser(scanned_tokens)

        ast, is_success = parser.parse()
        if is_success:
            global import_flag
            import_flag = False
            generated_code = optimize_code(generate_python_code(ast))
            print("\nGenerated Python Code:\n")
            print(generated_code)

            print("CSVLang Output\n")
            exec(generated_code)
            print("")
    else:
        print("\nLexical Errors Found:\n")
        for error in errors:
            print(error)
        print("")


if __name__ == "__main__":
    main()