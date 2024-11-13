# **CSVLang: CSV File Manipulation**

**CSVLang**, is a declarative language designed to simplify and supercharge your interactions with CSV files. Whether
you're a data analyst, developer, or someone working with tabular data, CSVLang transforms how you perform CRUD (Create,
Read, Update, Delete) operations—no more verbose code or dependency nightmares like pandas or the csv module!

## Why CSVLang?

CSVLang empowers you to manipulate CSV files using intuitive, SQL-like commands. Forget about tedious loops or
complex logic! With **simple, one-line commands** like `DISPLAY` and `MERGE`, you can effortlessly:

- Select and filter rows.
- Perform mathematical transformations on columns.
- Merge multiple CSV files into a unified dataset.
- Create complex views and generate reports from raw data.

CSVLang is **designed for simplicity** and **optimized for efficiency**, making it a perfect fit for technical and
non-technical users alike.

---

## **Key Features**

**No Dependencies**: Works directly without the need for external libraries — no pandas, no csv modules, just CSVLang.

**CRUD Operations**: Perform all standard CRUD operations on CSV files with streamlined, SQL-inspired commands.

**Single-Line Magic**: Achieve complex operations like filtering, merging, and updating data with concise, readable
code.

**Merging Made Easy**: Seamlessly combine CSV files, resolving columns and rows with minimal effort.

**Data Transformation**: Simplify data transformations such as column operations and aggregations like averages.

**Declarative Syntax**: Specify *what* you want to do, and CSVLang handles the *how* for you. Focus on results, not
implementation details.

---

## **Novelty**

**Python (Pandas) vs CSVLang**:

- Pandas is a powerful tool, but it comes with a learning curve and additional overhead. CSVLang, on the other hand,
  allows you to:
    - Avoid learning a full data manipulation library.
    - Skip heavy installations and configurations.
    - Work directly on CSV files, with a **simpler syntax** and zero hassle.

**Java (OpenCSV) vs CSVLang**:

- OpenCSV requires you to handle file parsing and manipulation manually. CSVLang **abstracts** all of that, giving you
  instant control over CSV operations with declarative commands.

---

# CSVLang Lexical Grammar

The language recognizes a variety of tokens that form the core structure of valid CSVLang programs.

## Token Classes (in order of priority)

### KEYWORD

- **Description**: Reserved words that perform specific actions in CSVLang. All keywords are case-sensitive.
- **Regex**:
  `LOAD|CREATE|ADD|REMOVE|DELETE|DISPLAY|STORE|MERGE|AVERAGE|SUM|MAX|MIN|COUNT|PRINT|save|num|sort|filter|tag|path|header`
- **Examples**: `LOAD`, `DISPLAY`, `STORE`

### LITERAL

- **Description**: Boolean literals that represent `true` or `false`. All literals are case-sensitive.
- **Regex**: `true|false`
- **Examples**: `true`, `false`

### NUMBER

- **Description**: The set of whole numbers.
- **Regex**: `(0 | [1-9][0-9]*)`
- **Examples**: `123`, `456`, `0`, `10`

### OPERATOR

- **Description**: Symbols used for arithmetic, logical, or comparison operations.
- **Regex**: `[+-*/%=&|<>]|<=|>=|<>`
- **Examples**: `+`, `-`, `*`, `/`, `=`, `<=`, `>=`, `<>`

### SEPARATOR

- **Description**: Symbols used to group or separate elements in the language. Semicolon (`;`) is used to separate
  different lines of code.
- **Regex**: `[(),;]`
- **Examples**: `(`, `)`, `,`, `;`

### STRING

- **Description**: A sequence of characters enclosed in double quotes, typically representing file paths or text.
- **Regex**: `"[^"]*"`
- **Examples**: `"path/to/file.csv"`, `"hello world"`

Note: Whitespaces are ignored by our language.

---

## Token Summary Table

