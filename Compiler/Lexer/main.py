import os
from dotenv import load_dotenv

from readSourceCode import readSourceCode
from wordBreaker import breakWords
from classifyToken import classifyToken
from generateOutput import generateOutput

load_dotenv()

input_file_path = os.getenv('INPUT_FILE_PATH')
output_file_path = os.getenv('OUTPUT_FILE_PATH')

sourceCode = readSourceCode(input_file_path)

breakedWords = breakWords(sourceCode)

print(breakedWords[1].value, breakedWords[1].type, breakedWords[1].line)

classifiedToken = classifyToken(breakedWords)

with open(output_file_path, "w") as outputfile:
    outputfile.write(generateOutput(classifiedToken))