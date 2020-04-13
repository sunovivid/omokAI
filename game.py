import os
import random
import copy
import asyncio

#rule -렌주룰
#흑, 백 중 흑이 먼저 시작
#흑만 33, 44, 장목 금지
#금지된 수를 놓으면서 5가 만들어지는 것은 승리
#백은 장목 허용
from pip._vendor.html5lib._utils import memoize
from pprint import pprint

import sys

SIZE = 11
LENGTH = 5
TIMEOUT = 'x' #Constant

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

    @staticmethod
    def create_board_from_txt(txt, reverse_value=1):
        if txt[0] == '\n':
            txt = txt[1:]
        i = 0
        for k, line in enumerate(txt.split('\n')):
            if k == 0:
                continue
            j = 0
            for char in line[1:].split(' '):
                if char == '┼':
                    Board.b[i][j] = 0
                elif char == '●':
                    Board.b[i][j] = 1 * reverse_value
                elif char == '○':
                    Board.b[i][j] = -1 * reverse_value
                j += 1
            i += 1

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
        # print(f"is_acceptable({move}, player_turn: {player_turn})")
        for i, direction in enumerate( ( c(0, 1), c(1, 0), c(1, 1), c(1, -1) ) ):# [ -, |, \, /]
            check_spots = [move, move]
            len = [1, 1]
            is_blocked = False
            # print(f"\tdirection: {direction}")
            for j, toward in enumerate((direction, -direction)):
                # print(f"\t\ttoward: {toward}")
                len[j] = 1
                while True:
                    check_spots[j] = check_spots[j] + toward
                    if not Board.is_move_inside_board(check_spots[j]) or Board.check(check_spots[j]) == -player_turn:
                        # print(f"\t\t\tblocked: {check_spots[j]}, len:{len[j]}, Board.check:"
                        #       f"{Board.check(check_spots[j]) if Board.is_move_inside_board(check_spots[j]) else 'OUT_OF_BOARD'}")
                        is_blocked = True
                        break
                    elif Board.check(check_spots[j]) == 0:
                        # print(f"\t\t\tcheck spot found: {check_spots[j]}, len:{len[j]}")
                        break
                    else:
                        # print(f"\t\t\tcheck spot++: {check_spots[j]}, len:{len[j]}")
                        len[j] += 1
            len_max = 0
            if is_blocked:
                continue
            for j, toward in enumerate((direction, -direction)):
                check_spot = check_spots[j]
                assert Board.is_move_inside_board(check_spot)
                # if not Board.is_move_inside_board(check_spot): #후보 자리 자체가 판 밖에 있는 경우 -> 한쪽이 막혀 있어서 열린n 불가능
                #     break
                assert Board.check(check_spot) != -player_turn
                # if Board.check(check_spot) == -player_turn:
                #     print(f"check_spot {check_spot} is already placed")
                #     break
                temp = check_spot
                assert Board.check(temp) == 0
                Board.input(temp, player_turn)
                len_more = 1
                # print(f"\t\tcheck spot: {temp}, toward: {toward}")
                while True:
                    check_spot = check_spot + toward
                    if (not Board.is_move_inside_board(check_spot)) or Board.check(check_spot) == -player_turn:
                        # print(f"\t\t\tblocked: {check_spots[j]}, len_more: {len_more}")
                        Board.input(temp, 0)
                        break
                    elif Board.check(check_spot) == 0:
                        # print(f"\t\t\tend of line: {check_spots[j]}, len_more: {len_more}")
                        Board.input(temp,0)
                        break
                    else:
                        # print(f"\t\t\tcheck spot++: {check_spots[j]}, len_more: {len_more}")
                        len_more += 1
                len_max = max(len_max, len[0] + len[1] - 1 + len_more)
                # print(f"\t\tlen: {len[0] + len[1] - 1 + len_more}, len_max: {len_max}")
                Board.input(temp,0)
            len_max_dir[i] = len_max - 1 #방향별 열린 'n'에 대해 'n-1' 저장 (열린4 -> 3)
            # 오른쪽 넣을 수 있는 공간 확인, 연속된 개수 저장
            # 왼쪽 넣을 수 있는 공간 확인, 연속된 개수 저장
            # 오른쪽 열린 k 측정 (오른쪽에 넣었다 가정하고 왼쪽 연속된 개수 + 오른쪽 연속된 개수 + 더 가보기)
            # 왼쪽도 같은 방법으로 l측정
            # n = k + l - 1
        Board.input(move, 0)
        # print(len_max_dir, "# [-, |, \, /]")

        len_count = [0,0,0,0,0,0,0,0]

        for i in len_max_dir:#일반룰
            len_count[i] += 1

        if len_count[3] >= 2:
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
                    a = Board.is_acceptable(c(i,j),1)
                    b = Board.is_acceptable(c(i,j),-1)
                    if a and b:
                        Board.bs[i][j] = True
                    elif a:
                        Board.bs[i][j] = 1
                    elif b:
                        Board.bs[i][j] = -1
                else:
                    Board.bs[i][j] = False


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
            if len[0] + len[1] - 1 == LENGTH:
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
    elif elem == 1:
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

