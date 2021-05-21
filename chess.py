import numpy
import piece_moves

validate_coordinates = piece_moves.validate_coordinates

class Position:
    def __init__(self, position):
        XVALUES = list("ABCDEFGH")
        YVALUES = list("87654321")
        if isinstance(position, str):
            #POSITION CAN BE PROVIDED AS A STRING LIKE "A2"
            position = position.upper()
            self.chess_notation = position
            x = XVALUES.index(position[0])
            y = YVALUES.index(position[1])
            self.vector = numpy.array([x,y])
        elif isinstance(position, (numpy.ndarray)):
            #POSITION CAN ALSO BE PROVIDED AS A VECTOR(NUMPY ARRAY)
            self.vector = position.copy()
            chess_notation = ""
            chess_notation += XVALUES[self.vector[0]]
            chess_notation += YVALUES[self.vector[1]]
            self.chess_notation = chess_notation
    def print(self):
        print(self.chess_notation)
        print(self.vector)
    def add_move(self, movement_vector):
        if not isinstance(movement_vector, numpy.ndarray):
            movement_vector = numpy.array(movement_vector)
        return Position(self.vector + movement_vector)

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
        self.piece_moves = piece_moves.move_methods[self.piece]
    def piece_ascii(self):
        piece_str = ""
        piece_str += self.color[0]
        piece_str += self.get_ascii()
        return piece_str
    def get_ascii(self):
        return self.ascii[self.piece]
    def eval_moves(self, position):
        #REFACTOR THE EVAL
        moves = self.piece_moves()
        return_moves = {"moves":[], "captures":[]}
        for m in moves["moves"]:
            #CREATE A COPY OF THE ORIGINAL COORDINATES
            #ADD THE X/Y VALUES OF A MOVE VECTOR TO THAT COORDINATE
            if self.color == "BLACK":
                m *= -1
            new_position = position.add_move(m)
        if validate_coordinates(new_position):
            return_moves["moves"].append(new_position)
        for c in moves["captures"]:
            #CREATE A COPY OF THE ORIGINAL COORDINATES
            #ADD THE X/Y VALUES OF A CAPTURE VECTOR TO THAT COORDINATE
            new_position = position.add_move(c)
            if validate_coordinates(new_position):
                return_moves["captures"].append(new_position)
            return return_moves
    
        

class Spot:
    def __init__(self):
        self.state = "EMPTY"
        self.occupant = None
    def occupy(self, new_occupant):
        #OCCUPY SPOT WITH NEW PIECE
        self.occupant = new_occupant
        self.state = "FULL"
    def empty(self):
        #CLEAR SPOT
        self.occupant = None
        self.state = "EMPTY"
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
        start_spot = self.get_position(start)
        end_spot = self.get_position(end)
        end_spot.occupy(start_spot.occupant)
        start_spot.empty()
        pass

def take_turn(board, side):
    #TAKES IN A BOARD WITH THE CURRENT STATE OF A CHESS GAME
    #AND THE SIDE TO GO AS A BOOL (TRUE = BLACK, FALSE = WHITE)
    #GETS COMMAND (EX. MOVE E7 E5) USING GET_STRING() OR GET_INPUT()
    #USES SPLIT() TO BREAK THE COMMAND INTO THE NAME OF THE BOARD METHOD
    #TO BE CALLED AND THE ARGUMENTS/PARAMETERS FOR THAT FUNCTION CALL
    command = raw_input('%s: WHAT IS YOUR COMMAND?' % side)
    command_array = command.split()
    if command_array[0] == "MOVE":
        board.move()
    
board = Board()
board.setup_board()
board.print_board()
print(board.translate_position("E7"))
print(board.get_position("E7").get_ascii())
board.move("H7", "H4")
board.print_board()
position = Position("H4")
#moves = piece_moves.eval_moves(position, piece_moves.pawn_moves())
#print(moves)
moves = board.get_position("E7").occupant.eval_moves(Position("E7"))
for m in moves["moves"]:
    m.print()
