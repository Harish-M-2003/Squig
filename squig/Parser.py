from Lexer import *
import numpy as np
from helper.Error import *
from helper.Node import *


class Parser:

    def __init__(self, tokens, file):

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
        # try:
        result, error = self.statements()
        # print(result)
        if error:
            return None, error
        return result, None

    # except Exception as e:
    #     print(e)
    #     return None , WrongSyntaxError(self.file , "Error occured due to inconsistent placing of brackets. check in parse function , if you get this is error kindly report this to us by raising an github issue in the repo https://github.com/Harish-M-2003/Squig" )

    def statements(self, parent=None):

        if self.current_token.type == token_eof:
            return CollectionNode(elements=[]), None

        collection_node = CollectionNode(elements=[], parent=None)
        statement, error = self.expression(collection_node)
        # if parent:
        #     statement.parent = parent
        # else:
        #     statement.parent = collection_node
        # print("let Node" , statements)
        if error:
            return None, error

        collection_node.elements.append(statement)

        while self.current_token.type != token_eof:
            # while self.current_token.type == token_newline:
            #     self.next()
            if self.current_token.type == token_eof:
                break

            if self.current_token.type == token_rb:
                #     self.next()
                break

            statement, error = self.expression(collection_node)

            if error:
                return None, error

            # if parent:
            #     statement.parent = parent
            # else:
            #     statement.parent = collection_node

            collection_node.elements.append(statement)

        # print("working for for loop in statement" , statements)
        # collection_node.elements = statements
        collection_node.parent = parent
        # print("example : " , collection_node.elements[0].parent)
        return collection_node, None

    def expression(self, parent=None):

        if self.current_token.type == token_keyword and self.current_token.value in (
            "let",
            "imu",
        ):
            isConstant = self.current_token.value == "imu"

            let_node = LetNode(None, None, None, None)

            self.next()
            if self.current_token.type != token_variable:
                # print(self.current_token)
                return None, WrongSyntaxError(
                    self.file,
                    "Expected a variable after the 'let' keyword.",
                    position=self.current_token.position.copy_position(),
                )

            variable = self.current_token

            self.next()

            if (
                self.current_token.type != token_colon
                and self.current_token.type != token_type_specifier
            ):
                return None, WrongSyntaxError(
                    self.file,
                    f"Expected a ':' after variable '{variable.value}'.",
                    position=self.current_token.position.copy_position(),
                )

            type_mentioned = None
            if self.current_token.type == token_type_specifier:
                self.next()
                type_mentioned = self.current_token
                self.next()
                if self.current_token.type != token_colon:
                    let_node.variable = variable
                    let_node.isConstant = isConstant
                    let_node.type_mentioned = type_mentioned
                    let_node.factor = None
                    let_node.parent = parent
                    return let_node, None

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
            try:
                expression, error = self.expression(let_node)
            except:
                return None, WrongSyntaxError(
                    self.file, "a value must be give after : "
                )

            if not type_mentioned:
                type_mentioned = (
                    type(expression).__name__.replace("Node", "").strip().lower()
                )

            if error:
                return None, error

            let_node.variable = variable
            let_node.isConstant = isConstant
            let_node.type_mentioned = type_mentioned
            let_node.factor = expression
            let_node.parent = parent
            return let_node, None

        if self.current_token.type == token_bitwise_not:
            unary_operator_node = UnaryOperatorNode(None, None)
            operator = self.current_token
            self.next()
            factor, error = self.expression(unary_operator_node)
            if error:
                return None, error
            factor.factor = factor
            factor.operator = operator
            factor.parent = parent
            return factor, None

        left, error = self.logical_expression(parent)

        if error:
            return None, error

        # while self.current_token.type in (token_and , token_or):

        while self.current_token.type in (
            token_bitwise_and,
            token_bitwise_or,
            token_bitwise_xor,
            token_left_shift,
            token_right_shift,
        ):
            operator = self.current_token
            self.next()
            right, error = self.relational_expression(left)
            if error:
                return None, error
            left = BinaryOperatorNode(left, operator, right)
            left.parent = parent
        # print(left , "test")

        # print(left , "expression method")
        left.parent = parent
        return left, None

    def logical_expression(self, parent=None):

        left, error = self.relational_expression(parent)

        if error:
            return None, error

        while self.current_token.type in (token_and, token_or):

            operator = self.current_token
            self.next()
            right, error = self.logical_expression(left)
            if error:
                return None, error
            left = BinaryOperatorNode(left, operator, right)
            left.parent = parent

        # print(left , "expression method")
        left.parent = parent
        return left, None

    def relational_expression(self, parent=None):

        # print("Asdasd" , self.current_token.type)
        if self.current_token.type == token_not:
            self.next()
            relaion, error = self.relational_expression(parent)
            if error:
                return None, error

            unary_operator_node = (
                UnaryOperatorNode(
                    Token(token_type=token_not, token_position=None), relaion
                ),
                None,
            )
            unary_operator_node[0].parent = parent
            return unary_operator_node

        left, error = self.arithmatic_expression(parent)

        if error:
            return None, error

        while self.current_token.type in (
            token_lt,
            token_gt,
            token_lte,
            token_gte,
            token_ne,
            token_eql,
        ):
            operator = self.current_token
            self.next()
            if self.current_token.type in (
                token_lt,
                token_gt,
                token_lte,
                token_gte,
                token_ne,
                token_eql,
            ):
                return None, InvalidOperationError(
                    self.file,
                    f"Invalid operator used in relational statement.",
                    position=self.current_token.position.copy_position(),
                )
            right, error = self.arithmatic_expression(left)

            if error:
                return None, error
            left = BinaryOperatorNode(left, operator, right)
            left.parent = parent

        return left, None

    def arithmatic_expression(self, parent=None):

        left, error = self.term(parent)
        if error:
            return None, error

        while self.current_token.type in (token_plus, token_minus):
            operator = self.current_token
            self.next()
            right, error = self.term(left)
            if error:
                return None, error
            left = BinaryOperatorNode(left, operator, right)
            left.parent = parent

        left.parent = parent
        return left, None

    def term(self, parent=None):

        left, error = self.factor(parent)
        if error:
            return None, error

        while self.current_token.type in (token_mul, token_divide, token_modulo):
            operator = self.current_token
            self.next()
            right, error = self.factor(left)
            if error:
                return None, error
            left = BinaryOperatorNode(left, operator, right)
            left.parent = parent

        left.parent = parent
        return left, None

    def factor(self, parent=None):

        if self.current_token.type in (token_plus, token_minus):
            operator = self.current_token
            self.next()
            factor, error = self.factor(parent)
            if error:
                return None, error
            unary_operator_node = UnaryOperatorNode(operator, factor)
            unary_operator_node.parent = parent
            return unary_operator_node, None

        power, error = self.power(parent)
        if error:
            return None, error
        return power, None

    def power(self, parent=None):
        atom_rule, error = self.atom(parent)
        if error:
            return None, error

        while self.current_token.type == token_power:
            operator = self.current_token
            self.next()
            factor, error = self.factor(atom_rule)
            if error:
                return None, error
            atom_rule = BinaryOperatorNode(atom_rule, operator, factor)
            atom_rule.parent = parent

        atom_rule.parent = parent
        return atom_rule, None

    def call(self, variable, parent=None):

        if self.current_token.type != token_lb:
            return None, WrongSyntaxError(
                self.file,
                "Expected '{'" + f" after {variable.value} function call.",
                position=self.current_token.position.copy_position(),
            )

        self.next()

        if self.current_token.type == token_rb:
            self.next()
            function_call_node = FunctionCallNode(variable)
            function_call_node.parent = parent
            return function_call_node, None

        arg, error = self.expression(parent)
        if error:
            return None, error

        params = [arg]

        while self.current_token.type == token_comma:
            self.next()
            arg, error = self.expression(arg)
            if error:
                return None, error
            params.append(arg)

        if self.current_token.type != token_rb:
            return None, WrongSyntaxError(
                self.file,
                "Expected '}'" + f" in '{variable.value}' function call.",
                position=self.current_token.position.copy_position(),
            )
        self.next()

        function_call_node = FunctionCallNode(variable, params)
        function_call_node.parent = parent
        return function_call_node, None

    def atom(self, parent=None):
        # print(self.current_token)
        if self.current_token.type == token_bitwise_not:
            return None, None
        if self.current_token.type in (token_int, token_float):
            token = self.current_token
            self.next()
            number_node = NumberNode(token)
            number_node.parent = parent
            return number_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "null"
        ):
            self.next()
            null_node = NullNode()
            null_node.parent = parent
            return null_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "type"
        ):
            self.next()
            types_node = TypesNode(None)
            types, error = self.expression(types_node)
            if error:
                return None, error

            types_node.data = types
            types_node.parent = parent
            return types_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "clear"
        ):
            self.next()
            clear_node = ClearNode(None)
            variable_name, error = self.expression(clear_node)
            if error:
                return None, error
            clear_node.variable_name = variable_name
            clear_node.parent = parent
            return clear_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "copy"
        ):
            self.next()
            deep_code_node = DeepCopyNode(None)

            if self.current_token.type != token_variable:
                return None, RunTimeError(
                    self.file, "copy keyword must be associated with a variable"
                )
            variable, error = self.expression(parent)
            if error:
                return None, error

            deep_code_node.value = variable
            deep_code_node.parent = parent
            return deep_code_node, None

        elif self.current_token.type == token_keyword and self.current_token.value in (
            "true",
            "false",
        ):

            boolean_node = BooleanNode(self.current_token.value)
            self.next()
            boolean_node.parent = parent
            return boolean_node, None

        elif self.current_token.type == token_string:
            string_node = StringNode(None)
            string = self.current_token
            self.next()
            indexs = []

            if self.current_token.type == token_ls:
                string_access_node = StringAccessNode(None, None)
                while self.current_token.type == token_ls:
                    self.next()
                    index, error = self.expression(string_access_node)
                    if error:
                        return None, error

                    if self.current_token.type != token_rs:
                        return None, WrongSyntaxError(
                            self.file,
                            "Expected a '[' in staring indexing statement.",
                            position=self.current_token.position.copy_position(),
                        )
                    self.next()
                    indexs.append(index)

                # string_access_node = StringAccessNode(Token(token_type=token_string  , token_value=string.value) , indexs)
                string_access_node.string = Token(
                    token_type=token_string, token_value=string.value
                )
                string_access_node.indexs = indexs
                string_access_node.parent = parent
                return string_access_node, None

            # return StringNode(Token(token_type=token_string , token_value=string.value)) , None
            # string_node = StringNode(string)
            string_node.string = string
            string_node.parent = parent
            return string_node, None

        elif self.current_token.type == token_mutstring:
            mutstring = self.current_token
            self.next()

            mutable_string_node = MutableStringNode(mutstring)
            mutable_string_node.parent = parent
            return mutable_string_node, None

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
                variable_node = VariableNode(None, None)
                expression, error = self.expression(variable_node)

                if error:
                    return None, error
                # variable_node = VariableNode(variable , expression)
                variable_node.variable = variable
                variable_node.factor = expression
                variable_node.parent = parent

                return variable_node, None

            if self.current_token.type == token_dot:

                self.next()
                prop_node = self.current_token
                self.next()
                # if self.current_token.type == token_lb:
                #     print("it function call")
                if self.current_token.type != token_colon:
                    variable_access_node = VariableAccessNode(variable, prop_node)
                    variable_access_node.parent = parent
                    return variable_access_node, None

                self.next()
                variable_node = VariableNode(None, None, None)
                value, error = self.expression(variable_node)

                if error:
                    return None, error

                variable_node.factor = value
                variable_node.variable = variable
                variable_node.parent = parent

                return variable_node, None

            if self.current_token.type == token_writetofile:
                self.next()
                file_write_node = FileWriteNode(None, None)
                expression, error = self.expression(file_write_node)
                if error:
                    return None, error
                file_write_node.variable = variable
                file_write_node.content = expression
                file_write_node.parent = parent
                return file_write_node, None

            if self.current_token.type == token_lb:

                function_call, error = self.call(variable, parent)

                if error:
                    return None, error

                if self.current_token.type == token_colon:
                    return None, WrongSyntaxError(
                        self.file,
                        "Unexpected '{'"
                        + f" bracket found after variable {variable.value}.",
                    )

                return function_call, None

            if (
                self.current_token.type == token_keyword
                and self.current_token.value == "fn"
            ):
                function_expression, error = self.function_statement(variable, parent)

                if error:
                    return None, error
                return function_expression, None

            if self.current_token.type in (
                token_colon_divide,
                token_colon_minus,
                token_colon_mul,
                token_colon_plus,
                token_colon_power,
            ):
                operator = self.current_token
                self.next()
                assignment_operation_node = AssignmentOperatorNode(None, None, None)

                expression, error = self.expression(assignment_operation_node)

                if error:
                    return None, error

                variable_access_node = VariableAccessNode(variable)
                variable_access_node.parent = assignment_operation_node

                assignment_operation_node.left = variable_access_node
                assignment_operation_node.operator = operator
                assignment_operation_node.right = expression
                assignment_operation_node.parent = parent

                return assignment_operation_node, None

            if self.current_token.type == token_ls:
                # isHashmap = False
                while self.current_token.type == token_ls:
                    self.next()
                    if self.current_token.type == token_rs:
                        return None, WrongSyntaxError(
                            self.file,
                            f"Expected a 'key' before ']' in variable '{variable}'.",
                            position=self.current_token.position.copy_position(),
                        )
                    index, error = self.expression(parent)
                    # if type(index) == StringNode:
                    #     isHashmap = True
                    if error:
                        return None, error

                    if self.current_token.type != token_rs:
                        return None, WrongSyntaxError(
                            self.file,
                            f"Expected a ']' in variable '{variable}'.",
                            position=self.current_token.position.copy_position(),
                        )
                    self.next()
                    indexs.append(index)
                    # print(isHashmap)cls

                if self.current_token.type == token_colon:
                    self.next()
                    # value = self.current_token

                    variable_manipulation_node = VariableManipulationNode(
                        None, None, None
                    )
                    value, error = self.expression(variable_manipulation_node)
                    # print("koay" , type(value) , value)
                    if error:
                        return None, error
                    # print(value , variable)
                    # print(type(value))

                    # if isHashmap:
                    # print("working")
                    variable_manipulation_node.variable = variable
                    variable_manipulation_node.index = indexs
                    variable_manipulation_node.value = value
                    variable_manipulation_node.parent = parent

                    return variable_manipulation_node, None

                    # if type(value) == MutableStringNode:
                    # return VariableManipulationNode(variable , indexs , MutableStringNode(value)) , None
                    # return VariableManipulationNode(variable , indexs , value) , None
                    # else:
                    # return None , RunTimeError(self.file , "Trying to Manipulate Unsupported types")
                    # return VariableManipulationNode(variable , indexs , StringNode(value)) , None
                    # return VariableManipulationNode(variable , indexs , value) , None

                collection_access_node = CollectionAccessNode(variable, indexs)
                collection_access_node.parent = parent
                return collection_access_node, None

            variable_access_node = VariableAccessNode(variable)
            variable_access_node.parent = parent
            return variable_access_node, None

        elif self.current_token.type == token_input:

            input_message = self.current_token
            self.next()
            input_string_node = InputStringNode(input_message)
            input_string_node.parent = parent
            return input_string_node, None

        elif self.current_token.type == token_lparen:
            self.next()
            expression, error = self.expression(parent)
            if error:
                return None, error
            if self.current_token.type != token_rparen:
                return None, WrongSyntaxError(
                    self.file,
                    f"Expected a ')' after expression.",
                    position=self.current_token.position.copy_position(),
                )
            self.next()

            return expression, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "log"
        ):

            show_node = ShowNode(None)

            self.next()
            expression, error = self.expression(show_node)

            if error:
                return None, error

            expressions = [expression]

            while self.current_token.type == token_comma:
                self.next()
                line, error = self.expression(show_node)
                if error:
                    return None, error
                expressions.append(line)

            show_node.statement = expressions
            show_node.parent = parent
            # print(show_node.parent)
            return show_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "file"
        ):

            self.next()

            # filename , error = self.expression()
            # if error:
            #     return None , error

            # return FileNode(filename , "r") , None # need to get input from squig for the file mode.

            file, error = self.file_statement(parent)
            if error:
                return None, error

            return file, error

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "close"
        ):

            self.next()
            close_node = CloseNode(None)
            filename, error = self.expression(close_node)
            # print(filename)
            if error:
                return None, error
            close_node.filename = filename
            close_node.parent = parent
            return close_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "if"
        ):
            # print("if statementt : " , parent)
            if_statement, error = self.if_statement(parent)

            if error:
                return None, error
            return if_statement, None

        elif self.current_token.type == token_lb:

            collection, error = self.collection_statement(parent)
            if error:
                return None, error
            return collection, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "for"
        ):

            for_statement, error = self.for_statement(parent)
            if error:
                return None, error
            return for_statement, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "delete"
        ):
            self.next()
            variables = []
            if self.current_token.type != token_variable:
                return None, WrongSyntaxError(
                    self.file,
                    "Expected a variable but got an expression.",
                    position=self.current_token.position.copy_position(),
                )

            variables.append(self.current_token)
            self.next()

            while self.current_token.type == token_comma:
                self.next()
                if self.current_token.type != token_variable:
                    return None, WrongSyntaxError(
                        self.file,
                        "Expected a variable but got an expression.",
                        position=self.current_token.position.copy_position(),
                    )
                variables.append(self.current_token)
                self.next()

            delete_node = DeleteNode(variables)
            delete_node.parent = parent
            return delete_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "use"
        ):
            self.next()
            use_node = UseNode(None)
            module_name, error = self.expression(use_node)

            if error:
                return None, error
            module_name.parent = use_node
            return use_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "switch"
        ):

            self.next()
            switchNode, error = self.switch_statement(parent)
            if error:
                return None, error

            return switchNode, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "pop"
        ):
            self.next()
            pop_node = PopNode(None, None)

            if self.current_token.type != token_variable:
                return None, WrongSyntaxError(
                    self.file,
                    "Expected a variable but got an expression.",
                    position=self.current_token.position.copy_position(),
                )

            variable = self.current_token

            accessNode, error = self.expression(pop_node)

            if error:
                return None, error

            pop_node.variable = variable
            pop_node.index = accessNode
            pop_node.parent = parent

            return pop_node, None

        elif (
            self.current_token.type == token_keyword
            and self.current_token.value == "try"
        ):

            try_catch_node = TryCatchNode(None, None)
            catch_blocks = []
            self.next()

            if self.current_token.type != token_colon:
                return None, WrongSyntaxError(
                    self.file, "Expected a ':' after try keyword"
                )

            self.next()
            if self.current_token.type != token_lb:
                return None, WrongSyntaxError(
                    self.file, "Expected a '{' after the ':' in try statement"
                )

            self.next()
            try:
                try_block, error = self.statements(try_block)
            except:
                return None, WrongSyntaxError(self.file, "expected a '}' for try block")

            if error:
                return None, error

            if self.current_token.type != token_rb:
                return None, WrongSyntaxError(
                    self.file, "Expected a '}' for try statement"
                )
            self.next()

            if (
                self.current_token.type != token_keyword
                and self.current_token.value != "catch"
            ):
                return None, WrongSyntaxError(
                    self.file, "Expected atleast a single catch block"
                )

            else:
                while (
                    self.current_token.type == token_keyword
                    and self.current_token.value == "catch"
                ):
                    self.next()
                    if self.current_token.type != token_lb:
                        return None, WrongSyntaxError(
                            self.file, "Expected '{' after the catch block"
                        )
                    self.next()
                    if self.current_token.type != token_variable:
                        return None, WrongSyntaxError(
                            self.file, "Expected a catch variable"
                        )

                    variable_name = self.current_token
                    self.next()
                    if self.current_token.type != token_eql:
                        return None, WrongSyntaxError(
                            self.file, "Expected a '=' in catch condition"
                        )
                    self.next()
                    type_name, error = self.expression(try_block)
                    if error:
                        return None, error

                    if self.current_token.type != token_rb:
                        return None, WrongSyntaxError(
                            self.file,
                            "Expected a '}' in catch block after the catch variable",
                        )
                    self.next()
                    if self.current_token.type != token_colon:
                        return None, WrongSyntaxError(
                            self.file, "Expected a ':' in catch block"
                        )
                    self.next()
                    if self.current_token.type != token_lb:
                        return None, WrongSyntaxError(
                            self.file, "Expected a '{' in catch after ':'"
                        )
                    self.next()

                    catch_block, error = self.statements(try_block)
                    catch_blocks.append((catch_block, variable_name, type_name))
                    if error:
                        return None, error

                    if self.current_token.type != token_rb:
                        return None, WrongSyntaxError(
                            self.file, "Expected a '}' in catch"
                        )

                    self.next()

            if (
                self.current_token.type == token_keyword
                and self.current_token.value == "finally"
            ):
                self.next()
                if self.current_token.type != token_colon:
                    return None, WrongSyntaxError(
                        self.file, "Expected a ':' in finally block"
                    )
                self.next()
                if self.current_token.type != token_lb:
                    return None, WrongSyntaxError(
                        self.file, "Expected a '{' after ':' in finally block"
                    )
                self.next()
                finally_block_statement, error = self.statements(try_block)
                if error:
                    return None, error
                if self.current_token.type != token_rb:
                    return None, WrongSyntaxError(
                        self.file, "Expected a '}' after ':' in finally block"
                    )
                self.next()
                # return TryCatchNode(try_block , catch_blocks , variable_name , finally_block_statement) , None
                # return TryCatchNode(try_block , catch_blocks , variable_name ) , None
                try_catch_node.try_block_statements = try_block
                try_catch_node.catch_block_statements = catch_blocks
                try_catch_node.finally_block_statements = finally_block_statement
                try_catch_node.parent = parent
                return try_catch_node, None

            try_catch_node.try_block_statements = try_block
            try_catch_node.catch_block_statements = catch_blocks
            try_catch_node.parent = parent
            return try_catch_node, None

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

    def switch_statement(self, parent=None):

        switch_node = SwitchNode(None, None, None)

        if self.current_token.type != token_lb:
            return None, WrongSyntaxError(
                file=self.file,
                details="Expected a '{' in switch statement.",
                position=None,
            )

        self.next()

        condition, error = self.expression(switch_node)
        if error:
            return None, error

        if self.current_token.type != token_rb:
            return None, WrongSyntaxError(
                file=self.file,
                details="Expected a '}' in switch statement.",
                position=None,
            )

        self.next()
        if self.current_token.type != token_colon:
            return None, WrongSyntaxError(
                file=self.file,
                details="Expected a ':' in switch statement.",
                position=None,
            )

        self.next()

        if self.current_token.type != token_lb:
            return None, WrongSyntaxError(
                file=self.file,
                details="Expected a '{' in switch statement.",
                position=None,
            )

        self.next()

        case_conditions = {}

        # while self.current_token.type == token_newline:
        #         self.next()

        while (
            self.current_token.type == token_keyword
            and self.current_token.value == "case"
        ):
            # print("checking")
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            case_condition = str(self.current_token.value)
            # if error:
            #     return None , error

            self.next()
            if self.current_token.type != token_colon:
                return None, WrongSyntaxError(
                    file=self.file,
                    details="Expected a ':' in switch statement.",
                    position=None,
                )

            self.next()
            # print("in parser" , self.current_token )
            error, case_body = None, None

            if self.current_token.type != token_lb:
                case_body, error = self.expression(switch_node)
            else:
                self.next()
                case_body, error = self.statements(switch_node)

            if error:
                return None, error

            # while self.current_token.type == token_newline:
            #     self.next()

            case_conditions[case_condition] = case_body

            if self.current_token.type == token_rb:
                self.next()

        # while self.current_token.type == token_newline:
        #     self.next()
        if (
            self.current_token.type != token_keyword
            and self.current_token.value != "default"
        ):

            return None, WrongSyntaxError(
                file=self.file,
                details="Expected a 'default' in switch statement.",
                position=None,
            )

        has_brackets = False
        self.next()
        if self.current_token.type != token_colon:
            return None, WrongSyntaxError(
                file=self.file,
                details="Expected a ':' in switch statement.",
                position=None,
            )

        self.next()
        default_body, error = None, None

        if self.current_token.type != token_lb:
            has_brackets = True
            default_body, error = self.expression(switch_node)
        else:
            self.next()
            default_body, error = self.statements(switch_node)

        if error:
            return None, error

        if has_brackets and self.current_token.type != token_rb:

            return None, WrongSyntaxError(
                file=self.file,
                details="Expected a '}' in switch statement.",
                position=None,
            )

        self.next()

        if not has_brackets and self.current_token.type != token_rb:
            return None, WrongSyntaxError(
                file=self.file,
                details="Expected a '}' in switch statement.",
                position=None,
            )

        self.next()

        switch_node.cases = case_conditions
        switch_node.condition = condition
        switch_node.default = default_body
        switch_node.parent = parent
        return switch_node, None

    def file_statement(self, parnet=None):

        mode = "r"
        file_node = FileNode(None, None)

        if self.current_token.type == token_lt:
            self.next()

            if self.current_token.type == token_string:
                mode = self.current_token.value

            if self.current_token.type != token_string:
                mode = "undefined variable " + "'" + self.current_token.value + "'"
                return None, WrongSyntaxError(
                    file=self.file,
                    details=f"Expected arguments (a , r, w, r+ ,w+ ,a+) , but got {mode}.",
                    position=None,
                )

            self.next()

            if self.current_token.type != token_gt:

                return None, WrongSyntaxError(
                    file=self.file,
                    details=f"Expected a closing '>' , but got {self.current_token}",
                    position=None,
                )

            self.next()

        file_name, error = self.expression(file_node)

        if error:
            return None, error

        mode = StringNode(
            Token(token_type=token_string, token_value=mode, token_position=None)
        )
        file_node.filename = file_name
        file_node.mode = mode
        file_node.parent = parnet
        return file_node, None

    def function_statement(self, function_name, parent=None):

        function_node = FunctionNode(None, None, None, None)
        self.next()

        if self.current_token.type != token_lb:
            return None, WrongSyntaxError(
                self.file,
                "Expected a '{' after the 'function' keyword in " + function_name.value,
                position=self.current_token.position.copy_position(),
            )

        self.next()
        param_list = []
        if self.current_token.type == token_variable:
            # print("it's a function call")
            param_name, error = self.expression(function_node)
            if error:
                return None, WrongSyntaxError(
                    self.file,
                    "Something went wrong in function definition.",
                    position=self.current_token.position.copy_position(),
                )
            param_list.append(param_name.variable)

            while self.current_token.type == token_comma:
                self.next()
                param_name, error = self.expression(function_node)
                if error:
                    return None, WrongSyntaxError(
                        self.file,
                        "something went worng in function deefinition.",
                        position=self.current_token.position.copy_position(),
                    )
                param_list.append(param_name.variable)
        else:
            if not self.current_token.type == token_rb:
                return None, WrongSyntaxError(
                    self.file,
                    f"'{self.current_token.value}' cannot be a parameter while defining a function.",
                )
            

        if self.current_token.type != token_rb:
            return None, WrongSyntaxError(
                self.file,
                "Expected a '}' in " + f"{function_name.value} function definition.",
                position=self.current_token.position.copy_position(),
            )

        self.next()
        if (
            self.current_token.type != token_colon
            and self.current_token.type != token_type_specifier
        ):

            return None, WrongSyntaxError(
                self.file,
                "Expected a ':' in " + f"{function_name.value} function definition",
                position=self.current_token.position.copy_position(),
            )

        type_mentioned = None
        if self.current_token.type == token_type_specifier:
            self.next()
            type_mentioned = self.current_token

        self.next()

        if self.current_token.type == token_lb:
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            statement, error = self.statements(function_node)

            if error:
                return None, error

            if self.current_token.type != token_rb:
                return None, WrongSyntaxError(
                    self.file, "Expected a closing '}' in function ."
                )

            self.next()

            function_node.variable = function_name
            function_node.param = param_list
            function_node.body = statement
            function_node.type_mentioned = type_mentioned
            function_node.parent = parent
            
            return function_node, None

        function_body, error = self.expression(function_node)

        # print("after in function statement in parser")
        if error:
            return None, WrongSyntaxError(
                self.file,
                "Something went wrong in function body.",
                position=self.current_token.position.copy_position(),
            )
        # if self.current_token.type != token_keyword and self.current_token.value == "end":
        #     return None , WrongSyntaxError(self.file , f"expected an 'end' in {function_name} definition.")
        # # self.next()
        function_node.variable = function_name
        function_node.param = param_list
        function_node.body = function_body
        function_node.type_mentioned = type_mentioned
        function_node.parent = parent
        return function_node, None
        # return FunctionNode(function_name , param_list , function_body , type_mentioned) , None

    def for_statement(self, parent=None):

        for_node = ForNode(None, None, None, None, None, None)

        self.next()

        if self.current_token.type != token_variable:
            return None, WrongSyntaxError(
                self.file,
                "Expected  a iterator variable name after for keyword.",
                position=self.current_token.position.copy_position(),
            )

        iterator_variable_name = self.current_token
        self.next()

        if self.current_token.type != token_lb:

            return None, WrongSyntaxError(
                self.file,
                "Expected a '{' after the interator variable.",
                position=self.current_token.position.copy_position(),
            )

        self.next()
        start_range, error = self.expression(for_node)
        step_range = 1
        end_range = None

        if self.current_token.type == token_comma:
            self.next()
            end_range, error = self.expression(for_node)
            if error:
                return None, error

            if self.current_token.type == token_comma:
                self.next()
                step_range, error = self.expression(for_node)
                if error:
                    return None, error

        if self.current_token.type != token_rb:

            return None, WrongSyntaxError(
                self.file,
                "Expected a '}' after the range in for loop.",
                position=self.current_token.position.copy_position(),
            )
        self.next()

        if self.current_token.type != token_colon:

            return None, WrongSyntaxError(
                self.file,
                "Expected a ':' after the for loop range",
                position=self.current_token.position.copy_position(),
            )

        self.next()

        if self.current_token.type == token_lb:
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            if self.current_token.type == token_rb:
                return None, RunTimeError(
                    self.file,
                    "blocks cannot be empty , check 'for clause' at line {linenumber}.",
                )
            statement, error = self.statements(for_node)
            # print("it's  a newline statement" , self.current_token)
            if error:
                return None, error

            # while self.current_token.type == token_newline:
            #     self.next()

            if self.current_token.type != token_rb:
                return None, WrongSyntaxError(
                    self.file, "Expected a closing '}' in for loop.", position=None
                )

            self.next()
            for_node.start_value = start_range
            for_node.end_value = end_range
            for_node.step_value = step_range
            for_node.body = statement
            for_node.variable = iterator_variable_name
            for_node.parent = parent
            return for_node, None

        loop_body, error = self.expression(for_node)
        if error:

            return None, WrongSyntaxError(
                self.file,
                "Something went wrong in for loop body.",
                position=self.current_token.position.copy_position(),
            )
        for_node.start_value = start_range
        for_node.end_value = end_range
        for_node.step_value = step_range
        for_node.body = loop_body
        for_node.variable = iterator_variable_name
        for_node.parent = parent
        return for_node, None

    def if_statement(self, parent=None):

        cases = []
        else_case = None

        if_node = IfNode(None, None, None)  # (cases , else_case , parent)

        if not (
            self.current_token.type == token_keyword
            and self.current_token.value == "if"
        ):

            return None, WrongSyntaxError(
                self.file,
                "Expected 'if' keyword.",
                position=self.current_token.position.copy_position(),
            )
        self.next()

        if self.current_token.type != token_lb:
            return None, WrongSyntaxError(
                self.file,
                "Expected a '{' after the 'if' keyword.",
                position=self.current_token.position.copy_position(),
            )

        self.next()

        # while self.current_token.type == token_newline:
        #     self.next()
        condition, error = self.expression(if_node)

        if type(condition) == VariableNode:
            return None, RunTimeError(
                self.file, "cannot use assignment statement in conditions"
            )

        # print("inside if" , self.current_token)
        # while self.current_token.type == token_newline:
        #     self.next()
        if error:
            return None, error

        if self.current_token.type != token_rb:
            return None, WrongSyntaxError(
                self.file,
                "Expected a '}' before ':' in 'if statement'.",
                position=self.current_token.position.copy_position(),
            )
        self.next()

        if self.current_token.type != token_colon:
            return None, WrongSyntaxError(
                self.file,
                "Expected a ':' after '}' in 'if statement'.",
                position=self.current_token.position.copy_position(),
            )

        self.next()
        cases1, error = None, None  # Check this line
        if self.current_token.type == token_lb:
            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            if self.current_token.type == token_rb:
                return None, RunTimeError(
                    self.file,
                    "blocks cannot be empty. check 'if clause' at line {linenumber}",
                )
            cases1, error = self.statements(if_node)
        else:

            # while self.current_token.type == token_newline:
            #     self.next()
            if self.current_token.type == token_rb:
                return None, RunTimeError(
                    self.file,
                    "blocks cannot be empty. check 'if clause' at line {linenumber}",
                )
            cases1, error = self.expression(if_node)

        if error:
            return None, error

        # cases1.parent = if_node
        cases.append((condition, cases1))
        if self.current_token.type != token_rb:
            return None, WrongSyntaxError(
                self.file, "Expected a closing '}' in if statement"
            )
        self.next()
        # while self.current_token.type == token_newline:
        #     self.next()
        while (
            self.current_token.type == token_keyword
            and self.current_token.value == "elif"
        ):

            self.next()
            if self.current_token.type != token_lb:
                return None, WrongSyntaxError(
                    self.file,
                    "Expected '{' after 'elif' keyword.",
                    position=self.current_token.position.copy_position(),
                )

            self.next()
            # while self.current_token.type == token_newline:
            #     self.next()
            condition, error = self.expression(if_node)

            # while self.current_token.type == token_newline:
            #     self.next()
            if error:
                return None, error

            if self.current_token.type != token_rb:
                return None, WrongSyntaxError(
                    self.file,
                    "Expected a '}' before ':' in 'elif statement'.",
                    position=self.current_token.position.copy_position(),
                )
            self.next()

            if self.current_token.type != token_colon:
                return None, WrongSyntaxError(
                    self.file,
                    "Expected a ':' after '}' in 'elif statement'.",
                    position=self.current_token.position.copy_position(),
                )

            self.next()

            block, error = None, None
            if self.current_token.type == token_lb:
                self.next()
                if self.current_token.type == token_rb:
                    return None, RunTimeError(
                        self.file,
                        "blocks cannot be empty. check 'elif clause' at line {linenumber}",
                    )

                block, error = self.statements(if_node)
            else:
                if self.current_token.type == token_rb:
                    return None, RunTimeError(
                        self.file,
                        "blocks cannot be empty. check 'elif clause' at line {linenumber}",
                    )

                block, error = self.expression(if_node)

            if error:
                return None, error

            # block.parent = if_node
            if self.current_token.type != token_rb:
                return None, WrongSyntaxError(
                    self.file, "Expected a closing '}' for elif block."
                )
            self.next()
            cases.append((condition, block))

            # while self.current_token.type == token_newline:
            #     self.next()

        if (
            self.current_token.type == token_keyword
            and self.current_token.value == "else"
        ):

            self.next()

            if self.current_token.type != token_colon:
                return None, WrongSyntaxError(
                    self.file,
                    "Expected a ':' after the 'else' keyword.",
                    position=self.current_token.position.copy_position(),
                )
            self.next()

            block, error = None, None
            if self.current_token.type == token_lb:
                self.next()
                if self.current_token.type == token_rb:
                    return None, RunTimeError(
                        self.file,
                        "blocks cannot be empty. check 'else clause' at line {linenumber}",
                    )

                block, error = self.statements(if_node)
            else:
                if self.current_token.type == token_rb:
                    return None, RunTimeError(
                        self.file,
                        "blocks cannot be empty. check 'else clause' at line {linenumber}",
                    )
                block, error = self.expression(if_node)

            if error:
                return None, error

                # print("if statement" , self.current_token)
            # print(self.current_token)
            # block.parent = if_node
            if self.current_token.type != token_rb:
                return None, WrongSyntaxError(
                    self.file,
                    "Expected a '}' in the 'else clause'.",
                    position=self.current_token.position.copy_position(),
                )

            self.next()

            else_case = block

        if_node.cases = cases
        if_node.else_case = else_case
        if_node.parent = parent

        return if_node, None

    def collection_statement(self, parent=None):

        collection_node = CollectionNode(None)

        # print("working")
        elements = ()
        first_element_type = None
        same_type = True

        if self.current_token.type != token_lb:
            return None, WrongSyntaxError(
                self.file,
                "Expected a '{' in collection statement.",
                position=self.current_token.position.copy_position(),
            )
        self.next()

        # while self.current_token.type == token_newline:
        #     self.next()

        if self.current_token.type == token_rb:
            return CollectionNode(elements), None

        element, error = self.expression(collection_node)
        if error:
            return None, error

        first_element_type = type(element)

        # Map Feature
        if self.current_token.type == token_colon:

            hashmap = HashMapNode()

            self.next()
            value, error = self.expression(HashMapNode)
            if error:
                return None, error

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
                key, error = self.expression()

                if error:
                    return None, error

                if self.current_token.type != token_colon:
                    return None, WrongSyntaxError(
                        self.file, "Expected a ':' in hashmap declaration."
                    )

                self.next()

                value, error = self.expression(hashmap)
                if error:
                    return None, error

                # print("workigng" , value.string.value)
                # print(hashmap.index_key , hashmap.key_value , type(value) , type(key))

                hashmap.key_value[key.string.value] = value
                hashmap.index_key.append(key.string.value)
                # print(hashmap.index_key)

            # while self.current_token.type == token_newline:
            #     self.next()

            if self.current_token.type != token_rb:
                return None, WrongSyntaxError(
                    self.file, "Expected a '}' in hashmap declaration."
                )
            self.next()

            hashmap.parent = parent
            return hashmap, None

        elements += (element,)

        # while self.current_token.type == token_newline:
        #     self.next()

        while self.current_token.type == token_comma:

            if self.current_token.type == token_comma:
                # print(self.current_token , elements)
                self.next()
            # while self.current_token.type == token_newline:
            #     self.next()

            element, error = self.expression(collection_node)
            if error:
                return None, error

            elements += (element,)
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
            return None, WrongSyntaxError(
                self.file,
                "Expected a '}' in 'collection statement'.",
                position=self.current_token.position.copy_position(),
            )
        self.next()
        # print(type(elements))

        collection_node.elements = elements
        collection_node.parent = parent
        return collection_node, None

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
        lexer = Lexer("", input("Enter a expression :"))
        tokens, error = lexer.tokenize()

        if error:
            print(error.print())
            continue

        parser = Parser(tokens, "<ProgramFile>")
        result, error = parser.parse()
        print(result)
        if error:
            print(error.print())
            continue

        del lexer, parser