def player_index(player_turn): #return player index: black(-1) => 0, white(0) => 1
    return (player_turn + 1) // 2

class Node:
    def __init__(self, board):
        self.board = board
        self.children = list()

    def input(self, c, player_turn):
        (x, y) = c.tuplize()
        self.board[x][y] = player_turn

    def is_move_inside_board(self,c):
        (x, y) = c.tuplize()
        if x >= SIZE or y >= SIZE or x < 0 or y < 0:
            return False
        return True

    def check(self,c):
        assert self.is_move_inside_board(c)
        (x, y) = c.tuplize()
        return self.board[x][y]

    def update_board(self, c, player_turn):
        if self.check(c) == 0:
            self.input(c, player_turn)
        else:
            assert True

    def is_empty(self, c):
        if self.check(c) == 0:
            return True
        return False

    def goal_test_pos(self, pos):
        player = self.check(pos)
        assert player != 0
        for d in (c(1,0), c(0,1), c(1,1), c(-1,1)):
            #print(f"방향:{d}")
            len = [1, 1]
            for i, dir in enumerate((d, -d)):
                next = pos + dir
                while True:
                    if self.is_move_inside_board(next) and self.check(next) == player:
                        #print(f"\t({x},{y}) 연결 확인, len[{i}] = {len[i]}")
                        len[i] += 1
                        next = next + dir
                    else:
                        #print(f"\t({x},{y}) 끊어짐 확인, len[{i}] = {len[i]}")
                        break
            #print(f"방향:{d} 연결된 길이:{len[0]+len[1]-1}")
            if len[0] + len[1] - 1 == LENGTH:
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

    @memoize
    def get_evaluation_function(self, player_now):
        #print("get_evaluation_function start")
        #새로 둔 수가 33체커를 이용해 인접 3,4,5를 만들면 +
        #인접한 블록의 상대방 3,4,5를 막으면 +

        #내가 공격할 수 있는 공간이 상대방이 공격할 수 있는 공간보다 많을때
        #내가 공격할 수 있는 공간 수 * 각 상황별 가중치 - 상대방이 공격할 수 있는 공간 수 * 각 상황별 가중치
        #초기에는 내가 이길 가능성이 높고 상대방이 이길 가능성이 적은 경우를 고르고
        #후반에는 거의 정답에 근사해야 한다. (이기는 것이 확실해질수록 100%에 수렴)
        #'양쪽이 막혀버린 수'는 더 이상 고려할 필요 없음
        #'한쪽이 막힌 수'는 보통 가치가 없으나 3이상부터는 의미있음. 두 턴 안에 안막으면 이기는 게 가능.
        #3 (열린 4)를 만드는 것은 무조건 좋음

        #공격하면 이기는 상황 (열린 4 만들어지는 경우) -> 공격
        #아닐경우: 무조건 막아야 하는 상황 -> 무조건 막아야 함.
        #아닐경우: 공격하면 상대가 무조건 막아야 하는 상황 -> 일단 공격하고 볼 수도 있고, 킵할 수도 있음. AI는 대체로 공격. 여러 개면 그 중 방어하면서 공격하는 것으로.

        #eval_func : utility의 추정값. 어느 쪽이 이길 것 같은지.

        # 5 만들기 > 5 막기 > 열린 4 만들기 >= 열린 4 막기 > 열린 3 만들기 >= 열린 3 막기 >= 닫힌 4 막기
        #위와 같이 행동하도록 state의 eval func의 구현하려면? (상태,턴) => eval_func
        #계산법: 현재 상태에서 나의 점수 - 상대 점수
        #(내 열린 5, ) => 승리 INF
        #(내 열린 4, 내 턴) => 승리 1600
        #(내 열린 4, 상대 턴) => 승리
        #(내 열린 3/ 닫힌 4, 내 턴) => 최고 점수 (사실상 승리) 800
        #(내 열린 3/ 닫힌 4, 상대 턴) => 좋은 점수 (상대가 열린 4가 아닌 이상 무조건 막아야 함)
        #(상대 열린 3/ 닫힌 4, 내 턴) => 나쁜 점수 (내가 열린 4가 아닌 이상 무조건 막아야 함)
        #(상대 열린 3/ 닫힌 4, 상대 턴) => 최악 점수 (사실상 패배) -8
        #(상대 열린 4, 상대 턴) => 패배 -1600
        #(상대 열린 5, ) => 패배 -INF

        #점수계산법
        #모든 스팟 체크
        # if goal_test() => INF
        # elif '44' => INF/2
        # elif '43' => INF/4
        # elif '33' => -INF/8
        # elif '열린4' => INF/8

        # elif '3' => 개수당 +16 ┼○○○┼ ┼○○┼○┼
        # elif 반닫힌'3' => 개수당 +8 ●○○○┼ ●○○┼○┼
        # elif '2' => 개수당 +4 ┼○○┼ ┼○┼○┼
        # elif 반닫힌'2' => 개수당 +2 ●○○┼ ●○┼○┼
        # elif '1' => 개수당 +1 ┼○┼
        # elif 반닫힌 '1' => 개수당 +0.5 ●○┼

        score = [0, 0]
        INF = 87654321

        for x in range(SIZE):
            for y in range(SIZE):
                # print(f"c({x},{y})탐색중..")
                move = c(x, y)
                #인접한 노드가 있거나 이미 있는 노드에 대하여
                if self.check(move):
                    player_pos = self.check(move)
                    len_max_dir = [0, 0, 0, 0]
                    block = [0, 0, 0, 0]
                    # print(f"now: {move}")
                    for i, direction in enumerate((c(0, 1), c(1, 0), c(1, 1), c(1, -1))):  # [ -, |, \, /]
                        check_spots = [move, move]
                        len = [1, 1]
                        len_block = [0,0]
                        len_block_bidirectional = 1
                        # print(f"direction: {direction}")
                        for j, toward in enumerate((direction, -direction)):
                            # print(f"\ttoward: {toward}")
                            len[j] = 1
                            while True:
                                check_spots[j] = check_spots[j] + toward
                                if not self.is_move_inside_board(check_spots[j]) or self.check(check_spots[j]) == -player_pos:
                                    block[i] += 1
                                    check_spots[j] = False
                                    len_block[j] = len[j]
                                    # print(f"\t\tblocked: {check_spots[j]}, len[{j}]:{len[j]}, len_block[{j}]:{len_block[j]}")
                                    break
                                elif self.check(check_spots[j]) == 0:
                                    temp_check_spot = check_spots[j]
                                    while True:
                                        if len_block_bidirectional >= 5 or not self.is_move_inside_board(temp_check_spot) or self.check(temp_check_spot) == -player_pos:
                                            break
                                        len_block[j] += 1
                                        len_block_bidirectional += 1
                                        # print(f"\t\tcheck more: {temp_check_spot}, len_block_bidirectional:{len_block_bidirectional}, len_block[{j}]:{len_block[j]}")
                                        temp_check_spot = temp_check_spot + toward
                                    # print(f"\t\tcheck spot found: {check_spots[j]}, len:{len[j]}")
                                    #안막혀있으면 => 막혀 있는 데까지 가보기. 총 가본 거리가 5를 넘어가면 중단(오목이 satisfiable)
                                    #양쪽 len_block이 5보다 작으면 +0, check_spot 고려할 필요 없음.
                                    break
                                else:
                                    # print(f"\t\tcheck spot++: {check_spots[j]}, len:{len[j]}, len_block_bidirectional:{len_block_bidirectional}")
                                    len[j] += 1
                                    len_block_bidirectional += 1
                        # print(len_block[0],len_block[1])
                        if len[0] + len[1] - 1 == 5: #goal_test
                            # print(f"goal_found({move})")
                            return INF
                        elif len_block_bidirectional < 5: #가능한 공간이 5보다 작은 경우
                            # print(f"************OMOK IS UNSATISFIABLE IN THIS MOVE: {move}, DIRECTION: {direction}************")
                            continue

                        len_max = 0
                        for j, toward in enumerate((direction, -direction)):
                            #check_spot에서 toward쪽으로 가보며 점검
                            #block[j] 기록 0 = 막혀 있지 않음, 1 = 한쪽 막힘, 2 = 양쪽 막힘
                            #len_max_dir[i], block[i] 기록해 두 리스트 조합해서 판단
                            check_spot = check_spots[j]
                            if check_spot == False:
                                continue
                            temp = check_spot
                            assert self.check(temp) == 0
                            self.input(temp, player_pos)
                            len_more = 1
                            # print(f"\tcheck spot: {temp}, toward: {toward}")
                            while True:
                                check_spot = check_spot + toward
                                if (not self.is_move_inside_board(check_spot)) or self.check(check_spot) == -player_pos:
                                    # print(f"\t\tblocked: {check_spots[j]}, len_more: {len_more}")
                                    # block[j] += 1
                                    self.input(temp, 0)
                                    break
                                elif self.check(check_spot) == 0:
                                    #block될 때까지 가보기
                                    #지금까지 발견한 길이 + 가본 길이가 5보다 작을 경우 stop
                                    # print(f"\t\tend of line: {check_spot}, len_more: {len_more}")
                                    self.input(temp, 0)
                                    break
                                else:
                                    # print(f"\t\tcheck spot++: {check_spot}, len_more: {len_more}")
                                    len_more += 1
                            # print(f"\t\tlen[0]={len[0]}, len[1]={len[1]}")
                            len_max = max(len_max, len[0] + len[1] - 1 + len_more)
                            self.input(temp, 0)
                        len_max_dir[i] = len_max - 1  # 방향별 열린 'n'에 대해 'n-1' 저장 (열린4 -> 3)
                        # print(f"\t\tlen_max_dir{len_max_dir}")
                        # 오른쪽 넣을 수 있는 공간 확인, 연속된 개수 저장
                        # 왼쪽 넣을 수 있는 공간 확인, 연속된 개수 저장
                        # 오른쪽 열린 k 측정 (오른쪽에 넣었다 가정하고 왼쪽 연속된 개수 + 오른쪽 연속된 개수 + 더 가보기)
                        # 왼쪽도 같은 방법으로 l측정
                        # n = k + l - 1
                    len_count = [0, 0, 0, 0, 0, 0, 0, 0]
                    halfblocked_len_count = [0, 0, 0, 0, 0, 0, 0, 0]
                    for i, len in enumerate(len_max_dir):  # 일반룰
                        if block[i] == 0:
                            len_count[len] += 1
                        elif block[i] == 1:
                            halfblocked_len_count[len] += 1
                        else:
                            assert True
                    # print(f"\tlen_count:             {len_count}")
                    # print(f"\thalfblocked_len_count: {halfblocked_len_count}")
                    #절대치 기준: 5 > 열린4 > 닫힌4 > 열린3 > 닫힌 3 > ...
                    if len_count[4] >= 2:
                        # print("\t44")
                        score[player_index(player_pos)] += INF//32
                    elif len_count[4] >= 1 and len_count[3] == 1:
                        # print("\t43")
                        score[player_index(player_pos)] += INF//34
                    elif len_count[4] >= 1:
                        # print("\t4")
                        score[player_index(player_pos)] += INF//36
                    elif halfblocked_len_count[4] >= 1:
                        score[player_index(player_pos)] += INF//38
                    elif len_count[3] >= 2:
                        # print("\t33")
                        # print(f"33 detected: {move}")
                        score[player_index(player_pos)] += -INF
                    elif len_count[3] == 1:
                        # print("3")
                        # print("3발견!")
                        score[player_index(player_pos)] += INF//128

                    for i, _len in enumerate(len_max_dir):
                        if _len > 0:
                            score[player_index(player_pos)] += 2 ** (1 + _len*2 - block[i])  # score[1]: player 1(black) socre, score[0]: player -1(white) score

                    # print(f"현재 eval_func: {score[player_index(player_now)] - score[player_index(-player_now)]}")
        #어떻게 작동해야 하나?
        #eval func: 한 수만 볼 수 있는 경우 eval func는 greedy하게 움직이는 건 어쩔 수 없나? 어차피 두 수 후만 봐도 OOO을 막아야 한다는걸 아나?
        #5, 열린4 => MAX보상

        # elif '3' => 개수당 +32 ┼○○○┼ ┼○○┼○┼
        # elif 반닫힌'3' => 개수당 +16 ●○○○┼ ●○○┼○┼
        # elif '2' => 개수당 +8 ┼○○┼ ┼○┼○┼
        # elif 반닫힌'2' => 개수당 +4 ●○○┼ ●○┼○┼
        # elif '1' => 개수당 +2 ┼○┼
        # elif 반닫힌 '1' => 개수당 +1 ●○┼
        # 만약 가능한 길이 < 5 인 경우 +0 ●????● ●???● ●??● ●?●

        #print("get_evaluation_function end")
        # print(f"score[player: {player_now}]: {score[(player_now + 1) // 2]}, score[player: {-player_now}]: {score[(-player_now + 1) // 2]}")
        # print(f"result: {score[(player_now + 1) // 2] - score[(-player_now + 1) // 2] * 8}")
        return score[player_index(player_now)] - score[player_index(-player_now)] * 1.5#나의 이득이 우선. 이득이 비슷하면 상대의 점수를 낮추는 수가 더 좋음.
    #def is_acceptable

