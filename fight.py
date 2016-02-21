from __future__ import print_function
import random

class WorldMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[None for x in range(self.width)] for y in range(self.height)]

    def is_occupied(self, x, y):
        ''' Checks if a given space on the map and returns True if occupied. '''
        return self.map[x][y] is not None

world = WorldMap(100, 100)

class Entity(object):
    #def __init__(self, x, y):
        #self.set_position(x, y)
        # TODO: prompt for new x & y when (x,y) is already occupied
        # PROPOSED: new __init__ below:

    def __init__(self, x, y):
       if world.is_occupied(x, y):
           print("oops, there's someone here already")
       else:
           self.set_position(x, y)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        world.map[x][y] = self

    def remove(self):
        world.map[self.x][self.y] = None

    def distance(self, other):
        return [abs(other.x-self.x), abs(other.y-self.y)]

class Character(Entity):

    def __init__(self, x, y, hp):
        Entity.__init__(self, x, y)
        self.hp = hp
        self.items = []
        self.protection = 0

    def move(self, direction):
        '''
            Moves a character one space in a given direction. Takes as input a 
            direction 'left', 'right', 'up' or 'down'. Allows wrapping of the 
            world map (eg. moving left from x = 0 moves you to x = -1)
        '''
        x, y = 0, 0

        if direction == 'left':
            x = -1
        elif direction == 'right':
            x = 1
        elif direction == 'up':
            y = 1
        elif direction == 'down':
            y = -1
        else:
            print("Please enter a valid direction: 'left', 'right', 'up', or 'down'")
            return

        new_x, new_y = ((self.x + x) % world.width), ((self.y + y) % world.height)
        if world.is_occupied(new_x, new_y):
            print('Position is occupied, try another move.')
        else:
            self.remove()
            self.set_position(x, y)
            if isinstance(self, Wizard):  # Provides a way for the wizard to regen. mana
                self.mana += 1

    def attack(self, enemy):
        damage = 10
        if self.can_attack(enemy):
            if not enemy.has_protection():
                enemy.lose_health(damage)
            else:
                enemy.lose_protection(damage)

    def power_attack(self,enemy):  # power attack
        damage = 20
        if self.can_attack(enemy):
            if not enemy.has_protection():
                enemy.lose_health(damage)
            else:
                self.lose_protection(damage)

    def can_attack(self, enemy):
        enemy_dx, enemy_dy = self.distance(enemy)
        return (enemy_dx == 1 and enemy_dy == 0)

    def gain_health(self): # gain hp....
        self.hp += 10

    def lose_health(self, reduction):
        self.hp = max(self.hp - reduction, 0)

    def gain_protection(self):   
        # its provide  a kind of protection from enemy attack
        self.protection += 4

    def lose_protection(self, reduction):
        self.protection = max(self.protection - reduction, 0)

    def has_protection(self):
        return self.protection > 0


class Enemy(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, hp)

    def challenge(self, other):
        print("Let's fight!")

class Wizard(Character):
    def __init__(self, x, y, hp, mana):
        Character.__init__(self, x, y, hp)
        self.mana = mana

    def cast_spell(self, enemy):
        if self.can_attack(self, enemy) and self.mana >= 5:
            self.mana -= 5
            for i in range(random.randint(1, 5)):
                self.attack(self, enemy)

    def heal(self, char):
        #if self.can_attack(self, enemy) and self.mana >= 5:
        if self.mana >= 5:        
            self.mana -= 5
            char.hp += 15

class Archer(Character):
    def __init__(self, x, y, hp):
        Character.__init__(self, x, y, hp)

    def range_attack(self, enemy):
        enemy_dx, enemy_dy = self.distance(enemy)
        if enemy_dx <= 5 and enemy_dy == 0:
            enemy.hp -= 5

if __name__ == "__main__":
    print("testing: " + __file__ )
    alice = Character(10,10,100)
    bob = Character(11,10,100)
    clare = Wizard(15,10,60,50)
    dan = Archer(6,10,30)
    character_list = [alice, bob, clare, dan]
    for character in character_list:
        print(character.__dict__)

