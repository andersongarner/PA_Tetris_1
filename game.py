# +------------------------------------------------------ TETRIS ------------------------------------------------------+
# |                                By William Mason hvv9dc and Anderson Garner zyf5jh                                  |
# |                                                                                                                    |
# | We are gonna make a tetris game / CHECKPOINT 2: WE ARE MAKING A TETRIS GAME                                        |
# |                                                                                                                    |
# | We will use user input with the arrow keys to move the falling blocks                                              |
# |                                                                / CHECKPOINT 2: CHANGED TO WASD CONTROL SCHEME      |
# |                   CONTROLS                                                                             IMPLEMENTED |
# |                    W - Rotate block clockwise                                                                      |
# |                    C - Rotate block counter-clockwise                                                              |
# |                    A - Move block left                                                                             |
# |                    S - Soft drop                                                                                   |
# |                    D - Move block right                                                                            |
# |           Left Shift - Hold block                                                                                  |
# |                Space - Hard drop                                                                                   |
# |                    R - Reset Game (When game is over)                                                              |
# |                                                                                                                    |
# |                CAMERA CONTROLS                                                                                     |
# |           Arrow Keys - Move Camera                                                                                 |
# |                 IJKL - Rotate Camera                                                                               |
# |                                                                                                                    |
# | Game over is when the blocks go above the screen / CHECKPOINT 2: CHANGED TO WHEN BLOCKS CANNOT BE ADDED TO SCREEN  |
# |                                                                                                       IMPLEMENTED  |
# | Our project will use graphics to display the tetris logo / CHECKPOINT 2: NOT IMPLEMENTED YET / 12/3/23 IMPLEMENTED |
# | We will also use object-oriented programming to organize our code / CHECKPOINT 2: SEE TETRIS HELPER, FULL OF OOP   |
# |                                                                                                       IMPLEMENTED  |
# | We will do restart from game over / CHECKPOINT 2: NOT IMPLEMENTED YET / IMPLEMENTED 11/29/23                       |
# | we will use a timer to count how long you play / CHECKPOINT 2: NOT IMPLEMENTED YET / IMPLEMENTED                   |
# | we will also use a file to save highscores so no matter how many times you open it, your score will be saved!      |
# |                                                                          / CHECKPOINT 2: NOT IMPLEMENTED YET       |
# +--------------------------------------------------------------------------------------------------------------------+
import math
import threading

import ThreeD_Helper
import uvage
import Tetris_Helper as tH
import ThreeD_Helper as Tdh
import Score
import random as r

#Global setup
board = [[tH.blank_color for i in range(tH.board_width)] for j in range(tH.board_height)]
camera = uvage.Camera(tH.scene_width, tH.scene_height)
my_tetrimino = tH.generate_new_tetrimino()
game_over = False
held_this_turn = False
t_spin_flag = False
mini_t_spin_flag = False
fps = 30
timer = 0.0
score = 0
level = 0
total_lines_cleared = 0
milestone = 10
b2b = False
combo = 0
number_of_lines_cleared = 0

# ---- DEFINE ANIMATION TIMERS ----
animation_timer = 0
frames_between_move_down = 10
frames_after_each_input = {"a": 0, "d": 0, "w": 0, "s": 0, "space": 0, "left shift": 0}
frames_to_move_on_ground = fps * 2
current_frames_on_ground = 0

current_shape = Tdh.Cube([tH.board_width * tH.block_width + tH.board_top_left_position[0] + 500, 500, 500], 100)

camera_animator = 0
direction = 1

