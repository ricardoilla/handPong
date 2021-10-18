import pygame
from pygame.locals import *
import random
import time
import cv2


import mediapipe as mp


import time


width = 1280
height = 720
rPos = height / 2
lPos = height / 2
Fullscreen = False



def run_tracking():
    global rPos
    global lPos
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    mpHands = mp.solutions.hands
    # Performs detection and then tracking while the confidence is enough
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()
        # print('Shape: ', img.shape)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):

                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    if id == 0:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                        if cx*2 > width/2:
                            lPos = int(cy*1.5)
                        else:
                            rPos = int(cy*1.5)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        cv2.resize(img, (width, height))
        cv2.imshow('Image', cv2.flip(img, 1))
        k = cv2.waitKey(1)
        if k == 27:  # close on ESC key
            cv2.destroyAllWindows()
            break



class Pong(object):

    def __init__(self, width, height):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Therapy Pong - version 0.1")
        self.ball_sound = pygame.mixer.Sound("sounds/ball.wav")
        self.score_sound = pygame.mixer.Sound("sounds/ring.wav")
        self.gameover_sound = pygame.mixer.Sound("sounds/game_over.wav")
        self.display_width = width
        self.display_height = height
        if Fullscreen:
            self.display = pygame.display.set_mode((self.display_width, self.display_height), FULLSCREEN) # FULLSCREEN
        else:
            self.display = pygame.display.set_mode((self.display_width, self.display_height))
        self.bg_color = (44, 62, 80)

        self.bg = pygame.image.load("images/bg.png")

        self.ball = pygame.image.load("images/ball.png")


        self.plank = pygame.image.load("images/plank.png")


        self.ball_x = random.randint(300, 340)
        self.ball_y = random.randint(0, 50)
        self.left_paddle_mv = self.right_paddle_mv = self.centery = 240
        self.ball_side = 100
        self.color = (0, 0, 0)
        self.color_1 = (0, 0, 0)
        self.color_2 = (0, 0, 0)
        self.color_3 = (0, 0, 0)
        self.direction = [1, 1]
        self.speed = 8
        self.hit_edge_left = False
        self.hit_edge_right = False
        self.paddle_height = 100
        self.paddle_width = 30
        self.info_division_height = 5
        # make height of information area 10% of window height
        self.info_area = (0.1 * self.display_height)
        self.game_area_top = self.info_area
        self.game_area_bottom = self.display_height
        # self.ball_rect = pygame.Rect(self.ball_x,self.ball_y,
        #                        self.ball,self.ball)
        self.ball_rect = self.ball.get_rect(center=(self.ball_x + self.ball_side/2, self.ball_y + self.ball_side/2))
        self.score = 0
        self.lifes = 3
        self.angle = 0
        self.incremented = False
        self.right_paddle_veloc = 0




    def play_ball_sound(self):
        # for sound effect
        self.channel = self.ball_sound.play()
        # set volume
        self.ball_sound.set_volume(0.8)

    def play_score_sound(self):
        # for sound effect
        self.channel = self.score_sound.play()
        # set volume
        self.ball_sound.set_volume(0.8)

    def play_gameover_sound(self):
        # for sound effect
        self.channel = self.gameover_sound.play()
        # set volume
        self.gameover_sound.set_volume(0.8)

    def info(self):
        ## division
        # y coordinate for division line
        self.info_division_y = self.info_area - 5
        # draw divider
        pygame.draw.rect(self.display, self.color_3,
                         (0, self.info_division_y,
                          self.display_width, self.info_division_height))

        ## printing scores 
        pygame.font.init()
        font = pygame.font.SysFont("agencyfb,tahoma", 20)
        font2 = pygame.font.SysFont("agencyfb,tahoma", 40)

        # score
        right_label = font.render("Puntaje:", 1, self.color_3)
        self.display.blit(right_label, (width//2 - 50, 3))
        left_label = font2.render("%d" % self.score, 1, self.color_3)
        self.display.blit(left_label, (width//2, 20))

        # lifes left
        right_label = font.render("Vidas Restantes:", 1, self.color_3)
        self.display.blit(right_label, (width - 200, 3))
        right_label = font2.render("%d" % self.lifes, 1, self.color_3)
        self.display.blit(right_label, (width-100, 20))

        # reset instruction
        reset_label = font.render("Presione ENTER o ESPACIO para resetear", 1, self.color_3)
        self.display.blit(reset_label, (0, 30))
        # quit instruction
        quit_label = font.render("Presione ESC para salir", 1, self.color_3)
        self.display.blit(quit_label, (0, 50))

    def fill(self):
        self.display.fill(self.bg_color)
        self.display.blit(self.bg, (0, 0))

    # Paddle at the right side
    def right_paddle(self, pos):  # set ai = 1 or anything to make ai control the paddle
        # print('Right Position: ', pos)
        self.right_paddle_mv = pos
        self.display.blit(self.plank, (self.display_width - self.paddle_width, pos))
        # for user


        # limit the posible y positons so that paddle doesn't go off window
        if self.right_paddle_mv <= self.game_area_top:
            self.right_paddle_mv = self.game_area_top
        if self.right_paddle_mv + self.paddle_height >= self.game_area_bottom:
            self.right_paddle_mv = self.game_area_bottom - self.paddle_height

        # draw right paddle as we update its y position
        # pygame.draw.rect(self.display, self.color,
        #                   (self.display_width - self.paddle_width,  # for right oaddle to be at far right of the window
        #                    self.right_paddle_mv, self.paddle_width, self.paddle_height)
        #                   )
        # self.display.blit(self.plank, (self.display_width - self.paddle_width, self.right_paddle_mv))


    # Paddle at the left side
    def left_paddle(self, pos, ai=None):  # set ai = None, if there are two human users
        # print('Left Position: ', pos)
        self.left_paddle_mv = pos
        self.display.blit(self.plank, (0, pos))


        # limit the posible y positons so that paddle doesn't go off window 
        if self.left_paddle_mv <= self.game_area_top:
            self.left_paddle_mv = self.game_area_top
        if self.left_paddle_mv + self.paddle_height >= self.game_area_bottom:
            self.left_paddle_mv = self.game_area_bottom - self.paddle_height

        # draw left paddle as we update its y position
        # pygame.draw.rect(self.display, self.color_1,
        #                   (0,  # 0 because paddle is on far left of the window
        #                    self.left_paddle_mv, self.paddle_width, self.paddle_height)
        #                   )
        # self.display.blit(self.plank, (0, self.left_paddle_mv))

    def get_right_pos(self):
        return self.right_paddle_mv

    def get_left_pos(self):
        return self.left_paddle_mv



    def update_puck(self, right_speed, left_speed):
        self.ball_x += self.speed * self.direction[0]
        self.ball_y += self.speed * self.direction[1]


        # Change direction of puck if it hits the right paddle
        if (self.ball_rect.right >= self.display_width - self.paddle_width) and (
                self.ball_rect.right <= self.display_width - 1):
            if (self.ball_rect.top <= self.right_paddle_mv + self.paddle_height) and (
                    self.ball_rect.bottom >= self.right_paddle_mv) and self.direction[0] != -1:
                self.direction[0] = -1
                self.direction[1] = self.direction[1] + right_speed
                self.play_ball_sound()
                self.score += 1
                self.incremented = False


        # If puck hits right side, change direct of puck
        # set variable for score keeping to True 
        if (self.ball_rect.right >= self.display_width) and self.direction[0] != -1:
            self.direction[0] = -1
            self.hit_edge_left = True
            self.play_score_sound()


        # Change direction of puck if it hits the left paddle
        if (self.ball_rect.left <= self.paddle_width) and (self.ball_rect.left >= 0):
            if (self.ball_rect.top <= self.left_paddle_mv + self.paddle_height) and (
                    self.ball_rect.bottom >= self.left_paddle_mv) and self.direction[0] != 1:
                self.direction[0] = 1
                self.direction[1] = self.direction[1] + left_speed
                self.play_ball_sound()
                self.score += 1
                self.incremented = False

        # If puck hits left side, change direct of puck
        # set variable for score keeping to True 
        if (self.ball_rect.left <= 0) and self.direction[0] != 1:
            self.direction[0] = 1
            self.hit_edge_right = True
            self.play_score_sound()

        # change direction of puck when it hits the top or bottom 
        # for top
        if self.ball_rect.top <= self.game_area_top and self.direction[1] != 1:
            self.direction[1] = 1
            self.play_ball_sound()
        # for bottom
        if self.ball_rect.bottom >= self.game_area_bottom and self.direction[1] != -1:
            self.direction[1] = -1
            self.play_ball_sound()

        # draw puck!
        #pygame.draw.rect(self.display, self.color_2, self.ball_rect )

        # ROTACION:
        self.ball_rotated = pygame.transform.rotozoom(self.ball, self.angle, 1)
        self.ball_rotated_rect = self.ball_rotated.get_rect(
            center=(self.ball_x + self.ball_side / 2, self.ball_y + self.ball_side / 2))

        self.ball_rect = pygame.Rect(self.ball_rotated_rect.centerx - self.ball_side/2,
                                     self.ball_rotated_rect.centery - self.ball_side/2,
                                     self.ball_side,self.ball_side)
        #pygame.draw.rect(self.display, self.color_2, self.ball_rect)
        self.display.blit(self.ball_rotated, self.ball_rotated_rect)


        if self.hit_edge_left or self.hit_edge_right:
            self.lifes -= 1
            self.hit_edge_left = False
            self.hit_edge_right = False

        self.angle += self.speed // 2
        if (self.score+1) % 10 == 0 and self.incremented == False:
            self.speed += 2
            self.incremented = True


        if self.lifes < 0:
            self.play_gameover_sound()
            self.ball_x = random.randint(300, 340)
            self.ball_y = random.randint(0, 50)
            self.left_paddle_mv = self.right_paddle_mv = random.randint(300, 340)
            self.direction = [1, 1]
            self.score = 0
            self.lifes = 3
            time.sleep(5)

        # You can uncomment these three lines to see the scores in the commandline
        # print("[STATUS]  Left has %d point(s)" %self.score[0])
        # print("[STATUS]  Right has %d point(s)" %self.score[1])
        # print("[ INFO ]  Press Space bar or Enter to reset game")

    def reset(self):
        # Initialize keyboard listener
        key = pygame.key.get_pressed()

        # On pressing Return/Enter or Escape key, reset game 
        if key[K_RETURN] or key[K_SPACE]:
            self.ball_x = random.randint(300, 340)
            self.ball_y = random.randint(0, 50)
            self.left_paddle_mv = self.right_paddle_mv = random.randint(300, 340)
            self.direction = [1, 1]
            self.score = 0
            time.sleep(1)


def run_game():
    global rPos
    global lPos
    clock = pygame.time.Clock()
    game = Pong(width, height)
    status = True
    last_r = 0
    last_l = 0


    while status:
        clock.tick(64)

        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if pressed[K_ESCAPE]:
                status = False
            if event.type == QUIT:
                status = False
        actual_r = game.get_right_pos()
        actual_l = game.get_left_pos()
        r_speed = actual_r - last_r
        l_speed = actual_l - last_l
        last_r = actual_r
        last_l = actual_l
        # print('Right paddle speed:', r_speed)
        # print('Left paddle speed:', l_speed)

        game.fill()
        game.info()
        game.right_paddle(rPos)
        game.left_paddle(lPos)
        game.update_puck(r_speed//5, l_speed//5)
        pygame.display.flip()
        game.reset()
        pygame.event.pump()
        #clock.tick(30)
    pygame.quit()