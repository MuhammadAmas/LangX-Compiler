import re
import os
from dotenv import load_dotenv

load_dotenv()

input_file_path = os.getenv('INPUT_FILE_PATH')

output_file_path = os.getenv('OUTPUT_FILE_PATH')

token = []

# try:
#     with open(input_file_path, 'r') as file, open(output_file_path, 'w') as output_file:
#         for line_number, line in enumerate(file, start=1):
#             line = line.strip()  # Remove leading/trailing whitespace
#             if not line:
#                 continue  # Skip empty lines
            
#             pattern = r'^(num|dec|text) ([a-zA-Z_][a-zA-Z0-9_]*) = ([-]?[0-9]|[-]?[0-9]+(\.[0-9]+)?|"[^"]*");$'
            
#             match = re.match(pattern, line)
#             if match:
#                 data_type = match.group(1)
#                 variable_name = match.group(2)
#                 value = match.group(3)
                
#                 if data_type == 'num' and '.' not in value:
#                     output_file.write(f"Line {line_number}:\n")
#                     output_file.write(f"  Data Type: {data_type}\n")
#                     output_file.write(f"  Variable Name: {variable_name}\n")
#                     output_file.write(f"  Value: {value}\n\n")
                
#                 elif data_type == 'dec' and '.' in value:
#                     output_file.write(f"Line {line_number}:\n")
#                     output_file.write(f"  Data Type: {data_type}\n")
#                     output_file.write(f"  Variable Name: {variable_name}\n")
#                     output_file.write(f"  Value: {value}\n\n")
                    
#                 elif data_type == 'text' and '"' in value:
#                     output_file.write(f"Line {line_number}:\n")
#                     output_file.write(f"  Data Type: {data_type}\n")
#                     output_file.write(f"  Variable Name: {variable_name}\n")
#                     output_file.write(f"  Value: {value}\n\n")
#                 else:
#                     output_file.write(f"Line {line_number}: Invalid syntax\n\n")
#                     token.append({"Line {line_number}: Invalid syntax"})
                    
#                 token.append({'line_number': line_number, 'data_type': data_type, 'variable_name': variable_name , 'value': value })
                
#             else:
#                 output_file.write(f"Line {line_number}: Invalid syntax\n\n")
#                 token.append({"Line {line_number}: Invalid syntax"})

# except FileNotFoundError:
#     print(f"Error: File '{input_file_path}' not found.")
# except IOError:
#     print(f"Error: Unable to read the file '{input_file_path}'.")

class token():
    def __init__(self,value,line):
        self.type ="undefined"
        self.value = value
        self.line = line
        
    def displayToken(self):
        showToken = "\t(" + self.type + ", " + self.value + \
            ", " + str(self.line) + ")"
        return showToken
    
def intConst(word):
    pattern = "(^[+|-]?[0-9]+$)"
    matchPattern=pattern.match(pattern,word)
    
    if matchPattern:
        return True
    else:
        return False
    
def floatConst(word):
    pattern = "(^[+|-]?[0-9]*[.][0-9]+$)"
    matchPattern=pattern.match(pattern,word)
    
    if matchPattern:
        return True
    else:
        return False
    
def stringConst(word):
    pattern = "(\"(.*)\")"
    matchPattern=pattern.match(pattern,word)
    
    if matchPattern:
        return True
    else:
        return False
    
def isIdentifier(word):
    pattern = "([a-zA-Z_][a-zA-Z0-9_]*)"
    matchPattern=pattern.match(pattern,word)
    
    if matchPattern:
        return True
    else:
        return False
    
def generateToken(word,line,i):
    currentToken = token(word,line)
    #showToken = str(line) +"\t" + word
    #print(showToken)
    i=i+1
    return "",i,currentToken

def breakToken(word):
    word = ""
    line = 1
    tokenlist = []
    singleBreak = []
    comboBreak = []
    
def classifyToken(tokenlist):
    keywords={}
    operators={}
    punctuators={}
    
def generateOutput(tokens):