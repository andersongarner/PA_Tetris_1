import math
import uvage
import copy


def rotate_point_around(point_0, point_1, pitch, yaw, roll):
    cosa = math.cos(yaw)
    sina = math.sin(yaw)
    cosb = math.cos(pitch)
    sinb = math.sin(pitch)
    cosc = math.cos(roll)
    sinc = math.sin(roll)
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
        # cam_pitch = camera.rotation[0]
        # cam_yaw = camera.rotation[1]
        # cam_roll = camera.rotation[2]
        copy_of_quad_list = copy.deepcopy(self.quad_list)
        rotated_quad_list = []
        for i in copy_of_quad_list:
            model_rotation_quad = i.get_rotated_quad([0, 0, 0], pitch, yaw, roll)
            rotated_quad_list.append(model_rotation_quad)
        # Sort quads by z value
        quad_z_quicksort(rotated_quad_list, 0, len(rotated_quad_list) - 1)
        for i in rotated_quad_list:
            current_game_box = i.get_game_box()
            current_game_box.x += self.position[0]
            current_game_box.y += self.position[1]
            game_box_list.append(current_game_box)
        return game_box_list


cam = uvage.Camera(1920, 1080)

cube = Model()
cube.position = [500, 500, 500]

top_left_back = [-100, 100, -100]
bottom_left_back = [-100, -100, -100]
top_right_back = [100, 100, -100]
bottom_right_back = [100, -100, -100]
top_left_front = [-100, 100, 100]
bottom_left_front = [-100, -100, 100]
top_right_front = [100, 100, 100]
bottom_right_front = [100, -100, 100]

bottom_quad = Quad([bottom_right_front, bottom_right_back, bottom_left_back, bottom_left_front], [0, 0, 255])  # Blue
top_quad = Quad([top_right_front, top_right_back, top_left_back, top_left_front], [0, 255, 255])  # Cyan
left_quad = Quad([top_left_back, top_left_front, bottom_left_front, bottom_left_back], [255, 255, 0])  # Orange/Yellow
right_quad = Quad([top_right_back, top_right_front, bottom_right_front, bottom_right_back], [0, 255, 0])  # Green
back_quad = Quad([top_left_back, top_right_back, bottom_right_back, bottom_left_back], [255, 0, 255])  # Magenta
front_quad = Quad([top_left_front, top_right_front, bottom_right_front, bottom_left_front], [255, 0, 0])  # Red

cube.add_quad(bottom_quad)
cube.add_quad(top_quad)
cube.add_quad(left_quad)
cube.add_quad(right_quad)
cube.add_quad(back_quad)
cube.add_quad(front_quad)

my_cam = Camera()

current_shape = cube


def tick():
    global current_shape
    cam.clear("black")
    if uvage.is_pressing("left arrow"):
        current_shape.position[0] -= 5
    if uvage.is_pressing("right arrow"):
        current_shape.position[0] += 5
    if uvage.is_pressing("up arrow"):
        current_shape.position[1] -= 5
    if uvage.is_pressing("down arrow"):
        current_shape.position[1] += 5
    if uvage.is_pressing("i"):
        current_shape.rotate_degrees(1, 0, 0)
    if uvage.is_pressing("j"):
        current_shape.rotate_degrees(0, 0, 1)
    if uvage.is_pressing("k"):
        current_shape.rotate_degrees(-1, 0, 0)
    if uvage.is_pressing("l"):
        current_shape.rotate_degrees(0, 0, -1)
    for i in current_shape.get_game_box_list(my_cam):
        cam.draw(i)
    #cube.rotate_degrees(1, 1, 1)
    current_shape.draw_origin(cam)
    cam.display()



uvage.timer_loop(60, tick)
