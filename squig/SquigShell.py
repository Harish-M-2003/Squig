
import os , sys 
from helper.SymbolTable import symbol_table
from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
from pyfiglet import figlet_format

#  rewrite this program to support handling interrupts

print("\n\tNote: If you happen to find any bugs, kindly report them to us on GitHub: https://github.com/Harish-M-2003/Squig")
print()

file = sys.argv[-1]

if len(sys.argv) == 1:
    print(figlet_format("Squig" , font="cybermedium"))

while True:
        try:

            if len(sys.argv) > 1:

                if not file.endswith(".squig"):
                    print(f"File : '{file[:file.find('.')]}' is not a squig file.")
                    break
                
                code = open(file).read().strip()
                
                if not code: break

            else:
                try:
                    code = open(r"C:\Users\Harish\harish\Projects\language\test\testing_final.squig").read() # debugging
                    # code = input("squig >") 
                    code = code.strip()
                except EOFError:
                    break
            
        except FileNotFoundError:
            print(f"\tInvalid file {file} , check is that a squig file\n")
            sys.exit()

        except KeyboardInterrupt:
            print("Type 'exit' to close the console.")
            break

        if code == 'exit':
            break
        elif code in ('cls' , 'clear'):
            os.system("cls")
            continue

        if not code: continue

        lexer = Lexer(file , code)
        tokens , error = lexer.tokenize()

        if error:
            print(error.print())
            if len(sys.argv) > 1:
                break
        try:
            # try :
            parser = Parser(tokens , file)
            ast , error = parser.parse()
            # except Exception:
            #     print("Squig : \nSomething went wrong while trying to parse your code , kindly raise an issue in github , attach the code that caused this error in the issue.")
            #     break
            
            if error:
                print(error.print())
                if len(sys.argv) > 1:
                    break
                continue
            
            if ast and not ast.elements:
                break

            # try:
            interpreter = Interpreter(file , symbol_table)
            result , error = interpreter.process(ast)
            # except Exception:
            #     print("\tSquig : \n\t\tSomething went wrong while trying to interpret your code , kindly raise an issue in github ,  attach the code that caused this error in the issue.")
            #     break
            if error:
                print(error.print())
                if len(sys.argv) > 1:
                    break
                continue
                
            
            if result:
                for output in result.elements:
                    
                    if type(output).__name__ == "Collection" and output and output.elements and output.elements[0] == None:

                        if len(output.elements) == 1:#and type(output).__name__ != 'Collection':
                            continue

                        elif len(output.elements) != 1:
                            if output.elements[-1]:
                                print(output.elements[-1].elements)

        except KeyboardInterrupt: 
            break

        if len(sys.argv) > 1:
            break