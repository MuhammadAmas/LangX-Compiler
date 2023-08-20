import os
from dotenv import load_dotenv
from readSourceCode import readSourceCode
from wordBreaker import breakWords
from classifyToken import classifyToken
from lexer import *
from generateOutput import generateOutput
load_dotenv()

input_file_path = os.getenv('INPUT_FILE_PATH')
output_file_path = os.getenv('OUTPUT_FILE_PATH')

with open(output_file_path, "w") as outputfile:
    outputfile.write(generateOutput(classifyToken(breakWords(readSourceCode(input_file_path)))))