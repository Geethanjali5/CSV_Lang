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

**CSVLang** recognizes the following token types:

### 1.1 COMMAND
- **Description**: Commands that perform specific operations like loading or displaying CSV files.
- **Pattern**: `LOAD|DISPLAY|STORE|MERGE|INSERT|DELETE|UPDATE`
- **Example**:  
  In `LOAD("path/to/file.csv", header=true);`, the token `LOAD` is a command that triggers the loading of a CSV file.

### 1.2 STRING_LITERAL
- **Description**: A sequence of characters enclosed in double quotes, representing file paths or text values.
- **Pattern**: `\"[^\"]*\"`
- **Example**:  
  In `LOAD("path/to/file.csv", header=true);`, `"path/to/file.csv"` is a string literal representing the file path.

### 1.3 IDENTIFIER
- **Description**: Represents column names or variable names in CSVLang.
- **Pattern**: `[a-zA-Z_][a-zA-Z0-9_]*`
- **Example**:  
  In `DISPLAY("name", "score", num=2);`, `name`, `score`, and `num` are all identifiers.

### 1.4 INTLITERAL (Integer Literal)
- **Description**: A sequence of digits representing an integer.
- **Pattern**: `[0-9]+`
- **Example**:  
  In `num=2`, `2` is an integer literal that specifies the number of rows to display.

### 1.5 OPERATOR
- **Description**: Symbols used to assign or compare values.
- **Pattern**: `[=+*/<>-]`
- **Example**:  
  In `header=true`, the `=` symbol is an operator that assigns the value `true` to `header`.

### 1.6 SEPARATOR
- **Description**: Symbols used for grouping and separating values in the program.
- **Pattern**: `[(),;]`
- **Example**:  
  In `DISPLAY("name", "score", num=2);`, the commas and semicolon are separators.

## 2. Token Summary Table

| Token Type       | Pattern                       | Examples                                |
|------------------|-------------------------------|-----------------------------------------|
| **COMMAND**      | "LOAD|DISPLAY|STORE|..."      | `LOAD`, `DISPLAY`, `MERGE`              |
| **STRING_LITERAL**| `\"[^\"]*\"`                 | `"file.csv"`, `"average score"`         |
| **IDENTIFIER**   | `[a-zA-Z_][a-zA-Z0-9_]*`      | `name`, `score`, `header`               |
| **INTLITERAL**   | `[0-9]+`                      | `2`, `100`, `10`                        |
| **OPERATOR**     | `[=+*/<>-]`                   | `=`, `+`, `-`, `<`, `>`                 |
| **SEPARATOR**    | `[(),;]`                      | `(`, `)`, `,`, `;`                      |


## 3. Sample Tokenization

Let’s look at a simple CSVLang code example and how the tokens will be categorized:

### Example CSVLang Code:
```plaintext
LOAD("path/to/file.csv", header=true);
DISPLAY("name", "score", num=2);



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
