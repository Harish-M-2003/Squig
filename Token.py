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

keywords = ("if" , "else" ,"not", "elif", "function" , "end",
            "for","return", "break" ,"continue","show" , "let",
            "delete" , "types" , "use")

class Token:

    def __init__(self,token_type , token_value = None):

        self.type = token_type
        self.value = token_value

    def __repr__(self):

        if self.value:
            return f"{self.type} : {self.value}"
        return f"{self.type}"
