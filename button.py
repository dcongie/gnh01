from tkinter import *
class App:
  def __init__(self):
    #frame = Frame(master)
    #frame.pack()
    self.button = Button(text="QUIT", fg="red",
                         command=self.write_slogan)
    self.button.pack(side=LEFT)
    self.slogan = Button(text="Hello",
                         command=self.write_slogan)
    self.slogan.pack(side=LEFT)
    root.mainloop()

  def write_slogan(self):
    print ("Tkinter is easy to use!")

if __name__ == "__main__":
    root = Tk()
    app = App()
