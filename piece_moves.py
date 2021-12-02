import numpy

def cast_ray(board, position, direction):
    #CAST A RAY OUT FROM A POSITION IN A GIVEN DIRECTION AND
    #STOP UPON HITTING A PIECE OR THE EDGE OF THE BOARD
    #USED FOR PIECES LIKE THE BISHOP, ROOK, QUEEN, WHERE
    #MOVEMENT CAN BE OBSTRUCTED BY OTHER PIECES.
    collision = []
    traversed = []
    return_dict = {}
    
    if board and validate_coordinates(position) and direction:
        direction = numpy.array(direction)
        ray_position = position.add_move(direction)
        distance_traveled = direction.copy()
        while validate_coordinates(ray_position) and len(collision) == 0:
            current_spot = board.get_spot_by_position(ray_position)
            if current_spot.state == "FULL":
                collision = distance_traveled
                break
            else:
                traversed.append(distance_traveled.copy())
            ray_position = ray_position.add_move(direction)
            distance_traveled += direction
    return_dict = {'collision':collision, 'traversed':traversed}
    return return_dict

def moves_from_rays(board, position, directions):
    #CAST MULTIPLE RAYS FROM A POSITION ON THE BOARD USING A LIST OF DIRECTIONS
    #AND ASSEMBLE THE RESULTS OF THE RAY CAST INTO A LIST OF MOVES AND CAPTURES
    moves = []
    captures = []
    for d in directions:
        ray = cast_ray(board, position, d)
        if ray:
            if len(ray['collision']):
                captures.append(ray['collision'])
            if len(ray['traversed']):
                moves = moves + ray['traversed']
    return {"moves":moves, "captures":captures}
    
def pawn_moves(piece,board,position):
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A PAWN CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    moves = []
    captures = []
    moves.append(numpy.array([0,1]))
    captures.append(numpy.array([1,1]))
    captures.append(numpy.array([-1,1]))
    if piece.move_counter == 0:
        moves.append(numpy.array([0,2]))
    return {"moves":moves, "captures":captures}

def rook_moves(piece,board,position):
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A ROOK CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    directions = [[1,0],[-1,0],[0,-1],[0,1]]
    return moves_from_rays(board, position, directions)

def bishop_moves(piece,board, position):
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A BISHOP CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    directions = [[1,1],[1,-1],[-1,-1],[-1,1]]
    return moves_from_rays(board, position, directions)

def knight_moves(piece,board,position):
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A KNIGHT CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    moves = [numpy.array([1,2]),numpy.array([2,1]),numpy.array([-1,2]),numpy.array([-2,1]),numpy.array([1,-2]),numpy.array([2,-1]),numpy.array([-1,-2]),numpy.array([-2,-1])]
    captures = numpy.array([[1,2],[2,1],[-1,2],[-2,1],[1,-2],[2,-1],[-1,-2],[-2,-1]])
    return {"moves":moves, "captures":captures}

def queen_moves(piece,board,position):
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A QUEEN CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    #BISHOP + ROOK
    directions = [[1,0],[-1,0],[0,-1],[0,1],[1,1],[1,-1],[-1,-1],[-1,1]]
    return moves_from_rays(board, position, directions)

def king_moves(piece,board,position):
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A KING CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    #EVERY COMBINATION OF 0,1, AND -1 EXCEPT 0,0
    moves = [[1,0],[-1,0],[0,-1],[0,1],[1,1],[1,-1],[-1,-1],[-1,1]]
    captures = [[1,0],[-1,0],[0,-1],[0,1],[1,1],[1,-1],[-1,-1],[-1,1]]
    return {"moves":moves, "captures":captures}

def validate_coordinates(position):
    coordinates = position.vector
    #CHECK IF A GIVEN PAIR OF COORDINATES ON THE BOARD MAPS TO A VALID LOCATION ON THE BOARD
    if coordinates[0] >= 0 and coordinates[0] < 8 and \
       coordinates[1] >= 0 and coordinates[1] < 8:
        return True
    else:
        return False

def eval_moves(position, moves):
    #TAKE IN THE CURRENT POSITION AND A DICTIONARY OF MOVES AND CAPTURES.
    #REPLACE ALL MOVES AND CAPTURES WITH THE RESULTING LOCATIONS ON THE BOARD
    return_moves = {"moves":[], "captures":[]}
    for m in moves["moves"]:
        #CREATE A COPY OF THE ORIGINAL COORDINATES
        #ADD THE X/Y VALUES OF A MOVE VECTOR TO THAT COORDINATE
        new_position = [*position]
        print(new_position)
        print(m)
        new_position[0] += m[0]
        new_position[1] += m[1]
        if validate_coordinates(new_position):
            return_moves["moves"].append(new_position)
    for c in moves["captures"]:
        #CREATE A COPY OF THE ORIGINAL COORDINATES
        #ADD THE X/Y VALUES OF A CAPTURE VECTOR TO THAT COORDINATE
        new_position = [*position]
        print(new_position)
        print(c)
        new_position[0] += c[0]
        new_position[1] += c[1]
        if validate_coordinates(new_position):
            return_moves["captures"].append(new_position)
    return return_moves

move_methods = {
    "PAWN":pawn_moves,
    "ROOK":rook_moves,
    "BISHOP":bishop_moves,
    "KNIGHT":knight_moves,
    "QUEEN":queen_moves,
    "KING":king_moves
}
