from flask import *
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
import os
import pofile_extraction as po
import load_pofile_data as lopo
import wofile_extraction as wo
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


@app.route("/")
def main():
    return render_template("main.html")

@app.route("/get_purchase_file_name")
def get_purchase_file_name():
    return render_template("pofile_Web.html")

@app.route("/load_purchase_file_name", methods=['POST'])
def load_purchase_file_name():
    files_name=os.listdir(uploads_purchase)
    for x in files_name:
        os.remove(uploads_purchase+'/'+x)
    data=[]
    if(request.method=='POST'):
        pofiles=request.files.getlist('purchase_order_file')
        # pofiles.save(pofiles.filename)
    print("pofile",pofiles)
    for file in pofiles:
            file.save(os.path.join(uploads_purchase,secure_filename(file.filename)))
            # print(file)
    files_name=os.listdir(uploads_purchase)
    print("dir",dir)
    # return ("OK")
    # return render_template('show_result.html', result=pofiles)
    print("file",files_name)
    if(files_name!=None):   
        for x in files_name:   
            try:
                obj=po.pofile_extraction(uploads_purchase+'/'+x)    
                print(x,obj.return_data())  
                data.append(obj.return_data())
            except:
                flash(f"Error in file {x}", "danger")
                return redirect(url_for('get_purchase_file_name'))
    # print("maon",data)
    data=list({v["Purchase_Order_Number"]:v for v in data }.values())
    
    if(lopo.load_pofile_data(data)):
        
        flash(f"Data added successfully", "success")
        return redirect(url_for('main'))
    else:
        flash("Error in inserting data", "FAIL")
        return redirect(url_for('main'))
    

@app.route("/get_work_file_name") 
def get_work_file_name():
    return render_template("wofile_Web.html")

@app.route("/load_file_name", methods=["POST"])
def load_work_file_name():
    files_name=os.listdir(uploads_work)
    for x in files_name:
        os.remove(uploads_work+'/'+x)
    data=[]
    if(request.method=='POST'):
        wofiles=request.files.getlist('work_order_file')
        # pofiles.save(pofiles.filename)
    for file in wofiles:
            file.save(os.path.join(uploads_work,secure_filename(file.filename)))
            # print(file)
    files_name=os.listdir(uploads_work)
    print(dir)
    # return ("OK")
    # return render_template('show_result.html', result=pofiles)
    if(files_name!=None):   
        for x in files_name:   
            try:
                obj=wo.wofile_extraction(uploads_work+'/'+x)      
                data.append(obj.return_data())
            except:
                flash(f"Error in file {x}", "danger")
                return redirect(url_for('get_work_file_name'))
    # print(data)
    data=list({v["Work_Order_Number"]:v for v in data }.values())
    
    if(lowo.load_wofile_data(data)):
        
        flash(f"Data added successfully", "success")
        return redirect(url_for('main'))
    else:
        flash("Error in inserting data", "FAIL")
        return redirect(url_for('main'))
    

@app.route("/write_to_excel")
def write_to_excel():
    wrt.write_to_excel(uploads_excel)
    
    return send_from_directory(directory=uploads_excel,path="STPI_Data.xlsx")


def alert():
    obj=al.alert()
    data=obj.check()
    print("main\n",data)
    if(len(data)!=0):
        obj=ml.mail(data)
        
        


if(__name__=="__main__"):   
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=alert, trigger="interval" , days=7)
    scheduler.start()
    app.run(use_reloader=False,debug=True)