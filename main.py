import pygame
import time
import random
pygame.font.init()  # to create an object font so we can display text

WIDTH, HEIGHT = 1000, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Volcano Dodge")

BACKGROUND = pygame.image.load("volcano.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND,(WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5 # how much will the player move on the x-axis
plant_image = pygame.image.load("plant.psd.png")
plant_image = pygame.transform.scale(plant_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
player = plant_image.get_rect()

DROP_WIDTH = 25
DROP_HEIGHT = 60
DROP_VELOCITY = 8
drop_flame_img = pygame.image.load("drop_flames.png")
drop_flame_img = pygame.transform.scale(drop_flame_img, (DROP_WIDTH, DROP_HEIGHT))

FONT_TIME = pygame.font.SysFont("Open Sans", 30)
FONT_LOST = pygame.font.SysFont("Open Sans",70)
FONT_PLAY_AGAIN = pygame.font.SysFont("Open Sans",70)

def draw(player, plant_image, elapsed_time, drops, drop_flame_img):
    WINDOW.blit(BACKGROUND,(0,0))

    time_text = FONT_TIME.render(f"Time: {round(elapsed_time)}seconds",1, "white")
    WINDOW.blit(time_text, (15, 15))

    WINDOW.blit(plant_image, player.topleft)

    for drop in drops:
        WINDOW.blit(drop_flame_img,drop.topleft)

    pygame.display.update()

def main():
    run = True


    player.center = (WIDTH/2, HEIGHT - PLAYER_HEIGHT)      #set the player's start position

    clock = pygame.time.Clock()
    start_time = time.time()    # time.time is the current time
    elapsed_time = 0

    drops_add_increment = 2000 # milliseconds
    drops_count = 0  # counter to know if we have to add more drops

    drops = []
    hit = False

    while run:
        clock.tick(200)                  #maximun fps the loop while can run
        elapsed_time = time.time() - start_time     # saves the time from start till the end of the game
        drops_count += clock.tick(100) #counts milliseconds from the last clock tick

        if drops_count > drops_add_increment:
            for _ in range(3):
                drop_x = random.randint(0, WIDTH - DROP_WIDTH)
                drop = drop_flame_img.get_rect()
                drop.center = (drop_x, -DROP_HEIGHT)
                drops.append(drop)

            drops_add_increment = max(200, drops_add_increment - 50) #each time the increment gets faster
            drops_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()  #assigns a list with all vailable keys ok keyboard
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VELOCITY

        for drop in drops[:]:
            drop.y += DROP_VELOCITY
            if drop.y > HEIGHT:
                drops.remove(drop)
            elif drop.y + drop.height >= player.y and drop.colliderect(player):
                drops.remove(drop)
                hit = True
                break

        if hit:

            pause = False

            lost_text = FONT_LOST.render("YOU GOT BURNED!", 1, "white")
            WINDOW.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            play_again_text = FONT_PLAY_AGAIN.render("PLAY AGAIN?",1,"white")
            WINDOW.blit(play_again_text, (WIDTH/2 - play_again_text.get_width()/2 , HEIGHT/2 -
                                          (play_again_text.get_height()/2 - lost_text.get_height())))
            pygame.display.update()

            pygame.time.delay(1000) # one sec to display button options

            #create buttons
            button_yes = pygame.Rect(WIDTH/2 - 150, HEIGHT/2 + lost_text.get_height() + play_again_text.get_height(), 80, 40)

            button_exit = pygame.Rect(WIDTH/2, HEIGHT/2 + lost_text.get_height() +
                                     play_again_text.get_height(), 80, 40)

            #display buttons
            yes_button_text = FONT_PLAY_AGAIN.render("YES",1, "white")
            exit_button_text = FONT_PLAY_AGAIN.render("EXIT", 1, "white")

            WINDOW.blit(yes_button_text,(WIDTH/2 - 150 , HEIGHT/2 + lost_text.get_height() + play_again_text.get_height() + 10))
            WINDOW.blit(exit_button_text,(WIDTH/2, HEIGHT/2 + lost_text.get_height() + play_again_text.get_height() + 10))

            pygame.display.update()

            pause = True

            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_yes.collidepoint(event.pos):
                            #play again
                            hit = False
                            player.center = (WIDTH / 2, HEIGHT - PLAYER_HEIGHT)
                            drops.clear()
                            start_time = time.time()
                            drops_add_increment = 2000
                            drops_count = 0
                            pause = False
                        elif button_exit.collidepoint(event.pos):
                            pygame.quit()

        draw(player, plant_image, elapsed_time, drops, drop_flame_img)

if __name__ == "__main__":
    main()
