# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading
import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
ret, image = cap.read()
cv2.imshow('Mediapipe Feed', image)
cap.release()


import pygame

pygame.init()
pygame.mixer.music.load('assets/music/Super_Mario_Bros_Theme_Song.wav')
pygame.mixer.music.set_volume(2)
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound('assets/music/jump.wav')
jump_sound.set_volume(0.8)
duck_sound = pygame.mixer.Sound('assets/music/duck.wav')
duck_sound.set_volume(1)

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

# RUNNING = [
#     pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
#     pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
# ]
# JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
# DUCKING = [
#     pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
#     pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
# ]
RUNNING = [
    pygame.image.load(os.path.join("assets/Penguin", "run1.png")),
    pygame.image.load(os.path.join("assets/Penguin", "run2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Penguin", "jump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Penguin", "duck.png")),
    pygame.image.load(os.path.join("assets/Penguin", "duck.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

FONT_COLOR=(0,0,0)

class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, stage):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (stage == 'JUMP') and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            jump_sound.play()
            
        elif stage == 'SQUAT' and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            duck_sound.play()

        elif not (self.dino_jump or stage == 'SQUAT'):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
    
    # def update(self, userInput):
    #     if self.dino_duck:
    #         self.duck()
    #     if self.dino_run:
    #         self.run()
    #     if self.dino_jump:
    #         self.jump()

    #     if self.step_index >= 10:
    #         self.step_index = 0

    #     if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
    #         self.dino_duck = False
    #         self.dino_run = False
    #         self.dino_jump = True
    #     elif userInput[pygame.K_DOWN] and not self.dino_jump:
    #         self.dino_duck = True
    #         self.dino_run = False
    #         self.dino_jump = False
    #     elif not (self.dino_jump or userInput[pygame.K_DOWN]):
    #         self.dino_duck = False
    #         self.dino_run = True
    #         self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 250, 250]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    global squat_thres, jump_thres, ankle_thres
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0)
    web_cam_resolution = [1920, 1080]
    # Curl counter variables
    squat_cnt = 0
    jump_cnt = 0 
    stage = "STAND"

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour
        if not os.path.exists("score.txt"):
            with open("score.txt", "w") as f:
                f.write(str(0) + '\n')
            f.close()
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle 

    while run:
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, image = cap.read()
        
                # Recolor image to RGB
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
                # Make detection
                results = pose.process(image)
            
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Get coordinates
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    
                    # Calculate angle
                    angle = calculate_angle(left_hip, left_knee, left_ankle)
                    
                    # Visualize angle
                    cv2.putText(image, str(angle), 
                                tuple(np.multiply(left_knee, [web_cam_resolution[0], web_cam_resolution[1]]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    cv2.putText(image, str(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y), 
                                tuple(np.multiply(left_ankle, [web_cam_resolution[0], web_cam_resolution[1]]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    cv2.putText(image, str(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y), 
                                tuple(np.multiply(left_hip, [web_cam_resolution[0], web_cam_resolution[1]]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    # Curl counter logic
                    # squat_thres = 135
                    # jump_thres = 90
                    # ankle_thres = 0.65
                    if angle < jump_thres and landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y < ankle_thres - 0.05:
                        stage="JUMP"
                    elif angle < squat_thres and stage == "STAND" and landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y > ankle_thres + 0.1:
                        stage = "SQUAT"
                    elif angle > 170:
                        if stage == "SQUAT":
                            squat_cnt += 1
                            print("squat_cnt", squat_cnt)
                        elif stage == "JUMP":
                            jump_cnt += 1
                            print("jump_cnt", jump_cnt)
                        stage = "STAND"
      
                except:
                    pass
                
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0,0), (300,90), (245,117,16), -1)
                
                # Rep data
                cv2.putText(image, 'squat_cnt', (15,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(squat_cnt), 
                            (15,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                
                cv2.putText(image, 'jump_cnt', (110,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(jump_cnt), 
                            (110,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                
                # Stage data
                cv2.putText(image, 'STAGE', (200,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, stage, 
                            (200,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                
                
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                        )               
                
                cv2.imshow('Mediapipe Feed', image)


            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        run = False
                        paused()

                current_time = datetime.datetime.now().hour
                current_time = 8
                if 7 < current_time < 19:
                    SCREEN.fill((196, 196, 196))
                else:
                    SCREEN.fill((0, 0, 0))
                userInput = pygame.key.get_pressed()

                player.draw(SCREEN)
                # player.update(userInput)
                player.update(stage)

                if len(obstacles) == 0:
                    if random.randint(0, 2) == 0:
                        obstacles.append(SmallCactus(SMALL_CACTUS))
                    elif random.randint(0, 2) == 1:
                        obstacles.append(LargeCactus(LARGE_CACTUS))
                    elif random.randint(0, 2) == 2:
                        obstacles.append(Bird(BIRD))

                for obstacle in obstacles:
                    obstacle.draw(SCREEN)
                    obstacle.update()
                    if player.dino_rect.colliderect(obstacle.rect):
                        pygame.time.delay(2000)
                        death_count += 1
                        menu(death_count)

                background()

                cloud.draw(SCREEN)
                cloud.update()

                score()

                clock.tick(30)
                pygame.display.update()
            

            cap.release()
            cv2.destroyAllWindows()


def menu(death_count):
    global points
    global FONT_COLOR
    global squat_thres, jump_thres, ankle_thres, DIFFICULTY
    run = True
    DISPLAY_UPDATED = False
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    web_cam_resolution = [1920, 1080]
    while run:
        current_time = datetime.datetime.now().hour
        current_time = 8
        if 7 < current_time < 19:
            FONT_COLOR=(0,0,0)
            SCREEN.fill((255, 255, 255))
        else:
            FONT_COLOR=(255,255,255)
            SCREEN.fill((128, 128, 128))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            with open("score.txt", "r") as f:
                score = (
                    f.read()
                )  # Read all file in case values are not on a single line
                score_ints = [int(x) for x in score.split()]  # Convert strings to ints
            highscore = max(score_ints)  # sum all elements of the list
            hs_score_text = font.render(
                "Best Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)

            if not os.path.exists("score.txt"):
                with open("score.txt", "w") as f:
                    f.write(str(0) + '\n')
                f.close()
            with open("score.txt", "r") as f:
                score_ints = [int(x) for x in f.read().split()]  
                highscore = max(score_ints)
            f.close()
            with open("score.txt", "w") as f:
                f.write(str(highscore) + '\n')
            f.close()

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))

        # Hidden menu: choose difficulty
        if death_count == 0:
            squat_thres = 135
            jump_thres = 90
            ankle_thres = 0.6
            DIFFICULTY = 'NORMAL'
            difficulty = font.render("Difficulty: " + DIFFICULTY, True, FONT_COLOR)
            difficultyRect = difficulty.get_rect()
            difficultyRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
            SCREEN.blit(difficulty, difficultyRect)
        if DISPLAY_UPDATED == False:
            pygame.display.update()
            DISPLAY_UPDATED = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                
                if event.key == pygame.K_UP:
                    if DIFFICULTY == 'NORMAL':
                        squat_thres = 130
                        jump_thres = 80
                        DIFFICULTY = 'HARD'
                    elif DIFFICULTY == 'EASY':
                        squat_thres = 135
                        jump_thres = 90
                        DIFFICULTY = 'NORMAL'
                    difficulty = font.render("Choose Difficulty: " + DIFFICULTY, True, FONT_COLOR)
                    difficultyRect = difficulty.get_rect()
                    difficultyRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
                    SCREEN.blit(difficulty, difficultyRect)
                    pygame.display.update()
                    DISPLAY_UPDATED = True
                elif event.key == pygame.K_DOWN:
                    if DIFFICULTY == 'NORMAL':
                        squat_thres = 140
                        jump_thres = 110
                        DIFFICULTY = 'EASY'
                    elif DIFFICULTY == 'HARD':
                        squat_thres = 135
                        jump_thres = 90
                        DIFFICULTY = 'NORMAL'
                    difficulty = font.render("Choose Difficulty: " + DIFFICULTY, True, FONT_COLOR)
                    difficultyRect = difficulty.get_rect()
                    difficultyRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
                    SCREEN.blit(difficulty, difficultyRect)
                    pygame.display.update()
                    DISPLAY_UPDATED = True
                else:
                    # make sure the distance is enough for capturing whole body
                    waiting = font.render("Legs not detected, please move back...", True, (178, 34, 34))
                    waitingRect = waiting.get_rect()
                    waitingRect.center = (SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2 + 260)
                    SCREEN.blit(waiting, waitingRect)
                    pygame.display.update()

                    cap = cv2.VideoCapture(0)
                    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                        while cap.isOpened():
                            ret, image = cap.read()
                    
                            # Recolor image to RGB
                            image.flags.writeable = False
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                            # Make detection
                            results = pose.process(image)
                        
                            # Recolor back to BGR
                            image.flags.writeable = True
                            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                            
                            # Extract landmarks
                            try:
                                landmarks = results.pose_landmarks.landmark
                                
                                # Get coordinates
                                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                                
                                
                                # Visualize visibility
                                cv2.putText(image, str(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility), 
                                            tuple(np.multiply(left_knee, [web_cam_resolution[0], web_cam_resolution[1]]).astype(int)), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA
                                                    )
                                
                                cv2.putText(image, str(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].visibility), 
                                            tuple(np.multiply(left_ankle, [web_cam_resolution[0], web_cam_resolution[1]]).astype(int)), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA
                                                    )
                                
                                cv2.putText(image, str(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility), 
                                            tuple(np.multiply(left_hip, [web_cam_resolution[0], web_cam_resolution[1]]).astype(int)), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA
                                                    )
                                
                                start_condition1 = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility > 0.9
                                start_condition2 = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].visibility > 0.9
                                start_condition3 = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility > 0.9
                                # print('#####################', start_condition1, '#####################')
                                # print('#####################', start_condition2, '#####################')
                                # print('#####################', start_condition3, '#####################')
                                if start_condition1 and start_condition2 and start_condition3:
                                    cap.release()
                                    break
                
                            except:
                                pass
                            
                            print('Capturing distance!!!!')

                    
                    main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
