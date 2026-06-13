from llvmlite import ir
from helper.Token import token_plus, token_minus, token_mul, token_divide, token_modulo, token_or, token_and # Arithmetics
from helper.Token import token_bitwise_and, token_bitwise_or, token_bitwise_not, token_bitwise_xor # BitWise Arithmetics
from helper.Token import token_int # Data Types

from Environment import Environment

class Compiler:
    def __init__(self):

        self.module = ir.Module(name="main")
        self.builder = None
        self.func = None

        self.environment: Environment = Environment()

        self.zero = ir.Constant(ir.IntType(32), 0) # For or, and comparison

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
        if node.operator.type == token_minus:
            return self.builder.sub(left, right)
        if node.operator.type == token_mul:
            return self.builder.mul(left, right)
        if node.operator.type == token_divide:
            return self.builder.sdiv(left, right)
        if node.operator.type == token_modulo:
            return self.builder.srem(left, right)
        if node.operator.type == token_or: # true | false = true [LOGICAL OR]
            left_bool = self.builder.icmp_signed('!=', left, self.zero)
            right_bool = self.builder.icmp_signed('!=', right, self.zero)

            return self.builder.or_(left_bool, right_bool)
        if node.operator.type == token_and: # true & true = true [LOGICAL AND]
            left_bool = self.builder.icmp_signed('!=', left, self.zero)
            right_bool = self.builder.icmp_signed('!=', right, self.zero)

            return self.builder.and_(left_bool, right_bool)

        # BitWise Arithmetics
        if node.operator.type == token_bitwise_and:
            return self.builder.and_(left, right)
        if node.operator.type == token_bitwise_or:
            return self.builder.or_(left, right)
        if node.operator.type == token_bitwise_not:
            return self.builder.not_(left)
        if node.operator.type == token_bitwise_xor:
            return self.builder.xor(left, right)

        raise Exception("Unknown operator")

    def CollectionNode(self, node):

        last = ir.Constant(ir.IntType(32), 0)

        for element in node.elements:
            last = self.process(element)

        return last
    
    def LetNode(self, node):
        name: str = node.variable.value
        value = self.process(node.factor)
        type: ir.Type = value.type

        ptr = self.builder.alloca(type, name=name)
        self.builder.store(value, ptr)
        self.environment.set(name=name, value=ptr, type=type)

        return value

    def VariableAccessNode(self, node):
        ptr, type = self.environment.get(node.variable.value)

        return self.builder.load(ptr)