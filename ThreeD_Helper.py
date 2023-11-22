import math
import uvage
import copy


def rotate_point_around(point_0, point_1, pitch, yaw, roll):
    cosa = math.cos(roll)
    sina = math.sin(roll)
    cosb = math.cos(yaw)
    sinb = math.sin(yaw)
    cosc = math.cos(pitch)
    sinc = math.sin(pitch)

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
    pz = azx * p10x * azy * p10y + azz * p10z

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
        self.point_list = point_list
        self.color = color

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
        if array[j].get_avg(2) <= pivot:
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
cube.add_quad(Quad([[100, 100, 100], [100, 100, -100], [100, -100, -100], [100, -100, 100]], [0, 0, 255]))
cube.add_quad(Quad([[-100, 100, 100], [-100, 100, -100], [-100, -100, -100], [-100, -100, 100]], [255, 255, 0]))
cube.add_quad(Quad([[100, 100, 100], [100, -100, 100], [-100, -100, 100], [-100, 100, 100]], [255, 0, 0]))
cube.add_quad(Quad([[100, 100, -100], [100, -100, -100], [-100, -100, -100], [-100, 100, -100]], [0, 255, 0]))
cube.add_quad(Quad([[100, 100, 100], [100, 100, -100], [-100, 100, -100], [-100, 100, 100]], [0, 255, 255]))
cube.add_quad(Quad([[100, -100, 100], [100, -100, -100], [-100, -100, -100], [-100, -100, 100]], [255, 0, 255]))

my_cam = Camera()

test_shape = Model()
test_shape.position = [500, 500, 0]
test_shape.add_quad(Quad([[50, 50, 0], [50, -50, 0], [-50, -50, 0], [-50, 50, 0]], [255, 0, 0]))
test_shape.add_quad(Quad([[50, 50, 0], [50, -50, 0], [-50, -50, -50], [-50, 50, -50]], [255, 0, 255]))
test_shape.rotate_degrees(45, 45, 45)

current_shape = cube


def tick():
    global current_shape
    cam.clear("black")
    for i in current_shape.get_game_box_list(my_cam):
        cam.draw(i)
    cube.rotate_degrees(1, 1, 1)
    current_shape.draw_origin(cam)
    cam.display()



uvage.timer_loop(30, tick)
