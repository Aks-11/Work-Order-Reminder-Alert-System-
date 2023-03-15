import wofile_extraction as wo
import load_wofile_data as lowo
from tkinter import *
import tkinter.messagebox as tmsg
from tkfilebrowser import askopenfilenames
class wofile():
    
    def __init__(self, master=None):
        self.master=master
        self.get_wofile_name()
        self.submit_button()
        
    def get_wofile_name(self):
        Lbl1=Label(self.master, text="Select Work Order Files")
        Lbl1.grid(row=0, column=1, padx=10, pady=10)
        Btn=Button(self.master, text="Browse", command=lambda:self.get_files_name()) 
        Btn.grid(row=0, column=3, padx=10, pady=10)
        
    def get_files_name(self):
        self.files_name=askopenfilenames(parent=self.master, initialdir=".",title="Select files", filetypes=[("Doc", ".docx")])
        Label(self.master, text="File Selected").grid(row=2, column=1)
        print(self.files_name)
        
    def submit_button(self):
        submit=Button(self.master,text="Submit", command=lambda:self.submit_action())
        submit.grid(row =2, column=3)
    
    def submit_action(self):
        # try:
        self.data=[]
        if(self.files_name!=None):   
            for x in self.files_name:   
                obj=wo.wofile_extraction(x)      
                self.data.append(obj.return_data())
        print(self.data)
        self.data=list({v["Work_Order_Number"]:v for v in self.data }.values())
        if(lowo.load_wofile_data(self.data)):
            tmsg.showinfo("Success",    "Data Input successful ")
        
            
        self.master.destroy()
        # except:
            
        #     tmsg.showerror("Error", "File Error")
        
# root=Tk()
# obj=wofile(root)
# mainloop()
