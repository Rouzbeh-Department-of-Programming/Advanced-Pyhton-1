
import pygame
import sys, random

pygame.init()

mainWindow = pygame.display.set_mode((500, 400))  #(width, height)

pygame.display.set_caption('flappy bird')

white = (255, 255, 255) # RGB: (red, green, blue)  # range: 0-255
black = (0, 0, 0)
red = (255, 0, 0)

clock = pygame.time.Clock()

wall_top = pygame.Rect(350, 0, 40, 120)
wall_bottom = pygame.Rect(350, 280, 40, 120)
bird = pygame.Rect(130,150,50,50)

v_wall = -6
v_bird = 5
a_bird = 1

background_img = pygame.image.load(r'photos\background.png')
background_img_resized = pygame.transform.scale(background_img, (500,400))

bird1_img = pygame.image.load(r'photos\bird1.png')
bird1_img = pygame.transform.scale(bird1_img, (50,50))

bird2_img = pygame.image.load(r'photos\bird2.png')
bird2_img = pygame.transform.scale(bird2_img, (50,50))

bird3_img = pygame.image.load(r'photos\bird3.png')
bird3_img = pygame.transform.scale(bird3_img, (50,50))

bird4_img = pygame.image.load(r'photos\bird4.png')
bird4_img = pygame.transform.scale(bird4_img, (50,50))

bird_images =[bird1_img, bird1_img, bird1_img, bird1_img,
              bird2_img, bird2_img, bird2_img, bird2_img,
              bird3_img, bird3_img, bird3_img, bird3_img,
              bird4_img, bird4_img, bird4_img, bird4_img]

wall_top_img = pygame.image.load(r'photos\wall.png')
wall_top_img = pygame.transform.scale(wall_top_img, (40,120))

wall_bottom_img = pygame.image.load(r'photos\wall.png')
wall_bottom_img = pygame.transform.scale(wall_bottom_img, (40,120))

i_bird = 0 #iterator

myfont = pygame.font.SysFont('Magento', 30)
gameover_text = myfont.render('Gameover', True, red)
score = 0
score_text = myfont.render('Score: ' + str(score), True, red)
pause_text = myfont.render('Pause', True, red)
continue_text = myfont.render('Press Space to continue ...', True, red)
replay_text = myfont.render('Press "r" to replay', True, red)

state = "start"
flag = True

score_file = open('scores.txt', 'r')
score_list = score_file.readlines()
for item in score_list:
    item.replace('\n','')
score_list_int = []
for item in score_list:
    score_list_int.append(int(item))
highest_score = max(score_list_int)
highest_score_text = myfont.render('Highest score: ' + str(highest_score), True, red)

while True:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score != 0 :
                score_file = open('scores.txt', 'a')
                score_file.write(str(score)+"\n")
                score_file.close()
            pygame.quit()
            sys.exit()
            
    mainWindow.blit(background_img_resized, (0,0)) #topleft
    mainWindow.blit(bird_images[i_bird], (bird.x, bird.y)) #topleft
    mainWindow.blit(wall_top_img, (wall_top.x, wall_top.y)) #topleft
    mainWindow.blit(wall_bottom_img, (wall_bottom.x, wall_bottom.y)) #topleft
    mainWindow.blit(score_text, (15,40))
    mainWindow.blit(highest_score_text, (15,15))

    if state == "start":
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_SPACE]:
            state="playing"
            
    if state == "playing":
        
        i_bird += 1
        if i_bird == len(bird_images):
            i_bird = 0
            
        wall_top.x += v_wall
        wall_bottom.x += v_wall
        bird.y += v_bird
        v_bird += a_bird

        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_SPACE]:
            v_bird = -7
        if keypressed[pygame.K_p]:
            state = "pause"
               
        if wall_top.x <= -40:
            wall_top.x = 500
            flag = True
            wall_bottom.x = 500
            wall_top.h = random.randint(20, 220)
            wall_bottom.h = 400 - wall_top.h - 160
            wall_bottom.y = wall_top.h + 160        
            wall_top_img = pygame.transform.scale(wall_top_img, (40,wall_top.h))
            wall_bottom_img = pygame.transform.scale(wall_bottom_img, (40,wall_bottom.h))

        if wall_top.x +40 <= bird.x and flag==True: #
            score += 1
            score_text = myfont.render('Score: ' + str(score), True, red)
            flag = False
            
        if bird.colliderect(wall_top) or bird.colliderect(wall_bottom) or bird.y>=360 or (bird.y<=0 and wall_top.x<=bird.x):
            state = "gameover"

    if state == "pause":
        mainWindow.blit(pause_text, (200, 150))
        mainWindow.blit(continue_text, (200, 200))
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_SPACE]:
            state = "playing"
                        
    if state == "gameover":
        mainWindow.blit(gameover_text, (200, 150))
        mainWindow.blit(replay_text, (200, 200))

        bird.y += 5
        if bird.y>=360:
            bird.y=360
        
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_r]:            
            wall_top = pygame.Rect(350, 0, 40, 120)
            wall_bottom = pygame.Rect(350, 280, 40, 120)
            bird = pygame.Rect(130,150,50,50)
            wall_top_img = pygame.transform.scale(wall_top_img, (40,wall_top.h))
            wall_bottom_img = pygame.transform.scale(wall_bottom_img, (40,wall_bottom.h))
            score_file = open('scores.txt', 'a')
            score_file.write(str(score)+"\n")
            score_file.close()
            score = 0
            score_text = myfont.render('Score: ' + str(score), True, red)
            state="start"            
            
    pygame.display.update()
    clock.tick(30) #fps: frame per second

