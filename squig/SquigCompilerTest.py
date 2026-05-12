import os

from Lexer import Lexer
from Parser import Parser
from Compiler import Compiler


DEBUG_IR_PATH = "./Debug/output.ll"
file = "./test_array.squig"

def run(code):
    lexer = Lexer(file, source_code=code)
    tokens, error = lexer.tokenize()
    if error:
        print(error)
        return

    parser = Parser(tokens, file)
    ast, error = parser.parse()
    if error:
        print(error)
        return
    
    compiler = Compiler()
    compiler.compile(ast)
    module = compiler.module

    os.makedirs("./Debug", exist_ok=True)

    with open(DEBUG_IR_PATH, "w") as f:
        f.write(str(module))

def main():

    while True:
        try:
            code = input("Squig > ").strip()
            if code == "exit":
                break
            if not code:
                continue
            run(code)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()