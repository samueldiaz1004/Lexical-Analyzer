'''
Samuel Alejandro Diaz del Guante Ochoa - A01637592
Computer Science Advanced Applications Development - TC3002B
Module #3: Compilers
Lexical Analysis
'''

# Import libraries
import pandas as pd
import os

# Set global variables
DIR = (os.path.join(os.path.dirname(__file__)))

transitionTable = pd.read_csv(DIR+'/input/TransitionTable.txt', sep='\t')
validTokens = pd.read_csv(DIR+'/input/ValidTokens.txt', sep='\t')

token_list = []
identifiers_table = []
numbers_table = []
strings_table = []

# Get the current state and map it to the next state from the transition table
# Get current character and state
# Return the next state of the token
def getState(state:int, char:str) -> int:

    blank = "\t "
    new_line = "\n"
    specialChars = "+-*/<>=!;,\".()[]{}"
    alphabet = [chr(value) for value in range(97, 123)]

    if char in blank:
        col = transitionTable['blank']
    elif char in new_line:
        col = transitionTable['new_line']
    elif char.lower() in alphabet:
        col = transitionTable['letter']
    elif char.isdigit():
        col = transitionTable['digit']
    elif char in specialChars:
        col = transitionTable[char]
    else:
        col = transitionTable['bad_char']

    return col.loc[state]

# This function manages errors if a token finalizes in said state
# Get token, final state of token and analyzed  text
# Return text string with modifications
def errorHandler(token:str, state:int) -> None:
    
    # Default message, unrecognizable character
    message = "Token has an unknown character"
    # '!=' was not fully stated
    if token == '!':
        message = "'!' has to be followed by a '='"
    # Number end with a dot
    elif token[-1] == '.':
        message = "Float numbers cannot end by with a '.'"
    # String was not closed
    elif token[0] == '"':
        message = "String was not properly closed"
    # Comment was not closed
    elif token[:2] == '/*':
        message = "Comment was not properly closed"
    # Number contains a letter
    elif token[0].isdigit() and (token.isupper() or token.islower()):
        message = "Numbers cannot contain letters"

    token_list.append([state,message])

# Process token to store in transition table and (if it applies) to one of the symbol tables
# Get token and the ending state to be translated to state found in the ValidToken.txt table
def processToken(token:str, state:int) -> None:

    t = list(validTokens['Token'].values)
    t.insert(0,'')

    # IDs/Keywords
    if state == 19:
        # Lowercase input since IDs/Keywords are NOT case sensitive
        token = token.lower()
        # Keywords
        if token in t:
            s = t.index(token)
            token_list.append([s])
        # IDs
        else:
            # Determine if it is already in the table
            if not token in identifiers_table:
                identifiers_table.append(token)
            s = t.index('ID')
            index = identifiers_table.index(token)+1
            token_list.append([s,index])
    # Numbers
    elif state == 20:
        # Determine the type of the number
        num_type = 'float' if '.' in token else 'int'
        numbers_table.append([token,num_type])
        s = t.index('NUMBER')
        index = len(numbers_table)
        token_list.append([s,index])
    # Strings
    elif state == 30:
        strings_table.append(token)
        s = t.index('STRING')
        index = len(strings_table)
        token_list.append([s,index])
    # Comments
    elif state == 22:
        s = t.index('COMMENT')
        token_list.append([s])
    # Special characters
    elif token in t:
        s = t.index(token)
        token_list.append([s])

# Formats and outputs the different types of tables to a .txt
# Gets the data structure that contains the information of the table 
# (usually contains Entry number and lexeme), file and column names
def outputTables(l:list, fileName:str, col_names:list) -> None:

    table = pd.DataFrame(l, columns=col_names)
    table.insert(0, 'Entry', range(1,len(l)+1))
    table.to_csv(DIR+'/output/'+fileName, sep='\t', index=False)

# Formats and outputs the scanner tokens to a .txt
def outputScanner() -> None:
    
    output = ''

    for item in token_list:
        if len(item) == 1:
            output += '<' + str(item[0]) + '>\n'
        else:
            output += '<' + str(item[0]) + ',' + str(item[1]) + '>\n'

    f = open(DIR+'/output/ScannerOutput.txt', 'w')
    f.write(output)
    f.close()
    
# Main function of the program
# Tokenizes each keyword, special character using a transition table
# Outputs .txt file that each represent tokens, identifiers, numbers and string tables
def scanner(text:str) -> None:

    # Scanner wont do anything if text is empty
    if not len(text): return
    # Add next line char at the end of the input string if file does not already have it to avoid errors while reading file
    text += '\n' if text[-1] != "\n" else ''
    # Flag to stop process if a bad token has been reached
    err = False
    # Process every char in the input file or until an error is detected
    while text and not err:
        # Pop and store the first char in queue
        char = text[0]
        text = text[1:]
        # Try again if the first char of the token is a blank
        if char in "\t\n ":
            continue
        # Store the first char of the token and get its first state
        token = char
        state = getState(0,char)
        # Continue to get next token char and state until it has reached a final state
        while text and state < 19:
            state = getState(state,text[0])
            if state < 19:
                char = text[0]
                text = text[1:]
                token += char
        # Error state
        if state < 19 or state == 43:
            errorHandler(token,37)
            err = True
        # Valid state
        else:
            processToken(token,state)
    # Output scanner and symbol tables contents
    outputScanner()
    outputTables(identifiers_table,'IdentifiersTable.txt',['Lexeme'])
    outputTables(numbers_table,'NumbersTable.txt',['Lexeme', 'Type'])
    outputTables(strings_table,'StringTable.txt',['Lexeme'])

    print("❌ Something went wrong! Check the scanner output to verify the bad token.") if err \
        else print("✅ Looks green to me! Check the scanner output and lexeme tables.")

def main():

    pathToSource = './input/source.txt'
    with open(pathToSource, 'r') as f:
        text = f.read()

    scanner(text)

if __name__ == "__main__":
    main()