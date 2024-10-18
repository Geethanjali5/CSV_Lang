import argparse
import sys


# states in the DFA (in order of priority as per the lexical specification rules)
token_classes = {
    "KEYWORD": "keyword", # reserved words
    "LITERAL": "literal", # true, false
    "NUMBER": "number", # any whole number
    "OPERATOR": "operator", # +,-,*,/,%,=,&,|,<,>,<=,>=,<>
    "SEPARATOR": "separator", # ( ) , ;
    "STRING": "string", # any valid string
}

def is_keyword(lexeme):
    keywords = ["LOAD", "CREATE", "ADD", "REMOVE", "DELETE", "DISPLAY", "STORE", "MERGE", "AVERAGE", "SUM",
                "MAX", "MIN", "COUNT", "PRINT", "save", "num", "sort", "filter", "tag", "path", "header"]
    return lexeme in keywords

def is_literal(lexeme):
    literals = ["true", "false"]
    return lexeme in literals

def is_operator(char):
    return char in "+-*/%=&|<>"

def is_separator(char):
    return char in "(),;"

def is_digit(char):
    return '0' <= char <= '9'

def is_letter(char):
    return char.isalpha()

def scanner(program):
    i = 0
    length = len(program)
    tokens = []
    errors = []

    while i < length:
        current_char = program[i]

        # Skip whitespace
        if current_char.isspace():
            i += 1
            continue

        # Check for keyword / literal
        if is_letter(current_char):
            lexeme = current_char
            i += 1

            # State transitions
            while i < length and is_letter(program[i]):
                lexeme += program[i]
                i += 1
            if is_keyword(lexeme):
                tokens.append((token_classes["KEYWORD"], lexeme)) # accepting state
            elif is_literal(lexeme):
                tokens.append((token_classes["LITERAL"], lexeme)) # accepting state
            else:
                errors.append(f"Invalid keyword or literal: {lexeme}")

        # Check for number
        elif is_digit(current_char):
            lexeme = current_char
            i += 1

            # State transitions
            while i < length and is_digit(program[i]):
                lexeme += program[i]
                i += 1

            # Check for leading zeros
            if lexeme != "0" and lexeme[0] == '0':
                errors.append(f"Invalid number with leading zero(s): {lexeme}")
            else:
                tokens.append((token_classes["NUMBER"], lexeme))  # accepting state

        # Check for operator
        elif is_operator(current_char):
            lexeme = current_char
            i += 1

            if i < length and current_char == '<' and program[i] == '>': # checking for <>
                lexeme += program[i]
                i += 1
                tokens.append((token_classes["OPERATOR"], lexeme))  # accepting state
            elif i < length and ((current_char == '<' and program[i] == '=') or (current_char == '>' and program[i] == '=')): # checking for <= or >=
                lexeme += program[i]
                i += 1
                tokens.append((token_classes["OPERATOR"], lexeme))  # accepting state
            else:
                tokens.append((token_classes["OPERATOR"], lexeme)) # accepting state

        # Check for separator
        elif is_separator(current_char):
            tokens.append((token_classes["SEPARATOR"], current_char)) # accepting state
            i += 1

        # Check for string
        elif current_char == '"':
            lexeme = current_char
            i += 1

            # State transitions
            while i < length and program[i] != '"':
                lexeme += program[i]
                i += 1
            if i < length:
                lexeme += '"'
                tokens.append((token_classes["STRING"], lexeme)) # accepting state
                i += 1
            else:
                errors.append(f"Unclosed string: {lexeme}")

        # Handle unrecognized character
        else:
            errors.append(f"Unrecognized character: {current_char}")
            i += 1

    return tokens, errors

def main():
    parser = argparse.ArgumentParser(description = "Lexer for CSV Lang")
    parser.add_argument("file", help = "Path to the CSV Lang source code")

    args = parser.parse_args()

    # Read the file
    try:
        with open(args.file, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: File {args.file} not found.")
        sys.exit(1)

    tokens, errors = scanner(source_code)

    if len(tokens) > 0:
        print("\nTOKENS")
    else:
        print("No tokens found.")

    # Print tokens
    for token in tokens:
        print(f"< {token[0]}, {token[1]} >")
    print("")

    # Print errors
    if errors:
        print("ERRORS")
        for error in errors:
            print(error)
        print("")


if __name__ == "__main__":
    main()