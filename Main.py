import random

import pygame

pygame.init()
DISPLAY_Y_PARAM = 768
DISPLAY_X_PARAM = 1024
display = pygame.display.set_mode((DISPLAY_X_PARAM, DISPLAY_Y_PARAM))
pygame.display.set_caption("Dungeon Master III")
score = 0
# спрайт анимации персонажа
# fds
background = pygame.image.load(r'Images\Map\Background\bg.jpg')
music = pygame.mixer.music.load(r"Sounds\Music\dungeon-master.mp3")
arrowSound = pygame.mixer.Sound(r"Sounds\Arrow\strela_1.mp3")
arrowHitSound = pygame.mixer.Sound(r"Sounds\Arrow\hit.mp3")

pygame.mixer.music.play(-1)


class player_class(object):
    heroHealth = [pygame.image.load(r"Images\Hero\Health\health_0.png"),
                  pygame.image.load(r"Images\Hero\Health\health_1.png"),
                  pygame.image.load(r"Images\Hero\Health\health_2.png"),
                  pygame.image.load(r"Images\Hero\Health\health_3.png"),
                  pygame.image.load(r"Images\Hero\Health\health_4.png"),
                  pygame.image.load(r"Images\Hero\Health\health_5.png"),
                  pygame.image.load(r"Images\Hero\Health\health_6.png"),
                  pygame.image.load(r"Images\Hero\Health\health_7.png"),
                  pygame.image.load(r"Images\Hero\Health\health_8.png"),
                  pygame.image.load(r"Images\Hero\Health\health_9.png"),
                  pygame.image.load(r"Images\Hero\Health\health_10.png")]
    heroWalkRight = [pygame.image.load(r'Images\Hero\WalkRight\R1.png'),
                     pygame.image.load(r'Images\Hero\WalkRight\R2.png'),
                     pygame.image.load(r'Images\Hero\WalkRight\R3.png'),
                     pygame.image.load(r'Images\Hero\WalkRight\R4.png'),
                     pygame.image.load(r'Images\Hero\WalkRight\R5.png'),
                     pygame.image.load(r'Images\Hero\WalkRight\R6.png')]
    heroWalkLeft = [pygame.image.load(r'Images\Hero\WalkLeft\L1.png'),
                    pygame.image.load(r'Images\Hero\WalkLeft\L2.png'),
                    pygame.image.load(r'Images\Hero\WalkLeft\L3.png'),
                    pygame.image.load(r'Images\Hero\WalkLeft\L4.png'),
                    pygame.image.load(r'Images\Hero\WalkLeft\L5.png'),
                    pygame.image.load(r'Images\Hero\WalkLeft\L6.png')]
    heroLookRight = pygame.image.load(r'Images\Hero\Stand\SR_1.png')
    heroLookLeft = pygame.image.load(r'Images\Hero\Stand\SL_1.png')

    def __init__(self, x, y):
        self.x = self.s_x = x
        self.y = self.s_y = y
        self.width = self.s_width = 128
        self.height = self.s_height = 128
        self.speed = self.s_speed = 10
        self.jump_power = self.s_jump_power = 10
        self.walkCount = 0  # needed for keys in arrays of images
        self.hitbox = (self.x + 25, self.y + 18, 76, 111)
        self.health = 10
        # Состояние персонажа
        self.is_alive = True
        self.is_run = False
        self.rightDirection = True
        self.leftDirection = False
        self.is_jump = False
        self.is_sit_down = False

    def draw(self, display):
        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        if self.is_run:
            if self.rightDirection:
                display.blit(self.heroWalkRight[self.walkCount // 5], (self.x, self.y))
                self.walkCount += 1
            elif self.leftDirection:
                display.blit(self.heroWalkLeft[self.walkCount // 5], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.rightDirection:
                display.blit(self.heroLookRight, (self.x, self.y))
            if self.leftDirection:
                display.blit(self.heroLookLeft, (self.x, self.y))
        display.blit(self.heroHealth[self.health], (10, 10))
        self.hitbox = (self.x + 25, self.y + 18, 76, 111)
        # pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def run_left(self):
        self.is_run = True
        self.leftDirection = True
        self.rightDirection = False
        self.x -= self.speed

    def run_right(self):
        self.is_run = True
        self.rightDirection = True
        self.leftDirection = False
        self.x += self.speed

    def stand(self):
        self.is_run = False
        self.walkCount = 0

    def sit_down(self):
        if self.is_sit_down:
            self.is_sit_down = False
            self.height = self.s_height
            self.speed = self.s_speed
            self.y -= self.height / 2
        else:  # присел
            self.is_sit_down = True
            self.height = self.s_height / 2
            self.speed = self.s_speed / 2
            self.y += self.height
        pygame.time.delay(200)

    def pre_jump(self):
        self.is_jump = True
        self.is_run = False
        self.walkCount = 0

    def hit(self, damage):
        if self.health - damage <= 0:
            self.health = 0
            print('YOU - DIED\nGAME OVER\nWait 1 sec')
            self.is_alive = False
        else:
            self.health -= damage

    def jump(self):
        if self.jump_power > 0:  # летит вверх
            if self.y - (self.jump_power ** 2) / 2 >= 0:  # другие условия удара можно добавить!
                self.y -= (self.jump_power ** 2) / 2
                self.jump_power -= 1
            else:  # ударился в потолок
                self.y = 0  # типа стукнулся головой
                self.jump_power = 0
                # k, jump_power = jump_power, 0
        # летит вниз
        elif self.jump_power <= 0:
            if self.y + (self.jump_power ** 2) / 2 < DISPLAY_Y_PARAM - self.height - 20:
                self.y += (self.jump_power ** 2) / 2
                self.jump_power -= 1
            else:  # ударился об пол
                self.y = DISPLAY_Y_PARAM - self.height - 20  # типа стукнулся ногами
                self.is_jump = False
                self.jump_power = self.s_jump_power


class arrow_class(object):
    arrowLeftDirection = pygame.image.load(r"Images\Arrows\arrow_l.png")
    arrowRightDirection = pygame.image.load(r"Images\Arrows\arrow_r.png")

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10 * direction
        self.color = (255, 255, 255)
        self.length = 50
        self.width = 8
        self.damage = random.randint(4, 7)

    def draw(self, display):
        middle_arrow_x = self.x + self.length // 2
        middle_arrow_y = self.y + self.width // 2
        for woodman in woodmans:
            if middle_arrow_x > woodman.hitbox[0] and middle_arrow_x < woodman.hitbox[0] + woodman.hitbox[
                2] and middle_arrow_y > woodman.hitbox[1] and middle_arrow_y < woodman.hitbox[1] + woodman.hitbox[3]:
                arrowHitSound.play()
                woodman.hit(self.damage)
                arrows.pop(arrows.index(self))
        if self.x + self.speed < DISPLAY_X_PARAM and self.x - self.speed > 0:
            self.x += self.speed
        else:
            arrows.pop(arrows.index(self))
        if self.direction == 1:
            display.blit(self.arrowRightDirection, (self.x, self.y))
        else:
            display.blit(self.arrowLeftDirection, (self.x, self.y))


class Enemies(object):
    walkRight = [pygame.image.load(r"Images\Enemies\Drovosek\R1.png"),
                 pygame.image.load(r"Images\Enemies\Drovosek\R2.png"),
                 pygame.image.load(r"Images\Enemies\Drovosek\R3.png"),
                 pygame.image.load(r"Images\Enemies\Drovosek\R4.png"),
                 pygame.image.load(r"Images\Enemies\Drovosek\R5.png"),
                 pygame.image.load(r"Images\Enemies\Drovosek\R6.png")]
    walkLeft = [pygame.image.load(r"Images\Enemies\Drovosek\L1.png"),
                pygame.image.load(r"Images\Enemies\Drovosek\L2.png"),
                pygame.image.load(r"Images\Enemies\Drovosek\L3.png"),
                pygame.image.load(r"Images\Enemies\Drovosek\L4.png"),
                pygame.image.load(r"Images\Enemies\Drovosek\L5.png"),
                pygame.image.load(r"Images\Enemies\Drovosek\L6.png")]
    counter_hits = 0

    def __init__(self):
        self.width = 112
        self.height = 140
        self.x = DISPLAY_X_PARAM + self.width
        self.y = DISPLAY_Y_PARAM - self.height - 20
        self.walkCount = 0
        self.direction = -1
        self.speed = 3
        self.last_direction = 0
        self.hitbox = (self.x, self.y + 10, 90, 140)
        self.health = 10
        self.is_alive = True

    def draw(self, display):
        if self.is_alive:
            self.move()
            if self.walkCount + 1 >= 30:
                self.walkCount = 0
            if self.direction == -1:
                display.blit(self.walkLeft[self.walkCount // 5], (self.x, self.y))
                self.walkCount += 1
            elif self.direction == 1:
                display.blit(self.walkRight[self.walkCount // 5], (self.x, self.y))
                self.walkCount += 1
            else:
                self.walkCount = 0
                if self.last_direction == -1:
                    display.blit(self.walkLeft[0], (self.x, self.y))
                else:
                    display.blit(self.walkRight[0], (self.x, self.y))
            pygame.draw.rect(display, (40, 40, 40), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(display, (150, 0, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 20, self.y + 5, 70, 135)
            # pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def move(self):
        for woodman in woodmans:
            if woodman != self:
                if self.hitbox[0] - self.speed > player.hitbox[0] + player.hitbox[2]:
                    self.direction = -1
                    self.last_direction = self.direction
                elif self.hitbox[0] + self.hitbox[2] + self.speed < player.hitbox[0]:
                    self.direction = 1
                    self.last_direction = self.direction
                else:
                    self.direction = 0

        self.x += self.speed * self.direction

    def hit(self, damage):
        if self.health - damage <= 0:
            self.health = 0
            self.died()
        else:
            self.health -= damage

    def died(self):
        woodmans.pop(woodmans.index(self))
        global score
        global enemySpawnReload
        enemySpawnReload = 1
        score += 1
        self.is_alive = False


def draw_game_window():
    global run_main_while
    display.blit(background, (0, 0))  # draw background on display
    player.draw(display)  # draw player on display
    for woodman in woodmans:
        woodman.draw(display)
    for arrow in arrows:
        arrow.draw(display)
    text = font.render("Score: " + str(score), 1, (100, 200, 100))
    display.blit(text, (600, 10))
    if not (player.is_alive):
        text = font.render("YOU DIED", 1, (255, 0, 0))
        display.blit(text, (DISPLAY_X_PARAM // 2, DISPLAY_Y_PARAM // 2))
        pygame.display.update()  # update display
        pygame.time.wait(3000)
        run_main_while = False
    # использую для рисования прямоугольника
    # pygame.draw.rect(display, hero_color, (hero_x, hero_y, hero_width, hero_height))  # draw main hero
    pygame.display.update()  # update display


font = pygame.font.SysFont("comicsans", 30, True, True)
run_main_while = True
clock = pygame.time.Clock()
player = player_class(50, DISPLAY_Y_PARAM - 128 - 20)
# woodman = Enemies()
arrows = []
woodmans = []
arrowsReload = 0
enemySpawnReload = 0
# MAIN LOOP

while run_main_while:
    clock.tick(30)  # 6(кол-во картинок) * n(делитель в методе draw) = 30
    if arrowsReload > 0:
        arrowsReload += 1
    if arrowsReload == 30:
        arrowsReload = 0
    if enemySpawnReload > 0:
        enemySpawnReload += 1
    if enemySpawnReload == 50:
        enemySpawnReload = 0
    for event in pygame.event.get():
        # close game
        if event.type == pygame.QUIT:
            run_main_while = False
    if len(woodmans) < 2 and enemySpawnReload == 0:
        woodmans.append(Enemies())
        enemySpawnReload += 1
    # лист со всеми нажатами клавишами
    keys = pygame.key.get_pressed()

    if keys[pygame.K_f]:
        if len(arrows) < 5 and arrowsReload == 0:
            arrowSound.play()
            if player.rightDirection:
                direction = 1
            else:
                direction = -1
            arrows.append(arrow_class(player.x + player.width // 2, player.y + player.height // 2 - 15, direction))
            arrowsReload += 1

    if keys[pygame.K_c]:
        # приседание
        player.sit_down()

    if keys[pygame.K_a] and player.x > 1:
        # бежит влево
        player.run_left()
    elif keys[pygame.K_d] and player.x < DISPLAY_X_PARAM - player.width:
        # бежит вправо
        player.run_right()
    # придумаю что-то с лестницей
    # elif keys[pygame.K_w] and hero_y >= 0:
    #     hero_y -= hero_speed
    # elif keys[pygame.K_s] and hero_y < DISPLAY_Y_PARAM - hero_height:
    #     hero_y += hero_speed

    else:
        # стоит на месте
        player.stand()
    if player.is_jump:
        # прыжок
        player.jump()
    else:
        if keys[pygame.K_SPACE]:
            # подготовка к прыжку
            player.pre_jump()
    draw_game_window()
pygame.quit()
