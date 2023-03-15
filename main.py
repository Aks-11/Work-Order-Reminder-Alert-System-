import pofile as po
import wofile as wo
import write_to_excel as exc
from sqlalchemy import *
from tkinter import *
from tkfilebrowser import askopenfilenames


class Main():
   def __init__(self, master=None):
      self.files_name=[]
      self.master=master
      self.geoma()
      self.pofile_button()
      self.wofile_button()
      self.start_writing()
   
   def geoma(self):
      self.master.geometry("400x200")
      self.master.configure(bg='grey')
      
   def pofile_button(self):
      
      btn1=Button(self.master, text="PO_File", command=lambda:self.pofile_action())
      btn1.grid(row=1, column=1, padx=20, pady=30)
      
   def pofile_action(self):
      rt=Toplevel()
      rt.grab_set()
      po.pofile(rt)
      rt.mainloop()
   
      
   def wofile_button(self):
      btn2=Button(self.master, text="WO_File", command=lambda:self.wofile_action())
      btn2.grid(row=1, column=2, padx=20, pady=30)
      
   def wofile_action(self):
      rt=Toplevel()
      rt.grab_set()
      wo.wofile(rt)
      rt.mainloop()
   def start_writing(self):
      btn3=Button(self.master, text="Get Excel", command=self.start_writing_action)
      btn3.grid(row=1, column=3, padx=20, pady=30)
      
   def start_writing_action(self):
      rt=Toplevel()
      rt.grab_set()
      exc.write_to_excel(rt)
      rt.mainloop()
root=Tk()

obj=Main(root)
mainloop()