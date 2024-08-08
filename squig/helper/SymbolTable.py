import helper.Types as Types
from Interpreter import FILE as file

symbol_table = {
    "string": Types.BuiltinFunction(file, "String"),
    "mut": Types.BuiltinFunction(file, "MutableString"),
    "number": Types.BuiltinFunction(file, "Number"),  # has some issue
    "bool": Types.BuiltinFunction(file, "Bool"),  # has some issue
    "int": Types.BuiltinFunction(file, "int"),
    "isnumber": Types.BuiltinFunction(file, "is_number"),  # checked
    "isstring": Types.BuiltinFunction(file, "is_string"),  # checked
    "isbool": Types.BuiltinFunction(file, "is_bool"),  # checked
    "length": Types.BuiltinFunction(file, "length"),  # checked
    "iscollection": Types.BuiltinFunction(file, "is_collection"),  # checked
    "find": Types.BuiltinFunction(file, "find"),
    "replace": Types.BuiltinFunction(file, "replace"),
    "ispalindrome": Types.BuiltinFunction(file, "is_palindrome"),
    "isfunction": Types.BuiltinFunction(file, "is_function"),
    "ltrim": Types.BuiltinFunction(file, "ltrim"),
    "rtrim": Types.BuiltinFunction(file, "rtrim"),
    "trim": Types.BuiltinFunction(file, "trim"),
    "isalpha": Types.BuiltinFunction(file, "is_alpha"),
    "isalnum": Types.BuiltinFunction(file, "is_alnum"),
    "isint": Types.BuiltinFunction(file, "is_int"),
    "isupper": Types.BuiltinFunction(file, "isUpper"),
    "islower": Types.BuiltinFunction(file, "isLower"),
    "isfloat": Types.BuiltinFunction(file, "is_float"),  # checked
    "istitle": Types.BuiltinFunction(file, "is_title"),  # checked
    "isascii": Types.BuiltinFunction(file, "is_ascii"),
    "lower": Types.BuiltinFunction(file, "lower"),  # checked
    "upper": Types.BuiltinFunction(file, "upper"),  # checked
    "isspace": Types.BuiltinFunction(file, "is_space"),
    "slice": Types.BuiltinFunction(file, "slice"),
    "tocap": Types.BuiltinFunction(file, "toCap"),
    "startswith": Types.BuiltinFunction(file, "startswith"),  # checked
    "endswith": Types.BuiltinFunction(file, "endswith"),  # checked
    "swapcase": Types.BuiltinFunction(file, "swapcase"),
    "charat": Types.BuiltinFunction(file, "charat"),
    "reverse": Types.BuiltinFunction(file, "reverse"),
    "title": Types.BuiltinFunction(file, "title"),
    "split": Types.BuiltinFunction(file, "split"),
    "remove": Types.BuiltinFunction(file, "remove"),
    "insert": Types.BuiltinFunction(file, "insert"),
    "sort": Types.BuiltinFunction(file, "sort"),
    "lsearch": Types.BuiltinFunction(file, "lsearch"),
    "bsearch": Types.BuiltinFunction(file, "bsearch"),
}
