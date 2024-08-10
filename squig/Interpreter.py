from Parser import *
import helper.Types as Types
import sys

class Interpreter:

    def __init__(self , file, global_symbol_table):
        self.file = file
        self.global_symbol_table = global_symbol_table

    def process(self , node):
        
        method = getattr(self , f"{type(node).__name__}" , self.no_process)
        # print(method)
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
        return Types.Null() , None
    
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
        error_message = f"cannot be used between {type(left).__name__} and {type(right).__name__}."

        if error:
            return None , error

        if operator == token_plus:
            try:
                return left.add(right)
            except :
                return None , RunTimeError(self.file , f"'+' {error_message}")
        
        elif operator == token_minus:
            try:
                return left.sub(right)
            except :
                return None , RunTimeError(self.file , f"'-' {error_message}")
            
        elif operator == token_mul:
            try:
                return left.mul(right)
            except :
                return None , RunTimeError(self.file , f"'*' {error_message}")
            
        elif operator == token_modulo:
            
            try:
                return left.modulo(right)
            except :
                try:
                    if right.number != 0:
                        return None , RunTimeError(self.file , f"'%' {error_message}")
                except:
                    
                    return None , WrongTypeError(self.file  ,f"'%' cannot be used between {type(left).__name__} and {type(right).__name__}")

                return None , RunTimeError(self.file , f"0 is an invalid modulo operand.")
            
        elif operator == token_divide:
            try:
                return left.div(right_operand = right)
            except :
                try:
                    if right.number != 0:
                        return None , RunTimeError(self.file , f"'/' {error_message}")
                except :
                    # return None , WrongTypeError(self.file  ,f"'/' cannot be used between {type(left).__name__} and {type(right).__name__}")
                    return None , WrongTypeError(self.file  ,f"'/' {error_message}")
                return None , RunTimeError(self.file , f"{left.number} cannot be divided by zero.")
        
        elif operator == token_power:
            try:
                return left.pow(right)
            except :
                return None , RunTimeError(self.file , f"** {error_message}")
        elif operator == token_lt:
            try:
                return left.lt(right)
            except :
                return None , RunTimeError(self.file , f"'<' {error_message}")
        elif operator == token_gt:

            try:
                return left.gt(right)
            except :
                return None , RunTimeError(self.file , f"'>' {error_message}")
        elif operator == token_lte:
            try:
                return left.lte(right)
            except :
                return None , RunTimeError(self.file , f"'<=' {error_message}")
        elif operator == token_gte:
            try:
                return left.gte(right)
            except :
                return None , RunTimeError(self.file , f" '>=' {error_message}")
        
        elif operator == token_eql:
            try:
                return left.eql(right)
            except :
                return None , RunTimeError(self.file , f"'=' {error_message}")
        
        elif operator == token_ne:
            try:
                return left.ne(right)
            except :
                return None , RunTimeError(self.file , f"'!=' {error_message}")
        
        elif operator == token_and:
            try:
                return left._and_(right)
            except :
                return None , RunTimeError(self.file , f"'&' {error_message}")
        
        elif operator == token_or:
            try:
                return left._or_(right)
            except:
                return None , RunTimeError(self.file , f"'|' {error_message}")
        

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
        variable_value = self.global_symbol_table[variable][0]
        # print(type(variable_value[0]))
        # print(type(variable_value))
        # print(node.index)
        for idx in node.index:
            index , error = self.process(idx)
            # if not isinstance(self.global_symbol_table[variable] , Types.Collection):
            # print(type(variable_value) , isinstance(variable_value , Types.MutableString))
            if not isinstance(variable_value , Types.Collection) and \
                not isinstance(variable_value , Types.MutableString) and \
                not isinstance(variable_value , Types.HashMap) and \
                not isinstance(variable_value , Types.String):
                # return None , WrongTypeError(self.file , f"variable '{variable}' of type {type(self.global_symbol_table[variable]).__name__} cannot be indexed.")
                return None , WrongTypeError(self.file , f"variable '{variable}' of type {type(variable_value).__name__} cannot be indexed.")
            
            if not isinstance(index , Types.Number) and \
                (isinstance(variable_value , Types.Collection) or \
                isinstance(variable_value , Types.String)):
                    return None , WrongTypeError(self.file , f"Type '{type(index).__name__}' connot be used for indexing Collection '{variable}'.")
            if error:
                return None , error
            indexs.append(index)
        
        # if isinstance(self.global_symbol_table[variable],Types.Collection) or isinstance(self.global_symbol_table[variable] , Types.String):
        if isinstance(variable_value,Types.Collection) or \
            isinstance(variable_value, Types.String):
            
            # value = self.global_symbol_table[variable].index(indexs[0].number)
            value = variable_value.index(indexs[0].number)

            if len(indexs) > 1:
                if isinstance(value , CollectionNode) or isinstance(value,Types.String) or isinstance(value , StringNode) or isinstance(value , Types.Collection):

                    for _ in indexs[1:]:
                        value = value.index(_.number)
                else:

                    return None , InvalidOperationError(self.file , "Cannot slice a Number Type.")

            return value , None
        
        # elif isinstance(self.global_symbol_table[variable], Types.MutableString):
        elif isinstance(variable_value, Types.MutableString):


            # value = self.global_symbol_table[variable].string
            value = variable_value.string
            if not value:
                return None , RunTimeError(self.file , "Cannot slice a empty string")
            
            if type(value) == Types.MutableString:
                value = value.string
            return Types.MutableString(value[indexs[0].number]) , None
        
        # elif isinstance(self.global_symbol_table[variable] ,Types.HashMap):
        elif isinstance(variable_value ,Types.HashMap):
            # print("Asdad")
            
        #     if len(indexs) > 1:
        #         return None , RunTimeError(self.file , "squig dose'nt support nested accessing of hashmap currently")
            
            if isinstance(indexs[0] , Types.Number):

                # key = self.global_symbol_table[variable].index_values.get(indexs[0].value , -1)
                # if indexs[0].value > len(self.global_symbol_table[variable].key_values) or indexs[0].value < 0:
                if indexs[0].value > len(variable_value.key_values) or indexs[0].value < 0:
                    return None , RunTimeError(self.file , "Index out of range while trying to acessing the 'Map'.")
                # key = self.global_symbol_table[variable].index_values[indexs[0].value]
                key = variable_value.index_values[indexs[0].value]
                # print("index value is of type number")
                # print(key , "acessing")
                
        #         if key == -1:
        #             return None , RunTimeError(self.file , "Index out of range , while trying to accessing Map data.")
                return  Types.Collection(filename=self.file , elements=[key , variable_value.key_values.get(key , Types.Null() )]), None
                # return  Types.Collection(filename=self.file , elements=[key , self.global_symbol_table[variable].key_values.get(key , None )]), None
            
            elif isinstance(indexs[0] , Types.String):
                
                # print("index value is of type string")
                key = indexs[0].string
        #         # print("it's string")
                # return self.global_symbol_table[variable].key_values.get(key , None ) , None
                return variable_value.key_values.get(key , Types.Null() ) , None
        # elif isinstance(self.global_symbol_table[variable] , Types.String):{
        #     if 
        # }

        return Types.Null() , None
        

    def VariableNode(self , node):

        variable = node.variable.value
        members = node.members
        value , error = self.process(node.factor)
        
        
        if error:
            return None , error
        
        object_name = self.global_symbol_table.get(variable , -1)
        if object_name == -1:
            return None , RunTimeError(self.file , f"Variable {variable} is undefined.")

        # if  type(object_name) == Types.String and "@" not in object_name.value:
            
        #     self.global_symbol_table[variable] = value
        
        # elif type(self.global_symbol_table[object_name[:object_name.find("@")]]) == dict:

        #     object_member = self.global_symbol_table[object_name[:object_name.find("@")]]
        #     object_member[members.value] = value
        # else:
        if not object_name[1]:
            # current_value_type = type(value).__name__.lower().strip()

            # if current_value_type == "boolean" :
            #     current_value_type = "bool"

            # if current_value_type != object_name[-1].value:
            #     type_mentioned  = object_name[-1].value
            #     type_mentioned = type_mentioned if type_mentioned != "bool" else "boolean"
            #     return None , WrongTypeError(self.file , f"'{current_value_type}' cannot be assigned to variable '{variable}' of type '{type_mentioned}'")
            self.global_symbol_table[variable] = (value , object_name[1] , object_name[-1])
        else:
            return None , RunTimeError(self.file , f"immutable variable '{variable}' cannot be modified")
        # else:
        #     print("constant node")
        return Types.Null() , None
    
    def NullNode(self , node):

        return Types.Null() , None
    
    def LetNode(self , node):
        
        variable = node.variable.value
        
        # if variable in self.global_symbol_table:
        #     return None , RedeclarationError(file=self.file , details=f"variable '{variable}' cannot be created more than once." , position=None )
        # if node.factor:
        # print(node.factor)
        value , error = self.process(node.factor)
        type_mentioned = None



        if type(node.type_mentioned) != Token:
            type_mentioned = Types.DataType(node.type_mentioned)
        # print(value , "check")
        # else:
        #     value , error = None , None

        if error:
            return None , error
        
        if not type_mentioned:

            type_mentioned = Types.DataType(node.type_mentioned.value)

        # current_value_type = Types.DataType(type(value).__name__.lower().strip())
        
        # if current_value_type.value != "null" and current_value_type.value != type_mentioned.value:
        #     return None , WrongTypeError(self.file , f"'{current_value_type.value}' cannot be assigned to variable '{variable}' of type '{type_mentioned.value}'")

        
        self.global_symbol_table[variable] = (value , node.isConstant , type_mentioned)
        
        return Types.Null() , None
    
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

        return Types.Null(), None


    def VariableAccessNode(self , node):

        variable = node.variable.value
        members = node.members # Need to fix this for access nested props

        if variable in self.global_symbol_table:
            # print(self.global_symbol_table)
            variable_value = self.global_symbol_table[variable]
            # print("Testing" , variable_value)
            if type(variable_value) != tuple:
                variable_value = (variable_value , False )

            # print(variable_value)
            # if isinstance(self.global_symbol_table[variable][0] , Types.File): # comment this line , because got Type Error
            if isinstance(variable_value[0] , Types.File):
                # print(self.global_symbol_table[variable].content())
                
                try:
                    file = variable_value[0]
                    # print(file.file.read())
                    return file.content() , None
                except:
                    return None , WrongFileOperationError(file=self.file , name="IOFileOperationError" , details=f"Performing unsupported operation for file '{self.global_symbol_table[variable].file_name}'.")
            # elif isinstance(self.global_symbol_table[variable] , Types.HashMap):
            #     return self.global_symbol_table[variable] , None
            # if type(self.global_symbol_table.get(variable , None)) == str : # changed this line
            #     # print("it is a class")
            #     object_members = self.global_symbol_table[self.global_symbol_table[variable][:self.global_symbol_table[variable].find("@")]]
            #     return object_members[members.value] , None

            return variable_value[0] , None
        else:
            return None , RunTimeError(self.file , f"Variable '{variable}' is undefined.")

    def InputStringNode(self , node):

        string = node.string.value

        data = Types.InputString()
        try:
            result , error = data.value(input(string).strip())
        except KeyboardInterrupt:
            # result , error = data.value("")
            sys.exit(0)
            # return None , None

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
            
        return Types.Null() , None

    

    def TypesNode(self , node):

        node , error  = self.process(node.data)
        if error:
            return None , error

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
        
        return Types.Null() ,None

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
        

        return Types.String(string[indexs[0].number]) , None
    
    def ForNode(self , node):

        # need to fix the bugs ....

        variable = node.variable.value
        elements = []
        start_value , error = self.process(node.start_value)
        end_value = Types.Number(0)
        step_value = Types.Number(node.step_value)

        if node.end_value:
            end_value , error = self.process(node.end_value)
            if error:
                return None , error
            
        if node.step_value != 1:

            step_value , error = self.process(node.step_value)

            if error:
                return None , error
        
        if not end_value.number:

            if type(start_value) == Types.String or type(start_value) == Types.MutableString:
                is_mutable = type(start_value) == Types.String
                for var in start_value.string:

                    self.global_symbol_table[variable] = Types.String(var) if is_mutable else Types.MutableString(var)
                    body , error = self.process(node.body)
                    if error:
                        return None , error
                    
                    elements.append(body)
                del is_mutable
            
            elif type(start_value) == Types.Number:
                
                for var in range(start_value.number):

                    self.global_symbol_table[variable] = Types.Number(var)
                    body , error = self.process(node.body)
                    if error:
                        return None , error
                    
                    elements.append(body)
            
            elif type(start_value) == Types.Collection:

                for var in start_value.elements:
                    self.global_symbol_table[variable] = var
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

        return Types.Null() , None
    

    def FunctionNode(self , node):     
        variable = node.variable.value

        return_type = node.type_mentioned
        if type(return_type) != Token:
            return_type = Types.DataType(node.type_mentioned)
        else:
            return_type = Types.DataType(node.type_mentioned.value)
        
        body = node.body
        params = []

        for param in node.param:
            params.append(param.value)

        # if error:
        #     return None , error
        
        function =  Types.UserDefinedFunction(self.file , variable , params  , body , return_type)

        self.global_symbol_table[variable] = function 
        
        return  Types.Null() , None 


        
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

        # print(self.global_symbol_table[variable])
        function_output  = self.global_symbol_table[variable]
        output , error = function_output.execute(args , self.global_symbol_table) # changing for fix
        # print(type(output) , "asdasd")
        # if output and function_output.type_mentioned.value != "null" and  type(output.elements[0]).__name__.lower().strip() != function_output.type_mentioned.value:
        #     return None , WrongTypeError(self.file , f"Mistached return type '{function_output.type_mentioned.value}' found in function '{variable}'.")
        if error:
            return None , error
        
        if isinstance(output , Types.Collection):
            return output , None
        
        return output , None
        
        # return output.elements[-1] if isinstance(output , Types.Collection) else output , None
    
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

        return Types.Null() , None
    
    def CloseNode(self , node):

        # file_name , error = self.process(node.filename)
        file = node.filename.variable.value
        self.global_symbol_table[file].close()
        del self.global_symbol_table[file]
        return Types.Null() , None
    
    def PopNode(self , node):

        # Need to fix this bug

        variable = node.variable.value
        # print(node.)
        # local_symbol_table = self.global_symbol_table[variable].key_values

        if variable not in self.global_symbol_table:
            return None , RuntimeError(self.file , f"variable '{variable}' is undefined.")
        
        # print(self.global_symbol_table[variable] , node.index.index , "in Pop Node")
        # print(type(node.index.index[0]) , node.index.index)
        # print("testing " , type(node.index))
        index = Types.Number(-1)
        if type(node.index) == CollectionAccessNode:
            
            index , error = self.process(node.index.index[0])
            if error:
                return None , error
        
        datastructure , is_constant , literal_type = self.global_symbol_table[variable]

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
            if not datastructure.elements:
                return None , RunTimeError(self.file , "Cannot pop from an Empty Collection")
            
            if index.number >= len(datastructure.elements):
                return None, RunTimeError(self.file , "Index out of range , in pop statemtent.")
            
            value = datastructure.elements[index.number]
            del datastructure.elements[index.number]
            
            return value , None
        
        elif type(datastructure[0]) == Types.MutableString and type(index) == Types.Number:

            if index.number >= len(datastructure[0].mut_string):
                
                return None, RunTimeError(self.file , "Index out of range , in pop statemtent.")
            
            value , error =  datastructure[0].remove(index.number)
            if error!= None:
                return None , error
            
            # print("testing" , value)
            return value , None
        # return None , None 

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

        import os
        
        module_name = os.path.join(os.getcwd() , node.name.string.value.replace(":","\\"))
        code = ""
        isRead = False

        if not module_name.endswith('.squig'):
            
            try:
                path = module_name + ".squig"
                with open(path) as script:
                    code = script.read()
                    isRead = True
            except Exception as e:

                return None , WrongImportError(self.file , f"Cannot use '{module_name}' as module.")

        if not isRead:
            try:
                with open(module_name) as script:
                    code = script.read()
            except Exception as e:

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
        variable_value , is_constant , literal_type = self.global_symbol_table[variable]

        # print(variable_value , variable)

        if len(node.index) > 1:
            return None , RunTimeError(self.file , "Mutabel String cannot be accessed via '[][]'.")
        
        # if variable not in self.global_symbol_table and type(variable_value) == Types.HashMap:
        #     return None , RunTimeError(self.file , f"Variable '{variable}' is undefined.")
        
        if type(variable_value) == Types.String:
            return None , RunTimeError(self.file , f"'{variable}' is a immutable string which cannot be modified.")
        
        # print(node.index , "node.index")
        index  , error = self.process(node.index[0])
        # print(index.number)
        if error:
            return None , error

        # if not variable_value.isType(target_value):
        #     return None , RunTimeError(self.file , "Cannot Manipulate a Mutable String with Another type.")
        # print(type(variable_value) , variable_value)
        if type(variable_value) == Types.MutableString:
            # print("right" , target_value)
            if type(target_value) != Types.MutableString:
                return None , WrongTypeError(self.file , f"'{type(target_value).__name__}' cannot be combined with 'MutableString.'")
            value , error = variable_value.include(index.number , target_value.string)
            if error:
                return None , error
            if not value :
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
                    return Types.Null() , None
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
            
        return Types.Null() , None
    
    def SwitchNode(self , node):

        condition , error = self.process(node.condition)
        if error:
            return None , error
        
        cases = node.cases.get(str(condition.value) , False)
        
        if not cases :
            
            default_body , error = self.process(node.default)
            if error:
                return None , error
            
            return  default_body , None
        
        else:
            statement , error = self.process(node.cases.get(str(condition.value)))
            if error:
                return None , error
            
            return statement , None

    # def ClassNode(self , node):

    #     class_name = node.class_name.value
    #     class_scope = {}
    #     interpreter = Interpreter(self.file , class_scope)
    #     result , error = interpreter.process(node.class_body)
    #     if error:
    #         return None , error

    #     if class_name not in self.global_symbol_table:
    #         self.global_symbol_table[class_name] = class_scope
    #     else:
    #         return None , RunTimeError(self.file , f"{class_name} cannot be used again for declaring a class.")
    #     return None , None
    

    def ClearNode(self , node):

        variable_name = node.variable_name.variable.value
        if variable_name in self.global_symbol_table:
            collection = self.global_symbol_table[variable_name]
            if type(collection) == Types.Collection:
                # check this statemenet in newer versions.
                collection.elements.clear()
            elif type(collection) == tuple:
                if type(collection[0]) == Types.Collection:
                    collection[0].elements.clear()
                elif type(collection[0]) == Types.String:
                    self.global_symbol_table[variable_name] = Types.Null()
                elif type(collection[0]) == Types.MutableString:
                    self.global_symbol_table[variable_name] =Types.Null()
                else:
                    return None , RunTimeError(self.file , f"Cannot clear elements of type {type(collection).__name__}")
            else:
                return None , RunTimeError(self.file , f"Cannot clear elements of type {type(collection).__name__}")
        else:
            return None , RunTimeError(self.file , f"Variable '{variable_name}' is undefined.")
                
        return Types.Null() , None
    
    def DeepCopyNode(self , node):
        
        variable = node.value.variable.value
        if variable not in self.global_symbol_table:
            return None , RunTimeError(self.file , f"variable {variable} is undefined")
        
        value , is_constant , literal_value = self.global_symbol_table[variable]
        if isinstance(value , Types.Collection):
            return Types.Collection(filename=self.file , elements=value.elements.copy()) , None

        return None , RunTimeError(self.file , "Deep copy is implemented only for collection.")
    
    

    # def ObjectNode(self , node):

    #     object_name = node.object_name.value
    #     class_name = node.class_name.value

    #     if object_name not in self.global_symbol_table :
    #         self.global_symbol_table[object_name] = class_name+"@"+ str(id(self.global_symbol_table[class_name]))
    
    #     return None , None
    
    # def ObjectPropAccessNode(self , node):

    #     object_name = node.object_name.value
    #     prop_name = node.prop_name.value

    #     if object_name not in self.global_symbol_table :
    #         return None , RuntimeError(self.file , f"Object '{object_name}' is undefined.")
        
    #     elif type(self.global_symbol_table[self.global_symbol_table[object_name][:self.global_symbol_table[object_name].find("@")]]) != dict:
    #         # print(type(self.global_symbol_table[self.global_symbol_table[object_name][:self.global_symbol_table[object_name].find("@")]]))
    #         return None , RunTimeError(self.file , f"'{object_name}' is not a valid class.")
        
    #     object_members = self.global_symbol_table[self.global_symbol_table[object_name][:self.global_symbol_table[object_name].find("@")]]
        
    #     needed_member = object_members[prop_name]
    #     # print(self.global_symbol_table)
    #     return  needed_member , None

    def no_process(self , node):

        return Types.Null() , None

FILE = "<core>"
