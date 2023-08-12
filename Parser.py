from Lexer import *
import numpy as np
from Error import *

class NumberNode:

    def __init__(self,factor):

        self.factor = factor

    def __repr__(self):

        return f"{self.factor.value}"
    


class StringNode:

    def __init__(self,string):

        self.string = string

    def __repr__(self):

        return f'"{self.string.value}"'

class InputStringNode:

    def __init__(self,string):

        self.string = string

    def __repr__(self):

        return f"{self.string.value}"

class BinaryOperatorNode:

    def __init__(self,left , operator , right):

        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):

        return f"({self.left},{self.operator},{self.right})"

class AssignmentOperatorNode(BinaryOperatorNode):

    pass

class VariableNode:

    def __init__(self,variable , factor):

        self.variable = variable
        self.factor = factor

    def __repr__(self):

        return f"{self.variable} : {self.factor}"

class VariableAccessNode:

    def __init__(self,variable):

        self.variable = variable

    def __repr__(self):

        return f"{self.variable.value}"
        

class UnaryOperatorNode:

    def __init__(self , operator , factor):

        self.operator = operator
        self.factor = factor

    def __repr__(self):

        return f"{'-' if self.operator.type == token_minus else None}{self.factor.factor.value}"

class IfNode:

    def __init__(self , cases , else_case):

        self.cases = cases
        self.else_case = else_case

    def __repr__(self):

        return f"{self.cases} , {self.else_case}"

class CollectionNode:

    def __init__(self , elements):

        self.elements = elements

    def __repr__(self):

        return f"{self.elements}".replace(')','}').replace('(','{')



class CollectionAccessNode:

    def __init__(self , variable , index):

        self.variable = variable
        self.index = index

    def __repr__(self):

        return f"{self.variable}:{self.index}"


class StringAccessNode:

    def __init__(self,string , indexs):

        self.string = string
        self.indexs = indexs

class DeleteNode:

    def __init__(self,variable):

        self.variable = variable

    def __repr__(self):

        return f"DeleteNode({self.variable})"

class ForNode:

    def __init__(self,variable , start , end , step , body , multi_value):

        self.variable = variable
        self.start_value = start
        self.end_value = end
        self.step_value = step
        self.body = body
        self.multi_value = multi_value

    def __repr__(self):

        return f"ForNode({self.variable},{self.start_value},{self.end_value},{self.step_value},{self.body})"
    
class FunctionNode:

    def __init__(self , variable , param , body):

        self.variable = variable
        self.param = param
        self.body = body

    def __repr__(self):

        return f"FunctionNode({self.variable} , {self.param} , {self.body})"


class FunctionCallNode:

    def __init__(self , variable , param = []):

        self.variable = variable
        self.param = param

    def __repr__(self):

        return f"FunctionCallNode({self.variable} , {self.param})"
    
class TypesNode:
    
    def __init__(self,data):

        self.data = data

class UseNode:

    def __init__(self,name,alias = None):

        self.name = name
        self.alias = alias

    def __repr__(self):

        if self.alias == None:
            return f"{self.name}"
        return f"({self.name} , {self.alias})"


class DotOperatorNode:

    def __init__(self,variable , properties = []):

        self.variable = variable
        self.properties = properties

    def __repr__(self) -> str:
        
        return f"DotOperator({self.variable , self.properties})"

