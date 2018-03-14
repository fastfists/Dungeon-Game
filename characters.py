''' Where I put all of my game classes at (Player, Zombie, Boss) '''

import classydungeon as dun

class Player:
    def __init__(self, xStart, yStart):
        self.x = xStart
        self.y = yStart
        self.health = 100
        self.isAlive = True
    
    def show(self):
        print('hello')
    
    def shoot(self):
        print("pew")
    
    def move(self,xChange=0, yChange=0):
        self.x += xChange
        self.y += yChange

    def hit(self, dmg):
        self.health -= dmg


class Monster:
    def __init__(self, room):
        self.room = room
        self.health = 50
    
    def attack(self):
        pass

    def hit(self):
        pass
    
    def patrol(self):
        pass

if __name__ == '__main__':
    boi = dun.dungeon()
    boi.make()
    boi.draw()
    print("?")
