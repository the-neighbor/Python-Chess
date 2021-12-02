import numpy
import piece_moves
import copy

validate_coordinates = piece_moves.validate_coordinates
cast_ray = piece_moves.cast_ray

#POSITION CLASS STORES A GIVEN POSITION ON THE CHESS BOARD
#WHEN INITIALIZED, IT TAKES IN A POSITION AS EITHER A PAIR OF COORDINATES
#OR AS A STRING CONTAINING A BOARD POSITION IN CHESS NOTATION
#AND IT THEN CONVERTS THIS INTO AN OBJECT WHICH CONTAINS BOTH
#THE CHESS NOTATION OF THE POSITION AND A 2D VECTOR WITH THE POSITION COORDINATES
#THIS MAKES IT EASIER TO HANDLE CONVERSIONS BETWEEN THE TWO
#AND FACILITATES THE USE OF VECTOR OPERATIONS LIKE ADDITION AND MULTIPLICATION
#TO EASILY CALCULATE NEW BOARD POSITIONS FROM A STARTING POSITION AND A MOVEMENT VECTOR
class Position:
    def __init__(self, position):
        XVALUES = list("ABCDEFGH")
        YVALUES = list("87654321")
        self.chess_notation = ""
        self.vector = numpy.array([-1,-1])
        if isinstance(position, str):
            #POSITION CAN BE PROVIDED AS A STRING LIKE "A2"
            position = position.upper()
            if position[0] in XVALUES and position[1] in YVALUES:
                self.chess_notation = position
                x = XVALUES.index(position[0])
                y = YVALUES.index(position[1])
                self.vector = numpy.array([x,y])
        elif isinstance(position, (numpy.ndarray, list)):
            #POSITION CAN ALSO BE PROVIDED AS A VECTOR(NUMPY ARRAY)
            if position[0] in range(0,8) and position[1] in range(0,8): 
                self.vector = position.copy()
                chess_notation = ""
                chess_notation += XVALUES[self.vector[0]]
                chess_notation += YVALUES[self.vector[1]]
                self.chess_notation = chess_notation
    def print(self):
        #PRINT BOTH FORMS OF THE NOTATION TO STDOUT
        print(self.chess_notation)
        #print(self.vector)
    def add_move(self, movement_vector):
        #USE THE VECTOR ADDITION PROVIDED BY NUMPY TO RETURN THE POSITION
        #YOU WOULD ARRIVE AT IF YOU FOLLOWED SOME MOVEMENT VECTOR FROM THIS ONE.
        if not isinstance(movement_vector, numpy.ndarray):
            movement_vector = numpy.array(movement_vector)
        return Position(self.vector + movement_vector)


