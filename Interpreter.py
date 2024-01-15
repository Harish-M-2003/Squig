from Parser import *
import Types

class Interpreter:

    def __init__(self , file, global_symbol_table):
        self.file = file
        self.global_symbol_table = global_symbol_table

    def process(self , node):

        method = getattr(self , f"{type(node).__name__}" , self.no_process)
        
        return method(node)
    
    def ShowNode(self , node):

        # print(self.process(node.statement))
        # print(type(node.statement))
        # statement , error = self.process(node.statement)
        # print("working")
        # print("in interpretor" , node.statement)
        # print(node.statement)

        lines = []
        for statement in node.statement:
            line ,error = self.process(statement)
            if error:
                return None , error
            lines.append(line)
        
        # print(lines)
        # print(*lines)
        # print(self.process(node.statement))
        
        # if error:
        #     return None , error
        
        print(*lines)
        return None , None
    
    def StringNode(self , node):

        string = node.string.value
        
        return Types.String(string=string,filename=self.file) , None

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
        elif operator == token_modulo:
            return left.modulo(right)
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
        
        processed_elements = []

        for every_element in elements:
            element , error = self.process(every_element)
            if error:
                return None , error
            processed_elements.append(element)

        return Types.Collection(filename=self.file,elements=processed_elements) , None
    
    def HashMapNode(self , node):
        # print("hasmap node")

        key_values = node.key_value
        index_key = node.index_key


        processed_key_value = {}
        processed_index_key = []


        index = 0
        for key , value in key_values.items():
            processed_key , error = self.process(key_values[key])
            if error:
                return None , error
            processed_index = index_key[index]
            
            processed_key_value[key] = processed_key
            processed_index_key.append(processed_index)
            index += 1
        
        # print(processed_index_key , processed_key_value)
            
    #     # print(type(processed_index_key[0]))
        return Types.HashMap(processed_key_value , processed_index_key) , None

    def CollectionAccessNode(self , node):
        # print("got the node")
        variable = node.variable.value
        value = None    

        if not variable in self.global_symbol_table :
            return None , RunTimeError(self.file , f"Collection '{variable}' is undefind.")
        
        indexs = []
        for idx in node.index:
            index , error = self.process(idx)
            if not isinstance(index , Types.Number) and isinstance(self.global_symbol_table[variable] , Types.Collection):
                return None , WrongTypeError(self.file , f"Unexpected index type found in Collection '{variable}'")
            if error:
                return None , error
            indexs.append(index)
        if isinstance(self.global_symbol_table[variable],Types.Collection) or isinstance(self.global_symbol_table[variable] , Types.String):

            value = self.global_symbol_table[variable].index(indexs[0].number)

            if len(indexs) > 1:
                if isinstance(value , CollectionNode) or isinstance(value,Types.String) or isinstance(value , StringNode) or isinstance(value , Types.Collection):

                    for _ in indexs[1:]:
                        value = value.index(_.number)
                else:

                    return None , InvalidOperationError(self.file , "Cannot slice a Number Type.")

            return value , None
        
        elif isinstance(self.global_symbol_table[variable] ,Types.HashMap):
            # print("Asdad")
            
        #     if len(indexs) > 1:
        #         return None , RunTimeError(self.file , "squig dose'nt support nested accessing of hashmap currently")
            
            if isinstance(indexs[0] , Types.Number):

                # key = self.global_symbol_table[variable].index_values.get(indexs[0].value , -1)
                if indexs[0].value > len(self.global_symbol_table[variable].key_values) or indexs[0].value < 0:
                    return None , RunTimeError(self.file , "Index out of range while trying to acessing the 'Map'.")
                key = self.global_symbol_table[variable].index_values[indexs[0].value]
                # print("index value is of type number")
                # print(key , "acessing")
                
        #         if key == -1:
        #             return None , RunTimeError(self.file , "Index out of range , while trying to accessing Map data.")
               
                return  Types.Collection(filename=self.file , elements=[key , self.global_symbol_table[variable].key_values.get(key , None )]), None
            
            elif isinstance(indexs[0] , Types.String):
                
                # print("index value is of type string")
                key = indexs[0].string
        #         # print("it's string")
                return self.global_symbol_table[variable].key_values.get(key , None ) , None
        # elif isinstance(self.global_symbol_table[variable] , Types.String):{
        #     if 
        # }
        
        

    def VariableNode(self , node):

        variable = node.variable.value
        
        value , error = self.process(node.factor)

        
        if error:
            return None , error
        
        self.global_symbol_table[variable] = value

        return "" , None
    
    def LetNode(self , node):
        
        variable = node.variable.value
        
        if variable in self.global_symbol_table:
            return None , RedeclarationError(file=self.file , details=f"variable '{variable}' cannot be created more than once." , position=None )
        
        value , error = self.process(node.factor)
        if error:
            return None , error
        self.global_symbol_table[variable] = value

        return "" , None
    
    def FileWriteNode(self , node):
        # need to fix issue
        variable = node.variable.value

        file_content , error = self.process(node.content)
        if error:
            return None , error
        
        if variable in self.global_symbol_table:
            try:                
                self.global_symbol_table[variable].write(file_content.string)
            except:

                return None , WrongFileOperationError(file=self.file , name="IOFileOperationError" , details="check in interpreter in fileWriteNode method for replacing the error in future")
        else:
            return None , WrongFileOperationError(file=self.file , name="IOFileOperationError" , details=f"Trying to write content to a closed file '{self.global_symbol_table[variable].file_name}'.")

        return None, None


    def VariableAccessNode(self , node):

        variable = node.variable.value

        if variable in self.global_symbol_table:
            if isinstance(self.global_symbol_table[variable] , Types.File):
                # print(self.global_symbol_table[variable].content())
                
                try:
                    file = self.global_symbol_table[variable]
                    # print(file.file.read())
                    return file.content() , None
                except:
                    return None , WrongFileOperationError(file=self.file , name="IOFileOperationError" , details=f"Performing unsupported operation for file '{self.global_symbol_table[variable].file_name}'.")
            # elif isinstance(self.global_symbol_table[variable] , Types.HashMap):
            #     return self.global_symbol_table[variable] , None
            return self.global_symbol_table[variable] , None
        else:
            return None , RunTimeError(self.file , f"Variable '{variable}' is undefined.")

    def InputStringNode(self , node):

        string = node.string.value

        data = Types.InputString()
        try:
            result , error = data.value(input(string).strip())
            
        except:
            result , error = data.value("")

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

        # types = "Type : '" + type(node).__name__.replace("Node" , '') +"'"
        types = type(node).__name__.replace("Node" , '')

        return Types.String(string=types , filename=self.file) , None


    def IfNode(self , node):

        cases = node.cases
        else_case = node.else_case

        for condition , statement in cases:
           
            predicate , error = self.process(condition)
            if error:
                return None , error
            if predicate.value == 'true':
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
            
            return number._not_() , None
    

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
        

        return Types.Collection(filename=self.file,elements=elements) , None
    
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
        output , error = function_output.execute(args , self.global_symbol_table) # changing for fix
        
        if error:
            return None , error
        return output , None
    
    def FileNode(self , node):
        
        variable_name = node.filename.variable
        
        file_name , error = self.process(node.filename.factor)
    
        if error:
            return None , error
        
        file_mode , error = self.process(node.mode)

        if error:
            return None , error
        
        try:
            self.global_symbol_table[variable_name.value] = Types.File(file=open(file_name.string , file_mode.string) , file_name=file_name.string)
        
        except:
            return None , WrongFileError(file=self.file , name="FileError", details=f"File '{file_name.string}' does not exists.")

        # print(self.global_symbol_table[variable_name.value].read())

        return None , None
    
    def CloseNode(self , node):

        # file_name , error = self.process(node.filename)
        file = node.filename.variable.value
        self.global_symbol_table[file].close()
        del self.global_symbol_table[file]
        return None , None
    
    def PopNode(self , node):

        # print("Need to complete pop interpertor node")

        variable = node.variable.value
        # local_symbol_table = self.global_symbol_table[variable].key_values

        if variable not in self.global_symbol_table:
            return None , RuntimeError(self.file , f"variable '{variable}' is undefined.")
        
        # print(self.global_symbol_table[variable] , node.index.index , "in Pop Node")
        # print(type(node.index.index[0]) , node.index.index)
        index , error = self.process(node.index.index[0])
        if error:
            return None , error
        
        datastructure = self.global_symbol_table[variable]

        if type(datastructure) == Types.HashMap and type(index) == Types.String:
            datastructure.index_values.remove(index.string)
            return datastructure.key_values.pop(index.string) , None
        
        elif type(datastructure) == Types.HashMap and  type(index) == Types.Number:

            key = datastructure.index_values[index.number]
            del datastructure.index_values[index.number]
            # print(hashmap.key_values , hashmap.index_values)
            # print(type(key))
            return datastructure.key_values.pop(key) , None
        
        elif type(datastructure) == Types.Collection and type(index) == Types.Number:

            if index.number >= len(datastructure.elements):
                return None, RunTimeError(self.file , "Index out of range , in pop statemtent.")
            
            value = datastructure.elements[index.number]
            del datastructure.elements[index.number]
            
            return value , None
        
        elif type(datastructure) == Types.MutableString and type(index) == Types.Number:

            if index.number >= len(datastructure.mut_string):
                
                return None, RunTimeError(self.file , "Index out of range , in pop statemtent.")
            
            value =  datastructure.remove(index.number)
            return value , None

        # print(type(index) , "in pop")
        
    #     if type(index) == Types.Number:
    #         # if index.number >= len(local_symbol_table) or index.number < 0:
    #         #     return None , RunTimeError(self.file , f"Access index out of range")
            
    #         # print(index.number)
    #         print(self.global_symbol_table[variable].index_values)
    #         status = local_symbol_table.pop(str(index.number) , -1)
            
    #         self.global_symbol_table[variable].index_values.pop(index.number , -1)
    #         # print(self.global_symbol_table[variable].index_values)
    #         if status != -1:
    #             return status , None
    #         return Types.Boolean("false") , None
            
            
    #     elif type(index) == Types.String:
    #         # print("index is a string")
    #         status = local_symbol_table.pop(str(index.string) , -1)
    #         if status == -1:
    #             return Types.Boolean("false") , None
            
    #         return status , None

        
    #     # print(type(variable))

    #     return None , None
    
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
        
        interpreter = Interpreter(file , self.global_symbol_table)
    
        output , error = interpreter.process(ast)
        if error:
            return None , error
        
        return output , None
    
    def BooleanNode(self , node):
        
        return Types.Boolean(node.bool) , None
    
    def MutableStringNode(self , node):
        string  = node.string.value
        
        return Types.MutableString(string) , None
    
    def VariableManipulationNode(self , node):
        # print("yeah" , type(node.value) , node.index)
        target_value , error = self.process(node.value)
        # print(type(target_value))
        if error:
            return None , error

        variable = node.variable.value
        variable_value = self.global_symbol_table[variable]

        # print(variable_value , variable)

        if len(node.index) > 1:
            return None , RunTimeError(self.file , "Mutabel String cannot be accessed via '[][]'.")
        
        # if variable not in self.global_symbol_table and type(variable_value) == Types.HashMap:
        #     return None , RunTimeError(self.file , f"Variable '{variable}' is undefined.")
        
        if type(variable_value).__name__ == "String":
            return None , RunTimeError(self.file , f"Cannot Manipulate Immutable string '{variable_value}' stored in variable '{variable}'.")
        
        # print(node.index , "node.index")
        index  , error = self.process(node.index[0])
        # print(index.number)
        if error:
            return None , error

        # if not variable_value.isType(target_value):
        #     return None , RunTimeError(self.file , "Cannot Manipulate a Mutable String with Another type.")

        if type(variable_value).__name__ == "MutableString":
            # print("right")
            value , error = variable_value.include(index.number , target_value.string)
            if error:
                return None , error
            if not value:
                return None , RunTimeError(self.file , f"Manipulation Index out of range for MutableString '{variable_value.string}' stored in variable '{variable}'")
        
        elif type(variable_value) == Types.HashMap:
            # self.global_symbol_table[variable]
            # length = variable_value.length
            # variable_value.index_values[length] = index.string
            
            if type(index) == Types.Number:
                if index.number > len(variable_value.key_values):
                    return None , RunTimeError(self.file , "Index out of range in 'Map' datatype.")
                # if index.number < 0:
                #     return None , RunTimeError(self.file , "Negative indexing is not supported in 'Map' datatype.")
                key = variable_value.index_values[index.number]
                variable_value.key_values[key] = target_value

            elif type(index) == Types.String:
                # print(index.string , "inex")
                variable_value.key_values[index.string] = target_value
                if index.string not in variable_value.index_values:
                    variable_value.index_values.append(index.string)
                # print(variable_value.index_values , variable_value.key_values)
                    return None , None
        #     # print(variable_value.index_values)
            # variable_value.key_values[index.string] = target_value
            # print(target_value , variable_value.key_values[index.string] , type(index))

        elif type(variable_value) == Types.Collection:
            # print(type(variable_value.elements) , variable_value)
            # if type(variable_value.elements).__name__ == 'tuple':
            #     print("it's array")
            # else: 
            variable_value.elements[index.number] = target_value
        #     if error:
        #         return None , error
                
        #     if not value:
        #         return None , RunTimeError(self.file , f"Manipulation Index out of range for Collection '{variable_value.string}' stored in variable '{variable}'")
            
        return None , None
    
    def SwitchNode(self , node):

        condition , error = self.process(node.condition)
        if error:
            return None , error
        
        # print(node.cases)
        cases = node.cases.get(str(condition.value) , False)
        
        if not cases :
            
            default_body , error = self.process(node.default)
            if error:
                return None , error
            
            return  default_body , None
        
        else:
            statement , error = self.process(node.cases.get(str(condition.value)))
            # print(type(node.cases.get(str(condition.value))) , "t")
            if error:
                return None , error
            
            return statement , None
        

        
        # cases = {}



        # for case_key , case_value in node.cases.items():
          
        #     if case_key == condition:
        #         case_value , error = self.process(case_value)

        #         if error:
        #             return None , error
            
        
        #         cases[case_key] = case_value 
        
        # statement = cases.get(str(condition.value))
        
    def no_process(self , node):

        return "No process Node" , None

