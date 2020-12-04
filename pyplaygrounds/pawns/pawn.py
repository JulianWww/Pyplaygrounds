from copy import copy

class pawn():
    """
    the baseclass for all pawns containing pawn movement and controls
    """
    movement_map = [(0,1),
                    (1,0),
                    (0,-1),
                    (-1,0)]
    def __init__(self, id, hmap):
        """initiate the base pawn with a location an id and a hmap in witch it exists
        """
        self.id = id
        "a unique value for each hmap, used to initiate the inital location and all other values loaded from file"
        pos, self.rotation = hmap.initPos[id]
        "self.rotation is the rotation 0, 1,2,3 etc"
        self.pos = pos[0], pos[1]
        "a 3d tuple containing the x, y, z locations of the pawn"
        self.hmap = hmap
        "reference to the hmap the pawn is on or in"

        self.initTrans = copy(pos), copy(self.rotation)
        """inital transfrorm

        a tupple containing a copy of the inital positon and the inital rotation"""
        # add the pawn to reset list of hmap
        hmap.add_pawn(self)
    
    def turn(self, direction):
        """turns the pawn

        direction + or - 1 one being left the other right
        """
        self.rotation += direction
        # turn the liniear roation into a circle
        self.rotation = int(0 if self.rotation>=4 else 3 if self.rotation<0 else self.rotation)
        self._setPawnRenderRotation()
        #rotate the pawn
    
    def _setPawnRenderRotation(self):
        """set roation for render

        an internal function that translates the game engine rotation to render engeine rotation
        and rotats the actor
        """
        angleMap = [180, 90, 0, 270]
        self.actor.setHpr(angleMap[self.rotation], 0, 0)
    
    def _setPawnLoc(self, pos):
        """sets the postition of the pawn

        @param pos: the x, y of the pawn
        @type pos: tuple(x,y)
        """
        # calculate render location from inengine location
        if pos is None:
            return
        x = pos[0]+.5
        y = pos[1]+.5
        z = self.hmap._arr[pos] + 1
        self.actor.setPos(x, y, z)

    
    def moveForward(self, distance=1):
        """move pawn forward by distance
        
        @param distance: how many blocks to move forward
        @type distance: int"""
        # get current hight
        currentHight = self.hmap._arr[self.pos]
        # calculate new position
        x, y = self.pos
        dx, dy = pawn.movement_map[self.rotation]
        new_pos = (x+dx, y+dy)
        # if not in map return
        if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] > self.hmap._arr.shape[0] or new_pos[1] > self.hmap._arr.shape[1]: return
        if self.hmap._arr[new_pos]+1 >= currentHight >= max(1, self.hmap._arr[new_pos]-1):
            self.pos = new_pos
            self._setPawnLoc(self._setPawnLoc(new_pos))

    def reset(self):
        "reste the actors location"
        self.pos, self.rotation =  self.initTrans

        self._setPawnLoc(self.pos)
        self._setPawnRenderRotation()
    
    def collectGem(self):
        """collect the gem the pawn is standing on"""
        if self.pos in self.hmap.gemPoses:
            idx = self.hmap.gemPoses.index(self.pos)
            if not idx in self.hmap.collectedGems:
                self.hmap.collectedGems.append(self.hmap.gemPoses.index(self.pos))
                self.hmap.gemsRemaining -= 1

                self.hmap.engine.gems[self.hmap.gemPoses.index(self.pos)].hide()
                print(self.hmap.gemsRemaining)
    

    def isBlocked(self, rdir):
        """is the pawn blocked??
        
        retuns a boolian value containing weather or not the pawn is bloked in the relative direction withc is comuted identicly to the turning

        @param rdir: the reletive direction 
        @type rdir: int
        """
        #cumpute absolute rotation
        adir = self.rotation + rdir
        adir = int(0 if adir>=4 else 3 if adir<0 else adir)
        (x, y), (dx, dy) = self.pos, pawn.movement_map[adir]
        new_pos = x+dx, y+dy
        try:
            return  not (self.hmap._arr[new_pos] + 1>= self.hmap._arr[self.pos] >= max(1, self.hmap._arr[new_pos]-1))
        except IndexError:
            return True
