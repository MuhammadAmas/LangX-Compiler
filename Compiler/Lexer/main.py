import os
from dotenv import load_dotenv
from readSourceCode import readSourceCode
from wordBreaker import breakWords

load_dotenv()

input_file_path = os.getenv('INPUT_FILE_PATH')
output_file_path = os.getenv('OUTPUT_FILE_PATH')

input_text = readSourceCode(input_file_path)
print(input_text)
temp = breakWords(input_text)
print(temp)
# classifiedTokens = classifyToken(generatedTokens)
# output_text = generateOuput(classifiedTokens)

# with open(output_file_path, "w") as outputfile:
#     outputfile.write(generateOuput(classifyToken(breakWords(input_text))))