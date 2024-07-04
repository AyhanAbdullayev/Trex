import pygame 
from random import*

H , W = 128 , 72
tile = 10
Res = H * tile , W * tile
pygame.init()
screen = pygame.display.set_mode((Res))
pygame.display.set_caption("T-rex")
clock = pygame.time.Clock()
bg1 = pygame.image.load("images/Track.png")
bg2 = pygame.image.load("images/Track2.png")
dino = pygame.image.load("images/DinoStart.png")
walk_run = [
    pygame.image.load("images/DinoRun1.png"),
    pygame.image.load("images/DinoRun2.png"),
]
bird = [
    pygame.image.load("images/Bird1.png"),
    pygame.image.load("images/Bird2.png"),
]
cactus_type = [
    
    pygame.image.load("images/LargeCactus1.png"),
    pygame.image.load("images/LargeCactus2.png"),
    pygame.image.load("images/LargeCactus3.png"),
    pygame.image.load("images/SmallCactus1.png"),
    pygame.image.load("images/SmallCactus2.png"),
    pygame.image.load("images/SmallCactus3.png"),
    
]
die_sound = pygame.mixer.Sound("images/die.mp3")
jump_sound = pygame.mixer.Sound("images/jump2.mp3")
point_sound = pygame.mixer.Sound("images/point.mp3")
win_sound = pygame.mixer.Sound("images/win .wav")
bird_x = 1180
bird_y = 180
bg_x = 0
bg_y = 500
bg_x2 = Res[0]
is_jump = False
jump_count = 9.5
Fps = 15
dino_x = 0
dino_y = 430
cactus_x = Res[0] - 50  
bg_speed = 40
current_frame = 0
frame_counter = 0
frame_threshold = 10
current_frame_bird = 0
frame_counter_bird = 0
frame_threshold_bird = 10
enemy_cactus = {
    'large': {'x':Res[0] - 50,'y':415,'speed':30},
    'small': {'x':Res[0] - 50,'y':440,'speed':30}
}
def spawn_cactus(cactus):
    cactus['x'] -= cactus['speed']
    if cactus['x']< -cactus_type[0].get_width():
        cactus['x'] = Res[0] + randint(100,430)
def spawn_bird():
    global  bird_x,bird_y
    bird_x -= bg_speed
    if bird_x < -bird[0].get_width():
        bird_x = 1180
        bird_y =180
myfont = pygame.font.Font("images/txt.ttf",70)
def check_collision(dino_rect,cactus_rect):
    return dino_rect.colliderect(cactus_rect)
score = 0
running = True
gameplay = True
while running:
    screen.fill((255,255,255))
    score_text = myfont.render('Score:'+ str(score),False,"gray")
    bg_x -= bg_speed
    bg_x2 -= bg_speed
    keys = pygame.key.get_pressed()
    if gameplay:
        if bg_x <= -bg1.get_width():
            bg_x = Res[0]
        if bg_x2 <= -bg2.get_width():
            bg_x2 = Res[0]
        

        keys = pygame.key.get_pressed()
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
                jump_sound.play()
        else:
            if jump_count >= -9.5:
                if jump_count > 0:
                    dino_y -= (jump_count ** 2) / 2
                else:
                    dino_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9.5
        
        frame_counter += 10
        if frame_counter >= frame_threshold:
            current_frame = (current_frame + 1) % len(walk_run)
            frame_counter = 0
        frame_counter_bird += 10
        if frame_counter_bird >= frame_threshold_bird:
            current_frame_bird = (current_frame_bird + 1) % len(bird)
            frame_counter_bird = 0

        spawn_cactus(enemy_cactus['large'])
        spawn_cactus(enemy_cactus['small'])  


        screen.blit(bg1, (bg_x, bg_y))
        screen.blit(bg2, (bg_x2, bg_y))

            
        dino_rect =  pygame.Rect(dino_x,dino_y,dino.get_width(),dino.get_height())
        large_cactus_rect = pygame.Rect(enemy_cactus['large']['x'],enemy_cactus['large']['y'],
                                        cactus_type[0].get_width(),cactus_type[0].get_height())
        small_cactus_rect = pygame.Rect(enemy_cactus['small']['x'],enemy_cactus['small']['y'],
                                        cactus_type[3].get_width(),cactus_type[3].get_height())

        if dino_rect.colliderect(large_cactus_rect) or dino_rect.colliderect(small_cactus_rect):
                gameplay = False
                die_sound.play()
    
        screen.blit(walk_run[current_frame], (dino_x, dino_y))

        screen.blit(cactus_type[2], (enemy_cactus['large']['x'], enemy_cactus['large']['y']))  
        screen.blit(cactus_type[3], (enemy_cactus['small']['x'], enemy_cactus['small']['y']))  
        
        screen.blit(score_text,(0,15))
        score += 1
    else:
            gameplay = False
            screen.fill('gray')
            text_end = myfont.render("You lose",False,"red")
            try_again = myfont.render("Try Again",False,'green')
            screen.blit(text_end,(550,300))
            screen.blit(try_again,(540,370))   
            try_again_rect = try_again.get_rect(topleft=(540,370))
            mouse = pygame.mouse.get_pos()
            if try_again_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                dino_x = 0
                score = 0 
                cactus_x = Res[0] - 50   
                enemy_cactus['large']['x'] = Res[0] - 50
                enemy_cactus['small']['y'] = Res[0] - 50


        
    if score == 10000:
        gameplay = False
        screen.fill("blue")
        text = myfont.render("Tebrik eliyirem bizden domestos qazandiniz",False,'green')
        try_again = myfont.render("Try Again",False,'green')
        screen.blit(text,(200,300))
        screen.blit(try_again,(540,370))  
        try_again_rect = try_again.get_rect(topleft=(540,370))
        mouse = pygame.mouse.get_pos()
        if try_again_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            dino_x = 0
            score = 0 
            cactus_x = Res[0] - 50   
            enemy_cactus['large']['x'] = Res[0] - 50
            enemy_cactus['small']['y'] = Res[0] - 50

    pygame.display.update()
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False


    clock.tick(Fps)