from flask import *
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import tabulate
from forms import purchase_order,work_order,search
import load_pofile_data as lopo
import load_wofile_data as lowo
import write_to_excel as wrt
import alert as al
import mail as ml

app=Flask(__name__)
app.config['SECRET_KEY']='1805654e9e7fd00be253cca13ddab5da'
uploads_purchase = os.path.join(app.instance_path, 'purchase')
os.makedirs(uploads_purchase,exist_ok=True)
uploads_work = os.path.join(app.instance_path, 'work')
os.makedirs(uploads_work,exist_ok=True)
uploads_excel = os.path.join(app.instance_path, 'excel')
os.makedirs(uploads_excel,exist_ok=True)
city=['NOIDA', 'Lucknow', 'Kanpur', 'Gwalior', 'Meerut', 'Prayagraj','Indore', 'Bhopal','Bhilai','Dehradun']
for x in city:
    path1=os.path.join(uploads_purchase,x)
    path2=os.path.join(uploads_work,x)
    
    os.makedirs(path1,exist_ok=True)
    os.makedirs(path2,exist_ok=True)
    

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/get_purchase_file_name", methods=['GET', 'POST'])
def get_purchase_file_name():
    form=purchase_order()
    if form.validate_on_submit() and request.method=='POST':
        data={}
        for x in form.data:
            data[x]=form.data.get(x)
        store_file={'File_name':data['File'], 'Date':data['Date'], 'City':data['City']}
        print("sdfs",store_file['File_name'])
        del data['File']
        del data['csrf_token']
        print(data)
        # print(x, form.data.get(x))
       
        try:
            
                
            myFile = secure_filename(form.File.data.filename)
            print(myFile)
            # file = request.files['Upload File']
            path=uploads_purchase+"/"+store_file['City']
            name=data['Purchase_Order_Number']
            rep=[ ("/", ""), (":",""), ("*",""), ("?",""), ('''"''',""),("<",""),(">",""),("|","")]
            
            for x,y in rep:
                name=name.replace(x,y)
            print("ASDFASI\n\n",name)
            form.File.data.save(os.path.join(path,name))
            lopo.load_pofile_data(data)
        except Exception as error:
            flash(f"{error}", "danger")
        else:
            
            
            flash(f'File submitted',"success")   
            # file.save(os.path.join(uploads_purchase,secure_filename(store_file['File_name'])))
            
            # if(store_file['Date'].year in os.listdir(uploads_purchase)):
                
                # file_path=uploads_purchase+f"/{store_file['City']},"
                # file=secure_filename(form.File.file.filename)
                # file.save(os.path.join(file_path, secure_filename(store_file['File_name'])))
        
        return redirect(url_for('main'))
    
    return render_template("pofile_web.html", form=form)


    

@app.route("/get_work_file_name",methods=['POST', 'GET']) 
def get_work_file_name():
    form=work_order()
    if form.validate_on_submit():
        data={}
        print("WORK ORDER FILE")
        for x in form.data:
            data[x]=form.data.get(x)
        print(data)
        store_file={'File_name':data['File'], 'Date':data['Date'], 'City':data['City']}
        print("sdfs",store_file)
        del data['File']
        del data['csrf_token']
        print(data)
        try:
            
            myFile = secure_filename(form.File.data.filename)
            print(myFile)
            # file = request.files['Upload File']
            path=uploads_work+"/"+store_file['City']
            name=data['Work_Order_Number']
            rep=[ ("/", ""), (":",""), ("*",""), ("?",""), ('''"''',""),("<",""),(">",""),("|","")]
            
            for x,y in rep:
                name=name.replace(x,y)
            form.File.data.save(os.path.join(path,secure_filename(name)))
            lowo.load_wofile_data(data)
            # print("excdedf e",res)
            # if(res==101):
            #     print(101)
            #     raise Exception(flash(f"Data already in database","danger"))
            
        except Exception as error:
            # print(error,"Not submitted")
            flash(f"{error}", "danger")
        else:
            # print("submitted")
            
            flash(f'File submitted',"success")
        
        return redirect(url_for('main'))
    
    return render_template("wofile_web.html", form=form)
    

@app.route("/write_to_excel")
def write_to_excel():
    try:
        wrt.write_to_excel(uploads_excel)
    
        return send_from_directory(directory=uploads_excel,path="STPI_Data.xlsx")
    except Exception as error:
        flash(f"{error}", 'danger')
        return redirect(url_for('main'))

@app.route("/search_file",methods=['POST','GET'])
def search_file():
    form=search()
    if(form.validate_on_submit()):
        print(form.data['City'])
        direc=os.path.join(app.instance_path,form.data['File_type']+'/'+form.data['City'])
        rep=[ ("/", ""), (":",""), ("*",""), ("?",""), ('''"''',""),("<",""),(">",""),("|","")]
        order_id=form.data['Order_ID']
        for x,y in rep:
            print(x)
            order_id=order_id.replace(x,y)
        print(direc,order_id)
        try:
            return send_from_directory(directory=direc, path=order_id )
        except Exception as error:
            flash(f"File Not Found",'danger')
        else:
            return redirect(url_for('main'))
    return render_template("search_file.html",form=form)
    
def alert():
    obj=al.alert()
    data=obj.check()
    # print("main\n",data)
    if(len(data)!=0):
            header=data[0].keys()
            for x in data:
                email=x['Email']
                # print(email)
                # x.remove('Email')
                rows=x.values()
                data1=tabulate.tabulate([rows],header)
                # print(data1)
                time.sleep(10)
                obj=ml.mail(data1,email)
            # print("alert",l)
          

        
        


if(__name__=="__main__"):   
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=alert, trigger="interval" , days=7)
    scheduler.start()
    app.run(debug=True)
