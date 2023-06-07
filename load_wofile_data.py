from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
Base=declarative_base()
class WO_FILE(Base):
    __tablename__="wofile"
    Start_Period=Column("Start_Period", Date)
    End_Period=Column("End_Period",Date)
    Date=Column("Date",Date)
    Work_Order_Number=Column("Work_Order_Number",String, primary_key=True)
    File_Order_Number=Column("File_Order_Number",String)
    Subject=Column("Subject",String) 
    Contact=Column("Contact",Integer)
    Amount=Column("Amount",Float)
    Address=Column("Address",String)
    Email=Column("Email", String)
    Reminder=Column("Reminder", Integer, default=0)
    City=Column("City", String)
    
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
     
        result= [x[0] for x in result.fetchall()]
        print(result)
        x=self.data
        print(self.data)
        if(x['Work_Order_Number'] in result):
            print("Data already in database")
            raise Exception("Data already in database")

        
        self.insert_data()
    
    def insert_data(self):
        query=insert(WO_FILE)
        conn=self.engine.connect()
        result=conn.execute(query, self.data)
        conn.commit()
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