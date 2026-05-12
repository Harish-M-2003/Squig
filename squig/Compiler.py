from llvmlite import ir
from helper.Token import token_plus

class Compiler:
    def __init__(self):

        self.module = ir.Module(name="main")
        self.builder = None
        self.func = None

    def process(self, node):

        method = getattr(
            self,
            type(node).__name__,
            self.no_process
        )

        return method(node)

    def no_process(self, node):
        raise Exception(f"No handler for {type(node).__name__}")

    def compile(self, node):

        func_type = ir.FunctionType(
            ir.IntType(32),
            []
        )

        self.func = ir.Function(
            self.module,
            func_type,
            name="main"
        )

        block = self.func.append_basic_block("entry")

        self.builder = ir.IRBuilder(block)

        result = self.process(node)

        self.builder.ret(result)

        return self.module
    
    def NumberNode(self, node):
        return ir.Constant(
            ir.IntType(32),
            node.factor.value
        )
    
    def BinaryOperatorNode(self, node):

        left = self.process(node.left)
        right = self.process(node.right)

        if node.operator.type == token_plus:
            return self.builder.add(left, right)

        raise Exception("Unknown operator")

    def CollectionNode(self, node):

        last = ir.Constant(ir.IntType(32), 0)

        for element in node.elements:
            last = self.process(element)

        return last
        