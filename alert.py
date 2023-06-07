from datetime import datetime
from sqlalchemy import *
import tabulate
class alert():
    def __init__(self):

        self.engine =create_engine("sqlite:///stpi.db",future=True)
        self.conn=self.engine.connect()
    
    def check(self):
        query=text(f"select Email,Start_Period, End_Period, Date, Work_Order_Number, File_Order_Number, Subject,Contact ,Amount, Reminder from wofile")
        result=self.conn.execute(query)
        l=[]
        for x in result.fetchall() :
            d=x._mapping
            l.append(d)
        # print(l)
     
        n=0
        sze=len(l)
        while(n<sze):
            x=l[n]
            date_object = datetime.strptime(x["End_Period"], '%Y-%m-%d').date()
            # print((date_object))
            res=date_object-datetime.today().date()
            if(res.days>60 or x["Reminder"]>=40):
                l.pop(n)
                sze-=1
            else:
                n+=1
            # print(res.days)
        
        t=tuple(x["Work_Order_Number"] for x in l)
        t+=("s","t")
        query=text(f"update wofile set reminder=reminder+1 where Work_Order_Number in {t}")
        self.conn.execute(query)
        self.conn.commit()
        self.conn.close()
        self.engine.dispose()
        # print(l,"\n\n",t)
        return l
        print(l)
        print(l[0])
        if(len(l)!=0):
            header=l[0].keys()
            rows=[x.values() for x in l]
            # print("alert",l)
            return tabulate.tabulate(rows, header)
        return []
        
# o=alert()
# print(o.check())