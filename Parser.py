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

        if self.operator.type == token_minus:
            return '-' + f"{self.factor.factor.value}"
        elif self.operator.type == token_not:
            return "! " + f"{self.factor}"
        # return f"{'-' if self.operator.type == token_minus else 'not'}{self.factor.factor.value}"

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

    def __init__(self,name):

        self.name = name

    def __repr__(self):

        return f"{self.name}"

class BooleanNode:

    def __init__(self , value):

        self.bool = value

    def __repr__(self):
        
        return f"BooleanNode({self.bool})"
        
        
class ReturnNode:

    def __init__(self , return_value):
        self.value = return_value
    
    def __repr__(self):

        return f"ReturnNode({self.value})"
    
class ShowNode:

    def __init__(self , statement):

        self.statement = statement
    
    def __repr__(self):

        return f"ShowNode({self.statement})"
    
class LetNode:

    def __init__(self , variable , expression):
        
        self.variable = variable
        self.factor = expression
    
    def __repr__(self):

        return f"LetNode({self.variable})"

class FileNode:

    def __init__(self , filename , mode):

        self.filename = filename
        self.mode = mode
    
    def __repr__(self):
        
        return f"FileNode({self.filename} , {self.mode})"
    
class CloseNode:

    def __init__(self , file):

        self.filename = file
    
    def __repr__(self) -> str:
        
        return f"close( {self.filename } )"
    
class FileWriteNode:

    def __init__(self , variable , content):

        self.variable = variable
        self.content = content

    def __repr__(self):

        return f"FileWriteNode ( {self.variable } , {self.content} )"
    
class SwitchNode:

    def __init__(self , condition , default_body , cases = {} , ):

        self.condition = condition
        self.cases = cases
        self.default = default_body

    def __repr__(self):

        return f"SwitchNode({self.condition} , {self.cases})"

# class HashMapNode:

#     def __init__(self):

#         self.key_value = {}
#         self.index_key = {}

#     def __repr__(self):

#         return f"{self.key_value}".replace(')','}').replace('(','{')

class MutableStringNode:

    def __init__(self , string):
        self.string = string
    
    def __repr__(self):

        return f"MutableString({self.string})"
    

class VariableManipulationNode:

    def __init__(self , variable , index , value):
        
        self.variable = variable
        self.index = index
        self.value = value

    def __repr__(self):

        return f"VariableManipulationNode({self.variable , self.index , self.value})"
    
class PopNode:

    def __init__(self , variable , index = None):

        self.variable = variable
        self.index = index

