
class Cache:

    ## This class keeps a recode of processed statements.

    def __init__(self):

        self.statements = ()
    
    def add(self , code):

        self.statements += (code , )