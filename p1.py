import random
from urllib.parse import ParseResult

NOT_FINISH = "NOT_FINISH"
FINISH_SUCCESS = "FINISH_SUCCESS"
FINISH_FAILURE = "FINISH_FAILURE"

#************************** options **************************
def options(sudoku_board : list, loc : tuple) -> list:
    num_options = [] #list of all the options of numbers
    num_excist = [] #list of all the excist numbers
    i, j = loc #location on board
    if sudoku_board[i][j] != -1: #if the location is not empty
        return num_options
    else:
        #checking the row, col and square
        num_excist = checking_the_row(sudoku_board, i, num_excist)
        num_excist = checking_the_col(sudoku_board, j, num_excist)
        num_excist = checking_the_square(i, j, num_excist)
        #connect all the numbers to one list
        num_options = connecting_list(num_excist, num_options)
        return num_options

#************************** checking_the_row **************************
def checking_the_row(sudoku_board : list, i : int,num_excist : list ) -> list:
        for s in sudoku_board[i]: #check every number on the same row
            if s != -1: #if the number is not empty (-1)
                num_excist.append(s) #add to the excist list
        return num_excist

#************************** checking_the_col **************************
def checking_the_col(sudoku_board: list, j : int, num_excist: list) -> list:
        for t in range(9): #check every number on the same col
            if sudoku_board[t][j] != -1:
                if sudoku_board[t][j] not in num_excist: #if the number alredy there no need to add again
                    num_excist.append(sudoku_board[t][j])
        return num_excist

#************************** checking_the_square **************************
def checking_the_square(i : int, j : int, num_excist : list) -> list:
    x = i // 3 * 3 #row
    y = j//3 * 3 + 3 #col
    num_excist = square(board, x, y, num_excist)
    return num_excist

# ************************** square **************************
def square(sudoku_board: list, x : int, y : int, num_excist : list) -> list:
    for t in range(x,(x+3)): #row
        for l in range((y-3),y): #col
            if sudoku_board[t][l] != -1: #not empty
                if sudoku_board[t][l] not in num_excist: #checking duplicates
                    num_excist.append(sudoku_board[t][l])
    return num_excist

# ************************** connecting_list **************************
def connecting_list(num_excist: list, num_options : list) -> list:
    for r in range(1, 10): #check every optional number
        if r not in num_excist: #if the number in num excist is not an option
            num_options.append(r)
    if num_options == []: #no options
        return None
    else:
        return num_options


# ************************** possible_digits **************************
def possible_digits(sudoku_board : list) -> list:
    possible_board = []
    # cheking options for all the locations on the board
    for i in range(9): # i = row
        row = []
        for j in range(9): # j = col
            lst = options(sudoku_board, (i,j))
            row.append(lst) #collect the option for each row
        possible_board.append(row)
    return possible_board


# ************************** one_stage **************************
def one_stage(sudoku_board : list, possible_board : list) -> tuple or str:
    min_location = ""
    updated = True
    while updated is True:
        updated = False
        for t in range(9):
            for r in range(9):
                if possible_board[t][r] != None:
                    if len(possible_board[t][r]) == 1:
                        #if there is one option it will add it to the board
                        sudoku_board[t][r] = possible_board[t][r][0]
                        updated = True
        if updated:
            possible_board = possible_digits(sudoku_board)
    min_location = checking_min_location(possible_board)
    if min_location:
        final = min_location, NOT_FINISH
        fill_board(sudoku_board, possible_board)
    if fail_row(sudoku_board, False) == False or fail_col(sudoku_board,False) == False or fail_square(sudoku_board,False):
        return FINISH_FAILURE
    else:
        return FINISH_SUCCESS

# ************************** checking_min_location **************************
def checking_min_location (possible_board : list) -> tuple:
    min_location = ""
    min_len_possible_lst = 10  # the max options is 9 so some list will be correct
    for i in range(9):
        for j in range(9):
            if possible_board[i][j] != None:
                if len(possible_board[i][j]) > 1:
                    if min_len_possible_lst > len(possible_board[i][j]):
                        min_len_possible_lst = len(possible_board[i][j])
                        min_location = (i,j)
    return min_location

