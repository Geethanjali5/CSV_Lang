# **CSVLang: CSV File Manipulation**

**CSVLang**, is a declarative language designed to simplify and supercharge your interactions with CSV files. Whether you're a data analyst, developer, or someone working with tabular data, CSVLang transforms how you perform CRUD (Create, Read, Update, Delete) operations—no more verbose code or dependency nightmares like pandas or the csv module!

## Why CSVLang?

CSVLang empowers you to manipulate CSV files using intuitive, SQL-like commands. Forget about tedious loops or 
complex logic! With **simple, one-line commands** like `DISPLAY` and `MERGE`, you can effortlessly:
- Select and filter rows.
- Perform mathematical transformations on columns.
- Merge multiple CSV files into a unified dataset.
- Create complex views and generate reports from raw data.

CSVLang is **designed for simplicity** and **optimized for efficiency**, making it a perfect fit for technical and non-technical users alike.

---

## **Key Features**

**No Dependencies**: Works directly without the need for external libraries — no pandas, no csv modules, just CSVLang.

**CRUD Operations**: Perform all standard CRUD operations on CSV files with streamlined, SQL-inspired commands.

**Single-Line Magic**: Achieve complex operations like filtering, merging, and updating data with concise, readable code.

**Merging Made Easy**: Seamlessly combine CSV files, resolving columns and rows with minimal effort.

**Data Transformation**: Simplify data transformations such as column operations and aggregations like averages.

**Declarative Syntax**: Specify *what* you want to do, and CSVLang handles the *how* for you. Focus on results, not implementation details.

---

## **Novelty**

**Python (Pandas) vs CSVLang**:
- Pandas is a powerful tool, but it comes with a learning curve and additional overhead. CSVLang, on the other hand, allows you to:
  - Avoid learning a full data manipulation library.
  - Skip heavy installations and configurations.
  - Work directly on CSV files, with a **simpler syntax** and zero hassle.

 **Java (OpenCSV) vs CSVLang**:
- OpenCSV requires you to handle file parsing and manipulation manually. CSVLang **abstracts** all of that, giving you instant control over CSV operations with declarative commands.

---


# CSVLang Lexical Grammar

The language recognizes a variety of tokens that form the core structure of valid CSVLang programs.

## Token Classes (in order of priority)

### KEYWORD
- **Description**: Reserved words that perform specific actions in CSVLang. All keywords are case-sensitive.
- **Regex**: `LOAD|CREATE|ADD|REMOVE|DELETE|DISPLAY|STORE|MERGE|AVERAGE|SUM|MAX|MIN|COUNT|PRINT|save|num|sort|filter|tag|path|header`
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

