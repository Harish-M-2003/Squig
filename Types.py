import Interpretor
from Error import *
from os import *

def isFloat(num):

    numbers = [char for char in num]
    dot_count = 0

    for char in numbers:
        if char == '.':
            if dot_count == 0:
                dot_count += 1
            else:
                return False
            
        if not char in "123456789.0":
            return False
        
    if dot_count == 0:
        return False
    
    return True

class String:

    def __init__(self,string):

        self.string = string
        self.file = "change to file name later info for harish"

    def __repr__(self):

        return f'"{self.string}"'
    
    def div(self , number):
        if isinstance(number , Number):
            return Number(int(self.string) / number.number) , None
        elif isinstance(number , String):
            if number.string.isdigit():
                return Number(int(self.string) / int(number.string)) , None
            
        return None , RunTimeError(self.file , f"cannot perform operation between types {type(self).__name__ , type(number).__name__}")
    
    def add(self , string):

        if isinstance(string , String):

            if self.string.isdigit() and string.string.isdigit():
                return Number(int(self.string) + int(string.string)) , None
            
            return String(self.string + string.string) , None
        
        elif isinstance(string , Number):
            if self.string.isdigit():
                return Number(int(self.string) + string.number) , None
            elif isFloat(self.string):
                return Number(string.number*float(self.string)) , None
            return String(self.string + str(string.number)) , None
        else:
            return None , RunTimeError(self.file ,
                                 f"Unexpected operation for '{type(self.string).__name__ , type(string).__name__}'.")
            
    def mul(self , number):
        if isinstance(number , Number):
            return String(self.string * number.number) , None
        else:
            return None , RunTimeError(self.file ,f"Unexpected operation for '{type(self.string).__name__ , type(number).__name__}'.")
        
    def index(self,index):

        if index > len(self.string):
            return Number(-1)

        return String(self.string[index])
    
    def lt(self , string):
        if isinstance(string, String):
            return Boolean(self.string < string.string) , None
    
    def gt(self , string):
        if isinstance(string, String):
            return Boolean(self.string > string.string) , None
    
    def lte(self , string):
        if isinstance(string, String):
            return Boolean(self.string <= string.string) , None
        
    def gte(self , string):
        if isinstance(string, String):
            return Boolean(self.string >= string.string) , None
    
    def eql(self , string):
        if isinstance(string, String):
            return Boolean(self.string == string.string) , None
    
    def ne(self , string):
        if isinstance(string, String):
            return Boolean(self.string != string.string) , None
    
    def _and_(self , string):
        if isinstance(string, String):
            return Boolean(self.string and string.string) , None
    
    def _or_(self , string):
        if isinstance(string, String):
            return Boolean(self.string or string.string) , None
    
class InputString:

    def value(self , input):

        if input.isalpha():
            return String(input) , None
        
        elif input.isdigit():
            return Number(int(input)) , None
        
        return String(input) , None
        

class Collection:

    def __init__(self,elements):

        self.elements = elements
        self.file = "change to file name later info for harish"

    def __repr__(self):

        return f"{self.elements}".replace('(','{').replace(')','}')


    def index(self,index):

        if index > len(self.elements):
            return Number(-1)

        return self.elements[index]
    
    def mul(self , number):

        if isinstance(number , Number):
            return Collection(self.elements*number.number) , None
        else:
            return None ,  RunTimeError(self.file , f"Unsupported operation '*' for types ('Collection' , {type(number).__name}).")

    def add(self , collection):

        if isinstance(collection , Collection):

            return Collection(self.elements + collection.elements) , None
        else:
            return Collection(self.elements + (collection,))  , None

class Boolean:

    def __init__(self,value):

        self.value = value

    def __repr__(self):

        return f"{self.value}"

