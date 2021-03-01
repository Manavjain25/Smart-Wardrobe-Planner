from flask import Flask, render_template, request, redirect, session
import random
from cv2 import cv2
import  pandas as pd
import numpy as np 
# import tensorflow as tf
import tensorflow as tf
# from keras.preprocessing.image import load_img
# from keras.preprocessing.image import img_to_array
# from keras.models import load_model
from tensorflow.keras.models import load_model
import mysql.connector
import os,shutil
from PIL import Image 
import matching_script as ms
import occasion as oc


app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost", user="root" ,password="", database="wardrobe_users")
cursor=conn.cursor()

classification_loaded_model = load_model('Clothes Classification/class_model.h5')
def classfiy_image(img):
    print(img)
    img=cv2.imread(img)
    img=cv2.GaussianBlur(img,(3,3),9)
    img=cv2.resize(img,(128,128),cv2.INTER_AREA)
    img=img/255
    x=[]
    x.append(img)
    x=np.asarray(x)
    prediction=classification_loaded_model.predict_classes(x,True,None)
    return prediction[0]

# app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
# ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# def init():
#     global graph
    # graph = tf.get_default_graph()

@app.route('/')
def login_SignUp():
    return render_template('login_SignUp.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    return redirect('/')

@app.route('/occasion/<typ>', methods=['GET','POST'])
def occasion(typ):
    print(typ)
   
    # print(request.form.get("occasion"))
       
    Tshirts=os.listdir('static/wardrobe_users/{}/T-shirts'.format(session['user_id']))
    Shirts=os.listdir('static/wardrobe_users/{}/Shirts'.format(session['user_id']))
    Shorts=os.listdir('static/wardrobe_users/{}/Shorts'.format(session['user_id']))
    Pants=os.listdir('static/wardrobe_users/{}/Pants'.format(session['user_id']))
    user=session['user_id']
    Ethnic_upper=[]
    Ethnic_lower=[]
    Casuals_upper=[]
    Casuals_lower=[]
    Formals_upper=[]
    Formals_lower=[]

    
     
      
    for i in Tshirts:
        m = oc.kunal('static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i)
        if m =="ethnic":
            Ethnic_upper.append('static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i)
        elif m=="cassual":
            Casuals_upper.append('static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i)
        elif m=="formal":
            Formals_upper.append('static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i)
        else:
            pass

    for i in Shirts:
        m = oc.kunal('static/wardrobe_users/'+session['user_id'] + '/Shirts/'+i)
        if m =="ethnic":
            Ethnic_upper.append('static/wardrobe_users/'+session['user_id'] + '/Shirts/'+i)
        elif m=="cassual":
            Casuals_upper.append('static/wardrobe_users/'+session['user_id'] + '/Shirts/'+i)
        elif m=="formal":
            Formals_upper.append('static/wardrobe_users/'+session['user_id'] + '/Shirts/'+i)
        else:
            pass

    for i in Pants:
        m = oc.kunal('static/wardrobe_users/'+session['user_id'] + '/Pants/'+i)
        if m =="ethnic":
            Ethnic_lower.append('static/wardrobe_users/'+session['user_id'] + '/Pants/'+i)
        elif m=="cassual":
            Casuals_lower.append('static/wardrobe_users/'+session['user_id'] + '/Pants/'+i)
        elif m=="formal":
            Formals_lower.append('static/wardrobe_users/'+session['user_id'] + '/Pants/'+i)
        else:
            pass
    
    for i in Shorts:
        m = oc.kunal('static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i)
        if m =="ethnic":
            Ethnic_lower.append('static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i)
        elif m=="cassual":
            Casuals_lower.append('static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i)
        elif m=="formal":
            Formals_lower.append('static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i)
        else:
            pass
    
    Ethnic_matched=[ [] for i in range(0,len(Ethnic_upper))]
    m=0
    for i in Ethnic_upper:
        for j in Ethnic_lower:
            k = ms.get_matching(i,j)
            if k and k[0] > 0.5:
                Ethnic_matched[m].append(j)
        m+=1

    Casuals_matched=[[] for i in range(0,len(Casuals_upper))]
    m=0
    for i in Casuals_upper:
        for j in Casuals_lower:
            k = ms.get_matching(i,j)
            if k and k[0] > 0.5:
                Casuals_matched[m].append(j)
        m+=1

    Formals_matched=[[] for i in range(0,len(Formals_upper))]
    m=0
    for i in Formals_upper:
        for j in Formals_lower:
            k = ms.get_matching(i,j)
            if k and k[0] > 0.5:
                Formals_matched[m].append(j)
        m+=1 
    
    Ethnic = Ethnic_upper + Ethnic_lower
    Casuals = Casuals_upper + Casuals_lower
    Formals = Formals_upper + Formals_lower
   
    if typ == "Ethnic":
        return render_template('occasion.html' ,Final_array =Ethnic_matched , Upper = Ethnic_upper , length=len(Ethnic_upper) , Clothes = Ethnic , typ =typ)
    elif typ == "Casuals":
        return render_template('occasion.html' ,Final_array =Casuals_matched ,Upper = Casuals_upper , length = len(Casuals_upper) , Clothes = Casuals , typ = typ )
    elif typ == "Formals":
        return  render_template('occasion.html' ,Final_array =Formals_matched ,Upper= Formals_upper , length = len(Formals_upper), Clothes = Formals , typ =typ )


    
@app.route('/Check_Matching', methods=['GET','POST'])
def Check_Matching():
    matched_dict={}

    if request.method=='POST':
        image = request.files['user_image']
        Image= request.files['user_image']
        print(image)
        
        f = 'static\\folder\\'+ image.filename
        image.save(f)

        class_prediction=classfiy_image(f)
        if class_prediction==0:
            product="T-shirts"
        elif class_prediction==1:
            product="Shirts"
        elif class_prediction==2:
            product="Shorts"
        elif class_prediction==3:
            product="Pants"
        elif class_prediction==4:
            product="Jackets"

            
        print(product)
        
        
        if product == "Shirts" or product== "T-shirts":
            Shorts=os.listdir('static/wardrobe_users/{}/Shorts'.format(session['user_id']))
            Pants=os.listdir('static/wardrobe_users/{}/Pants'.format(session['user_id']))

            for i in Shorts:
                k = ms.get_matching(f,'static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i)
                if k and k[0] > 0.5:
                    m = 'static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i
                    matched_dict[m] = round(k[0]*100,2)

            for j in Pants:
                k =  ms.get_matching(f,'static/wardrobe_users/'+session['user_id'] + '/Pants/'+j)
                if k and k[0] > 0.5:
                    m= 'static/wardrobe_users/'+session['user_id'] + '/Pants/'+j
                    matched_dict[m]= round(k[0]*100,2)


        elif product=="Pants" or product== "Shorts":
            Tshirts=os.listdir('static/wardrobe_users/{}/T-shirts'.format(session['user_id']))
            Shirts=os.listdir('static/wardrobe_users/{}/Shirts'.format(session['user_id']))
            
            for i in Tshirts:
                k = ms.get_matching('static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i,f)
                if k and k[0] > 0.5:
                    m= 'static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i
                    matched_dict[m]= round(k[0]*100,2)

            for j in Shirts:
                k = ms.get_matching('static/wardrobe_users/'+session['user_id'] + '/Shirts/'+j,f)
                if k and  k[0] > 0.5:
                    m= 'static/wardrobe_users/'+session['user_id'] + '/Shirts/'+j
                    matched_dict[m] =round(k[0]*100,2)

        
        print(matched_dict)
        d = dict(sorted(matched_dict.items(), key=lambda x: x[1], reverse=True))
        

        
        return render_template('Matching.html', f=f , matched_dict = d)

    return render_template('Matching.html',f="https://www.google.com/imgres?imgurl=https%3A%2F%2Ficon-library.com%2Fimages%2Ffashion-icon-png%2Ffashion-icon-png-2.jpg&imgrefurl=https%3A%2F%2Ficon-library.com%2Ficon%2Ffashion-icon-png-2.html&tbnid=iRTKHeVZXJP7wM&vet=10CBQQMyhwahcKEwjo0tjLk-7uAhUAAAAAHQAAAAAQAg..i&docid=iW9zkMagg3a-KM&w=980&h=600&q=dummy%20clothes%20icon&ved=0CBQQMyhwahcKEwjo0tjLk-7uAhUAAAAAHQAAAAAQAg")




@app.route('/your_closet', methods=['GET', 'POST'])
def your_closet():
    if request.method=='POST':
        image = request.files['user_image']
        Image= request.files['user_image']
        print(image)
        # os.mkdir('static')
        # file_saved=os.path.join('static\dummy',image.filename)
        n = 'static\\dummy\\'+ image.filename
        # m = os.path.join('static\temp',image.filename)
        # print(n)
        image.save(n) 

        # file_saved=os.path.join('static\wardrobe_users',image.filename)
        # image.save(file_saved)
  
        
        class_prediction=classfiy_image(n)
        if class_prediction==0:
            product="T-shirts"
        elif class_prediction==1:
            product="Shirts"
        elif class_prediction==2:
            product="Shorts"
        elif class_prediction==3:
            product="Pants"
        elif class_prediction==4:
            product="Jackets"

            
        # print(product)

        m = file_path=os.path.join('static\wardrobe_users\{}\{}'.format(session['user_id'],product),image.filename)
        shutil.move(n, m)
        # image.save(m)  

        # print(image)
        # file_path=os.path.join('static\wardrobe_users\{}\{}'.format(session['user_id'],product),image.filename)
        # print(file_path)
        # m= 'static\\wardrobe_users\\'+image.filename
        # image.save(n)
        # print(file_path)
        # os.remove(file_saved)
        # image.save(ENTER FILE WHERE YOU WANT TO SAVE IMAGE)

    Tshirts=os.listdir('static/wardrobe_users/{}/T-shirts'.format(session['user_id']))
    Shirts=os.listdir('static/wardrobe_users/{}/Shirts'.format(session['user_id']))
    Shorts=os.listdir('static/wardrobe_users/{}/Shorts'.format(session['user_id']))
    Pants=os.listdir('static/wardrobe_users/{}/Pants'.format(session['user_id']))
    Jackets=os.listdir('static/wardrobe_users/{}/Jackets'.format(session['user_id']))
    user=session['user_id']
    
    print(user)

    return render_template('your_closet.html', Tshirts=Tshirts, Shirts=Shirts, Shorts=Shorts, Pants=Pants, Jackets=Jackets, user=user)



    

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute(""" SELECT * from `users` where `email` LIKE '{}' and `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][1]
        if 'user_id' in session:
        # return render_template('home.html')
            return redirect('/your_closet')
    return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    username=request.form.get('username')
    email=request.form.get('s_email')
    password=request.form.get('s_password')

    cursor.execute("""INSERT INTO `users`(`username`, `email`, `password`) VALUES ('{}', '{}', '{}')""".format(username,email,password))
    conn.commit()

    cursor.execute(""" SELECT * from `users` where `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][1]
    os.makedirs('static/wardrobe_users/{}'.format(email))
    os.makedirs('static/wardrobe_users/{}/T-shirts'.format(email))
    os.makedirs('static/wardrobe_users/{}/Shirts'.format(email))
    os.makedirs('static/wardrobe_users/{}/Shorts'.format(email))
    os.makedirs('static/wardrobe_users/{}/Pants'.format(email))
    os.makedirs('static/wardrobe_users/{}/Jackets'.format(email))
    return redirect('/your_closet')




@app.route('/delete' , methods=['POST'])
def delete():
    if request.method=='POST':
        print("in")
        print(request)
        m = request.form["id"]
        print(m)
        os.remove(m)


    Tshirts=os.listdir('static/wardrobe_users/{}/T-shirts'.format(session['user_id']))
    Shirts=os.listdir('static/wardrobe_users/{}/Shirts'.format(session['user_id']))
    Shorts=os.listdir('static/wardrobe_users/{}/Shorts'.format(session['user_id']))
    Pants=os.listdir('static/wardrobe_users/{}/Pants'.format(session['user_id']))
    Jackets=os.listdir('static/wardrobe_users/{}/Jackets'.format(session['user_id']))
    user=session['user_id']
    
    print(Tshirts)
    
    return render_template('your_closet.html', Tshirts=Tshirts, Shirts=Shirts, Shorts=Shorts, Pants=Pants, Jackets=Jackets, user=user)
    
    # return redirect('/your_closet')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__ == "__main__":
    # init()
    app.run(debug=True)