You can run this lexer using the following command. Detailed installation and execution steps are given [below](#installation-and-usage).

```bash
python scanner.py </path/to/file.csv>
```
or

```bash
python3 scanner.py </path/to/file.csv>
```

### Algorithm

The lexical scanning algorithm starts by reading the text in the input CSVLang source code provided.
We use a [Deterministic Finite Automata](https://en.wikipedia.org/wiki/Deterministic_finite_automaton) to scan and classify the input into tokens. Whitespaces are ignored and the 
pointer moves forward. The input is traversed using **state-transitions in the DFA** and there is an **accepting state
corresponding to each [Token Class](#token-classes-in-order-of-priority)** specified above. There is also an **error state** which reports an error if 
the 
input ends up there. However, the lexer is capable of handling it successfully by reporting the error category to the user 
and proceeding with the rest of the code.

#### Accepting States

1. [**Keyword / Literal**](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L51): If the current character is a letter, the scanner keeps moving forward appending 
   every character to a temporary variable called lexeme as long as it keeps encountering a letter. It stops when it 
   gets something other than a letter. At this point, it compares the lexeme against the set of known keywords and literals. If a match is found, it 
   classifies the lexeme accordingly, else it reports an error.
2. [**Number**](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L67): If the current character is a digit, the scanner keeps moving forward appending 
   every character to a temporary variable called lexeme as long as its a digit. It stops when it gets something other 
   than a digit. At this point, it checks if lexeme is `0` or any other number without a leading 0, if that is the 
   case it classifies it as a number else it reports an error.
3. [**Operator**](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L83): If the current character belongs to the list of operators and is one of `<` 
   or `>`, the scanner **looks ahead** to check the next character. If the first character is `<` and the next character happens to be `>` or `=`,
   or if the first character is `>` and the next character happens to be `=`, the scanner classifies both the characters as a 
   operator else only the first character.
4. [**Separator**](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L99): If the current character belongs to the list of separators, then it is classified as a separator.
5. [**String**](https://github.com/Geethanjali5/CSV_Lang/blob/f0ac58bd7fd2d8567fd91fc554973b64f48a8f95/scanner.py#L104): If the current character is a `"`, the scanner keeps moving forward appending 
   every character to a temporary variable called lexeme. It stops when it 
   gets another `"` or reaches the end of file. If the closing `"` is reached before the end of file, it classifies 
   the lexeme as a string, else it reports an error.

#### Error States

The following inputs end up in error states.

1. A mismatched keyword / literal.
2. A number with leading zero(s).
3. A string without an ending `"`.
4. Any other character which does not fit any of the [lexical specifications](#token-summary-table) given above.

### Test Cases

You can run the [unit test file](test.py) that checks the scanner against some [Sample Programs](#sample-programs) using the 
following command.

```bash
python test.py
```

or 

```bash
python3 test.py
```

### Error Handling

There are 4 kinds of errors the lexer can detect.
1. Invalid keyword / literal: If the code contains a keyword or literal unrecognised by the grammar.
2. Invalid number with leading zero(s): If a number starts with a leading `0` (except the number `0` itself)
3. Unclosed string: If a string is not properly enclosed in double quotes (`"`).
4. Unrecognised character: If any character in the source code is not matched by any of the [lexical specifications](#token-summary-table)
   mentioned above.

The lexer has capabilities of reporting the error gracefully with a suitable message and proceeding with the rest of 
the code smoothly.

## [Sample Programs](sample_programs)

### Program 1
This program loads the [student_scores.csv](/csv_files/student_scores.csv) file into the memory and displays the 
first 2 rows. It also displays the average score and persists the displayed data as a new csv file into the memory 
called [student_scores_new.csv](/csv_files/student_scores_new.csv)

[Source Code](sample_programs/Program1.csvlang)<br>
[Lexical Output](lexical_outputs/Program1.txt)<br>
[Program Output](sample_outputs/Program1.txt)

### Program 2
This program loads the [sales.csv](/csv_files/sales.csv) and [sales1.csv]() files into the memory and tags them as 
batch1 and batch2 respectively. It merges the two files and displays the combined data and also persists it as a new 
file in memory called [combined_sales.csv](/csv_files/combined_sales.csv). It also prints the total sales of batch 1 and batch 2.

[Source Code](sample_programs/Program2.csvlang)<br>
[Lexical Output](lexical_outputs/Program2.txt)<br>
[Program Output](sample_outputs/Program2.txt)

### Program 3
This program loads the [sales.csv](/csv_files/sales.csv) file into the memory. It then displays the data after sorting 
goods lexicographically, and proceeds to display all Paper sales which are more than 10. It also displays the 
maximum sales, minimum sales, and the count of unique goods. However, this does not compile owing to some lexical 
errors such as invalid number 02, invalid keyword MAXIMUM, unrecognised character @ and an unclosed string.

[Source Code](sample_programs/Program3.csvlang)<br>
[Lexical Output](lexical_outputs/Program3.txt)<br>
Program Output: No output produced as there is a lexical error

### Program 4
This program loads the [student_scores.csv](/csv_files/student_scores.csv) file into the memory and then proceeds to 
delete it. It creates a new file with the same name and adds a few records in it. Finally, it aims to display goods 
and sales from the new table after incrementing sales by 10. However, this does not compile owing to the lexical 
error of invalid literal True (which is case-sensitive).

[Source Code](sample_programs/Program4.csvlang)<br>
[Lexical Output](lexical_outputs/Program4.txt)<br>
Program Output: No output produced as there is a lexical error

### Program 5
This program loads the [matrix.csv](/csv_files/matrix.csv) file into the memory and removes a row from it. It then 
proceeds to display all records of three columns in the file.

[Source Code](sample_programs/Program5.csvlang)<br>
[Lexical Output](lexical_outputs/Program5.txt)<br>
[Program Output](sample_outputs/Program5.txt)


## Installation and Usage

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

Alternatively, you can also run the pre-existing [shell scripts](shell_scripts) which take care of the installations.

[run_tests.sh](shell_scripts/run_tests.sh): It runs all the test cases. <br>
[run_lexer.sh](shell_scripts/run_tests.sh): It performs lexical analysis on a csvlang file which is passed as an 
argument. <br>
[run_sample_programs.sh](shell_scripts/run_tests.sh): It performs lexical analysis and displays the outputs of 
   all the [Sample Programs](sample_programs).


1. Navigate to the [shell_scripts](shell_scripts) folder.
   ```bash
   cd shell_scripts
   ```
2. Run the following commands to make it executable.
   ```bash
   chmod +x run_tests.sh
   chmod +x run_lexer.sh
   chmod +x run_sample_programs.sh
   ```
3. Run the shell scripts using the following commands.
   ```bash
   ./run_tests.sh
   ```
   ```bash
   ./run_lexer.sh <path/to/test.csvlang>
   ```
   ```bash
   ./run_sample_programs.sh
   ```




#Assignment 2#

# Context-Free Grammar (CFG) for CSVLang

**Context-Free Grammar (CFG)** for CSVLang is a custom language designed to manipulate CSV files using a set of intuitive commands. The CFG defines the rules for forming valid commands and operations in CSVLang.

## Terminals and Non-Terminals
In the CFG, **terminals** are symbols representing actual content (keywords, symbols, literals), while **non-terminals** represent the abstract structure of the language.

### Terminals
- **Keywords**: `LOAD`, `DISPLAY`, `STORE`, `PRINT`, `MERGE`, `DELETE`, `CREATE`, `ADD`, `REMOVE`, `header`, `num`, `sort`, `filter`, `tag`, `save`, etc.
- **Operators**: Symbols like `=`, `<`, `>`, `<=`, `>=`, `!=`, etc.
- **Separators**: Symbols like `(`, `)`, `,`, `;`.
- **Types**: `number`, `string`, `literal` (e.g., `true`, `false`).

### Non-Terminals
- **`<program>`**: Represents the entire set of commands.
- **`<statement>`**: Represents individual commands.
- **`<attribute_list>`**: Represents a list of attributes.
- **`<condition>`**: Represents a condition for filtering data.
- **`<expression>`**: Represents an arithmetic or logical expression.
- **`<tuple>`**: Represents a group of values.
- **`<number_list>`** and **`<column_list>`**: Represents lists of numbers and column names, respectively.

## Grammar Rules
Below is the CFG that represents the CSVLang language grammar.

### 1. Program Rules
The `<program>` represents a collection of statements, each ending with a semicolon:
```
<program> → <statement> ";"
          | <statement> ";" <program>
```
This means a program consists of one or more statements, with each statement ending in a `;`.

### 2. Statement Rules
Statements represent individual operations that the CSVLang language can perform:
```
<statement> → "LOAD" "(" <path> <optional_attribute_list> ")"
            | "DISPLAY" "(" <column_or_index_list> <optional_attribute_list> ")"
            | "STORE" "(" <column_or_index_list> <optional_attribute_list> ")"
            | "PRINT" "(" <message> <optional_aggr_func> <optional_tag> ")"
            | "MERGE" "(" <tag_list> <optional_attribute_list> ")"
            | "DELETE" "(" <tag> ")"
            | "CREATE" "(" <path> ")"
            | "ADD" <tuple_list>
            | "REMOVE" <tuple_list>
```
The `<statement>` non-terminal defines the valid operations, such as loading a CSV (`LOAD`), displaying columns (`DISPLAY`), or storing data (`STORE`).

### 3. Attributes and Path
- **Attributes** are options for commands, such as `header`, `path`, or `num`.
- **Path** is a string value representing a file path.
```
<optional_attribute_list> → "," <attribute_list> | ε
<attribute_list> → <attribute> | <attribute> "," <attribute_list>
<attribute> → "header" "=" "literal"
            | "path" "=" "string"
            | "num" "=" "number"
            | "sort" "=" "(" <column_or_index_list> ")"
            | "filter" "=" "(" <condition> ")"
            | "tag" "=" "string"
            | "save" "=" "literal"
```

### 4. Tuples and Tuple List
Tuples are used for operations like adding or removing rows of data:
```
<tuple_list> → "(" <tuple> ")" | "(" <tuple> ")" "," <tuple_list>
<tuple> → "(" <value_list> ")"
<value_list> → "string" | "string" "," <value_list>
```

### 5. Column or Index List
The `<column_or_index_list>` is used for commands like `DISPLAY` or `STORE` to specify which columns or indices to work with:
```
<column_or_index_list> → <column_list> | <number_list>
<column_list> → "string" | "string" "," <column_list>
<number_list> → "number" | "number" "," <number_list>
```

### 6. Conditions and Expressions
Conditions are used for filtering rows in commands such as `filter`:
```
<condition> → <expression> <operator> <expression>
            | <condition> "&" <condition>
            | <condition> "|" <condition>

<expression> → "string" | "number" | "(" <condition> ")"
<operator> → "=" | "<" | ">" | "<=" | ">=" | "!="
```
Conditions can be combined using logical operators `&` (AND) and `|` (OR).


### 7. Aggregate Functions
For commands like `PRINT`, aggregate functions such as `SUM`, `AVERAGE`, etc., can be specified:
```
<optional_aggr_func> → "," <aggr_func> | ε
<aggr_func> → "SUM" "(" "string" ")"
            | "AVERAGE" "(" "string" ")"
            | "MAX" "(" "string" ")"
            | "MIN" "(" "string" ")"
            | "COUNT" "(" "string" ")"
```

### 8. Tags
Tags can be used to mark certain operations:
```
<tag_list> → "string" | "string" "," <tag_list>
<tag> → "string"
```
These are used in statements like `MERGE` to specify the data sets to be combined.

## Example Walkthrough
Suppose you have an input like:
```
LOAD("file.csv", header="true");
DISPLAY("column1", num=5);
```
The grammar would parse this input as follows:
1. **`LOAD("file.csv", header="true")`**:
   - Match the keyword `LOAD`.
   - Parse `(` and `"file.csv"` as `<path>`.
   - Optionally parse `header="true"` as part of `<optional_attribute_list>`.
   - End with `)` and `:`.
   
   This will generate an AST node of type `LOAD-STMT` with children nodes representing the path and the attribute.

2. **`DISPLAY("column1", num=5)`**:
   - Match the keyword `DISPLAY`.
   - Parse `(` and `"column1"` as part of `<column_or_index_list>`.
   - Optionally parse `num=5` as an attribute.
   - End with `)` and `:`.

## Summary
- The **CFG** describes how the tokens produced by the lexical analyzer can be combined to create valid CSVLang commands.
- **Non-terminals** represent the structure, such as `<program>`, `<statement>`, `<attribute_list>`, `<condition>`, etc.
- **Terminals** represent the actual tokens, such as keywords (`LOAD`, `DISPLAY`), operators (`=`), separators (`(`, `)`), etc.
- The **parser** follows these grammar rules to generate the **AST**, which is used to understand the structure of the source code and execute the appropriate operations on CSV files.

## Sample Input Programs used to test the CSVLang parser - Part 2 

### Program 1: Load and Display Columns
- **Input**: `LOAD("data.csv", header=true); DISPLAY("column1", num=2);`
- **Description**: Loads the CSV file `data.csv` with the header set to true, then displays the first two rows of the `column1`.
- **Expected Output**: A valid AST containing nodes for the `LOAD` and `DISPLAY` statements, with appropriate attributes.
- **[Source Code](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_programs-Part2/Program1.csvlang)**
- **[Program Output](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_outputs-Part2/Program1.txt)**

### Program 2: Create and Add Tuples
- **Input**: `CREATE("new_data.csv"); ADD(("value1", "value2"), ("value3", "value4"));`
- **Description**: Creates a new CSV file named `new_data.csv` and adds two tuples of data to it.
- **Expected Output**: An AST containing nodes for the `CREATE` and `ADD` statements, with `ADD` having a child node representing the list of tuples.
- **[Source Code](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_programs-Part2/Program2.csvlang)**
- **[Program Output](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_outputs-Part2/Program2.txt)**

### Program 3: Merge Tagged Data
- **Input**: `MERGE("tag1", "tag2", save=true, path="merged.csv");`
- **Description**: Merges data sets tagged as `tag1` and `tag2`, saving the merged data to `merged.csv`.
- **Expected Output**: An AST containing a `MERGE` node with children representing the tags and attributes (`save` and `path`).
- **[Source Code](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_programs-Part2/Program3.csvlang)**
- **[Program Output](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_outputs-Part2/Program3.txt)**

### Program 4: Delete and Print
- **Input**: `DELETE("tag1"); PRINT("Deleted tag1 data");`
- **Description**: Deletes data tagged as `tag1` and prints a message confirming the deletion.
- **Expected Output**: An AST containing nodes for the `DELETE` and `PRINT` statements, with `PRINT` having a child representing the message.
- **[Source Code](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_programs-Part2/Program4.csvlang)**
- **[Program Output](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_outputs-Part2/Program4.txt)**


### Program 5: Error Handling with Missing Separator
- **Input**: `DELETE("tag1" ADD(("value1", "value2"));`
- **Description**: Demonstrates error handling by omitting the closing parenthesis for the `DELETE` statement. The parser is expected to identify and report the missing separator.
- **Expected Output**: A `SyntaxError` indicating that a closing parenthesis was expected but not found.
- **[Source Code](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_programs-Part2/Program5.csvlang)**
- **[Program Output](https://github.com/Geethanjali5/CSV_Lang/blob/main/sample_outputs-Part2/Program5.txt)**





## Contribution
**Teammates**:  
1. Geethanjali P (UNI: gp2755)
2. Abhishek Paul (UNI: ap4623)

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE.txt) file for more details.

---

Happy coding! 
