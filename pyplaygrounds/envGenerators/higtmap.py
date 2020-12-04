import numpy as np
import pickle
import os

def makeHightMap(xsize, ysize, lvl):
    """make a new higtmap

    crate new higtmap with dimentions xsize, ysize, and level key lvl
    @param xsize: the amount of values in the x dimention
    @type xsize: int

    @param ysize: the amount of values in the y dimention
    @type ysize: int

    @param lvl: the level key in witch the data is saved
    @type lvl: int
    """
    return higthmap((xsize, ysize, lvl))

class higthmap:
    """a container representing how high the level is at every point
    
    basicly its a wrapper of a numyp array containing the higts
    the caracter can wark down any hit cant work on lvl 0 but can only go up 1 block

    aswell as the initial character position
    """
    def __init__(self, lvl=(10,10, -1)):
        """initiate the container

        load data from save file using subscript load
        if we pass a tupple to level it will crate a new level of size lvl and level key of lvl[-1]
        """

        self.level = lvl[-1] if isinstance(lvl, tuple) else lvl
        """a int containing witch level is loaded"""
        self._arr = np.ones(lvl[:-1], dtype=np.int) if isinstance(lvl, tuple) else higthmap.loadHightmap(lvl)
        """the actual higt map
        
        as np array type"""

        self.initPos =[((0,0), 0)] if isinstance(lvl, tuple) else higthmap.loadPawnPositions(lvl)
        """the initial positon of the pawns

        writen as a list of tuples"""

        self.gemPoses = [(0,1)] if isinstance(lvl, tuple) else higthmap.loadGemPositions(lvl)
        """the inital positions of the gems

        writen as a list of tuples"""
        self.collectedGems = []
        """the gems that where already collected as an index
        
        used py the pawns collect gem method to ignore the gems that where already collected"""
        self.gemsRemaining = len(self.gemPoses)
        """the number of remaining gems

        how many gems remain to collect"""

        self.pawns = []
        "a reference to every pawn in it for reset"
    
    def setEngine(self, engine):
        """set the rendering script

        tels the hmap witch eninge instance is uset for rendering

        @param engine: the engine instance to render in
        @type engine: render engine defiend in rener.mainRender
        """
        self.engine = engine
    
    @staticmethod
    def loadGemPositions(lvl):
        """load the postions of the gems

        load the positions of the gems from file
        @param lvl: the level to load from
        @type lvl: int

        return: a list of tuples contining the inital gen locations"""
        try:
            exec(f"""from envGenerators.levelData.level{lvl} import gen;arr = gen.gems(); pickle.dump(arr, open(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{lvl}/initGemLocs.p", "wb"))""")
        except Exception as e:
            pass

        arr = pickle.load(open(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{lvl}/initGemLocs.p", "rb"))
        if arr == "script":
            exec("import envGenerators.levelData.level{level}.gen as gen; arr = gen.gems()")
        return arr
    
    @staticmethod
    def loadHightmap(level):
        """load higtmap data from level {level}

        @param level: the level to be loaded
        @type level: int,
        
        @return: an ndarray contining the higtmap data"""
        try:
            exec(f"""from envGenerators.levelData.level{level} import gen;arr = gen.map(); np.save(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{level}/hightmap.npy", arr)""")
        except Exception as e:
            pass

        arr = np.load(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{level}/hightmap.npy")
        return arr
    
    @staticmethod
    def loadPawnPositions(level):
        """load the inital pawn locations

        load the inital pawn locations from saves

        @param level: the level to load from
        @type level:  int

        @return: a list of tuples contining the inital pawn locations
        """
        try:
            exec(f"""from envGenerators.levelData.level{level} import gen;arr = gen.pawns(); pickle.dump(arr, open(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{level}/initPoses.p", "wb"))""")
        except Exception as e:
            print(e)

        arr = pickle.load(open(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{level}/initPoses.p", "rb"))
        return arr
    
    def __getitem__(self, idx):
        return self._arr[idx]
       
    def save(self):
        """save current higt data to file

        save the current higtmap fore later loading
        """
        #crate saves directory
        if not os.path.isdir(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{self.level}"):
            os.makedirs(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{self.level}")
            print("made file")
        # save the hightmap
        np.save(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{self.level}/hightmap.npy", self._arr)
        # save inital locations
        pickle.dump(self.initPos, open(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{self.level}/initPoses.p", "wb"))
        # save inital gem locations
        pickle.dump(self.gemPoses, open(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/level{self.level}/initGemLocs.p", "wb"))

        #add level to level list
        allLevels = pickle.load(open(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/allLevels.p", "rb")) if os.path.isfile(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/allLevels.p") else []
        if not self.level in allLevels:
            allLevels.append(self.level)
        pickle.dump(allLevels, open(f"{os.path.dirname(os.path.abspath(__file__))}/levelData/allLevels.p", "wb"))

    def add_pawn(self, pawn):
        """add a pawn to the pawn list"""
        self.pawns.append(pawn)

    def reset(self):
        """resets the level to init state

        resets pawn positions and rotation

        replaces all gems
        resets gemm counter
        """
        for pawn in self.pawns:
            pawn.reset()

        #replace gems
        self.collectedGems = []
        for actor in self.engine.gems: 
            actor.show()
        #reset gem counter
        self.gemsRemaining = len(self.gemPoses)

    def isDone(self):
        """is the level compleat
        
        a function to detect weather or not we are done with the level aka it has bean compleated
        @returns: a bool that is true if all gems where collected
        """
        return not bool(self.gemsRemaining)