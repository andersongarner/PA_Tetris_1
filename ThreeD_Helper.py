import math

import Tetris_Helper as tH
import uvage
import copy


def rotate_point_around(point_0, point_1, pitch, yaw, roll):
    cosa = math.cos(-roll)
    sina = math.sin(-roll)
    cosb = math.cos(yaw)
    sinb = math.sin(yaw)
    cosc = math.cos(-pitch)
    sinc = math.sin(-pitch)
    axx = cosa * cosb
    axy = cosa * sinb * sinc - sina * cosc
    axz = cosa * sinb * cosc + sina * sinc
    ayx = sina * cosb
    ayy = sina * sinb * sinc + cosa * cosc
    ayz = sina * sinb * cosc - cosa * sinc
    azx = -1 * sinb
    azy = cosb * sinc
    azz = cosb * cosc
    p10x = point_1[0] - point_0[0]
    p10y = point_1[1] - point_0[1]
    p10z = point_1[2] - point_0[2]
    px = axx * p10x + axy * p10y + axz * p10z
    py = ayx * p10x + ayy * p10y + ayz * p10z
    pz = azx * p10x + azy * p10y + azz * p10z

    return [px + point_0[0], py + point_0[1], pz + point_0[2]]


class Camera:
    position = [0, 0, 0]
    rotation = [0, 0, 0]

    def __init__(self):
        pass

    def rotate_degrees(self, pitch, yaw, roll):
        self.rotation[0] += pitch * math.pi / 180
        self.rotation[1] += yaw * math.pi / 180
        self.rotation[2] += roll * math.pi / 180


class Quad:
    point_list = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    color = [0, 0, 0]

    def __init__(self, point_list: list, color):
        self.point_list = copy.deepcopy(self.point_list)
        self.color = copy.deepcopy(self.color)
        self.point_list = copy.deepcopy(point_list)
        self.color = copy.deepcopy(color)

    def move_all_points(self, xyz):
        for i in self.point_list:
            for j in range(len(i)):
                i[j] += xyz[j]

    def get_rotated_quad(self, point_0, pitch, yaw, roll):
        new_points = []
        for i in self.point_list:
            new_points.append(rotate_point_around(point_0, i, pitch, yaw, roll))
        return Quad(new_points, self.color)

    def get_avg(self, index):
        total = 0
        for i in range(len(self.point_list)):
            total += self.point_list[i][index]
        return total / 4

    def get_game_box(self):
        t_l = []
        for i in self.point_list:
            t_l.append((i[0], i[1]))
        return uvage.from_polygon(self.get_avg(0), self.get_avg(1), self.color, t_l[0], t_l[1], t_l[2], t_l[3]) #Fix X and Y


def partition(array: list[Quad], low, high):
    pivot = array[high].get_avg(2)
    i = low - 1
    for j in range(low, high):
        if array[j].get_avg(2) >= pivot:
            i += 1
            (array[i], array[j]) = (array[j], array[i])
    (array[i+1], array[high]) = (array[high], array[i+1])
    return i + 1


def quad_z_quicksort(array: list[Quad], low, high):
    if low < high:
        pi = partition(array, low, high)
        quad_z_quicksort(array, low, pi - 1)
        quad_z_quicksort(array, pi + 1, high)