class Parser:

    def __init__(self,tokens , file):

        self.tokens = tokens
        self.index = -1
        self.current_token = None
        self.file = file
        self.next()

    def next(self):

        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = Token("eof")

    def parse(self):

        result , error = self.expression()
        
        if error:
            return None , error
        return result , None
        
    def expression(self):

        if self.current_token.type == token_keyword and self.current_token.value == "let":
            self.next()
            if self.current_token.type != token_variable:
                return None , WrongSyntaxError(self.file , "Expected a variable after the 'let' keyword.")
            
            variable = self.current_token
            self.next()

            if self.current_token.type != token_colon:
                return None , WrongSyntaxError(self.file , f"Expected a ':' after variable '{variable.value}'.")

            self.next()

            expression , error = self.expression()
            if error:
                return None , error

            return VariableNode(variable , expression) , None

        left , error = self.relational_expression()
        if error:
            return None , error

        while self.current_token.type in (token_and , token_or):

            operator = self.current_token
            self.next()
            right , error = self.relational_expression()
            if error:
                return None , error
            left = BinaryOperatorNode(left , operator , right)

        return left , None
    
    def relational_expression(self):

        # fix not statemenets

        if self.current_token.type == token_keyword and self.current_token.value == "not":
            self.next()
            relation , error = self.relational_expression()
            if error:
                return None , error
            return UnaryOperatorNode(token_not , relation) , None

        left , error = self.arithmatic_expression()
        
        if error:
            return None , error

        while self.current_token.type in (token_lt , token_gt ,
                                          token_lte , token_gte ,
                                          token_ne , token_eql):
            operator = self.current_token
            self.next()
            if self.current_token.type in (token_lt , token_gt ,
                                          token_lte , token_gte ,
                                          token_ne , token_eql):
                return None , InvalidOperationError(self.file , f"Invalid operator used in relational statement.")
            right , error = self.arithmatic_expression()

            if error:
                return None , error
            left = BinaryOperatorNode(left , operator , right)

        return left , None

    def arithmatic_expression(self):

        left , error = self.term()
        if error:
            return None , error

        while self.current_token.type in (token_plus , token_minus):
            operator = self.current_token
            self.next()
            right , error = self.term()
            if error:
                return None , error
            left = BinaryOperatorNode(left, operator , right)

        return left , None

    def term(self):

        left , error = self.factor()
        if error:
            return None , error

        while self.current_token.type in (token_mul , token_divide):
            operator = self.current_token
            self.next()
            right , error = self.factor()
            if error:
                return None , error
            left = BinaryOperatorNode(left, operator , right)

        return left , None
    
    def factor(self):

        if self.current_token.type in (token_plus , token_minus):
            operator = self.current_token
            self.next()
            factor , error = self.factor()
            if error:
                return None , error
            return UnaryOperatorNode(operator , factor) , None

        power , error = self.power()
        if error:
            return None , error
        return power , None
            

    def power(self):
        atom_rule , error = self.atom()
        if error:
            return None , error

        while self.current_token.type == token_power:
            operator = self.current_token
            self.next()
            factor , error = self.factor()
            if error:
                return None , error
            atom_rule = BinaryOperatorNode(atom_rule , operator , factor)

        return atom_rule , None

    def call(self , variable):
        if self.current_token.type != token_lb:
            return None , WrongSyntaxError(self.file ,"Expected '{'" + f" after {variable.value} function call.")
        
        self.next()

        if self.current_token.type == token_rb:
            self.next()
            return FunctionCallNode(variable) , None
        
        arg , error = self.expression()
        if error:
            return None , error

        params = [arg]

        while self.current_token.type == token_comma:
            self.next()
            arg , error = self.expression()
            if error:
                return None , error
            params.append(arg)

            
        if self.current_token.type != token_rb:
            return None , WrongSyntaxError(self.file , "Expected '}'" +f" in '{variable.value}' function call.")
        self.next()

        return FunctionCallNode(variable , params) , None

    def atom(self):

        if self.current_token.type in (token_int , token_float):
            token = self.current_token
            self.next()
            return NumberNode(token) , None
        
        
        elif self.current_token.type  == token_keyword and self.current_token.value == "types":
            self.next()
            types , error = self.expression()
            if error:
                return None , error

            return TypesNode(types) , None
        
        elif self.current_token.type == token_string:
            string = self.current_token
            self.next()
            indexs = []
            if self.current_token.type == token_ls:
                while self.current_token.type == token_ls:
                    self.next()
                    index , error = self.expression()
                    if error:
                        return None , error
                    
                    if self.current_token.type != token_rs:
                        return None , WrongSyntaxError(self.file , "Expected a '[' in staring indexing statement.")
                    self.next()
                    indexs.append(index)
                return StringAccessNode(string , indexs) , None

            return StringNode(string) , None

        elif self.current_token.type == token_variable:
            variable = self.current_token
            indexs = []
            self.next()

            if self.current_token.type == token_colon:
                self.next()
                expression , error = self.expression()
                if error:
                    return None , error
                return VariableNode(variable , expression) , None

            if self.current_token.type == token_lb:

                function_call , error = self.call(variable)
                if error:
                    return None , error
                
                return function_call  , None
                
            if self.current_token.type == token_keyword and self.current_token.value == "function":
                function_expression , error = self.function_statement(variable)
                
                if error:
                    return None , error
                return function_expression , None
            
            if self.current_token.type in (token_colon_divide ,token_colon_minus ,
                                            token_colon_mul , token_colon_plus,
                                            token_colon_power):
                operator = self.current_token
                self.next()
                expression , error = self.expression()
                if error:
                    return None , error
                
                return AssignmentOperatorNode(VariableAccessNode(variable) , operator , expression) , None
            

            if self.current_token.type == token_ls:

                while self.current_token.type == token_ls:
                    self.next()
                    index , error = self.expression()
                    if error:
                        return None , error
                        
                    if self.current_token.type != token_rs:
                        return None , WrongSyntaxError(self.file , f"Expected a ']' in variable '{variable}'.")
                    self.next()
                    indexs.append(index)

                return CollectionAccessNode(variable , indexs) , None
            
            
            return VariableAccessNode(variable) , None
        
        
        elif self.current_token.type == token_input:

            input_message = self.current_token
            self.next()
            return InputStringNode(input_message) , None
            
        elif self.current_token.type == token_lparen:
            self.next()
            expression , error = self.expression()
            if error:
                return None , error
            if self.current_token.type != token_rparen:
                return None , WrongSyntaxError(self.file , f"Expected a ')' after expression.")
            self.next()

            return expression , None

        elif self.current_token.type == token_keyword and self.current_token.value == "show":

            self.next()
            expression , error = self.expression()

            if error:
                return None , error
            return expression , None

        elif self.current_token.type == token_keyword and self.current_token.value == "if":

            if_statement , error = self.if_statement()
            if error:
                return None , error
            return if_statement , None

        elif self.current_token.type == token_lb:

            collection , error = self.collection_statement()
            if error:
                return None , error
            return collection , None
        
        elif self.current_token.type == token_keyword and self.current_token.value == "for":

            for_statement , error = self.for_statement()
            if error:
                return None , error
            return for_statement , None
        
        elif self.current_token.type == token_keyword and self.current_token.value == "delete":
            self.next()
            variables = []
            if self.current_token.type != token_variable:
                return None , WrongSyntaxError(self.file , "Expected a variable but got an expression.")
            variables.append(self.current_token)
            self.next()

            while self.current_token.type == token_comma:
                self.next()
                if self.current_token.type != token_variable:
                    return None , WrongSyntaxError(self.file , "Expected a variable but got an expression.")
                variables.append(self.current_token)
                self.next()
            
            return DeleteNode(variables) , None

        elif self.current_token.type == token_keyword and self.current_token.value == "use":
            self.next()
            module_name, error = self.expression()
            if error:
                return None , error
            return UseNode(module_name) , None
        
    def if_statement(self):

        cases = []
        else_case = None

        if not (self.current_token.type == token_keyword and self.current_token.value == "if"):

            return None , WrongSyntaxError(self.file , "Expected 'if' keyword.")
        self.next()

        if self.current_token.type != token_lb:
            return None ,  WrongSyntaxError(self.file , "Expected a '{' after the 'if' keyword.")

        self.next()
        condition ,  error = self.expression()
        if error:
            return None , error
        
        if self.current_token.type != token_rb:
            return None , WrongSyntaxError(self.file , "Expected a '}' before ':' in 'if statement'.")
        self.next()

        if self.current_token.type != token_colon:
            return None , WrongSyntaxError(self.file , "Expected a ':' after '}' in 'if statement'.")

        self.next()
        case1 , error = self.expression()
        if error:
            return None , error
        cases.append((condition , case1))

        while self.current_token.type == token_keyword and self.current_token.value == "elif":

            self.next()
            if self.current_token.type != token_lb:
                return None , WrongSyntaxError(self.file , "Expected '{' after 'elif' keyword.")
            
            self.next()
            condition , error = self.expression()
            if error:
                return None , error
            
            if self.current_token.type != token_rb:
                return None , WrongSyntaxError(self.file , "Expected a '}' before ':' in 'elif statement'.")
            self.next()

            if self.current_token.type != token_colon:
                return None , WrongSyntaxError(self.file , "Expected a ':' after '}' in 'elif statement'.")

            self.next()

            block , error = self.expression()
            if error:
                return None , error

            cases.append((condition , block))

        if self.current_token.type == token_keyword and self.current_token.value == "else":

            self.next()
            if self.current_token.type != token_colon:
                return None , WrongSyntaxError(self.file , "Expected a ':' after the 'else' keyword.")
            self.next()
            block , error = self.expression()
            if error:
                return None , error

            else_case = block

        return IfNode(cases , else_case) , None


    def collection_statement(self):

        elements = ()
        first_element_type = None
        same_type = True

        if self.current_token.type != token_lb:
            return None , WrongSyntaxError(self.file , "Expected a '{' in collection statement.")
        self.next()

        if self.current_token.type == token_rb:
            return CollectionNode(elements) , None

        element , error = self.expression()
        if error:
            return None , error
        
        first_element_type = type(element)

        elements += (element ,)

        while self.current_token.type == token_comma:
            self.next()
            element , error = self.expression()
            if error:
                return None , error
            
            elements += (element , )

        for element in elements[1:]:
            if type(element) != first_element_type:
                same_type = False
                break

        if same_type:
            elements = np.array(elements)

        if self.current_token.type != token_rb:
            return None , WrongSyntaxError(self.file , "Expected a '}' in 'collection statement'.")
        self.next()
        return CollectionNode(elements) , None
    



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
        print(result)
        del lexer , parser
        