class Number:

    def __init__(self,number):

        self.number = number
        self.file = "change to file name later info for harish"

    def __repr__(self):

        return f"{self.number}"

    def add(self , number):

        if isinstance(number , Number):
            return Number(self.number + number.number) , None
        elif isinstance(number , Collection):
            return Collection((self.number,) + number.elements) , None
        elif isinstance(number , String):
            if number.string.isdigit():
                return Number(self.number + int(number.string)) , None
            elif isFloat(number.string):
                return Number(float(number.string)*self.number) , None
            return String(str(self.number) + number.string) , None
        
        return None , RunTimeError(self.file , f"cannot perform operation between types {type(self).__name__ , type(number).__name__}")

    
    def sub(self , number):

        if isinstance(number , Number):
            return Number(self.number - number.number) , None
        elif isinstance(number , String):
            if number.string.isdigit():
                return Number(self.number - int(number.string)) , None
            elif isFloat(number.string):
                return Number(float(number.string)*self.number) , None

        return None , RunTimeError(self.file , f"cannot perform operation between types {type(self).__name__ , type(number).__name__}")
    
    def mul(self , number):

        if isinstance(number , Number):
            return Number(self.number * number.number) , None
        elif isinstance(number , Collection):
            return Collection(number.elements*self.number ) , None
        elif isinstance(number , String):
            if number.string.isdigit():
                return Number(int(number.string)*self.number) , None
            elif isFloat(number.string):
                return Number(float(number.string)*self.number) , None
            return String(self.number * number.string) , None

        return None , RunTimeError(self.file , f"cannot perform operation between types {type(self).__name__ , type(number).__name__}")

    def div(self , number):
        if isinstance(number , Number):
            return Number(self.number / number.number) , None
        elif isinstance(number , String):
            if number.string.isdigit():
                return Number(self.number / int(number.string)) , None
            elif isFloat(number.string):
                return Number(self.number / float(number.number)) , None
   
        return None , RunTimeError(self.file , f"cannot perform operation between types {type(self).__name__ , type(number).__name__}")
    
    def pow(self , number):
        if isinstance(number , Number):
            return Number(self.number ** number.number) , None
        elif isinstance(number , String):
            if number.string.isdigit():
                return Number(self.number ** int(number.string)) , None
            
        return None , RunTimeError(self.file , f"cannot perform operation between types {type(self).__name__ , type(number).__name__}")
        
    def lt(self , number):
        if isinstance(number , Number):
            return Boolean(self.number < number.number) , None
    
    def gt(self , number):
        if isinstance(number , Number):
            return Boolean(self.number > number.number) , None
    
    def lte(self , number):
        if isinstance(number , Number):
            return Boolean(self.number <= number.number) , None
        
    def gte(self , number):
        if isinstance(number , Number):
            return Boolean(self.number >= number.number) , None
    
    def eql(self , number):
        if isinstance(number , Number):
            return Boolean(self.number == number.number) , None
    
    def ne(self , number):
        if isinstance(number , Number):
            return Boolean(self.number != number.number) , None
    
    def _and_(self , number):
        if isinstance(number , Number):
            return Boolean(self.number and number.number) , None
    
    def _or_(self , number):
        if isinstance(number , Number):
            return Boolean(self.number or number.number) , None
        
class BaseFunction:

    def __init__(self , file , variable , params , body):

        self.file = file
        self.variable = variable
        self.params = params
        self.body = body

    def generate_local_symbol_table(self):

        return {}
    
    def check_param_and_arg_length(self , params , args):

        if len(params) < len(args):

            return None , RunTimeError(self.file , f"'{self.variable}' function got too high arguments.")
        
        if len(params) > len(args):

            return None , RunTimeError(self.file , f"'{self.variable}' function got too low arguments.")
        
        return None , None
        
    def update_local_symnol_table(self ,params , args, symbol_table):

        for idx in range(len(args)):
            symbol_table[params[idx]] = args[idx]
        
        return None

        
class UserDefinedFunction(BaseFunction):

    def __init__(self ,file, variable , params , body):

        super().__init__(file , variable , params , body)
    
    def execute(self , args):

        local_symbol_table = {}
        function_processor = Interpretor.Interpretor(self.file , local_symbol_table)
        
        status , error = self.check_param_and_arg_length(self.params , args)
        if error:
            return None , error
        
        self.update_local_symnol_table(self.params , args , local_symbol_table)
        
        function_expression , error = function_processor.process(self.body)

        if error:
            return None , error
        return function_expression , None


