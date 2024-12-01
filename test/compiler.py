from helper import Types
from Lexer import Lexer
from Parser import Parser

code = """
section .text
    global _start

_start:
    
    mov rdi, 1
    mov rsi, msg
    mov rdx, 14
    mov rax, 1
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall

"""

class SquigCompiler:


    def __init__(self):

        self.assembly = []

    def _complie(self):

        import os , sys

        with open("output.asm" , "w") as asm:
            asm.write(code)

        os.system("nasm -f win64 -o target.o output.asm")
        os.system("gcc -o a.exe target.o -lkernel32")

        os.system("del output.asm target.o")
        

    def process(self , node):
        
        method = getattr(self , f"{type(node).__name__}" , self.no_process)
        return method(node)
    
    def ShowNode(self , node):
        global code
        value , error = self.process(node.statement[0])
        if error:
            return None , error

        code += f"""section .data \n\tmsg db '{value}', 0xA"""

        return None , None
    
    def StringNode(self , node):

        return node.string.value , None
    
    def CollectionNode(self , node):

        elements = []

        for element_node in node.elements:
            element , error = self.process(element_node)
            if error:
                return None , error
            elements.append(element)

        return elements , None
    
    
    def no_process(self , node):
        print(type(node))
        return "no function"
    


if __name__ == "__main__":

    while True:
        lexer = Lexer("",input("Enter a expression :"))
        tokens , error = lexer.tokenize()
    
        if error:
            print(error.print())
            continue
        
        parser = Parser(tokens , "<ProgramFile>")
        result , error = parser.parse()
        if error:
            print(error.print())
            continue
        compiler = SquigCompiler()
        output , error = compiler.process(result)
        if error:
            print(error.print())
            continue

        compiler._complie()