#PIECE CLASS STORES THE ATTRIBUTES OF A PARTICULAR PIECE. IT IS RESPONSIBLE FOR
#STORING WHAT KIND OF CHESS PIECE IT IS, AS WELL AS THE COLOR, AND USING THAT
#TO DETERMINE WHAT POTENTIAL MOVES CAN BE MADE FROM A GIVEN BOARD POSITION.
#IN OUR CASE, WE CURRENTLY USE THE PIECE CLASS TO STORE AND PRINT THE ASCII
#REPRESENTATION THAT CORROSPONDS TO THAT PIECE
class Piece:
    ascii = {
        'PAWN':"P",
        'ROOK':"R",
        'KNIGHT':"N",
        'BISHOP':"B",
        'KING':"K",
        'QUEEN':"Q"
    }
    def __init__(self, board, color="WHITE", piece="PAWN"):
        self.board = board
        self.color = color
        self.piece = piece
        self.move_counter = 0
        self.capture_counter = 0
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
        moves = self.piece_moves(self, self.board, position)
        #print(moves)
        return_moves = {"moves":[], "captures":[]}
        for m in moves["moves"]:
            #CREATE A COPY OF THE ORIGINAL COORDINATES
            #ADD THE X/Y VALUES OF A MOVE VECTOR TO THAT COORDINATE
            if self.color == "BLACK" and self.piece == "PAWN":
                m *= -1
            new_position = position.add_move(m)
            if validate_coordinates(new_position):
                return_moves["moves"].append(new_position)
        for c in moves["captures"]:
            #CREATE A COPY OF THE ORIGINAL COORDINATES
            #ADD THE X/Y VALUES OF A CAPTURE VECTOR TO THAT COORDINATE
            if self.color == "BLACK" and self.piece == "PAWN":
                c *= -1
            new_position = position.add_move(c)
            #print (new_position.chess_notation)
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
        #FIRST PLACE THE WHITE PIECES
        self.set_spot(0,0,Piece(self, "WHITE","ROOK"))
        self.set_spot(7,0,Piece(self, "WHITE","ROOK"))
        self.set_spot(1,0,Piece(self, "WHITE","KNIGHT"))
        self.set_spot(6,0,Piece(self, "WHITE","KNIGHT"))
        self.set_spot(2,0,Piece(self, "WHITE","BISHOP"))
        self.set_spot(5,0,Piece(self, "WHITE","BISHOP"))
        self.set_spot(3,0,Piece(self, "WHITE","KING"))
        self.set_spot(4,0,Piece(self, "WHITE","QUEEN"))
        for i in range(0,8):
            self.set_spot(i,1,Piece(self, "WHITE","PAWN"))
        self.set_spot(0,7,Piece(self, "BLACK","ROOK"))
        self.set_spot(7,7,Piece(self, "BLACK","ROOK"))
        self.set_spot(1,7,Piece(self, "BLACK","KNIGHT"))
        self.set_spot(6,7,Piece(self, "BLACK","KNIGHT"))
        self.set_spot(2,7,Piece(self, "BLACK","BISHOP"))
        self.set_spot(5,7,Piece(self, "BLACK","BISHOP"))
        self.set_spot(3,7,Piece(self, "BLACK","KING"))
        self.set_spot(4,7,Piece(self, "BLACK","QUEEN"))
        for i in range(0,8):
            self.set_spot(i,6,Piece(self, "BLACK","PAWN"))
        return self
    def print_board(self):
        #PRINTS THE BOARD TO THE TERMINAL USING ASCII CHARACTERS
        board_str = "  "
        XVALUES = list("ABCDEFGH")
        YVALUES = list("87654321")
        index = 0
        for c in XVALUES:
            board_str += (c)
            board_str += "  "
        board_str += "\n"
        for y in self.state:
            board_str += (YVALUES[index])
            board_str += " "
            for x in y:
                board_str += x.get_ascii()
                board_str += " "
            board_str += '\n'
            index += 1
        board_str += '\n'
        print(board_str)    
    def get_position(self, position):
        #RETURNS THE SPOT ON THE BOARD SPECIFIED BY A GIVEN POSITION IN CHESS NOTATION
        coordinate = self.translate_position(position)
        return self.get_spot(coordinate[0], coordinate[1])
    def get_spot_by_position(self, position):
        #RETURNS THE SPOT ON THE BOARD SPECIFIED BY A POSITION OBJECT 
        return self.get_spot(position.vector[0], position.vector[1])
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
        end_spot.occupant.move_counter += 1
        start_spot.empty()
        pass
    def look_ahead(self, start, end):
        board_state = copy.deepcopy(self)
        board_state.move(start, end)
        return board_state
    def capture(self, start, end):
        #MOVES, BUT ALSO ADDS THE CAPTURED PIECE TO A LIST
        self.move(start, end)
        end_spot.occupant.capture_counter += 1
    def check(self, color):
        #EVAL THE CURRENT STATE OF THE BOARD TO DETERMINE IF EITHER PLAYER HAS CHECK
        #IF NOT, RETURN FALSE, IF SO, RETURN THE PLAYER WHO HAS THE OTHER PLAYER IN CHECK
        check = False
        potential_captures = self.possible_captures(color)
        for c in potential_captures:
            print(c)
            spot = self.get_spot_by_position(c)
            if spot and spot.state == "FULL" :
                if spot.occupant.color != color and spot.occupant.piece == "KING":
                    check = True
        return check
    def checkmate(self):
        #EVAL THE CURRENT STATE OF THE BOARD TO DETERMINE IF EITHER PLAYER HAS CHECKMATE
        #IF NOT, RETURN FALSE, IF SO, RETURN THE PLAYER WHO HAS CHECKMATE/THE WINNER
        pass
    def possible_selections(self, color):
        #RETURN AN ARRAY OF POSITIONS THAT ARE OCCUPIED BY A GIVEN SIDE
        possibilities = []
        for y in range(0,8):
            for x in range(0,8):
                current_spot = self.get_spot_by_position(Position([x,y]))
                if current_spot and current_spot.state == "FULL":
                    if current_spot.occupant.color == color:
                        possibilities.append(Position([x,y]))
        return possibilities
    def possible_moves(self, position):
        #PASSED IN A POSITION AS A PARAMETER, RETURN THE LIST OF POSSIBLE MOVES
        #THAT CAN BE MADE WITH THE PIECE ON THAT POSITION
        spot = self.get_spot_by_position(position)
        if spot and spot.state == "FULL":
            moves = spot.occupant.eval_moves(position)
            return moves
    def possible_captures(self, color):
        #get possible captures
        movable_pieces = self.possible_selections(color)
        possibilities = []
        for p in movable_pieces:
            #p.print()
            current_piece_moves = self.possible_moves(p)
            for m in current_piece_moves['captures']:
                #m.print()
                if self.validate_capture(color,p.chess_notation,m.chess_notation):
                    m.print()
                    possibilities.append(m)
        return possibilities
    def valid_position(self, position):
        return validate_coordinates(position)
    def validate_move(self, side, origin, destination):
        #CHECK THAT A MOVE IS VALID BY MAKING SURE THAT THE FOLLOWING CONDITIONS ARE MET:
        #THAT THE ORIGIN AND DESTINATION ARE BOTH VALID BOARD POSITIONS
        #THAT THE ORIGIN IS OCCUPIED BY A PIECE WHOSE COLOR == SIDE
        #THAT THE DESTINATION IS EMPTY
        origin = Position(origin)
        destination = Position(destination)
        if side and self.valid_position(origin) and self.valid_position(destination):
            origin_spot = self.get_spot_by_position(origin)
            destination_spot = self.get_spot_by_position(destination)
            if origin_spot.state == "FULL" and \
               origin_spot.occupant.color == side and \
               destination_spot.state == "EMPTY":
                if any(destination.chess_notation == d.chess_notation for d in self.possible_moves(origin)["moves"]):
                    return True
        return False
    def validate_capture(self, side, origin, destination):
        #CHECK THAT A CAPTURE IS VALID BY MAKING SURE THAT THE DESTINATION IS VALID AND OCCUPIED BY A PIECE OF THE OPPOSITE COLOR
        origin = Position(origin)
        destination = Position(destination)
        if side and self.valid_position(origin) and self.valid_position(destination):
            origin_spot = self.get_spot_by_position(origin)
            destination_spot = self.get_spot_by_position(destination)
            if origin_spot.state == "FULL" and \
               origin_spot.occupant.color == side and \
               destination_spot.state == "FULL" and \
               destination_spot.occupant.color != side:
                if any(destination.chess_notation == d.chess_notation for d in self.possible_moves(origin)["captures"]):
                    return True
        return False

