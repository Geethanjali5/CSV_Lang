import io
import sys
import unittest
from unittest.mock import patch
sys.path.append(sys.path[0] + '/../..')
from optimised_code_generator import main


class TestCodeGenerator(unittest.TestCase):

    # Testing Sample Program 1
    @patch('sys.argv', ['optimised_code_generator.py', 'sample_programs/programming_assignment_4/Program1.csvlang'])
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
    @patch('sys.argv', ['optimised_code_generator.py', 'sample_programs/programming_assignment_4/Program2.csvlang'])
    def test_sample_program_2(self):
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
a4 = (a0.sort_values(by=[]).loc[(((a0["sales"] >= (2 << 0) + (2 << 2)) & (a0["goods"] == "Paper")) | (a0["sales"] == 5))])
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



    # Testing Sample Program 3
    @patch('sys.argv', ['optimised_code_generator.py', 'sample_programs/programming_assignment_4/Program3.csvlang'])
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
a4 = (a0.sort_values(by=[]).loc[(((a0["sales"] >= 28) & (a0["goods"] == "Paper")) | (a0["sales"] == 5))])
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



    # Testing Sample Program 4
    @patch('sys.argv', ['optimised_code_generator.py', 'sample_programs/programming_assignment_4/Program4.csvlang'])
    def test_sample_program_5(self):
        with patch('sys.stdout', new=io.StringIO()) as mocked_stdout:
            main()

            received_output = mocked_stdout.getvalue()

            expected_output = '''Generated Python Code:

from pathlib import Path
import pandas as pd

batch1 = pd.read_csv("csv_files/matrix.csv", header=None)
batch2 = batch1
a4 = (batch1.sort_values(by=[]))
print(a4.iloc[:, [0, 1]])
print()
a4 = (batch2.sort_values(by=[]))
print(a4.iloc[:, [1]])
print()

CSVLang Output

     0    1
0  1.0  2.0
1  2.3  4.5

     1
0  2.0
1  4.5'''

            self.assertEqual(expected_output, received_output.strip())



if __name__ == '__main__':
    unittest.main()
