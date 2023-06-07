from flask import *
class search_file():
    def __init__(self, order, center,uniq_num):
        self.order=order
        self.center=center
        self.uniq_num=uniq_num
    def find(self):
        direc=self.order+'/'+self.center
        rep=[ ("/", ""), (":",""), ("*",""), ("?",""), ('''"''',""),("<",""),(">",""),("|","")]
            
        for x,y in rep:
            self.uniq_num=self.uniq_num.replace(x,y)
        return send_from_directory(directory=direc, path=self.uniq_num )
    
o=search_file('purchase', 'NOIDA', 'STPIN/PUR/PO/22-23/08')
o.find()

