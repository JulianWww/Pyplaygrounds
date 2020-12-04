# Run tkinter code in another thread

import tkinter as tk
import threading

class App(threading.Thread):

    def __init__(self, *args):
        self.jvals = args
        threading.Thread.__init__(self, args=args)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self, *args):
        print(args)
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        label = tk.Label(self.root, text="Hello World")
        label.pack()

        self.root.mainloop()


app = App(1, "hi")
print('Now we can continue running code while mainloop runs!')

for i in range(5):
    print(i)