#************************** fail_row **************************
def fail_row(sudoku_board : list, fail : bool) -> bool:
    num_excist = []
    for i in range(9):
        for s in sudoku_board[i]:
            if s != -1:
                if s in num_excist:
                    fail = True
                num_excist.append(s)
        num_excist = []
    fail = True


#************************** fail_col **************************
def fail_col(sudoku_board: list, fail : bool) -> list:
        num_excist = []
        for s in range(9):
            for t in range(9):
                if sudoku_board[t][s] != -1:
                    if sudoku_board[t][s] in num_excist:
                        fail = True
                    num_excist.append(sudoku_board[t][s])
            num_excist = []
        fail = False

# ************************** fail_square **************************
def fail_square(sudoku_board, fail : bool) -> bool:
    x = 0
    y = 0
    num_excist = []
    while (x + y) < 15:
        if x == 9:
            x = 0
            y += 3
        for s in range(x, (x + 3)):
            for t in range(y, (y + 3)):
                if sudoku_board[t][s] != -1:
                    if sudoku_board[t][s] in num_excist:
                        fail = True
                    num_excist.append(sudoku_board[t][s])
        num_excist = []
        x += 3
    fail = False


# ************************** fill_board **************************
def fill_board(sudoku_board : list, possible_board : list):
    min_location = checking_min_location(possible_board)
    t, r= min_location
    choosen_num = int(input(possible_board[t][r]))
    sudoku_board[t][r] = choosen_num
    possible_board[t][r] = []
    possible_board = possible_digits(sudoku_board)
    one_stage(sudoku_board, possible_board)


# ************************** create_random_board **************************
def create_random_board(sudoku_board : list) -> list:
    N = random.randrange(10, 21)
    # random num is the number of cells that will have a value
    row = []
    location_tuple = ()
    for i in range(9):
        for j in range(9):
            row.append(-1)
        sudoku_board.append(row)
        row = []

    options_of_loc = [(x, y) for x in range(9) for y in range(9)]
    size_of_options = 81

    for n in range(N):
        K = random.randrange(1, size_of_options)
        size_of_options -= 1
        chosen_tuple = options_of_loc[K]
        row, col = chosen_tuple
        options_of_loc.remove(chosen_tuple) #remove the tuple from the list
        size_of_options -= 1
        option_num = options(sudoku_board,chosen_tuple) #found the options fot the tuple
        random_value = random.randrange(1, len(option_num))
        sudoku_board[row][col] = option_num[random_value]
    return sudoku_board


# ************************** print_board **************************
def print_board(sudoku_board) -> list:
    between = "-" * 27
    for row in range(9):
        print(between, end="")
        print()
        for num in range(9):
            if sudoku_board[row][num] == -1:
                print("| ", end="")
            else:
                print("|",sudoku_board[row][num], end="")

        print("| ", end="")
        print()



def print_board_to_file(sudoku_board, filename: str) -> list:
    with open(filename, "a") as f:
        between = "-" * 27
        for row in range(9):
            f.write(between)
            f.write("\n")
            for num in range(9):
                if sudoku_board[row][num] == -1:
                    f.write("| ")
                else:
                    num_to_print = "|"
                    num_to_print += str(sudoku_board[row][num])
                    f.write(num_to_print)

            f.write("| ")
            f.write("\n")



example_board = [[5,3,-1,-1,7,-1,-1,-1,-1],
 [6,-1,-1,-1,-1,-1,1,-1,-1],
 [-1,-1,9,-1,-1,-1,-1,6,-1],
 [-1,-1,-1,-1,6,-1,-1,-1,3],
 [-1,-1,-1,8,-1,3,-1,-1,1],
 [-1,-1,-1,-1,-1,-1,-1,-1,-1],
 [-1,6,-1,-1,-1,-1,-1,-1,-1],
 [-1,-1,-1,-1,1,-1,-1,-1,-1],
 [-1,-1,-1,-1,8,-1,-1,-1,9]]

perfect_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]

impossible_board = [[5,1,6,8,4,9,7,3,2],
 [3,-1,7,6,-1,5,-1,-1,-1],
 [8,-1,9,7,-1,-1,-1,6,5],
 [1,3,5,-1,6,-1,9,-1,7],
 [4,7,2,5,9,1,-1,-1,6],
 [9,6,8,3,7,-1,-1,5,-1],
 [2,5,3,1,8,6,-1,7,4],
 [6,8,4,2,-1,7,5,-1,-1],
 [7,9,1,-1,5,-1,6,-1,8]]

