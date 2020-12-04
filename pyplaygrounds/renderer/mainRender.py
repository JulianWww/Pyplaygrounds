"main rendering script"

import os
from math import cos, pi, sin

import matplotlib.pyplot as plt
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Filename, Material, NodePath, Point3


class renderEngine(ShowBase):
    """
    the main renderer for pandas

    the costom rendering engien parameters
    """
    def __init__(self, higthMap):
        ShowBase.__init__(self)
        "initate pandas"

        self.boxes = []
        """a 3d list containning the rendered boxes"""
        self.gems = []
        """a 1d list containing the gem actors"""
        self.showHigtMap(higthMap)
        # set inital camera location
        self.camera.setPos(0,0,1000)

    def showHigtMap(self, hightMap):
        """create render objects from hightmap

        given a hightmap the function crates cubes stackt on top of each other to render the board
        for every position in the hightmap
        its not very optimized

        will alsow create list of gems called gems and add them bla bla bla

        @param hightmap: the hightmap we get render data from
        @type hightmap: hightmap object
        """
        #create every box and write it to boxes simultainously generate the box list using append
        for x in range(hightMap._arr.shape[0]):
            self.boxes.append([])
            for y in range(hightMap._arr.shape[1]):
                self.boxes[-1].append([])
                for z in range(int(hightMap._arr[x,y]+1)):
                    #crate the actor
                    actor = loader.loadModel("models/box")
                    actor.setScale(1,1,1)
                    actor.setPos(x,y,z)
                    actor.setTexture(renderEngine.getBlockTex(hightMap,x, y,z),2)
                    # add actor to render tree
                    actor.reparentTo(self.render)
        
        #crate the gems
        for x, y in hightMap.gemPoses:
            try:
                z = hightMap._arr[x,y]
            except:
                print(f"invalid gem location, location is {x}, {y} of map of shape {hightMap._arr.shape}")

            gemActor = loader.loadModel("models/smiley")
            gemActor.setPos(x+.5,y+.5,z+1.5)
            gemActor.setScale(.5,.5,.5)
            gemActor.reparentTo(self.render)
            self.gems.append(gemActor)
    
    @staticmethod
    def getBlockTex(hightmap, *loc):
        """returns the texture of the block

        given the position and hmap we crate a pandas texture to set the actor to
        this is an indev function and is subject to change

        @param hightmap: the hmap data to get data from
        @type hightmap: higthmap

        @param loc: the position of the block whos tex wer setting
        @type loc: 3 intagers

        @return: a pandas3d texture for the objects
        """
        # get panda path of this files dir
        path = Filename.fromOsSpecific(os.path.dirname(os.path.abspath(__file__)))
        # get witch text to load
        # it top most block make grass else dirt and bottom most wather
        imag = "wather" if loc[-1] == 0 else ("grass" if loc[-1] == hightmap[loc[:-1]] else "dirt")
        tex  = loader.loadTexture(f"{path}/blocks/{imag}.jpg")
        return tex
    
    def addPawn(self, pawn):
        """add a pawn to render scene using its actor to represent it

        @param pawn: the pawn to be added
        @type pawn: a pawn object defined int pawns.pawn
        """
        pawn.actor.reparentTo(self.render)
        pawn._setPawnLoc(pawn.pos)
        pawn._setPawnRenderRotation()
