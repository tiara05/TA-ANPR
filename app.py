from flask import Flask, render_template, request
import os 
from deeplearning import object_detection
from deeplearning import OCR
import shutil
import csv
import time

# webserver gateway interface
app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')

def getfd():
    idxs = 0
    while True:
        try : 
            os.mkdir(f"./static/upload/{idxs}")
            return idxs
        except Exception as E: 
            idxs += 1

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        fd = getfd()
        path_save = os.path.join(UPLOAD_PATH+str(fd)+"/"+'images.jpg')
        upload_file.save(path_save)
#         plat = OCR(os.path.join(UPLOAD_PATH+str(fd)+"/"+'images.jpg'))
        a = object_detection(path=(os.path.join(UPLOAD_PATH+str(fd)+"/"+'images.jpg')),filename='image.jpg')
        shutil.move('image.jpg', os.path.join(UPLOAD_PATH+str(fd)+"/"+'image.jpg'))
        plat = OCR('./static/roi/image_1.jpg')
        with open("database.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            if len(plat) == 0: plat="Undetected"
            writer.writerow([fd,time.strftime("%d"),time.strftime("%b"),time.strftime("%Y"),f"/static/upload/{fd}/images.jpg",f"/static/upload/{fd}/image.jpg",plat])
        return render_template('index.html',upload=True,upload_image=str(fd)+"/images.jpg",text=plat,no=len(plat),idx=fd)
    return render_template('index.html',upload=False)

@app.route('/history',methods=['POST','GET'])
def history():
    rows = []
    M = None
    Y = 2023
    if request.method == 'POST':
        M = request.form['Month']
        Y = request.form['Year']
        print(M,Y)
        with open("database.csv", 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                if M and Y != None:
                    if M == "all": 
                        if row[3] == Y: rows.append(row)
                    elif row[2] == M and row[3] == Y:
                        rows.append(row)
                elif M != None:
                    if M == "all" or row[2] == M :
                        rows.append(row)
                elif Y != None:
                    if row[3] == Y:
                        rows.append(row)
    else :
        with open("database.csv", 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                rows.append(row)
    print(rows)
    return render_template('history.html',data=rows,M=M,Y=Y)

if __name__ =="__main__":
    app.run(debug=True)