from Parser import *
import helper.Types as Types
import sys

class Interpreter:

    def __init__(self, file, global_symbol_table):
        self.file = file
        self.global_symbol_table = global_symbol_table
    
    def travers(self , root , execute_right_subtree = True):
        
        # this function travers the binary operator node inorder to reterview the object.

        if isinstance(root , BinaryOperatorNode):

            # the updated values of the class attribute are not available inside this function , instead it has the old value
            left , error = self.travers(root.left , True)
            if error:
                return None , error
                    
            # do stuff here , if the statement is chained object access
            # the issue for that unexpected behaviour of the object assignmet statement if in this part of the code

            if not isinstance(left , Types.Object) and execute_right_subtree and root.right.variable.value:
                # this statement should execute if the chained object access is not consistent , 
                # meaning it should throw an error , is the object becomes a different type other than object ,
                # but still we are trying to access it with attributes
                # print("trying to access the Non object type as obejct" , root.right.variable.value)
                return None , RunTimeError(self.file , "Trying to use Non Object type as Object")

            if isinstance(left , Types.Object) and execute_right_subtree:
                # print(left.object[root.right.variable.value])
                left = left.object[root.right.variable.value]
            
            if isinstance(left , tuple):
                left = left[0]

            return left , None

        object_ , error = self.process(root)
        if error:
            return None , error
        
        return object_ , None

    def process(self, node):
        
        # getattr return the attribute from the current class , if exists
        method = getattr(self, f"{type(node).__name__}", self.no_process)
        return method(node)

    def ShowNode(self, node):

        # this method is automatically invoked by the ShowNode 
        # in the ast given to the interpreter and returns Null type
        # will print the node which is of type ShowNode.

        lines = []
        for statement in node.statement:
            # print(statement. , "testing")
            line, error = self.process(statement)
            
            if error:
                return None, error

            lines.append(line)

        print(*lines)
        return Types.Null(), None

    def StringNode(self, node):

        # this method is automatically invoked by the StringNode node in ast.
        # it converts the StringNode to StringType which Squig can understand.

        return Types.String(node.string.value, self.file), None

    def NumberNode(self, node):

        # this method is automatically invoked by the NumberNode node in ast
        # it converts the NumberNode to NumberType which squig can understand.

        return Types.Number(node.factor.value), None

    def BinaryOperatorNode(self, node):

        # This method is automatically invoked by th BinaryOperatorNode node in ast.
        # This method is reposible for processing the binary operator statements
        # represeneted in ast, and returns the final evaluated results
        # and it is responsible for interpreting the dot operator statements.
        # in short , all the operators are evaluated in the function

        # The final result of the operation in depended on the type of the operater
        # and the operands , so first we'll capture of the operator
        operator = node.operator.type

        # if the operator is of type dot , then we know we are dealing with objects.
        # if operator == token_dot:

        #     try:
                
        #         # need to include support for accessing attribute
        #         # methods
        #         # assignment

        #         left, error = self.process(node.left)
        #         # print(node , type(left) , type(node.right))
        #         # print(node.scope)
        #         # print("interpretor")
        #         # def inorder_traversal(root):
        #         #     #implement a inorder traversal

        #         #     if isinstance(root.left , BinaryOperatorNode):
        #         #         return
                    
        #         #     left = inorder_traversal(root.left)

        #         #     right = inorder_traversal(root.right)

        #         # print(type(left) ,  left)
        #         if isinstance(node.right, BinaryOperatorNode):
        #             pass
        #         else:
        #             value = left.object[node.right.variable.value]
                    
        #             if isinstance(value, tuple):
        #                 value = value[0]
        #             # elif isinstance(value , Types.UserDefinedFunction):
        #             #     print(type(value))
        #             #     # value
        #             # print(right_operand , "example")
        #             # print(left.object)
        #             if isinstance(value, Types.UserDefinedFunction):
                    
        #                 # print(node.scope)
        #                 args  , error = self.process(node.scope[node.right.variable.value])
        #                 # print(type(args.elements) , args.elements , error)
        #                 # print(node.scope[node.right.variable.value])
        #                 print(args , error)
        #                 if error:
        #                     return None ,error
        #                 return value.execute(args.elements)
                
        #         return value, None

            # except Exception as e:
            #     print(e)
            #     return None, RunTimeError(
            #         self.file, f"Error in dot operator accessing part"
            #     )
            
        # get the result of the expression we need to first convert the left and right operand to 
        # Appropriate type , i.e NumberType , BooleanType , etc.
        # So we'll process the left child of the current node.
        left, error = self.process(node.left)
        if error:
            return None, error
        
        # Similarly we'll process the right child of the current node.
        right, error = self.process(node.right)
        if error:
            return None, error

        error_message = (
            f"cannot be used between {type(left).__name__} and {type(right).__name__}."
        )

        # Based on the type of operation , we perform the appropriate operation.
        # Once the expression is evaluated , the methods i.e 'add' , 'mul' , 'lte' ,etc
        # will return (output , None)

        if operator == token_plus:
            try:
                return left.add(right)
            except:
                return None, RunTimeError(self.file, f"'+' {error_message}")

        elif operator == token_minus:
            try:
                return left.sub(right)
            except:
                return None, RunTimeError(self.file, f"'-' {error_message}")

        elif operator == token_mul:
            try:
                return left.mul(right)
            except:
                return None, RunTimeError(self.file, f"'*' {error_message}")

        elif operator == token_modulo:

            try:
                return left.modulo(right)
            except:
                try:
                    if right.number != 0:
                        return None, RunTimeError(self.file, f"'%' {error_message}")
                except:

                    return None, WrongTypeError(
                        self.file,
                        f"'%' cannot be used between {type(left).__name__} and {type(right).__name__}",
                    )

                return None, RunTimeError(self.file, f"0 is an invalid modulo operand.")

        elif operator == token_divide:
            try:
                return left.div(right_operand=right)
            except:
                try:
                    if right.number != 0:
                        return None, RunTimeError(self.file, f"'/' {error_message}")
                except:
                    return None, WrongTypeError(self.file, f"'/' {error_message}")
                return None, RunTimeError(
                    self.file, f"{left.number} cannot be divided by zero."
                )

        elif operator == token_power:
            try:
                return left.pow(right)
            except:
                return None, RunTimeError(self.file, f"** {error_message}")
        elif operator == token_lt:
            try:
                return left.lt(right)
            except:
                return None, RunTimeError(self.file, f"'<' {error_message}")
        elif operator == token_gt:

            try:
                return left.gt(right)
            except:
                return None, RunTimeError(self.file, f"'>' {error_message}")
        elif operator == token_lte:
            try:
                return left.lte(right)
            except:
                return None, RunTimeError(self.file, f"'<=' {error_message}")
        elif operator == token_gte:
            try:
                return left.gte(right)
            except:
                return None, RunTimeError(self.file, f" '>=' {error_message}")

        elif operator == token_eql:
            try:
                return left.eql(right)
            except:
                return None, RunTimeError(self.file, f"'=' {error_message}")

        elif operator == token_ne:
            try:
                return left.ne(right)
            except:
                return None, RunTimeError(self.file, f"'!=' {error_message}")

        elif operator == token_and:
            try:
                return left._and_(right)
            except:
                return None, RunTimeError(self.file, f"'&' {error_message}")

        elif operator == token_or:
            try:
                return left._or_(right)
            except:
                return None, RunTimeError(self.file, f"'|' {error_message}")
        elif operator == token_bitwise_and:
            try:
                return left.bit_and(right)
            except:
                return None, RunTimeError(self.file, f"'&&' {error_message}")

        elif operator == token_right_shift:

            try:
                return left.bit_right_shift(right)
            except:
                return None, RunTimeError(self.file, f"'>>' {error_message}")

        elif operator == token_bitwise_xor:

            try:
                return left.bit_xor(right)
            except:
                return None, RunTimeError(self.file, f"'^' {error_message}")

        elif operator == token_bitwise_or:
            try:
                return left.bit_or(right)
            except:
                return None, RunTimeError(self.file, f"'||' {error_message}")

        elif operator == token_left_shift:
            try:
                return left.bit_left_shift(right)
            except:
                return None, RunTimeError(self.file, f"'<<' {error_message}")

    def CollectionNode(self, node):

        elements = []

        parent = node.parent

        while parent:
            if isinstance(parent, ForNode):
                break
            else:
                parent = parent.parent

        for element_node in node.elements:
            # print(type(element_node))
            element, error = self.process(element_node)
            if error:
                return None, error

            elements.append(element)

            if isinstance(element_node, BreakNode) or (
                parent and isinstance(parent, ForNode) and parent.is_broken
            ):
                break
                # parent = node.parent
                # while parent :
                #     if isinstance(parent , ForNode):
                #         break
                #     else:
                #         parent = parent.parent

                # # print(type(parent))
                # if parent == None:
                #     return None , RunTimeError("Break can be used only within the loops")
                # else:
                #     parent.is_broken = True

        return Types.Collection(self.file, elements), None

    def HashMapNode(self, node):

        # this function is invoked automatically when the HashMapNode node in ast found.
        # it create a HashMap datastructure and return the Map

        # to construct the hashmap we need to know the list of keys 
        key_values = node.key_value
        index_key = node.index_key

        processed_key_value = {}
        processed_index_key = []

        index = 0
        for key, value in key_values.items():
            processed_key, error = self.process(key_values[key])
            if error:
                return None, error
            processed_index = index_key[index]

            processed_key_value[key] = processed_key
            processed_index_key.append(processed_index)
            index += 1

        return Types.HashMap(processed_key_value, processed_index_key), None

    def CollectionAccessNode(self, node):

        variable = node.variable.value
        value = None

        variable_value_tuple = self.global_symbol_table.get(variable, None)

        if variable_value_tuple == None:
            return None, RunTimeError(
                self.file, f"Collection '{variable}' is undefind."
            )

        indexs = []
        variable_value = variable_value_tuple[0]
        # print(variable_value)

        if (
            not isinstance(variable_value, Types.Collection)
            and not isinstance(variable_value, Types.MutableString)
            and not isinstance(variable_value, Types.HashMap)
            and not isinstance(variable_value, Types.String)
        ):
            return None, WrongTypeError(
                self.file,
                f"variable '{variable}' of type {type(variable_value).__name__} cannot be indexed.",
            )

        for idx in node.index:
            index, error = self.process(idx)
            if error:
                return None, error

            # if not isinstance(variable_value , Types.Collection) and \
            #     not isinstance(variable_value , Types.MutableString) and \
            #     not isinstance(variable_value , Types.HashMap) and \
            #     not isinstance(variable_value , Types.String):
            #     return None , WrongTypeError(self.file , f"variable '{variable}' of type {type(variable_value).__name__} cannot be indexed.")

            # if not isinstance(index , Types.Number) and \
            #     (isinstance(variable_value , Types.Collection) or \
            #     isinstance(variable_value , Types.String)):
            if not isinstance(index, Types.Number):
                return None, WrongTypeError(
                    self.file,
                    f"Type '{type(index).__name__}' connot be used for indexing Collection '{variable}'.",
                )
            indexs.append(index)

        # if isinstance(self.global_symbol_table[variable],Types.Collection) or isinstance(self.global_symbol_table[variable] , Types.String):
        if isinstance(variable_value, Types.Collection) or isinstance(
            variable_value, Types.String
        ):

            # value = self.global_symbol_table[variable].index(indexs[0].number)
            # print(variable_value.index(indexs[0].number))
            value, error = variable_value.index(indexs[0].number)
            if error:
                return None, error

            if len(indexs) > 1:
                if (
                    isinstance(value, CollectionNode)
                    or isinstance(value, Types.String)
                    or isinstance(value, StringNode)
                    or isinstance(value, Types.Collection)
                ):

                    for idx in range(1, len(indexs)):
                        value, error = value.index(indexs[idx].number)
                        # print("testing" , value , error)
                        if error:
                            return None, error
                else:

                    return None, InvalidOperationError(
                        self.file, "Cannot slice a Number Type."
                    )

            return value, None

        # elif isinstance(self.global_symbol_table[variable], Types.MutableString):
        elif isinstance(variable_value, Types.MutableString):

            # value = self.global_symbol_table[variable].string
            # value = variable_value.string

            # if not value:
            if not variable_value.string:
                return None, RunTimeError(
                    self.file, "Cannot slice a empty mutable string"
                )

            # if isinstance(value , Types.MutableString):
            #     value = value.string

            return Types.MutableString(variable_value.string[indexs[0].number]), None

        # elif isinstance(self.global_symbol_table[variable] ,Types.HashMap):
        elif isinstance(variable_value, Types.HashMap):
            # print("Asdad")

            #     if len(indexs) > 1:
            #         return None , RunTimeError(self.file , "squig dose'nt support nested accessing of hashmap currently")

            if isinstance(indexs[0], Types.Number):

                # key = self.global_symbol_table[variable].index_values.get(indexs[0].value , -1)
                # if indexs[0].value > len(self.global_symbol_table[variable].key_values) or indexs[0].value < 0:
                if (
                    indexs[0].value > len(variable_value.key_values)
                    or indexs[0].value < 0
                ):
                    return None, RunTimeError(
                        self.file,
                        "Index out of range while trying to acessing the 'Map'.",
                    )
                # key = self.global_symbol_table[variable].index_values[indexs[0].value]
                key = variable_value.index_values[indexs[0].value]
                # print("index value is of type number")
                # print(key , "acessing")

                #         if key == -1:
                #             return None , RunTimeError(self.file , "Index out of range , while trying to accessing Map data.")
                return (
                    Types.Collection(
                        filename=self.file,
                        elements=[
                            key,
                            variable_value.key_values.get(key, Types.Null()),
                        ],
                    ),
                    None,
                )
                # return  Types.Collection(filename=self.file , elements=[key , self.global_symbol_table[variable].key_values.get(key , None )]), None

            elif isinstance(indexs[0], Types.String):

                # print("index value is of type string")
                key = indexs[0].string
                #         # print("it's string")
                # return self.global_symbol_table[variable].key_values.get(key , None ) , None
                return variable_value.key_values.get(key, Types.Null()), None
        # elif isinstance(self.global_symbol_table[variable] , Types.String):{
        #     if
        # }

        return Types.Null(), None

    def VariableNode(self, node):

        
        is_object = isinstance(node.variable , ObjectAccessNode)
        # print(is_object)
        if not is_object:
            variable = node.variable.value
        else:
            variable = node.variable
        # print(variable , type(node.factor))
        value, error = self.process(node.factor)
        if error:
            return None, error

        parent = node.parent

        object_name = None

        if is_object:
                
            # for assigning new value to object attribute , we should not process the last attribute in the chain
            # forexample -> node.data.data : 20
            # for assigning 20 to node.data.data we should not access the data of node.data
            # instead we should assign the value 20 to node.data
            # so that's why we passed execute_right_subtree = False in traverse function.
            object_name , error = self.travers(node.variable.object , execute_right_subtree = False)
            # print(object_name)
            if error:
                return None , error
            
        else:

            while parent:
                object_name = parent.scope.get(variable, None)
                if not object_name:
                    parent = parent.parent
                else:
                    break
            # print(parent , "\n" , object_name , variable)


        if object_name == None:
            return None, RunTimeError(self.file, f"Variable {variable} is undefined.")
        
        # print(object_name.object["data"])
        # if not object_name[1]: this condition is not checking mutability
        # print(node.variable , is_object)
        if not is_object:
                parent.scope[variable] = (value, object_name[1], object_name[-1])
                # print(parent.scope[variable] , value)
        else:
                attribute = node.variable.object.right.variable.value
                # print(object_name , value , "first")
                object_name.object[attribute] = (value, False , False)

        # else:
        #     return None, RunTimeError(
        #         self.file, f"immutable variable '{variable}' cannot be modified"
        #     )
        # else:
        #     print("constant node")
        # print(object_name[0].object["data"][0].object ,)
        return Types.Null(), None

    def NullNode(self, node):

        return Types.Null(), None

    def LetNode(self, node):

        variable = node.variable.value

        # if variable in self.global_symbol_table:
        #     return None , RedeclarationError(file=self.file , details=f"variable '{variable}' cannot be created more than once." , position=None )
        # if node.factor:
        # print(node.factor)
        value, error = self.process(node.factor)
        if error:
            return None, error

        type_mentioned = None

        if not isinstance(node.type_mentioned, Token):
            type_mentioned = Types.DataType(node.type_mentioned)
        # print(value , "check")
        # else:
        #     value , error = None , None

        if not type_mentioned:

            type_mentioned = Types.DataType(node.type_mentioned.value)

        # current_value_type = Types.DataType(type(value).__name__.lower().strip())

        # if current_value_type.value != "null" and current_value_type.value != type_mentioned.value:
        #     return None , WrongTypeError(self.file , f"'{current_value_type.value}' cannot be assigned to variable '{variable}' of type '{type_mentioned.value}'")

        # self.global_symbol_table[variable] = (value , node.isConstant , type_mentioned)

        if node.parent and isinstance(
            node.parent, BlockLevelNode
        ):  # if not the root node:

            node.parent.scope[variable] = (value, node.isConstant, type_mentioned)
        else:
            # need check this case
            node.scope[variable] = (value, node.isConstant, type_mentioned)

        # print(node.parent.scope)

        return Types.Null(), None

    def FileWriteNode(self, node):
        # need to fix issue
        variable = node.variable.value

        file_content, error = self.process(node.content)
        if error:
            return None, error

        if variable in self.global_symbol_table:
            try:
                self.global_symbol_table[variable].write(file_content.string)
            except:

                return None, WrongFileOperationError(
                    file=self.file,
                    name="IOFileOperationError",
                    details="check in interpreter in fileWriteNode method for replacing the error in future",
                )
        else:
            return None, WrongFileOperationError(
                file=self.file,
                name="IOFileOperationError",
                details=f"Trying to write content to a closed file '{self.global_symbol_table[variable].file_name}'.",
            )

        return Types.Null(), None

    def VariableAccessNode(self, node):
        # print(node , "testing")
        variable = node.variable.value
        members = node.members  # Need to fix this for access nested props

        # variable_value = self.global_symbol_table.get(variable , None) # find the variable in the parent until it is found
        
        parent = node.parent  # need to set the parent for binary operator node
        variable_value = None
        while parent:
            variable_value = parent.scope.get(variable, None)
            if not variable_value:
                parent = parent.parent
            else:
                break
        
        if variable_value != None:
            # if variable in self.global_symbol_table:
            # print(self.global_symbol_table)
            # variable_value = self.global_symbol_table[variable]
            # print("Testing" , variable_value)

            if type(variable_value) != tuple:
                variable_value = (variable_value, False , "Type : null")

            # print(variable_value)
            # if isinstance(self.global_symbol_table[variable][0] , Types.File): # comment this line , because got Type Error
            if isinstance(variable_value[0], Types.File):
                # print(self.global_symbol_table[variable].content())

                try:
                    file = variable_value[0]
                    # print(file.file.read())
                    return file.content(), None
                except:
                    return None, WrongFileOperationError(
                        file=self.file,
                        name="IOFileOperationError",
                        details=f"Performing unsupported operation for file '{self.global_symbol_table[variable].file_name}'.",
                    )
            # elif isinstance(self.global_symbol_table[variable] , Types.HashMap):
            #     return self.global_symbol_table[variable] , None
            # if type(self.global_symbol_table.get(variable , None)) == str : # changed this line
            #     # print("it is a class")
            #     object_members = self.global_symbol_table[self.global_symbol_table[variable][:self.global_symbol_table[variable].find("@")]]
            #     return object_members[members.value] , None
            # print(parent.scope , "\n")
            # if isinstance(variable_value[0] , Types.Object):
            # print(variable_value)
            return variable_value[0], None

        return None, RunTimeError(self.file, f"Variable '{variable}' is undefined.")

    def InputStringNode(self, node):

        string = node.string.value

        data = Types.InputString()
        try:
            result, error = data.value(input(string).strip())
        except KeyboardInterrupt:
            # result , error = data.value("")
            sys.exit(0)
            # return None , None

        if error:
            return None, error
        return result, None

    def AssignmentOperatorNode(self, node):

        variable = node.left.variable
        left, error = self.process(node.left)
        if error:
            return None, error
        right, error = self.process(node.right)
        if error:
            return None, error

        operator = node.operator

        if not variable.value in self.global_symbol_table:
            return None, RunTimeError(self.file, f"Variable {variable} is undefined.")

        if operator.type == token_colon_plus:

            if isinstance(left, Types.String):

                output, error = left.add(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output

            elif isinstance(left, Types.Number):

                output, error = left.add(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output

            elif isinstance(left, Types.Collection):

                output, error = left.add(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output
            else:

                return None, RunTimeError(
                    self.file,
                    f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.",
                )

        elif operator.type == token_colon_minus:
            if isinstance(left, Types.String):

                output, error = left.sub(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output

            elif isinstance(left, Types.Number):

                output, error = left.sub(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output

            elif isinstance(left, Types.Collection):

                output, error = left.sub(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output
            else:
                return None, RunTimeError(
                    self.file,
                    f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.",
                )

        elif operator.type == token_colon_divide:
            if isinstance(left, Types.String):

                output, error = left.div(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output

            elif isinstance(left, Types.Number):

                output, error = left.div(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output
            else:
                return None, RunTimeError(
                    self.file,
                    f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.",
                )

        elif operator.type == token_colon_mul:

            if isinstance(left, Types.String):

                output, error = left.mul(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output

            elif isinstance(left, Types.Number):

                output, error = left.mul(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output

            else:
                return None, RunTimeError(
                    self.file,
                    f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.",
                )

        elif operator.type == token_colon_power:

            if isinstance(left, Types.Number):

                output, error = left.pow(right)
                if error:
                    return None, error

                self.global_symbol_table[variable.value] = output

            else:
                return None, RunTimeError(
                    self.file,
                    f"cannot perfom unsupported operation between {type(left).__name__ , type(right).__name__}.",
                )

        return Types.Null(), None

    def TypesNode(self, node):

        node, error = self.process(node.data)
        if error:
            return None, error

        types = type(node).__name__.replace("Node", "")

        return Types.String(types, self.file), None

    def IfNode(self, node):
        
        cases = node.cases
        else_case = node.else_case

        for condition, statement in cases:
          
            predicate, error = self.process(condition)

            if error:
                return None, error
            if predicate.value == "true":
                block, error = self.process(statement)
                if error:
                    return None, error
                return block, None

        if else_case:
            block, error = self.process(else_case)
            if error:
                return None, error
            return block, None
        
        return Types.Null(), None

    def UnaryOperatorNode(self, node):

        number, error = self.process(node.factor)

        if error:
            return None, error

        if node.operator.type == token_minus:

            number, error = number.mul(Types.Number(-1))
            if error:
                return None, error

        elif node.operator.type == token_not:

            return number._not_(), None

        return number, None

    def StringAccessNode(self, node):

        string = node.string.value

        indexs = []
        for idx in node.indexs:
            index, error = self.process(idx)
            if not isinstance(index, Types.Number):
                return None, WrongTypeError(
                    self.file, f"Unexpected index type found in string '{string}'."
                )
            if error:
                return None, error
            indexs.append(index)

        return Types.String(string[indexs[0].number]), None

    def ForNode(self, node):

        # need to fix the bugs ....

        variable = node.variable.value
        elements = []
        start_value, error = self.process(node.start_value)
        end_value = Types.Number(0)
        step_value = Types.Number(node.step_value)

        if node.end_value:
            end_value, error = self.process(node.end_value)
            if error:
                return None, error

        if node.step_value != 1:

            step_value, error = self.process(node.step_value)

            if error:
                return None, error

        if not end_value.number:

            if isinstance(start_value, Types.String) or isinstance(
                start_value, Types.MutableString
            ):
                is_mutable = isinstance(start_value, Types.String)
                for var in start_value.string:

                    node.scope[variable] = (
                        Types.String(var) if is_mutable else Types.MutableString(var)
                    )
                    body, error = self.process(node.body)
                    if error:
                        return None, error

                    elements.append(body)
                    if node.is_broken:
                        # print(elements)
                        node.is_broken = False
                        break
                # del is_mutable

            elif isinstance(start_value, Types.Number):
                # print("number loop " , type(node))
                for var in range(start_value.number):

                    node.scope[variable] = Types.Number(var)

                    body, error = self.process(node.body)

                    if error:
                        return None, error

                    elements.append(body)

                    if node.is_broken:
                        # print(elements)
                        node.is_broken = False
                        break

            elif isinstance(start_value, Types.Collection):

                for var in start_value.elements:
                    node.scope[variable] = var
                    body, error = self.process(node.body)
                    if error:
                        return None, error
                    elements.append(body)
                    if node.is_broken:
                        # print(elements)
                        node.is_broken = False
                        break

        elif end_value.number:

            for var in range(start_value.number, end_value.number, step_value.number):

                node.scope[variable] = Types.Number(var)
                body, error = self.process(node.body)
                if error:
                    return None, error

                elements.append(body)
                if node.is_broken:
                    node.is_broken = False
                    break

        return Types.Collection(self.file, elements), None

    def DeleteNode(self, node):

        variable = [var.value for var in node.variable]

        for var in node.variable:
            value = self.global_symbol_table.get(var.value, None)
            if value == None:
                return None, RunTimeError(
                    self.file, f"Variable '{var.value}' is  undefined."
                )
            if isinstance(value, Types.BuiltinFunction):
                return None, RunTimeError(
                    self.file, f"Cannot delete buitin method '{var.value}'"
                )

        for var in variable:
            if not var in self.global_symbol_table:
                return None, RunTimeError(
                    self.file, f"Variable '{variable}' is  undefined."
                )

            del self.global_symbol_table[var]

        return Types.Null(), None

    def FunctionNode(self, node):
        # print("testing")
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
        function = Types.UserDefinedFunction(
            self.file, variable, params, body, return_type
        )
        # print("\n" , node.parent)
        node.parent.scope[variable] = function
        # print(variable , type(node))
        # print(node.parent.scope)

        return Types.Null(), None

    def FunctionCallNode(self, node):
        
        # using the name of the function , reterview the FunctionNode object from then scope
        # once reterving the FunctionNode Object , we have access to execute method
        # it is this method that executes the function based on the given args.
        # Current issue in functionCallNode is that , we need to somehow reterview the
        # FunctionNode object from the scope for object statement
        # the current logic of this function works well for ordinary function.

        # First we need to get the name of the function so that we can reterview it's
        # body from the parent scope where it is available

        variable = node.variable.value

        # After getting the name of the function we need to find where this function is decleared
        # so we'll check in the parent scope of the FunctionCallNode, we'll go up the ast tree
        # until we find the function name in parent scope
        # if the function name is not found in the any of the parent scope , it means that 
        # the function is not decleared in the program , so we'll throw an error
        # if the function name is found in any of the scope , we'll get it and use futher

        parent = node.parent

        function_value = None

        while parent:
            function_value = parent.scope.get(variable, None)
            if not function_value:
                parent = parent.parent
            else:
                break
        # if the function name is not found in any of the parent scope , parent will be None.
        if parent == None:
            return None, RunTimeError(self.file, f"Function {variable} is undefined.")

        args = []
        for arg in node.param:
            value, error = self.process(arg)
            if error:
                return None, error
            args.append(value)
        
        # the issue is how do we take the method body function the class
        # and use that to execute it , the execute method is avaible in the functionNode not in functionCallNOde

        # Once the arguments are processed , we'll get the function from the scope from the parent
        function_output = parent.scope[variable]

        # print(type(function_output))

        # object_ = node.parent
        # while not isinstance(object_ , VariableAccessNode):
        #     object_ = object_.left
        
        # print(type(object_))

        # from here there is an issue in the implementation of the code.
        # this current implementation need to be rewritten from here after. 
        
        if isinstance(function_output , FunctionCallNode):
            function_output = parent.parent.scope["Os"][variable]

        output, error = function_output.execute(args)
        # print(type(output))
        if error:
            return None, error

        # if isinstance(output, Types.Collection):
        #     return output, None

        return output, None

    def FileNode(self, node):

        variable_name = node.filename.variable

        file_name, error = self.process(node.filename.factor)

        if error:
            return None, error

        file_mode, error = self.process(node.mode)

        if error:
            return None, error

        try:
            self.global_symbol_table[variable_name.value] = Types.File(
                file=open(file_name.string, file_mode.string),
                file_name=file_name.string,
            )

        except:
            return None, WrongFileError(
                file=self.file,
                name="FileError",
                details=f"File '{file_name.string}' does not exists.",
            )

        # print(self.global_symbol_table[variable_name.value].read())

        return Types.Null(), None

    def CloseNode(self, node):

        # file_name , error = self.process(node.filename)
        file = self.global_symbol_table.get(node.filename.variable.value, None)
        if not file:
            file[0].close()
            del self.global_symbol_table[file]

        return Types.Null(), None

    def PopNode(self, node):

        # Need to fix this bug

        variable = node.variable.value
        datastructure, is_constant, literal_type = self.global_symbol_table.get(
            variable, None
        )
        # print(node.)
        # local_symbol_table = self.global_symbol_table[variable].key_values

        if datastructure == None:
            return None, RuntimeError(self.file, f"variable '{variable}' is undefined.")

        # print(self.global_symbol_table[variable] , node.index.index , "in Pop Node")
        # print(type(node.index.index[0]) , node.index.index)
        # print("testing " , type(node.index))
        index = Types.Number(-1)
        if isinstance(node.index, CollectionAccessNode):

            index, error = self.process(node.index.index[0])
            if error:
                return None, error

        if isinstance(datastructure, Types.HashMap) and isinstance(index, Types.String):
            datastructure.index_values.remove(index.string)
            return datastructure.key_values.pop(index.string), None

        elif isinstance(datastructure, Types.HashMap) and isinstance(
            index, Types.Number
        ):

            key = datastructure.index_values[index.number]
            del datastructure.index_values[index.number]
            # print(hashmap.key_values , hashmap.index_values)
            # print(type(key))
            return datastructure.key_values.pop(key), None

        elif isinstance(datastructure, Types.Collection) and isinstance(
            index, Types.Number
        ):
            if not datastructure.elements:
                return None, RunTimeError(
                    self.file, "Cannot pop from an Empty Collection"
                )

            if index.number >= len(datastructure.elements):
                return None, RunTimeError(
                    self.file, "Index out of range , in pop statemtent."
                )

            value = datastructure.elements[index.number]
            del datastructure.elements[index.number]

            return value, None

        elif isinstance(datastructure[0], Types.MutableString) and isinstance(
            index, Types.Number
        ):

            if index.number >= len(datastructure[0].mut_string):

                return None, RunTimeError(
                    self.file, "Index out of range , in pop statemtent."
                )

            value, error = datastructure[0].remove(index.number)
            if error != None:
                return None, error

            # print("testing" , value)
            return value, None
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

    def UseNode(self, node):

        import os

        module_name = os.path.join(
            os.getcwd(), node.name.string.value.replace(":", "\\")
        )
        code = ""
        isRead = False

        if not module_name.endswith(".squig"):

            try:
                path = module_name + ".squig"
                with open(path) as script:
                    code = script.read()
                    isRead = True
            except Exception as e:

                return None, WrongImportError(
                    self.file, f"Cannot use '{module_name}' as module."
                )

        if not isRead:
            try:
                with open(module_name) as script:
                    code = script.read()
            except Exception as e:

                return None, RunTimeError(
                    self.file, f"file '{module_name}' doesn't exists."
                )

        file = "<" + module_name + ">"
        lexer = Lexer(file, code)
        tokens, error = lexer.tokenize()
        if error:
            return None, error
        parser = Parser(tokens, file)
        ast, error = parser.parse()
        if error:
            return None, error

        interpreter = Interpreter(file, self.global_symbol_table)

        output, error = interpreter.process(ast)
        if error:
            return None, error

        return Types.Null(), None

    def BooleanNode(self, node):

        return Types.Boolean(node.bool), None

    def MutableStringNode(self, node):

        return Types.MutableString(node.string.value), None

    def VariableManipulationNode(self, node):
        # print("yeah" , type(node.value) , node.index)
        target_value, error = self.process(node.value)
        # print(type(target_value))
        if error:
            return None, error

        variable = node.variable.value
        variable_value, is_constant, literal_type = self.global_symbol_table[variable]

        # print(variable_value , variable)

        if len(node.index) > 1:
            return None, RunTimeError(
                self.file, "Mutabel String cannot be accessed via '[][]'."
            )

        # if variable not in self.global_symbol_table and type(variable_value) == Types.HashMap:
        #     return None , RunTimeError(self.file , f"Variable '{variable}' is undefined.")

        if isinstance(variable_value, Types.String):
            return None, RunTimeError(
                self.file,
                f"'{variable}' is a immutable string which cannot be modified.",
            )

        # print(node.index , "node.index")
        index, error = self.process(node.index[0])
        # print(index.number)
        if error:
            return None, error

        # if not variable_value.isType(target_value):
        #     return None , RunTimeError(self.file , "Cannot Manipulate a Mutable String with Another type.")
        # print(type(variable_value) , variable_value)
        if isinstance(variable_value, Types.MutableString):
            # print("right" , target_value)
            if not isinstance(target_value, Types.MutableString):
                return None, WrongTypeError(
                    self.file,
                    f"'{type(target_value).__name__}' cannot be combined with 'MutableString.'",
                )
            value, error = variable_value.include(index.number, target_value.string)
            if error:
                return None, error
            if not value:
                return None, RunTimeError(
                    self.file,
                    f"Manipulation Index out of range for MutableString '{variable_value.string}' stored in variable '{variable}'",
                )

        elif isinstance(variable_value, Types.HashMap):
            # self.global_symbol_table[variable]
            # length = variable_value.length
            # variable_value.index_values[length] = index.string

            if isinstance(index, Types.Number):
                if index.number > len(variable_value.key_values):
                    return None, RunTimeError(
                        self.file, "Index out of range in 'Map' datatype."
                    )
                # if index.number < 0:
                #     return None , RunTimeError(self.file , "Negative indexing is not supported in 'Map' datatype.")
                key = variable_value.index_values[index.number]
                variable_value.key_values[key] = target_value

            elif isinstance(index, Types.String):
                # print(index.string , "inex")
                variable_value.key_values[index.string] = target_value
                if index.string not in variable_value.index_values:
                    variable_value.index_values.append(index.string)
                    # print(variable_value.index_values , variable_value.key_values)
                    return Types.Null(), None
        #     # print(variable_value.index_values)
        # variable_value.key_values[index.string] = target_value
        # print(target_value , variable_value.key_values[index.string] , type(index))

        elif isinstance(variable_value, Types.Collection):
            # print(type(variable_value.elements) , variable_value)
            # if type(variable_value.elements).__name__ == 'tuple':
            #     print("it's array")
            # else:
            variable_value.elements[index.number] = target_value
        #     if error:
        #         return None , error

        #     if not value:
        #         return None , RunTimeError(self.file , f"Manipulation Index out of range for Collection '{variable_value.string}' stored in variable '{variable}'")

        return Types.Null(), None

    def SwitchNode(self, node):

        condition, error = self.process(node.condition)
        if error:
            return None, error

        cases = node.cases.get(str(condition.value), None)

        if not cases:

            default_body, error = self.process(node.default)
            if error:
                return None, error

            return default_body, None

        else:
            statement, error = self.process(node.cases.get(str(condition.value)))
            if error:
                return None, error

            return statement, None

    def ClassNode(self, node):

        class_name = node.class_name
        
        class_body, error = self.process(node.class_body)
        
        # print(node.parent)
        if error:
            return None, error
        
        # print("\nbody" , node.class_body.scope)
        if class_name.value not in node.parent.scope:
            node.parent.scope[class_name.value] = node.class_body.scope.copy()
            # node.parent.scope[class_name.value] = node.class_body.scope
        else:
            return None, RunTimeError(
                self.file, f"class with name {class_name.value} already exists."
            )

        # print("\nbody" , node.class_body.scope)
        # print(node.class_body.scope)
        return Types.Null(), None
        # return node , None

    def ObjectNode(self, node):

        # class_name = node.class_name.value

        class_name = node.class_name.variable.value
        parent = node.parent
        while parent:
            if class_name in parent.scope:
                break
            parent = parent.parent
 
        if parent == None:
            return RunTimeError(self.file , f"Class '{class_name}' is not defined.")
        
        object_body = parent.scope[class_name].copy()
        # print(class_name)
        args_length = len(node.class_name.param)
        if args_length == 0:
            return Types.Object(object_=object_body , class_name=class_name), None
        else:
            args = node.class_name.param
            args_list = [Types.Object(object_=object_body , class_name=class_name)]
            for arg in args:
                processed_arg , error = self.process(arg)
                if error:
                    return None , error
                args_list.append(processed_arg)
            
            constructor = object_body.get(class_name , None)
            if not constructor:
                return None , RunTimeError(self.file , f"Constructor of parameter length {args_length} not found in class {class_name}")
            output , error = constructor.execute(args_list)
            if error:
                return None , error
            
            # print(args_list[0].object)
            return args_list[0] , None
        # object_ = ObjectAccessNode(class_name=class_name)
        # object_.object = object_body
        # return object_ , None
    
    
    def ObjectAccessNode(self , node):

        # Object node contains the should contain the BinaryOpeartor Node.
        # Try to implement it properly or reimplement

        # class_name = node.class_name.value
        # parent = node.parent
        # print(parent.parent.scope["os"][0].object)
        # class_name = node.parent.parent.scope[node.object.left.variable.value]
        
        
        # print(node.object)
        # object_ , error = self.travers(node.object)
        object_ , error = self.travers(node.object , execute_right_subtree=False)
        # print("testing" , object_)
        if error:
            return None , error

        # if the object_memeber is a class_variable then a tuple will be returned to attribute
        # else if the object_member is method then the method will be return to attribute
        # print(type(object_))
        # attribute = object_.object[node.object.right.variable.value]
        attribute = object_.object[node.object.right.variable.value]
        # print(type(attribute) , attribute)
        if isinstance(attribute , Types.UserDefinedFunction):

            function_call = node.object.scope[node.object.right.variable.value]
            args = [object_]

            for arg in function_call.param:
                value , error = self.process(arg)
                if error:
                    return None , error
                args.append(value)
            
            if error:
                return None , error
            
            output , error = attribute.execute(args)
            return output , error
        
        elif isinstance(attribute , Types.Object):
            
            return attribute , None
        
        elif isinstance(attribute , tuple):
            return attribute[0] , None
    
        return attribute , None

    def ClearNode(self, node):

        variable_name = node.variable_name.variable.value
        collection = self.global_symbol_table.get(variable_name, None)

        if collection != None:

            if isinstance(collection, Types.Collection):
                # check this statemenet in newer versions.
                collection.elements.clear()
            elif isinstance(collection, tuple):
                if isinstance(collection[0], Types.Collection):
                    collection[0].elements.clear()
                elif isinstance(collection[0], Types.String) or isinstance(
                    collection[0], Types.MutableString
                ):
                    self.global_symbol_table[variable_name] = Types.Null()
                else:
                    return None, RunTimeError(
                        self.file,
                        f"Cannot clear elements of type {type(collection).__name__}",
                    )
            else:
                return None, RunTimeError(
                    self.file,
                    f"Cannot clear elements of type {type(collection).__name__}",
                )
        else:
            return None, RunTimeError(
                self.file, f"Variable '{variable_name}' is undefined."
            )

        return Types.Null(), None

    def DeepCopyNode(self, node):

        variable = node.value.variable.value

        value, is_constant, literal_value = self.global_symbol_table.get(variable, None)

        if value == None:
            return None, RunTimeError(self.file, f"variable {variable} is undefined")

        # value , is_constant , literal_value = self.global_symbol_table[variable]

        if isinstance(value, Types.Collection):
            return (
                Types.Collection(filename=self.file, elements=value.elements.copy()),
                None,
            )
        elif isinstance(value, Types.MutableString):
            return Types.MutableString(value.string), None

        return None, RunTimeError(
            self.file, "Deep copy is implemented only for collection."
        )

    def TryCatchNode(self, node):
        # print(type(node.try_block_statements) , node.try_block_statements)
        try_statement, error = self.process(node.try_block_statements)
        # catch_block_variable = node.catch_block_variable
        # return None ,  None
        catch_variable = None
        if error:
            # print(node.catch_block_statements)

            # catch_block , error = self.process(CollectionNode(elements=node.catch_block_statements))
            # if error:
            #     return None ,error
            # print("testing" , node.catch_block_statements)

            exception_handled = False
            for catch_statement in node.catch_block_statements:

                # print(catch_statement[-1] , catch_statement)

                expected_error, error_status = self.process(catch_statement[-1])
                if error_status:
                    return None, error_status

                if type(error).__name__ == expected_error.value:
                    catch_variable = catch_statement[1].value
                    self.global_symbol_table[catch_variable] = (
                        error,
                        "type",
                        "is_constant",
                    )
                    catch_block, error = self.process(catch_statement[0])
                    # print(catch_statement)
                    if error:
                        return None, error
                    exception_handled = True
                    break

            #     if error:
            #         return None , error

        if not exception_handled:
            return None, error

        if node.finally_block_statements:
            finally_statement, error = self.process(node.finally_block_statements)
            if error:
                return None, error
        try:
            del self.global_symbol_table[catch_variable]
        except:
            pass
        return Types.Null(), None

    def BreakNode(self, node):
        # print("testing" , type(node.parent.parent.parent.parent))
        parent = node.parent
        while parent:
            if isinstance(parent, ForNode):
                break
            else:
                parent = parent.parent

        # print(type(parent))
        if parent == None:
            return None, RunTimeError("Break can be used only within the loops")
        else:
            parent.is_broken = True

        return Types.Break(), None
    

    def no_process(self, node):
        print("Unknown Node", node)
        return Types.Null(), None


FILE = "<core>"
