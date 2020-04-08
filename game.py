import os
import random
import copy

#rule -렌주룰
#흑, 백 중 흑이 먼저 시작
#흑만 33, 44, 장목 금지
#금지된 수를 놓으면서 5가 만들어지는 것은 승리
#백은 장목 허용
from pprint import pprint

import sys

SIZE = 3

class Board:
    b = [[0 for x in range(SIZE)] for y in range(SIZE)] #board
    # b = [
    #     [-1, 1, 0],
    #     [0, 0, 0],
    #     [0, 1, 0]
    # ]
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
                    Board.bs[i][j] = True
                else:
                    Board.bs[i][j] = False
                    # a = Board.is_acceptable(c(i,j),1)
                    # b = Board.is_acceptable(c(i,j),-1)
                    # if a and b:
                    #     Board.bs[i][j] = True
                    # elif a:
                    #     Board.bs[i][j] = 1
                    # elif b:
                    #     Board.bs[i][j] = -1
                    # else:
                    #     assert True

    @staticmethod
    def get_allowable_pos_board():
        return Board.bs

    @staticmethod
    def get_board():
        return Board.b

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
            if len[0] + len[1] - 1 == 3:
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

class node:
    def __init__(self, board):
        self.board = board
        self.children = list()

    def input(self, c, player_turn):
        (x, y) = c.tuplize()
        self.board[x][y] = player_turn

    def goal_test_pos(self, pos):
        (x, y) = pos.tuplize()
        player = self.board[x][y]
        # if player == 0:
        #     return False #돌이 있는 곳만 체크
        for d in (c(1,0), c(0,1), c(1,1), c(-1,1)):
            #print(f"방향:{d}")
            len = [1, 1]
            for i, dir in enumerate((d, -d)):
                next = pos + dir
                while True:
                    (x, y) = next.tuplize()
                    if (0 <= x < SIZE) and (0 <= y < SIZE) and self.board[x][y] == player:
                        #print(f"\t({x},{y}) 연결 확인, len[{i}] = {len[i]}")
                        len[i] += 1
                        next = next + dir
                    else:
                        #print(f"\t({x},{y}) 끊어짐 확인, len[{i}] = {len[i]}")
                        break
            #print(f"방향:{d} 연결된 길이:{len[0]+len[1]-1}")
            if len[0] + len[1] - 1 == 3:
                return player
        return False

    def print_board(self):
        print(' ',end='')
        print(" ".join(map(num_to_index, range(SIZE))))
        for i in range(SIZE):
            print(num_to_index(i), end='')
            for j in range(SIZE):
                print(draw_cell(self.board[i][j]), end=' ')
            print()
        print()  # empty line

    def get_board(self):
        return self.board
    #def is_acceptable

def minimax_descision(allowable_board, player_turn): #returns best action c(n,m) for player(player_turn)
    argmax = c(0,0)
    INF = 987654321
    max_t = -INF
    is_available_pos = False
    for i in range(SIZE):
        for j in range(SIZE):
            if allowable_board[i][j] == True or allowable_board[i][j] == player_turn:
                is_available_pos = True
                child = node(copy.deepcopy(Board.get_board()))
                child.input(c(i,j), player_turn)
                min_val = min_value(child, c(i,j), -INF, INF, player_turn, 0)
                if min_val > max_t:
                    max_t = min_val
                    argmax = c(i,j)
    if not is_available_pos:
        print("GAME END! There is no available position.")
        print("press any key to quit..")
        input()
        sys.exit()
    return argmax

    #for 가능한 모든 액션에 대해
    #   MIN_VALUE실행
    #   MIN_VALUE가 MAX보다 크면 MAX, ARGMAX 갱신
    #리턴 ARGMAX