@memoize #loop, limit 고려안하도록.
def heuristic_minimax(state, last_input, a, b, player_turn_in_state, player_now, limit, loop, end_time, depth_limit): #returns utility 값 / heuristic 값
    indent = '\t' * (depth_limit - limit + 1)
    # print(f"{indent}heuristic_minimax(depth:{depth_limit-limit}, last_input: {last_input}, alpha: {a}, beta: {b}, player: {player_turn_in_state}, limit: {limit})")
    #state.print_board()
    #assert state.goal_test_pos(last_input) == False or state.goal_test_pos(last_input) == player_turn
    win_player = state.goal_test_pos(last_input)
    if win_player == player_now: #player_now win
        print(f"goal state found{last_input}, state.check:{state.check(last_input)}, win_player:{win_player} eval_func: +987654321")
        return False, 987654321 #마지막 수가 player_now의 수였을 경우
    elif win_player == -player_now: #player_now lose
        print(f"goal state found{last_input}, state.check:{state.check(last_input)}, win_player:{win_player}, eval_func: -987654321")
        return False, -987654321
    if limit == 0: #or
        # state.print_board()
        # print(state.get_evaluation_function(player_now))
        # print()
        # print(f"{indent}heuristic_result: eval_func: {state.get_evaluation_function(player_now)}")
        return True, state.get_evaluation_function(player_now)
    elif loop.time() > end_time:
        return True, TIMEOUT
    cutoff_occurred = False
    cutoff = False

    INF = 987654321
    if player_turn_in_state == player_now:  # max_value
        v = -INF
    else:  # min_value
        v = INF
    is_available_pos = False

    for i in range(SIZE):
        for j in range(SIZE):
            if state.board[i][j] == 0:
                is_pos_worth_check = False
                for __i in range(-2, 3):
                    for __j in range(-2, 3):
                        ii = i + __i
                        jj = j + __j
                        if ii >= 0 and ii < SIZE and jj >= 0 and jj < SIZE and state.board[i + __i][j + __j] != 0:
                            is_pos_worth_check = True
                            break
                if is_pos_worth_check:
                    is_available_pos = True
                    child = Node(copy.deepcopy(state.get_board()))
                    child.input(c(i,j), player_turn_in_state)
                    #child.update_evaluation_func(c(i,j))
                    state.children.append(child)
                    cutoff, h_minimax = heuristic_minimax(child, c(i, j), a, b, -player_turn_in_state, player_now, limit - 1, loop, end_time, depth_limit)
                    if h_minimax == TIMEOUT:
                        return True, TIMEOUT
                    elif cutoff:
                            cutoff_occurred = True
                    if player_turn_in_state == player_now: #max_value
                        v = max(v, h_minimax) #v 최댓값 갱신
                        if v >= b:
                            return cutoff, v #베타 가지치기
                        a = max(a, v)
                    else: #min_value
                        v = min(v, h_minimax) #v 최솟값 갱신
                        if v <= a:
                            return cutoff, v #알파 가지치기
                        b = min(b, v)

    if not is_available_pos: #Terminal state 판단 (한 칸씩 확인해야 하므로 뒤로 미룸)
        return False, 0
    # print(f"{indent}heuristic_result: selected_eval_func: {v}")
    return cutoff_occurred, v

    #만약 보드가 terminal state이면 utility 리턴 (승리 1 패배 -1)
    #v = -INF
    #for 가능한 액션에 대해
    #   v = min(v, MAX_VALUE(board에 액션 수행한 보드,a,b))
    #   if v <= a then return v #a = alpha = MAX 경로에서 현재까지 발견한 최선의 선택 (값이 가장 큰 선택)
    #   b = min(b,v)
    #return v