class Parser:

    def __init__(self,tokens , file ):

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
        try:
            result , error = self.statements()
            # print(result)
            if error:
                return None , error
            return result , None
        except:
            return None , Error(self.file , "Check in parse function in parser" , "Somthing went worng in the programm" )
    
    def statements(self):

        while self.current_token.type == token_newline:
            self.next()
        if self.current_token.type == token_eof:
            return CollectionNode(elements=statements) , None
        
        statements = []
        
        statement,  error = self.expression()
        if error:
            return None , error
        
        statements.append(statement)

        while self.current_token.type != token_eof:
            while self.current_token.type == token_newline:
                self.next()
            if self.current_token.type == token_eof:
                break
            
            if self.current_token.type == token_rb:
                self.next()
                break

            statement , error = self.expression()
            if error:
                return None , error
            statements.append(statement)
        
        # print("working for for loop in statement" , statements)
        return CollectionNode(elements=statements) , None
        
    def expression(self):
        if self.current_token.type == token_keyword and self.current_token.value == "let":
            self.next()
            if self.current_token.type != token_variable:
                # print(self.current_token)
                return None , WrongSyntaxError(self.file , "Expected a variable after the 'let' keyword.", position = self.current_token.position.copy_position() )
            
            variable = self.current_token
            self.next()

            if self.current_token.type != token_colon:
                return None , WrongSyntaxError(self.file , f"Expected a ':' after variable '{variable.value}'.",position = self.current_token.position.copy_position())

            self.next()

            expression , error = self.expression()

            if error:
                return None , error

            # return VariableNode(variable , expression) , None
            return LetNode(variable , expression) , None

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

        # print(left , "expression method")
        return left , None
    
    def relational_expression(self):

        if self.current_token.type == token_not:
            self.next()
            relaion , error = self.relational_expression()
            if error:
                return None , error
            
            return UnaryOperatorNode(Token(token_type=token_not , token_position=None) , relaion) , None

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
                return None , InvalidOperationError(self.file , f"Invalid operator used in relational statement.", position = self.current_token.position.copy_position() )
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

        while self.current_token.type in (token_mul , token_divide , token_modulo):
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
            return None , WrongSyntaxError(self.file ,"Expected '{'" + f" after {variable.value} function call.", position = self.current_token.position.copy_position() )
        
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
            return None , WrongSyntaxError(self.file , "Expected '}'" +f" in '{variable.value}' function call.", position = self.current_token.position.copy_position() )
        self.next()

        return FunctionCallNode(variable , params) , None

    def atom(self):

        if self.current_token.type in (token_int , token_float):
            token = self.current_token
            self.next()
            return NumberNode(token) , None
        
        
        elif self.current_token.type  == token_keyword and self.current_token.value == "type":
            self.next()
            types , error = self.expression()
            if error:
                return None , error

            return TypesNode(types) , None
        
        elif self.current_token.type == token_keyword and self.current_token.value in ("true" , "false"):

            boolean_node  = BooleanNode(self.current_token.value)
            self.next()
            return boolean_node , None
        
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
                        return None , WrongSyntaxError(self.file , "Expected a '[' in staring indexing statement.", position = self.current_token.position.copy_position() )
                    self.next()
                    indexs.append(index)
                return StringAccessNode(Token(token_type=token_string  , token_value=string.value) , indexs) , None

            # return StringNode(Token(token_type=token_string , token_value=string.value)) , None
            return StringNode(string) , None
        
        elif self.current_token.type == token_mutstring:
            mutstring = self.current_token
            self.next()
            
            return MutableStringNode(mutstring) , None

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
            
            if self.current_token.type == token_writetofile:
                self.next()
                expression , error = self.expression()
                if error:
                    return None , error
                return FileWriteNode(variable=variable , content=expression) , None

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
                # isHashmap = False
                while self.current_token.type == token_ls:
                    self.next()
                    index , error = self.expression()
                    # if type(index) == StringNode:
                        # print("yeah")
                        # isHashmap = True
                    if error:
                        return None , error
                        
                    if self.current_token.type != token_rs:
                        return None , WrongSyntaxError(self.file , f"Expected a ']' in variable '{variable}'.", position = self.current_token.position.copy_position() )
                    self.next()
                    indexs.append(index)

                if self.current_token.type == token_colon:
                    self.next()
                    # value = self.current_token

                    value , error = self.expression()
                    # print("koay" , type(value) , value)
                    if error:
                        return None , error
                    # print(value , variable)
                    # print(type(value))

                    # if isHashmap:
                    #     return VariableManipulationNode(variable , indexs , value) , None
                    
                    if type(value) == MutableStringNode:
                        # return VariableManipulationNode(variable , indexs , MutableStringNode(value)) , None
                        return VariableManipulationNode(variable , indexs , value) , None
                    else:
                        return None , RunTimeError(self.file , "Trying to Manipulate Unsupported types")
                        # return VariableManipulationNode(variable , indexs , StringNode(value)) , None
                        # return VariableManipulationNode(variable , indexs , value) , None
                    
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
                return None , WrongSyntaxError(self.file , f"Expected a ')' after expression.", position = self.current_token.position.copy_position() )
            self.next()

            return expression , None

        elif self.current_token.type == token_keyword and self.current_token.value == "log":

            self.next()
            expression , error = self.expression()

            if error:
                return None , error
            # return expression , None

            return ShowNode(expression)  , None
        
        elif self.current_token.type == token_keyword and self.current_token.value == "file":
            
            self.next()

            # filename , error = self.expression()
            # if error:
            #     return None , error
            
            # return FileNode(filename , "r") , None # need to get input from squig for the file mode.
            
            file , error = self.file_statement()
            # print(type(file.mode.string))
            if error:
                return None , error
            
            return file , error
        
        elif self.current_token.type == token_keyword and self.current_token.value == "close":

            self.next()
            filename , error = self.expression()
            # print(filename)
            if error:
                return None , error
            
            return CloseNode(filename) , None

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
                return None , WrongSyntaxError(self.file , "Expected a variable but got an expression.", position = self.current_token.position.copy_position() )
            
            variables.append(self.current_token)
            self.next()

            while self.current_token.type == token_comma:
                self.next()
                if self.current_token.type != token_variable:
                    return None , WrongSyntaxError(self.file , "Expected a variable but got an expression.", position = self.current_token.position.copy_position() )
                variables.append(self.current_token)
                self.next()
            
            return DeleteNode(variables) , None

        elif self.current_token.type == token_keyword and self.current_token.value == "use":
            self.next()
            module_name, error = self.expression()

            if error:
                return None , error
            return UseNode(module_name) , None
        
        elif self.current_token.type == token_keyword and self.current_token.value == "switch":

            self.next()
            switchNode , error = self.switch_statement()
            if error:
                return None , error
            
            return switchNode , None
        
        elif self.current_token.type == token_keyword and self.current_token.value == "pop":
            self.next()
            if self.current_token.type != token_variable:
                return None , WrongSyntaxError(self.file , "Expected a variable but got an expression.", position = self.current_token.position.copy_position() )
            variable = self.current_token
            self.next()
            if self.current_token.type == token_ls:
                self.next()
                if self.current_token.type != token_int and  self.current_token.type != token_string:
                    return None , RunTimeError(self.file , "Expected a 'index' or 'string' as key but got unexpected key type.")
                index  , error = self.expression()
                # print("index" , index)
                if error:
                    return None , error
                
                if self.current_token.type != token_rs:
                    return None , WrongSyntaxError(self.file , "Expected a ']' in pop statement.", position = self.current_token.position.copy_position() )
                
                self.next()

                return PopNode(variable=variable , index = index ) , None
            
            return PopNode(variable=variable) , None
    
    def switch_statement(self):

        if self.current_token.type != token_lb:
            return None , WrongSyntaxError(file=self.file , details="Expected a '{' in switch statement.",position=None)
        
        self.next()

        condition , error = self.expression()
        if error:
            return None , error
        
        if self.current_token.type != token_rb:
            return None , WrongSyntaxError(file=self.file , details="Expected a '}' in switch statement.",position=None)
        
        self.next()
        if self.current_token.type != token_colon:
            return None ,  WrongSyntaxError(file=self.file , details="Expected a ':' in switch statement." , position=None)
        
        self.next()

        case_conditions = {}

        while self.current_token.type == token_newline:
                self.next()

        while self.current_token.type == token_keyword and self.current_token.value == "case":
            # print("checking")
            self.next()
            while self.current_token.type == token_newline:
                self.next()
            case_condition = str(self.current_token.value)
            # if error:
            #     return None , error
            
            self.next()
            if self.current_token.type != token_colon:
                return  None , WrongSyntaxError(file=self.file , details="Expected a ':' in switch statement.",position=None)
            
            self.next()
            # print("in parser" , self.current_token )
            error , case_body = None , None

            if self.current_token.type != token_lb:
                case_body , error = self.expression()
            else:
                self.next()
                case_body , error = self.statements()
                
            if error:
                return None , error
            
            while self.current_token.type == token_newline:
                self.next()

            
            
            case_conditions[case_condition] = case_body

        while self.current_token.type == token_newline:
            self.next()

        if self.current_token.type != token_keyword and self.current_token.value != "default":
            
            return None ,  WrongSyntaxError(file=self.file , details="Expected a 'default' in switch statement.",position=None)
        
        self.next()
        if self.current_token.type != token_colon:
            return None ,  WrongSyntaxError(file=self.file , details="Expected a ':' in switch statement.",position=None)
        
        self.next()
        default_body , error = None , None
       
        if self.current_token.type != token_lb:
            default_body , error = self.expression()
        else:
            self.next()
            default_body , error = self.statements()

        if error:
            return None , error

        return SwitchNode(condition=condition , cases=case_conditions , default_body= default_body) , None


    
    def file_statement(self):
        
        mode = "r"
        
        if self.current_token.type == token_lt:
            self.next()

            if self.current_token.type == token_string:
                mode = self.current_token.value
            
            if self.current_token.type != token_string:
                mode = "undefined variable " + "'" +  self.current_token.value + "'"
                return None , WrongSyntaxError(file=self.file , details=f"Expected arguments (a , r, w, r+ ,w+ ,a+) , but got {mode}." ,position=None)
            
            self.next()

            if self.current_token.type != token_gt:
                
                return None , WrongSyntaxError(file=self.file , details=f"Expected a closing '>' , but got {self.current_token}" ,position=None)
            
            self.next()
            
        file_name , error = self.expression()
        
        if error:
            return None , error
        
        mode = StringNode(Token(token_type=token_string , token_value=mode , token_position=None))
        
        return FileNode(filename=file_name , mode=mode) , None
        
    
    def function_statement(self , function_name):

        self.next()

        if self.current_token.type != token_lb:
            return None, WrongSyntaxError(self.file , "Expected a '{' after the 'function' keyword in " + function_name.value, position = self.current_token.position.copy_position() )
        
        self.next()
        param_list = []
        if self.current_token.type == token_variable:
            param_name , error = self.expression()
            if error:
                return None , WrongSyntaxError(self.file , "Something went wrong in function definition.", position = self.current_token.position.copy_position() )
            param_list.append(param_name.variable)

            while self.current_token.type == token_comma:
                self.next()
                param_name , error = self.expression()
                if error:
                    return None , WrongSyntaxError(self.file , 'something went worng in function deefinition.', position = self.current_token.position.copy_position() )
                param_list.append(param_name.variable)

        if self.current_token.type != token_rb:
            return None , WrongSyntaxError(self.file  , "Expected a '}' in " + f"{function_name.value} function definition.", position = self.current_token.position.copy_position() )
        
        self.next()
        if self.current_token.type != token_colon:

            return None , WrongSyntaxError(self.file , "Expected a ':' in " +f"{function_name.value} function definition", position = self.current_token.position.copy_position() )
        
        self.next()

        if self.current_token.type == token_lb:
            self.next()
            while self.current_token.type == token_newline:
                self.next()
            statement , error = self.statements()

            if error:
                return None , error
            
            return FunctionNode(function_name , param_list , statement) , None

        function_body , error = self.expression()

        # print("after in function statement in parser")
        if error:
            return None , WrongSyntaxError(self.file , "Something went wrong in function body.", position = self.current_token.position.copy_position() )
        # if self.current_token.type != token_keyword and self.current_token.value == "end":
        #     return None , WrongSyntaxError(self.file , f"expected an 'end' in {function_name} definition.")
        # # self.next()

        return FunctionNode(function_name , param_list , function_body) , None

    def for_statement(self):

        self.next()

        if self.current_token.type != token_variable:
            return None , WrongSyntaxError(self.file , "Expected  a iterator variable name after for keyword.", position = self.current_token.position.copy_position() )
        
        iterator_variable_name = self.current_token
        self.next()

        if self.current_token.type != token_lb:

            return None , WrongSyntaxError(self.file , "Expected a '{' after the interator variable.", position = self.current_token.position.copy_position() )
        
        self.next()
        start_range , error = self.expression()
        end_range = None

        if self.current_token.type == token_comma:

            end_range , error = self.expression()

        elif self.current_token.type != token_rb:

            return None , WrongSyntaxError(self.file , "Expected a '}' after the range in for loop.", position = self.current_token.position.copy_position() )
        self.next()

        if self.current_token.type != token_colon:

            return None , WrongSyntaxError(self.file , "Expected a ':' after the for loop range", position = self.current_token.position.copy_position() )
        
        self.next()

        # start of newline feature

        if self.current_token.type == token_lb:
            self.next()
            while self.current_token.type == token_newline:
                self.next()
            statement , error = self.statements()
            # print("it's  a newline statement" , self.current_token)
            if error:
                return None , error
            
            # while self.current_token.type == token_newline:
            #     self.next()
            
            # if self.current_token.type != token_rb:
            #     return None , WrongSyntaxError(self.file , "Expected a closing '{' in for loop." , position = None) 
            
            return ForNode(iterator_variable_name , start_range , end_range , None , statement , None) , None


        loop_body , error = self.expression()
        if error:

            return None , WrongSyntaxError(self.file , "Something went wrong in for loop body.", position = self.current_token.position.copy_position() )
        

        return ForNode(iterator_variable_name , start_range , end_range , None , loop_body , None) , None
                
    def if_statement(self):

        cases = []
        else_case = None

        if not (self.current_token.type == token_keyword and self.current_token.value == "if"):

            return None , WrongSyntaxError(self.file , "Expected 'if' keyword.", position = self.current_token.position.copy_position() )
        self.next()

        if self.current_token.type != token_lb:
            return None ,  WrongSyntaxError(self.file , "Expected a '{' after the 'if' keyword.", position = self.current_token.position.copy_position() )

        self.next()
        condition ,  error = self.expression()
        if error:
            return None , error
        
        if self.current_token.type != token_rb:
            return None , WrongSyntaxError(self.file , "Expected a '}' before ':' in 'if statement'.", position = self.current_token.position.copy_position() )
        self.next()

        if self.current_token.type != token_colon:
            return None , WrongSyntaxError(self.file , "Expected a ':' after '}' in 'if statement'.", position = self.current_token.position.copy_position() )
        
        self.next()
        cases1 , error = None , None
        if self.current_token.type == token_lb:
            self.next()
            case1 , error = self.statements()
        else:
            case1 , error = self.expression()

        if error:
                return None , error
        
        cases.append((condition , case1))

        while self.current_token.type == token_newline:
            self.next()

        while self.current_token.type == token_keyword and self.current_token.value == "elif":

            self.next()
            if self.current_token.type != token_lb:
                return None , WrongSyntaxError(self.file , "Expected '{' after 'elif' keyword.", position = self.current_token.position.copy_position() )
            
            self.next()
            condition , error = self.expression()
            if error:
                return None , error
            
            if self.current_token.type != token_rb:
                return None , WrongSyntaxError(self.file , "Expected a '}' before ':' in 'elif statement'.", position = self.current_token.position.copy_position() )
            self.next()

            if self.current_token.type != token_colon:
                return None , WrongSyntaxError(self.file , "Expected a ':' after '}' in 'elif statement'.", position = self.current_token.position.copy_position() )

            self.next()

            block , error = None , None
            if self.current_token.type == token_lb:
                self.next()
                block , error = self.statements()
            else:
                block , error = self.expression()
            
            if error:
                return None , error

            cases.append((condition , block))

            while self.current_token.type == token_newline:
                self.next()

        if self.current_token.type == token_keyword and self.current_token.value == "else":

            self.next()
    
            if self.current_token.type != token_colon:
                return None , WrongSyntaxError(self.file , "Expected a ':' after the 'else' keyword.", position = self.current_token.position.copy_position() )
            self.next()

            block , error = None , None
            if self.current_token.type == token_lb:
                self.next()
                block , error = self.statements()
            else:
                block , error = self.expression()

            if error:
                return None , error

            else_case = block

        # print("it's ifNode in parser")
        return IfNode(cases , else_case) , None


    def collection_statement(self):

        elements = ()
        first_element_type = None
        same_type = True

        if self.current_token.type != token_lb:
            return None , WrongSyntaxError(self.file , "Expected a '{' in collection statement.", position = self.current_token.position.copy_position() )
        self.next()

        while self.current_token.type == token_newline:
            self.next()

        if self.current_token.type == token_rb:
            return CollectionNode(elements) , None

        element , error = self.expression()
        if error:
            return None , error
        
        first_element_type = type(element)

        # if self.current_token.type == token_colon:
            
        #     hashmap = HashMapNode()

        #     self.next()
        #     value , error = self.expression()
        #     if error:
        #         return None , error
                        
        #     hashmap.key_value[element.string.value] = value
        #     hashmap.index_key[len(hashmap.key_value) - 1] = element

        #     while self.current_token.type == token_comma:

        #         self.next()
                 
        #         # print("it working" , self.current_token.type)
        #         while self.current_token.type == token_newline:
        #             self.next()

        #         if self.current_token.type == token_rb:
        #             break

        #         while self.current_token.type == token_newline:
        #             self.next()
        #         key , error = self.expression()

        #         if error:
        #             return None , error
                
        #         if self.current_token.type != token_colon:
        #             return None , WrongSyntaxError(self.file , "Expected a ':' in hashmap declaration.")
                
        #         self.next()
        #         value , error = self.expression()
        #         if error:
        #             return None , error
                
        #         hashmap.key_value[key.string.value] = value
        #         hashmap.index_key[len(hashmap.key_value) - 1] = key

        #         # print(self.current_token.type)


        #     while self.current_token.type == token_newline:
        #         self.next()

        #     if self.current_token.type != token_rb:
        #         return None , WrongSyntaxError(self.file , "Expected a '}' in hashmap declaration.")
        #     self.next()

        #     return hashmap , None
            
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
            return None , WrongSyntaxError(self.file , "Expected a '}' in 'collection statement'.", position = self.current_token.position.copy_position() )
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
        print(result)
        if error:
            print(error.print())
            continue
        
        del lexer , parser