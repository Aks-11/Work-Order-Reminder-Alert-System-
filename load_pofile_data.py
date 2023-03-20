from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
Base= declarative_base()
class PO_FILE(Base):    
    __tablename__="pofile"
    Date=Column("Date",Date)
    Purchase_Order_Number=Column("Purchase_Order_Number",String, primary_key=True)
    File_Order_Number=Column("File_Order_Number",String)
    Subject=Column("Subject",String) 
    Contact=Column("Contact",Integer)
    Amount=Column("Amount",Float)
    Address=Column("Address",String)



class load_pofile_data():
    def __init__(self, data):
        self.engine=create_engine("sqlite:///stpi.db", future=True, connect_args={"check_same_thread": False})
        self.meta=MetaData()
        self.conn=self.engine.connect()
        self.data=data
        self.check_table()
        self.check_data()
        
        
        
    def check_table(self):  
        inspector=inspect(self.engine)
        if ("pofile" not in inspector.get_table_names()):
            Base.metadata.create_all(self.engine)
    
    def check_data(self):
        query=select(PO_FILE.Purchase_Order_Number) 
        result=self.conn.execute(query)
        # print(result.scalars().all())
        l=[]
        result= [x[0] for x in result.fetchall()]
        print(result)
        i=0
        while(i<len(self.data)):
            x=self.data[i]
            if(x['Purchase_Order_Number'] in result):
                l.append(x['Purchase_Order_Number'])
                self.data.remove(x)
            else:
                i+=1
        print(l)
        print(self.data)            
        if(len(self.data)!=0):
            self.insert_data()
    def insert_data(self):
        
        query=insert(PO_FILE)
        
        result=self.conn.execute(query,self.data)
        self.conn.commit()       
        
        query=select(PO_FILE)
        result=self.conn.execute(query)
        self.conn.close()
        self.engine.dispose()
        return True
        # for row in result:
        #     print(row)
        
# # data=[{'Date': '08/08/2022', 'Purchase_Order_Number': 'STPIN/PUR/WO/22-23/07', 'File_Order_Number': 'SMSG/OMS/02/006-STPIN', 'Address': 'M/s Fusion ServicesJ-5, Park Street,Mayur Vihar-IIDelhi-110091', 'Contact': '9717054734', 'Subject': 'Subject: Comprehensive AMC for Tritronics make UPS Systems installed at STPI Noida', 'Amount': 141600.00},{'Date': '08/08/2022', 'Purchase_Order_Number': 'STPIN/PUR/WO/22-23/08', 'File_Order_Number': 'SMSG/OMS/02/006-STPIN', 'Address': 'M/s Fusion ServicesJ-5, Park Street,Mayur Vihar-IIDelhi-110091', 'Contact': '9717054734', 'Subject': 'Subject: Comprehensive AMC for Tritronics make UPS Systems installed at STPI Noida', 'Amount': 141600.00}]
# data=[{'Date': datetime.datetime(2022, 7, 26, 0, 0), 'Purchase_Order_Number': 'STPIN/PUR/PO/22-23/08', 'File_Order_Number': 'SMSG/MPU/16/025-STPIN', 'Address': 'M/s  Kartik Infotech723, 7th Floor,Hemkunt Chamber89Nehru Place, Delhi-110019', 'Contact': '8527874292', 'Subject': ' Supply of 01no. 4Ton Tower AC  at STPI-Noida', 'Amount': 100000.0}, {'Date': datetime.datetime(2022, 7, 26, 0, 0), 'Purchase_Order_Number': 'STPIN/PUR/PO/22-23/08', 'File_Order_Number': 'SMSG/MPU/16/025-STPIN', 'Address': 'M/s  Kartik Infotech723, 7th Floor,Hemkunt Chamber89Nehru Place, Delhi-110019', 'Contact': '8527874292', 'Subject': ' Supply of 01no. 4Ton Tower AC  at STPI-Noida', 'Amount': 100000.0}]
# # l=list(map(int,data[0]["Date"].split("/")))
# # from datetime import datetime
# # data[0]["Date"]=datetime(l[2],l[1],l[0])
# # data[1]["Date"]=datetime(l[2],l[1],l[0])

# obj=load_pofile_data(data)