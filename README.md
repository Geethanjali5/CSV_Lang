# **CSVLang: CSV File Manipulation**

**CSVLang**, is a declarative language designed to simplify and supercharge your interactions with CSV files. Whether you're a data analyst, developer, or someone working with tabular data, CSVLang transforms how you perform CRUD (Create, Read, Update, Delete) operations—no more verbose code or dependency nightmares like pandas or the csv module!

## Why CSVLang?

CSVLang empowers you to manipulate CSV files using intuitive, SQL-like commands. Forget about tedious loops or complex logic! With **simple, one-line commands** like `SELECT` and `MERGE`, you can effortlessly:
- Select and filter rows.
- Perform mathematical transformations on columns.
- Merge multiple CSV files into a unified dataset.
- Create complex views and generate reports from raw data.

CSVLang is **designed for simplicity** and **optimized for efficiency**, making it a perfect fit for technical and non-technical users alike.

---

## **Key Features**

**No Dependencies**: Works directly without the need for external libraries—no pandas, no csv modules, just CSVLang.

**CRUD Operations**: Perform all standard CRUD operations on CSV files with streamlined, SQL-inspired commands.

**Single-Line Magic**: Achieve complex operations like filtering, merging, and updating data with concise, readable code.

**Merging Made Easy**: Seamlessly combine CSV files, resolving columns and rows with minimal effort.

**Data Transformation**: Simplify data transformations such as column operations and aggregations like averages.

**Declarative Syntax**: Specify *what* you want to do, and CSVLang handles the *how* for you. Focus on results, not implementation details.

---

## **Why Choose CSVLang Over Traditional Methods?**

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

## 1. Token Types

### 1.1 KEYWORD
- **Description**: Reserved words that perform specific actions in CSVLang.
- **Pattern**: `LOAD|CREATE|ADD|REMOVE|DELETE|DISPLAY|STORE|MERGE|AVERAGE|SUM|MAX|MIN|COUNT|PRINT|save|num|sort|filter|tag|path|header`
- **Examples**: `LOAD`, `DISPLAY`, `STORE`

### 1.2 LITERAL
- **Description**: Boolean literals that represent `true` or `false`.
- **Pattern**: `true|false`
- **Examples**: `true`, `false`

### 1.3 NUMBER
- **Description**: A sequence of digits representing an integer.
- **Pattern**: `[0-9]+`
- **Examples**: `123`, `456`

### 1.4 OPERATOR
- **Description**: Symbols used for arithmetic, logical, or comparison operations.
- **Pattern**: `[\+\-\*/%=&|<>]|<=|>=|<>`
- **Examples**: `+`, `-`, `*`, `/`, `=`, `<=`, `>=`, `<>`

### 1.5 SEPARATOR
- **Description**: Symbols used to group or separate elements in the language.
- **Pattern**: `[(),;]`
- **Examples**: `(`, `)`, `,`, `;`

### 1.6 STRING
- **Description**: A sequence of characters enclosed in double quotes, typically representing file paths or text.
- **Pattern**: `"[^"]*"`
- **Examples**: `"path/to/file.csv"`, `"hello world"`

### 1.7 IDENTIFIER
- **Description**: Identifiers are user-defined names for variables, functions, or columns in CSV files.
- **Pattern**: `[a-z A-Z_][a-z A-Z 0-9]*`
- **Examples**: `name`, `score`, `header`

---


## Token Summary Table

| Token Type       | Pattern                | Examples                                |
|------------------|------------------------|-----------------------------------------|
| **KEYWORD**      | `LOAD`, `DISPLAY`, ...  | `LOAD`, `DISPLAY`, `MERGE`              |
| **STRING**| `"[^\"]*"`             | `"file.csv"`, `"average score"`         |
| **IDENTIFIER**   | `[a-z A-Z_][a-z A-Z 0-9]*`| `name`, `score`, `header`               |
| **LITERAL**   | `[0-9]+`                | `2`, `100`, `10`                        |
| **OPERATOR**     | `[=+*/<>-]`             | `=`, `+`, `-`, `<`, `>`                 |
| **SEPARATOR**    | `[(),;]`                | `(`, `)`, `,`, `;`                      |



