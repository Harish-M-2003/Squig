from Error import *
from os import *
import Interpreter

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



class BaseType:

    def __init__(self , name, value , file=None):

        self.name = name
        self.value = value
        self.file = file
    
    def isType(self , value):

        if type(value) == type(self):
            return True
        return False
    
    def add(self , right_operand):

        if isinstance( self , String) and isinstance(right_operand , String):
            return String(self.string + right_operand.string) , None
        
        if isinstance(self , Number) and isinstance(right_operand , Number):
            return Number(self.number + right_operand.number) , None
        
        if isinstance(self , Collection) and isinstance(right_operand , Collection):
            return Collection(filename=self.file , elements=self.elements + right_operand.elements) , None
        
        if isinstance(self , MutableString) and isinstance(right_operand , MutableString):
            return MutableString(self.string + right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            left_bool = True if self.value == "true" else False
            right_bool = True if right_operand.value == "true" else False
            return Boolean(True if left_bool + right_bool else False) , None
        
        raise Error()

    def div(self , right_operand):
        
        if isinstance(self , Number) and isinstance(right_operand , Number):
            return Number(self.number / right_operand.number) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            left_bool = True if self.value == "true" else False
            right_bool = True if right_operand.value == "true" else False
            try:
                return Boolean(True if left_bool / right_bool else False) , None
            except ZeroDivisionError:
                return None , RunTimeError(self.file , "Cannot divide by false.")

        raise Error()

    def mul(self , right_operand):

        if isinstance(self , String) and isinstance(right_operand , Number): 
            return String(self.string * right_operand.number) , None
        
        if isinstance(self , Number) and isinstance(right_operand , String):
            return String(self.number * right_operand.string) , None
        
        if isinstance(self , Number) and isinstance(right_operand , Number):
            return Number(self.number * right_operand.number) ,  None
        
        if isinstance(self , Collection) and isinstance(right_operand , Number):
            return Collection(filename=self.file , elements=self.elements * right_operand.number) , None
        
        if isinstance(self , Number) and isinstance(right_operand , Collection):
            return Collection(filename=self.file , elements=right_operand.elements * self.number) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value and right_operand.value) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            left_bool = True if self.value == "true" else False
            right_bool = True if right_operand.value == "true" else False
            return Boolean(True if left_bool * right_bool else False) , None
            
        raise Error()
        

    def sub(self , right_operand):

        if isinstance(self , Number) and isinstance(right_operand , Number):
            return Number(self.number - right_operand.number) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            left_bool = True if self.value == "true" else False
            right_bool = True if right_operand.value == "true" else False
            return Boolean(True if left_bool - right_bool else False) , None
        
        raise Error()

    def lt(self , right_operand):
        
        if isinstance( self, String) and isinstance( right_operand , String):
            return Boolean(self.string < right_operand.string) , None
        
        if isinstance(self , MutableString) and isinstance(right_operand , MutableString):
            return Boolean(self.string < right_operand.string) , None
        
        if isinstance(self , Number) and isinstance(right_operand , Number):
            return Boolean(self.number < right_operand.number) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value < right_operand.value) , None

        raise Error()

    def gt(self , right_operand):
        
        if isinstance(self , String) and isinstance(right_operand , String):
            return Boolean(self.string > right_operand.string) , None
        
        if isinstance(self , MutableString) and isinstance(right_operand , MutableString):
            return Boolean(self.string > right_operand.string) , None
        
        if isinstance(self , Number) and isinstance(right_operand , Number):
            return Boolean(self.number > right_operand.number) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value > right_operand.value) , None
        
        raise Error()

    def lte(self , right_operand):
        
        if isinstance(self, String) and isinstance(self , String):
            return Boolean(self.string <= right_operand.string) , None
        
        if isinstance(self , Number) and isinstance(self , Number):
            return Boolean(self.number <= right_operand.number) , None
        
        if isinstance(self , MutableString) and isinstance(self , MutableString):
            return Boolean(self.string <= right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value <= right_operand.value) , None

        raise Error()

    def gte(self , right_operand):
        
        if isinstance(self, String) and isinstance(self , String):
            return Boolean(self.string >= right_operand.string) , None
        
        if isinstance(self , Number) and isinstance(self , Number):
            return Boolean(self.number >= right_operand.number) , None
        
        if isinstance(self , MutableString) and isinstance(self , MutableString):
            return Boolean(self.string >= right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value >= right_operand.value) , None

        raise Error()

    def eql(self , right_operand):
        
        if isinstance(self, String) and isinstance(self , String):
            return Boolean(self.string == right_operand.string) , None
        
        if isinstance(self , Number) and isinstance(self , Number):
            return Boolean(self.number == right_operand.number) , None
        
        if isinstance(self , MutableString) and isinstance(self , MutableString):
            return Boolean(self.string == right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value == right_operand.value) , None

        raise Error()

    def ne(self , right_operand):

        if isinstance(self, String) and isinstance(self , String):
            return Boolean(self.string != right_operand.string) , None
        
        if isinstance(self , Number) and isinstance(self , Number):
            return Boolean(self.number != right_operand.number) , None
        
        if isinstance(self , MutableString) and isinstance(self , MutableString):
            return Boolean(self.string != right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value != right_operand.value) , None

        raise Error()

    def _and_(self , right_operand ):
        
        if isinstance(self, String) and isinstance(right_operand , String):
            return Boolean(self.string and right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            
            left_value = True if self.value == "true" else False
            right_value = False if right_operand.value == "false" else True

            return Boolean(left_value and right_value) , None
        
        if isinstance(self , Number) and isinstance(right_operand , Number):
            return Boolean(self.number and right_operand.number) , None
        
        if isinstance(self , MutableString) and isinstance(right_operand , MutableString):
            return Boolean(self.string and right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value and right_operand.value) , None
        
        raise Error()

    def _or_(self , right_operand):


        if isinstance(self, String) and isinstance(right_operand , String):
            return Boolean(self.string or right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):

            left_value = True if self.value == "true" else False
            right_value = False if right_operand.value == "false" else True

            return Boolean(left_value or right_value) , None
        
        if isinstance(self , Number) and isinstance(right_operand , Number):
            return Boolean(self.number or right_operand.number) , None
        
        if isinstance(self , MutableString) and isinstance(right_operand , MutableString):
            return Boolean(self.string or right_operand.string) , None
        
        if isinstance(self , Boolean) and isinstance(right_operand , Boolean):
            return Boolean(self.value or right_operand.value) , None
        
        raise Error()

class String(BaseType):

    def __init__(self , string ,filename=None):

        super().__init__("String" , string)
        self.string = string
        self.file = filename

    def __repr__(self):

        return f'{self.string}'
    
    def index(self,index): # Need to check this method

        if index > len(self.string):
            return -1

        return String(self.string[index])
    

    
class InputString:

    def value(self , input):

        if isFloat(input):

            return Number(float(input)) , None

        if input.isalpha():
            return String(string=input) , None
        
        elif input.isdigit():
            return Number(int(input)) , None
        
        return String(string=input, filename=None) , None
        
        

class Collection(BaseType):

    def __init__(self , filename , elements):

        super().__init__("Collection" , elements)
        self.elements = elements
        self.file = filename

    def __repr__(self):

        return f"{self.elements}".replace('[','{ ').replace(']',' }')


    def index(self,index): # Need to check this method

        if index > len(self.elements):
            return Number(-1)

        return self.elements[index]
    

class  Boolean(BaseType):

    def __init__(self , value):

        super().__init__("Boolean" , value)
        self.value = str(value).lower() if type(value).__name__ == "bool" else value
        
        # In the above line if the value is of type bool it is converted to a lower case string and stored in the
        # self.value propertie . need to implement it in a better way.

    def __repr__(self):

        return f"{self.value}"
    
    def _not_(self):
        return Boolean("true" if self.value != "true" else "false")
    
    


class Number(BaseType):

    def __init__(self,number):

        super().__init__("Number" , number)
        self.number = number
        self.file = "change to file name later info for harish"

    def __repr__(self):

        return f"{self.number}"

    
    def pow(self , number):
        if isinstance(number , Number):
            return Number(self.number ** number.number) , None
        # elif isinstance(number , String):
        #     if number.string.isdigit():
        #         return Number(self.number ** int(number.string)) , None
        raise Error()
    
    def modulo(self , number):

        if isinstance(number , Number):
            return Number(self.number % number.number) , None
        raise Error()

class BaseFunction(BaseType):

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

    def __repr__(self):

        return f"Function< {id(self)} >"
    
    def execute(self , args , global_symbol_table = None):

        local_symbol_table = {}
        local_symbol_table.update(global_symbol_table)
        function_processor = Interpreter.Interpreter(self.file , local_symbol_table)
        
        status , error = self.check_param_and_arg_length(self.params , args)
        if error:
            return None , error
        
        self.update_local_symnol_table(self.params , args , local_symbol_table)
        # print("executing")
        
        function_expression , error = function_processor.process(self.body)

        if error:
            return None , error
        return function_expression , None


class BuiltinFunction(BaseFunction):

    def __init__(self,file , variable ):

        self.file = file
        self.variable = variable

    def execute(self , args  , global_symbol_table = None):
        
        local_symbol_table = {}
        method = getattr(self , f"execute_{self.variable}" , self.no_function)
        
        self.update_local_symnol_table(method.params , args , local_symbol_table )

        return method(local_symbol_table)
    
    def execute_int(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , Number):
            return Number(int(value.value)) , None
    execute_int.params = ["value"]

    def execute_isUpper(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return  Boolean(value.string.isupper()) , None
    execute_isUpper.params = ["value"]    
    
    def execute_isLower(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.islower()) , None
    execute_isLower.params = ["value"]    

    def execute_MutableString(self , symbol_table):
        value = symbol_table["value"]
        if isinstance(value , String) :
            return MutableString(value.string) , None
        if isinstance(value , MutableString):
            return MutableString(value.string) , None
        return None , WrongTypeError(self.file , f"Cannot convert {type(value).__name__} to MutableString.")
    
    execute_MutableString.params = ["value"]
    
    def execute_title(self , symbol_table):

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.title()) , None
    execute_title.params = ["value"]

    def execute_split(self , symbol_table):

        value = symbol_table["value"]
        pattern = symbol_table["pattern"]
        if isinstance(value , String):
            return Collection(filename=self.file , elements=list(map(String , value.string.split(pattern.string)))) , None
        
    execute_split.params = ["value" , "pattern"]
    
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
        
        if isinstance(value , Boolean):

            if value.value:
                return Boolean(True) , None
            else:
                return Boolean(False) , None
        
        return None , WrongTypeError(self.file , f"Cannot convert {type(value).__name__} to Bool.")
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
        
        if isinstance(value , HashMap):
            return Number(len(value.key_values)) , None
        
        if isinstance(value , MutableString):
            return Number(len(value.string)) , None
         
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


    def execute_is_collection(self,symbol_table): # Types Checked
        value = symbol_table["value"]
        if isinstance(value , Collection):
            return Boolean(True) , None
        return Boolean(False) , None
    execute_is_collection.params = ["value"]

    def execute_is_function(self,symbol_table): # Types Checked
        value = symbol_table["value"]
        if isinstance(value , BaseFunction):
            return Boolean(True) , None
        return Boolean(False) , None
    execute_is_function.params = ["value"]

    def execute_ltrim(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.lstrip()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'ltrim'.")
    execute_ltrim.params = ["value"]
    
    def execute_rtrim(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.rstrip()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'rtrim'.")
    execute_rtrim.params = ["value"]
    
    def execute_trim(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.strip()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'trim'.")
    execute_trim.params = ["value"]

    def execute_is_int(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            if value.string.isdigit():
                return Boolean(True) , None
            
        elif isinstance(value , Number):
            if str(value.number).isdigit():
                return Boolean(True) , None
        return Boolean(False) , None
        
    execute_is_int.params = ["value"]

    def execute_is_float(self , symbol_table): # Types Checked
        value = symbol_table["value"]
        if isinstance(value , String):
            if isFloat(value.string):
                return Boolean(True) , None
        elif isinstance(value , Number):
            if isFloat(str(value.number)):
                return Boolean(True) , None
            
        return Boolean(False) , None
        
    execute_is_float.params = ["value"]

    def execute_is_alpha(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.isalpha()) , None
        # elif isinstance(value , Number):
        #     return Boolean(str(value.number).isalpha()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'is_alpha'.")
    execute_is_alpha.params = ["value"]

    def execute_is_ascii(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.isascii()) , None
        # elif isinstance(value , Number):
        #     return Boolean(str(value.number).isascii()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'is_ascii'.")
    execute_is_ascii.params = ["value"]
    
    def execute_is_title(self , symbol_table): # Types Checked

        
        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.istitle()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'isTitle'.")
    
    execute_is_title.params = ["value"]

    def execute_lower(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.lower()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'lower'.")
    execute_lower.params = ["value"]

    def execute_upper(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.upper()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'upper'.")
    execute_upper.params = ["value"]

    def execute_is_space(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.isspace()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'is_space'.")
    execute_is_space.params = ["value"]

    def execute_slice(self , symbol_table): # Types Checked

        string = symbol_table["string"]
        start = symbol_table["start"]
        stop = symbol_table["stop"]
        
        if isinstance(string , String):
            return String(string.string[start.number : stop.number]) , None
        
        return None , RunTimeError(self.file , f"{type(string).__name__} has no function 'slice'.")
    execute_slice.params = ["string","start","stop"]

    def execute_is_alnum(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return Boolean(value.string.isalnum()) , None
        # elif isinstance(value , Number):
        #     return Boolean(str(value.number).isalnum()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'is_alnum'.")
    
    execute_is_alnum.params = ["value"]

    def execute_toCap(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.capitalize()) , None
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'toCap'.")
    execute_toCap.params = ["value"]

    def execute_endswith(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , Collection):
            return None , RunTimeError(self.file , "Collection has no function 'endswith'.")
        target = symbol_table["target"]
        
        if isinstance(value , String) and isinstance(target,String):
                return Boolean(value.string.endswith(target.number)) , None
        #     elif isinstance(target , Number):
        #         return Boolean(value.string.endswith(str(target.number))) , None
        # elif isinstance(value , Number):
        #     if isinstance(target , Number):
        #         return Boolean(str(value.number).endswith(str(target.number))) , None
        #     elif isinstance(target , String):
        #         return Boolean(str(value.number).endswith(target.string)) , None
                               
        return None , RunTimeError(self.file , f"Collection has no function 'endswith'.")
    execute_endswith.params = ["value" , "target"]

    def execute_startswith(self , symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , Collection):
            return None , RunTimeError(self.file , "Collection has no function 'startswith'.")
        target = symbol_table["target"]
        
        if isinstance(value , String) and isinstance(target,String):
                return Boolean(value.string.startswith(target.string)) , None
            # elif isinstance(target , Number):
            #     return Boolean(value.string.startswith(str(target.number))) , None
        # elif isinstance(value , Number):
        #     if isinstance(target , Number):
        #         return Boolean(str(value.number).startswith(str(target.number))) , None
        #     elif isinstance(target , String):
        #         return Boolean(str(value.number).startswith(target.string)) , None
                               
        return None , RunTimeError(self.file , f"Collection has no function 'startswith'.")
    execute_startswith.params = ["value" , "target"]

    def execute_swapcase(self,symbol_table): # Types Checked

        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string.swapcase()) , None
        
        return None , RunTimeError(self.file , f"{type(value).__name__} has no function 'lower'.")
    execute_swapcase.params = ["value"]

    def execute_charat(self , symbol_table): # Types checked

        value = symbol_table["value"]
        index = symbol_table["index"]

        # if not isinstance(index , Number):
        #     return None , RunTimeError(self.file , f"index cannot be a {type(index).__name__}.")
        
        if not str(index.number).isdigit():
            return None , RunTimeError(self.file , f"index cannot be a 'float'.")

        if isinstance(value , String):
            return String(value.string[index.number]) , None
    
    execute_charat.params = ["value" , "index"]

    def execute_reverse(self,symbol_table): # Types checked
        value = symbol_table["value"]
        if isinstance(value , String):
            return String(value.string[::-1]) , None
        # elif isinstance(value , Number):
        #     return Number(int(str(value.number)[::-1])) , None
        # elif isinstance(value , Collection):
        #     return Collection(value.elements[::-1]) , None
    execute_reverse.params = ["value"]
                              

    def no_function(self , symbol_table):

        return None , "undefined function"
    
class File:

    def __init__(self , file , file_name):

        self.file = file
        self.file_name = file_name

    def __repr__(self):

        return f"File( {self.file_name} )"

    def content(self):

        return String(self.file.read())
    
    def write(self , content):

        self.file.write(content)
        # return self
    
    def close(self):

        self.file.close()


class HashMap(BaseType):

    """
        The 'HashMap' or 'Map' is a ordered datatype which stores key , value paris. 
        In "HashMap" or "Map" we can create , update and delete (key , value) pairs either by key or index.
        since the "Map" is a ordered pair , their values can be accessed either by key or index.

        feature idea : Mohan Dass.
    """

    

    def __init__(self , key_values , index_values):

        self.key_values = key_values
        self.index_values = index_values
        self.length = len(self.key_values)
        super().__init__("Map" , self.key_values)

    def __repr__(self):

        return f"{self.key_values}"

        # formatted = "{ "

        # for key , value in self.key_values.items():
        #     formatted += str(key) + " : " +  str(value) + " , "
        
        # formatted = formatted[:-2].strip() +  " }"
        
        # return formatted if self.key_values else ''
    
    
class MutableString(BaseType):

    """
        The 'Mutable string' is a string datatype in which we can create , update and 
        remove letters or words from a Mutable string. 
        
        In otherwords , it's a mutable string datatype (i.e) it values can be changed at runtime.

        feature idea : Mohan Dass
    """

    def __init__(self , string):

        self.string = string
        self.mut_string = [char for char in string]

    
    def __repr__(self):

        return f"{self.string}"

    def include(self , index , char):

        """
            The 'include' method is used to add a letter in the mutable string ,
            it takes the index and letter as parameter for processing the mutable string.

        """

        if  index < len(self.mut_string) and index >= 0 :
            # self.mut_string[index] =  char #this the bug
            del self.mut_string[index]
            # self.mut_string = self.mut_string[:index] + list(char) + self.mut_string[index :]
            self.mut_string.insert(index , char)
            self.string = MutableString("".join(self.mut_string))
        else:
            return None ,  None
        # Need to handle this
        
        return self , None
    

    def remove(self , index):
        
        """
            The 'remove' pop the specified letter at the index in the mutable string.
            Once the letter is pop from the self.mut_string property , the string property get
            updated to reflect the changes in the language.
        """

        value = self.mut_string[index]

        del self.mut_string[index]
        self.string = MutableString("".join(self.mut_string))
        return value , None
    
    def __len__(self):

        return len(self.mut_string)
    