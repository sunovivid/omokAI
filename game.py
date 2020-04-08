import os
import random

#rule -렌주룰
#흑, 백 중 흑이 먼저 시작
#흑만 33, 44, 장목 금지
#금지된 수를 놓으면서 5가 만들어지는 것은 승리
#백은 장목 허용

SIZE = 19

class Board:
    b = [[0 for x in range(SIZE)] for y in range(SIZE)] #board
    # b = [
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, -1, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 0, 1, 0, 1, 0, 0],
    #     [0, 0, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, -1, 0, 0, 0]
    # ]

    bs = [[0 for z in range(SIZE)] for w in range(SIZE)] #board for allowable position

    @staticmethod
    def input(c, player_turn):
        (x, y) = c.tuplize()
        Board.b[x][y] = player_turn

    @staticmethod
    def is_move_inside_board(c):
        (x, y) = c.tuplize()
        if x >= SIZE or y >= SIZE or x < 0 or y < 0:
            return False
        return True

    @staticmethod
    def check(c):
        assert Board.is_move_inside_board(c)
        (x, y) = c.tuplize()
        return Board.b[x][y]

    @staticmethod
    def update_board(c, player_turn):
        if Board.check(c) == 0:
            Board.input(c, player_turn)
        else:
            assert True

    @staticmethod
    def is_empty(c):
        if Board.check(c) == 0:
            return True
        return False

    @staticmethod
    def is_acceptable(move, player_turn):
        # 3-3
        # 좌우/상하/대각1/대각2로 열린4체크
        # 두 개 이상이 열린 4면 return False
        Board.input(move, player_turn)
        len_max_dir = [0, 0, 0, 0]
        #print(f"now: {move}")
        for i, direction in enumerate( ( c(0, 1), c(1, 0), c(1, 1), c(1, -1) ) ):# [ -, |, \, /]
            check_spots = [move, move]
            len = [1, 1]
            is_blocked = False
            #print(f"direction: {direction}")
            for j, toward in enumerate((direction, -direction)):
                #print(f"\ttoward: {toward}")
                len[j] = 1
                while True:
                    check_spots[j] = check_spots[j] + toward
                    if not Board.is_move_inside_board(check_spots[j]) or Board.check(check_spots[j]) == -player_turn:
                        #print(f"\t\tblocked: {check_spots[j]}, len:{len[j]}")
                        is_blocked = True
                        break
                    elif Board.check(check_spots[j]) == 0:
                        #print(f"\t\tcheck spot found: {check_spots[j]}, len:{len[j]}")
                        break
                    else:
                        #print(f"\t\tcheck spot++: {check_spots[j]}, len:{len[j]}")
                        len[j] += 1
            len_max = 0
            for j, toward in enumerate((direction, -direction)):
                check_spot = check_spots[j]
                if not Board.is_move_inside_board(check_spot): #후보 자리 자체가 판 밖에 있는 경우 -> 한쪽이 막혀 있어서 열린n 불가능
                    break
                if Board.check(check_spot) == -player_turn:
                    print(f"check_spot {check_spot} is already placed")
                    break
                is_blocked = False
                temp = check_spot
                Board.input(temp,player_turn)
                len_more = 1
                #print(f"\tcheck spot: {temp}, toward: {toward}")
                while True:
                    check_spot = check_spot + toward
                    if not Board.is_move_inside_board(check_spot) or Board.check(check_spot) == -player_turn:
                        #print(f"\t\tblocked: {check_spots[j]}, len_more: {len_more}")
                        is_blocked = True
                        Board.input(temp, 0)
                        break
                    elif Board.check(check_spot) == 0:
                        #print(f"\t\tend of line: {check_spots[j]}, len_more: {len_more}")
                        Board.input(temp,0)
                        break
                    else:
                        #print(f"\t\tcheck spot++: {check_spots[j]}, len_more: {len_more}")
                        len_more += 1
                if is_blocked:
                    Board.input(temp, 0)
                    #print(f"\tblocked, skip search toward: {toward}")
                    continue
                len_max = max(len_max, len[0] + len[1] - 1 + len_more)
                Board.input(temp,0)
            len_max_dir[i] = len_max - 1 #방향별 열린 'n'에 대해 'n-1' 저장 (열린4 -> 3)
            # 오른쪽 넣을 수 있는 공간 확인, 연속된 개수 저장
            # 왼쪽 넣을 수 있는 공간 확인, 연속된 개수 저장
            # 오른쪽 열린 k 측정 (오른쪽에 넣었다 가정하고 왼쪽 연속된 개수 + 오른쪽 연속된 개수 + 더 가보기)
            # 왼쪽도 같은 방법으로 l측정
            # n = k + l - 1
        Board.input(move, 0)
        print(len_max_dir, "# [-, |, \, /]")

        line = [0,0,0,0,0,0,0,0]

        for i in len_max_dir:#일반룰
            line[i] += 1
        if line[3] >= 2:
            return False
        return True

        # if player_turn == 1: 렌주룰
        #     for i in len_max_dir:
        #         line[i] += 1
        #     if line[4] >= 2:
        #         return False #44
        #     elif line[4] == 1 and line[3] >= 1:
        #         return True #34
        #     elif line[3] >= 2:
        #         return False #33
        # return True

    @staticmethod
    def update_allowable_pos_board(): #False is not allowable for both. 1/-1 is allowable for black/white respectively. True is allowable for both.
        for i in range(SIZE):
            for j in range(SIZE):
                if Board.is_empty(c(i,j)):
                    Board.bs[i][j] = False
                else:
                    a = Board.is_acceptable(c(i,j),1)
                    b = Board.is_acceptable(c(i,j),-1)
                    if a and b:
                        Board.bs[i][j] = True
                    elif a:
                        Board.bs[i][j] = 1
                    elif b:
                        Board.bs[i][j] = -1
                    else:
                        assert True

    @staticmethod
    def get_allowable_pos_board():
        return Board.bs

    @staticmethod
    def goal_test_pos(pos):
        player = Board.check(pos)
        if player == 0:
            return False #돌이 있는 곳만 체크
        for d in (c(1,0), c(0,1), c(1,1), c(-1,1)):
            len = [1, 1]
            for i, dir in enumerate((d, -d)):
                next = pos + dir
                while True:
                    if Board.is_move_inside_board(next) and Board.check(next) == player:
                        len[i] += 1
                        next = next + dir
                    else:
                        break
            if len[0] + len[1] - 1 == 5:
                return player
        return False