## 2. Example CSVLang and Tokens

Let’s look at a simple CSVLang code example and how the tokens will be categorized:

```plaintext
LOAD("path/to/file.csv", header=true);
DISPLAY("name", "score", num=2);
```


### Tokenized Output:

| Lexeme             | Token Type      |
|--------------------|-----------------|
| LOAD               | KEYWORD         |
| (                  | SEPARATOR       |
| "path/to/file.csv"  | STRING  |
| ,                  | SEPARATOR       |
| header             | KEYWORD      |
| =                  | OPERATOR        |
| true               | LITERAL      |
| )                  | SEPARATOR       |
| ;                  | SEPARATOR       |
| DISPLAY            | KEYWORD         |
| (                  | SEPARATOR       |
| "name"             | STRING  |
| ,                  | SEPARATOR       | 
| "score"            | STRING  |
| ,                  | SEPARATOR       |
| num                | KEYWORD      |
| =                  | OPERATOR        |
| 2                  | INTLITERAL      |
| )                  | SEPARATOR       |
| ;                  | SEPARATOR       |

## 4. CSVLang Lexer

The lexer reads a source file, processes it, and outputs the tokens and errors (if any).

## Installation and Usage

### 1. Requirements
- Python 3.x installed on your machine.
- A source file containing **CSVLang** code (e.g., `test.csvlang`).

### 2. Installation Steps
1. Clone or download the repository containing `scanner.py` and `run_scanner.sh`.
2. Ensure you have Python 3 installed. You can check this by running:
   ```bash
   python3 --version
   ```

If Python 3 is not installed, download it from [python.org](https://www.python.org/downloads/)
.

3. Make the shell script executable: You need to make the run_lexer.sh script executable before you can run it. Use the following command:
   ```bash
   chmod +x run_lexer.sh
   ```
4. Prepare a CSVLang source file: The lexer processes files containing CSVLang code. You can create a test file, e.g., test.csvlang, with content like this:
   ```plaintext 
   LOAD("path/to/file.csv", header=true);
   DISPLAY("name", "score", num=2);
   ```
### 3. Running the Shell Script

The shell script `run_lexer.sh` automates running the lexer. Here's how to use it:

### 4. Step-by-Step Instructions:

1. **Run the shell script**: Provide the CSVLang source file as an argument to the shell script:

   ```bash
   ./run_lexer.sh test.csvlang
   ```
   
2. **Output**: The lexer will output the tokens found in the source file and any lexical errors (if applicable).

3. **Shell Script (run_lexer.sh)**:
The shell script is used to execute the scanner.py file. Below is the content of the script:
```bash
#!/bin/bash

# Check if a file is provided as an argument
if [ $# -eq 0 ]; then
    echo "No source code file provided. Usage: ./run_lexer.sh <source_code_file>"
    exit 1
fi

# Store the provided file argument
file=$1

# Check if the file exists
if [ ! -f "$file" ]; then
    echo "File '$file' not found."
    exit 1
fi

# Execute the lexer Python script
python3 scanner.py "$file"
```
**Notes**
Ensure that both the run_lexer.sh script and scanner.py file are in the same directory.

The lexer will print out tokens in the format <Token Type, Token Value>, and will report any errors it encounters.


### How to Use:
- The shell script will run `scanner.py` to tokenize and process CSVLang code files.
- The instructions above are written assuming the lexer code is stored in `scanner.py` and can be executed via a shell script.



## Final Thoughts

With **CSVLang**, working with CSV files has never been easier. By abstracting away the complexity of traditional CSV manipulation tools and offering a SQL-like interface, CSVLang allows users to focus on data insights rather than tedious coding tasks. Whether you're cleaning data, generating reports, or performing complex transformations, CSVLang ensures that your workflow is both efficient and intuitive.

Feel free to explore the project, test it with your own CSV files, and make contributions to improve and extend its functionality. We’re always open to suggestions and new ideas!

---

## Contributing
**Teammates**:  
1. Geethanjali P [UNI: gp2755]  
2. Abhishek Paul [UNI: ap4623]


---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---

Happy coding! 
