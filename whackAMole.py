from mcpi.minecraft import Minecraft
from mcpi import block
import random, time

class Mole:
    
    def __init__(self, x, y, z):
        self.alive = False
        self.x = x
        self.y = y
        self.z = z
        self.timeCreated = 0
        self.timeAlive = 0

    def isAlive(self):
        return self.alive

    def isAtLocation(self, x, y, z):
        return self.x == x and self.y == y and self.z == z

    def spawn(self, mc):
        self.alive = True
        mc.setBlock(self.x, self.y, self.z, block.WOOL.id, 14)
        self.timeCreated = time.time()
        self.timeAlive = random.uniform(1.0, 3.0)

    def despawn(self, mc):
        self.alive = False
        mc.setBlock(self.x, self.y, self.z, block.AIR.id)

    def shouldDespawn(self):
        return time.time() > self.timeCreated + self.timeAlive

# Create game room
def genGameRoom(mc, ppos):
    mc.setBlocks(ppos.x - 5, ppos.y - 2, ppos.z - 5,
                 ppos.x + 5, ppos.y + 5, ppos.z + 5, block.GLASS.id)
    mc.setBlocks(ppos.x - 4, ppos.y - 1, ppos.z - 4,
                 ppos.x + 4, ppos.y + 5, ppos.z + 4, block.AIR.id)

# Create square of green wool to play game on
def genGamePlatform(mc, ppos):
    mc.setBlocks(ppos.x - 2, ppos.y - 1, ppos.z - 2,
                 ppos.x + 2, ppos.y - 1, ppos.z + 2, block.WOOL.id, 13)

def movePlayer(mc, ppos):
    mc.player.setPos(ppos.x - 3, ppos.y, ppos.z)    

def setupGameSpace(mc, ppos):
    genGameRoom(mc, ppos)
    genGamePlatform(mc, ppos)
    movePlayer(mc, ppos)

def listOfMoles(mc, ppos):
    y = ppos.y
    moles = []
    for x in range(ppos.x - 2, ppos.x + 3):
        for z in range(ppos.z - 2, ppos.z + 3):
            moles.append(Mole(x, y, z))
    return moles

def getRandomMoleNotAlive(moles):
    found = False
    mole = random.choice(moles)
    while(not found):
        if(not mole.isAlive()):
            found = True
        else:
            mole = random.choice(moles)
    return random.choice(moles)

def getMoleIndexAtLocation(moles, x, y, z):
    i = 0
    moleIndex = -1
    found = False
    while(i < len(moles) and not found):
        if(moles[i].isAtLocation(x, y, z)):
            found = True
            moleIndex = i
        i = i + 1
    return moleIndex

def spawnRandomMole(mc, moles):
    time.sleep(random.uniform(0.25, 1))
    mole = getRandomMoleNotAlive(moles)
    mole.spawn(mc)

def despawnDeadMoles(mc, moles):
    for mole in moles:
        if(mole.shouldDespawn()):
            mole.despawn(mc)

def spawnMoleThread(mc, timeStart, matchTime, moles):
    while(time.time() < timeStart + matchTime):
        spawnRandomMole(mc, moles)

try:
    import _thread as thread
except ImportError:
    import thread
    
def playGame(mc, matchTime):
    ppos = mc.player.getTilePos()
    setupGameSpace(mc, ppos)
    moles = listOfMoles(mc, ppos)
    mc.postToChat("Ready...");
    time.sleep(3)
    mc.postToChat("Go!")
    startTime = time.time()
    score = 0
    thread.start_new_thread(spawnMoleThread, (mc, startTime, matchTime, moles))
    while(time.time() < startTime + matchTime):
        for hit in mc.events.pollBlockHits():
            hx, hy, hz = hit.pos.x, hit.pos.y, hit.pos.z
            hitIndex = getMoleIndexAtLocation(moles, hx, hy, hz)
            if(hitIndex != -1):
                mole = moles[hitIndex]
                if(mole.isAlive()):
                   score = score + 1
                   mole.despawn(mc)
    mc.postToChat("Game over! Score: " + str(score))

mc = Minecraft.create()
playGame(mc, 10)

        
