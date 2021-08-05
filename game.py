import random
import pygame
pygame.init()
DISPLAY_Y_PARAM = 800
DISPLAY_X_PARAM = 1100
display = pygame.display.set_mode((DISPLAY_X_PARAM, DISPLAY_Y_PARAM))
pygame.display.set_caption("Dungeon Master III")
background = pygame.image.load(r'Images\Map\Background\bg.jpg')
music = pygame.mixer.music.load(r"Sounds\Music\dungeon-master.mp3")



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
    heroSwordsManAttackRight = [pygame.image.load(r'Images\Hero\SwordsMan\AttackRight\R1.png'),
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
        # начальное положение
        self.x = self.s_x = x
        self.y = self.s_y = y
        # ширина/высота модели
        self.width = self.s_width = 96
        self.height = self.s_height = 96
        # скорость
        self.speed = self.s_speed = 5
        # сила прыжка
        self.jump_power = self.s_jump_power = 10
        # хитбокс персонажа
        self.hitbox = (self.x, self.y, 96, 96)
        # здоровье
        self.health = 10
        # урон с меча
        self.minSwordDamage = 5
        self.maxSwordDamage = 8
        # уровень
        self.arrowsCount = 69
        self.level = 1
        self.maxLevel = 5
        self.xp = 0
        self.needed_xp = 100
        # --
        # Состояния персонажа
        # --
        self.is_alive = True
        # состояние бега
        self.is_run = False
        # триггер атаки мечом
        self.is_swordAttack = False
        # попала ли атака по противнику
        self.is_attack_hit = False
        # направление персонажа
        self.rightDirection = True
        self.leftDirection = False
        # триггер прыжка
        self.is_jump = False
        self.stand_on_enemy = False
        # состояние оружие
        self.is_archer = False
        self.is_swordsman = True
        # счетчики для анимаций
        self.walkCount = 0
        self.attackCount = 0
        # ссылка на объект класса enemies
        self.whichZombieMaybeHit = []
        self.whichZombieHit = None

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
        self.hitbox = (self.x, self.y, 96, 96)
        pygame.draw.rect(display, (255, 0, 0), self.hitbox, 2)

    def draw_attackAnimation(self, display, heroAnimation):
        if self.attackCount + 1 >= 30:
            self.attackCount = 0
            self.is_swordAttack = False
            self.is_attack_hit = False
            self.whichZombieHit = None
        if self.is_attack_hit and self.attackCount == 28:
            for zombie in zombies:
                if zombie == self.whichZombieHit:
                    zombie.hit(random.randint(self.minSwordDamage, self.maxSwordDamage))
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
                for zombie in zombies:
                    if self.hitbox[0] <= zombie.hitbox[0] and self.hitbox[0] + self.hitbox[2] + 80 >= zombie.hitbox[0]:
                        if self.hitbox[1] + self.hitbox[3] - self.height // 2 > zombie.hitbox[1] and self.hitbox[1] + self.height // 2 < zombie.hitbox[1] + zombie.hitbox[3]:
                            self.is_attack_hit = True
                            self.whichZombieHit = zombie
            elif self.leftDirection:
                for zombie in zombies:
                    if self.hitbox[0] + self.hitbox[2] >= zombie.hitbox[0] + zombie.hitbox[2] and self.hitbox[0] - 80 <= zombie.hitbox[0] + zombie.hitbox[2]:
                        if self.hitbox[1] + self.hitbox[3] - self.height // 2 > zombie.hitbox[1] and self.hitbox[1] + self.height // 2 < zombie.hitbox[1] + zombie.hitbox[3]:
                            self.is_attack_hit = True
                            self.whichZombieHit = zombie

    def bow_attack(self):
        global arrowsReload
        if self.arrowsCount != 0 and arrowsReload == 0:
            # arrowSound.play()
            if self.rightDirection:
                direction = 1
            else:
                direction = -1
            arrowList.append(arrow_class(self.x + self.width // 2 - 15, self.y + self.height // 2 - 16, direction))
            arrowsReload += 1
            self.arrowsCount -= 1

    def run_left(self):
        self.leftDirection = True
        self.rightDirection = False
        self.is_run = True
        # упор в противника
        for zombie in zombies:
            if self.hitbox[0] - self.speed < zombie.hitbox[0] + zombie.hitbox[2] and self.hitbox[0] + self.hitbox[2] > zombie.hitbox[0] + zombie.hitbox[2] and (
                    self.hitbox[1] + self.hitbox[3] > zombie.hitbox[1] and self.hitbox[1] < zombie.hitbox[1] + zombie.hitbox[3]):
                self.x = zombie.hitbox[0] + zombie.hitbox[2] + 1
                self.stand()
                return
        """
            сверяет находится ли 3 точки игрока по Х внутри хитбокса противника по Х
            сверяет крайнюю левую, правую и центральную
        """
        if self.stand_on_enemy:
            k = 0
            for zombie in zombies:
                if (zombie.hitbox[0] + zombie.hitbox[2]>self.hitbox[0]-self.speed>zombie.hitbox[0]) or(zombie.hitbox[0] + zombie.hitbox[2]>self.hitbox[0]+self.hitbox[2]-self.speed>zombie.hitbox[0]) or (zombie.hitbox[0] + zombie.hitbox[2]>self.hitbox[0]+self.hitbox[2]//2-self.speed>zombie.hitbox[0]):
                    k +=1
                    break
                # if (self.hitbox[0] + self.hitbox[2] - self.speed > zombie.hitbox[0] and self.hitbox[0] + self.hitbox[2]- self.speed < zombie.hitbox[0] + zombie.hitbox[2]) or (self.hitbox[0] - self.speed < zombie.hitbox[0] + zombie.hitbox[2] and self.hitbox[0] - self.speed> zombie.hitbox[0]):
                #     k += 1
                #     break
            if k == 0:
                self.jump_power = 0
                self.stand_on_enemy = False
                self.pre_jump()
                self.jump_down()
                self.stand()
                return
        if self.is_run or len(zombies) == 0:
            self.x -= self.speed

    def run_right(self):
        self.rightDirection = True
        self.leftDirection = False
        self.is_run = True
        for zombie in zombies:
            if self.hitbox[0] + self.hitbox[2] + self.speed > zombie.hitbox[0] and self.hitbox[0] < zombie.hitbox[
                0] and (self.hitbox[1] + self.hitbox[3] > zombie.hitbox[1] and self.hitbox[1] < zombie.hitbox[1] +
                        zombie.hitbox[3]):
                self.x = zombie.hitbox[0] - self.hitbox[3] - 1
                self.stand()
                return
        """
            сверяет находится ли 3 точки игрока по Х внутри хитбокса противника по Х
            сверяет крайнюю левую, правую и центральную
        """
        if self.stand_on_enemy:
            k = 0
            for zombie in zombies:
                if (zombie.hitbox[0] + zombie.hitbox[2]>self.hitbox[0]+ self.speed>zombie.hitbox[0]) or(zombie.hitbox[0] + zombie.hitbox[2]>self.hitbox[0]+self.hitbox[2]+ self.speed>zombie.hitbox[0]) or (zombie.hitbox[0] + zombie.hitbox[2]>self.hitbox[0]+self.hitbox[2]//2+ self.speed>zombie.hitbox[0]):
                    k +=1
                    break
                # if (self.hitbox[0] + self.hitbox[2] + self.speed > zombie.hitbox[0] and  self.hitbox[0] + self.hitbox[2] + self.speed < zombie.hitbox[0] + zombie.hitbox[2]) or (self.hitbox[0] + self.speed < zombie.hitbox[0] + zombie.hitbox[2] and self.hitbox[0] + self.speed > zombie.hitbox[0]):
                #     k += 1
                #     break
            if k == 0:
                self.jump_power = 0
                self.stand_on_enemy = False
                self.pre_jump()
                self.jump_down()
                self.stand()
                return
            k=0
        if self.is_run or len(zombies)==0:
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
            self.health -= damage

    def jump_up(self):
        if self.jump_power > 0:  # летит вверх
            for zombie in zombies:
                if (self.hitbox[1] - self.jump_power ** 2 // 2 < zombie.hitbox[1] + zombie.hitbox[3] and self.hitbox[1] - self.jump_power ** 2 // 2 > zombie.hitbox[1]) and ((self.hitbox[0] > zombie.hitbox[0] and self.hitbox[0] < zombie.hitbox[0] + zombie.hitbox[2]) or (self.hitbox[0] + self.hitbox[2] > zombie.hitbox[0] and self.hitbox[0] + self.hitbox[2] < zombie.hitbox[ 0] + zombie.hitbox[2]) or (self.hitbox[0] + self.hitbox[2]//2 > zombie.hitbox[0] and self.hitbox[0] + self.hitbox[2]//2 < zombie.hitbox[0] + zombie.hitbox[2])):
                    self.y = zombie.hitbox[1] + zombie.hitbox[3] + 1
                    self.jump_power = 0
                    self.jump_down()
                    return
            for ObjectOnMap in listObjectsOnMap:
                if (self.hitbox[1] - self.jump_power ** 2 // 2 < ObjectOnMap.hitbox[1] + ObjectOnMap.hitbox[3] and self.hitbox[1] - self.jump_power ** 2 // 2 > ObjectOnMap.hitbox[1]) and ((self.hitbox[0] > ObjectOnMap.hitbox[0] and self.hitbox[0] < ObjectOnMap.hitbox[0] + ObjectOnMap.hitbox[2]) or (self.hitbox[0] + self.hitbox[2] > ObjectOnMap.hitbox[0] and self.hitbox[0] + self.hitbox[2] < ObjectOnMap.hitbox[ 0] + ObjectOnMap.hitbox[2])or (self.hitbox[0] + self.hitbox[2]//2 > ObjectOnMap.hitbox[0] and self.hitbox[0] + self.hitbox[2]//2 < ObjectOnMap.hitbox[ 0] + ObjectOnMap.hitbox[2])):
                    self.y = ObjectOnMap.hitbox[1] + ObjectOnMap.hitbox[3] + 1
                    self.jump_power = 0
                    self.jump_down()
                    return
            if self.hitbox[1] - self.jump_power ** 2 // 2 < 0:  # другие условия удара можно добавить!
                self.y = 0  # типа стукнулся головой
                self.jump_power = 0
                self.jump_down()
                return
            else:
                self.y -= (self.jump_power ** 2) // 2
                self.jump_power -= 1  # 1
        else:
            self.jump_down()
        # летит вниз

    def jump_down(self):
        for zombie in zombies:
            if (self.hitbox[1] + self.hitbox[3] + self.jump_power ** 2 // 2 > zombie.hitbox[1] and self.hitbox[1] + self.hitbox[3] + self.jump_power ** 2 // 2 < zombie.hitbox[1] + zombie.hitbox[3]) and ((self.hitbox[0] > zombie.hitbox[0] and self.hitbox[0] < zombie.hitbox[0] + zombie.hitbox[2]) or (self.hitbox[0] + self.hitbox[2] > zombie.hitbox[0] and self.hitbox[0] + self.hitbox[2] < zombie.hitbox[0] + zombie.hitbox[2])):
                self.y = zombie.hitbox[1] - self.height - 1
                self.is_jump = False
                self.stand_on_enemy = True
                self.speed = self.s_speed
                self.jump_power = self.s_jump_power
                return
        for ObjectOnMap in listObjectsOnMap:
            if (self.hitbox[1] + self.hitbox[3] + self.jump_power ** 2 // 2 > ObjectOnMap.hitbox[1] and self.hitbox[1] + self.hitbox[3] + self.jump_power ** 2 // 2 < ObjectOnMap.hitbox[1] + ObjectOnMap.hitbox[3]) and ((self.hitbox[0] > ObjectOnMap.hitbox[0] and self.hitbox[0] < ObjectOnMap.hitbox[0] + ObjectOnMap.hitbox[2]) or (self.hitbox[0] + self.hitbox[2] > ObjectOnMap.hitbox[0] and self.hitbox[0] + self.hitbox[2] < ObjectOnMap.hitbox[0] + ObjectOnMap.hitbox[2])or (self.hitbox[0] + self.hitbox[2]//2 > ObjectOnMap.hitbox[0] and self.hitbox[0] + self.hitbox[2]//2 < ObjectOnMap.hitbox[0] + ObjectOnMap.hitbox[2])):
                self.y = ObjectOnMap.hitbox[1] - self.height - 1
                self.is_jump = False
                self.speed = self.s_speed
                self.jump_power = self.s_jump_power
                return
        # if self.hitbox[1] + self.hitbox[3] + (self.jump_power ** 2) // 2 < DISPLAY_Y_PARAM - 20:
        #     # летит вниз
        self.y += (self.jump_power ** 2) // 2
        self.jump_power -= 1
        # else:  # ударился об пол
        #     self.y = DISPLAY_Y_PARAM - self.height - 50
        #     self.is_jump = False
        #     self.speed = self.s_speed
        #     self.jump_power = self.s_jump_power

    def loot(self, xp):
        if self.level + 1 <= self.maxLevel:
            self.xp += xp
            if self.xp >= self.needed_xp:
                self.levelup()

    def levelup(self):
        self.level += 1
        if self.level == self.maxLevel:
            self.xp = self.needed_xp
        else:
            self.xp = self.xp - self.needed_xp
            self.needed_xp *= 1.2
        self.minSwordDamage += 1
        self.maxSwordDamage += 1
        if self.health + 3 > 10:
            self.health = 10
        else:
            self.health += 3
        self.arrowsCount += 5


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
        self.x = DISPLAY_X_PARAM # DISPLAY_X_PARAM + self.width
        self.y = DISPLAY_Y_PARAM - self.height - 50
        self.walkCount = 0
        self.attackCount = 0
        self.direction = -1
        self.speed = 2
        self.xp = 55
        self.last_direction = 0
        self.hitbox = (self.x + 3, self.y, 85, 96)
        self.health = 10
        self.is_alive = True
        self.is_attack = False
        self.damage = 1
        self.attack_delay = 0
        Enemies.enemiesList.append(self)

    def draw(self, display):
        if self.is_alive:
            self.move()
            if self.attack_delay + 1 >= 75:
                self.attack_delay = 0
            if self.attack_delay > 0:
                self.attack_delay += 1
            if self.is_attack and self.attack_delay == 0:
                if self.attackCount + 1 >= 40:
                    self.attackCount = 0
                    self.is_attack = False
                    self.walkCount = 0
                if self.attackCount == 38:
                    player.hit(self.damage)
                    self.attack_delay += 1
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
            pygame.draw.rect(display, (40, 40, 40), (self.hitbox[0] + 20, self.hitbox[1] - 15, 50, 10))
            pygame.draw.rect(display, (138, 3, 3), (self.hitbox[0] + 20, self.hitbox[1] - 15, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 3, self.y, 85, 96)
            # draw hitbox
            pygame.draw.rect(display, (255, 255, 0), self.hitbox, 2)

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
                        if (self.hitbox[0] + self.hitbox[2] + self.speed > woodIndex.hitbox[0]) and (self.hitbox[0] + self.hitbox[2] + self.speed < woodIndex.hitbox[0] + woodIndex.hitbox[2]):
                            self.direction = 0
            else:
                self.direction = 0
                # атакует если он по y +- рядом
                if player.hitbox[1] + player.hitbox[3] - self.height // 2 > self.hitbox[1] and player.hitbox[1] + self.height // 2 < self.hitbox[1] + self.hitbox[3]:                    self.attack()
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
        zombies.pop(zombies.index(self))
        Enemies.enemiesList.pop(Enemies.enemiesList.index(self))
        global enemySpawnReload
        enemySpawnReload = 1
        player.loot(self.xp)

class arrow_class(object):
    arrowLeftDirection = pygame.image.load(r"Images\Arrows\arrow_l.png")
    arrowRightDirection = pygame.image.load(r"Images\Arrows\arrow_r.png")
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10 * direction
        self.length = 50
        self.width = 8
        self.damage = random.randint(4, 7)

    def draw(self, display):
        middle_arrow_x = self.x + self.length // 2
        middle_arrow_y = self.y + self.width // 2
        for zombie in zombies:
            if middle_arrow_x > zombie.hitbox[0] and middle_arrow_x < zombie.hitbox[0] + zombie.hitbox[2] and middle_arrow_y > zombie.hitbox[1] and middle_arrow_y < zombie.hitbox[1] + zombie.hitbox[3]:
                # arrowHitSound.play()
                zombie.hit(self.damage)
                arrowList.pop(arrowList.index(self))
                return
        if self.x + self.speed < DISPLAY_X_PARAM and self.x - self.speed > 0:
            self.x += self.speed
        else:
            arrowList.pop(arrowList.index(self))
            return
        if self.direction == 1:
            display.blit(self.arrowRightDirection, (self.x, self.y))
        else:
            display.blit(self.arrowLeftDirection, (self.x, self.y))


class ObjectsOnMap(object):
    def __init__(self, x, y, lengthx, lengthy):
        self.x = x
        self.y = y
        self.lengthx = lengthx
        self.lengthy = lengthy
        self.hitbox = (self.x, self.y, self.lengthx, self.lengthy)

def drawObjectsOnMap(mapLevel):
    if mapLevel == 1:
        for ObjectOnMap in listObjectsOnMap:
            pygame.draw.rect(display, (200, 200, 200), (ObjectOnMap.x, ObjectOnMap.y, ObjectOnMap.lengthx, ObjectOnMap.lengthy))


def draw_game_window():
    global run_main_while
    global mapLevel
    display.blit(background, (0, 0))  # draw background on display
    # draw all zombies
    for zombie in zombies:
        zombie.draw(display)
    # draw player on display
    player.draw()
    # draw all arrows
    for arrow in arrowList:
        arrow.draw(display)

    drawObjectsOnMap(mapLevel)

    if not (player.is_alive):
        fontDie = pygame.font.SysFont("arial", 60, True, True)
        textDie = fontDie.render("YOU DIED", True, (60, 0, 0))
        display.blit(textDie, (DISPLAY_X_PARAM // 2 - 50, DISPLAY_Y_PARAM // 2))
        pygame.display.update()  # update display
        pygame.time.wait(3000)
        run_main_while = False
    draw_UI()
    pygame.display.update()

def draw_UI():
    # backgroud UI
    pygame.draw.rect(display, (35, 20, 35), (0, DISPLAY_Y_PARAM - 50, DISPLAY_X_PARAM, 50))
    # health bar
    display.blit(player.heroHealth[player.health], (15, DISPLAY_Y_PARAM - 45))
    # xp bar
    pygame.draw.rect(display, (100, 100, 100), (15, DISPLAY_Y_PARAM - 10, (DISPLAY_X_PARAM - 30), 5))
    pygame.draw.rect(display, (255, 215, 0),(15, DISPLAY_Y_PARAM - 10, (DISPLAY_X_PARAM - 30) * float(player.xp / player.needed_xp), 5))
    # text Level 1...5
    lvl = font.render("Level " + str(player.level), True, (255,215,0))
    display.blit(lvl, (DISPLAY_X_PARAM // 2 - 50, DISPLAY_Y_PARAM - 40))
    # count arrows which allowed
    if player.arrowsCount > 0:
        display.blit(font.render(str(player.arrowsCount), True, (255, 255, 255)),
                     (DISPLAY_X_PARAM - 85, DISPLAY_Y_PARAM - 38))
    else:
        display.blit(font.render(str(player.arrowsCount), True, (255, 0, 0)),
                     (DISPLAY_X_PARAM - 85, DISPLAY_Y_PARAM - 38))
    display.blit(arrow_class.arrowRightDirection, (DISPLAY_X_PARAM - 65, DISPLAY_Y_PARAM - 30))

listObjectsOnMap = []
listObjectsOnMap.append(ObjectsOnMap(0, DISPLAY_Y_PARAM - 50, DISPLAY_X_PARAM, 50))
listObjectsOnMap.append(ObjectsOnMap(0, DISPLAY_Y_PARAM - 50 - 96 - 20 - 33, 200, 50))
listObjectsOnMap.append(ObjectsOnMap(500, DISPLAY_Y_PARAM - 50 - 96 - 50 - 100, DISPLAY_X_PARAM - 500, 50))
listObjectsOnMap.append(ObjectsOnMap(800, 0, 50, 400))
mapLevel = 1




font = pygame.font.SysFont("arial", 20, True, True)
run_main_while = True
clock = pygame.time.Clock()
player = player_class(50, DISPLAY_Y_PARAM - 96 - 50)  # DISPLAY_Y_PARAM - 96 - 20
zombies = []

arrowList = []
swordReload = 0
arrowsReload = 0
enemySpawnReload = 0

# MAIN LOOP
while run_main_while:
    clock.tick(60)  # 6(кол-во картинок) * n(делитель в методе draw) = 30
    if swordReload > 0:
        swordReload += 1
    if swordReload >= 40:
        swordReload = 0

    if arrowsReload > 0:
        arrowsReload += 1
    if arrowsReload >= 40:
        arrowsReload = 0

    if enemySpawnReload > 0:
        enemySpawnReload += 1
    if enemySpawnReload == 100:
        enemySpawnReload = 0
    for event in pygame.event.get():
        # close game
        if event.type == pygame.QUIT:
            run_main_while = False
    if len(zombies) < 2 and enemySpawnReload == 0:
        zombies.append(Enemies())
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
        player.jump_up()
    else:
        if keys[pygame.K_SPACE]:
            # подготовка к прыжку
            player.pre_jump()
    draw_game_window()
pygame.quit()
