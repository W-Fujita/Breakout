import pygame
import pygame.mixer
import random

RED = (255,0,0)
ORANGE = (243,152,0)
YELLO = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
INDIGO = (16,87,121)
PURPLE = (167,87,168)
BLACK = (0,0,0)
BROWN = (115,66,41)

X = 640 #画面のx座標の大きさ
Y = 480 #画面のy座標の大きさ

pygame.init() #pygameの初期化
pygame.mixer.init()
pygame.display.set_caption("Breakout")
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()

class Ball():
    x = X/2 #ボールのx座標
    y = Y/2 #ボールのy座標
    x_speed = 0
    y_speed = 5
    previous_x = x
    previous_y = y
    pygame.mixer.music.load("collide.mp3")
    
    def __init__(self):
        direction = random.randint(0, 1)
        if direction == 0:
            self.x_speed = 5
        elif direction == 1:
            self.x_speed = -5
    
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
    
    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 7) #半径が7のボールを生成
        
    def collide_block(self, x, y):
        #ボールとブロックの衝突判定
        if self.x > block.rect.left and self.x < block.rect.right:
            if self.previous_y > block.rect.bottom and self.y <= block.rect.bottom: #ボールが下から来たとき
                block.position[x][y] = 0
                self.y_speed = -self.y_speed
                pygame.mixer.music.play(1)
            if self.previous_y < block.rect.top and self.y >= block.rect.top: #ボールが上から来たとき
                block.position[x][y] = 0
                self.y_speed = -self.y_speed
                pygame.mixer.music.play(1)
                
        if self.y > block.rect.top and self.y < block.rect.bottom:
            if self.previous_x < block.rect.left and self.x >= block.rect.left: #ボールが左から来たとき
                block.position[x][y] = 0
                self.x_speed = -self.x_speed
                pygame.mixer.music.play(1)
            if self.previous_x > block.rect.right and self.x <= block.rect.right: #ボールが右から来たとき
                block.position[x][y] = 0
                self.x_speed = -self.x_speed
                pygame.mixer.music.play(1)
                
        if (sum(block.position, [])).count(1) == 0: #positionを1次元のリストにしている
            write.gameclear()
                
    def save(self):
        self.previous_x = self.x
        self.previous_y = self.y
        
    def collide_paddle(self):
        #ボールとパドルとの衝突判定
        if self.x > paddle.rect.left and self.x < paddle.rect.right:
            if self.y >= paddle.rect.top:
                #パドルを5等分にし衝突した位置に応じてボールの反射角を変える
                if self.x - paddle.rect.left < paddle.length/5:
                    if self.x_speed > 0: #ボールが右から来たとき
                        self.x_speed = -6
                        self.y_speed = -4
                    else: #ボールが左から来たとき
                        self.x_speed = -5
                        self.y_speed = -5
                elif self.x - paddle.rect.left < 2*paddle.length/5:
                    if self.x_speed > 0:
                        self.x_speed = 5
                        self.y_speed = -5
                    else:
                        self.x_speed = -5
                        self.y_speed = -5
                elif self.x - paddle.rect.left < 3*paddle.length/5:
                    if self.x_speed > 0:
                        self.x_speed = 1
                        self.y_speed = -7
                    else:
                        self.x_speed = -1
                        self.y_speed = -7
                elif self.x - paddle.rect.left < 4*paddle.length/5:
                    if self.x_speed > 0:
                        self.x_speed = 5
                        self.y_speed = -5
                    else:
                        self.x_speed = -5
                        self.y_speed = -5
                else:
                    if self.x_speed > 0:
                        self.x_speed = 5
                        self.y_speed = -5
                    else:
                        self.x_speed = 6
                        self.y_speed = -4
                pygame.mixer.music.play(1)

    def collide_wall(self):
        global continue_screen
        #ボールと壁との衝突判定
        if self.x < 0: #左の壁
            self.x_speed = -self.x_speed
        if self.x > X: #右の壁
            self.x_speed = -self.x_speed
        if self.y < 0: #上の壁
            self.y_speed = -self.y_speed
        if self.y > Y: #下の壁
            continue_screen = True
            write.gameover()
            
            
class Block():
    rect = 0

    def __init__(self):
        self.position = [[1 for i in range(7)] for j in range(7)]
        
    def draw(self):
        for y in range(7):
            for x in range(7):
                if self.position[x][y] == 1:
                    self.rect = pygame.Rect(X/10*x+x+(X/10*3/2), Y/20*y+y+(Y/20), X/10, Y/20)
                    if y == 0:
                        pygame.draw.rect(screen, RED, self.rect)
                    elif y == 1:
                        pygame.draw.rect(screen, ORANGE, self.rect)
                    elif y == 2:
                        pygame.draw.rect(screen, YELLO, self.rect)
                    elif y == 3:
                        pygame.draw.rect(screen, GREEN, self.rect)
                    elif y == 4:
                        pygame.draw.rect(screen, BLUE, self.rect)
                    elif y == 5:
                        pygame.draw.rect(screen, INDIGO, self.rect)
                    elif y == 6:
                        pygame.draw.rect(screen, PURPLE, self.rect)

                    ball.collide_block(x, y)
        
        