def take_turn(board, side):
    #TAKES IN A BOARD WITH THE CURRENT STATE OF A CHESS GAME
    #AND THE SIDE TO GO AS A BOOL (TRUE = BLACK, FALSE = WHITE)
    #GETS COMMAND (EX. MOVE E7 E5) USING GET_STRING() OR GET_INPUT()
    #USES SPLIT() TO BREAK THE COMMAND INTO THE NAME OF THE BOARD METHOD
    #TO BE CALLED AND THE ARGUMENTS/PARAMETERS FOR THAT FUNCTION CALL
    board.print_board()
    #BOOL SO WE KNOW WHEN THE TURN IS OVER
    turn_complete = False
    #UNTIL THE TURN IS COMPLETE, PROMPT FOR INPUT
    while not turn_complete:
        #PROMPT USER FOR INPUT
        print("CHECK?\nBLACK:%s WHITE:%s" % (str(board.check('BLACK')),str(board.check('WHITE'))))
        command = input('%s: WHAT IS YOUR COMMAND?\n' % side)
        #SPLIT INPUT INTO COMMAND AND PARAMETERS
        command_array = command.split()
        if command_array[0] == "MOVE":
            #COMMAND TO HANDLE MOVING A PIECE FROM ONE TILE TO ANOTHER
            if board.validate_move(side, command_array[1], command_array[2]):
                board.move(command_array[1], command_array[2])
                turn_complete = True
            else:
                print("Error")
            #TO ADD:
            #ADD VALIDATION TO CHECK AND MAKE SURE THAT THE MOVE IS VALID BEFORE EXECUTING
            #DO THIS BY USING THE BOARD'S POSSIBLE MOVES METHOD.
            #CHECK THAT THE THIRD ARGUMENT, THE TARGET
            #IS IN THE MOVES ELEMENT OF THE DICT RETURNED BY CALLING POSSIBLE_MOVES()
            #ON THE SECOND ARGUMENT, THE PIECE THE PLAYER WANTS TO MOVE.
            #TARGET MUST ALSO BE EMPTY
        if command_array[0] == "CAPTURE":
                #COMMAND TO HANDLE CAPTURING ONE PIECE BY MOVING YOUR OWN PIECE.
                #SIMILAR VALIDATION TO THE MOVE COMMAND, JUST ALSO HAVE TO CHECK THAT THE TILE WE WANT
                #TO CAPTURE
            if board.validate_capture(side, command_array[1], command_array[2]):
                board.capture(command_array[1], command_array[2])
                turn_complete = True
            else:
                print ("Error")
        if command_array[0] == "PIECES":
            for i in board.possible_selections(side):
                print (i.chess_notation)
        if command_array[0] == "LISTMOVES":
            #USE THE NEXT ARGUMENT AS THE LOCATION OF THE PIECE WE WANT TO LIST THE MOVES FOR
            moves = board.possible_moves(Position(command_array[1]))
            if moves:
                print ("MOVES: ")
                for m in moves['moves']:
                    print (m.chess_notation)
                print ("CAPTURES: ")
                for c in moves['captures']:
                    if board.validate_capture(side, command_array[1], c.chess_notation):
                        print (c.chess_notation)

board = Board()
def play_game(board):
    #FUNCTION TO INITIATE AND CARRY A GAME TO COMPLETION
    
    #SETUP THE CHESS BOARD WITH THE STARTING POSITION OF ALL THE PIECES
    board.setup_board()
    #PRINT THE STATE OF THE CHESS BOARD
    board.print_board()
    #SET A COUNTER FOR THE TURNS
    turn_counter = 0
    #UNTIL WE REACH CHECKMATE
    while not (board.checkmate()):
        #TAKE THE TURN OF EACH PLAYER
        if turn_counter % 2:
            #ON ODD TURNS, BLACK GOES
            take_turn(board, "BLACK")
        else:
            #ON EVEN TURNS, WHITE GOES
            take_turn(board, "WHITE")
        turn_counter += 1
#board.setup_board()
#print(board.translate_position("E7"))
#print(board.get_position("G8").get_ascii())
#board.move("H7", "H4")
#board.print_board()
#position = Position("H4")
#moves = piece_moves.eval_moves(position, piece_moves.pawn_moves())
#print(moves)
#moves = board.get_position("G8").occupant.eval_moves(Position("G8"))
#for m in moves["moves"]:
#    m.print()

board.setup_board()


play_game(board)

