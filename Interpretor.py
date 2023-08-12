from Parser import *
import Types

class Interpretor:

    def __init__(self , file, global_symbol_table):
        self.file = file
        self.global_symbol_table = global_symbol_table

    def process(self , node):
        method = getattr(self , f"{type(node).__name__}" , self.no_process)
        return method(node)
    
    def StringNode(self , node):

        string = node.string.value
        return Types.String(string) , None

    def NumberNode(self , node):

        number = node.factor.value
        return Types.Number(number) , None

    def BinaryOperatorNode(self , node):

        left , error = self.process(node.left)
        if error:
            return None , error
        operator = node.operator.type
        right , error = self.process(node.right)
        if error:
            return None , error

        if operator == token_plus:
            return left.add(right)
        elif operator == token_minus:
            return left.sub(right)
        elif operator == token_mul:
            return left.mul(right)
        elif operator == token_divide:
            return left.div(right)
        elif operator == token_power:
            return left.pow(right)
        elif operator == token_lt:
            return left.lt(right)
        elif operator == token_gt:
            return left.gt(right)
        elif operator == token_lte:
            return left.lte(right)
        elif operator == token_gte:
            return left.gte(right)
        elif operator == token_eql:
            return left.eql(right)
        elif operator == token_ne:
            return left.ne(right)
        elif operator == token_and:
            return left._and_(right)
        elif operator == token_or:
            return left._or_(right)

    def CollectionNode(self , node):

        elements = node.elements
        
        processed_elements = ()

        for every_element in elements:
            element , error = self.process(every_element)
            if error:
                return None , error
            processed_elements += (element , )

        return Types.Collection(processed_elements) , None

    def CollectionAccessNode(self , node):


        variable = node.variable.value
        value = None

        if not variable in self.global_symbol_table:
            return None , RunTimeError(self.file , f"Collection '{variable}' is undefind.")

        indexs = []
        for idx in node.index:
            index , error = self.process(idx)
            if not isinstance(index , Types.Number):
                return None , WrongTypeError(self.file , f"Unexpected index type found in Collection '{variable}'")
            if error:
                return None , error
            indexs.append(index)

        
        value = self.global_symbol_table[variable].index(indexs[0].number)

        if len(indexs) > 1:
            if isinstance(value , CollectionNode) or isinstance(value,Types.String) or isinstance(value , StringNode) or isinstance(value , Types.Collection):

                for _ in indexs[1:]:
                    value = value.index(_.number)
            else:

                return None , InvalidOperationError(self.file , "Cannot slice a Number Type.")

        return value , None

    def VariableNode(self , node):

        variable = node.variable.value
        
        value , error = self.process(node.factor)
        if error:
            return None , error

        self.global_symbol_table[variable] = value

        return "" , None


    def VariableAccessNode(self , node):

        variable = node.variable.value

        if variable in self.global_symbol_table:
            return self.global_symbol_table[variable] , None
        else:
            return None , RunTimeError(self.file , f"Variable '{variable}' is undefined.")

    def InputStringNode(self , node):

        string = node.string.value

        data = Types.InputString()
        result , error = data.value(input(string).strip())
        if error:
            return None , error
        return result , None
    
    def AssignmentOperatorNode(self , node):

        variable = node.left.variable
        left , error = self.process(node.left)
        if error:
            return None , error
        right , error = self.process(node.right)
        if error:
            return None , error
        
        operator = node.operator

        if not variable.value in self.global_symbol_table:
            return None , RunTimeError(self.file , f"Variable {variable} is undefined.")
        
        if operator.type == token_colon_plus:
            
            if isinstance(left , Types.String):

                output , error = left.add(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output
            
            elif isinstance(left , Types.Number):

                output , error = left.add(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output

            elif isinstance(left , Types.Collection):

                output , error = left.add(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output
            else:

                return None , RunTimeError(self.file , f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.")
            
            
        elif operator.type == token_colon_minus:
            if isinstance(left , Types.String):

                output , error = left.sub(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output
            
            elif isinstance(left , Types.Number):

                output , error = left.sub(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output

            elif isinstance(left , Types.Collection):

                output , error = left.sub(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output
            else:
                return None , RunTimeError(self.file , f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.")
        
        elif operator.type == token_colon_divide:
            if isinstance(left , Types.String):

                output , error = left.div(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output
            
            elif isinstance(left , Types.Number):

                output , error = left.div(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output
            else:
                return None , RunTimeError(self.file , f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.")
            
        elif operator.type == token_colon_mul:

            if isinstance(left , Types.String):

                output , error = left.mul(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output
            
            elif isinstance(left , Types.Number):

                output , error = left.mul(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output

            else:
                return None , RunTimeError(self.file , f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.")
            
        elif operator.type == token_colon_power:
            
            if isinstance(left , Types.Number):

                output , error = left.pow(right)
                if error:
                    return None , error
                
                self.global_symbol_table[variable.value] = output

            else:
                return None , RunTimeError(self.file , f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.")
        

        return None , None

    

    def TypesNode(self , node):

        node , error  = self.process(node.data)
        if error:
            return None , error

        types = "Type : '" + type(node).__name__.replace("Node" , '') +"'"

        return Types.String(types) , None


    def IfNode(self , node):

        cases = node.cases
        else_case = node.else_case

        for condition , statement in cases:
            predicate , error = self.process(condition)
            if error:
                return None , error
            if predicate.value:
                block , error = self.process(statement)
                if error:
                    return None,error
                return block , None
            

        if else_case:
            block , error = self.process(else_case)
            if error:
                return None , error
            return block , None
        return "",None

    def UnaryOperatorNode(self , node):

        number , error = self.process(node.factor)
        
        if error:
            return None , error

        if node.operator.type == token_minus:
            
            number ,error = number.mul(Types.Number(-1))
            if error:
                return None , error
            
        elif node.operator.type == token_not:

            return "not operator" , None
    

        return number , None
    
    def StringAccessNode(self , node):

        string = node.string.value

        indexs = []
        for idx in node.indexs:
            index , error = self.process(idx)
            if not isinstance(index , Types.Number):
                return None , WrongTypeError(self.file , f"Unexpected index type found in string '{string}'.")
            if error:
                return None , error
            indexs.append(index)
        

        return string[indexs[0].number] , None
    
    def ForNode(self , node):

        # need to fix the bugs ....

        variable = node.variable.value
        elements = []
        start_value , error = self.process(node.start_value)
        end_value = Types.Number(0)
        step_value = Types.Number(1)

        if node.end_value:
            end_value , error = self.process(node.end_value)
            if error:
                return None , error
            
        if node.step_value:

            step_value , error = self.process(node.step_value)
            if error:
                return None , error
        
        if not end_value.number:

            for var in range(start_value.number):

                self.global_symbol_table[variable] = Types.Number(var)
                body , error = self.process(node.body)
                if error:
                    return None , error
                
                elements.append(body)
        
        elif end_value.number:

            
            for var in range(start_value.number , end_value.number , step_value.number):

                self.global_symbol_table[variable] = Types.Number(var)
                body , error = self.process(node.body)
                if error:
                    return None , error
                
                elements.append(body)
        

        return Types.Collection(elements) , None
    
    def DeleteNode(self , node):


        variable = [var.value for var in node.variable]
        
        for var in node.variable:
            if isinstance(self.global_symbol_table[var.value] , Types.BuiltinFunction):
                return None , RunTimeError(self.file , f"Cannot delete buitin method '{var.value}'")

        for var in variable:
            if not var in self.global_symbol_table:
                return None , RunTimeError(self.file , f"Variable '{variable}' is  undefined.")
        
            self.global_symbol_table.pop(var) 

        return None , None
    

    def FunctionNode(self , node):        

        variable = node.variable.value
        body = node.body
        params = []

        for param in node.param:
            params.append(param.value)

        if error:
            return None , error
        
        function =  Types.UserDefinedFunction(self.file , variable , params  , body)

        self.global_symbol_table[variable] = function

        return  None , None


        
    def FunctionCallNode(self , node):

        variable = node.variable.value
        if variable not in self.global_symbol_table:
            return None , RunTimeError(self.file , f"Function {variable} is undefined.")
        
        args = []
        for arg in node.param:
            value , error = self.process(arg)
            if error:
                return None , error
            args.append(value)

        function_output  = self.global_symbol_table[variable]

        output , error = function_output.execute(args)
        if error:
            return None , error
        return output , None
    
    def UseNode(self , node):

        module_name = node.name.string.value

        code = ""

        if not module_name.endswith('.squig'):
            
            try:
                with open(module_name+".squig") as script:
                    code = script.read()
            except:
                return None , WrongImportError(self.file , f"Cannot use '{module_name}' as module.")

        if not code:
            try:
                with open(module_name) as script:
                    code = script.read()
            except:
                return None , RunTimeError(self.file , f"file '{module_name}' doesn't exists.")
        
        file = "<" + module_name +">"
        lexer  = Lexer(file , code)
        tokens , error = lexer.tokenize()
        if error:
            return None , error
        parser  = Parser(tokens , file)
        ast , error = parser.parse()
        if error:
            return None , error
        
        interpretor = Interpretor(file , self.global_symbol_table)
        output , error = interpretor.process(ast)
        if error:
            return None , error
        
        return output , None

    def no_process(self , node):

        return "No process Node" , None

if __name__ == "__main__":

    file = "<Core>"


    symbol_table = {
        "True" : Types.Boolean(True),
        "False" : Types.Boolean(False),
        "String" : Types.BuiltinFunction(file , "String"),

        "Number" : Types.BuiltinFunction(file , "Number"), #has some issue
        "Bool" : Types.BuiltinFunction(file , "Bool"), #has some issue

        "isNumber" : Types.BuiltinFunction(file , "is_number"),#checked
        "isString" : Types.BuiltinFunction(file , "is_string"),#checked
        "isBool" : Types.BuiltinFunction(file , "is_bool"),#checked
        "length" : Types.BuiltinFunction(file , "length"),#checked
        "isCollection" : Types.BuiltinFunction(file , "is_collection"),#checked

        "find" : Types.BuiltinFunction(file , "find"),
        "replace" : Types.BuiltinFunction(file , "replace"),
        "isPalindrome" : Types.BuiltinFunction(file , "is_palindrome"),
        "isFunction" : Types.BuiltinFunction(file , "is_function"),
        "lTrim" : Types.BuiltinFunction(file , "ltrim"),
        "rTrim" : Types.BuiltinFunction(file , "rtrim"),
        "trim" : Types.BuiltinFunction(file , "trim"),
        "isAlpha" : Types.BuiltinFunction(file ,"is_alpha"),
        "isAlnum" : Types.BuiltinFunction(file , "is_alnum"),
        "isInt" : Types.BuiltinFunction(file , "is_int"),

        "isFloat" : Types.BuiltinFunction(file , "is_float"),#checked
        "isTitle" : Types.BuiltinFunction(file , "is_title"),#checked
        "isAscii" : Types.BuiltinFunction(file , "is_ascii"),
        "lower" : Types.BuiltinFunction(file , "lower"), #checked
        "upper" : Types.BuiltinFunction(file , "upper"), #checked

        "isSpace" : Types.BuiltinFunction(file , "is_space"),
        "slice" : Types.BuiltinFunction(file , "slice"),
        "toCap" : Types.BuiltinFunction(file , "toCap"),

        "startsWith" : Types.BuiltinFunction(file , "startswith"),#checked
        "endsWith" : Types.BuiltinFunction(file , "endswith"),#checked
        
        "swapCase" : Types.BuiltinFunction(file , "swapcase"),
        "charAt" : Types.BuiltinFunction(file , "charat"),
        "reverse" : Types.BuiltinFunction(file , "reverse"),
    }

    
    
    while True:
        try:
            code = input("Squig > ")

        except KeyboardInterrupt:
            print("Type 'exit' to close the console.")
            continue
        if code == 'exit':
            break
        if not code:
            continue
        lexer = Lexer(file , code)
        tokens , error = lexer.tokenize()
        if error:
            print(error.print())
            continue
        
        parser = Parser(tokens , file)
        ast , error = parser.parse()
        
        if error:
            print(error.print())
            continue
        interpretor = Interpretor(file , symbol_table)
        result , error = interpretor.process(ast)
        if error:
            print(error.print())
            continue
        if result:
            print(result)
        
