from mcpi.minecraft import Minecraft
from mcpi import block
import math, random

# Euclidean distance between points (x1, y1, z1) and (x2, y2, z2)
def distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt((dx ** 2) + (dy ** 2) + (dz ** 2))

# Returns a random x, y, z point beteen (x0, y0, z0) and (x1, y1, z1) inclusive
def getRandPoint(x0, y0, z0, x1, y1, z1):
    x = random.randint(x0, x1)
    y = random.randint(y0, y1)
    z = random.randint(z0, z1)
    return x, y, z

# Finds x, y, z location of a non air block within a range
def getNonAir(mc, x0, y0, z0, x1, y1, z1):
    x, y, z = 0, 0, 0
    isAir = True
    while(isAir):
        x, y, z = getRandPoint(x0, y0, z0, x1, y1, z1)
        blkid = mc.getBlockWithData(x, y, z).id
        isAir = blkid == block.AIR.id
    return x, y, z
        

# Creates diamond block at random location, returns the coordiantes of the block
def createDiamond(mc, ppos):
    playerHeight = mc.getHeight(ppos.x, ppos.z)
    ymin = playerHeight - 5
    ymax = playerHeight + 5
    xmin = -124
    xmax = 124
    zmin = -124
    zmax = 124
    x, y, z = getNonAir(mc, xmin, ymin, zmin, xmax, ymax, zmax)
    mc.setBlock(x, y, z, block.DIAMOND_BLOCK.id)
    return x, y, z

# Main game function
def playGame(mc):
    mc.postToChat("Right click on blocks to find the diamond block!")
    mc.postToChat("Placing diamond block...")
    ppos = mc.player.getTilePos()
    dx, dy, dz = createDiamond(mc, ppos)
    print(dx, dy, dz)
    found = False
    prevDist = -1
    mc.postToChat("Go!")
    while(not found):
        for hit in mc.events.pollBlockHits():
            # Get hit position
            hx, hy, hz = hit.pos.x, hit.pos.y, hit.pos.z
            if(hx == dx and hy == dy and hz == dz):
                mc.postToChat("You found it!")
                found = True
            else:
                # Get the distance between the block hit and the diamond
                dist = distance(dx, dy, dz, hx, hy, hz)
                if(prevDist == -1): # If no distance has been calculated
                    mc.postToChat("Keep looking and you find the block")
                else:
                    if(dist > prevDist):
                        mc.postToChat("Getting colder!")
                    else:
                        mc.postToChat("Getting warmer!")
                # copy distance to previous distance
                prevDist = dist
mc = Minecraft.create()
playGame(mc)