class c:
    # def __init__(self, tuple):
    #     self.x = tuple[0]
    #     self.y = tuple[1]

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self, coordinate):
        return c(self.x + coordinate.x, self.y + coordinate.y)

    def __str__(self):
        return f"({self.x},{self.y})"

    def __neg__(self):
        return c(-self.x,-self.y)

    def tuplize(self):
        return (self.x, self.y)

def num_to_index(number):
    if number >= 10:
        return chr(ord('A') + number - 10)
    else:
        return str(number)

def index_to_num(index):
    try:
        return int(index)
    except:
        return ord(index) - ord('A') + 10

def cls():
    pass
    #print("\n"*10)
    #os.system('cls' if os.name=='nt' else 'clear')

def draw_cell(elem):
    if elem == 0:
        return "┼"
    elif elem == -1:
        return "●"
    else:
        return "○"

def print_board():
    cls()
    print(' ',end='')
    print(" ".join(map(num_to_index,range(SIZE))))
    for i in range(SIZE):
        print(num_to_index(i), end='')
        for j in range(SIZE):
            print( draw_cell(Board.check(c(i,j))), end = ' ')
        print()
    print() #empty line

def get_input():
    player_move = input("Enter your move: ")
    x, y = index_to_num(player_move[0]), index_to_num(player_move[1])
    return c(x, y)

def ai(allowable_board):
    return c(random.randrange(0,SIZE), random.randrange(0,SIZE))

def get_winner():
    pass

TIME_LIMIT = 10#int(input("set AI's turn time limit (second): "))
player_turn = 1#1 for black(play  first), -1 for white
while True:
    you = int(input("set player to play first (1 = you, -1 = AI): "))
    if you in (-1,1):
        break
    print("Invalid input. Try again.")
next_move = None
while True:
    print_board()
    if next_move is not None:
        goal_test = Board.goal_test_pos(next_move)
        if goal_test != False:
            print(f"{('Black','White')[(goal_test+1)//2]} win!")
            break
    if player_turn == 1:
        next_move = get_input()
        while not Board.is_move_inside_board(next_move):
            print("Invalid user movement. Place the stone inside Board. Try another.")
            next_move = get_input()
        while not Board.is_empty(next_move):
            print("Invalid user movement. There is a stone already. Try another.")
            next_move = get_input()
        while not Board.is_acceptable(next_move, player_turn):
            print("Invalid user movement. Violated 33 or 44 rule. Only 43 is permitted. Try another.")
            next_move = get_input()
        Board.update_board(next_move, player_turn)
        player_turn = -player_turn
    elif player_turn == -1:
        #Board.update_allowable_pos_board()
        allowable_board = Board.get_allowable_pos_board()
        next_move = ai(allowable_board)
        while not Board.is_empty(next_move):
            print(f"{next_move} Invalid computer movement. Stone already exists. Retrying..")
            next_move = ai(allowable_board)
        while not Board.is_acceptable(next_move, player_turn):
            print(f"{next_move} Invalid computer movement. Unacceptable. Retrying..")
            next_move = ai(allowable_board)
        Board.update_board(next_move, player_turn)
        player_turn = -player_turn