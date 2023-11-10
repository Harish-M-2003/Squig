
class Error:

    def __init__(self,file , name , details , position = None):
        
        self.file = file
        self.name = name
        self.details = details
        self.position = position

    def print(self):
        error_message = f"\n\tFile '{self.file}' at line {self.position.line_number if self.position else None}\n"
        error_message += f"\t{self.name} : {self.details}\n"
        return error_message

class WrongSyntaxError(Error):

    def __init__(self,file , details,position):

        super().__init__(file ,"SyntaxError", details , position=position)

class InvalidLiteral(Error):

    def __init__(self,file,details,position):

        super().__init__(file,"InvalidLiteral" , details , position=position)

class RunTimeError(Error):

    def __init__(self,file,details):

        super().__init__(file,"RunTimeError" , details)

class WrongTypeError(Error):

    def __init__(self , file , details):

        super().__init__(file , "IndexTypeError" , details)

class StringError(Error):

    def __init__(self, file, details):
        super().__init__(file, "StringError" , details) 


class InputStringError(Error):

    def __init__(self, file, details):
        super().__init__(file, "InputStringError" , details)

class InvalidOperationError(Error):

    def __init__(self,file,details):
        super().__init__(file , "OperationError" , details)

class WrongImportError(Error):

    def __init__(self,file,details):
        super().__init__(file , "UseError" , details)