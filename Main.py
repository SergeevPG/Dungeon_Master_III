import random

import pygame

pygame.init()
DISPLAY_Y_PARAM = 768
DISPLAY_X_PARAM = 1024
display = pygame.display.set_mode((DISPLAY_X_PARAM, DISPLAY_Y_PARAM))
pygame.display.set_caption("Dungeon Master III")
score = 0
background = pygame.image.load(r'Images\Map\Background\bg.jpg')
music = pygame.mixer.music.load(r"Sounds\Music\dungeon-master.mp3")
arrowSound = pygame.mixer.Sound(r"Sounds\Arrow\strela_1.mp3")
arrowHitSound = pygame.mixer.Sound(r"Sounds\Arrow\hit.mp3")


# pygame.mixer.music.play(-1)

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
    heroArcherRunRight = [pygame.image.load(r'Images\Hero\Archer\RunRight\R1.png'),
                          pygame.image.load(r'Images\Hero\Archer\RunRight\R2.png'),
                          pygame.image.load(r'Images\Hero\Archer\RunRight\R3.png'),
                          pygame.image.load(r'Images\Hero\Archer\RunRight\R4.png'),
                          pygame.image.load(r'Images\Hero\Archer\RunRight\R5.png')]
    heroArcherRunLeft = [pygame.image.load(r'Images\Hero\Archer\RunLeft\L1.png'),
                         pygame.image.load(r'Images\Hero\Archer\RunLeft\L2.png'),
                         pygame.image.load(r'Images\Hero\Archer\RunLeft\L3.png'),
                         pygame.image.load(r'Images\Hero\Archer\RunLeft\L4.png'),
                         pygame.image.load(r'Images\Hero\Archer\RunLeft\L5.png')]
    heroSwordsManRunRight = [pygame.image.load(r'Images\Hero\SwordsMan\RunRight\R1.png'),
                             pygame.image.load(r'Images\Hero\SwordsMan\RunRight\R2.png'),
                             pygame.image.load(r'Images\Hero\SwordsMan\RunRight\R3.png'),
                             pygame.image.load(r'Images\Hero\SwordsMan\RunRight\R4.png'),
                             pygame.image.load(r'Images\Hero\SwordsMan\RunRight\R5.png')]
    heroSwordsManRunLeft = [pygame.image.load(r'Images\Hero\SwordsMan\RunLeft\L1.png'),
                            pygame.image.load(r'Images\Hero\SwordsMan\RunLeft\L2.png'),
                            pygame.image.load(r'Images\Hero\SwordsMan\RunLeft\L3.png'),
                            pygame.image.load(r'Images\Hero\SwordsMan\RunLeft\L4.png'),
                            pygame.image.load(r'Images\Hero\SwordsMan\RunLeft\L5.png')]
    heroSwordsManAttackRight= [pygame.image.load(r'Images\Hero\SwordsMan\AttackRight\R1.png'),
                             pygame.image.load(r'Images\Hero\SwordsMan\AttackRight\R2.png'),
                             pygame.image.load(r'Images\Hero\SwordsMan\AttackRight\R3.png'),
                             pygame.image.load(r'Images\Hero\SwordsMan\AttackRight\R4.png'),
                             pygame.image.load(r'Images\Hero\SwordsMan\AttackRight\R5.png')]
    heroSwordsManAttackLeft = [pygame.image.load(r'Images\Hero\SwordsMan\AttackLeft\L1.png'),
                            pygame.image.load(r'Images\Hero\SwordsMan\AttackLeft\L2.png'),
                            pygame.image.load(r'Images\Hero\SwordsMan\AttackLeft\L3.png'),
                            pygame.image.load(r'Images\Hero\SwordsMan\AttackLeft\L4.png'),
                            pygame.image.load(r'Images\Hero\SwordsMan\AttackLeft\L5.png')]
    def __init__(self, x, y):
        self.x = self.s_x = x
        self.y = self.s_y = y
        self.width = self.s_width = 96
        self.height = self.s_height = 96
        self.speed = self.s_speed = 5
        self.jump_power = self.s_jump_power = 10
        self.walkCount = 0  # needed for keys in arrays of images
        self.attackCount = 0
        self.hitbox = (self.x, self.y, 96, 96)
        self.health = 10
        self.swordDamage = 2
        # Состояние персонажа
        self.is_attack_hit = False
        self.is_alive = True
        self.is_run = False
        self.is_swordAttack = False
        self.rightDirection = True
        self.leftDirection = False
        self.is_jump = False
        self.is_archer = True
        self.is_swordsman = False
        self.hitCounter = 0

    def draw(self):
        if self.is_archer:
            if self.rightDirection:
                self.draw_run(display, self.heroArcherRunRight)
            elif self.leftDirection:
                self.draw_run(display, self.heroArcherRunLeft)
        elif self.is_swordsman:
            if self.is_swordAttack:
                if self.rightDirection:
                    self.draw_attackAnimation(display, self.heroSwordsManAttackRight)
                elif self.leftDirection:
                    self.draw_attackAnimation(display, self.heroSwordsManAttackLeft)
            else:
                if self.rightDirection:
                    self.draw_run(display, self.heroSwordsManRunRight)
                elif self.leftDirection:
                    self.draw_run(display, self.heroSwordsManRunLeft)
        display.blit(self.heroHealth[self.health], (10, 10))
        self.hitbox = (self.x, self.y, 96, 96)
        # pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def draw_attackAnimation(self, display, heroAnimation):
        if self.attackCount + 1 >= 30:
            self.attackCount = 0
            self.is_swordAttack = False
        # if self.is_attack_hit and self.attackCount ==29:
            # woodman.hit(self.swordDamage)
        display.blit(heroAnimation[self.attackCount // 6], (self.x, self.y))
        self.attackCount += 1

    def draw_run(self, display, heroAnimation):
        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        if self.is_run:
            display.blit(heroAnimation[self.walkCount // 6], (self.x, self.y))
            self.walkCount += 1
        else:
            display.blit(heroAnimation[0], (self.x, self.y))
            self.walkCount = 0

    def sword_attack(self):
        global swordReload
        if swordReload == 0:
            swordReload += 1
            self.is_swordAttack = True
            if self.rightDirection:
                for woodman in woodmans:
                    if self.hitbox[0] + self.hitbox[2] // 2 <= woodman.hitbox[0] and self.hitbox[0] + self.hitbox[2] + 150 >= woodman.hitbox[0] + woodman.hitbox[2]:
                        if self.hitbox[1] - self.height // 2 <= woodman.hitbox[1] and self.hitbox[1] + self.hitbox[3] + self.height // 2 >= woodman.hitbox[1] + woodman.hitbox[3]:
                            self.is_attack_hit = True
                            print("sword attack")
                            woodman.hit(self.swordDamage)
            elif self.leftDirection:
                for woodman in woodmans:
                    if self.hitbox[0] + self.hitbox[2] // 2 >= woodman.hitbox[0] + woodman.hitbox[2] and self.hitbox[0] - 150 <= woodman.hitbox[0]:
                        if self.hitbox[1] - self.height // 2 <= woodman.hitbox[1] and self.hitbox[1] + self.hitbox[3] + self.height // 2 >= woodman.hitbox[1] + woodman.hitbox[3]:
                            self.is_attack_hit = True
                            print("sword attack")
                            woodman.hit(self.swordDamage)

    def bow_attack(self):
        global arrowsReload
        if len(arrows) < 3 and arrowsReload == 0:
            # arrowSound.play()
            if player.rightDirection:
                direction = 1
            else:
                direction = -1
            arrows.append(
                arrow_class(player.x + player.width // 2 - 15, player.y + player.height // 2 - 10, direction))
            arrowsReload += 1

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

    def pre_jump(self):
        self.is_jump = True
        self.speed *= 1.5
        self.is_run = False
        self.walkCount = 0

    def hit(self, damage):
        if self.health - damage <= 0:
            self.health = 0
            print('YOU - DIED\nGAME OVER\nWait 1 sec')
            self.is_alive = False
        else:
            self.hitCounter += 1
            print(self.hitCounter, "\tHIT!")
            self.health -= damage

    def jump(self):
        if self.jump_power > 0:  # летит вверх
            if self.y - (self.jump_power ** 2) / 2 >= 0:  # другие условия удара можно добавить!
                self.y -= (self.jump_power ** 2) / 2
                self.jump_power -= 0.6  # 1
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
                self.speed = self.s_speed
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
                # arrowHitSound.play()
                woodman.hit(self.damage)
                arrows.pop(arrows.index(self))
                return
        if self.x + self.speed < DISPLAY_X_PARAM and self.x - self.speed > 0:
            self.x += self.speed
        else:
            arrows.pop(arrows.index(self))
            return
        if self.direction == 1:
            display.blit(self.arrowRightDirection, (self.x, self.y))
        else:
            display.blit(self.arrowLeftDirection, (self.x, self.y))


class Enemies(object):
    runRight = [pygame.image.load(r"Images\Enemies\Zombie\Run\R1.png"),
                pygame.image.load(r"Images\Enemies\Zombie\Run\R2.png"),
                pygame.image.load(r"Images\Enemies\Zombie\Run\R3.png"),
                pygame.image.load(r"Images\Enemies\Zombie\Run\R4.png")]
    runLeft = [pygame.image.load(r"Images\Enemies\Zombie\Run\L1.png"),
               pygame.image.load(r"Images\Enemies\Zombie\Run\L2.png"),
               pygame.image.load(r"Images\Enemies\Zombie\Run\L3.png"),
               pygame.image.load(r"Images\Enemies\Zombie\Run\L4.png")]
    attackRight = [pygame.image.load(r"Images\Enemies\Zombie\Attack\attackR1.png"),
                   pygame.image.load(r"Images\Enemies\Zombie\Attack\attackR2.png"),
                   pygame.image.load(r"Images\Enemies\Zombie\Attack\attackR3.png"),
                   pygame.image.load(r"Images\Enemies\Zombie\Attack\attackR4.png")]
    attackLeft = [pygame.image.load(r"Images\Enemies\Zombie\Attack\attackL1.png"),
                  pygame.image.load(r"Images\Enemies\Zombie\Attack\attackL2.png"),
                  pygame.image.load(r"Images\Enemies\Zombie\Attack\attackL3.png"),
                  pygame.image.load(r"Images\Enemies\Zombie\Attack\attackL4.png")]
    enemiesList = []

    def __init__(self):
        self.width = 96
        self.height = 96
        self.x = DISPLAY_X_PARAM + self.width
        self.y = DISPLAY_Y_PARAM - self.height - 20
        self.walkCount = 0
        self.attackCount = 0
        self.direction = -1
        self.speed = 1
        self.last_direction = 0
        self.hitbox = (self.x + 3, self.y, 85, 96)
        self.health = 10
        self.is_alive = True
        self.is_attack = False
        self.damage = 0  # random.randint(1, 2)
        self.attack_delay = 0
        Enemies.enemiesList.append(self)

    def draw(self, display):
        if self.is_alive:
            self.move()
            if self.is_attack:
                if self.attackCount + 1 >= 40:
                    self.attackCount = 0
                    self.is_attack = False
                    self.walkCount = 0
                if self.attackCount == 38:
                    player.hit(self.damage)
                if self.last_direction == -1:
                    display.blit(self.attackLeft[self.attackCount // 10], (self.x, self.y))
                    self.attackCount += 1
                elif self.last_direction == 1:
                    display.blit(self.attackRight[self.attackCount // 10], (self.x, self.y))
                    self.attackCount += 1

            else:
                self.attackCount = 0
                if self.walkCount + 1 >= 28:
                    self.walkCount = 0
                if self.direction == -1:
                    display.blit(self.runLeft[self.walkCount // 7], (self.x, self.y))
                    self.walkCount += 1
                elif self.direction == 1:
                    display.blit(self.runRight[self.walkCount // 7], (self.x, self.y))
                    self.walkCount += 1
                else:
                    self.walkCount = 0
                    if self.last_direction == -1:
                        display.blit(self.runLeft[0], (self.x, self.y))
                    else:
                        display.blit(self.runRight[0], (self.x, self.y))
            # health bar
            pygame.draw.rect(display, (40, 40, 40), (self.hitbox[0] + 25, self.hitbox[1] - 15, 50, 10))
            pygame.draw.rect(display, (138, 3, 3),
                             (self.hitbox[0] + 25, self.hitbox[1] - 15, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 3, self.y, 85, 96)
            # draw hitbox
            # pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if len(Enemies.enemiesList) < 2:
            if self.hitbox[0] - self.speed > player.hitbox[0] + player.hitbox[2]:
                self.is_attack = False
                self.direction = -1
                self.last_direction = self.direction
            elif self.hitbox[0] + self.hitbox[2] + self.speed < player.hitbox[0]:
                self.is_attack = False
                self.direction = 1
                self.last_direction = self.direction
            else:
                self.direction = 0
        else:
            if self.hitbox[0] - self.speed > player.hitbox[0] + player.hitbox[2]:
                self.is_attack = False
                self.last_direction = self.direction = -1
                for woodIndex in Enemies.enemiesList:
                    if woodIndex != self:
                        if (self.hitbox[0] - self.speed < woodIndex.hitbox[0] + woodIndex.hitbox[2]) and (
                                self.hitbox[0] - self.speed > woodIndex.hitbox[0]):
                            self.direction = 0
            elif self.hitbox[0] + self.hitbox[2] + self.speed < player.hitbox[0]:
                self.is_attack = False
                self.last_direction = self.direction = 1
                for woodIndex in Enemies.enemiesList:
                    if woodIndex != self:
                        if (self.hitbox[0] + self.hitbox[2] + self.speed > woodIndex.hitbox[0]) and (
                                self.hitbox[0] + self.hitbox[2] + self.speed < woodIndex.hitbox[0] + woodIndex.hitbox[
                            2]):
                            self.direction = 0
            else:
                self.direction = 0
                # атакует если он по y +- рядом
                if player.hitbox[1] + player.hitbox[3] - self.height * 0.75 <= self.hitbox[1] + self.hitbox[3] and \
                        player.hitbox[1] + self.height * 0.75 >= self.hitbox[1]:
                    self.attack()
        self.x += self.speed * self.direction

    def attack(self):
        self.is_attack = True

    def hit(self, damage):
        if self.health - damage <= 0:
            self.health = 0
            self.died()
        else:
            self.health -= damage

    def died(self):
        self.is_alive = False
        woodmans.pop(woodmans.index(self))
        Enemies.enemiesList.pop(Enemies.enemiesList.index(self))
        global score
        global enemySpawnReload
        enemySpawnReload = 1
        score += 1


def draw_game_window():
    global run_main_while
    display.blit(background, (0, 0))  # draw background on display
    for woodman in woodmans:
        woodman.draw(display)
    player.draw()  # draw player on display
    for arrow in arrows:
        arrow.draw(display)
    text = font.render("Score: " + str(score), True, (100, 200, 100))
    display.blit(text, (600, 10))
    if not (player.is_alive):
        text = font.render("YOU DIED", True, (255, 0, 0))
        display.blit(text, (DISPLAY_X_PARAM // 2, DISPLAY_Y_PARAM // 2))
        pygame.display.update()  # update display
        pygame.time.wait(3000)
        run_main_while = False
    pygame.display.update()  # update display


font = pygame.font.SysFont("comicsans", 30, True, True)
run_main_while = True
clock = pygame.time.Clock()
player = player_class(50, DISPLAY_Y_PARAM - 96 - 70)
arrows = []
woodmans = []
arrowsReload = 0
swordReload = 0
enemySpawnReload = 0
# MAIN LOOP
while run_main_while:
    clock.tick(60)  # 6(кол-во картинок) * n(делитель в методе draw) = 30
    if arrowsReload > 0:
        arrowsReload += 1
    if arrowsReload >= 40:
        arrowsReload = 0
    if swordReload > 0:
        swordReload += 1
    if swordReload >= 40:
        swordReload = 0
    if enemySpawnReload > 0:
        enemySpawnReload += 1
    if enemySpawnReload == 100:
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
    if keys[pygame.K_1]:
        player.is_swordsman = True
        player.is_archer = False
    if keys[pygame.K_2]:
        player.is_archer = True
        player.is_swordsman = False
    if keys[pygame.K_f]:
        if player.is_archer:
            player.bow_attack()
        elif player.is_swordsman:
            player.sword_attack()
    if keys[pygame.K_a] and player.x > 1:
        # бежит влево
        player.run_left()
    elif keys[pygame.K_d] and player.x < DISPLAY_X_PARAM - player.width:
        # бежит вправо
        player.run_right()
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
