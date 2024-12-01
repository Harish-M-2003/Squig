from helper.Token import *
class BlockLevelNode:

    def __init__(self, parent):
        self.parent = parent
        self.scope = {}
class NonBlockLevelNode:

    def __init__(self, parent):

        self.parent = parent
        self.scope = {}
class NumberNode(NonBlockLevelNode):

    def __init__(self, factor, parent=None):

        self.factor = factor
        super().__init__(parent)

    def __repr__(self):

        return f"{self.factor.value}"
class ClearNode(NonBlockLevelNode):

    def __init__(self, variable_name, parent=None):

        self.variable_name = variable_name
        super().__init__(parent)

    def __repr__(self):

        return f"ClearNode({self.variable_name})"
class StringNode(NonBlockLevelNode):

    def __init__(self, string, parent=None):

        self.string = string
        super().__init__(parent)

    def __repr__(self):

        return f'"{self.string.value}"'
class InputStringNode(NonBlockLevelNode):

    def __init__(self, string, parent=None):

        self.string = string
        super().__init__(parent)

    def __repr__(self):

        return f"{self.string.value}"
class BinaryOperatorNode(NonBlockLevelNode):

    def __init__(self, left, operator, right, parent=None):

        self.left = left
        self.operator = operator
        self.right = right
        super().__init__(parent)

    def __repr__(self):

        return f"({self.left},{self.operator},{self.right})"
class AssignmentOperatorNode(BinaryOperatorNode, NonBlockLevelNode):

    def __init__(self, parent=None):

        super().__init__(parent)
class VariableNode(NonBlockLevelNode):

    def __init__(self, variable, factor, members=None, parent=None):

        self.variable = variable
        self.factor = factor
        self.members = members
        super().__init__(parent)

    def __repr__(self):

        return f"{self.variable} : {self.factor}"
class VariableAccessNode(NonBlockLevelNode):

    def __init__(self, variable, members=None, parent=None):

        self.variable = variable
        self.members = members
        super().__init__(parent)

    def __repr__(self):
        return f"{self.variable.value}"
class UnaryOperatorNode(NonBlockLevelNode):

    def __init__(self, operator, factor, parent=None):

        self.operator = operator
        self.factor = factor
        super().__init__(parent)

    def __repr__(self):

        if self.operator.type == token_minus:
            return "-" + f"{self.factor.factor.value}"

        elif self.operator.type == token_not:
            return "! " + f"{self.factor}"
class IfNode(BlockLevelNode):

    def __init__(self, cases, else_case, parent=None):

        self.cases = cases
        self.else_case = else_case
        super().__init__(parent)

    def __repr__(self):

        return f"{self.cases} , {self.else_case}"
class CollectionNode(BlockLevelNode):

    def __init__(self, elements, parent=None):

        self.elements = elements
        super().__init__(parent)

    def __repr__(self):

        return f"{self.elements}".replace("]", "}").replace("(", "[")
class CollectionAccessNode(BlockLevelNode):

    def __init__(self, variable, index, parent=None):

        self.variable = variable
        self.index = index
        super().__init__(parent)

    def __repr__(self):
        return f"{self.variable}:{self.index}"
class StringAccessNode(NonBlockLevelNode):

    def __init__(self, string, indexs, parent=None):

        self.string = string
        self.indexs = indexs
        super().__init__(parent)
class DeleteNode(NonBlockLevelNode):

    def __init__(self, variable, parent=None):
        self.variable = variable
        super().__init__(parent)

    def __repr__(self):

        return f"DeleteNode({self.variable})"
class ForNode(BlockLevelNode):

    def __init__(self, variable, start, end, step, body, multi_value, parent=None):

        self.variable = variable
        self.start_value = start
        self.end_value = end
        self.step_value = step
        self.body = body
        self.multi_value = multi_value
        super().__init__(parent)

    def __repr__(self):

        return f"ForNode({self.variable},{self.start_value},{self.end_value},{self.step_value},{self.body})"
class FunctionNode(BlockLevelNode):

    def __init__(self, variable, param, body, type_mentioned, parent=None):

        self.variable = variable
        self.param = param
        self.body = body
        self.type_mentioned = type_mentioned
        super().__init__(parent)

    def __repr__(self):

        return f"FunctionNode({self.variable} , {self.param} , {self.body})"
