from time import sleep as wait

std_pawn = None
"the std pawn to execute on"
def setPawn(pawn):
    "define the std_pawn"
    global std_pawn
    std_pawn = pawn

def forward():
    "move std pawn forwards by 1"
    wait(.5)
    std_pawn.moveForward(1)
    wait(.5)

def fd():
    "move std pawn forwards by 1"
    forward()

def turnLeft():
    "turn the pawn to the left"
    wait(.5)
    std_pawn.turn(-1)
    wait(.5)

def left():
    "turn the pawn to the left"
    turnLeft()

def turnRight():
    "turn the pawn to the right"
    wait(.5)
    std_pawn.turn(1)
    wait(.5)

def right():
    "turn the pawn to the right"
    turnRight()

def collect():
    "collect gem on current location"
    wait(.5)
    std_pawn.collectGem()
    wait(.5)

def collectGem():
    collect()

def isBlocked():
    return std_pawn.isBlocked(0)

def isBlocked_left():
    return std_pawn.isBlocked(-1)

def isBlocked_right():
    return std_pawn.isBlocked(1)