| Token Class   | Regex                                                                                                                                                                                | Examples                        |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| **KEYWORD**   | `LOAD \| CREATE \| ADD \| REMOVE \| DELETE \| DISPLAY \| STORE \| MERGE \| AVERAGE \| SUM \| MAX \| MIN \| COUNT \| PRINT \| save \| num \| sort \| filter \| tag \| path \| header` | `LOAD`, `DISPLAY`, `MERGE`      |
| **LITERAL**   | `true \| false`                                                                                                                                                                      | `true`, `false`                 |
| **NUMBER**    | `(0 \| [1-9][0-9]*)`                                                                                                                                                                 | `2`, `100`, `0`                 |
| **OPERATOR**  | `[+-*/%=&\|<>] \| <= \| >= \| <>`                                                                                                                                                    | `=`, `+`, `-`, `<=`, `<>`       |
| **SEPARATOR** | `[(),;]`                                                                                                                                                                             | `(`, `)`, `,`, `;`              |
| **STRING**    | `"[^\"]*"`                                                                                                                                                                           | `"file.csv"`, `"average score"` |

## Example CSVLang and Tokens

Let’s look at a simple CSVLang code example and how the tokens will be categorized:

```plaintext
LOAD("path/to/file.csv", header=true);
DISPLAY("name", "score", num=2);
```

### Tokenized Output:

| Lexeme             | Token Class |
|--------------------|-------------|
| LOAD               | KEYWORD     |
| (                  | SEPARATOR   |
| "path/to/file.csv" | STRING      |
| ,                  | SEPARATOR   |
| header             | KEYWORD     |
| =                  | OPERATOR    |
| true               | LITERAL     |
| )                  | SEPARATOR   |
| ;                  | SEPARATOR   |
| DISPLAY            | KEYWORD     |
| (                  | SEPARATOR   |
| "name"             | STRING      |
| ,                  | SEPARATOR   | 
| "score"            | STRING      |
| ,                  | SEPARATOR   |
| num                | KEYWORD     |
| =                  | OPERATOR    |
| 2                  | NUMBER      |
| )                  | SEPARATOR   |
| ;                  | SEPARATOR   |

## CSVLang Lexer

The lexer reads a source file, processes it, and prints the tokens and errors (if any).

### Input

A csvlang source file

### Output

The output is of the following format.

```bash
TOKENS
< token_class, lexeme >
...

ERRORS
error type: invalid token
...
```

### Execution

