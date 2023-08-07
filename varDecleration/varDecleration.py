file_path = 'F:/LangX-Compiler/varDecleration/input.txt'

try:
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
except IOError:
    print(f"Error: Unable to read the file '{file_path}'.")