#resets global variables
def reset_game():
    global my_tetrimino
    global animation_timer
    global frames_between_move_down
    global frames_after_each_input
    global frames_to_move_on_ground
    global current_frames_on_ground
    global game_over
    global held_this_turn
    global current_shape
    global t_spin_flag
    global mini_t_spin_flag
    global board
    global my_tetrimino
    global timer
    global total_lines_cleared
    global my_board_model
    global score
    global milestone
    global b2b
    global combo
    global number_of_lines_cleared
    global camera_animator
    global direction

    board = [[tH.blank_color for i in range(tH.board_width)] for j in range(tH.board_height + tH.board_extra_space)]
    my_tetrimino = tH.generate_new_tetrimino()

    # ---- ANIMATION TIMERS ----
    animation_timer = 0
    frames_between_move_down = 101
    frames_after_each_input = {"a": 0, "d": 0, "w": 0, "c": 0, "s": 0, "space": 0, "left shift": 0}
    frames_to_move_on_ground = 35
    current_frames_on_ground = 0

    current_shape = Tdh.Cube([tH.board_width * tH.block_width + tH.board_top_left_position[0] + 500, 500, 500], 100)

    game_over = False
    held_this_turn = False
    t_spin_flag = False
    mini_t_spin_flag = False

    timer = 0.0
    total_lines_cleared = 0
    milestone = 10
    number_of_lines_cleared = 0

    my_board_model = ThreeD_Helper.get_three_d_board(board)

    score = 0
    b2b = False
    combo = 0

    tH.hold_tetrimino = None
    tH.next_tetrimino = tH.generate_new_tetrimino()
    camera_animator = 0
    direction = 1

#easy to call to get input
def get_input(m_t, f_a_e_i):
    global held_this_turn
    global t_spin_flag
    global mini_t_spin_flag
    global current_tetrimino_model
    global my_board_model
    global score
    global level
    global total_lines_cleared
    global milestone
    global b2b
    global combo
    global number_of_lines_cleared
    global wallpaper
    global title_screen
    #each if statement uses a timer to have a gap between presses
    if uvage.is_pressing("a"):
        t_spin_flag = False
        mini_t_spin_flag = False
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
        t_spin_flag = False
        mini_t_spin_flag = False
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
        t_spin_flag = False
        mini_t_spin_flag = False
        if f_a_e_i["s"] == 0:
            x = m_t.move_down(board)
            if x > 0:
                total_lines_cleared += x
                number_of_lines_cleared = x
                if number_of_lines_cleared == 0:
                    combo = 0
                y = Score.get_guideline_scoring(number_of_lines_cleared, level, b2b, combo, t_spin_flag,
                                                mini_t_spin_flag)
                score += y[0]
                combo = y[1]
                b2b = y[2]
                mini_t_spin_flag = False
                t_spin_flag = False
                m_t = tH.get_next_tetrimino()
                current_tetrimino_model = ThreeD_Helper.get_three_d_tetrimino(my_tetrimino)
                my_board_model = ThreeD_Helper.get_three_d_board(board)
            elif x == 0:
                combo = 0
            else:
                score += 1
            f_a_e_i["s"] += 1
        elif f_a_e_i["s"] == 1:
            f_a_e_i["s"] = 0
        else:
            f_a_e_i["s"] += 1
    else:
        f_a_e_i["s"] = 0
    if uvage.is_pressing("w"):
        if f_a_e_i["w"] == 0:
            l_my = m_t.rotate(board, "clockwise")  # returns list [rotation successful, t-spin-flag, mini-t-spin-flag]
            if l_my[0]:
                for i in current_tetrimino_model:
                    i.rotate_degrees(0, 0, -90)
                t_spin_flag = l_my[1]
                mini_t_spin_flag = l_my[2]
            f_a_e_i["w"] += 1
        elif f_a_e_i["w"] == 5:
            f_a_e_i["w"] = 0
        else:
            f_a_e_i["w"] += 1
    else:
        f_a_e_i["w"] = 0
    if uvage.is_pressing("c"):
        if f_a_e_i["c"] == 0:
            l_my = m_t.rotate(board, "counter")
            if l_my[0]:
                for i in current_tetrimino_model:
                    i.rotate_degrees(0, 0, 90)
                t_spin_flag = l_my[1]
                mini_t_spin_flag = l_my[2]
            f_a_e_i["c"] += 1
        elif f_a_e_i["c"] == 5:
            f_a_e_i["c"] = 0
        else:
            f_a_e_i["c"] += 1
    if uvage.is_pressing("left shift") and not held_this_turn:
        t_spin_flag = False
        mini_t_spin_flag = False
        if f_a_e_i["left shift"] == 0:
            held_this_turn = True
            m_t = tH.swap_hold_tetrimino(my_tetrimino)
            current_tetrimino_model = ThreeD_Helper.get_three_d_tetrimino(m_t)
            f_a_e_i["left shift"] += 1
        elif f_a_e_i["left shift"] == 5:
            f_a_e_i["left shift"] = 0
        else:
            f_a_e_i["left shift"] += 1
    else:
        f_a_e_i["left shift"] = 0
    return m_t

