
import os , sys 
from rich.console import Console, Text
from helper.SymbolTable import symbol_table
from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
from pyfiglet import figlet_format
from argparse import ArgumentParser
import time


 
class Squig:

    def execute(self, cli_args):

        file = cli_args.filename[0]
        print(cli_args)
        try:

            if not file.endswith(".squig"):
                print(f"File : '{file[:file.find('.')]}' is not a squig file.")
            
            code = open(file).read().strip()
            
            if not code:
                print("Please provide a script to execute.")
                sys.exit(1)
            
        except FileNotFoundError:
            print(f"\tInvalid file {file} , check is that a squig file\n")
            sys.exit()

        except KeyboardInterrupt:
            print("Type 'exit' to close the console.")
        
        try:

                
            lexer = Lexer(file , code)
            tokens , error = lexer.tokenize()
            if error:
                print(error.print())
                sys.exit(1)
            
            parser = Parser(tokens , file)
            ast , error = parser.parse()            
            if error:
                print(error.print())
                sys.exit(1)

            
            if ast and not ast.elements:
                sys.exit(1)

            
            interpreter = Interpreter(file , symbol_table)
            result , error = interpreter.process(ast)
            if error:
                print(error.print())
                sys.exit(1)
                
            
            if result:
                for output in result.elements:
                    
                    if type(output).__name__ == "Collection" and output and output.elements and output.elements[0] == None:

                        if len(output.elements) == 1:#and type(output).__name__ != 'Collection':
                            continue

                        elif len(output.elements) != 1:
                            if output.elements[-1]:
                                print(output.elements[-1].elements)

        except KeyboardInterrupt: 
            sys.exit(1)

    def terminal_text(self, ascii_text):

        console = Console()

        chrome = ["#ffffff", "#d9d9d9", "#a6a6a6", "#737373", "#00e5ff"]

        text = Text()

        lines = ascii_text.splitlines()

        for y, line in enumerate(lines):
            base_color = chrome[min(y * len(chrome) // len(lines), len(chrome)-2)]

            for x, ch in enumerate(line):
                if ch != " " and x % 12 == 0:
                    text.append(ch, style="bold #00e5ff")  # cinematic glow points
                else:
                    text.append(ch, style=f"bold {base_color}")

            text.append("\n")


        console.print(text)

    def shell(self):

        # print(figlet_format("Squig" , font="cybermedium",))
        # fonts = [
            
        #     "ascii12",
           
        #     "basic",
         
        #     "bigascii12",
         
        #     "broadway",
           
        #     "calgphy2",
        #     "caligraphy",
            
        #     "chunky",
        #     "clb6x10",
        #     "clb8x10",
        #     "clb8x8",
        #     "cli8x8",
        #     "clr4x6",
        #     "clr5x10",
        #     "clr5x6",
        #     "clr5x8",
        #     "clr6x10",
        #     "clr6x6",
        #     "clr6x8",
        #     "clr7x10",
        #     "clr7x8",
        #     "clr8x10",
        #     "clr8x8",
        #     "coil_cop",
        #     "coinstak",
        #     "cola",
        #     "colossal",
        #     "com_sen_",
        #     "computer",
        #     "contessa",
         
        #     "doh",
        #     "doom",

        #     "double",
            
        #     "epic",
        
           
        #     "georgia11",
        
        #     "graffiti",
        
        #     "henry_3d",
          
        #     "hollywood",
            
        #     "italic",

        #     "jacky",
            
        #     "mini",
        
        #     "pebbles",
        #     "pepper",
           
        #     "poison",
            
        #     "red_phoenix",
          
        #     "roman",
           
        #     "rounded",
          
        #     "santa_clara",
            
        #     "shimrod", 
            
        #     "small_shadow", 
        #     "small_slant", 
        #     "standard", 
        #     "starwars", 
        #     "swan", 
        #     "tinker-toy",
        #     "univers",
        
        #     "varsity",
        #     "vortron_",
        #     "wavy",

        # ]
        
        self.terminal_text(figlet_format("Squig"))

        print("\n\tNote: If you happen to find any bugs, kindly report them to us on GitHub: https://github.com/Harish-M-2003/Squig")
        print()

        file = "<main>"

        while True:
 
            try:
            
                code = input("~  ")  
                
                if not code: 
                    continue  

                if code == 'exit':
                    break

                elif code in ('cls' , 'clear'):
                    os.system("cls")
                    self.terminal_text(figlet_format("Squig"))
                    print("\n\tNote: If you happen to find any bugs, kindly report them to us on GitHub: https://github.com/Harish-M-2003/Squig")
                    print()

                    continue

                lexer = Lexer(file , code)
                tokens , error = lexer.tokenize()

                if error:
                    print(error.print())
                    
                parser = Parser(tokens , file)
                ast , error = parser.parse()
                
                if error:
                    print(error.print())
                    
                if ast and not ast.elements:
                    break

                interpreter = Interpreter(file , symbol_table)
                result , error = interpreter.process(ast)
                
                if error:
                    print(error.print())
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


    def run(self):

        cli = ArgumentParser(description="Squig Shell")

        sub_parser = cli.add_subparsers(title="Commands", dest="command")

        idx = sub_parser.add_parser("run", help='Executes Squig Scripts')
        idx.add_argument("filename", nargs="+")

        
        idx = sub_parser.add_parser("shell", help='Open Squig Shell')

        cli.add_argument("-v", "-version", help="Display the current version of squig")

        cli_args = cli.parse_args()

        match cli_args.command:
            case "run":
                self.execute(cli_args)
            case "shell":
                self.shell()
            case _:
                cli.print_help()


if __name__ == '__main__':

    Squig().run()