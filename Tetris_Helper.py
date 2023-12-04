import copy
import math

import ThreeD_Helper
import uvage
import random as r


board_width = 10
board_height = 25
board_extra_space = 5
scene_width = 1920
scene_height = 1080
board_top_left_position = [100, 100]
blank_color = [255, 255, 255]
block_width = 40


def get_high_score():
    f = open('tetris_data.txt', 'r')
    high_score = int(f.readline())
    f.close()
    return high_score


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
    center_position = [5, 2]
    block_positions = []
    color = [0, 0, 0]
    current_rotation = 0  # 0, 1=R, 2, 3=L
    offset = [[]]

    def __init__(self):
        self.center_position = copy.deepcopy([5, 2])
        self.block_positions = []
        self.offset = [[]]

    def check_game_over(self, board):
        for i in self.block_positions:
            if board[int(i[1] + self.center_position[1])][int(i[0] + self.center_position[0])] != blank_color:
                return True
            if int(i[1] + self.center_position[1]) < 0:
                return True
        return False

    def check_t_spin(self, board):
        return [False, False]

    def rotate(self, board, direction="clockwise"):  # Returns [Rotation Successful, t-spin, mini t-spin]
        new_block_positions = []
        new_center_position = copy.deepcopy(self.center_position)
        issues = False
        c_r = self.current_rotation
        if direction == "clockwise":
            if c_r + 1 >= 4:
                c_r = 0
            else:
                c_r += 1
            kick_translations = []
            for i in range(len(self.offset[self.current_rotation])):
                x = self.offset[self.current_rotation][i][0] - self.offset[c_r][i][0]
                y = self.offset[self.current_rotation][i][1] - self.offset[c_r][i][1]
                kick_translations.append([x, y])
            for i in kick_translations:
                issues = False
                new_center_position[0] = self.center_position[0] + i[0]
                new_center_position[1] = self.center_position[1] - i[1]
                for j in range(len(self.block_positions)):
                    new_block_position = rotate_point_around(self.block_positions[j], [0, 0], direction)
                    new_block_positions.append(new_block_position)
                    new_x = int(new_block_position[0] + new_center_position[0])
                    new_y = int(new_block_position[1] + new_center_position[1])
                    while new_x < 0:
                        new_center_position[0] += 1
                        new_x += 1
                    while new_x >= board_width:
                        new_center_position[0] -= 1
                        new_x -= 1
                    # ("new_center:", new_center_position)
                    if new_x < 0 or new_x > board_width or new_y >= board_height or new_y < 0 or board[new_y][new_x] != blank_color:
                        issues = True
                        break
                if not issues:
                    break
            if issues:
                return [False, False, False]
            self.center_position = new_center_position
            self.block_positions = new_block_positions
            self.current_rotation = c_r
            my_list = self.check_t_spin(board)
            return [True, my_list[0], my_list[1]]
        elif direction == "counter":
            if c_r - 1 < 0:
                c_r = 3
            else:
                c_r -= 1
            kick_translations = []
            for i in range(len(self.offset[self.current_rotation])):
                x = self.offset[self.current_rotation][i][0] - self.offset[c_r][i][0]
                y = self.offset[self.current_rotation][i][1] - self.offset[c_r][i][1]
                kick_translations.append([x, y])
            for i in kick_translations:
                issues = False
                new_center_position[0] = self.center_position[0] + i[0]
                new_center_position[1] = self.center_position[1] - i[1]
                for j in range(len(self.block_positions)):
                    new_block_position = rotate_point_around(self.block_positions[j], [0, 0], direction)
                    new_block_positions.append(new_block_position)
                    new_x = int(new_block_position[0] + new_center_position[0])
                    new_y = int(new_block_position[1] + new_center_position[1])
                    while new_x < 0:
                        new_center_position[0] += 1
                        new_x += 1
                    while new_x >= board_width:
                        new_center_position[0] -= 1
                        new_x -= 1
                    # ("new_center:", new_center_position)
                    if new_x < 0 or new_x > board_width or new_y >= board_height or new_y < 0 or board[new_y][new_x] != blank_color:
                        issues = True
                        break
                if not issues:
                    break
            if issues:
                return [False, False, False]
            self.center_position = new_center_position
            self.block_positions = new_block_positions
            self.current_rotation = c_r
            my_list = self.check_t_spin(board)
            return [True, my_list[0], my_list[1]]
        else:
            return [False, False, False]


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
                number_of_lines_cleared = check_clear_lines(board)
                return number_of_lines_cleared
        self.center_position[1] += 1
        return -1  # Returns -1 if move_down successfully moved tetrimino down

    def add_to_board(self, board):
        for i in self.block_positions:
            x = int(i[0] + self.center_position[0])
            y = int(i[1] + self.center_position[1])
            board[y][x] = self.color

    def get_copy(self):
        my_copy = Tetrimino()
        my_copy.block_positions = copy.deepcopy(self.block_positions)
        my_copy.color = copy.deepcopy(self.color)
        my_copy.center_position[0] = self.center_position[0]
        my_copy.center_position[1] = self.center_position[1]
        return my_copy

    def get_ghost(self, board):
        current_y = self.center_position[1]
        loop = current_y
        while loop < board_height:
            current_y += 1
            loop = current_y
            for i in self.block_positions:
                x = int(i[0] + self.center_position[0])
                y = int(i[1] + current_y)
                if 0 <= x < board_width and y >= board_height or board[y][x] != blank_color:
                    loop = 100
                    continue
        ghost = Tetrimino()
        new_color = [(self.color[0] + 3 * blank_color[0]) / 4, (self.color[1] + 3 * blank_color[1]) / 4, (self.color[2] + 3 * blank_color[2]) / 4]
        ghost.color = new_color
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
        self.center_position = [5, board_extra_space - 1]
        self.block_positions = copy.deepcopy([[-1, 0], [0, 0], [1, 0], [2, 0]])
        o_offsets = [[0, 0], [-1, 0], [2, 0], [-1, 0], [2, 0]]
        r_offsets = [[-1, 0], [0, 0], [0, 0], [0, 1], [0, -2]]
        two_offsets = [[-1, 1], [1, 1], [-2, 1], [1, 0], [-2, 0]]
        l_offsets = [[0, 1], [0, 1], [0, 1], [0, -1], [0, 2]]
        self.offset = [o_offsets, r_offsets, two_offsets, l_offsets]

    
class TBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [125, 0, 255]
        self.set_defaults()

    def check_t_spin(self, board):  # returns [t-spin, mini t-spin]
        # check mini t-spin
        # check true t-spin
        t_spin = False
        mini_t_spin = False
        number_in_front = 0
        number_behind = 0
        if self.center_position[1] - 1 < 0 or self.center_position[0] - 1 < 0:
            return [False, False]
        if self.center_position[1] + 1 >= board_height or self.center_position[0] + 1 >= board_width:
            return [False, False]
        if self.current_rotation == 0:
            if board[int(self.center_position[1] - 1)][int(self.center_position[0] - 1)] != blank_color:
                number_in_front += 1
            if board[int(self.center_position[1] - 1)][int(self.center_position[0] + 1)] != blank_color:
                number_in_front += 1
            if board[int(self.center_position[1] + 1)][int(self.center_position[0] - 1)] != blank_color:
                number_behind += 1
            if board[int(self.center_position[1] + 1)][int(self.center_position[0] + 1)] != blank_color:
                number_behind += 1
        elif self.current_rotation == 1:
            if board[int(self.center_position[1] - 1)][int(self.center_position[0] - 1)] != blank_color:
                number_behind += 1
            if board[int(self.center_position[1] - 1)][int(self.center_position[0] + 1)] != blank_color:
                number_in_front += 1
            if board[int(self.center_position[1] + 1)][int(self.center_position[0] - 1)] != blank_color:
                number_behind += 1
            if board[int(self.center_position[1] + 1)][int(self.center_position[0] + 1)] != blank_color:
                number_in_front += 1
        elif self.current_rotation == 2:
            if board[int(self.center_position[1] - 1)][int(self.center_position[0] - 1)] != blank_color:
                number_behind += 1
            if board[int(self.center_position[1] - 1)][int(self.center_position[0] + 1)] != blank_color:
                number_behind += 1
            if board[int(self.center_position[1] + 1)][int(self.center_position[0] - 1)] != blank_color:
                number_in_front += 1
            if board[int(self.center_position[1] + 1)][int(self.center_position[0] + 1)] != blank_color:
                number_in_front += 1
        elif self.current_rotation == 3:
            if board[int(self.center_position[1] - 1)][int(self.center_position[0] - 1)] != blank_color:
                number_in_front += 1
            if board[int(self.center_position[1] - 1)][int(self.center_position[0] + 1)] != blank_color:
                number_behind += 1
            if board[int(self.center_position[1] + 1)][int(self.center_position[0] - 1)] != blank_color:
                number_in_front += 1
            if board[int(self.center_position[1] + 1)][int(self.center_position[0] + 1)] != blank_color:
                number_behind += 1
        if number_in_front == 2 and number_behind == 1:
            t_spin = True
        elif number_behind == 2 and number_in_front == 1:
            mini_t_spin = True
        return [t_spin, mini_t_spin]

    def set_defaults(self):
        self.center_position = [5, board_extra_space - 1]
        self.block_positions = [[-1, 0], [0, 0], [0, -1], [1, 0]]
        o_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        r_offsets = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
        two_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        l_offsets = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
        self.offset = [o_offsets, r_offsets, two_offsets, l_offsets]

        
class ZBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [255, 0, 0]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, board_extra_space - 1]
        self.block_positions = [[-1, -1], [0, -1], [0, 0], [1, 0]]
        o_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        r_offsets = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
        two_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        l_offsets = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
        self.offset = [o_offsets, r_offsets, two_offsets, l_offsets]


