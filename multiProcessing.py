import multiprocessing
import classydungeon as new
import random
import time
import dungeon_with_res as old

def make_new(seed, rooms):
    x = new.Dungeon(resolution=(20,20), roomCount=rooms, seed=seed)
    x.make()
    x.draw()

def make_old(seed, rooms):
    old.setup(seed, 20, rooms)

if __name__ == "__main__":
    for i in range(8):
        seed = random.randint(0, 67280421310721)
        rooms = random.randint(15, 25)
        p = multiprocessing.Process(target=make_new, args=(seed,rooms))
        pp = multiprocessing.Process(target=make_old, args=(seed,rooms))
        p.start()
        pp.start()
    