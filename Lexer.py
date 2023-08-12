from Token import *
from Error import *

## Developements issues note section
## No isusse currently.

class Lexer:

    """
        This class is used to perfrom lexcical analysis.
    """

    def __init__(self,file , source_code):

        self.code = source_code
        self.index = -1
        self.current_char = None
        self.file = file
        self.next()

    def next(self):

        self.index += 1
        if self.index < len(self.code):
            self.current_char = self.code[self.index]
        else:
            self.current_char = None

    def tokenize_lesser_or_lesserThanEqual(self):

        # Checks wether the given token is < or <= and return the Token.
        self.next()

        if self.current_char == "=":
            self.next()
            return Token(token_lte) , None
        return Token(token_lt) , None

    
    def tokenize_greater_or_greaterThanEqual(self):

        # Checks wether the given token is > or >= and returns the token.
        self.next()

        if self.current_char == "=":
            self.next()
            return Token(token_gte) , None
        return Token(token_gt) , None

    def tokenize_not_or_notEqual(self):

        # Checks wether the given token is ! or != and returns the token.

        self.next()

        if self.current_char == "=":
            self.next()
            return Token(token_ne) , None
        return Token(token_not) , None

    def tokenize_mul_or_power(self):

        # Checks wether the given token is * or ** and returns the token.
        self.next()

        if self.current_char == "*":
            self.next()
            return Token(token_power) , None
        return Token(token_mul) , None
    
    def tokenize_assignment(self):

        #checks wether the given token is : , :+ ,:* or :** and returns the token.
        self.next()

        if self.current_char == "+":
            self.next()
            return Token(token_colon_plus) , None
        elif self.current_char == "*":
            self.next()
            if self.current_char == "*":
                self.next()
                return Token(token_colon_power) , None
        
            return Token(token_colon_mul) , None
        
        elif self.current_char == "-":
            self.next()
            return Token(token_colon_minus) , None
        elif self.current_char == "/":
            self.next()
            return Token(token_colon_divide)  , None
        

        return Token(token_colon) , None

    def tokenize_string(self):

        #Checks wether the given token is a string and return the token.

        string = ""
        self.next()

        while self.current_char != None and self.current_char != '"':
            string += self.current_char
            self.next()
        
        if self.current_char != '"':
            return None , StringError(self.file , f"Expected a '\"' after the string '{string}'.")
            
        self.next()

        return Token(token_string , string) , None


    def tokenize_variable(self):

        #checks wether the given token is a variable and return token.

        variable = ""

        while self.current_char != None and self.current_char in token_letters + token_digit[1:] + '_':
            variable += self.current_char
            self.next()

        if variable in keywords:
            return Token(token_keyword , variable)  , None

        return Token(token_variable , variable) , None

    def tokenize_digit(self):
        
        # checks wether the given token is digit and returns the token.

        number = ""
        if self.current_char == ".":
            self.next()
            return Token(token_dot) , None
        point_count = 0

        while self.current_char != None and self.current_char in token_digit + '.':
            if self.current_char == '.':
                if point_count == 0:
                    point_count += 1
                else:
                    return None 
            number += self.current_char
            self.next()

        if point_count == 0:
            return Token(token_int , int(number)) , None
        return Token(token_float , float(number)) , None

    def tokenize_input_message(self):

        #Checks wether the given input is a input message and returns the token
        message = ""
        self.next()

        while self.current_char != None and self.current_char != "'":
            message += self.current_char
            self.next()
        
        
        if self.current_char != "'":
            return None , InputStringError(self.file , f"Expected a '\'' after the string '{message}'.")
            
        self.next()

        return Token(token_input , message) , None
            


    def tokenize(self):

        # This method return the tokens extracted from the given code.

        tokens = []

        while self.current_char != None:

            if self.current_char in ' \t':
                self.next()

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

            elif self.current_char == "'":
                input_string , error = self.tokenize_input_message()
                if error:
                    return None , error
                tokens.append(input_string)

            elif self.current_char == "(":
                tokens.append(Token(token_lparen))
                self.next()

            elif self.current_char == ")":
                tokens.append(Token(token_rparen))
                self.next()

            elif self.current_char == "{":
                tokens.append(Token(token_lb))
                self.next()

            elif self.current_char == "}":
                tokens.append(Token(token_rb))
                self.next()

            elif self.current_char == "[":
                tokens.append(Token(token_ls))
                self.next()

            elif self.current_char == "]":
                tokens.append(Token(token_rs))
                self.next()

            elif self.current_char == '+':
                tokens.append(Token(token_plus))
                self.next()

            elif self.current_char == "%":
                tokens.append(Token(token_modulo))
                self.next()

            elif self.current_char == ',':
                tokens.append(Token(token_comma))
                self.next()

            elif self.current_char == '-':
                tokens.append(Token(token_minus))
                self.next()

            elif self.current_char == '*':
                operator , error = self.tokenize_mul_or_power()
                if error:
                    return None , error
                tokens.append(operator)

            elif self.current_char == '/':
                tokens.append(Token(token_divide))
                self.next()

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
                tokens.append(Token(token_and , self.current_char))
                self.next()
            elif self.current_char == "|":
                tokens.append(Token(token_or , self.current_char))
                self.next()
            elif self.current_char == '=':
                tokens.append(Token(token_eql))
                self.next()
            else:
                return None , InvalidLiteral(self.file,f"Unexpected Literal '{self.current_char}'.")

        return tokens , None


if __name__ == "__main__":

    while True:
        lexer = Lexer("<Core>",input("Enter a expression : "))
        print(lexer.tokenize())