class SBlock(Tetrimino):

    def __init__(self):
        super().__init__()
        self.color = [0, 255, 0]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, board_extra_space - 1]
        self.block_positions = [[-1, 0], [0, 0], [0, -1], [1, -1]]
        o_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        r_offsets = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
        two_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        l_offsets = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
        self.offset = [o_offsets, r_offsets, two_offsets, l_offsets]


class LBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [255, 165, 0]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, board_extra_space - 1]
        self.block_positions = [[-1, 0], [0, 0], [1, 0], [1, -1]]
        o_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        r_offsets = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
        two_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        l_offsets = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
        self.offset = [o_offsets, r_offsets, two_offsets, l_offsets]


class JBlock(Tetrimino):

    def __init__(self):
        super().__init__()
        self.color = [0, 0, 255]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, board_extra_space - 1]
        self.block_positions = [[-1, -1], [-1, 0], [0, 0], [1, 0]]
        o_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        r_offsets = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
        two_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        l_offsets = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
        self.offset = [o_offsets, r_offsets, two_offsets, l_offsets]


class OBlock(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.color = [255, 255, 0]
        self.set_defaults()

    def set_defaults(self):
        self.center_position = [5, board_extra_space - 1]
        self.block_positions = [[0, 0], [0, -1], [1, 0], [1, -1]]
        o_offsets = [[0, 0]]
        r_offsets = [[0, -1]]
        two_offsets = [[-1, -1]]
        l_offsets = [[-1, 0]]
        self.offset = [o_offsets, r_offsets, two_offsets, l_offsets]


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
    for i in range(board_height - board_extra_space):
        y = board_top_left_position[1] + i * block_width + block_width / 2
        for j in range(len(board[i - board_extra_space])):
            x = board_top_left_position[0] + j * block_width + block_width / 2
            game_box = uvage.from_color(x, y, board[i + board_extra_space][j], block_width, block_width)
            camera.draw(game_box)

    for i in current_tetrimino.get_ghost(board).get_block_positions():  # Draw ghost
        x = board_top_left_position[0] + (i[0] + + 0.5) * block_width
        y = board_top_left_position[1] + (i[1] + 0.5 - board_extra_space) * block_width
        if y > board_top_left_position[1]:
            game_box = uvage.from_color(x, y, current_tetrimino.get_ghost(board).color, block_width, block_width)
        camera.draw(game_box)

    for i in current_tetrimino.get_block_positions():  # Draws the current tetrimino on top of the board
        x = board_top_left_position[0] + (i[0] + 0.5) * block_width
        y = board_top_left_position[1] + (i[1] + 0.5 - board_extra_space) * block_width
        if y > board_top_left_position[1]:
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
            y = board_top_left_position[1] + i[1] * block_width + block_width * 4 + 100
            game_box = uvage.from_color(x, y, hold_tetrimino.color, block_width, block_width)
            camera.draw(game_box)


def draw_next(camera, uvage_camera: uvage.Camera):
    x = uvage.from_text(camera.position[0] - 325 + 600, camera.position[1] - 250, "NEXT", 40, [127, 127, 127])
    uvage_camera.draw(x)
    for i in next_tetrimino.get_block_positions():  # Draws the next tetrimino to the right of the board
        x = i[0] * block_width + camera.position[0] - 550 + 600
        y = i[1] * block_width + camera.position[1] - 300
        game_box = uvage.from_color(x, y, next_tetrimino.color, block_width, block_width)
        uvage_camera.draw(game_box)


def draw_hold(camera, uvage_camera: uvage.Camera):
    x = uvage.from_text(camera.position[0] - 325 + 600, camera.position[1] - 75, "HOLD", 40, [127, 127, 127])
    uvage_camera.draw(x)
    if hold_tetrimino is not None:
        for i in hold_tetrimino.get_block_positions():  # Draws the hold tetrimino to the right of the board
            x = i[0] * block_width + camera.position[0] - 550 + 600
            y = i[1] * block_width + camera.position[1] - 125
            game_box = uvage.from_color(x, y, hold_tetrimino.color, block_width, block_width)
            uvage_camera.draw(game_box)


def check_clear_lines(board):
    number_of_lines_cleared = 0
    for i in range(len(board)):
        csf = True
        for j in range(len(board[i])):
            if board[i][j] == blank_color:
                csf = False
                break
        if csf:
            number_of_lines_cleared += 1
            for j in range(len(board[i])):
                for k in range(i, 1, -1):
                    board[k][j] = board[k - 1][j]
    return number_of_lines_cleared


def get_radians(degrees):
    return degrees * math.pi / 180


def compare_score(player_score, high_score):
    #compares score, if higher than score in file, overwrites file
    if player_score >= high_score:
        g = open('tetris_data.txt', 'w')
        g.write(str(player_score))
        return True
    else:
        return False
