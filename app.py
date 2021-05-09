from flask import Flask, Response,render_template,request
import cv2
from AI import *
app = Flask(__name__)


video = cv2.VideoCapture(0)
dim=(500,500)
Dict={}
List_x=[0,0,0]
List_flag=[0,0,0,0,0]
q=1
o=5
penalties=0
question=[['11.jpg','12.jpg','13.jpg','14.jpg','10.jpg'],['21.jpg','22.jpg','23.jpg','24.jpg','20.jpg'],['31.jpg','32.jpg','33.jpg','34.jpg','30.jpg']]
solution=[2,2,2]
option=[5,5,5]

for i in range(len(question)):
    Dict[i+1]={}
    for j in range(5):
        img=cv2.imread('./asset/'+question[i][j])
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        Dict[i+1][j+1]=resized


def dope(x,List):
    List.append(x)
    List=List[1:]
    if List==[x]*len(List):
    	List=[0]*len(List)
    else:
        x=0
    return x,List
    
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/', methods=['POST', 'GET'])
def get_data():
        if request.method == 'POST':
                name = request.form['name']
                email= request.form['email']
                return render_template('index.html')

def gen(video):
    while True:
        global q,o,List_flag,List_x,penalties,option
        flag,frame_ = video.read()
        x,flag,frame_ = update(frame_)
        x,List_x=dope(x,List_x)
        #flag,List_flag=dope(flag,List_flag)
        if flag:
            penalties+=1
        if x ==0:
            pass
        elif x==6:
            if q>1:
                q-=1
        elif x==7:
            if q<len(question):
                q+=1
        else:
            option[q-1]=x
        resized = cv2.resize(frame_, dim, interpolation = cv2.INTER_AREA)
        im_v=cv2.hconcat([resized,Dict[q][option[q-1]]])
        ret, jpeg = cv2.imencode('.jpg', im_v)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/results')
def results():
    global solution,option,penalties
    score=0
    total=30
    for i in range(3):
    	if option[i]==5:
    	    pass
    	elif option[i]==solution[i]:
    	    score+=10
    	else:
    	    score-=2
    score-=penalties 
    
    return render_template('results.html',score=score,total=total,penalty=penalties)

if __name__ == '__main__':
    app.run(threaded=True)
