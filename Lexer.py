from Token import *
from Error import *
from Position import *

## Developements issues note section
## No isusse currently.

class Lexer:

    """
        This class is used to perfrom lexcical analysis.
    """

    def __init__(self,file , source_code):

        self.code = source_code
        self.position = Position(line_number=-1 , column_number=-1 , index=-1 , file_name=file)
        self.current_char = None
        self.file = file
        self.next()

    def next(self):

        self.position.next(self.current_char)
        if self.position.index < len(self.code):
            self.current_char = self.code[self.position.index]
        else:
            self.current_char = None

    def tokenize_lesser_or_lesserThanEqual(self):

        # Checks wether the given token is < or <= and return the Token.
        self.next()
        if self.current_char == "<":
            
            self.next()
            if self.current_char == "<":
                self.next() 
                return Token(token_writetofile , token_position=self.position.copy_position()) , None
           
            else:
                return None , InvalidLiteral(file=self.file , details="Invalid operator" , position=None)
            

        if self.current_char == "=":
            self.next()
            return Token(token_lte , token_position=self.position.copy_position()) , None
        return Token(token_lt , token_position=self.position.copy_position()) , None

    
    def tokenize_greater_or_greaterThanEqual(self):

        # Checks wether the given token is > or >= and returns the token.
        self.next()

        if self.current_char == "=":
            self.next()
            return Token(token_gte,token_position=self.position.copy_position()) , None
        return Token(token_gt,token_position=self.position.copy_position()) , None

    def tokenize_not_or_notEqual(self):

        # Checks wether the given token is ! or != and returns the token.

        self.next()

        if self.current_char == "=":
            self.next()
            return Token(token_ne,token_position=self.position.copy_position()) , None
        return Token(token_not,token_position=self.position.copy_position()) , None

    def tokenize_mul_or_power(self):

        # Checks wether the given token is * or ** and returns the token.
        self.next()

        if self.current_char == "*":
            self.next()
            return Token(token_power,token_position=self.position.copy_position()) , None
        return Token(token_mul,token_position=self.position.copy_position()) , None
    
    def tokenize_assignment(self):

        #checks wether the given token is : , :+ ,:* or :** and returns the token.
        self.next()

        if self.current_char == "+":
            self.next()
            return Token(token_colon_plus,token_position=self.position.copy_position()) , None
        elif self.current_char == "*":
            self.next()
            if self.current_char == "*":
                self.next()
                return Token(token_colon_power,token_position=self.position.copy_position()) , None
        
            return Token(token_colon_mul,token_position=self.position.copy_position()) , None
        
        elif self.current_char == "-":
            self.next()
            return Token(token_colon_minus,token_position=self.position.copy_position()) , None
        elif self.current_char == "/":
            self.next()
            return Token(token_colon_divide,token_position=self.position.copy_position())  , None
        

        return Token(token_colon,token_position=self.position.copy_position()) , None

    def tokenize_string(self):

        # Checks wether the given token is a string and return the token.

        string = ""
        isMutString = False
        self.next()

        while self.current_char != None and (self.current_char != '"' and self.current_char != '`'):
            string += self.current_char
            self.next()

        if self.current_char not in '"`':
            return None , StringError(self.file , f"Expected a '\"' after the string '{string}'.")
        
        if self.current_char == '`':
            isMutString = True
            
        self.next()
        if not isMutString:
            return Token(token_string , string,token_position=self.position.copy_position()) , None
        else:
            return Token(token_mutstring , string , token_position=self.position.copy_position()) , None


    def tokenize_variable(self):

        # checks wether the given token is a variable and return token.

        variable = ""

        while self.current_char != None and self.current_char in token_letters + token_digit[1:] + '_':
            variable += self.current_char
            self.next()

        if variable in keywords:
            return Token(token_keyword , variable,token_position=self.position.copy_position())  , None

        return Token(token_variable , variable,token_position=self.position.copy_position()) , None

    def tokenize_digit(self):
        
        # checks wether the given token is digit and returns the token.

        number = ""
        if self.current_char == ".":
            self.next()
            return Token(token_dot,token_position=self.position.copy_position()) , None
        point_count = 0

        while self.current_char != None and self.current_char in token_digit + '.':
            if self.current_char == '.':
                if point_count == 0:
                    point_count += 1
                else:
                    return None 
            number += self.current_char
            self.next()

        if len(number) > 1 and number.startswith("0") and "." not in number:
            return None , InvalidLiteral(self.file , "Number cannot have leading zeros." , self.position.copy_position())
        if point_count == 0:
            return Token(token_int , int(number),token_position=self.position.copy_position()) , None
        return Token(token_float , float(number),token_position=self.position.copy_position()) , None

    def tokenize_input_message(self):

        # Checks wether the given input is a input message and returns the token
        message = ""
        self.next()

        while self.current_char != None and self.current_char != "'":
            message += self.current_char
            self.next()
        
        
        if self.current_char != "'":
            return None , InputStringError(self.file , f"Expected a '\'' after the string '{message}'.")
            
        self.next()

        return Token(token_input , message,token_position=self.position.copy_position()) , None
            


    def tokenize(self):

        # This method return the tokens extracted from the given code.

        tokens = []

        while self.current_char != None:

            if self.current_char in ' \t\n;':
                self.next()

            # elif self.current_char in ';\n':
                # tokens.append(Token(token_type=token_newline , token_position=self.position.copy_position()))
                # self.next()

            elif self.current_char == '"':
                string , error = self.tokenize_string()
                if error:
                    return None , error
                tokens.append(string)

            elif self.current_char in token_digit:
                digit , error = self.tokenize_digit()
                if error:
                    return None , error
                tokens.append(digit)
            
            elif self.current_char == "#":
                self.next()
                while self.current_char != '\n' and self.position.index < len(self.code):
                    self.next()
                

            elif self.current_char == "'":
                input_string , error = self.tokenize_input_message()
                if error:
                    return None , error
                tokens.append(input_string)
            
            elif self.current_char == "@":
                tokens.append(Token(token_at , token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == "(":
                tokens.append(Token(token_lparen,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == ")":
                tokens.append(Token(token_rparen,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == "{":
                tokens.append(Token(token_lb,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == "}":
                tokens.append(Token(token_rb,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == "[":
                tokens.append(Token(token_ls,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == "]":
                tokens.append(Token(token_rs,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == '+':
                tokens.append(Token(token_plus,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == "%":
                tokens.append(Token(token_modulo,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == ',':
                tokens.append(Token(token_comma,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == '-':
                tokens.append(Token(token_minus,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == '*':
                operator , error = self.tokenize_mul_or_power()
                if error:
                    return None , error
                tokens.append(operator)

            elif self.current_char == '/':
                tokens.append(Token(token_divide,token_position=self.position.copy_position()))
                self.next()
                if self.current_char == '/':
                    return None , InvalidLiteral(self.file,f"Unexpected Literal '//'.", position = self.position.copy_position() )


            elif self.current_char == '<':
                operator , error = self.tokenize_lesser_or_lesserThanEqual()
                if error:
                    return None , error
                tokens.append(operator)

            elif self.current_char == '>':
                operator , error = self.tokenize_greater_or_greaterThanEqual()
                if error:
                    return None , error
                tokens.append(operator)

            elif self.current_char == '!':
                operator , error = self.tokenize_not_or_notEqual()
                if error:
                    return None , error
                tokens.append(operator)
                
            elif self.current_char in token_letters:
                operator , error = self.tokenize_variable()
                if error:
                    return None , error
                tokens.append(operator)

            elif self.current_char == ':':
                operator , error = self.tokenize_assignment()
                if error:
                    return None , error
                tokens.append(operator)
                
            elif self.current_char == "&":
                tokens.append(Token(token_and , self.current_char,token_position=self.position.copy_position()))
                self.next()

            elif self.current_char == "|":
                tokens.append(Token(token_or , self.current_char,token_position=self.position.copy_position()))
                self.next()
                
            elif self.current_char == '=':
                tokens.append(Token(token_eql,token_position=self.position.copy_position()))
                self.next()
                if self.current_char == "=":
                    return None , InvalidLiteral(self.file,f"Unexpected Literal '{self.current_char}='.", position = self.position.copy_position() )

            elif self.current_char == '`':
                
                string , error = self.tokenize_string()
                if error:
                    return None , error
                tokens.append(string)
            else:
                return None , InvalidLiteral(self.file,f"Unexpected Literal '{self.current_char}'.", position = self.position.copy_position() )
        
        tokens.append(Token(token_eof , token_position=self.position.copy_position()))
        return tokens , None


if __name__ == "__main__":

    while True:
        lexer = Lexer("<core>",input("Enter a expression : "))
        tokens = lexer.tokenize()
        print(tokens)
            

