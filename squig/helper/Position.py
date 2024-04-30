
class Position:

    def __init__(self , file_name = None ,line_number = 0 , column_number = -1 , index = -1):

        self.line_number = line_number
        self.column_number = column_number
        self.file_name = file_name
        self.index = index
        # self.next()
    
    def next(self , currnet_char):

        self.index += 1
        self.column_number += 1

        if currnet_char == ';':
            self.line_number +=1
            self.column_number = 0
        
    def copy_position(self):

        return Position(file_name=self.file_name , line_number=self.line_number + 1 , column_number=self.column_number , index=self.index)