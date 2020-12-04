import tkinter
from tkinter import ttk
from pickle import dump, load
import os

from envGenerators import higtmap
from renderer.mainRender import renderEngine
from pawns.panda import PandaPawn
from editor.pythonEditor import editor

level = None

class levelSelector(tkinter.Tk):
    """tk window to select window

    a tk window used to get the level the user wants to play as well as initating the discriptor of the level in its txt box

    sublcass tk
    """
    def __init__(self):
        tkinter.Tk.__init__(self)
        "initaite supercalss tk"
        self.title("pyplaygrounds level selector")

        selector = tkinter.Label(self, text="plz select a level")
        selector.pack()  

        levles = load(open(f"{os.path.dirname(os.path.abspath(__file__))}/envGenerators/levelData/allLevels.p","rb"))
        # load the currently finisched levels from file
        self.selector = ttk.Combobox(self, values = levles)
        """slect witch level

        a combobox to select witch level to load
        """
        self.selector.bind("<<ComboboxSelected>>", self.levelSelecotValueChanged)
        self.selector.pack()

        self.discriptionBox = tkinter.Text(self)
        """what the level is about

        a txt widget that discribes what the level is all about
        """
        self.discriptionBox.pack()

        self.executeLevel = tkinter.Button(self, text = "play", command=self.runFunction)
        """run the level

        a button widet that is used to initate the level
        """
        self.executeLevel.pack()

    
    def levelSelecotValueChanged(self, *vals):
        """called when a level is selected by tk"""
        self.loadLevelDoc(self.selector.get(), self.discriptionBox)
    
    @staticmethod
    def loadLevelDoc(level, discriptionBox):
        """load the level doc saved as a txt file and render it to a text box

        @param level: the level to load from
        @type level: int
        """
        discriptionBox.delete('1.0',tkinter.END)
        #load the doc
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/envGenerators/levelData/level{level}/doc.txt") as f:
            data =  f.read().splitlines()
            for line in data:
                discriptionBox.insert(tkinter.END, line)
                discriptionBox.insert(tkinter.END, "\n")

    def runFunction(self):
        """run the level

        deconstruct this widget and initiate the level
        """
        global level
        level = self.selector.get()
        self.quit()



if __name__ == "__main__":
    selector = levelSelector()
    "the selectorwidget"
    selector.mainloop()

    hmap = higtmap.higthmap(level)
    "the higtmat that was selected"
    engine = renderEngine(hmap)
    "the renderengine to run on"
    hmap.setEngine(engine)

    CurrentEditor = editor(engine, hmap)
    "the edutior to write script in"
        #____________execute script
        #deconstructor