def ai_async_wrapper(allowable_board, player_turn, TIME_LIMIT):
    loop = asyncio.get_event_loop()
    end_time = loop.time() + TIME_LIMIT
    task = ai(allowable_board, player_turn, loop, end_time),
    result, = loop.run_until_complete(asyncio.gather(*task))
    return result

async def ai(allowable_board, player_turn, loop, end_time):
    INF = 999999999
    argmax = c(0, 0)
    for depth_limit in range(0, 1, +1): #iterative deepening
        is_available_pos = False
        argmax = c(0, 0)
        last_argmax = c(0, 0)
        v = -INF
        a = -INF
        b = INF #v, a, b를 매 depth마다 초기화해줘야 이전 탐색이 영향을 안 줌!!
        cutoff_occurred = False
        TIMEOUT_occurred = False
        print(f"Depth{depth_limit} search start")
        for i in range(SIZE):
            for j in range(SIZE):
                if not TIMEOUT_occurred:
                    is_pos_worth_check = False
                    if allowable_board[i][j] == player_turn:
                        is_pos_worth_check = True
                    elif allowable_board[i][j] == True:
                        for __i in range(-2,3):
                            for __j in range(-2,3):
                                ii = i + __i
                                jj = j + __j
                                if ii >= 0 and ii < SIZE and jj >= 0 and jj < SIZE and allowable_board[i+__i][j+__j] == False:
                                    is_pos_worth_check = True
                                    break
                    if is_pos_worth_check:
                        is_available_pos = True
                        child = Node(copy.deepcopy(Board.get_board()))
                        child.input(c(i,j), player_turn)
                        #child.update_evaluation_func(c(i,j))
                        cutoff, h_minimax = heuristic_minimax(child, c(i,j), a, b, -player_turn, player_turn, depth_limit, loop, end_time, depth_limit)
                        print(str(int(h_minimax)) + ' ', end = '')
                        # print(f"{c(i,j)}, v:{v}")
                        if h_minimax == INF and depth_limit == 0:
                            last_argmax = c(i,j)
                            TIMEOUT_occurred = True #한 step만에 goal을 찾은 경우 더 이상 탐색하지 않음. 이를 위해 TIMEOUT_occurred 이용
                            break
                        if h_minimax == TIMEOUT:
                            TIMEOUT_occurred = True #Timeout이 발생한 경우: 탐색을 취소하고 그전 단계의 결과 리턴
                            break
                        elif cutoff: #cutoff가 발생했는지 확인. 모든 경우의 수를 완전히 탐색했을 경우 발생하지 않음.
                            cutoff_occurred = True
                        if h_minimax >= v:
                            v = h_minimax
                            argmax = c(i,j)
                    else:
                        print(draw_cell(Board.check(c(i,j))) + ' ', end='')
            print()
                            # print(f"Best node update: {argmax}")
                        # if v >= b:
                        #     last_argmax = c(i,j)
                        #     TIMEOUT_occurred = True #베타 가지치기. TIMEOUT_occurred 이용

        if TIMEOUT_occurred:
            print(f"Cutoff by timeout. Previous depth result: {last_argmax}")
            return last_argmax
        print(f"Depth{depth_limit} search result: recommend {argmax}, eval_func: {v}")
        last_argmax = argmax
        if not cutoff_occurred:
            print(f"Completely searched in this depth limit: {depth_limit}. No cutoff found.")
            break
        if not is_available_pos: #depth
            print("GAME END! There is no available position.")
            print("press any key to quit..")
            input()
            sys.exit()
    return argmax