if __name__ == "__main__":

    file = "<Core>"
    import os , sys


    symbol_table = {

        "String" : Types.BuiltinFunction(file , "String"),

        "Number" : Types.BuiltinFunction(file , "Number"), #has some issue
        "Bool" : Types.BuiltinFunction(file , "Bool"), #has some issue
        "int" : Types.BuiltinFunction(file , "int") ,

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

        "title" : Types.BuiltinFunction(file , "title"),
        "split" : Types.BuiltinFunction(file , "split"),

    }
    
    while True:

        try:
            # file = sys.argv[-1]

            # if not file.endswith(".squig"):
            #      print(f"File : '{file[:file.find('.')]}' is not a squig file.")
            #      break
            # code = open(file).read()
            code = open("testing_final.squig").read()
            # code = input("squig >") 
            code = code.strip()
            if not code:
                break
        except KeyboardInterrupt:
            print("Type 'exit' to close the console.")
            break
        if code == 'exit':
            break
        elif code == 'clear':
            os.system("cls")
            continue
        if not code:
            continue
        lexer = Lexer(file , code)
        tokens , error = lexer.tokenize()

        if error:
            print(error.print())
            break
        
        parser = Parser(tokens , file)
        ast , error = parser.parse()
        
        if error:
            print(error.print())
            break
        
        if not ast.elements:
            break

        interpreter = Interpreter(file , symbol_table)
        result , error = interpreter.process(ast)

        if error:
            print(error.print())
            break
        
        if result:
            for output in result.elements:
                
                if type(output).__name__ == "Collection" and output and output.elements and output.elements[0] == None:

                    if len(output.elements) == 1:#and type(output).__name__ != 'Collection':
                        continue
                    elif len(output.elements) != 1:
                        if output.elements[-1]:
                            print(output.elements[-1].elements)            
            break