#moves the camera
def get_camera_input(my_camera: ThreeD_Helper.Camera):
    if uvage.is_pressing("left arrow"):
        if my_camera.position[0] >= 0:
            my_camera.position[0] -= 5
    if uvage.is_pressing("up arrow"):
        if my_camera.position[1] > 0:
            my_camera.position[1] -= 5
    if uvage.is_pressing("right arrow"):
        if my_camera.position[0] < tH.scene_width:
            my_camera.position[0] += 5
    if uvage.is_pressing("down arrow"):
        if my_camera.position[1] < tH.scene_height:
            my_camera.position[1] += 5
    if uvage.is_pressing("i"):
        if my_camera.rotation[0] - camera_add[0] < math.pi / 8:
            my_camera.rotate_degrees(2, 0, 0)
    if uvage.is_pressing("j"):
        if my_camera.rotation[1] - camera_add[1] > -math.pi / 8:
            my_camera.rotate_degrees(0, -2, 0)
    if uvage.is_pressing("k"):
        if my_camera.rotation[0] - camera_add[0] > -math.pi / 8:
            my_camera.rotate_degrees(-2, 0, 0)
    if uvage.is_pressing("l"):
        if my_camera.rotation[1] - camera_add[1] < math.pi / 8:
            my_camera.rotate_degrees(0, 2, 0)
    return my_camera

#setting up objects to use
my_cam = Tdh.Camera()

reset_game()

current_tetrimino_model = ThreeD_Helper.get_three_d_tetrimino(my_tetrimino.get_copy())

my_board_model = ThreeD_Helper.get_three_d_board(board)


my_cam.position = [tH.scene_width / 2, tH.scene_height / 2, 0]

fancy_color = [0, 127, 255]

game_on = False

#creates title screen resources
image = uvage.from_image(tH.scene_width / 2, tH.scene_height / 2, "tetris-logo-small.png")
title_screen_tetrimino_model_list = []
for i in range(30):
    new_model = ThreeD_Helper.get_whole_three_d_tetrimino(tH.generate_new_tetrimino())
    new_model.position = [r.randint(my_cam.position[0] - tH.scene_width / 2, my_cam.position[0] + tH.scene_width / 2), r.randint(my_cam.position[1] - tH.scene_height / 2, my_cam.position[1] + tH.scene_height / 2), r.randint(-tH.scene_width / 2, tH.scene_width / 2)]
    new_model.rotate_degrees(r.randint(0, 359), r.randint(0, 259), r.randint(0, 359))
    title_screen_tetrimino_model_list.append(new_model)

wallpaper = uvage.from_image(tH.scene_width / 2, tH.scene_height / 2, "wallpaper.jpg")
title_screen = uvage.from_image(tH.scene_width / 2, tH.scene_height / 2, "wallpaper.png")
camera_add = [0, 0]

