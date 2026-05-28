import os
import time

from Lexer import Lexer
from Parser import Parser
from Compiler import Compiler

DEBUG_IR_PATH = "./Debug/output.ll"
DEBUG_AST_PATH = "./Debug/ast.txt"
file = r'\test\compilerTest.squig'

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
    
    with open(DEBUG_AST_PATH, "w") as f:
        f.write(str(ast))

    compiler = Compiler()
    compiler.compile(ast)
    module = compiler.module

    os.makedirs("./Debug", exist_ok=True)

    with open(DEBUG_IR_PATH, "w") as f:
        f.write(str(module))

def main():
    if os.path.exists(file):
        try:
            code = open(file).read().strip()
            if not code:
                print("Empty file.")
                return

            start = time.perf_counter()
            run(code)
            end = time.perf_counter()

            print(f"\nProgram executed successfully in {(end - start):.4f}s")

        except FileNotFoundError:
            print(f"File not found: {file}")

        except KeyboardInterrupt:
            print("Stopped.")

    else:
        while True:
            try:
                code = input("Squig > ").strip()
                if code == "exit":
                    break

                if not code:
                    continue
                run(code)

            except KeyboardInterrupt:
                print("\nStopped.")
                break

            except EOFError:
                break

if __name__ == "__main__":
    main()