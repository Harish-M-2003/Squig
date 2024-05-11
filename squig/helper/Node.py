from helper.Token import * 

class NumberNode:

    def __init__(self,factor):

        self.factor = factor

    def __repr__(self):

        return f"{self.factor.value}"
    
class ClearNode:

    def __init__(self , variable_name):

        self.variable_name = variable_name
    
    def __repr__(self):

        return f"ClearNode({self.variable_name})"

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

    def __init__(self,variable , factor , members = None):

        self.variable = variable
        self.factor = factor
        self.members = members

    def __repr__(self):

        return f"{self.variable} : {self.factor}"

class VariableAccessNode:

    def __init__(self,variable , members = None):

        self.variable = variable
        self.members = members

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

        return f"{self.elements}".replace(']','}').replace('(','[')

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

    def __init__(self , variable , expression , isConstant):

        self.variable = variable
        self.factor = expression
        self.isConstant = isConstant
    
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
    
    def __repr__(self):
        
        return f"close({self.filename })"
    
class FileWriteNode:

    def __init__(self , variable , content):

        self.variable = variable
        self.content = content

    def __repr__(self):

        return f"FileWriteNode ( {self.variable } , {self.content} )"
    
class SwitchNode:

    def __init__(self , condition , default_body , cases = {}):

        self.condition = condition
        self.cases = cases
        self.default = default_body

    def __repr__(self):

        return f"SwitchNode({self.condition} , {self.cases})"

class HashMapNode:

    def __init__(self):

        self.key_value = {}
        self.index_key = []

    def __repr__(self):

        return f"{self.key_value}".replace(')','}').replace('(','{')

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

class NullNode:

    def __repr__(self) -> str:
        return "null"

# class ClassNode:
    
#     def __init__(self , class_name , class_body = []):

#         self.class_name = class_name
#         self.class_body = class_body
    
#     def __repr__(self) -> str:
        
#         return f"Class{self.class_name}"


# class ObjectNode:

#     def __init__(self , object_name , class_name):

#         self.object_name = object_name
#         self.class_name = class_name

# class ObjectPropAccessNode:

#     def __init__(self , object_name , prop_name):

#         self.object_name = object_name
#         self.prop_name = prop_name

        