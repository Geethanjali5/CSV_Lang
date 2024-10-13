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

## **How It Works**

Imagine a scenario where you need to load a CSV file, display two columns, and calculate the average of a numeric column. Here’s how it’s done with CSVLang:

**Input CSV** (`student_scores.csv`):
uni, name, score ap4623, Abhishek, 76 gp2755, Geethanjali, 86 dp7865, Darren, 71


**CSVLang Program**:
```csvlang
LOAD("/path/to/student_scores.csv", header=true);
DISPLAY("name", "score", num=2);
DISPLAY(message="The average score: ", AVERAGE(score));'''
```
**Output**:

Abhishek, 76
Geethanjali, 86
The average score: 77.67
```