class FunctionCallNode(NonBlockLevelNode):

    def __init__(self, variable, param=[], parent=None):

        self.variable = variable
        self.param = param
        super().__init__(parent)

    def __repr__(self):

        return f"FunctionCallNode({self.variable} , {self.param})"
class TypesNode(NonBlockLevelNode):

    def __init__(self, data, parent=None):

        self.data = data
        super().__init__(parent)
class UseNode(NonBlockLevelNode):

    def __init__(self, name, parent=None):

        self.name = name
        super().__init__(parent)

    def __repr__(self):

        return f"{self.name}"
class BooleanNode(NonBlockLevelNode):

    def __init__(self, value, parent=None):

        self.bool = value
        super().__init__(parent)

    def __repr__(self):

        return f"BooleanNode({self.bool})"
class ReturnNode(NonBlockLevelNode):

    def __init__(self, return_value, parent=None):

        self.value = return_value
        super().__init__(parent)

    def __repr__(self):

        return f"ReturnNode({self.value})"
class ShowNode(NonBlockLevelNode):

    def __init__(self, statement, parent=None):

        self.statement = statement
        super().__init__(parent)

    def __repr__(self):

        return f"ShowNode({self.statement})"
class LetNode(NonBlockLevelNode):

    def __init__(self, variable, expression, isConstant, type_mentioned, parent=None):

        self.variable = variable
        self.factor = expression
        self.isConstant = isConstant
        self.type_mentioned = type_mentioned
        super().__init__(parent)

    def __repr__(self):

        return f"LetNode({self.variable})"
class FileNode(NonBlockLevelNode):

    def __init__(self, filename, mode, parent=None):

        self.filename = filename
        self.mode = mode
        super().__init__(parent)

    def __repr__(self):

        return f"FileNode({self.filename} , {self.mode})"
class CloseNode(NonBlockLevelNode):

    def __init__(self, file, parent=None):

        self.filename = file
        super().__init__(parent)

    def __repr__(self):

        return f"close({self.filename })"
class FileWriteNode(NonBlockLevelNode):

    def __init__(self, variable, content, parent=None):

        self.variable = variable
        self.content = content
        super().__init__(parent)

    def __repr__(self):

        return f"FileWriteNode ( {self.variable } , {self.content} )"
class SwitchNode(BlockLevelNode):

    def __init__(self, condition, default_body, cases={}, parent=None):

        self.condition = condition
        self.cases = cases
        self.default = default_body
        super().__init__(parent)

    def __repr__(self):

        return f"SwitchNode({self.condition} , {self.cases})"
class HashMapNode(BlockLevelNode):

    def __init__(self, parent=None):

        self.key_value = {}
        self.index_key = []
        super().__init__(parent)

    def __repr__(self):

        return f"{self.key_value}".replace(")", "}").replace("(", "{")
class MutableStringNode(NonBlockLevelNode):

    def __init__(self, string, parent=None):

        self.string = string
        super().__init__(parent)

    def __repr__(self):

        return f"MutableString({self.string})"
class VariableManipulationNode(NonBlockLevelNode):

    def __init__(self, variable, index, value, parent=None):

        self.variable = variable
        self.index = index
        self.value = value
        super().__init__(parent)

    def __repr__(self):

        return f"VariableManipulationNode({self.variable , self.index , self.value})"
class PopNode(NonBlockLevelNode):

    def __init__(self, variable, index=None, parent=None):

        self.variable = variable
        self.index = index
        super().__init__(parent)
class NullNode(NonBlockLevelNode):

    def __init__(self, parent=None):

        super().__init__(parent)

    def __repr__(self):
        return "null"
class DeepCopyNode(NonBlockLevelNode):

    def __init__(self, value, parent=None):
        self.value = value
        super().__init__(parent)

    def __repr__(self):

        return f"{self.value}"
class TryCatchNode(BlockLevelNode):

    def __init__(
        self,
        try_block_statements,
        catch_block_statements,
        finally_block_statements=None,
        parent=None,
    ):

        self.try_block_statements = try_block_statements
        self.catch_block_statements = catch_block_statements
        # self.catch_block_variable = catch_block_variable
        self.finally_block_statements = finally_block_statements
        super().__init__(parent)


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