TIME_LIMIT = 99#int(input("set AI's turn time limit (second): "))
player_turn = 1#1 for black(play  first), -1 for white
while True:
    who_is_player = int(input("Choose player to play first (1 = you, 0 = computer): "))
    if who_is_player in (0,1):
        break
    print("Invalid input. Try again.")
who_is_player = ('computer', 'you')[who_is_player]
#player_turn : 흑 차례 (1), 백 차례 (-1)
#who_is_player : 'computer', 'you'


# n = Node([
#     [0, -1, -1, 1, -1, 0, 0, 0],
#     [0, 0, 1, 1, 1, 0, 0, 0],
#     [0, 1, -1, -1, 1, 0, 0, 0],
#     [-1, 1, -1, 1, 1, -1, 0, 0],
#     [0, 1, -1, -1, 1, 1, 0, 0],
#     [0, -1, 1, 1, -1, -1 0, 0],
#     [0, 0, 1, 1, -1, -1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
# ])
# n.print_board()
# print(n.get_evaluation_function(1))
# raise Exception

# Board.b = [
#     [0, -1, -1, 1, -1, 0, 0, 0],
#     [0, 0, 1, 1, 1, 0, 0, 0],
#     [0, 1, -1, -1, 1, 0, 0, 0],
#     [-1, 1, -1, 1, 1, -1, 0, 0],
#     [0, 1, -1, -1, 1, 1, 0, 0],
#     [0, -1, 1, 1, -1, -1, 0, 0],
#     [0, 0, 1, 1, -1, -1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
# ]

