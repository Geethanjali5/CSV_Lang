import sys
sys.path.append(sys.path[0] + '/../..')
from scanner import scanner


def test_scanner():
    # Test case 1: Sample Program 1
    program1 = '''
    LOAD ("../csv_files/student_scores.csv", header = true);
    DISPLAY ("name", "score", num=2, header = true);
    STORE ("name", "score", num=2, header = true, path = "../csv_files/student_scores_new.csv");
    PRINT ("The average score: ", AVERAGE("score"));
    '''

    tokens, errors = scanner(program1)
    expected_tokens = [('keyword', 'LOAD'), ('separator', '('), ('string', '"../csv_files/student_scores.csv"'),
                       ('separator', ','), ('keyword', 'header'), ('operator', '='), ('literal', 'true'),
                       ('separator', ')'), ('separator', ';'), ('keyword', 'DISPLAY'), ('separator', '('),
                       ('string', '"name"'), ('separator', ','), ('string', '"score"'), ('separator', ','),
                       ('keyword', 'num'), ('operator', '='), ('number', '2'), ('separator', ','),
                       ('keyword', 'header'), ('operator', '='), ('literal', 'true'), ('separator', ')'),
                       ('separator', ';'), ('keyword', 'STORE'), ('separator', '('), ('string', '"name"'),
                       ('separator', ','), ('string', '"score"'), ('separator', ','), ('keyword', 'num'),
                       ('operator', '='), ('number', '2'), ('separator', ','), ('keyword', 'header'), ('operator', '='),
                       ('literal', 'true'), ('separator', ','), ('keyword', 'path'), ('operator', '='),
                       ('string', '"../csv_files/student_scores_new.csv"'), ('separator', ')'), ('separator', ';'),
                       ('keyword', 'PRINT'), ('separator', '('), ('string', '"The average score: "'),
                       ('separator', ','), ('keyword', 'AVERAGE'), ('separator', '('), ('string', '"score"'),
                       ('separator', ')'), ('separator', ')'), ('separator', ';')]
    expected_errors = []

    assert tokens == expected_tokens, "Test case 1 failed"
    assert errors == expected_errors, "Test case 1 failed"

    # Test case 2: Sample Program 2
    program2 = '''
    LOAD ("../csv_files/sales.csv", header = true, tag = "batch1");
    LOAD ("../csv_files/sales1.csv", header = true, tag = "batch2");
    
    MERGE ("batch1", "batch2", save = true, path = "../csv_files/combined_sales.csv");
    
    PRINT ("The total sales of batch 1: ", SUM("sales"), tag = "batch1");
    PRINT ("The total sales of batch 2: ", SUM("sales"), tag = "batch2");
    '''

    tokens, errors = scanner(program2)
    expected_tokens = [('keyword', 'LOAD'), ('separator', '('), ('string', '"../csv_files/sales.csv"'),
                       ('separator', ','), ('keyword', 'header'), ('operator', '='), ('literal', 'true'),
                       ('separator', ','), ('keyword', 'tag'), ('operator', '='), ('string', '"batch1"'),
                       ('separator', ')'), ('separator', ';'), ('keyword', 'LOAD'), ('separator', '('),
                       ('string', '"../csv_files/sales1.csv"'), ('separator', ','), ('keyword', 'header'),
                       ('operator', '='), ('literal', 'true'), ('separator', ','), ('keyword', 'tag'),
                       ('operator', '='), ('string', '"batch2"'), ('separator', ')'), ('separator', ';'),
                       ('keyword', 'MERGE'), ('separator', '('), ('string', '"batch1"'), ('separator', ','),
                       ('string', '"batch2"'), ('separator', ','), ('keyword', 'save'), ('operator', '='),
                       ('literal', 'true'), ('separator', ','), ('keyword', 'path'), ('operator', '='),
                       ('string', '"../csv_files/combined_sales.csv"'), ('separator', ')'), ('separator', ';'),
                       ('keyword', 'PRINT'), ('separator', '('), ('string', '"The total sales of batch 1: "'),
                       ('separator', ','), ('keyword', 'SUM'), ('separator', '('), ('string', '"sales"'),
                       ('separator', ')'), ('separator', ','), ('keyword', 'tag'), ('operator', '='),
                       ('string', '"batch1"'), ('separator', ')'), ('separator', ';'), ('keyword', 'PRINT'),
                       ('separator', '('), ('string', '"The total sales of batch 2: "'), ('separator', ','),
                       ('keyword', 'SUM'), ('separator', '('), ('string', '"sales"'), ('separator', ')'),
                       ('separator', ','), ('keyword', 'tag'), ('operator', '='), ('string', '"batch2"'),
                       ('separator', ')'), ('separator', ';')]
    expected_errors = []

    assert tokens == expected_tokens, "Test case 2 failed"
    assert errors == expected_errors, "Test case 2 failed"

    # Test case 3: Sample Program 3
    program3 = '''
    LOAD ("../csv_files/sales.csv", header = true);

    DISPLAY ("goods", "sales", num = 02, header = true, sort = ("goods"));
    DISPLAY ("goods", "sales", header = true, filter = ("sales" >= 10 & "goods" = "Paper"));
    
    PRINT ("The maximum sales: ", MAXIMUM("sales"));@
    PRINT ("The minimum sales: ", MIN("sales"));
    PRINT ("The total number of goods: ", COUNT("goods));'''

    tokens, errors = scanner(program3)
    expected_tokens = [('keyword', 'LOAD'), ('separator', '('), ('string', '"../csv_files/sales.csv"'),
                       ('separator', ','), ('keyword', 'header'), ('operator', '='), ('literal', 'true'),
                       ('separator', ')'), ('separator', ';'), ('keyword', 'DISPLAY'), ('separator', '('),
                       ('string', '"goods"'), ('separator', ','), ('string', '"sales"'), ('separator', ','),
                       ('keyword', 'num'), ('operator', '='), ('separator', ','), ('keyword', 'header'),
                       ('operator', '='), ('literal', 'true'), ('separator', ','), ('keyword', 'sort'),
                       ('operator', '='), ('separator', '('), ('string', '"goods"'), ('separator', ')'),
                       ('separator', ')'), ('separator', ';'), ('keyword', 'DISPLAY'), ('separator', '('),
                       ('string', '"goods"'), ('separator', ','), ('string', '"sales"'), ('separator', ','),
                       ('keyword', 'header'), ('operator', '='), ('literal', 'true'), ('separator', ','),
                       ('keyword', 'filter'), ('operator', '='), ('separator', '('), ('string', '"sales"'),
                       ('operator', '>='), ('number', '10'), ('operator', '&'), ('string', '"goods"'),
                       ('operator', '='), ('string', '"Paper"'), ('separator', ')'), ('separator', ')'),
                       ('separator', ';'), ('keyword', 'PRINT'), ('separator', '('),
                       ('string', '"The maximum sales: "'), ('separator', ','), ('separator', '('),
                       ('string', '"sales"'), ('separator', ')'), ('separator', ')'), ('separator', ';'),
                       ('keyword', 'PRINT'), ('separator', '('), ('string', '"The minimum sales: "'),
                       ('separator', ','), ('keyword', 'MIN'), ('separator', '('), ('string', '"sales"'),
                       ('separator', ')'), ('separator', ')'), ('separator', ';'), ('keyword', 'PRINT'),
                       ('separator', '('), ('string', '"The total number of goods: "'), ('separator', ','),
                       ('keyword', 'COUNT'), ('separator', '(')]
    expected_errors = ['Invalid number with leading zero(s): 02', 'Invalid keyword or literal: MAXIMUM',
                       'Unrecognized character: @', 'Unclosed string: "goods));']

    assert tokens == expected_tokens, "Test case 3 failed"
    assert errors == expected_errors, "Test case 3 failed"

    # Test case 4: Sample Program 4
    program4 = '''
    LOAD ("../csv_files/sales.csv", header = true, tag = "sales");

    DELETE (tag = "sales");
    
    CREATE ("../csv_files/sales.csv");
    ADD (("goods", "date", "sales"), ("Paper", "10-14-2024", "100"), ("Pen", "10-13-2024", "86"));
    DISPLAY ("goods", "sales" + 10, header = True);
    '''

    tokens, errors = scanner(program4)
    expected_tokens = [('keyword', 'LOAD'), ('separator', '('), ('string', '"../csv_files/sales.csv"'),
                       ('separator', ','), ('keyword', 'header'), ('operator', '='), ('literal', 'true'),
                       ('separator', ','), ('keyword', 'tag'), ('operator', '='), ('string', '"sales"'),
                       ('separator', ')'), ('separator', ';'), ('keyword', 'DELETE'), ('separator', '('),
                       ('keyword', 'tag'), ('operator', '='), ('string', '"sales"'), ('separator', ')'),
                       ('separator', ';'), ('keyword', 'CREATE'), ('separator', '('),
                       ('string', '"../csv_files/sales.csv"'), ('separator', ')'), ('separator', ';'),
                       ('keyword', 'ADD'), ('separator', '('), ('separator', '('), ('string', '"goods"'),
                       ('separator', ','), ('string', '"date"'), ('separator', ','), ('string', '"sales"'),
                       ('separator', ')'), ('separator', ','), ('separator', '('), ('string', '"Paper"'),
                       ('separator', ','), ('string', '"10-14-2024"'), ('separator', ','), ('string', '"100"'),
                       ('separator', ')'), ('separator', ','), ('separator', '('), ('string', '"Pen"'),
                       ('separator', ','), ('string', '"10-13-2024"'), ('separator', ','), ('string', '"86"'),
                       ('separator', ')'), ('separator', ')'), ('separator', ';'), ('keyword', 'DISPLAY'),
                       ('separator', '('), ('string', '"goods"'), ('separator', ','), ('string', '"sales"'),
                       ('operator', '+'), ('number', '10'), ('separator', ','), ('keyword', 'header'),
                       ('operator', '='), ('separator', ')'), ('separator', ';')]
    expected_errors = ['Invalid keyword or literal: True']

    assert tokens == expected_tokens, "Test case 4 failed"
    assert errors == expected_errors, "Test case 4 failed"

    # Test case 5: Mixed operators and keywords
    program5 = '''
    LOAD ("../csv_files/matrix.csv", header = false);

    REMOVE (("22", "10.2", "45"));
    DISPLAY (1, 2, 3, header = false);
    '''

    tokens, errors = scanner(program5)
    expected_tokens = [('keyword', 'LOAD'), ('separator', '('), ('string', '"../csv_files/matrix.csv"'),
                       ('separator', ','), ('keyword', 'header'), ('operator', '='), ('literal', 'false'),
                       ('separator', ')'), ('separator', ';'), ('keyword', 'REMOVE'), ('separator', '('),
                       ('separator', '('), ('string', '"22"'), ('separator', ','), ('string', '"10.2"'),
                       ('separator', ','), ('string', '"45"'), ('separator', ')'), ('separator', ')'),
                       ('separator', ';'), ('keyword', 'DISPLAY'), ('separator', '('), ('number', '1'),
                       ('separator', ','), ('number', '2'), ('separator', ','), ('number', '3'), ('separator', ','),
                       ('keyword', 'header'), ('operator', '='), ('literal', 'false'), ('separator', ')'),
                       ('separator', ';')]
    expected_errors = []

    assert tokens == expected_tokens, "Test case 5 failed"
    assert errors == expected_errors, "Test case 5 failed"

    print("All tests passed!")


if __name__ == "__main__":
    test_scanner()
