import sys, pygame


class PLAYER:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2 - 70
        self.y = SCREEN_HEIGHT - 100

    
    def draw_player(self):
        player_rect = pygame.Rect(self.x, self.y, 135, 15)
        pygame.draw.rect(screen, (255, 255, 255), player_rect) 

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 8
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - 135:
            self.x += 8

    


class BLOCKS:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
    def draw_rect(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)


    def draw_block_rows(self):
        block_width = 50
        block_height = 20
        gap = 17
        rows = 4
        cols = SCREEN_WIDTH // (block_width + gap)

        for row in range(rows):
            for col in range(cols):
                x = col * (block_width + gap) + 18
                y = row * (block_height + gap) + 50  
                block = BLOCKS(x, y, block_width, block_height, (255, 0, 0))  
                block.draw_rect()            

    


class BALL:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT - 125
        self.ball_speed_x = 4.5
        self.ball_speed_y = 4.5
        self.player = PLAYER()
        self.lives = 3


    def reset(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT - 125
        self.ball_speed_x = 4.5
        self.ball_speed_y = 4.5

    def draw_ball(self):
        ball = pygame.Rect(0, 0, 30, 30)
        ball.center = (self.x, self.y)
        pygame.draw.ellipse(screen, (255, 255, 255), ball)

    def move_ball(self):
        self.y -= self.ball_speed_y
        self.x -= self.ball_speed_x
        if self.y <= 0:
            self.ball_speed_y = -self.ball_speed_y
        if self.y >= SCREEN_HEIGHT:
            # self.game_over()
            self.lives -= 1
            self.reset()
            self.lose()
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.ball_speed_x = -self.ball_speed_x    
    def lose(self):
        if self.lives <=0:
            self.game_over()


    def game_over(self):
        font = pygame.font.Font(None, 60)
        text = font.render('Game Over', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)
        self.reset() 




class MAIN:
    def __init__(self):
        self.player = PLAYER()
        self.blocks = self.create_blocks()
        self.ball = BALL()
    


    def won(self):
        self.blocks.clear()
        font = pygame.font.Font(None, 60)
        text = font.render('You won', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)
        sys.exit()

    def create_blocks(self):
        blocks = []
        block_width = 50
        block_height = 20
        gap = 17
        rows = 4
        cols = SCREEN_WIDTH // (block_width + gap)

        for row in range(rows):
            for col in range(cols):
                x = col * (block_width + gap) + 18
                y = row * (block_height + gap) + 50  
                block = BLOCKS(x, y, block_width, block_height, (255, 0, 0))  
                blocks.append(block)
        return blocks
    
    def check_len(self):
        len_blocks = len(self.blocks)

        if len_blocks <= 0:
            self.won()

    def draw_elements(self, window):
        window.fill((0, 0, 0))
        self.player.draw_player()
        for block in self.blocks:
            block.draw_rect()
        self.ball.draw_ball()
        pygame.display.update()

    def update(self):
        self.player.move()
        self.ball.move_ball()
        self.check_collision()
        self.check_len()
    
    def check_collision(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, 135, 15)
        ball_rect = pygame.Rect(self.ball.x - 15, self.ball.y - 15, 30, 30) 

        if player_rect.colliderect(ball_rect):
            self.ball.ball_speed_y = -self.ball.ball_speed_y  

        for block in self.blocks[:]:
            block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
            if ball_rect.colliderect(block_rect):
                self.ball.ball_speed_y = -self.ball.ball_speed_y  
                self.blocks.remove(block)

                



pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 650

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BreakOut Game')
clock = pygame.time.Clock()

FPS = 60

player = PLAYER()
main = MAIN()
ball = BALL()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    main.update()
    main.draw_elements(screen)
    clock.tick(FPS)