# Board.update_allowable_pos_board()
# print(Board.is_acceptable(c(6,3),1))
# raise Exception
# pprint(Board.bs)
#33을 막지 않고 51을 두는 이유
#  0 1 2 3 4 5 6 7
# 0┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼
# 1┼ ┼ ┼ ┼ ● ┼ ┼ ┼
# 2○ ● ● ● ● ○ ● ┼
# 3┼ ● ○ ○ ○ ● ○ ┼
# 4┼ ● ○ ○ ○ ● ○ ┼
# 5┼ ┼ ● ┼ ┼ ┼ ┼ ┼
# 6┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼
# 7┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼ 보다
#
#  0 1 2 3 4 5 6 7
# 0┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼
# 1┼ ┼ ┼ ┼ ● ┼ ┼ ┼
# 2○ ● ● ● ● ○ ● ┼
# 3┼ ● ○ ○ ○ ┼ ○ ┼
# 4┼ ● ○ ○ ○ ● ○ ┼
# 5┼ ● ● ┼ ┼ ┼ ┼ ┼
# 6┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼
# 7┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼ 의 가중치가 더 높아서 => 33/34/4 발견시 즉시 return 하게 해서 그랬음. INF/2 /4 /8로 가중치를 뒀으니 더하게 해도 됨.
#
#  0 1 2 3 4 5 6 7
# 0┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼
# 1┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼
# 2○ ● ● ● ● ○ ┼ ┼
# 3┼ ┼ ┼ ┼ ○ ○ ┼ ┼
# 4┼ ● ○ ○ ○ ○ ● ┼
# 5┼ ┼ ● ┼ ┼ ┼ ┼ ┼
# 6┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼
# 7┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼  이제는 여기서 33에 둠. 4 막기보다 33의 가중치가 높아서 그런듯. 상대방은 가중치를 2배? 혹은 2.5배? 로 해야할거같다.
#
#  0 1 2 3 4 5 6 7
# 0┼ ┼ ┼ ┼ ┼ ● ┼ ●
# 1┼ ┼ ┼ ┼ ○ ○ ○ ┼
# 2○ ● ● ● ● ○ ┼ ┼
# 3┼ ○ ○ ● ○ ○ ● ○
# 4┼ ● ○ ○ ○ ○ ● ┼
# 5┼ ┼ ● ● ○ ● ┼ ┼
# 6┼ ┼ ┼ ┼ ● ┼ ┼ ┼
# 7┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼ 상대방은 2.5배 해서 뺐는데도 여기서 65를 둠.
#
#  0 1 2 3 4 5 6 7
# 0┼ ┼ ┼ ┼ ┼ ● ┼ ●
# 1┼ ○ ┼ ┼ ○ ○ ○ ┼
# 2○ ● ● ● ● ○ ┼ ┼
# 3┼ ○ ○ ● ○ ○ ● ○
# 4┼ ● ○ ○ ○ ○ ● ┼
# 5┼ ┼ ● ● ○ ● ┼ ┼
# 6┼ ┼ ┼ ┼ ● ● ┼ ┼
# 7┼ ┼ ┼ ┼ ┼ ┼ ┼ ┼ 여기서는 금수까지둠 63 (33금수) 이건 allowable_board에서 제대로 테스트 안해서 그런듯. 이것 먼저 해결하자. => 해결!


