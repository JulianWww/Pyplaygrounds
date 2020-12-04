"an editor to write the script in"

import tkinter
from editor.translator import *
from pawns.panda import PandaPawn
from threading import Thread


class editor(Thread):
    """a tk window in used for user input

    the user writes his, her code in this window and it gets executed usting pythons exec function
    alsow this class is run via threads
    aswell as running the engine
    """
    def __init__(self, enigne, hmap):
        """initate the tk thread and run engine in main thread
        """
        self.engine = enigne
        "the panda render engine instance to execute in"

        self.hmap = hmap
        "the hmap on witch we play"
        Thread.__init__(self)
        self.start()

        std_pawn = PandaPawn(0, self.hmap)
        self.engine.addPawn(std_pawn)
        setPawn(std_pawn)
        self.engine.run()
    
    def run(self, *args):
        """acutal initation of the tk window

        this function is called by the thread when in executes
        """
        self.master = tkinter.Tk()
        self.master.title(f"level {self.hmap.level} editor")

        #crate the widget
        self.crateWidget()

        self.mainloop()

    def crateWidget(self):
        """initates the widget of the editor

        crates a text fielf for the input and an execute button
        """
        self.text = tkinter.Text(self.master)
        self.text.pack()

        # add a button
        executer = tkinter.Button(self.master, text = "run", command = self.executeUserInputCode)
        executer.pack()

    def executeUserInputCode(self):
        """execute the user inputed code
        """
        self.hmap.reset()
        try:
            exec(self.text.get('1.0', 'end-1c'))
        except Exception as e:
            self.text.insert(tkinter.END, f"\n ooops you seam to have done somthing wrong plz take an other look the\n\terror was {e}")
        # if at the end of the execution the game is done congratulate user
        if self.hmap.isDone():
            self.master.quit()
        #tkinter.messagebox.showinfo(title="level compleat", message="good job you have compleeted the level")
    
    def mainloop(self): 
        "run the window"
        self.master.mainloop()