class Model:
    position = [0, 0, 0]
    rotation = [0, 0, 0]  # [pitch, yaw, roll]
    quad_list: list[Quad] = []

    def __init__(self):
        self.position = copy.deepcopy(self.position)
        self.rotation = copy.deepcopy(self.rotation)
        self.quad_list = copy.deepcopy(self.quad_list)

    def move(self, xyz):
        for i in range(len(self.position)):
            self.position[i] = xyz[i]

    def rotate_degrees(self, pitch, yaw, roll):
        self.rotation[0] += pitch * math.pi / 180
        self.rotation[1] += yaw * math.pi / 180
        self.rotation[2] += roll * math.pi / 180

    def add_quad(self, new_quad: Quad):
        self.quad_list.append(new_quad)

    def draw_origin(self, cam):
        cam.draw(uvage.from_circle(self.position[0], self.position[1], [255, 255, 255], 5))
        cam.draw(uvage.from_circle(self.position[0], self.position[1], [0, 0, 0], 3))

    def get_game_box_list(self, camera: Camera):
        game_box_list = []
        pitch = self.rotation[0]
        yaw = self.rotation[1]
        roll = self.rotation[2]
        cam_pitch = camera.rotation[0]
        cam_yaw = camera.rotation[1]
        cam_roll = camera.rotation[2]
        copy_of_quad_list = copy.deepcopy(self.quad_list)
        rotated_quad_list = []
        for i in copy_of_quad_list:
            model_rotation_quad = i.get_rotated_quad([0, 0, 0], pitch, yaw, roll)
            model_rotation_quad.move_all_points([self.position[0], self.position[1], self.position[2]])
            rotated_quad_list.append(model_rotation_quad)
        camera_rotated_quad_list = []
        for i in rotated_quad_list:
            camera_rotated_quad = i.get_rotated_quad(camera.position, cam_pitch, cam_yaw, cam_roll)
            camera_rotated_quad_list.append(camera_rotated_quad)
        # Sort quads by z value
        quad_z_quicksort(camera_rotated_quad_list, 0, len(camera_rotated_quad_list) - 1)
        for i in camera_rotated_quad_list:
            current_game_box = i.get_game_box()
            current_game_box.x += camera.position[0] - tH.scene_width / 2
            current_game_box.y += camera.position[1] - tH.scene_height / 2
            game_box_list.append(current_game_box)
        return game_box_list


class Cube(Model):

    def __init__(self, position, width):
        super().__init__()
        self.position = position
        top_left_back = [-width, width, -width]
        bottom_left_back = [-width, -width, -width]
        top_right_back = [width, width, -width]
        bottom_right_back = [width, -width, -width]
        top_left_front = [-width, width, width]
        bottom_left_front = [-width, -width, width]
        top_right_front = [width, width, width]
        bottom_right_front = [width, -width, width]

        bottom_quad = Quad([bottom_right_front, bottom_right_back, bottom_left_back, bottom_left_front],
                               [0, 0, 255])  # Blue
        top_quad = Quad([top_right_front, top_right_back, top_left_back, top_left_front], [0, 255, 255])  # Cyan
        left_quad = Quad([top_left_back, top_left_front, bottom_left_front, bottom_left_back],
                             [255, 255, 0])  # Orange/Yellow
        right_quad = Quad([top_right_back, top_right_front, bottom_right_front, bottom_right_back],
                              [0, 255, 0])  # Green
        back_quad = Quad([top_left_back, top_right_back, bottom_right_back, bottom_left_back],
                             [255, 0, 255])  # Magenta
        front_quad = Quad([top_left_front, top_right_front, bottom_right_front, bottom_left_front],
                              [255, 0, 0])  # Red
        self.add_quad(bottom_quad)
        self.add_quad(top_quad)
        self.add_quad(left_quad)
        self.add_quad(right_quad)
        self.add_quad(back_quad)
        self.add_quad(front_quad)


