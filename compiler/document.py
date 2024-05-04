import os
import pydoc

def generate_docs(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, directory))[0].replace(os.path.sep, '.')
                pydoc.writedoc(module_name)

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    generate_docs(directory)