class BuiltinFunction(BaseFunction):

    def __init__(self,file , variable ):

        self.file = file
        self.variable = variable

    def execute(self , args):

        local_symbol_table = {}

        method = getattr(self , f"execute_{self.variable}" , self.no_function)
        
        self.update_local_symnol_table(method.params , args , local_symbol_table)

        return method(local_symbol_table)
    
    def execute_is_string(self,symbol_table):
        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(True) , None
        return Boolean(False) , None
    execute_is_string.params = ["value"]

    
    def execute_is_number(self,symbol_table):

        value = symbol_table["value"]
        if isinstance(value , Number):
            return Boolean(True) , None
        elif isinstance(value , String):
            if value.string.isdigit() or isFloat(value.string):
                return Boolean(True) , None
        return Boolean(False) , None
    
    execute_is_number.params = ["value"]
    
    def execute_is_bool(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , Boolean):
            return Boolean(True) , None
        return Boolean(False) , None
    execute_is_bool.params = ["value"]

    def execute_Bool(self , symbol_table):
        value = symbol_table["value"]
        if isinstance(value , String):
            if value.string:
                return Boolean(True) , None
            else:
                return Boolean(False) , None
        
        if isinstance(value , Number):
            if value.number:
                return Boolean(True) , None
            else:
                return Boolean(False) , None
        
        if isinstance(value , Collection):

            if value.elements:
                return Boolean(True) , None
            else:
                return Boolean(False) , None
        
        return None , WrongTypeError(self.file , f"Cannot convert {value} to Number type.")
    execute_Bool.params = ["value"]


    def execute_find(self,symbol_table):

        value = symbol_table["value"]
        target = symbol_table["target"]

        if isinstance(value , String):
            if isinstance(target , String):
                return Number(value.string.find(target.string)) , None
            elif isinstance(target , Number):
                return Number(value.string.find(str(target.number))) , None
            else:
                return None , RunTimeError(self.file , "got unexpected 'target' for String.")
        
        elif isinstance(value , Collection):
            if isinstance(value , Number):
                return Number(value.elements.index(target.number)) , None
            elif isinstance(value , String):
                return Number(value.elements.index(target.string)) , None
            elif isinstance(value , Boolean):
                return Number(value.elements.index(target.value)) , None
        
        elif isinstance(value , Number):
            if isinstance(target , Number):
                return Number(str(value.number).find(str(target.number))) , None
            elif isinstance(target , String):
                if target.string.isdigit() and isFloat(target.string):
                    return Number(str(value.number).find(target.string)) , None
                
        return None , RunTimeError(self.file , f"'Collection' has not function 'find'.")    
    execute_find.params = ["value" , "target"]

    def execute_String(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , Number):
            return String(str(value.number)) , None
        elif isinstance(value , String):
            return String(value.string) , None
        elif isinstance(value , Collection):
            return String(str(value.elements)) , None
    
    execute_String.params = ["value"]

    def execute_is_palindrome(self , symbol_table):

        value = symbol_table["value"]

        if isinstance(value , Number):
            number = str(value.number)
            return Boolean(number[::-1] == number) , None
        elif isinstance(value , String):
            string = value.string
            return Boolean(string[::-1] == string) , None
        
        return None , WrongTypeError(self.file , f"Collection has no function 'is_palindorme.")
    execute_is_palindrome.params = ["value"]

    def execute_replace(self,symbol_table):

        value = symbol_table["value"]
        old_value = symbol_table["old_value"]
        new_value = symbol_table["new_value"]

        if isinstance(value , String):

            if not isinstance(old_value , String):
                return None , RunTimeError(self.file , "'Old' string must be String type.")
            elif old_value.string not in value.string:
                return None , RunTimeError(self.file , f"'{value.string}' doesn't contains {old_value}")
            
            return String(value.string.replace(old_value.string , new_value.string)) , None
        
    execute_replace.params = ["value" , "old_value" , "new_value"]

    def execute_length(self,symbol_table):

        value = symbol_table["value"]
        if isinstance(value , Number):
            return Number(len(str(value.number))) , None
        if isinstance(value , String):
            return Number(len(value.string)) , None
        
        if isinstance(value , Collection):
            return Number(len(value.elements)) , None
        
        return None , WrongTypeError(self.file , f"Cannot convert {value} to Number type.")
    execute_length.params = ["value"]

    def execute_Number(self, symbol_table):

        value = symbol_table["value"]
        if isinstance(value , Number):
            return Number(value.number) , None
        
        elif isinstance(value , Collection):
            if not value.elements:
                return Number(0) , None
            
        elif isinstance(value , String):
            if value.string.isdigit():
                return Number(int(value.string)) , None
            elif isFloat(value.string):
                return Number(float(value.string)) , None
            elif not value.string:
                return Number(0) , None
        
        elif isinstance(value , Boolean):
            if value.value:
                return Number(1) , None
            else:
                return Number(0) , None
        
        return None , WrongTypeError(self.file , f"Cannot convert {value} to Number type.")
    execute_Number.params = ["value"]


    def execute_is_collection(self,symbol_table):
        value = symbol_table["value"]
        if isinstance(value , Collection):
            return Boolean(True) , None
        return Boolean(False) , None
    execute_is_collection.params = ["value"]

    def execute_is_function(self,symbol_table):
        value = symbol_table["value"]
        if isinstance(value , BaseFunction):
            return Boolean(True) , None
        return Boolean(False) , None
    execute_is_function.params = ["value"]

    def execute_ltrim(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.lstrip()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'ltrim'.")
    execute_ltrim.params = ["value"]
    
    def execute_rtrim(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.rstrip()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'rtrim'.")
    execute_rtrim.params = ["value"]
    
    def execute_trim(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.strip()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'trim'.")
    execute_trim.params = ["value"]

    def execute_is_int(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            if value.string.isdigit():
                return Boolean(True) , None
            
        elif isinstance(value , Number):
            if str(value.number).isdigit():
                return Boolean(True) , None
        return Boolean(False) , None
        
    execute_is_int.params = ["value"]

    def execute_is_float(self , symbol_table):
        value = symbol_table["value"]
        if isinstance(value , String):
            if isFloat(value.string):
                return Boolean(True) , None
        elif isinstance(value , Number):
            if isFloat(str(value.number)):
                return Boolean(True) , None
            
        return Boolean(False) , None
        
    execute_is_float.params = ["value"]

    def execute_is_alpha(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.isalpha()) , None
        elif isinstance(value , Number):
            return Boolean(str(value.number).isalpha()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'is_alpha'.")
    execute_is_alpha.params = ["value"]

    def execute_is_ascii(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.isascii()) , None
        elif isinstance(value , Number):
            return Boolean(str(value.number).isascii()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'is_ascii'.")
    execute_is_ascii.params = ["value"]
    
    def execute_is_title(self , symbol_table):

        
        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.istitle()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'isTitle'.")
    
    execute_is_title.params = ["value"]

    def execute_lower(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.lower()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'lower'.")
    execute_lower.params = ["value"]

    def execute_upper(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.upper()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'upper'.")
    execute_upper.params = ["value"]

    def execute_is_space(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.isspace()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'is_space'.")
    execute_is_space.params = ["value"]

    def execute_slice(self , symbol_table):

        string = symbol_table["string"]
        start = symbol_table["start"]
        stop = symbol_table["stop"]
        
        if isinstance(string , String):
            return String(string.string[start.number : stop.number]) , None
        
        return None , RunTimeError(self.file , f"{type(string).__name__} has no function 'slice'.")
    execute_slice.params = ["string","start","stop"]

    def execute_is_alnum(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.isalnum()) , None
        elif isinstance(value , Number):
            return Boolean(str(value.number).isalnum()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'is_alnum'.")
    
    execute_is_alnum.params = ["value"]

    def execute_toCap(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.capitalize()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'toCap'.")
    execute_toCap.params = ["value"]

    def execute_endswith(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , Collection):
            return None , RunTimeError(self.file , "Collection has no function 'endswith'.")
        target = symbol_table["target"]
        
        if isinstance(value , String):
            if isinstance(target,String):
                return Boolean(value.string.endswith(target.number)) , None
            elif isinstance(target , Number):
                return Boolean(value.string.endswith(str(target.number))) , None
        elif isinstance(value , Number):
            if isinstance(target , Number):
                return Boolean(str(value.number).endswith(str(target.number))) , None
            elif isinstance(target , String):
                return Boolean(str(value.number).endswith(target.string)) , None
                               
        return None , RunTimeError(self.file , f"Collection has no function 'endswith'.")
    execute_endswith.params = ["value" , "target"]

    def execute_startswith(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , Collection):
            return None , RunTimeError(self.file , "Collection has no function 'startswith'.")
        target = symbol_table["target"]
        
        if isinstance(value , String):
            if isinstance(target,String):
                return Boolean(value.string.startswith(target.number)) , None
            elif isinstance(target , Number):
                return Boolean(value.string.startswith(str(target.number))) , None
        elif isinstance(value , Number):
            if isinstance(target , Number):
                return Boolean(str(value.number).startswith(str(target.number))) , None
            elif isinstance(target , String):
                return Boolean(str(value.number).startswith(target.string)) , None
                               
        return None , RunTimeError(self.file , f"Collection has no function 'startswith'.")
    execute_startswith.params = ["value" , "target"]

    def execute_swapcase(self,symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.swapcase()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'lower'.")
    execute_swapcase.params = ["value"]

    def execute_charat(self , symbol_table):

        value = symbol_table["value"]
        index = symbol_table["index"]

        if not isinstance(index , Number):
            return None , RunTimeError(self.file , f"index cannot be a {type(index).__name__}.")
        
        if not str(index.number).isdigit():
            return None , RunTimeError(self.file , f"index cannot be a 'float'.")

        if isinstance(value , String):
            return String(value.string[index.number]) , None
    
    execute_charat.params = ["value" , "index"]

    def execute_reverse(self,symbol_table):
        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string[::-1]) , None
        elif isinstance(value , Number):
            return Number(int(str(value.number)[::-1])) , None
        elif isinstance(value , Collection):
            return Collection(value.elements[::-1]) , None
    execute_reverse.params = ["value"]
                              

    def no_function(self,symbol_table):

        return None , "undefined function"
