import argparse
import sys

from scanner import scanner


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.token_type}, {self.value})"

    def to_node(self, node_type = None):
        node_type = node_type or self.token_type
        return ASTNode(node_type, self.value)


class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children else []

    def display_tree(self, indent=0):
        if self.value is None:
            print("  " * indent + "├" + "── " + f"{self.node_type.upper()}")
        else:
            print("  " * indent + "├" + "── " + f"{self.node_type.upper()}: {self.value}")

        for child in self.children:
            if child is not None:
                child.display_tree(indent + 2)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            return None

    def prev_token(self):
        if len(self.tokens) > self.position - 1 >= 0:
            return self.tokens[self.position - 1]
        else:
            return None

    def next_token(self):
        if len(self.tokens) > self.position + 1 >= 0:
            return self.tokens[self.position + 1]
        else:
            return None

    def advance(self):
        self.position += 1

    def backtrack(self):
        self.position -= 1

    def expect(self, expected_type, expected_value=None):
        token = self.current_token()
        if token and token.token_type == expected_type and (expected_value is None or token.value in expected_value):
            self.advance()
            return token
        else:
            raise SyntaxError(
                f"Expected {expected_type}" +
                (f" {expected_value}" if expected_value is not None else "") +
                (f", found {token.token_type}: {token.value}" if token else " but found nothing"))

    def parse_program(self):
        nodes = []
        while self.position < len(self.tokens):
            node = self.parse_statement()
            nodes.append(node)
            self.expect("separator", ";")
        return ASTNode("PROGRAM", children=nodes)

    def parse_statement(self):
        token = self.current_token()
        if token.token_type == "keyword":
            if token.value == "LOAD":
                return self.parse_load()
            elif token.value == "DISPLAY":
                return self.parse_display()
            elif token.value == "STORE":
                return self.parse_store()
            elif token.value == "PRINT":
                return self.parse_print()
            elif token.value == "MERGE":
                return self.parse_merge()
            elif token.value == "DELETE":
                return self.parse_delete()
            elif token.value == "CREATE":
                return self.parse_create()
            elif token.value == "ADD":
                return self.parse_add()
            elif token.value == "REMOVE":
                return self.parse_remove()
            else:
                raise SyntaxError(f"Unexpected keyword {token.value}")
        else:
            raise SyntaxError(f"Unexpected token {token.token_type} {token.value}")

    def parse_header(self):
        header_keyword = self.expect("keyword", "header").to_node()
        header_operator = self.expect("operator", "=").to_node()
        header_literal = self.expect("literal").to_node()

        return ASTNode("HEADER-ATTR", children=[header_keyword, header_operator, header_literal])

    def parse_path_attr(self):
        path_keyword = self.expect("keyword", "path").to_node()
        path_operator = self.expect("operator", "=").to_node()
        path_string = self.expect("string").to_node()

        return ASTNode("PATH-ATTR", children=[path_keyword, path_operator, path_string])

    def parse_num(self):
        num_keyword = self.expect("keyword", "num").to_node()
        num_operator = self.expect("operator", "=").to_node()
        num_number = self.expect("number").to_node()

        return ASTNode("NUM-ATTR", children=[num_keyword, num_operator, num_number])

    def parse_sort(self):
        sort_keyword = self.expect("keyword", "sort").to_node()
        sort_operator = self.expect("operator", "=").to_node()
        self.expect("separator", "(")

        column_node = None
        index_node = None

        if self.current_token().token_type == "string":
            column_node = self.parse_strings_list('COLUMN-LIST', 'COLUMN')
            if column_node is None:
                raise SyntaxError("missing column list or index list in sort attribute")
        else:
            index_node = self.parse_number_list()
            if index_node is None:
                raise SyntaxError("missing column list or index list in sort attribute")

        if self.prev_token().token_type == "separator" and self.prev_token().value == ",":
            self.backtrack()
        self.expect("separator", ")")

        return ASTNode("SORT-ATTR", children=[sort_keyword, sort_operator, column_node or index_node])

    def parse_filter(self):
        filter_keyword = self.expect("keyword", "filter").to_node()
        filter_operator = self.expect("operator", "=").to_node()
        self.expect("separator", "(")
        filter_condition = self.parse_condition()
        self.expect("separator", ")")

        return ASTNode("FILTER-ATTR", children=[filter_keyword, filter_operator, filter_condition])

    def parse_column_extension(self):
        operator_node = self.expect("operator").to_node()
        number_node = self.expect("number").to_node()

        return operator_node, number_node

    def parse_number_list(self):
        numbers = []
        while self.current_token().token_type == "number":
            if self.next_token().token_type == "operator":
                column_node = self.expect("number").to_node('COL-INDEX')
                operator_node, number_node = self.parse_column_extension()
                numbers.append(ASTNode("COL-INDEX-EXPR", children=[column_node, operator_node, number_node]))
            else:
                numbers.append(self.expect("number").value)
            if self.current_token().token_type == "separator" and self.current_token().value == ",":
                self.advance()
            else:
                break

        number_nodes = []
        for number in numbers:
            if isinstance(number, ASTNode):
                number_nodes.append(number)
            else:
                number_nodes.append(ASTNode('COL-INDEX', number))
        if len(number_nodes) > 0:
            return ASTNode('COL-INDEX-LIST', children=number_nodes)
        else:
            return None

    def parse_strings_list(self, node_type, sub_node_type):
        strings = []
        while self.current_token().token_type == "string":
            if node_type == 'COLUMN-LIST':
                if self.next_token().token_type == "operator":
                    column_node = self.expect("string").to_node('COLUMN')
                    operator_node, number_node = self.parse_column_extension()
                    strings.append(ASTNode("COLUMN-EXPR", children=[column_node, operator_node, number_node]))
                else:
                    strings.append(self.expect("string").value)
            else:
                strings.append(self.expect("string").value)
            if self.current_token().token_type == "separator" and self.current_token().value == ",":
                self.advance()
            else:
                break

        string_nodes = []
        for string in strings:
            if isinstance(string, ASTNode):
                string_nodes.append(string)
            else:
                string_nodes.append(ASTNode(sub_node_type, string))
        if len(string_nodes) > 0: return ASTNode(node_type, children=string_nodes)
        else: return None

    def parse_tag(self):
        tag_keyword = self.expect("keyword", "tag").to_node()
        tag_operator = self.expect("operator", "=").to_node()
        tag_string = self.expect("string").to_node()

        return ASTNode("TAG-ATTR", children=[tag_keyword, tag_operator, tag_string])

    def parse_save(self):
        save_keyword = self.expect("keyword", "save").to_node()
        save_operator = self.expect("operator", "=").to_node()
        save_string = self.expect("literal").to_node()

        return ASTNode("SAVE-ATTR", children=[save_keyword, save_operator, save_string])

    def parse_attribute_list(self, attributes_to_be_checked):
        attribute_list = []
        attribute_nodes = []

        while self.current_token().token_type == "keyword":
            option = self.current_token().value
            if "num" in attributes_to_be_checked and option == "num":
                if 'NUM-ATTR' in attribute_list:
                    raise SyntaxError('num attribute already exists')
                else:
                    num_node = self.parse_num()
                    attribute_list.append(num_node.node_type)
                    attribute_nodes.append(num_node)

            elif "header" in attributes_to_be_checked and option == "header":
                if 'HEADER-ATTR' in attribute_list:
                    raise SyntaxError('header attribute already exists')
                else:
                    header_node = self.parse_header()
                    attribute_list.append(header_node.node_type)
                    attribute_nodes.append(header_node)

            elif "sort" in attributes_to_be_checked and option == "sort":
                if 'SORT-ATTR' in attribute_list:
                    raise SyntaxError('sort attribute already exists')
                else:
                    sort_node = self.parse_sort()
                    attribute_list.append(sort_node.node_type)
                    attribute_nodes.append(sort_node)

            elif "filter" in attributes_to_be_checked and option == "filter":
                if 'FILTER-ATTR' in attribute_list:
                    raise SyntaxError('filter attribute already exists')
                else:
                    filter_node = self.parse_filter()
                    attribute_list.append(filter_node.node_type)
                    attribute_nodes.append(filter_node)

            elif "path" in attributes_to_be_checked and option == 'path':
                if 'PATH-ATTR' in attribute_list:
                    raise SyntaxError('path attribute already exists')
                else:
                    path_node = self.parse_path_attr()
                    attribute_list.append(path_node.node_type)
                    attribute_nodes.append(path_node)

            elif "tag" in attributes_to_be_checked and option == 'tag':
                if 'TAG-ATTR' in attribute_list:
                    raise SyntaxError('tag attribute already exists')
                else:
                    tag_node = self.parse_tag()
                    attribute_list.append(tag_node.node_type)
                    attribute_nodes.append(tag_node)

            elif "save" in attributes_to_be_checked and option == 'save':
                if 'SAVE-ATTR' in attribute_list:
                    raise SyntaxError('save attribute already exists')
                else:
                    save_node = self.parse_save()
                    attribute_list.append(save_node.node_type)
                    attribute_nodes.append(save_node)

            if self.current_token().token_type == "separator" and self.current_token().value == ",":
                self.advance()
            else:
                break

        return attribute_list, attribute_nodes

    def parse_tuple(self):
        self.expect("separator", "(")

        value_nodes = []
        while self.current_token().token_type == "string":
            value_nodes.append(self.expect("string").to_node('VALUE'))
            if self.current_token().token_type == "separator" and self.current_token().value == ",":
                self.advance()
            else:
                break

        if self.prev_token().token_type == "separator" and self.prev_token().value == ",":
            self.backtrack()
        self.expect("separator", ")")

        return ASTNode("TUPLE", children=value_nodes)

    def parse_tuple_list(self):
        self.expect("separator", "(")

        tuple_nodes = []
        while self.current_token().token_type == "separator" and self.current_token().value == "(":
            tuple_nodes.append(self.parse_tuple())
            if self.current_token().token_type == "separator" and self.current_token().value == ",":
                self.advance()
            else:
                break

        if self.prev_token().token_type == "separator" and self.prev_token().value == ",":
            self.backtrack()
        self.expect("separator", ")")

        return ASTNode("TUPLE-LIST", children=tuple_nodes)

    def parse_load(self):
        self.expect("keyword", "LOAD")
        self.expect("separator", "(")

        path_node = self.expect("string").to_node('PATH')
        if path_node is None:
            raise SyntaxError("path is missing in load statement")

        attribute_nodes = []

        if self.current_token().token_type == "separator" and self.current_token().value == ",":
            self.advance()
            attribute_list, attribute_nodes = self.parse_attribute_list(['header', 'tag'])

        if self.prev_token().token_type == "separator" and self.prev_token().value == ",":
            self.backtrack()
        self.expect("separator", ")")

        return ASTNode("LOAD-STMT", children=[path_node] + attribute_nodes)

    def parse_display(self):
        self.expect("keyword", "DISPLAY")
        self.expect("separator", "(")

        column_node = None
        index_node = None

        if self.current_token().token_type == "string":
            column_node = self.parse_strings_list('COLUMN-LIST', 'COLUMN')
            if column_node is None:
                raise SyntaxError("column list or index list is missing in display statement")
        else:
            index_node = self.parse_number_list()
            if index_node is None:
                raise SyntaxError("column list or index list is missing in display statement")

        if (self.current_token().token_type != "separator" or self.current_token().value != ")")\
            and self.prev_token().value != ",":
                self.expect("separator", ",")

        attribute_list, attribute_nodes = self.parse_attribute_list(['num', 'header', 'sort', 'filter'])

        if self.prev_token().token_type == "separator" and self.prev_token().value == ",":
            self.backtrack()
        self.expect("separator", ")")

        return ASTNode("DISPLAY-STMT", children=[column_node or index_node] + attribute_nodes)

    def parse_store(self):
        self.expect("keyword", "STORE")
        self.expect("separator", "(")

        column_node = None
        index_node = None

        if self.current_token().token_type == "string":
            column_node = self.parse_strings_list('COLUMN-LIST', 'COLUMN')
            if column_node is None:
                raise SyntaxError("column list or index list is missing in store statement")
        else:
            index_node = self.parse_number_list()
            if index_node is None:
                raise SyntaxError("column list or index list is missing in store statement")

        if (self.current_token().token_type != "separator" or self.current_token().value != ")")\
            and self.prev_token().value != ",":
                self.expect("separator", ",")

        attribute_list, attribute_nodes = self.parse_attribute_list(['num', 'header', 'sort', 'filter', 'path'])

        if self.prev_token().token_type == "separator" and self.prev_token().value == ",":
            self.backtrack()
        self.expect("separator", ")")

        if 'PATH-ATTR' not in attribute_list:
            raise SyntaxError("path attribute is missing in store statement")
        return ASTNode("STORE-STMT", children=[column_node or index_node] + attribute_nodes)

    def parse_print(self):
        self.expect("keyword", "PRINT")
        self.expect("separator", "(")

        message_node = self.expect("string").to_node('MESSAGE')
        if message_node is None:
            raise SyntaxError("message is missing in print statement")

        aggr_func_node = None
        tag_node = None

        if self.current_token().token_type == "separator" and self.current_token().value == ",":
            self.advance()
            aggr_func_node = self.parse_aggr_func()
            if self.current_token().token_type == "separator" and self.current_token().value == ",":
                self.advance()
                tag_node = self.parse_tag()

        if self.prev_token().token_type == "separator" and self.prev_token().value == ",":
            self.backtrack()
        self.expect("separator", ")")

        return ASTNode("PRINT-STMT", children=[message_node, aggr_func_node, tag_node])

    def parse_merge(self):
        self.expect("keyword", "MERGE")
        self.expect("separator", "(")

        tag_list_node = self.parse_strings_list('TAG-LIST', 'TAG')
        if tag_list_node is None:
            raise SyntaxError("tag list is missing in merge statement")

        attribute_list, attribute_nodes = self.parse_attribute_list(['save', 'path'])

        for attribute_node in attribute_nodes:
            if attribute_node.node_type == 'SAVE-ATTR' and attribute_node.children[2].value == 'true' and 'PATH-ATTR'\
                    not in attribute_list:
                raise SyntaxError("path attribute is missing in merge statement with save=true")

        if self.prev_token().token_type == "separator" and self.prev_token().value == ",":
            self.backtrack()
        self.expect("separator", ")")

        return ASTNode("MERGE-STMT", children=[tag_list_node] + attribute_nodes)

    def parse_delete(self):
        self.expect("keyword", "DELETE")
        self.expect("separator", "(")

        tag_node = self.parse_tag()
        if tag_node is None:
            raise SyntaxError("tag is missing in delete statement")

        self.expect("separator", ")")

        return ASTNode("DELETE-STMT", children=[tag_node])

    def parse_create(self):
        self.expect("keyword", "CREATE")
        self.expect("separator", "(")

        path_node = self.expect("string").to_node('PATH')
        if path_node is None:
            raise SyntaxError("path is missing in create statement")

        self.expect("separator", ")")
        return ASTNode("CREATE-STMT", children=[path_node])

    def parse_add(self):
        self.expect("keyword", "ADD")
        tuple_list_node = self.parse_tuple_list()
        return ASTNode("ADD-STMT", children=[tuple_list_node])

    def parse_remove(self):
        self.expect("keyword", "REMOVE")
        tuple_list_node = self.parse_tuple_list()
        return ASTNode("REMOVE-STMT", children=[tuple_list_node])

    def parse_aggr_func(self):
        expected_values = ['SUM', 'AVERAGE', 'MAX', 'MIN', 'COUNT']
        value = self.expect("keyword", expected_values).value
        self.expect("separator", "(")
        column_node = self.expect("string").to_node('COLUMN')
        self.expect("separator", ")")
        return ASTNode("AGGR-FUNC", value=value, children=[column_node])

    def parse_expression(self):
        token = self.current_token()

        if token.token_type == "string":
            self.advance()
            return ASTNode("COLUMN", value=token.value)
        elif token.token_type == "number":
            self.advance()
            return ASTNode("NUMBER", value=token.value)
        elif token.token_type == "separator" and token.value == "(":
            self.advance()
            expr = self.parse_condition()
            self.expect("separator", ")")
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")

    def parse_condition(self):
        left = self.parse_expression()
        operator = self.expect("operator").to_node('OPERATOR')
        right = self.parse_expression()

        condition_node = ASTNode("CONDITION", children=[left, operator, right])

        while self.current_token().token_type == "operator" and self.current_token().value in ["&", "|"]:
            logical_operator = self.current_token().to_node('OPERATOR')
            self.advance()
            next_condition = self.parse_condition()
            condition_node = ASTNode("CONDITION", children=[condition_node, logical_operator, next_condition])

        return condition_node

    def parse(self):
        return self.parse_program()


def main():
    arg_parser = argparse.ArgumentParser(description = "Parser for CSV Lang")
    arg_parser.add_argument("file", help = "Path to the CSV Lang source code")

    args = arg_parser.parse_args()

    # Read the file
    try:
        with open(args.file, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: File {args.file} not found.")
        sys.exit(1)

    tokens, errors = scanner(source_code)

    if errors is None or len(errors) == 0:
        scanned_tokens = []
        for token in tokens:
            scanned_tokens.append(Token(token[0], token[1]))

        parser = Parser(scanned_tokens)

        try:
            ast = parser.parse()
            print("\nGenerated AST:\n")
            ast.display_tree()
            print("")
        except SyntaxError as err:
            print(f'\nSyntax Error: {err}\n')
    else:
        print("\nLexical Errors Found:\n")
        for error in errors:
            print(error)
        print("")


if __name__ == "__main__":
    main()