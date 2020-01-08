import pygame
import random
import sys

BLACK = (0,0,0)
BROWN = (115,66,41)
RED = (255,0,0)
ORANGE = (243,152,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
INDIGO = (16,87,121)
PURPLE = (167,87,168)
LIGHTBLUE = (36,166,213)

X = 640 #画面のx座標の大きさ
Y = 480 #画面のy座標の大きさ

pygame.init() #pygameの初期化
pygame.mixer.init()
pygame.display.set_caption("Breakout")
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()

class Ball():
    def __init__(self):
        self.set(BLACK, 0)
        pygame.mixer.music.load("collide.wav")

    def set(self, color, width):
        """ステージにより初期値の設定"""
        self.x = X/2 #ボールのx座標
        self.y = Y/2 #ボールのy座標
        self.x_speed = random.choice([-5, 5])
        self.y_speed = 5
        self.previous_x = self.x
        self.previous_y = self.y
        self.color = color
        self.width = width

    def move(self):
        """(x,y)座標に移動"""
        self.x += self.x_speed
        self.y += self.y_speed

    def draw(self):
        """(x,y)座標に半径7の円を描画"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 7, self.width)

    def collide_block(self, i, j):
        """ボールとブロックの衝突判定"""
        #ボールのx座標がブロックの幅の間にあるのとき
        if self.x > block.rect.left and self.x < block.rect.right:
            #ボールが下から来たとき
            if self.previous_y > block.rect.bottom and self.y <= block.rect.bottom:
                self.y_speed = -self.y_speed
                block.position[i][j] = "0"
                pygame.mixer.music.play(1)
            #ボールが上から来たとき
            elif self.previous_y < block.rect.top and self.y >= block.rect.top:
                self.y_speed = -self.y_speed
                block.position[i][j] = "0"
                pygame.mixer.music.play(1)
        #ボールのy座標がブロックの高さの間にあるのとき
        if self.y > block.rect.top and self.y < block.rect.bottom:
            #ボールが左から来たとき
            if self.previous_x < block.rect.left and self.x >= block.rect.left:
                self.x_speed = -self.x_speed
                block.position[i][j] = "0"
                pygame.mixer.music.play(1)
            #ボールが右から来たとき
            elif self.previous_x > block.rect.right and self.x <= block.rect.right:
                self.x_speed = -self.x_speed
                block.position[i][j] = "0"
                pygame.mixer.music.play(1)

    def save(self):
        """(x,y)座標の値を保存"""
        self.previous_x = self.x
        self.previous_y = self.y

    def collide_paddle(self):
        """ボールとパドルとの衝突判定"""
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
        """ボールと壁との衝突判定"""
        global game_state
        if self.x < 0: #左の壁
            self.x_speed = -self.x_speed
        if self.x > X: #右の壁
            self.x_speed = -self.x_speed
        if self.y < 0: #上の壁
            self.y_speed = -self.y_speed
        if self.y > Y: #下の壁
            game_state = CONTINUE


class Block():
    def __init__(self):
        self.position = None
        self.rect = None
        self.set()

    def set(self):
        """ゲーム状態により配置の設定"""
        global game_state
        if game_state == START:
            self.position = [["a","0","a","a","a","a","a","a","a","0"],
                             ["a","a","a","a","0","a","a","a","a","a"],
                             ["a","a","a","0","0","0","0","a","0","a"],
                             ["a","a","a","0","a","a","0","0","a","a"],
                             ["a","0","a","0","0","0","0","0","0","a"],
                             ["a","0","a","0","0","0","a","a","a","a"],
                             ["a","0","0","0","0","0","0","0","0","0"],
                             ["a","0","0","0","0","0","0","0","0","a"],
                             ["0","0","0","0","0","0","0","0","a","a"],
                             ["a","a","0","0","0","0","0","0","0","a"],
                             ["a","0","a","a","a","0","a","0","0","a"],
                             ["a","0","0","0","0","0","0","0","0","0"],
                             ["0","0","0","0","0","0","0","0","0","a"],
                             ["0","0","0","0","0","0","0","0","0","a"],
                             ["a","0","0","a","a","a","0","0","a","a"],
                             ["a","0","a","a","a","a","a","a","a","a"],
                             ["a","a","a","a","a","a","a","a","a","a"],
                             ["a","a","a","a","a","a","a","a","a","a"],
                             ["a","a","a","a","a","a","a","a","a","a"],
                             ["a","a","a","a","a","a","a","a","a","a"]]
        elif game_state == STAGE1:
            self.position = [["0","0","0","0","0","0","0","0","0","0"],
                             ["0","b","b","b","b","b","b","b","b","0"],
                             ["0","c","c","c","c","c","c","c","c","0"],
                             ["0","d","d","d","d","d","d","d","d","0"],
                             ["0","e","e","e","e","e","e","e","e","0"],
                             ["0","f","f","f","f","f","f","f","f","0"],
                             ["0","g","g","g","g","g","g","g","g","0"],
                             ["0","h","h","h","h","h","h","h","h","0"]]
        elif game_state == STAGE2:
            self.position = [["0","0","0","0","0","0","0","0","0","0"],
                             ["0","0","0","0","i","i","0","0","0","0"],
                             ["0","0","i","i","i","i","i","i","0","0"],
                             ["0","i","i","i","i","i","i","i","i","0"],
                             ["0","i","i","j","i","i","j","i","i","0"],
                             ["0","i","i","i","i","i","i","i","i","0"],
                             ["0","0","i","i","i","i","i","i","0","0"],
                             ["0","0","0","i","i","i","i","0","0","0"],
                             ["0","i","i","i","i","i","i","i","i","0"],
                             ["0","i","0","i","0","0","i","0","i","0"],
                             ["i","i","0","i","0","0","i","0","i","i"],
                             ["i","0","0","i","0","0","i","0","0","i"]]

    def draw(self):
        """ブロックを表示"""
        height = len(self.position)
        width = len(self.position[0])
        for i in range(height):
            for j in range(width):
                if self.position[i][j] != "0":
                    self.rect = pygame.Rect((X/10-1)*j+j, (Y/20-1)*i+i, X/10-1, Y/20-1)
                    if self.position[i][j] == "a":
                        pygame.draw.rect(screen, BROWN, self.rect)
                        edge = pygame.Rect((X/10-1)*j+j, (Y/20-1)*i+i, X/10, Y/20)
                        pygame.draw.rect(screen, BLACK, edge, 1)
                    elif self.position[i][j] == "b":
                        pygame.draw.rect(screen, RED, self.rect)
                    elif self.position[i][j] == "c":
                        pygame.draw.rect(screen, ORANGE, self.rect)
                    elif self.position[i][j] == "d":
                        pygame.draw.rect(screen, YELLOW, self.rect)
                    elif self.position[i][j] == "e":
                        pygame.draw.rect(screen, GREEN, self.rect)
                    elif self.position[i][j] == "f":
                        pygame.draw.rect(screen, BLUE, self.rect)
                    elif self.position[i][j] == "g":
                        pygame.draw.rect(screen, INDIGO, self.rect)
                    elif self.position[i][j] == "h":
                        pygame.draw.rect(screen, PURPLE, self.rect)
                    elif self.position[i][j] == "i":
                        pygame.draw.rect(screen, LIGHTBLUE, self.rect, 1)
                    elif self.position[i][j] == "j":
                        pygame.draw.rect(screen, RED, self.rect, 1)
                    #ボールが衝突したか調べる
                    ball.collide_block(i, j)
                    #ブロックが全て無くなったとき
                    self.count()
        #ボールの座標を保存
        ball.save()

    def count(self):
        """ブロックが無くなったときgame_stateを変える"""
        global game_state
        #positionを1次元にして全ての要素が"0"か調べる
        if all([i == "0" for i in sum(self.position, [])]) == True:
            if game_state == STAGE1:
                game_state = STAGE2
                ball.set(LIGHTBLUE, 1)
                self.set()
                background.set("sea")
            elif game_state == STAGE2:
                game_state = QUIT
                write.gameclear()
                pygame.display.flip()
            pygame.time.wait(1000)


class Paddle():
    def __init__(self):
        self.length = 100
        self.x = (X-self.length)/2
        self.x_speed = 0
        self.rect = None

    def move(self):
        """x方向のスピードの決定"""
        press = pygame.key.get_pressed()
        #左が押されたとき
        if press[pygame.K_LEFT]:
            self.x_speed = -20
        #右が押されたとき
        elif press[pygame.K_RIGHT]:
            self.x_speed = 20
        else:
            self.x_speed = 0
        #スピードにより座標を変化
        self.x += self.x_speed

    def collide_wall(self):
        """パドルと壁との衝突判定"""
        if self.x <= 0:
            self.x = 0
        elif self.x + self.length >= X:
            self.x = X - self.length

    def draw(self):
        """パドルの描画"""
        self.rect = pygame.Rect(self.x, Y-10, self.length, 10)
        pygame.draw.rect(screen, RED, self.rect) #パドルを生成


class Write():
    def breakout(self):
        """タイトルの文字を表示"""
        breakout_font = pygame.font.SysFont(None, 100)
        breakout = breakout_font.render("Breakout", True, RED)
        screen.blit(breakout, ((X-breakout.get_width())/2, 160))

    def start(self):
        """スタートの文字を表示"""
        start_font = pygame.font.SysFont(None, 60, italic=True)
        start = start_font.render("Press Enter to start game", True, ORANGE)
        screen.blit(start, ((X-start.get_width())/2, 280))

    def gameover(self):
        """ゲームオーバーの文字を表示"""
        gameover_font = pygame.font.SysFont(None, 100)
        gameover = gameover_font.render("GAME OVER", True, RED)
        screen.blit(gameover, ((X-gameover.get_width())/2, 100))

    def yes(self, left):
        """yesの文字を表示"""
        yes_font = pygame.font.SysFont(None, 30)
        yes_font.set_underline(left)
        yes = yes_font.render("YES", True, BLUE)
        screen.blit(yes, ((X-yes.get_width())/2-30, 300))

    def no(self, right):
        """noの文字を表示"""
        no_font = pygame.font.SysFont(None, 30)
        no_font.set_underline(right)
        no = no_font.render("NO", True, RED)
        screen.blit(no, ((X-no.get_width())/2+30, 300))

    def playagain(self):
        """PLAYAGAIN?の文字を表示"""
        playagain_font = pygame.font.SysFont(None, 60)
        playagain = playagain_font.render("PLAY AGAIN?", True, BLACK)
        screen.blit(playagain, ((X-playagain.get_width())/2, Y/2))

    def gameclear(self):
        """GAMECLEARの文字を表示"""
        gameclear_font = pygame.font.SysFont(None, 100)
        gameclear = gameclear_font.render("GAME CLEAR", True, GREEN)
        screen.blit(gameclear, ((X-gameclear.get_width())/2, Y/2))


class Background():
    def __init__(self):
        self.bg = None
        self.set("sky")

    def set(self, file_name):
        """ゲーム状態により背景の設定"""
        img = pygame.image.load("./background/{}.png".format(file_name))
        self.bg = pygame.transform.scale(img, (X, Y))

    def draw(self):
        """背景の表示"""
        rect_bg = self.bg.get_rect()
        screen.blit(self.bg, rect_bg)


class Select():
    def __init__(self):
        self.flash_count = 0
        self.left = True
        self.right = False

    def start(self):
        """スタート画面を表示"""
        global game_state
        press = pygame.key.get_pressed()
        #エンターキーが押されたとき
        if press[pygame.K_RETURN]:
            game_state = STAGE1
            block.set()
        #文字を点滅させる
        if self.flash_count % 100 < 70:
            write.start()
        self.flash_count += 1

    def quit(self):
        """ゲームを終えるか選ぶ"""
        global game_state
        #←か→が押されたとき
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            self.left = True
            self.right = False
        elif press[pygame.K_RIGHT]:
            self.left = False
            self.right = True
        #文字の表示
        write.yes(self.left)
        write.no(self.right)
        #Enterが押されたとき
        if press[pygame.K_RETURN]:
            if self.left == True:
                game_state = STAGE1
                block.set()
            else:
                game_state = QUIT


playing = True
START, STAGE1, STAGE2, CONTINUE, QUIT = (0, 1, 2, 3, 4) #ゲーム状態
game_state = START

while playing:
    ball = Ball()
    block = Block()
    paddle = Paddle()
    write = Write()
    background = Background()
    select = Select()

    while game_state == START:
        for event in pygame.event.get():
            #閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:
                game_state = QUIT

        background.draw()
        block.draw()
        write.breakout()
        select.start()

        pygame.display.flip() #画面の更新
        clock.tick(50)

    while game_state == STAGE1 or game_state == STAGE2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = QUIT

        background.draw()

        paddle.move()
        paddle.collide_wall()
        paddle.draw()

        ball.move()
        ball.draw()
        ball.collide_paddle()
        ball.collide_wall()

        block.draw()

        pygame.display.flip()
        clock.tick(50)

    while game_state == CONTINUE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = QUIT

        background.draw()
        block.draw()
        write.gameover()
        write.playagain()
        select.quit()

        pygame.display.flip()
        clock.tick(50)

    if game_state == QUIT:
        playing = False


pygame.quit()
sys.exit()