class Paddle():
    length = 100
    x = (X-length)/2
    x_speed = 0
    rect = 0

    def move(self):
        press = pygame.key.get_pressed()
        #左が押されたとき
        if press[pygame.K_LEFT]:
            self.x_speed = -20
        #右が押されたとき
        elif press[pygame.K_RIGHT]:
            self.x_speed = 20
        else:
            self.x_speed = 0

        self.x += self.x_speed
    
    def collide_wall(self):
        #パドルと壁との衝突判定
        if self.x <= 0:
            self.x = 0
        elif self.x + self.length >= X:
            self.x = X - self.length
            
    def draw(self):
        self.rect = pygame.Rect(self.x, Y-10, self.length, 10)
        pygame.draw.rect(screen, RED, self.rect) #パドルを生成


class Show():
    flash_count = 0
    left = True
    right = False
    
    def background(self):
        sky = pygame.image.load("sky.jpg")
        sky = pygame.transform.scale(sky, (X, Y))
        rect_sky = sky.get_rect()
        screen.blit(sky, rect_sky)
        
    def start(self):
        global start_screen
        press = pygame.key.get_pressed()
        #エンターキーが押されたとき
        if press[pygame.K_RETURN]:
            start_screen = False
            
        if self.flash_count % 100 < 70:
            write.pressenter()
        self.flash_count += 1
        
    def brick(self):
        position = [[1,1,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,1,1,1],
                    [0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1],
                    [1,1,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,1],
                    [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1],
                    [1,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1],
                    [1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
                    [1,1,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1],
                    [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
                    [1,1,0,1,0,1,0,0,1,0,0,0,0,0,1,1,1,1,1,1],
                    [0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1]]
        for x in range(10):
            for y in range(20):
                if position[x][y] == 1:
                    brick = pygame.Rect((X/10-1)*x+x, (Y/20-1)*y+y, X/10-1, Y/20-1)
                    pygame.draw.rect(screen, BROWN, brick)
                    brick_edge = pygame.Rect((X/10-1)*x+x, (Y/20-1)*y+y, X/10, Y/20)
                    pygame.draw.rect(screen, BLACK, brick_edge, 1)

    #ゲームを再び始めるかどうか選ぶ
    def select(self):
        global play_screen
        global continue_screen
        
        yes_font = pygame.font.SysFont(None, 30)
        yes_font.set_underline(self.left)
        no_font = pygame.font.SysFont(None, 30)
        no_font.set_underline(self.right)
            
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            self.left = True
            self.right = False
        elif press[pygame.K_RIGHT]:
            self.left = False
            self.right = True
        yes = yes_font.render("YES", True, BLUE)
        screen.blit(yes, ((X-yes.get_width())/2-30, 300)) #YESの表示      
        no = no_font.render("NO", True, RED)
        screen.blit(no, ((X-no.get_width())/2+30, 300)) #NOの表示
            
        if press[pygame.K_RETURN]:
            if yes_font.get_underline():
                play_screen = True
                continue_screen = False
            else:
                continue_screen = False
        
        
class Write():
    def breakout(self):
        breakout_font = pygame.font.SysFont(None, 100)
        breakout = breakout_font.render("Breakout", True, RED)
        screen.blit(breakout, ((X-breakout.get_width())/2, 160))
        
    def pressenter(self):
        pressenter_font = pygame.font.SysFont(None, 60, italic=True)
        pressenter = pressenter_font.render("Press Enter to start game", True, ORANGE)
        screen.blit(pressenter, ((X-pressenter.get_width())/2, 280))
        
    def gameover(self):
        global play_screen
        gameover_font = pygame.font.SysFont(None, 100)
        gameover = gameover_font.render("GAME OVER", True, RED)
        screen.blit(gameover, ((X-gameover.get_width())/2, 100)) #GAMEOVERの表示
        play_screen = False
                         
    def playagain(self):
        playagain_font = pygame.font.SysFont(None, 60)
        playagain = playagain_font.render("PLAY AGAIN?", True, BLACK)
        screen.blit(playagain, ((X-playagain.get_width())/2, Y/2)) #PLAYAGAIN?の表示
        
    def gameclear(self):
        global play_screen
        global continue_screen
        gameclear_font = pygame.font.SysFont(None, 100)
        gameclear = gameclear_font.render("GAME CLEAR", True, GREEN)
        screen.blit(gameclear, ((X-gameclear.get_width())/2, Y/2)) #GAMECLEARの表示
        pygame.display.flip()
        pygame.time.wait(1000)
        play_screen = False
        continue_screen = False


playing = True
start_screen = True
play_screen = True
continue_screen = True

while playing:
    ball = Ball()
    block = Block()
    paddle = Paddle()
    show = Show()
    write = Write()
    
    while start_screen:
        for event in pygame.event.get():
            #閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:
                start_screen = False
                play_screen = False
                continue_screen = False

        show.background()
        write.breakout()
        show.start()
        show.brick()

        pygame.display.flip() #画面の更新
        clock.tick(50)

    while play_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_screen = False
                continue_screen = False

        show.background()

        ball.move()
        ball.draw()
    
        paddle.move()
        paddle.collide_wall()
        paddle.draw()

        block.draw()
        
        ball.save()
        ball.collide_paddle()
        ball.collide_wall()

        pygame.display.flip()
        clock.tick(50)

    while continue_screen:
        for event in pygame.event.get():
            #閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:
                continue_screen = False

        show.background()
        block.draw()
        write.gameover()
        write.playagain()
        show.select()

        pygame.display.flip()
        clock.tick(50)

    if start_screen == False and play_screen == False and continue_screen == False:
        playing = False
        

pygame.quit()