bug_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,9],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]

interesting_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [-1,-1,-1,7,6,1,4,2,3],
 [-1,-1,-1,8,5,3,7,9,1],
 [-1,-1,-1,9,2,4,8,5,6],
 [-1,-1,-1,-1,3,7,2,8,4],
 [-1,-1,-1,-1,1,9,6,3,5],
 [-1,-1,-1,-1,8,6,1,7,9]]
empty_board = []

board = example_board
possible = possible_digits(board)
found_None = False
for i in possible:
    if None in i:
        found_None = True
if found_None:
    f = open("final_sudoko.txt", 'w')
    f.write("Board 1 is not legit!\n")
    f.close()
else:
    res = one_stage(board, possible)
    if res == FINISH_SUCCESS:
        f = open("final_sudoko.txt", 'w')
        f.write("Here is the solved board 1\n")
        f.close()
        print_board_to_file(board, "final_sudoko.txt")
    elif res == FINISH_FAILURE:
        f = open("final_sudoko.txt", 'w')
        f.write("Board 1 is unsolvable\n")
        f.close()
    else:
        f = open("final_sudoko.txt", 'w')
        f.write("Board 1 is not legit!\n")
        f.close()


board = perfect_board
possible = (possible_digits(board))
found_None = False
for i in possible:
    if None in i:
        found_None = True
if found_None:
    f = open("final_sudoko.txt", 'a')
    f.write("\n")
    f.write("Board 2 is not legit!\n")
    f.close()
else:
    res = one_stage(board, possible)
    if res == FINISH_SUCCESS:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Here is the solved board 2\n")
        f.close()
        print_board_to_file(board, "final_sudoko.txt")
    elif res == FINISH_FAILURE:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Board 2 is unsolvable\n")
        f.close()
    else:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Board 2 is not legit!\n")
        f.close()

board = impossible_board
possible = possible_digits(board)
found_None = False
for i in possible:
    if None in i:
        found_None = True
if found_None:
    f = open("final_sudoko.txt", 'a')
    f.write("\n")
    f.write("Board 3 is not legit!\n")
    f.close()
else:
    res = one_stage(board, possible)
    if res == FINISH_SUCCESS:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Here is the solved board 3\n")
        f.close()
        print_board_to_file(board, "final_sudoko.txt")
    elif None in possible:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Board 3 is not legit!\n")
        f.close()
    else:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Board 3 is unsolvable\n")
        f.close()

board = bug_board
final = ""
if fail_row(board,False) or fail_col(board, False) or fail_square(board,False):
    final = FINISH_FAILURE
if  final == FINISH_FAILURE :
    f = open("final_sudoko.txt", 'a')
    f.write("\n")
    f.write("Board 4 is not legit!\n")
    f.close()
else:
    res = one_stage(board, possible)
    if res == FINISH_SUCCESS:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Here is the solved board 4\n")
        f.close()
        print_board_to_file(board, "final_sudoko.txt")
    elif None in possible:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Board 4 is not legit!\n")
        f.close()
    else:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Board 4 is unsolvable\n")
        f.close()


board = interesting_board
possible = possible_digits(board)
found_None = False
for i in possible:
    if None in i:
        found_None = True
if found_None:
    f = open("final_sudoko.txt", 'a')
    f.write("\n")
    f.write("Board 5 is not legit!\n")
    f.close()
else:
    res = one_stage(board, possible)
    if res == FINISH_SUCCESS:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Here is the solved board 5\n")
        f.close()
        print_board_to_file(board, "final_sudoko.txt")
    elif res == FINISH_FAILURE:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Board 5 is unsolvable\n")
        f.close()
    else:
        f = open("final_sudoko.txt", 'a')
        f.write("\n")
        f.write("Board 5 is not legit!\n")
        f.close()

board = empty_board
res = create_random_board(board)
f = open("final_sudoko.txt", 'a')
f.write("\n")
f.write("Board 6 is unsolvable\n")
f.close()
print_board_to_file(res, "final_sudoko.txt")