def max_value(state, last_input, a, b, player_turn, depth): #returns utility 값 #가장 큰 min을 찾음 (내가 둘 차례)
    # print(f"Searching.. max_value(state, last_input: {last_input}, alpha: {a}, beta: {b}, depth: {depth})")
    # state.print_board()
    #assert state.goal_test_pos(last_input) == False or state.goal_test_pos(last_input) == -player_turn
    if state.goal_test_pos(last_input) != False: #이미 승리 상태 (마지막에 둔 수(상대의 수)가 승리조건달성)
        #print(f"***********************Player {player_turn} win***********************")
        return -9999 #플레이어 턴?
    INF = 987654321
    v = -INF
    is_available_pos = False
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board[i][j] == 0: #acceptable조건은 나중에 확인
                is_available_pos = True
                child = node(copy.deepcopy(state.get_board())) #copy 필요?
                child.input(c(i,j),player_turn)
                state.children.append(child)
                v = max(v, min_value(child,c(i,j),a,b,player_turn,depth+1))
    if not is_available_pos: #Terminal state 체크: 화면이 꽉 찼는지
        #raise Exception
        #print(f"***********************Draw***********************")
        return 0
    return v
    #만약 보드가 terminal state 이면 utility 리턴 (승리 1 패배 -1)
    #v = -INF
    #for 가능한 액션에 대해
    #   v = max(v, MIN_VALUE(board에 액션 수행한 보드,a,b))
    #   if v >= b then return v #b = beta = MIN 경로에서 현재까지 발견한 최선의 선택 (값이 가장 작은 선택)
    #   a = max(a,v)
    #return v

def min_value(state, last_input, a, b, player_turn, depth): #returns utility 값 #가장 작은 max를 찾음 (상대가 둘 차례)
    # print(f"Searching.. min_value(state, last_input: {last_input}, alpha: {a}, beta: {b}, depth: {depth})")
    # state.print_board()
    #assert state.goal_test_pos(last_input) == False or state.goal_test_pos(last_input) == player_turn
    if state.goal_test_pos(last_input) != False:
        #print(f"***********************Player {player_turn} win***********************")
        return 9999 #플레이어 턴?
    INF = 987654321
    v = INF
    is_available_pos = False
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board[i][j] == 0:
                is_available_pos = True
                child = node(copy.deepcopy(state.get_board()))
                child.input(c(i,j),-player_turn)
                state.children.append(child)
                v = min(v, max_value(child,c(i,j),a,b,player_turn,depth+1))
    if not is_available_pos:
        #raise Exception
        return 0
    return v

    #만약 보드가 terminal state이면 utility 리턴 (승리 1 패배 -1)
    #v = -INF
    #for 가능한 액션에 대해
    #   v = min(v, MAX_VALUE(board에 액션 수행한 보드,a,b))
    #   if v <= a then return v #a = alpha = MAX 경로에서 현재까지 발견한 최선의 선택 (값이 가장 큰 선택)
    #   b = min(b,v)
    #return v

def ai(allowable_board, player_turn):
    return minimax_descision(allowable_board, player_turn)

TIME_LIMIT = 10#int(input("set AI's turn time limit (second): "))
player_turn = 1#1 for black(play  first), -1 for white
# while True:
#     you = int(input("set player to play first (1 = you, -1 = AI): "))
#     if you in (-1,1):
#         break
#     print("Invalid input. Try again.")

# n = node([
#     [1, -1, 1],
#     [-1, 1, -1],
#     [1, -1, 0]
# ])
# print(n.print_board())
# print(n.goal_test_pos(c(2,0)))
# raise Exception

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
        # while not Board.is_acceptable(next_move, player_turn):
        #     print("Invalid user movement. Violated 33 or 44 rule. Only 43 is permitted. Try another.")
        #     next_move = get_input()
        Board.update_board(next_move, player_turn)
        player_turn = -player_turn
    elif player_turn == -1:
        Board.update_allowable_pos_board()
        ab = Board.get_allowable_pos_board()
        next_move = ai(ab, player_turn)
        while not Board.is_empty(next_move):
            print(f"{next_move} Invalid computer movement. Stone already exists. Retrying..")
            next_move = ai(ab, player_turn)
        # while not Board.is_acceptable(next_move, player_turn):
        #     print(f"{next_move} Invalid computer movement. Unacceptable. Retrying..")
        #     next_move = ai(ab, player_turn)
        Board.update_board(next_move, player_turn)
        player_turn = -player_turn
        print(f"Computer move: {next_move}")