import io
import sys
import unittest
from unittest.mock import patch
sys.path.append(sys.path[0] + '/../..')
from code_generator import main


class TestCodeGenerator(unittest.TestCase):

    # Testing Sample Program 1
    @patch('sys.argv', ['code_generator.py', 'sample_programs/programming_assignment_3/Program1.csvlang'])
    def test_sample_program_1(self):

        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Generated Python Code:

from pathlib import Path
import pandas as pd

a0 = pd.read_csv("csv_files/student_scores.csv", header=[0])
a4 = (a0.sort_values(by=[]).head(2))
print(a4.loc[:, ['name', 'score']])
print()
a4 = (a0.sort_values(by=[]).head(2))
a4.loc[:, ['name', 'score']].to_csv("csv_files/student_scores_new.csv", index=False)
print("")
print("The average score: ", a0["score"].mean())

CSVLang Output

         name  score
0    Abhishek     20
1  Githanjali     24


The average score:  19.0'''

            self.assertEqual(expected_output, received_output.strip())



    # Testing Sample Program 2
    @patch('sys.argv', ['code_generator.py', 'sample_programs/programming_assignment_3/Program2.csvlang'])
    def test_sample_program_2(self):
        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Generated Python Code:

from pathlib import Path
import pandas as pd

batch1 = pd.read_csv("csv_files/sales.csv", header=[0])
batch2 = pd.read_csv("csv_files/sales1.csv", header=[0])
pd.concat([batch1, batch2]).to_csv("csv_files/combined_sales.csv", index=False)
print("The total sales of batch 1: ", batch1["sales"].sum())
print("The total sales of batch 2: ", batch2["sales"].sum())

CSVLang Output

The total sales of batch 1:  79
The total sales of batch 2:  74'''

            self.assertEqual(expected_output, received_output.strip())



    # Testing Sample Program 3
    @patch('sys.argv', ['code_generator.py', 'sample_programs/programming_assignment_3/Program3.csvlang'])
    def test_sample_program_3(self):
        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Generated Python Code:

from pathlib import Path
import pandas as pd

a0 = pd.read_csv("csv_files/sales.csv", header=[0])
a4 = (a0.sort_values(by=['goods']).head(2))
print(a4.loc[:, ['goods', 'sales']])
print()
a4 = (a0.sort_values(by=[]).loc[(((a0["sales"] >= 10) & (a0["goods"] == "Paper")) | (a0["sales"] == 5))])
print(a4.loc[:, ['goods', 'sales']])
print()
print("The maximum sales: ", a0["sales"].max())
print("The minimum sales: ", a0["sales"].min())
print("The total number of goods: ", a0["goods"].nunique())

CSVLang Output

   goods  sales
2  Bread      5
1   Eggs     34

   goods  sales
0  Paper     40
2  Bread      5

The maximum sales:  40
The minimum sales:  5
The total number of goods:  3'''

            self.assertEqual(expected_output, received_output.strip())



    # Testing Sample Program 5
    @patch('sys.argv', ['code_generator.py', 'sample_programs/programming_assignment_3/Program5.csvlang'])
    def test_sample_program_5(self):
        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Syntax Error(s) Found:

Expected string, found keyword header at line 1'''

            self.assertEqual(expected_output, received_output.strip())



if __name__ == '__main__':
    unittest.main()
