from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
Base=declarative_base()
class WO_FILE(Base):
    __tablename__="wofile"
    AMC_Start_Period=Column("AMC_Start_Period", Date)
    AMC_End_Period=Column("AMC_End_Period",Date)
    Date=Column("Date",Date)
    Work_Order_Number=Column("Work_Order_Number",String, primary_key=True)
    File_Order_Number=Column("File_Order_Number",String)
    Subject=Column("Subject",String) 
    Contact=Column("Contact",Integer)
    Amount=Column("Amount",Float)
    Address=Column("Address",String)
    Reminder=Column("Reminder", Integer, default=0)
    
class load_wofile_data():
    def __init__(self, data):
        self.engine=create_engine("sqlite:///stpi.db", future=True)
        self.data=data
        self.conn=self.engine.connect()
        self.check_table()
        self.check_data()
        self.conn.close()
        self.engine.dispose()
    
    def check_table(self):
        inspector=inspect(self.engine)
        if ("wofile" not in inspector.get_table_names()):
            Base.metadata.create_all(self.engine)
            
    def check_data(self):
        query=select(WO_FILE.Work_Order_Number) 
        result=self.conn.execute(query)
        # print(result.scalars().all())
        l=[]
        result= [x[0] for x in result.fetchall()]
        print(result)
        i=0
        while(i<len(self.data)):
            x=self.data[i]
            if(x['Work_Order_Number'] in result):
                l.append(x['Work_Order_Number'])
                self.data.remove(x)
            else:
                i+=1
        print(l)
        print(self.data)            
        if(len(self.data)!=0):
            self.insert_data()
    
    def insert_data(self):
        query=insert(WO_FILE)
        conn=self.engine.connect()
        result=conn.execute(query, self.data)
        conn.commit()

        query=select(WO_FILE)
        result=conn.execute(query)
        
        for row in result:
            print(row)
        self.conn.close()
        self.engine.dispose()

    
# data=[{'Date': datetime.datetime(2022, 8, 8, 0, 0), 'Work_Order_Number': 'STPIN/PUR/WO/22-23/07', 'File_Order_Number': 'SMSG/OMS/02/006-STPIN', 'Address': 'M/s Fusion ServicesJ-5, Park Street,Mayur Vihar-IIDelhi-110091', 'Contact': '9717054734', 'Subject': ' Comprehensive AMC for Tritronics make UPS Systems installed at STPI Noida', 'Amount': 141600.0, 'AMC_Start_Period': datetime.datetime(2022, 9, 20, 0, 0), 'AMC_End_Period': datetime.datetime(2023, 9, 19, 0, 0)}]
# # # l=list(map(int,data[0]["Date"].split("/")))
# # # from datetime import datetime
# # # data["Date"]=datetime(l[2],l[1],l[0])
# # # l=list(map(int,data[0]["AMC_Start_Period"].split("/")))
# # # data['AMC_Start_Period']=datetime(l[2],l[1],l[0])
# # # l=list(map(int,data["AMC_End_Period"].split("/")))
# # # data["AMC_End_Period"]=datetime(l[2],l[1],l[0])
# obj=load_wofile_data(data)