next_move = None
while True:
    print_board()
    if next_move is not None:
        goal_test = Board.goal_test_pos(next_move)
        if goal_test != False:
            print(f"{('Black','White')[player_index(goal_test)]} win!")
            break
    if who_is_player == 'you':
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
        who_is_player = 'computer'
        player_turn = -player_turn
    elif who_is_player == 'computer':
        Board.update_allowable_pos_board()
        ab = Board.get_allowable_pos_board()
        next_move = ai_async_wrapper(ab, player_turn, TIME_LIMIT)
        while not Board.is_empty(next_move):
            print(f"{next_move} Invalid computer movement. Stone already exists. Retrying..")
            next_move = ai_async_wrapper(ab, player_turn, TIME_LIMIT)
        # while not Board.is_acceptable(next_move, player_turn):
        #     print(f"{next_move} Invalid computer movement. Unacceptable. Retrying..")
        #     next_move = ai(ab, player_turn)
        Board.update_board(next_move, player_turn)
        player_turn = -player_turn
        who_is_player = 'you'
        print(f"Computer move: {next_move}")

#해야할것. goal_test_pos가 작동안하는것같다. 3수 앞까지 봐도 ooo을 안막음. 검색에 뜨지도 않음. 그리고 휴리스틱을 한 수만 봐도 3을 막도록 하는건 어떻게 해야할지..