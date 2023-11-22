import copy

import uvage
import random as r

board_width = 10
board_height = 20
scene_width = 1920
scene_height = 1080
board_top_left_position = [100, 100]
blank_color = [255, 255, 255]
block_width = 20


def rotate_point_around(point0, point1, direction="clockwise"):  # Rotate point0 around point1
    x = point0[0] - point1[0]
    y = point0[1] - point1[1]
    if direction == "clockwise":
        cos = 0
        sin = 1
    elif direction == "counter":
        cos = 0
        sin = -1
    else:
        print("direction not recognized in rotate_point_around...")
        exit()
    new_x = (x * cos - y * sin) + point1[0]
    new_y = (x * sin - y * cos) + point1[1]
    return [new_x, new_y]


class Tetrimino:
    center_position = [2, 1]
    block_positions = []
    color = [0, 0, 0]

    def __init__(self):
        self.center_position = [5, 1]
        self.block_positions = []
        self.color = [0, 0, 0]

    def check_game_over(self, board):
        for i in self.block_positions:
            if board[int(i[1] + self.center_position[1])][int(i[0] + self.center_position[0])] != blank_color:
                return True
            if int(i[1] + self.center_position[1]) < 0:
                return True
        return False

    def rotate(self, board, direction="clockwise"):
        new_block_positions = []
        for i in range(len(self.block_positions)):
            new_block_position = rotate_point_around(self.block_positions[i], [0, 0], direction)
            new_block_positions.append(new_block_position)
            new_x = int(new_block_position[0] + self.center_position[0])
            new_y = int(new_block_position[1] + self.center_position[1])
            while new_x < 0:
                self.center_position[0] += 1
                new_x += 1
            while new_x >= board_width:
                self.center_position[0] -= 1
                new_x -= 1
            if new_y >= board_height or new_y < 0 or board[new_y][new_x] != blank_color:
                return False
        self.block_positions = new_block_positions
        return True

    def move_x(self, board, direction=""):
        move_val = 0
        if direction == "left":
            move_val = -1
            for i in self.block_positions:
                if i[0] + self.center_position[0] + move_val < 0:
                    move_val = 0
                    continue
                if board[int(i[1] + self.center_position[1])][int(i[0] + self.center_position[0] + move_val)] != blank_color:
                    move_val = 0
        elif direction == "right":
            move_val = 1
            for i in self.block_positions:
                if i[0] + self.center_position[0] + move_val >= board_width:
                    move_val = 0
                    continue
                if board[int(i[1] + self.center_position[1])][int(i[0] + self.center_position[0] + move_val)] != blank_color:
                    move_val = 0
        else:
            print("direction not recognized in move...")
        self.center_position[0] += move_val

    def get_block_positions(self):
        new_block_positions = []
        for i in self.block_positions:
            new_block_positions.append([i[0] + self.center_position[0], i[1] + self.center_position[1]])
        return new_block_positions

    def move_down(self, board):
        for i in self.block_positions:
            x = int(i[0] + self.center_position[0])
            y = int(i[1] + self.center_position[1]) + 1
            if y >= board_height or board[y][x] != blank_color:
                self.add_to_board(board)
                check_clear_lines(board)
                return False
        self.center_position[1] += 1
        return True

    def add_to_board(self, board):
        for i in self.block_positions:
            x = int(i[0] + self.center_position[0])
            y = int(i[1] + self.center_position[1])
            board[y][x] = self.color

    def get_ghost(self, board):
        current_y = self.center_position[1]
        loop = current_y
        while loop < board_height:
            current_y += 1
            loop = current_y
            for i in self.block_positions:
                x = int(i[0] + self.center_position[0])
                y = int(i[1] + current_y)
                if y >= board_height or board[y][x] != blank_color:
                    loop = 100
                    continue
        ghost = Tetrimino()
        ghost.color = [self.color[0] / 2, self.color[1] / 2, self.color[2] / 2]
        ghost.block_positions = copy.deepcopy(self.block_positions)
        ghost.center_position[0] = self.center_position[0]
        ghost.center_position[1] = current_y - 1
        return ghost


class IBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [0, 255, 255]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5.5, 0.5]
        self.block_positions = [[-1.5, 0.5], [-0.5, 0.5], [0.5, 0.5], [1.5, 0.5]]

    
class TBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [125, 0, 255]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, 1]
        self.block_positions = [[-1, 0], [0, 0], [0, -1], [1, 0]]

        
class ZBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [255, 0, 0]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, 1]
        self.block_positions = [[-1, 0], [0, 0], [0, -1], [1, -1]]



class SBlock(Tetrimino):

    def __init__(self):
        super().__init__()
        self.color = [0, 255, 0]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, 1]
        self.block_positions = [[-1, -1], [0, -1], [0, 0], [1, 0]]


class LBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [255, 165, 0]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, 1]
        self.block_positions = [[-1, 0], [0, 0], [1, 0], [1, 1]]


class JBlock(Tetrimino):

    def __init__(self):
        super().__init__()
        self.color = [0, 0, 255]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, 1]
        self.block_positions = [[-1, 1], [-1, 0], [0, 0], [1, 0]]


class OBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [255, 255, 0]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5.5, 0.5]
        self.block_positions = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]


def generate_new_tetrimino():
    rand = r.randint(1, 7)
    if rand == 1:
        return IBlock()
    elif rand == 2:
        return TBlock()
    elif rand == 3:
        return SBlock()
    elif rand == 4:
        return ZBlock()
    elif rand == 5:
        return LBlock()
    elif rand == 6:
        return JBlock()
    elif rand == 7:
        return OBlock()


next_tetrimino = generate_new_tetrimino()


def get_next_tetrimino():
    global next_tetrimino
    temp = copy.deepcopy(next_tetrimino)
    next_tetrimino = generate_new_tetrimino()
    return temp


hold_tetrimino = None


def swap_hold_tetrimino(my_tetrimino):
    global hold_tetrimino
    if hold_tetrimino is None:
        my_tetrimino.set_defaults()
        hold_tetrimino = my_tetrimino
        my_tetrimino = get_next_tetrimino()
        return my_tetrimino
    else:
        temp = hold_tetrimino
        my_tetrimino.set_defaults()
        hold_tetrimino = my_tetrimino
        return temp



def draw_board(board, current_tetrimino: Tetrimino, camera: uvage.Camera):
    for i in range(len(board)):
        y = board_top_left_position[1] + i * block_width + block_width / 2
        for j in range(len(board[i])):
            x = board_top_left_position[0] + j * block_width + block_width / 2
            game_box = uvage.from_color(x, y, board[i][j], block_width, block_width)
            camera.draw(game_box)

    for i in current_tetrimino.get_ghost(board).get_block_positions():  # Draw ghost
        x = board_top_left_position[0] + (i[0] + + 0.5) * block_width
        y = board_top_left_position[1] + (i[1] + 0.5) * block_width
        game_box = uvage.from_color(x, y, current_tetrimino.get_ghost(board).color, block_width, block_width)
        camera.draw(game_box)

    for i in current_tetrimino.get_block_positions():  # Draws the current tetrimino on top of the board
        x = board_top_left_position[0] + (i[0] + + 0.5) * block_width
        y = board_top_left_position[1] + (i[1] + 0.5) * block_width
        game_box = uvage.from_color(x, y, current_tetrimino.color, block_width, block_width)
        camera.draw(game_box)

    for i in next_tetrimino.get_block_positions():  # Draws the next tetrimino to the right of the board
        x = board_top_left_position[0] + board_width * block_width + i[0] * block_width + 50
        y = board_top_left_position[1] + i[1] * block_width
        game_box = uvage.from_color(x, y, next_tetrimino.color, block_width, block_width)
        camera.draw(game_box)

    if hold_tetrimino is not None:
        for i in hold_tetrimino.get_block_positions():  # Draws the hold tetrimino to the right of the board
            x = board_top_left_position[0] + board_width * block_width + i[0] * block_width + 50
            y = board_top_left_position[1] + i[1] * block_width +  block_width * 4 + 100
            game_box = uvage.from_color(x, y, hold_tetrimino.color, block_width, block_width)
            camera.draw(game_box)


def check_clear_lines(board):
    for i in range(len(board)):
        csf = True
        for j in range(len(board[i])):
            if board[i][j] == blank_color:
                csf = False
                break
        if csf:
            for j in range(len(board[i])):
                for k in range(i, 1, -1):
                    board[k][j] = board[k - 1][j]
