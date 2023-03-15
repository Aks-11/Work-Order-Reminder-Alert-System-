from sqlalchemy import *
import pandas as pd
from tkinter import *
import tkinter.messagebox as tmsg
from tkfilebrowser import askopendirname

class write_to_excel():
    def __init__(self, master=None):
        self.master=master
        self.file_dir=""
        self.engine=create_engine("sqlite:///stpi.db", future=True)
        meta=MetaData()
        self.conn=self.engine.connect()
        self.get_directory()
        self.submit()
        

    def writing(self):
        try:
            queries={'sheet 1': 'select * from pofile',
                    'sheet 2': 'select * from wofile'}
            writer=pd.ExcelWriter(self.file_dir)
            for sheet_name, query in queries.items():
                df=pd.read_sql_query(text(query),self.conn)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()
            tmsg.showinfo("Success", "File Written as STPI_Data")
            self.master.destroy()
        except:
            # print(exception)
            tmsg.showerror("Error", "Database Error") 

    def get_directory(self):
        lbl=Label(self.master,text="Select a folder" )
        lbl.grid(row=1,column=1, padx=20, pady=30)
        btn=Button(self.master, text="Browse", command=self.get_directory_action)
        btn.grid(row=1, column=2, padx=20, pady=30)
    
    def get_directory_action(self):
        self.file_dir=askopendirname(self.master, initialdir=".", title="Select folder")
        self.file_dir+="/STPI_Data.xlsx"
        lbl2=Label(self.master, text=self.file_dir)
        lbl2.grid(row=2,  column=1, padx=20, pady=30)
                
    def submit(self):
        if(self.file_dir!=None):
            btn2=Button(self.master, text="submit", command =lambda:self.writing())
            btn2.grid(row=2, column=2, padx=20, pady=30)
            
# root = Tk()
# obj=write_to_excel(root)
# mainloop()
