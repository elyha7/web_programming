from flask import Flask
from flask import send_from_directory,Response,json,render_template,request
import postgresql
import cv2
import numpy as np
from PIL import Image
from sklearn.preprocessing import normalize
import io
from core.face_processor import FaceProcessor, get_vectors, find_closest
from core.database_utils import DataBase
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/imgs/'

processor = FaceProcessor()
db = DataBase()

@app.route('/', methods=['POST', 'GET'])
def login():
    return render_template('test.html')

@app.route('/imgs/<path:path>')
def send_js(path):
    return send_from_directory('imgs', path)

@app.route('/webcamjs/<path:path>')
def send_library(path):
    return send_from_directory('webcamjs', path)

@app.route('/test',methods=['POST', 'GET'])
def send_test():
    print(request.files,request.form,request.data)
    photo = request.files.get('webcam')
    name = request.form.get('name')
    img=np.array(Image.open(io.BytesIO(photo.read())))
    cv2.imwrite('1.jpg',img)
    return Response('complete', status=200, mimetype='application/text')

@app.route('/add_face', methods=['POST'])
def add_face():
    global processor,db
    photo = request.files.get('webcam')
    name = request.form.get('name')
    img=np.array(Image.open(io.BytesIO(photo.read())))
    cv2.imwrite('1.jpg',img)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    vec,ok = get_vectors(processor,img)
    if ok == -1:
        return Response('no faces found', status=400, mimetype='application/text')
    if len(vec) != 512:
        return Response('more than one face', status=400, mimetype='application/text')
    res = db.add_to_db(vec,name,check=True)
    if res[0] == 1:
        return Response(res[1], status=200, mimetype='application/text')
    if res[0] == -1:
        return Response(res[1], status=400, mimetype='application/text')

@app.route('/find_face', methods=['POST'])
def find_face():
    global processor,db
    photo = request.files.get('webcam')
    name = request.form.get('name')
    img=np.array(Image.open(io.BytesIO(photo.read())))
    cv2.imwrite('1.jpg',img)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    vec,ok = get_vectors(processor,img)
    if ok==-1:
        return Response('no faces found', status=400, mimetype='application/text')
    if len(vec)!=512:
        vec = vec[:512]
    res = db.find_closest(vec)
    print(res)
    if res[0] == 1:
        return Response(res[1], status=200, mimetype='application/text')
    else:
        return Response(res[1], status=400, mimetype='application/text')
@app.route('/clear_db',methods=['GET'])
def clear():
    global db
    #res = db.clear_db() 
    print('db cleared')
    return Response('ok', status=200, mimetype='application/text')
if __name__ == '__main__':
    app.run(host='127.0.0.1',port =5007,debug=True) 