You can run [this scanner](scanner.py) using the following command. Detailed installation and execution steps are
given [below](#installation-and-usage-scanning).

```bash
python scanner.py </path/to/file.csv>
```

or

```bash
python3 scanner.py </path/to/file.csv>
```

### Algorithm

The lexical scanning algorithm starts by reading the text in the input CSVLang source code provided.
We use a [Deterministic Finite Automata](https://en.wikipedia.org/wiki/Deterministic_finite_automaton) to scan and
classify the input into tokens. Whitespaces are ignored and the
pointer moves forward. The input is traversed using **state-transitions in the DFA** and there is an **accepting state
corresponding to each [Token Class](#token-classes-in-order-of-priority)** specified above. There is also an **error
state** which reports an error if
the
input ends up there. However, the lexer is capable of handling it successfully by reporting the error category to the
user
and proceeding with the rest of the code.

#### Accepting States

1. [**Keyword / Literal
   **](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L51): If the
   current character is a letter, the scanner keeps moving forward appending
   every character to a temporary variable called lexeme as long as it keeps encountering a letter. It stops when it
   gets something other than a letter. At this point, it compares the lexeme against the set of known keywords and
   literals. If a match is found, it
   classifies the lexeme accordingly, else it reports an error.
2. [**Number**](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L67):
   If the current character is a digit, the scanner keeps moving forward appending
   every character to a temporary variable called lexeme as long as its a digit. It stops when it gets something other
   than a digit. At this point, it checks if lexeme is `0` or any other number without a leading 0, if that is the
   case it classifies it as a number else it reports an error.
3. [**Operator
   **](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L83): If the
   current character belongs to the list of operators and is one of `<`
   or `>`, the scanner **looks ahead** to check the next character. If the first character is `<` and the next character
   happens to be `>` or `=`,
   or if the first character is `>` and the next character happens to be `=`, the scanner classifies both the characters
   as a
   operator else only the first character.
4. [**Separator
   **](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L99): If the
   current character belongs to the list of separators, then it is classified as a separator.
5. [**String**](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L104):
   If the current character is a `"`, the scanner keeps moving forward appending
   every character to a temporary variable called lexeme. It stops when it
   gets another `"` or reaches the end of file. If the closing `"` is reached before the end of file, it classifies
   the lexeme as a string, else it reports an error.

#### Error States

The following inputs end up in error states.

1. A mismatched keyword / literal.
2. A number with leading zero(s).
3. A string without an ending `"`.
4. Any other character which does not fit any of the [lexical specifications](#token-summary-table) given above.

### Test Cases (Scanning)

You can run the [unit test file](tests/programming_assignment_1/test_scanner.py) that checks the scanner against
some [Sample Programs](#sample-programs--scanning-) using the
following command.

```bash
python tests/programming_assignment_1/test_scanner.py
```

or

```bash
python3 tests/programming_assignment_1/test_scanner.py
```

### Error Handling (Scanning)

There are 4 kinds of errors the lexer can detect.

1. Invalid keyword / literal: If the code contains a keyword or literal unrecognised by the grammar.
2. Invalid number with leading zero(s): If a number starts with a leading `0` (except the number `0` itself)
3. Unclosed string: If a string is not properly enclosed in double quotes (`"`).
4. Unrecognised character: If any character in the source code is not matched by any of
   the [lexical specifications](#token-summary-table)
   mentioned above.

The lexer has capabilities of reporting the error gracefully with a suitable message and proceeding with the rest of
the code smoothly.

## [Sample Programs (Scanning)](sample_programs/programming_assignment_1)

### Program 1

This program loads the [student_scores.csv](/csv_files/student_scores.csv) file into the memory and displays the
first 2 rows. It also displays the average score and persists the displayed data as a new csv file into the memory
called [student_scores_new.csv](/csv_files/student_scores_new.csv)

[Source Code](sample_programs/programming_assignment_1/Program1.csvlang)<br>
[Lexical Output](compiler_outputs/programming_assignment_1/Program1.txt)<br>
[Program Output](sample_outputs/programming_assignment_1/Program1.txt)

### Program 2

This program loads the [sales.csv](/csv_files/sales.csv) and [sales1.csv](/csv_files/sales1.csv) files into the 
memory and tags them as batch1 and batch2 respectively. It merges the two files and displays the combined data and also persists it as a new
file in memory called [combined_sales.csv](/csv_files/combined_sales.csv). It also prints the total sales of batch 1 and
batch 2.

[Source Code](sample_programs/programming_assignment_1/Program2.csvlang)<br>
[Lexical Output](compiler_outputs/programming_assignment_1/Program2.txt)<br>
[Program Output](sample_outputs/programming_assignment_1/Program2.txt)

### Program 3

This program loads the [sales.csv](/csv_files/sales.csv) file into the memory. It then displays the data after sorting
goods lexicographically, and proceeds to display all Paper sales which are more than 10. It also displays the
maximum sales, minimum sales, and the count of unique goods. However, this does not compile owing to some lexical
errors such as invalid number 02, invalid keyword MAXIMUM, unrecognised character @ and an unclosed string.

[Source Code](sample_programs/programming_assignment_1/Program3.csvlang)<br>
[Lexical Output](compiler_outputs/programming_assignment_1/Program3.txt)<br>
Program Output: No output produced as there is a lexical error

### Program 4

This program loads the [sales.csv](/csv_files/sales.csv) file into the memory and then proceeds to
delete it. It creates a new file with the same name and adds a few records in it. Finally, it aims to display goods
and sales from the new table after incrementing sales by 10. However, this does not compile owing to the lexical
error of invalid literal True (which is case-sensitive).

[Source Code](sample_programs/programming_assignment_1/Program4.csvlang)<br>
[Lexical Output](compiler_outputs/programming_assignment_1/Program4.txt)<br>
Program Output: No output produced as there is a lexical error

### Program 5

This program loads the [matrix.csv](/csv_files/matrix.csv) file into the memory and removes a row from it. It then
proceeds to display all records of three columns in the file.

[Source Code](sample_programs/programming_assignment_1/Program5.csvlang)<br>
[Lexical Output](compiler_outputs/programming_assignment_1/Program5.txt)<br>
[Program Output](sample_outputs/programming_assignment_1/Program5.txt)

## Installation and Usage (Scanning)

### Requirements

- [Python 3.x](https://www.python.org/) installed on your machine.
- A source file containing **CSVLang** code (e.g., `test.csvlang`).

### Installation Steps

1. Clone or download this repository.
    ```bash
   git clone https://github.com/Geethanjali5/CSV_Lang.git
   ```

2. If Python 3 is not installed, download it from [python.org](https://www.python.org/downloads/) manually. Or, you
   can use the following commands.

   #### MacOS
   If [Homebrew](https://brew.sh/) is not installed, then install it with the following command.
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   Install Python via Homebrew
   ```bash
   brew install python3
   ```

   #### Linux
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip
   ```

   #### Windows (PowerShell)
   ```bash
   # Download the Python installer
   Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python_installer.exe
    
   # Install Python silently with default options and add it to PATH
   Start-Process python_installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait
    
   # Clean up the installer
   Remove-Item python_installer.exe
   ```

3. Ensure Python has been successfully installed. You can check this by running the following command in Windows:
   ```bash
   python --version
   ```

   or (on Linux or Mac),

   ```bash
   python3 --version
   ```

Alternatively, you can also run the pre-existing [shell scripts](shell_scripts/programming_assignment_1) which take care of the installations.

[run_scanner_tests.sh](shell_scripts/programming_assignment_1/run_scanner_tests.sh): It runs all the [test cases](tests/programming_assignment_1/test_scanner.py).<br>
[run_scanner.sh](shell_scripts/programming_assignment_1/run_scanner.sh): It performs lexical analysis on a csvlang
file which is passed as an
argument. <br>
[run_sample_programs.sh](shell_scripts/programming_assignment_1/run_sample_programs.sh): It performs lexical 
analysis and
displays the outputs of
all the [Sample Programs](sample_programs/programming_assignment_1).

1. Navigate to the [shell_scripts](shell_scripts/programming_assignment_1) folder.
   ```bash
   cd shell_scripts/programming_assignment_1
   ```
2. Run the following commands to make it executable.
   ```bash
   chmod +x run_scanner_tests.sh
   chmod +x run_scanner.sh
   chmod +x run_sample_programs.sh
   ```
3. Run the shell scripts using the following commands.
   ```bash
   ./run_scanner_tests.sh
   ```
   ```bash
   ./run_scanner.sh <path/to/test.csvlang>
   ```
   ```bash
   ./run_sample_programs.sh
   ```

# Context-Free Grammar (CFG) for CSVLang

It defines the rules for forming valid commands and statements in CSVLang.

## Terminals and Non-Terminals

In the CFG, **terminals** are symbols representing actual content (keywords, literals, numbers, operators, 
separators and strings), while **non-terminals**
represent the abstract structure of the language.

### Terminals

- **Keywords**: `LOAD | CREATE | ADD | REMOVE | DELETE | DISPLAY | STORE | MERGE | AVERAGE | SUM | MAX | MIN | COUNT | PRINT | save | num | sort | filter | tag | path | header`
- **Operators**: `=`, `<`, `>`, `<=`, `>=`, `<>`, `&`, `|`, `+`, `-`, `*`, `/`, `%`
- **Separators**: `(`, `)`, `,`, `;`
- **String**: Any text enclosed in double quotes (`"`)
- **Literal**: `True`, `False`
- **Number**: The set of whole numbers

### Non-Terminals

- **`<program>`** : Represents the entire set of commands.
- **`<statement>`** : Represents an individual operation or command in CSVLang (e.g., LOAD, DISPLAY, STORE).
- **`<path>`** : A string that represents the file path for operations such as LOAD and STORE.
- **`<load_attribute_list>`** : Specifies optional attributes for the LOAD statement, such as `header` and `tag`.
- **`<column_or_index_list>`** : Specifies columns or indices to be displayed or operated on.
- **`<column_list>`** : A list of column names separated by commas.
- **`<index_list>`** : A list of indices (numbers) separated by commas.
- **`<display_attribute_list>`** : Specifies optional attributes for the DISPLAY statement, such as `num`, `header`, `sort`, and `filter`.
- **`<num-attr>`** : Specifies the `num` attribute in DISPLAY, which limits the number of displayed rows.
- **`<sort-attr>`** : Specifies the `sort` attribute in DISPLAY, which sorts the columns or indices.
- **`<filter-attr>`** : Specifies the `filter` attribute in DISPLAY, which filters rows based on a condition.
- **`<header-attr>`** : Specifies the `header` attribute, indicating whether the data has a header.
- **`<tag-attr>`** : Specifies the `tag` attribute, used for tagging or categorizing operations.
- **`<literal>`** : Represents a literal boolean value, either `true` or `false`.
- **`<number>`** : Represents a whole number (e.g., 0, 1, 2, ...).
- **`<string>`** : Represents a sequence of characters enclosed in double quotes.
- **`<condition>`** : Represents a condition, either a comparison or a logical expression.
- **`<operand>`** : Represents either a string or a number that is used in a condition.
- **`<operator>`** : Represents an operator used in a condition, such as `=`, `>`, `<`, `>=`, `<=`, `<>`, etc.
- **`<store_attribute_list>`** : Specifies the attributes for the STORE statement, such as display attributes and the path.
- **`<aggr-func>`** : Represents an aggregate function like `SUM`, `MAX`, `MIN`, `COUNT`, or `AVERAGE`.
- **`<function-param>`** : Represents the parameter for an aggregate function, which can be a string or number.
- **`<tuple-list>`** : Represents a list of tuples to be added or removed in operations like ADD and REMOVE.
- **`<merge-attribute_list>`** : Specifies attributes for the MERGE statement, such as the `save` option and the `path`.
- **`<tag-list>`** : Represents a list of tags and their associated columns for use in operations like MERGE or CREATE.
- **`<tuple>`** : Represents a tuple containing a `tag-list`.
- **`<tuple-sub-list>`** : A sub-list of additional tuples, used to add multiple tuples in the ADD statement.
- **`<logical-op>`** : `&` or `|` to be used between two conditions in a filter operation.

## Grammar Rules

Below is the CFG that represents the CSVLang grammar. Kindly note that for representational purposes we have written 
the non-terminals as `<non-terminal>` (enclosed within `<>`), while the terminals are written as it is.

### 1. Program Rules

The `<program>` represents a collection of statements, each ending with a semicolon.

```
<program> -> <statement> ";"
          | <statement> ";" <program>
```

This means a program consists of one or more statements, with each statement ending in a `;`.

### 2. Statement Rules

Statements represent individual operations that CSVLang can perform.

```
<statement> ->   LOAD ( <path> <load_attribute_list> )
               | DISPLAY ( <column_or_index_list> <display_attribute_list> )
               | STORE ( <column_or_index_list> <store_attribute_list> )
               | PRINT ( <message> <aggr_func> <tag-attr> )
               | MERGE ( <tag_list> <merge_attribute_list> )
               | DELETE ( <tag> )
               | CREATE ( <path> )
               | ADD ( <tuple_list> )
               | REMOVE ( <tuple_list> )
```

The `<statement>` non-terminal defines the valid operations, such as loading a CSV (`LOAD`), displaying columns (
`DISPLAY`), or storing data (`STORE`).

### 3. Path

```
<path> -> <string>
```

### 4. Load Attribute List

```
<load_attribute_list> -> <header-attr> <tag-attr> | ε
```

### 5. Column or Index List

```
<column_or_index_list> -> <string> <column_list> | <number> <index_list>
```

### 6. Column List

```
<column_list> -> , <string> <column_list> | ε
```

### 7. Index List

```
<index_list> -> , <number> <index_list> | ε
```

### 8. Display Attribute List

```
<display_attribute_list> -> <num-attr> <header-attr> <sort-attr> <filter-attr> | ε
```

### 9. Num Attribute

```
<num-attr> -> , num = <number> | ε
```

### 10. Sort Attribute

```
<sort-attr> -> , sort = <column_or_index_list> | ε
```

### 11. Filter Attribute

```
<filter-attr> -> , filter = <condition> | ε
```

### 12. Header Attribute

```
<header-attr> -> , header = <literal> | ε
```

### 13. Tag Attribute

```
<tag-attr> -> , tag = <literal> | ε
```

### 14. Literal

```
<literal> -> true | false
```

### 15. Number

```
<number> -> 0, 1, 2 ...
```

### 16. String

```
<string> -> any text in "" (double quotes)
```

### 17. Condition

```
<condition> -> <condition> <logical-op> <condition> | <operand> <operator> <operand>
```

### 18. Operand

```
<operand> -> <string> | <number>
```

### 19. Store Attribute List

```
<store_attribute_list> -> <display_attribute_list> <path>
```

### 20. Aggregate Function

```
<aggr-func> ->    , SUM ( <function-param> )
                | , MAX ( <function-param> )
                | , MIN ( <function-param> ) 
                | , COUNT ( <function-param> ) 
                | , AVERAGE ( <function-param> )
```

### 21. Function Parameter

```
<function-param> -> <string> | <number>
```

### 22. Tuple List

```
<tuple-list> -> <tuple> <tuple-sub-list>
```

### 23. Merge Attribute List

```
<merge-attribute_list> -> , save = false | , save = true , path = <path> | ε
```

### 24. Tag List

```
<tag-list> -> <string> <column-list>
```

### 25. Tuple

```
<tuple> -> ( <tag-list> )
```

### 26. Tuple Sub-List

```
<tuple-sub-list> -> , <tuple> <tuple-sub-list> | ε
```

### 27. Logical Operator

```
<logical-op> -> & | | 
```


## Example Walkthrough (Parsing)

Sample Input:

```
LOAD("file.csv", header="true");
DISPLAY("column1", num=5);
```

The grammar would parse this input as follows:

1. **`LOAD("file.csv", header=true)`**:
    - Match the keyword `LOAD`.
    - Parse `(` and `"file.csv"` as `<path>`.
    - Optionally parse `header=true` as part of `<load_attribute_list>`.
    - End with `)` and `;`.

   This will generate an AST node of type `LOAD-STMT` with children nodes representing the path and the attribute.

2. **`DISPLAY("column1", num=5)`**:
    - Match the keyword `DISPLAY`.
    - Parse `(` and `"column1"` as part of `<column_or_index_list>`.
    - Optionally parse `num=5` as part of `<display_attribute_list>`.
    - End with `)` and `;`.

## Parsing Summary

- The **CFG** describes how the tokens produced by the lexical analyzer can be combined to create valid CSVLang
  commands.
- **Non-terminals** represent the structure, such as `<program>`, `<statement>`, `<load_attribute_list>`, 
  `<condition>`, etc.
- **Terminals** represent the actual tokens, such as keywords (`LOAD`, `DISPLAY`), operators (`=`), separators (`(`,
  `)`), etc.
- The **parser** follows these grammar rules to generate the **AST**, which is used to understand the structure of the
  source code and execute the appropriate operations on CSV files.

## Error Handling (Parsing)

The parser is capable of handling different kinds of errors as shown below.

1. **File not found**: It shows an appropriate error message if the program to be parsed is not found.

2. **Lexical errors**: If the program has lexical errors, the parser shows the same without proceeding to the 
   syntactic phase of compilation.

3. **Unexpected token**: 
   ```aiignore
   LOAD ("../../csv_files/student_scores.csv" header = true);

   Expected separator ), found keyword header at line <line_num>
   ```
4. **Missing semicolon**: 
   ```aiignore
   DISPLAY ("name", "score", num=2, header = true)
   
   Missing semicolon at line <line_num>
   ```
5. **Attribute already exists**:
   ```aiignore
   STORE ("name", "score", num=2, num=2, header = true, path = "../../csv_files/student_scores_new_two_rows.csv");
   
   Num attribute already exists at line <line_num>
   ```
6. **Mandatory attribute missing**:
   ```aiignore
   MERGE ("batch1", "batch2", save = true);
   
   Path attribute is missing in merge statement with save=true at line <line_num>
   ```
7. **Aggregation Functions should have a proper parameter**:
   ```aiignore
   PRINT ("The total sales of batch 1: ", SUM(), tag = "batch1");
   
   Aggregate function should have a column name or a column index as the parameter at line <line_num>
   ```
   
These are some of the most common errors. Feel free to refer to this [demo video URL](https://drive.google.com/file/d/1KBIhaFnt1jEljXF3aCUTxZCgEEW380Ni/view?usp=sharing) also available [here](parsing_demo_url.txt) for a 
deep 
dive into the parsing logic.
   
## Execution (Parsing)

You can run [this parser](parser.py) using the following command.

```bash
python parser.py </path/to/file.csv>
```

or

```bash
python3 parser.py </path/to/file.csv>
```

## Test Cases (Parsing)

You can run the [unit test file](tests/programming_assignment_2/test_parser.py) that checks the parser against
some [Sample Programs](#sample-programs--parsing-) using the following command.

```bash
python tests/programming_assignment_2/test_parser.py
```
or

```bash
python3 tests/programming_assignment_2/test_parser.py
```

## [Sample Programs (Parsing)](sample_programs/programming_assignment_2)

### Program 1

This program loads the [student_scores.csv](/csv_files/student_scores.csv) file into the memory and displays the
first 2 rows. It then tries to persist the first one, two and three records into three new corresponding files in 
memory. It also displays the average score. However, this does not compile owing to some syntax errors like the ones
shown in the output below.

[Source Code](sample_programs/programming_assignment_2/Program1.csvlang)<br>
[Parser Output](compiler_outputs/programming_assignment_2/Program1.txt)<br>
Program Output: No output produced as there are syntax error(s) present.

### Program 2

This program loads the [sales.csv](/csv_files/sales.csv) and [sales1.csv](/csv_files/sales1.csv) files into the 
memory and tags them as batch1 and batch2 respectively. It merges the two files and displays the combined data and also persists it as a new
file in memory called [combined_sales.csv](/csv_files/combined_sales.csv). It also prints the total sales of batch 1 and
batch 2. However, this does not compile owing to some syntax errors like the ones shown in the output below.

[Source Code](sample_programs/programming_assignment_2/Program2.csvlang)<br>
[Parser Output](compiler_outputs/programming_assignment_2/Program2.txt)<br>
Program Output: No output produced as there are syntax error(s) present.

### Program 3

This program loads the [sales.csv](/csv_files/sales.csv) file into the memory. It then displays the data after sorting
goods lexicographically and sorting sales in ascending order for records of same goods, and then proceeds to display 
all Paper sales which are more than or equal to 10 or goods whose sales are equal to 5. It also displays 
the maximum sales, minimum sales, and the count of unique goods.

[Source Code](sample_programs/programming_assignment_2/Program3.csvlang)<br>
[Parser Output](compiler_outputs/programming_assignment_2/Program3.txt)<br>
[Program Output](sample_outputs/programming_assignment_2/Program3.txt)

### Program 4

This program loads the [sales.csv](/csv_files/sales.csv) file into the memory and then proceeds to
delete it. It creates a [new file](/csv_files/new_sales.csv) and adds a few records in it. Finally, it aims to display 
goods and sales from the new table after incrementing sales by 10.

[Source Code](sample_programs/programming_assignment_2/Program4.csvlang)<br>
[Parser Output](compiler_outputs/programming_assignment_2/Program4.txt)<br>
[Program Output](sample_outputs/programming_assignment_2/Program4.txt)

### Program 5

This program loads the [matrix.csv](/csv_files/matrix.csv) file into the memory and removes a row from it. It then
proceeds to display all records of three columns in the file.

[Source Code](sample_programs/programming_assignment_2/Program5.csvlang)<br>
[Parser Output](compiler_outputs/programming_assignment_2/Program5.txt)<br>
[Program Output](sample_outputs/programming_assignment_2/Program5.txt)

## Installation and Usage (Parsing)

For [Python](https://www.python.org/) and [Homebrew](https://brew.sh/), you can follow the same installation steps 
as shown [above](#installation-and-usage-scanning) for scanning.

Additionally, you can also run the pre-existing [shell scripts](shell_scripts/programming_assignment_2) 
specifically added for parsing, which take care of the installations.

[run_parser_tests.sh](shell_scripts/programming_assignment_2/run_parser_tests.sh): It runs all the [test cases](tests/programming_assignment_2/test_parser.py). <br>
[run_parser.sh](shell_scripts/programming_assignment_2/run_parser.sh): It performs syntactic analysis on a csvlang
file which is passed as an argument. <br>
[run_sample_programs.sh](shell_scripts/programming_assignment_2/run_sample_programs.sh): It performs syntactic 
analysis and displays the outputs of all the [Sample Programs](sample_programs/programming_assignment_2).

1. Navigate to the [shell_scripts](shell_scripts/programming_assignment_2) folder.
   ```bash
   cd shell_scripts/programming_assignment_2
   ```
2. Run the following commands to make it executable.
   ```bash
   chmod +x run_parser_tests.sh
   chmod +x run_parser.sh
   chmod +x run_sample_programs.sh
   ```
3. Run the shell scripts using the following commands.
   ```bash
   ./run_parser_tests.sh
   ```
   ```bash
   ./run_parser.sh <path/to/test.csvlang>
   ```
   ```bash
   ./run_sample_programs.sh
   ```

## Contribution

**Team Name**: Compile and Conquer

**Teammates**:

1. Geethanjali P (UNI: gp2755)
2. Abhishek Paul (UNI: ap4623)

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE.txt) file for more details.

---

Happy coding! 
