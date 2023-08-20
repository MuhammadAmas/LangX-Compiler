def readSourceCode(input_file_path):
    try:
        with open(input_file_path, 'r') as sourceCode:
            content = sourceCode.read()
            return content
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
        return None
    except IOError:
        print(f"Error: Unable to read the file '{input_file_path}'.")
        return None
