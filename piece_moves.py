import numpy

def pawn_moves():
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A PAWN CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    moves = []
    captures = []
    moves.append(numpy.array([0,1]))
    captures.append(numpy.array([1,1]))
    captures.append(numpy.array([-1,1]))
    return {"moves":moves, "captures":captures}

def rook_moves():
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A ROOK CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    moves = []
    captures = []
    for i in range(0,8):
        moves.append(numpy.array([i,0]))
        moves.append(numpy.array([-i,0]))
        moves.append(numpy.array([0,i]))
        moves.append(numpy.array([0,-i]))
        captures.append(numpy.array([i,0]))
        captures.append(numpy.array([-i,0]))
        captures.append(numpy.array([0,i]))
        captures.append(numpy.array([0,-i]))
    return {"moves":moves, "captures":captures}

def bishop_moves():
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A BISHOP CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    moves = []
    captures = []
    for i in range(0,8):
        moves.append(numpy.array([i,i]))
        moves.append(numpy.array([-i,i]))
        moves.append(numpy.array([i,-i]))
        moves.append(numpy.array([-i,-i]))
        captures.append(numpy.array([i,i]))
        captures.append(numpy.array([-i,i]))
        captures.append(numpy.array([i,-i]))
        captures.append(numpy.array([-i,-i]))
    return {"moves":moves, "captures":captures}

def knight_moves():
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A KNIGHT CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    moves = [numpy.array([1,2]),numpy.array([2,1]),numpy.array([-1,2]),numpy.array([-2,1]),numpy.array([1,-2]),numpy.array([2,-1]),numpy.array([-1,-2]),numpy.array([-2,-1])]
    captures = numpy.array([[1,2],[2,1],[-1,2],[-2,1],[1,-2],[2,-1],[-1,-2],[-2,-1]])
    return {"moves":moves, "captures":captures}

def queen_moves():
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A QUEEN CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    #BISHOP + ROOK
    moves = []
    captures = []
    return {"moves":moves, "captures":captures}

def king_moves():
    #GENERATE AND RETURN VECTORS THAT REPRESENT WHERE A KING CAN MOVE AND OR CAPTURE RELATIVE TO ITS CURRENT POSITION
    #EVERY COMBINATION OF 0,1, AND -1 EXCEPT 0,0
    moves = []
    captures = []
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
