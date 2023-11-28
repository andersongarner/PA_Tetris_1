# +------------------------------------------------------ TETRIS ------------------------------------------------------+
# |                                By William Mason hvv9dc and Anderson Garner zyf5jh                                  |
# |                                                                                                                    |
# | We are gonna make a tetris game / CHECKPOINT 2: WE ARE MAKING A TETRIS GAME                                        |
# |                                                                                                                    |
# | We will use user input with the arrow keys to move the falling blocks                                              |
# |                                                                / CHECKPOINT 2: CHANGED TO WASD CONTROL SCHEME      |
# |                                                                                                        IMPLEMENTED |
# |         W - Rotate block clockwise                                                                                 |
# |         A - Move block left                                                                                        |
# |         S - Soft drop                                                                                              |
# |         D - Move block right                                                                                       |
# |       Tab - Hold block                                                                                             |
# |     Space - Hard drop                                                                                              |
# |                                                                                                                    |
# | Game over is when the blocks go above the screen / CHECKPOINT 2: CHANGED TO WHEN BLOCKS CANNOT BE ADDED TO SCREEN  |
# |                                                                                                       IMPLEMENTED  |
# | Our project will use graphics to display the tetris logo / CHECKPOINT 2: NOT IMPLEMENTED YET                       |
# | We will also use object-oriented programming to organize our code / CHECKPOINT 2: SEE TETRIS HELPER, FULL OF OOP   |
# |                                                                                                       IMPLEMENTED  |
# | We will do restart from game over / CHECKPOINT 2: NOT IMPLEMENTED YET                                              |
# | we will use a timer to count how long you play / CHECKPOINT 2: NOT IMPLEMENTED YET                                 |
# | we will also use a file to save highscores so no matter how many times you open it, your score will be saved!      |
# |                                                                          / CHECKPOINT 2: NOT IMPLEMENTED YET       |
# +--------------------------------------------------------------------------------------------------------------------+

import uvage
import Tetris_Helper as tH
import ThreeD_Helper as Tdh

board = [[tH.blank_color for i in range(tH.board_width)] for j in range(tH.board_height)]
camera = uvage.Camera(tH.scene_width, tH.scene_height)
my_tetrimino = tH.generate_new_tetrimino()
game_over = False
held_this_turn = False
fps = 30


def get_input(m_t, f_a_e_i):
    global held_this_turn
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
    if uvage.is_pressing("tab") and not held_this_turn:
        if f_a_e_i["tab"] == 0:
            held_this_turn = True
            m_t = tH.swap_hold_tetrimino(my_tetrimino)
            f_a_e_i["tab"] += 1
        elif f_a_e_i["tab"] == 5:
            f_a_e_i["tab"] = 0
        else:
            f_a_e_i["tab"] += 1
    else:
        f_a_e_i["tab"] = 0
    return m_t


# ---- ANIMATION TIMERS ----
animation_timer = 0
frames_between_move_down = 10
frames_after_each_input = {"a": 0, "d": 0, "w": 0, "s": 0, "space": 0, "tab": 0}
frames_to_move_on_ground = 25
current_frames_on_ground = 0
my_cam = Tdh.Camera()

current_shape = Tdh.Cube([500, 500, 500], 100)


def tick():
    global my_tetrimino
    global animation_timer
    global frames_between_move_down
    global frames_after_each_input
    global frames_to_move_on_ground
    global current_frames_on_ground
    global game_over
    global held_this_turn
    global current_shape

    if not game_over:
        if animation_timer == 360:
            animation_timer = 0

        my_tetrimino = get_input(my_tetrimino, frames_after_each_input)

        if uvage.is_pressing("space"):
            if frames_after_each_input["space"] == 0:
                my_tetrimino.center_position[0] = my_tetrimino.get_ghost(board).center_position[0]
                my_tetrimino.center_position[1] = my_tetrimino.get_ghost(board).center_position[1]
                my_tetrimino.add_to_board(board)
                tH.check_clear_lines(board)
                my_tetrimino = tH.get_next_tetrimino()
                held_this_turn = False
                game_over = my_tetrimino.check_game_over(board)
                frames_after_each_input["space"] += 1
            elif frames_after_each_input["space"] == 5:
                frames_after_each_input["space"] = 0
            else:
                frames_after_each_input["space"] += 1
        else:
            frames_after_each_input["space"] = 0

        if not my_tetrimino.center_position[1] == my_tetrimino.get_ghost(board).center_position[1]:
            if animation_timer % frames_between_move_down == 0:
                number_of_lines_cleared = my_tetrimino.move_down(board)
                if number_of_lines_cleared != -1:
                    # implement score change based on number of lines cleared
                    my_tetrimino = tH.get_next_tetrimino()
                    held_this_turn = False
                    game_over = my_tetrimino.check_game_over(board)
                animation_timer = 0
        else:
            if current_frames_on_ground < frames_to_move_on_ground:
                current_frames_on_ground += 1
            elif current_frames_on_ground == frames_to_move_on_ground:
                if not my_tetrimino.move_down(board):
                    my_tetrimino = tH.get_next_tetrimino()
                    held_this_turn = False
                    game_over = my_tetrimino.check_game_over(board)
                current_frames_on_ground = 0

        camera.clear([0, 0, 0])
        tH.draw_board(board, my_tetrimino, camera)
        current_shape.rotate_degrees(1, 1, 1)
        for i in current_shape.get_game_box_list(my_cam):
            pass
            #camera.draw(i)
        camera.display()
        animation_timer += 1


uvage.timer_loop(fps, tick)
