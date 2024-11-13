import io
import unittest
from unittest.mock import patch
import sys
sys.path.append(sys.path[0] + '/../..')
from parser import main


class TestParser(unittest.TestCase):

    # Testing Sample Program 1
    @patch('sys.argv', ['parser.py', '../../sample_programs/programming_assignment_2/Program1.csvlang'])
    def test_sample_program_1(self):

        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Syntax Error(s) Found:

Expected separator ), found keyword header at line 1
Missing semicolon at line 2
Unexpected string "STORE" at line 3
Num attribute already exists at line 4
Column list or index list is missing in store statement at line 5'''

            self.assertEqual(expected_output, received_output.strip())



    # Testing Sample Program 2
    @patch('sys.argv', ['parser.py', '../../sample_programs/programming_assignment_2/Program2.csvlang'])
    def test_sample_program_2(self):
        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Syntax Error(s) Found:

Path attribute is missing in merge statement with save=true at line 3
Aggregate function should have a column name or a column index as the parameter at line 4'''

            self.assertEqual(expected_output, received_output.strip())



    # Testing Sample Program 3
    @patch('sys.argv', ['parser.py', '../../sample_programs/programming_assignment_2/Program3.csvlang'])
    def test_sample_program_3(self):
        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Generated AST:

├── PROGRAM
    ├── LOAD-STMT
        ├── PATH: "../../csv_files/sales.csv"
        ├── HEADER-ATTR
            ├── KEYWORD: header
            ├── OPERATOR: =
            ├── LITERAL: true
    ├── DISPLAY-STMT
        ├── COLUMN-LIST
            ├── COLUMN: "goods"
            ├── COLUMN: "sales"
        ├── NUM-ATTR
            ├── KEYWORD: num
            ├── OPERATOR: =
            ├── NUMBER: 2
        ├── HEADER-ATTR
            ├── KEYWORD: header
            ├── OPERATOR: =
            ├── LITERAL: true
        ├── SORT-ATTR
            ├── KEYWORD: sort
            ├── OPERATOR: =
            ├── COLUMN-LIST
                ├── COLUMN: "goods"
                ├── COLUMN: "sales"
    ├── DISPLAY-STMT
        ├── COLUMN-LIST
            ├── COLUMN: "goods"
            ├── COLUMN: "sales"
        ├── HEADER-ATTR
            ├── KEYWORD: header
            ├── OPERATOR: =
            ├── LITERAL: true
        ├── FILTER-ATTR
            ├── KEYWORD: filter
            ├── OPERATOR: =
            ├── CONDITION
                ├── CONDITION
                    ├── CONDITION
                        ├── COLUMN: "sales"
                        ├── OPERATOR: >=
                        ├── NUMBER: 10
                    ├── OPERATOR: &
                    ├── CONDITION
                        ├── COLUMN: "goods"
                        ├── OPERATOR: =
                        ├── COLUMN: "Paper"
                ├── OPERATOR: |
                ├── CONDITION
                    ├── COLUMN: "sales"
                    ├── OPERATOR: =
                    ├── NUMBER: 5
    ├── PRINT-STMT
        ├── MESSAGE: "The maximum sales: "
        ├── AGGR-FUNC: MAX
            ├── COLUMN: "sales"
    ├── PRINT-STMT
        ├── MESSAGE: "The minimum sales: "
        ├── AGGR-FUNC: MIN
            ├── COL-INDEX: 2
    ├── PRINT-STMT
        ├── MESSAGE: "The total number of goods: "
        ├── AGGR-FUNC: COUNT
            ├── COLUMN: "goods"'''

            self.assertEqual(expected_output, received_output.strip())



    # Testing Sample Program 4
    @patch('sys.argv', ['parser.py', '../../sample_programs/programming_assignment_2/Program4.csvlang'])
    def test_sample_program_4(self):
        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Generated AST:

├── PROGRAM
    ├── LOAD-STMT
        ├── PATH: "../../csv_files/sales_data.csv"
        ├── HEADER-ATTR
            ├── KEYWORD: header
            ├── OPERATOR: =
            ├── LITERAL: true
        ├── TAG-ATTR
            ├── KEYWORD: tag
            ├── OPERATOR: =
            ├── STRING: "sales"
    ├── DELETE-STMT
        ├── TAG-ATTR
            ├── KEYWORD: tag
            ├── OPERATOR: =
            ├── STRING: "sales"
    ├── CREATE-STMT
        ├── PATH: "../../csv_files/new_sales.csv"
    ├── ADD-STMT
        ├── TUPLE-LIST
            ├── TUPLE
                ├── VALUE: "goods"
                ├── VALUE: "date"
                ├── VALUE: "sales"
            ├── TUPLE
                ├── VALUE: "Paper"
                ├── VALUE: "11-12-2024"
                ├── VALUE: "100"
            ├── TUPLE
                ├── VALUE: "Pen"
                ├── VALUE: "11-9-2024"
                ├── VALUE: "86"
    ├── DISPLAY-STMT
        ├── COLUMN-LIST
            ├── COLUMN: "goods"
            ├── COLUMN-EXPR
                ├── COLUMN: "sales"
                ├── OPERATOR: +
                ├── NUMBER: 10
        ├── HEADER-ATTR
            ├── KEYWORD: header
            ├── OPERATOR: =
            ├── LITERAL: true'''

            self.assertEqual(expected_output, received_output.strip())




    # Testing Sample Program 5
    @patch('sys.argv', ['parser.py', '../../sample_programs/programming_assignment_2/Program5.csvlang'])
    def test_sample_program_5(self):
        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Generated AST:

├── PROGRAM
    ├── LOAD-STMT
        ├── PATH: "../../csv_files/matrix.csv"
        ├── HEADER-ATTR
            ├── KEYWORD: header
            ├── OPERATOR: =
            ├── LITERAL: false
    ├── REMOVE-STMT
        ├── TUPLE-LIST
            ├── TUPLE
                ├── VALUE: "22"
                ├── VALUE: "10.2"
                ├── VALUE: "45"
    ├── DISPLAY-STMT
        ├── COL-INDEX-LIST
            ├── COL-INDEX: 1
            ├── COL-INDEX: 2
            ├── COL-INDEX: 3
        ├── HEADER-ATTR
            ├── KEYWORD: header
            ├── OPERATOR: =
            ├── LITERAL: false'''

            self.assertEqual(expected_output, received_output.strip())



if __name__ == '__main__':
    unittest.main()
