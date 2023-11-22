import uvage
import Tetris_Helper as tH

board = [[tH.blank_color for i in range(tH.board_width)] for j in range(tH.board_height)]
camera = uvage.Camera(tH.scene_width, tH.scene_height)
my_tetrimino = tH.SBlock()
fps = 30


def get_input(m_t, f_a_e_i):
    if uvage.is_pressing("a"):
        if f_a_e_i["a"] == 0:
            m_t.move_x(board, "left")
            f_a_e_i["a"] += 1
        elif f_a_e_i["a"] == 2:
            f_a_e_i["a"] = 0
        else:
            f_a_e_i["a"] += 1
    else:
        f_a_e_i["a"] = 0
    if uvage.is_pressing("d"):
        if f_a_e_i["d"] == 0:
            m_t.move_x(board, "right")
            f_a_e_i["d"] += 1
        elif f_a_e_i["d"] == 2:
            f_a_e_i["d"] = 0
        else:
            f_a_e_i["d"] += 1
    else:
        f_a_e_i["d"] = 0
    if uvage.is_pressing("s") and m_t.center_position[1] != m_t.get_ghost(board).center_position[1]:
        if f_a_e_i["s"] == 0:
            m_t.move_down(board)
            f_a_e_i["s"] += 1
        elif f_a_e_i["s"] == 2:
            f_a_e_i["s"] = 0
        else:
            f_a_e_i["s"] += 1
    else:
        f_a_e_i["s"] = 0
    if uvage.is_pressing("w"):
        if f_a_e_i["w"] == 0:
            m_t.rotate(board, "clockwise")
            f_a_e_i["w"] += 1
        elif f_a_e_i["w"] == 5:
            f_a_e_i["w"] = 0
        else:
            f_a_e_i["w"] += 1
    else:
        f_a_e_i["w"] = 0





# ---- ANIMATION TIMERS ----
animation_timer = 0
frames_between_move_down = 10
frames_after_each_input = {"a": 0, "d": 0, "w": 0, "s": 0, "space": 0}
frames_to_move_on_ground = 25
current_frames_on_ground = 0

def tick():
    global my_tetrimino
    global animation_timer
    global frames_between_move_down
    global frames_after_each_input
    global frames_to_move_on_ground
    global current_frames_on_ground

    if animation_timer == 360:
        animation_timer = 0

    get_input(my_tetrimino, frames_after_each_input)

    if uvage.is_pressing("space"):
        if frames_after_each_input["space"] == 0:
            my_tetrimino.center_position[0] = my_tetrimino.get_ghost(board).center_position[0]
            my_tetrimino.center_position[1] = my_tetrimino.get_ghost(board).center_position[1]
            my_tetrimino.add_to_board(board)
            tH.check_clear_lines(board)
            my_tetrimino = tH.get_next_tetrimino()
            frames_after_each_input["space"] += 1
        elif frames_after_each_input["space"] == 5:
            frames_after_each_input["space"] = 0
        else:
            frames_after_each_input["space"] += 1
    else:
        frames_after_each_input["space"] = 0

    if not my_tetrimino.center_position[1] == my_tetrimino.get_ghost(board).center_position[1]:
        if animation_timer % frames_between_move_down == 0:
            if not my_tetrimino.move_down(board):
                my_tetrimino = tH.get_next_tetrimino()
            animation_timer = 0
    else:
        if current_frames_on_ground < frames_to_move_on_ground:
            current_frames_on_ground += 1
        elif current_frames_on_ground == frames_to_move_on_ground:
            if not my_tetrimino.move_down(board):
                my_tetrimino = tH.get_next_tetrimino()
            current_frames_on_ground = 0

    camera.clear([0, 0, 0])
    tH.draw_board(board, my_tetrimino, camera)
    #my_tetrimino.rotate()
    camera.display()
    animation_timer += 1



uvage.timer_loop(fps, tick)
