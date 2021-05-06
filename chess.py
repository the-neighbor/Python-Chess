class Piece:
    ascii = {
        'PAWN':"P",
        'ROOK':"R",
        'KNIGHT':"N",
        'BISHOP':"B",
        'KING':"K",
        'QUEEN':"Q"
    }
    def __init__(self, color="WHITE", piece="PAWN"):
        self.color = color
        self.piece = piece
    def piece_ascii(self):
        piece_str = ""
        piece_str += self.color[0]
        piece_str += self.get_ascii()
        return piece_str
    def get_ascii(self):
        return self.ascii[self.piece]
        

class Spot:
    def __init__(self):
        self.state = "EMPTY"
        self.occupant = None
    
    def get_ascii(self):
        if self.state == "EMPTY":
            return "__"
        elif self.state == "FULL" and isinstance(self.occupant, Piece):
            return self.occupant.piece_ascii()
        else:
            return "??"

class Board:
    #THE CLASS FOR THE BOARD. RESPONSIBLE FOR STORING THE STATE OF THE GAME
    def __init__(self):
        #INITIALIZES AN INSTANCE OF THE BOARD CLASS BY INSTANTIATING AND CREATING
        #A 2D MATRIX OF SPOT CLASS INSTANCES
        self.state = [[Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()]]
    def set_spot(self,x,y,value=None):
        #SETS A SPOT ON THE BOARD TO A PARTICULAR VALUE USING X-Y COORDINATES
        if type(value) is Piece:
            self.state[y][x].state = "FULL"
            self.state[y][x].occupant = value
        else:
            self.state[y][x].state = "EMPTY"
    def get_spot(self, x, y):
        return self.state[y][x]
    def setup_board(self):
        #PLACES ALL THE PIECES IN THEIR STARTING POSITION
        self.set_spot(0,0,Piece("WHITE","ROOK"))
        self.set_spot(7,0,Piece("WHITE","ROOK"))
        self.set_spot(1,0,Piece("WHITE","KNIGHT"))
        self.set_spot(6,0,Piece("WHITE","KNIGHT"))
        self.set_spot(2,0,Piece("WHITE","BISHOP"))
        self.set_spot(5,0,Piece("WHITE","BISHOP"))
        self.set_spot(3,0,Piece("WHITE","KING"))
        self.set_spot(4,0,Piece("WHITE","QUEEN"))
        for i in range(0,8):
            self.set_spot(i,1,Piece("WHITE","PAWN"))
        return self
    def print_board(self):
        #PRINTS THE BOARD TO THE TERMINAL USING ASCII CHARACTERS
        board_str = ""
        for y in self.state:
            for x in y:
                board_str += x.get_ascii()
                board_str += " "
            board_str += '\n'
        board_str += '\n'
        print(board_str)    
    def get_position(self, position):
        #RETURNS THE SPOT ON THE BOARD SPECIFIED BY A GIVEN POSITION IN CHESS NOTATION
        coordinate = self.translate_position(position)
        return self.get_spot(coordinate[0], coordinate[1])
    def translate_position(self, position):
        #TAKES A GIVEN CHESS POSITION IN THE FORMAT "E7" AND CONVERTS IT
        #TO XY COORDINATES THAT CAN BE USED TO ACCESS THAT SPOT
        XVALUES = list("ABCDEFGH")
        YVALUES = list("87654321")
        x = XVALUES.index(position[0])
        y = YVALUES.index(position[1])
        return [x,y]
    def move(self, start, end):
        #TAKES TWO CHESS POSITIONS AND MOVES THE PIECE AT 'START' TO OCCUPY 'END'
        #THIS DOES NOT HANDLE VALIDATION BY CHECKING WHETHER OR NOT THE MOVE IS LEGAL.
        #THAT WILL BE CHECKED WITH ANOTHER FUNCTION BEFORE THIS ONE IS CALLED.
        pass


board = Board()
board.setup_board()
board.print_board()
print(board.translate_position("E7"))
print(board.get_position("E7").get_ascii())
