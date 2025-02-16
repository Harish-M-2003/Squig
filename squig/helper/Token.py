token_plus = "plus"
token_minus = "minus"
token_divide = "divide"
token_dot = "dot"
token_modulo = "modulo"
token_mul = "mul"
token_letters = "abcdefghijklmnopqrstuvwxyz"
token_letters += token_letters.upper()
token_digit = ".0123456789"
token_variable = "variable"
token_string = "string"
token_int = "int"
token_float = "float"
token_gt = "gt"
token_lt = "lt"
token_gte = "gte"
token_lte = "lte"
token_ne = "ne"
token_colon = "colon"
token_comma = "comma"
token_lparen = "lparen"
token_rparen = "rparen"
token_not = "not"
token_power = "power"
token_keyword = "keyword"
token_eql = "eql"
token_lb = "lbrace"
token_rb = "rbrace"
token_input = "input"
token_and = "and"
token_or = "or"
token_ls = "lsquare"
token_rs = "rsquare"
token_colon_plus = "colonPlus"
token_colon_minus = "colonMinus"
token_colon_divide = "colonDivide"
token_colon_mul = "colonMul"
token_colon_power = "colonPower"
token_newline = "newline"
token_eof = "eof"
token_writetofile = "writetofile"
token_mutstring = "mutstring"
token_at = "at"
token_type_specifier = "typesecifiper"
token_left_shift = "leftshift"
token_right_shift = "rightshift"
token_bitwise_and = "bitwiseand"
token_bitwise_or = "bitwiseor"
token_bitwise_not = "bitwisenot"
token_bitwise_xor = "bitwisexor"

keywords = (
    "if",
    "else",
    "elif",
    "fn",
    "for",
    "return",
    "break",
    "continue",
    "let",
    "delete",
    "type",
    "use",
    "log",
    "file",
    "close",
    "default",
    "case",
    "switch",
    "true",
    "false",
    "pop",
    "clear",
    "null",
    "imu",
    "copy",
    "try",
    "catch",
    "finally",
    "class",
)


class Token:

    def __init__(self, token_type, token_value=None, token_position=None):

        self.type = token_type
        self.value = token_value
        self.position = token_position

    def __repr__(self):

        if self.value:
            return f"{self.type} : {self.value}"
        return f"{self.type}"