t_g_b = None
score_game_box = None
level_game_box = None
high_score = tH.get_high_score()

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
    global t_spin_flag
    global mini_t_spin_flag
    global timer
    global current_tetrimino_model
    global my_board_model
    global my_cam
    global score
    global level
    global total_lines_cleared
    global milestone
    global combo
    global b2b
    global fancy_color
    global number_of_lines_cleared
    global game_on
    global title_screen_tetrimino_model_list
    global camera_animator
    global direction
    global camera_add
    global t_g_b
    global score_game_box
    global level_game_box
    global high_score
    global title_screen


    if game_on is False:
        #if game on is false, game has not started yet
        #used for titlescreen
        camera.clear([0, 0, 0])
        camera.draw(title_screen)
        for i in title_screen_tetrimino_model_list:
            i.rotate_degrees(1, 1, 1)
            for j in i.get_game_box_list(my_cam):
                camera.draw(j)
        my_cam.rotate_degrees(0.25, 0.25, 0.25)

        text = uvage.from_text(tH.scene_width / 2, tH.scene_height / 2 + 300, "Press Enter to Start...", 60, [255, 255, 255])
        camera.draw(text)
        camera.draw(image)
        camera.display()
        if uvage.is_pressing("return"):
            #starts the game
            #sets some defaults
            my_cam.rotation = [0, 0, 0]
            my_cam.position = [tH.scene_width / 2 - 100, tH.scene_height / 2 + 50, 0]
            game_on = True
            camera_add = [0, 0]
            for i in range(0, 255 * 2, 1):
                #fade transition
                camera.clear([i // 15, i // 15, i // 5])
                x = uvage.from_color(tH.scene_width / 2 - 50, tH.scene_height / 2, [i // 2, i // 2, i // 2], tH.block_width * tH.board_width, tH.block_width * (tH.board_height - tH.board_extra_space))
                camera.draw(x)
                camera.display()
            my_cam.rotate_degrees(0, 0, 0)

    if not game_over and game_on:
        #at the start of each tick this rotates the board
        my_cam.rotation[0] -= camera_add[0]
        my_cam.rotation[1] -= camera_add[1]
        camera_animator += math.pi / 180
        if camera_animator == math.pi * 2:
            camera_animator = 0
        camera_add[0] = -math.sin(camera_animator / 1.5) / 4
        camera_add[1] = -math.cos(camera_animator / 1.5) / 4
        my_cam.rotation[0] += camera_add[0]
        my_cam.rotation[1] += camera_add[1]

        if frames_between_move_down <= 0:
            frames_between_move_down = 1
        fancy_color[0] += 5
        fancy_color[1] += 10
        fancy_color[2] += 15
        while fancy_color[0] > 255:
            fancy_color[0] = 0
        while fancy_color[1] > 255:
            fancy_color[1] = 0
        while fancy_color[2] > 255:
            fancy_color[2] = 0
        number_of_lines_cleared = 0
        current_tetrimino_model = ThreeD_Helper.get_three_d_tetrimino(my_tetrimino.get_copy())

        timer += 1 / fps

        if animation_timer == 360:
            animation_timer = 0

        my_tetrimino = get_input(my_tetrimino, frames_after_each_input)

        if uvage.is_pressing("space"):
            #hard drop procedure
            if frames_after_each_input["space"] == 0:
                score += int(2 * (my_tetrimino.get_ghost(board).center_position[1] - my_tetrimino.center_position[1]))
                my_tetrimino.center_position[0] = my_tetrimino.get_ghost(board).center_position[0]
                my_tetrimino.center_position[1] = my_tetrimino.get_ghost(board).center_position[1]
                my_tetrimino.add_to_board(board)
                number_of_lines_cleared = tH.check_clear_lines(board)
                if number_of_lines_cleared == 0:
                    combo = 0
                y = Score.get_guideline_scoring(number_of_lines_cleared, level, b2b, combo, t_spin_flag,
                                                    mini_t_spin_flag)
                score += y[0]
                combo = y[1]
                b2b = y[2]
                mini_t_spin_flag = False
                t_spin_flag = False
                total_lines_cleared += number_of_lines_cleared
                my_tetrimino = tH.get_next_tetrimino()
                current_tetrimino_model = ThreeD_Helper.get_three_d_tetrimino(my_tetrimino)
                my_board_model = ThreeD_Helper.get_three_d_board(board)
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
                    if number_of_lines_cleared == 0:
                        combo = 0
                    y = Score.get_guideline_scoring(number_of_lines_cleared, level, b2b, combo, t_spin_flag,
                                                        mini_t_spin_flag)
                    score += y[0]
                    combo = y[1]
                    b2b = y[2]
                    mini_t_spin_flag = False
                    t_spin_flag = False
                    # implement score change based on number of lines cleared
                    my_tetrimino = tH.get_next_tetrimino()
                    held_this_turn = False
                    game_over = my_tetrimino.check_game_over(board)
                animation_timer = 0
        else:
            if current_frames_on_ground < frames_to_move_on_ground:
                current_frames_on_ground += 1
            elif current_frames_on_ground == frames_to_move_on_ground:
                number_of_lines_cleared = my_tetrimino.move_down(board)
                if number_of_lines_cleared == 0:
                    combo = 0
                y = Score.get_guideline_scoring(number_of_lines_cleared, level, b2b, combo, t_spin_flag,
                                                mini_t_spin_flag)
                score += y[0]
                combo = y[1]
                b2b = y[2]
                mini_t_spin_flag = False
                t_spin_flag = False
                my_tetrimino = tH.get_next_tetrimino()
                current_tetrimino_model = ThreeD_Helper.get_three_d_tetrimino(my_tetrimino)
                my_board_model = ThreeD_Helper.get_three_d_board(board)
                held_this_turn = False
                game_over = my_tetrimino.check_game_over(board)
                current_frames_on_ground = 0

        camera.clear([0, 0, 0])
        camera.draw(wallpaper)
        for i in my_board_model:
            i.position = [tH.board_top_left_position[0] + tH.block_width / 2 + 600, tH.board_top_left_position[1] - 9/2 * tH.block_width, 0]

        my_cam = get_camera_input(my_cam)

        text_x_val = my_cam.position[0] - 325 + 600
        text_y_val = my_cam.position[1] - 400

        t_g_b = uvage.from_text(text_x_val, text_y_val, str("Timer: {:.2f}".format(timer)), 30, [127, 127, 127])

        score_game_box = uvage.from_text(text_x_val, text_y_val + 45, "Score: " + str(score), 30, [127, 127, 127])

        level_game_box = uvage.from_text(text_x_val, text_y_val + 90, "Level: " + str(level), 30, [127, 127, 127])

        high_score_box = uvage.from_text(my_cam.position[0] + 50, my_cam.position[1] + tH.scene_width / 2, "SCORE TO BEAT: " + str(high_score), 30, [127, 127, 127])

        left = tH.board_top_left_position[0] + 600
        right = left + tH.board_width * tH.block_width
        top = tH.board_top_left_position[1]
        bottom = top + (tH.board_height - tH.board_extra_space) * tH.block_width
        bg_top_left = [left, top, 0]
        bg_top_right = [right, top, 0]
        bg_bottom_right = [right, bottom, 0]
        bg_bottom_left = [left, bottom, 0]
        background_quad = ThreeD_Helper.Quad([bg_top_left, bg_top_right, bg_bottom_right, bg_bottom_left], [255, 255, 255])
        background_model = ThreeD_Helper.Model()
        background_model.add_quad(background_quad)
        for i in background_model.get_game_box_list(my_cam):
            camera.draw(i)

        model_x = my_tetrimino.center_position[0] * tH.block_width + tH.board_top_left_position[0] + tH.block_width / 2 + 600
        model_y = my_tetrimino.center_position[1] * tH.block_width + tH.board_top_left_position[
            1] - tH.board_extra_space * tH.block_width + tH.block_width / 2
        for i in current_tetrimino_model:
            i.position = [model_x, model_y, 0]

        #ghost model
        ghost_tetrimino = my_tetrimino.get_ghost(board)
        model_x = ghost_tetrimino.center_position[0] * tH.block_width + tH.board_top_left_position[
            0] + tH.block_width / 2 + 600
        model_y = ghost_tetrimino.center_position[1] * tH.block_width + tH.board_top_left_position[
            1] - tH.board_extra_space * tH.block_width + tH.block_width / 2
        ghost_tetrimino_model = ThreeD_Helper.get_three_d_tetrimino(ghost_tetrimino)
        for i in range(len(ghost_tetrimino_model)):
            ghost_tetrimino_model[i].position = [model_x, model_y, 0]

        #displays the correct faces based on camera pos
        #helps with performance
        if 0 <= my_cam.rotation[0] < math.pi:
            for i in my_board_model[1].get_game_box_list(my_cam):
                camera.draw(i)
            for i in ghost_tetrimino_model[1].get_game_box_list(my_cam):
                camera.draw(i)
            for i in current_tetrimino_model[1].get_game_box_list(my_cam):
                camera.draw(i)
        else:
            for i in my_board_model[3].get_game_box_list(my_cam):
                camera.draw(i)
            for i in ghost_tetrimino_model[3].get_game_box_list(my_cam):
                camera.draw(i)
            for i in current_tetrimino_model[3].get_game_box_list(my_cam):
                camera.draw(i)
        if 0 < my_cam.rotation[1] < math.pi:
            for i in my_board_model[4].get_game_box_list(my_cam):
                camera.draw(i)
            for i in ghost_tetrimino_model[4].get_game_box_list(my_cam):
                camera.draw(i)
            for i in current_tetrimino_model[4].get_game_box_list(my_cam):
                camera.draw(i)
        else:
            for i in my_board_model[2].get_game_box_list(my_cam):
                camera.draw(i)
            for i in ghost_tetrimino_model[2].get_game_box_list(my_cam):
                camera.draw(i)
            for i in current_tetrimino_model[2].get_game_box_list(my_cam):
                camera.draw(i)
        for i in my_board_model[0].get_game_box_list(my_cam):
            camera.draw(i)
        for i in ghost_tetrimino_model[0].get_game_box_list(my_cam):
            camera.draw(i)
        for i in current_tetrimino_model[0].get_game_box_list(my_cam):
            camera.draw(i)
        #draws the labels on the screen
        camera.draw(t_g_b)
        camera.draw(score_game_box)
        camera.draw(level_game_box)
        camera.draw(high_score_box)

        tH.draw_next(my_cam, camera)
        tH.draw_hold(my_cam, camera)

        if b2b:
            camera.draw(uvage.from_text(my_cam.position[0] + 200, my_cam.position[1] + 200, "Back-To-Back Bonus Active!", 30, fancy_color))

        camera.display()
        animation_timer += 1

        # increases level every ten lines
        if total_lines_cleared >= milestone:
            milestone += 10
            level += 1
            frames_between_move_down -= 10

    # if game is over
    elif game_on:
        if tH.compare_score(score, high_score):
            high_score = score
            camera.draw(uvage.from_text(tH.scene_width / 2, tH.scene_height / 2 - 100,"NEW HIGH SCORE! " + str(score), 60, [127,127, 127]))
        else:
            camera.draw(uvage.from_text(tH.scene_width / 2, tH.scene_height / 2 - 100, "YOUR SCORE: " + str(score), 60, [127, 127, 127]))

        camera.draw(uvage.from_text(tH.scene_width / 2, tH.scene_height / 2 + 100, "PRESS R TO RESTART...", 60, [127, 127, 127]))
        camera.display()

        if uvage.is_pressing("r"):
            reset_game()


uvage.timer_loop(fps, tick)
