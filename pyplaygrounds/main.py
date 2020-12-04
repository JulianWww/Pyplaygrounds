from envGenerators import higtmap
from renderer.mainRender import renderEngine
from pawns.panda import PandaPawn
from editor.pythonEditor import editor
import numpy as np



#hmap = higtmap.higthmap(0)
hmap = higtmap.makeHightMap(3, 3, 0)

#the level folder is     envGeneratos.levelData.level{hmap.level}

#setup map set element 0 to -1 and add a gen.py script to the level folder gen must have a map method that takes no arguments
hmap._arr = np.array([0])
#place gems set to script if using script generation and crate a gen.py in level folder this scipt must have a gems methode
hmap.gemPoses = [(0,2)]
#place pawns ((xpos, ypos), rotation id) set to script if genration via script, add a gen.py with method pawns methode in level folder
hmap.initPos = [((0,0), 0)]
#set level id
hmap.level = 0

hmap.save()

hmap = higtmap.higthmap(hmap.level)

engine = renderEngine(hmap)
hmap.setEngine(engine)

hmap.save()

CurrentEditor = editor(engine, hmap)