
class Error:

    def __init__(self,file , name , details):
        
        self.file = file
        self.name = name
        self.details = details

    def print(self):
        error_message = f"\n\tFile '{self.file}' at line ,\n"
        error_message += f"\t{self.name} : {self.details}\n"
        return error_message

class WrongSyntaxError(Error):

    def __init__(self,file , details):

        super().__init__(file ,"SyntaxError", details)

class InvalidLiteral(Error):

    def __init__(self,file,details):

        super().__init__(file,"InvalidLiteral" , details)

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