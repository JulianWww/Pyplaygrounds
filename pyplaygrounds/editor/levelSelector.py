import tkinter

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


if __name__ == "__main__":
    selector = levelSelector()
    selector.mainloop()
