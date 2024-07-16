from Lexer import *
import numpy as np
from helper.Error import *
from helper.Node import *

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
        except Exception as e:
            print(e)
            return None , WrongSyntaxError(self.file , "Error occured due to inconsistent placing of brackets. check in parse function , if you get this is error kindly report this to us by raising an github issue in the repo https://github.com/Harish-M-2003/Squig" )
    
    def statements(self):
        statements = []

        if self.current_token.type == token_eof:
            return CollectionNode(elements=statements) , None
        
        
        statement,  error = self.expression()
        # print("let Node" , statements)
        if error:
            return None , error
        
        statements.append(statement)

        while self.current_token.type != token_eof:
            # while self.current_token.type == token_newline:
            #     self.next()
            if self.current_token.type == token_eof:
                break
            
            if self.current_token.type == token_rb:
            #     self.next()
                break

            statement , error = self.expression()
            if error:
                return None , error
            statements.append(statement)
        
        # print("working for for loop in statement" , statements)
        return CollectionNode(elements=statements) , None
        
    def expression(self):
        if self.current_token.type == token_keyword and self.current_token.value in ("let" , "imu"):
            isConstant = self.current_token.value == "imu"
            
            self.next()
            if self.current_token.type != token_variable:
                # print(self.current_token)
                return None , WrongSyntaxError(self.file , "Expected a variable after the 'let' keyword.", position = self.current_token.position.copy_position() )
            
            variable = self.current_token
            
            self.next()

            if self.current_token.type != token_colon and self.current_token.type != token_type_specifier:
                return None , WrongSyntaxError(self.file , f"Expected a ':' after variable '{variable.value}'.",position = self.current_token.position.copy_position())
            
            type_mentioned = None
            if self.current_token.type == token_type_specifier:
                self.next()
                type_mentioned = self.current_token
                self.next()
                if self.current_token.type != token_colon:
                    return LetNode(variable , None , isConstant , type_mentioned) , None

            self.next()

            # if self.current_token.type == token_at:
            #     self.next()
            #     if self.current_token.type != token_variable:
            #         return None  , WrongSyntaxError(self.file , "Expected a class name after '@' for instantiation an object.")

            #     class_name = self.current_token
            #     self.next()
            #     return ObjectNode(variable , class_name) , None

            # if self.current_token.type == token_keyword and self.current_token.value == "none":
            #     self.next()
            #     return LetNode(variable , NullNode()) , None
            
            expression , error = self.expression()
            # print(expression , "in expression function")
            if not type_mentioned:
                type_mentioned = type(expression).__name__.replace("Node" , "").strip().lower()
            if error:
                return None , error

            # return VariableNode(variable , expression) , None
            
            return LetNode(variable , expression , isConstant , type_mentioned) , None

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
        
        elif self.current_token.type == token_keyword and self.current_token.value == "null":
            self.next()
            return NullNode() , None
        
        elif self.current_token.type  == token_keyword and self.current_token.value == "type":
            self.next()
            types , error = self.expression()
            if error:
                return None , error

            return TypesNode(types) , None
        
        elif self.current_token.type == token_keyword and self.current_token.value == "clear":
            self.next()
            variable_name , error  = self.expression()
            if error:
                return None , error
            return ClearNode(variable_name) , None
        
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

            # if self.current_token.type == token_keyword and self.current_token.value == "class":
            #     class_statement , error = self.class_statement(variable)
            #     if error:
            #         return None , error
            #     return class_statement , None


            if self.current_token.type == token_colon:
                self.next()

                expression , error = self.expression()
                
                if error:
                    return None , error
                return VariableNode(variable , expression) , None
            
            if self.current_token.type == token_dot:
                self.next()
                prop_node = self.current_token
                self.next()
                # if self.current_token.type == token_lb:
                #     print("it function call")
                if self.current_token.type != token_colon:
                    return VariableAccessNode(variable , prop_node) , None
                self.next()
                value , error = self.expression()
                if error:
                    return None , error
                return VariableNode(variable , value , prop_node) , None
            
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
                
                if self.current_token.type == token_colon:
                    return None , WrongSyntaxError(self.file , "Unexpected '{'" + f" bracket found after variable {variable.value}.")
                
                return function_call  , None
                
            if self.current_token.type == token_keyword and self.current_token.value == "fn":
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
                    if self.current_token.type == token_rs:
                        return None , WrongSyntaxError(self.file , f"Expected a 'key' before ']' in variable '{variable}'.", position = self.current_token.position.copy_position() )
                    index , error = self.expression()
                    # if type(index) == StringNode:
                    #     isHashmap = True
                    if error:
                        return None , error
                        
                    if self.current_token.type != token_rs:
                        return None , WrongSyntaxError(self.file , f"Expected a ']' in variable '{variable}'.", position = self.current_token.position.copy_position() )
                    self.next()
                    indexs.append(index)
                    # print(isHashmap)cls


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
                    # print("working")

                    return VariableManipulationNode(variable , indexs , value) , None
                    
                    # if type(value) == MutableStringNode:
                        # return VariableManipulationNode(variable , indexs , MutableStringNode(value)) , None
                        # return VariableManipulationNode(variable , indexs , value) , None
                    # else:
                        # return None , RunTimeError(self.file , "Trying to Manipulate Unsupported types")
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

            expressions = [expression]
            
            while self.current_token.type == token_comma:
                self.next()
                line , error = self.expression()
                if error:
                    return None , error
                expressions.append(line)
            
            return ShowNode(expressions)  , None
        
        elif self.current_token.type == token_keyword and self.current_token.value == "file":
            
            self.next()

            # filename , error = self.expression()
            # if error:
            #     return None , error
            
            # return FileNode(filename , "r") , None # need to get input from squig for the file mode.
            
            file , error = self.file_statement()
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
            acessNode , error = self.expression()
            if error:
                return None , error
            
            return PopNode(variable=variable , index =acessNode )  , None
            # variable = self.current_token
            # self.next()
            # if self.current_token.type == token_ls:
        #         self.next()
                # if self.current_token.type != token_int and  self.current_token.type != token_string:
                #     return None , RunTimeError(self.file , "Expected a 'index' or 'string' as key but got unexpected key type.")
                # index  , error = self.expression()
        #         # print("index" , index)
                # if error:
                #     return None , error
                
                # if self.current_token.type != token_rs:
                #     return None , WrongSyntaxError(self.file , "Expected a ']' in pop statement.", position = self.current_token.position.copy_position() )
                
                # self.next()

                # return PopNode(variable=variable , index = index ) , None
            
        #     return PopNode(variable=variable) , None
    
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

        if self.current_token.type != token_lb:
            return None , WrongSyntaxError(file=self.file , details="Expected a '{' in switch statement.",position=None)
        
        self.next()

        case_conditions = {}

        # while self.current_token.type == token_newline:
        #         self.next()

        while self.current_token.type == token_keyword and self.current_token.value == "case":
            # print("checking")
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
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
            
            # while self.current_token.type == token_newline:
            #     self.next()
            
            case_conditions[case_condition] = case_body

            if self.current_token.type == token_rb:
                self.next()

        # while self.current_token.type == token_newline:
        #     self.next()
        if self.current_token.type != token_keyword and self.current_token.value != "default":
            
            return None ,  WrongSyntaxError(file=self.file , details="Expected a 'default' in switch statement.",position=None)
        
        has_brackets = False
        self.next()
        if self.current_token.type != token_colon:
            return None ,  WrongSyntaxError(file=self.file , details="Expected a ':' in switch statement.",position=None)
        
        self.next()
        default_body , error = None , None
       
        if self.current_token.type != token_lb:
            has_brackets = True
            default_body , error = self.expression()
        else:
            self.next()
            default_body , error = self.statements()
        


        if error:
            return None , error
        
        if has_brackets and self.current_token.type != token_rb:
            
            return None , WrongSyntaxError(file=self.file , details="Expected a '}' in switch statement.",position=None)
        
        self.next()

        
        if not has_brackets and self.current_token.type != token_rb:
            return None , WrongSyntaxError(file=self.file , details="Expected a '}' in switch statement.",position=None)
        
        self.next()

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
            # print("it's a function call")
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
        if self.current_token.type != token_colon and self.current_token.type != token_type_specifier:

            return None , WrongSyntaxError(self.file , "Expected a ':' in " +f"{function_name.value} function definition", position = self.current_token.position.copy_position() )
        
        type_mentioned = None
        if self.current_token.type == token_type_specifier:
            self.next()
            type_mentioned = self.current_token

        self.next()

        if self.current_token.type == token_lb:
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            statement , error = self.statements()

            if error:
                return None , error
            
            if self.current_token.type != token_rb:
                return None , WrongSyntaxError(self.file , "Expected a closing '}' in function .")
            
            self.next()
            
            return FunctionNode(function_name , param_list , statement , type_mentioned) , None

        function_body , error = self.expression()

        # print("after in function statement in parser")
        if error:
            return None , WrongSyntaxError(self.file , "Something went wrong in function body.", position = self.current_token.position.copy_position() )
        # if self.current_token.type != token_keyword and self.current_token.value == "end":
        #     return None , WrongSyntaxError(self.file , f"expected an 'end' in {function_name} definition.")
        # # self.next()

        return FunctionNode(function_name , param_list , function_body , type_mentioned) , None

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
        step_range  = 1
        end_range = None

        if self.current_token.type == token_comma:
            self.next()
            end_range , error = self.expression()
            if error:
                return None , error

            if self.current_token.type == token_comma:
                self.next()
                step_range , error = self.expression()
                if error:
                    return None , error

        if self.current_token.type != token_rb:

            return None , WrongSyntaxError(self.file , "Expected a '}' after the range in for loop.", position = self.current_token.position.copy_position() )
        self.next()

        if self.current_token.type != token_colon:

            return None , WrongSyntaxError(self.file , "Expected a ':' after the for loop range", position = self.current_token.position.copy_position() )
        
        self.next()

        if self.current_token.type == token_lb:
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            if self.current_token.type == token_rb:
                return None , RunTimeError(self.file , "blocks cannot be empty , check 'for clause' at line {linenumber}.") 
            statement , error = self.statements()
            # print("it's  a newline statement" , self.current_token)
            if error:
                return None , error
        
            
            # while self.current_token.type == token_newline:
            #     self.next()
            
            if self.current_token.type != token_rb:
                return None , WrongSyntaxError(self.file , "Expected a closing '}' in for loop." , position = None) 
            
            self.next()

            return ForNode(iterator_variable_name , start_range , end_range , step_range , statement , None) , None


        loop_body , error = self.expression()
        if error:

            return None , WrongSyntaxError(self.file , "Something went wrong in for loop body.", position = self.current_token.position.copy_position() )

        return ForNode(iterator_variable_name , start_range , end_range , step_range , loop_body , None) , None
                
    def if_statement(self):

        cases = []
        else_case = None
        if not (self.current_token.type == token_keyword and self.current_token.value == "if"):

            return None , WrongSyntaxError(self.file , "Expected 'if' keyword.", position = self.current_token.position.copy_position() )
        self.next()

        if self.current_token.type != token_lb:
            return None ,  WrongSyntaxError(self.file , "Expected a '{' after the 'if' keyword.", position = self.current_token.position.copy_position() )

        self.next()
        
        # while self.current_token.type == token_newline:
        #     self.next()
        condition ,  error = self.expression()

        if type(condition) == VariableNode:
            return None , RunTimeError(self.file , "cannot use assignment statement in conditions")
        
        # print("inside if" , self.current_token)
        # while self.current_token.type == token_newline:
        #     self.next()
        if error:
            return None , error
        
        if self.current_token.type != token_rb:
            return None , WrongSyntaxError(self.file , "Expected a '}' before ':' in 'if statement'.", position = self.current_token.position.copy_position() )
        self.next()

        if self.current_token.type != token_colon:
            return None , WrongSyntaxError(self.file , "Expected a ':' after '}' in 'if statement'.", position = self.current_token.position.copy_position() )
        
        self.next()
        cases1 , error = None , None # Check this line
        if self.current_token.type == token_lb:
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            if self.current_token.type == token_rb:
                return None , RunTimeError(self.file , "blocks cannot be empty. check 'if clause' at line {linenumber}")
            cases1 , error = self.statements()
        else:
            
            # while self.current_token.type == token_newline:
            #     self.next()
            if self.current_token.type == token_rb:
                return None , RunTimeError(self.file , "blocks cannot be empty. check 'if clause' at line {linenumber}")
            cases1 , error = self.expression()
        
        if error:
                return None , error
        
        cases.append((condition , cases1))
        if self.current_token.type != token_rb:
            return None , WrongSyntaxError("Expected a closing '}' in if statement")
        self.next()
        # while self.current_token.type == token_newline:
        #     self.next()
        while self.current_token.type == token_keyword and self.current_token.value == "elif":

            self.next()
            if self.current_token.type != token_lb:
                return None , WrongSyntaxError(self.file , "Expected '{' after 'elif' keyword.", position = self.current_token.position.copy_position() )
            
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            condition , error = self.expression()
            
            # while self.current_token.type == token_newline:
            #     self.next()
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
                if self.current_token.type == token_rb:
                    return None , RunTimeError(self.file , "blocks cannot be empty. check 'elif clause' at line {linenumber}")
            
                block , error = self.statements()
            else:
                if self.current_token.type == token_rb:
                    return None , RunTimeError(self.file , "blocks cannot be empty. check 'elif clause' at line {linenumber}")
            
                block , error = self.expression()
            
            if error:
                return None , error
            
            if self.current_token.type != token_rb:
                return None , WrongSyntaxError(self.file , "Expected a closing '}' for elif block.")
            self.next()
            cases.append((condition , block))

            # while self.current_token.type == token_newline:
            #     self.next()

        if self.current_token.type == token_keyword and self.current_token.value == "else":

            self.next()
    
            if self.current_token.type != token_colon:
                return None , WrongSyntaxError(self.file , "Expected a ':' after the 'else' keyword.", position = self.current_token.position.copy_position() )
            self.next()

            block , error = None , None
            if self.current_token.type == token_lb:
                self.next()
                if self.current_token.type == token_rb:
                    return None , RunTimeError(self.file , "blocks cannot be empty. check 'else clause' at line {linenumber}")
            
                block , error = self.statements()
            else: 
                if self.current_token.type == token_rb:
                    return None , RunTimeError(self.file , "blocks cannot be empty. check 'else clause' at line {linenumber}")
                block , error = self.expression()

            if error:
                return None , error
            
                # print("if statement" , self.current_token)
            # print(self.current_token)
            if self.current_token.type != token_rb:
                return None , WrongSyntaxError(self.file , "Expected a '}' in the 'else clause'.", position = self.current_token.position.copy_position() )
            
            self.next()

            else_case = block
        

        return IfNode(cases , else_case) , None


    def collection_statement(self):
        # print("working")
        elements = ()
        first_element_type = None
        same_type = True

        if self.current_token.type != token_lb:
            return None , WrongSyntaxError(self.file , "Expected a '{' in collection statement.", position = self.current_token.position.copy_position() )
        self.next()

        # while self.current_token.type == token_newline:
        #     self.next()

        if self.current_token.type == token_rb:
            return CollectionNode(elements) , None

        element , error = self.expression()
        if error:
            return None , error
        
        first_element_type = type(element)

        #Map Feature
        if self.current_token.type == token_colon:
            
            hashmap = HashMapNode()

            self.next()
            value , error = self.expression()
            if error:
                return None , error
                        
            hashmap.key_value[element.string.value] = value
            hashmap.index_key.append(element.string.value)
            while self.current_token.type == token_comma:

                self.next()
                 
        #         # print("it working" , self.current_token.type)
                # while self.current_token.type == token_newline:
                #     self.next()

                if self.current_token.type == token_rb:
                    break

                # while self.current_token.type == token_newline:
                #     self.next()
                key , error = self.expression()

                if error:
                    return None , error
                
                if self.current_token.type != token_colon:
                    return None , WrongSyntaxError(self.file , "Expected a ':' in hashmap declaration.")
                
                self.next()

                value , error = self.expression()
                if error:
                    return None , error
                
                # print("workigng" , value.string.value)
                # print(hashmap.index_key , hashmap.key_value , type(value) , type(key))

                hashmap.key_value[key.string.value] = value
                hashmap.index_key.append(key.string.value)
                # print(hashmap.index_key)



            # while self.current_token.type == token_newline:
            #     self.next()

            if self.current_token.type != token_rb:
                return None , WrongSyntaxError(self.file , "Expected a '}' in hashmap declaration.")
            self.next()

            return hashmap , None
            
        elements += (element,)
        
        # while self.current_token.type == token_newline:
        #     self.next()

        while self.current_token.type == token_comma:

            if self.current_token.type == token_comma :
                # print(self.current_token , elements)
                self.next()
            # while self.current_token.type == token_newline:
            #     self.next()


            element , error = self.expression()
            if error:
                return None , error
            
            elements += (element , )
            # while self.current_token.type == token_newline:
            #     self.next()

        for element in elements[1:]:
            if type(element) != first_element_type:
                same_type = False
                break

        if same_type:
            elements = np.array(elements)

        # while self.current_token.type == token_newline:
        #     self.next()

        if self.current_token.type != token_rb:
            return None , WrongSyntaxError(self.file , "Expected a '}' in 'collection statement'.", position = self.current_token.position.copy_position() )
        self.next()
        # print(type(elements))
        return CollectionNode(elements) , None
    

    # def class_statement(self , class_name):
        
    #     self.next()

    #     if self.current_token.type != token_lb:
    #         return None , WrongSyntaxError(self.file , "Expected a opening '{' in class.")
        
    #     self.next()

    #     class_body , error = self.statements()
    #     if error:
    #         return None , error
        
    #     if self.current_token.type != token_rb:
    #         return None , WrongSyntaxError(self.file , "Expected a closing '}' in class.")
    #     self.next()
        
    #     return ClassNode(class_name , class_body) , None
    

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