def get_three_d_board(board: list[list[list[int]]]):
    front_model = Model()
    top_model = Model()
    right_model = Model()
    bottom_model = Model()
    left_model = Model()
    back_model = Model()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == tH.blank_color:
                continue
            f_top_left_corner = [j * tH.block_width - tH.block_width / 2, i * tH.block_width - tH.block_width / 2, tH.block_width / 2]
            f_top_right_corner = [j * tH.block_width + tH.block_width / 2, i * tH.block_width - tH.block_width / 2, tH.block_width / 2]
            f_bottom_right_corner = [j * tH.block_width + tH.block_width / 2, i * tH.block_width + tH.block_width / 2, tH.block_width / 2]
            f_bottom_left_corner = [j * tH.block_width - tH.block_width / 2, i * tH.block_width + tH.block_width / 2, tH.block_width / 2]
            b_top_left_corner = [j * tH.block_width - tH.block_width / 2, i * tH.block_width - tH.block_width / 2, -tH.block_width / 2]
            b_top_right_corner = [j * tH.block_width + tH.block_width / 2, i * tH.block_width - tH.block_width / 2, -tH.block_width / 2]
            b_bottom_right_corner = [j * tH.block_width + tH.block_width / 2, i * tH.block_width + tH.block_width / 2, -tH.block_width / 2]
            b_bottom_left_corner = [j * tH.block_width - tH.block_width / 2, i * tH.block_width + tH.block_width / 2, -tH.block_width / 2]

            # get front

            # get top
            if i - 1 < 0 or board[i - 1][j] == tH.blank_color:
                top_point_list = [b_top_left_corner, b_top_right_corner, f_top_right_corner, f_top_left_corner]
                top_color = [(board[i][j][0] + 255) // 2, (board[i][j][1] + 255) // 2,
                             (board[i][j][2] + 255) // 2]
                top_quad = Quad(top_point_list, top_color)
                top_model.add_quad(top_quad)


            # get bottom
            if i + 1 >= tH.board_height or board[i + 1][j] == tH.blank_color:
                bottom_point_list = [b_bottom_left_corner, b_bottom_right_corner, f_bottom_right_corner, f_bottom_left_corner]
                bottom_color = [board[i][j][0] // 2, board[i][j][1] // 2, board[i][j][2] // 2]
                bottom_quad = Quad(bottom_point_list, bottom_color)
                bottom_model.add_quad(bottom_quad)

            # get left side
            if j - 1 < 0 or board[i][j - 1] == tH.blank_color:
                left_point_list = [b_bottom_left_corner, b_top_left_corner, f_top_left_corner, f_bottom_left_corner]
                left_color = [(board[i][j][0] * 2) // 3, (board[i][j][1] * 2) // 3, (board[i][j][2] * 2) // 3]
                left_quad = Quad(left_point_list, left_color)
                left_model.add_quad(left_quad)
            # get right side
            if j + 1 >= tH.board_width or board[i][j + 1] == tH.blank_color:
                right_point_list = [b_bottom_right_corner, b_top_right_corner, f_top_right_corner, f_bottom_right_corner]
                right_color = [(board[i][j][0] * 2) // 3, (board[i][j][1] * 2) // 3, (board[i][j][2] * 2) // 3]
                right_quad = Quad(right_point_list, right_color)
                right_model.add_quad(right_quad)
            front_point_list = [f_top_left_corner, f_top_right_corner, f_bottom_right_corner, f_bottom_left_corner]
            front_quad = Quad(front_point_list, board[i][j])
            front_model.add_quad(front_quad)
            back_point_list = [b_top_left_corner, b_top_right_corner, b_bottom_right_corner, b_bottom_left_corner]
            back_quad = Quad(back_point_list, board[i][j])
            back_model.add_quad(back_quad)
    return [front_model, top_model, right_model, bottom_model, left_model, back_model]


def get_three_d_tetrimino(my_tetrimino: tH.Tetrimino):
    front_model = Model()
    top_model = Model()
    right_model = Model()
    bottom_model = Model()
    left_model = Model()
    back_model = Model()
    for i in my_tetrimino.block_positions:
        f_top_left_corner = [i[0] * tH.block_width - tH.block_width / 2, i[1] * tH.block_width - tH.block_width / 2, tH.block_width / 2]
        f_top_right_corner = [i[0] * tH.block_width + tH.block_width / 2, i[1] * tH.block_width - tH.block_width / 2, tH.block_width / 2]
        f_bottom_right_corner = [i[0] * tH.block_width + tH.block_width / 2, i[1] * tH.block_width + tH.block_width / 2, tH.block_width / 2]
        f_bottom_left_corner = [i[0] * tH.block_width - tH.block_width / 2, i[1] * tH.block_width + tH.block_width / 2, tH.block_width / 2]
        b_top_left_corner = [i[0] * tH.block_width - tH.block_width / 2, i[1] * tH.block_width - tH.block_width / 2, -tH.block_width / 2]
        b_top_right_corner = [i[0] * tH.block_width + tH.block_width / 2, i[1] * tH.block_width - tH.block_width / 2, -tH.block_width / 2]
        b_bottom_right_corner = [i[0] * tH.block_width + tH.block_width / 2, i[1] * tH.block_width + tH.block_width / 2, -tH.block_width / 2]
        b_bottom_left_corner = [i[0] * tH.block_width - tH.block_width / 2, i[1] * tH.block_width + tH.block_width / 2, -tH.block_width / 2]
        front_point_list = [f_top_left_corner, f_top_right_corner, f_bottom_right_corner, f_bottom_left_corner]
        front_quad = Quad(front_point_list, my_tetrimino.color)
        front_model.add_quad(front_quad)
        back_point_list = [b_top_left_corner, b_top_right_corner, b_bottom_right_corner, b_bottom_left_corner]
        back_quad = Quad(back_point_list, my_tetrimino.color)
        back_model.add_quad(back_quad)
        # [above = false, right = false, below = false, left = false]
        my_list = [False, False, False, False]
        for j in my_tetrimino.block_positions:
            if j[0] - i[0] == 0 and j[1] - i[1] == -1:
                my_list[0] = True
            elif j[0] - i[0] == 1 and j[1] - i[1] == 0:
                my_list[1] = True
            elif j[0] - i[0] == 0 and j[1] - i[1] == 1:
                my_list[2] = True
            elif j[0] - i[0] == -1 and j[1] - i[1] == 0:
                my_list[3] = True
        if not my_list[0]:  # no tetrimino above
            top_point_list = [b_top_left_corner, b_top_right_corner, f_top_right_corner, f_top_left_corner]
            top_color = [(my_tetrimino.color[0] + 255) // 2, (my_tetrimino.color[1] + 255) // 2, (my_tetrimino.color[2] + 255) // 2]
            top_quad = Quad(top_point_list, top_color)
            top_model.add_quad(top_quad)
        if not my_list[1]:  # no tetrimino right
            right_point_list = [b_top_right_corner, f_top_right_corner, f_bottom_right_corner, b_bottom_right_corner]
            right_color = [(2 * my_tetrimino.color[0]) // 3, (2 * my_tetrimino.color[1]) // 3, (2 * my_tetrimino.color[2]) // 3]
            right_quad = Quad(right_point_list, right_color)
            right_model.add_quad(right_quad)
        if not my_list[2]:  # no tetrimino bottom
            bottom_point_list = [b_bottom_left_corner, b_bottom_right_corner, f_bottom_right_corner, f_bottom_left_corner]
            bottom_color = [(my_tetrimino.color[0]) // 2, (my_tetrimino.color[1]) // 2, (my_tetrimino.color[2]) // 2]
            bottom_quad = Quad(bottom_point_list, bottom_color)
            bottom_model.add_quad(bottom_quad)
        if not my_list[3]:  # no tetrimino left
            left_point_list = [b_bottom_left_corner, b_top_left_corner, f_top_left_corner, f_bottom_left_corner]
            left_color = [(2 * my_tetrimino.color[0]) // 3, (2 * my_tetrimino.color[1]) // 3, (2 * my_tetrimino.color[2]) // 3]
            left_quad = Quad(left_point_list, left_color)
            left_model.add_quad(left_quad)

    return [front_model, top_model, right_model, bottom_model, left_model, back_model]


def get_whole_three_d_tetrimino(my_tetrimino: tH.Tetrimino):
    new_model = Model()
    for i in my_tetrimino.block_positions:
        f_top_left_corner = [i[0] * tH.block_width - tH.block_width / 2, i[1] * tH.block_width - tH.block_width / 2, tH.block_width / 2]
        f_top_right_corner = [i[0] * tH.block_width + tH.block_width / 2, i[1] * tH.block_width - tH.block_width / 2, tH.block_width / 2]
        f_bottom_right_corner = [i[0] * tH.block_width + tH.block_width / 2, i[1] * tH.block_width + tH.block_width / 2, tH.block_width / 2]
        f_bottom_left_corner = [i[0] * tH.block_width - tH.block_width / 2, i[1] * tH.block_width + tH.block_width / 2, tH.block_width / 2]
        b_top_left_corner = [i[0] * tH.block_width - tH.block_width / 2, i[1] * tH.block_width - tH.block_width / 2, -tH.block_width / 2]
        b_top_right_corner = [i[0] * tH.block_width + tH.block_width / 2, i[1] * tH.block_width - tH.block_width / 2, -tH.block_width / 2]
        b_bottom_right_corner = [i[0] * tH.block_width + tH.block_width / 2, i[1] * tH.block_width + tH.block_width / 2, -tH.block_width / 2]
        b_bottom_left_corner = [i[0] * tH.block_width - tH.block_width / 2, i[1] * tH.block_width + tH.block_width / 2, -tH.block_width / 2]
        front_point_list = [f_top_left_corner, f_top_right_corner, f_bottom_right_corner, f_bottom_left_corner]
        front_quad = Quad(front_point_list, my_tetrimino.color)
        new_model.add_quad(front_quad)
        back_point_list = [b_top_left_corner, b_top_right_corner, b_bottom_right_corner, b_bottom_left_corner]
        back_quad = Quad(back_point_list, my_tetrimino.color)
        new_model.add_quad(back_quad)
        # [above = false, right = false, below = false, left = false]
        my_list = [False, False, False, False]
        for j in my_tetrimino.block_positions:
            if j[0] - i[0] == 0 and j[1] - i[1] == -1:
                my_list[0] = True
            elif j[0] - i[0] == 1 and j[1] - i[1] == 0:
                my_list[1] = True
            elif j[0] - i[0] == 0 and j[1] - i[1] == 1:
                my_list[2] = True
            elif j[0] - i[0] == -1 and j[1] - i[1] == 0:
                my_list[3] = True
        if not my_list[0]:  # no tetrimino above
            top_point_list = [b_top_left_corner, b_top_right_corner, f_top_right_corner, f_top_left_corner]
            top_color = [(my_tetrimino.color[0] + 255) // 2, (my_tetrimino.color[1] + 255) // 2, (my_tetrimino.color[2] + 255) // 2]
            top_quad = Quad(top_point_list, top_color)
            new_model.add_quad(top_quad)
        if not my_list[1]:  # no tetrimino right
            right_point_list = [b_top_right_corner, f_top_right_corner, f_bottom_right_corner, b_bottom_right_corner]
            right_color = [(2 * my_tetrimino.color[0]) // 3, (2 * my_tetrimino.color[1]) // 3, (2 * my_tetrimino.color[2]) // 3]
            right_quad = Quad(right_point_list, right_color)
            new_model.add_quad(right_quad)
        if not my_list[2]:  # no tetrimino bottom
            bottom_point_list = [b_bottom_left_corner, b_bottom_right_corner, f_bottom_right_corner, f_bottom_left_corner]
            bottom_color = [(my_tetrimino.color[0]) // 2, (my_tetrimino.color[1]) // 2, (my_tetrimino.color[2]) // 2]
            bottom_quad = Quad(bottom_point_list, bottom_color)
            new_model.add_quad(bottom_quad)
        if not my_list[3]:  # no tetrimino left
            left_point_list = [b_bottom_left_corner, b_top_left_corner, f_top_left_corner, f_bottom_left_corner]
            left_color = [(2 * my_tetrimino.color[0]) // 3, (2 * my_tetrimino.color[1]) // 3, (2 * my_tetrimino.color[2]) // 3]
            left_quad = Quad(left_point_list, left_color)
            new_model.add_quad(left_quad)
    quad_z_quicksort(new_model.quad_list, 0, len(new_model.quad_list) - 1)
    return new_model
