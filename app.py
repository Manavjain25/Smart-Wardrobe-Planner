from flask import Flask, render_template, request, redirect, session
import random
from cv2 import cv2
import  pandas as pd
import numpy as np 
import tensorflow as tf
from tensorflow.keras.models import load_model
import mysql.connector
import os,shutil
from PIL import Image 
import matching_script as ms
import matching_online as mn
import occasion as oc
import online as on
import fil as fl
from sklearn.metrics.pairwise import cosine_similarity
import statistics

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
    Ethnic={}
    Casuals={}
    Formals={}

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
    
    if typ == "Ethnic":
        for i in Ethnic_upper:
            dummy={}
            for j in Ethnic_lower:
                k = ms.get_matching(i,j)
                if k and k[0] > 0.5:
                    dummy[j]=round(k[0]*100,2)
            Ethnic[i]=dummy

        Ethnic_list = Ethnic_upper + Ethnic_lower
        return render_template('occasion.html'  , Clothes = Ethnic_list , typ =typ, matched_dict =Ethnic)
    
    elif typ == "Casuals":
        for i in Casuals_upper:
            dummy={}
            for j in Casuals_lower:
                k = ms.get_matching(i,j)
                if k and k[0] > 0.5:
                    dummy[j]=round(k[0]*100,2)
            Casuals[i]=dummy
        Casuals_list = Casuals_upper + Casuals_lower
        return render_template('occasion.html'  , Clothes = Casuals_list , typ = typ, matched_dict=Casuals )
    
    elif typ == "Formals":
        for i in Formals_upper:
            dummy={}
            for j in Formals_lower:
                k = ms.get_matching(i,j)
                if k and k[0] > 0.5:
                    dummy[j]=round(k[0]*100,2)
            Formals[i] = dummy
        Formals_list = Formals_upper + Formals_lower
        return  render_template('occasion.html' ,  Clothes = Formals_list , typ =typ ,matched_dict = Formals)


    
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


@app.route('/online/<typ>',methods=['GET','POST'])
def online(typ):
    print(typ)
    res = on.data(typ,5)
    print(res)
    matched_dict={}
    matched_dict_len={}
    product = typ

    Shorts=os.listdir('static/wardrobe_users/{}/Shorts'.format(session['user_id']))
    Pants=os.listdir('static/wardrobe_users/{}/Pants'.format(session['user_id']))
    Tshirts=os.listdir('static/wardrobe_users/{}/T-shirts'.format(session['user_id']))
    Shirts=os.listdir('static/wardrobe_users/{}/Shirts'.format(session['user_id']))
    
    res= res[0:5]
    
    if product == "Shirt" or product== "T-shirt":
        for f in res:
            dummy = []
            for i in Shorts:
                k = mn.get_matching_upperurl(f,'static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i)
                if k and k[0] > 0.5:
                    m = 'static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i
                # matched_dict[m] = round(k[0]*100,2)
                    dummy.append(m)
            matched_dict[f]=dummy
            matched_dict_len[f]=len(dummy)

        for f in res:
            dummy1=[]
            for j in Pants:
                k =  mn.get_matching_upperurl(f,'static/wardrobe_users/'+session['user_id'] + '/Pants/'+j)
                if k and k[0] > 0.5:
                    m= 'static/wardrobe_users/'+session['user_id'] + '/Pants/'+j
                    # matched_dict[m]= round(k[0]*100,2)
                    dummy1.append(m)
            matched_dict[f]=dummy1
            matched_dict_len[f]=len(dummy1)

    elif product=="Jeans" or product== "Shorts":

        for f in res:
            dummy = []
            for i in Tshirts:
                k = mn.get_matching_lowerurl('static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i,f)
                if k and k[0] > 0.5:
                    m= 'static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i
                # matched_dict[m]= round(k[0]*100,2)
                    dummy.append(m)
            matched_dict[f]=dummy
            matched_dict_len[f]=len(dummy)

        for f in res:
            dummy1= []
            for j in Shirts:
                k = mn.get_matching_lowerurl('static/wardrobe_users/'+session['user_id'] + '/Shirts/'+j,f)
                if k and  k[0] > 0.5:
                    m= 'static/wardrobe_users/'+session['user_id'] + '/Shirts/'+j
                # matched_dict[m] =round(k[0]*100,2)
                    dummy1.append(m)
            matched_dict[f]=dummy1
            matched_dict_len[f]=len(dummy1)

        
    print(matched_dict)
    print(matched_dict_len)
    # This approach is giving error in runtime
    # for k,v in matched_dict_len.items():
    #     if v == 0:
    #         del matched_dict_len[k]

        

    m = { k:v for k, v in matched_dict_len.items() if v } #Dict Comprehension
    embedding_model= load_model('static/embeding_model/embeding_model.h5', compile=False)
    wardrobe_list=[]
        
    if product=="Shirt":
        for i in Shirts:
            wardrobe_list.append(ms.get_embedding(embedding_model,'static/wardrobe_users/'+session['user_id'] + '/Shirts/'+i))
    elif product=="T-shirt":
        for i in Tshirts:
            wardrobe_list.append(ms.get_embedding(embedding_model,'static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i))
    elif product=="Jeans":
        for i in Pants:
            wardrobe_list.append(ms.get_embedding(embedding_model,'static/wardrobe_users/'+session['user_id'] + '/Pants/'+i))
    else:
        for i in Shorts:
            wardrobe_list.append(ms.get_embedding(embedding_model,'static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i))
    
    print("wardobe shape",np.asarray(wardrobe_list).shape)
    
    matched_dict_similar={}
    for cloth in m.keys():
        cloth_embedding=mn.get_embedding_url(embedding_model,cloth)
        print(cloth_embedding,"shape",cloth_embedding.shape)
        print(wardrobe_list)
        similarities=cosine_similarity(np.asarray([cloth_embedding]),np.asarray(wardrobe_list))
        print("sim",similarities)
        print("sim1",similarities[0])
        x=statistics.mean(similarities[0])
        matched_dict_similar[cloth]=x

        print("----------matched_dict_len_embedding--------------")
        print(matched_dict_similar)


    d = dict(sorted(matched_dict_similar.items(), key=lambda x: x[1], reverse=True))
    # new_dict1 = {k:v for k, v in m.items() if k in d.keys()}
    # print("Manav")
    # print(new_dict1)
    new_dict={}
    # for i in d.keys():
    #     new_dict[i]=m[i]
    
    for i,v in d.items():
        new_dict[i] = [m[i],round(v*100,2)]

    # print("Atharva")
    print(new_dict)
    filters={"Shirt":{"brands":["Scott International","Allen Solly","AWG ALL WEATHER GEAR","Van Heusen","EYEBOGLER"],"sizes":["S","M","L","XL"],"colours":["Black","Brown","Red","Green","Blue"],"materal":["Cotton","Denim","Linen","Rayon","Synthetic"]}
    ,"T-shirt":{"brands":["Allen Solly","Louis Philippe","Arrow","Van Heusen","Peter England"],"sizes":["S","M","L","XL"],"colours":["Black","Brown","Red","Green","Blue"],"materal":["Cotton","Denim","Linen","Rayon","Synthetic"]}
    ,"Jeans":{"brands":["Levi's","Pepe Jeans","Spykar","Tommy Hilfiger","KILLER"],"sizes":["S","M","L","XL"],"colours":["Black","Brown","Red","Green","Blue"],"materal":["Cotton","Denim","Linen","Rayon","Synthetic"]},
    "Shorts":{"brands":["Reebok","Jockey","SHIV NARESH","Veirdo","Adidas"],"sizes":["S","M","L","XL"],"colours":["Black","Brown","Red","Green","Blue"],"materal":["Cotton","Denim","Linen","Rayon","Synthetic"]}}

    return render_template('online.html',matched_dict = matched_dict , matched_dict_len =new_dict,fil = filters[product],product =product)

@app.route('/filter',methods=['GET','POST'])
def fil():
    if request.method == "POST":
        brand1 = request.form.get('brand')
        size = request.form.get('size')
        colour = request.form.get('colour')
        material = request.form.get('material')
        cloth = request.form.get('cloth')
        brand=""
        for i in brand1:
            if i==" ":
                brand+='+'
            else:
                brand+=i
    
        # print("{},{},{},{},{}".format(brand,size,colour,material,cloth))

        res =  fl.data(cloth,brand,size,colour,material)
        # print(res)

        matched_dict={}
        matched_dict_len={}
        product = cloth

        Shorts=os.listdir('static/wardrobe_users/{}/Shorts'.format(session['user_id']))
        Pants=os.listdir('static/wardrobe_users/{}/Pants'.format(session['user_id']))
        Tshirts=os.listdir('static/wardrobe_users/{}/T-shirts'.format(session['user_id']))
        Shirts=os.listdir('static/wardrobe_users/{}/Shirts'.format(session['user_id']))
        
        res= res[0:5]
        
        if product == "Shirt" or product== "T-shirt":
            for f in res:
                dummy = []
                for i in Shorts:
                    k = mn.get_matching_upperurl(f,'static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i)
                    if k and k[0] > 0.5:
                        m = 'static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i
                    # matched_dict[m] = round(k[0]*100,2)
                        dummy.append(m)
                matched_dict[f]=dummy
                matched_dict_len[f]=len(dummy)

            for f in res:
                dummy1=[]
                for j in Pants:
                    k =  mn.get_matching_upperurl(f,'static/wardrobe_users/'+session['user_id'] + '/Pants/'+j)
                    if k and k[0] > 0.5:
                        m= 'static/wardrobe_users/'+session['user_id'] + '/Pants/'+j
                        # matched_dict[m]= round(k[0]*100,2)
                        dummy1.append(m)
                matched_dict[f]=dummy1
                matched_dict_len[f]=len(dummy1)

        elif product=="Jeans" or product== "Shorts":

            for f in res:
                dummy = []
                for i in Tshirts:
                    k = mn.get_matching_lowerurl('static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i,f)
                    if k and k[0] > 0.5:
                        m= 'static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i
                    # matched_dict[m]= round(k[0]*100,2)
                        dummy.append(m)
                matched_dict[f]=dummy
                matched_dict_len[f]=len(dummy)
            
            for f in res:
                dummy1= []
                for j in Shirts:
                    k = mn.get_matching_lowerurl('static/wardrobe_users/'+session['user_id'] + '/Shirts/'+j,f)
                    if k and  k[0] > 0.5:
                        m= 'static/wardrobe_users/'+session['user_id'] + '/Shirts/'+j
                    # matched_dict[m] =round(k[0]*100,2)
                        dummy1.append(m)
                matched_dict[f]=dummy1
                matched_dict_len[f]=len(dummy1)

        print("-----Matched_dict-------")    
        print(matched_dict)

        print("------------Matched_dict_len-------")
        print(matched_dict_len)
        embedding_model= load_model('static/embeding_model/embeding_model.h5', compile=False)
        wardrobe_list=[]
        
        if product=="Shirt":
            for i in Shirts:
                wardrobe_list.append(ms.get_embedding(embedding_model,'static/wardrobe_users/'+session['user_id'] + '/Shirts/'+i))
        elif product=="T-shirt":
            for i in Tshirts:
                wardrobe_list.append(ms.get_embedding(embedding_model,'static/wardrobe_users/'+session['user_id'] + '/T-shirts/'+i))
        elif product=="Jeans":
            for i in Pants:
                wardrobe_list.append(ms.get_embedding(embedding_model,'static/wardrobe_users/'+session['user_id'] + '/Pants/'+i))
        else:
            for i in Shorts:
                wardrobe_list.append(ms.get_embedding(embedding_model,'static/wardrobe_users/'+session['user_id'] + '/Shorts/'+i))
        print("wardobe shape",np.asarray(wardrobe_list).shape)
        
            
        # This approach is giving error in runtime
        # for k,v in matched_dict_len.items():
        #     if v == 0:
        #         del matched_dict_len[k]

        m = { k:v for k, v in matched_dict_len.items() if v } #Dict Comprehension

        matched_dict_similar={}
        for cloth in m.keys():
            cloth_embedding=mn.get_embedding_url(embedding_model,cloth)
            print(cloth_embedding,"shape",cloth_embedding.shape)
            print(wardrobe_list)
            similarities=cosine_similarity(np.asarray([cloth_embedding]),np.asarray(wardrobe_list))
            print("sim",similarities)
            print("sim1",similarities[0])
            x=statistics.mean(similarities[0])
            matched_dict_similar[cloth]=x

        print("----------matched_dict_len_embedding--------------")
        print(matched_dict_similar)

        d = dict(sorted(matched_dict_similar.items(), key=lambda x: x[1], reverse=True))
        # print(d)
        new_dict={}
        for i,v in d.items():
            new_dict[i] = [m[i],round(v*100,2)]

        filters={"Shirt":{"brands":["Scott International","Allen Solly","AWG ALL WEATHER GEAR","Van Heusen","EYEBOGLER"],"sizes":["S","M","L","XL"],"colours":["Black","Brown","Red","Green","Blue"],"materal":["Cotton","Denim","Linen","Rayon","Synthetic"]}
        ,"T-shirt":{"brands":["Allen Solly","Louis Philippe","Arrow","Van Heusen","Peter England"],"sizes":["S","M","L","XL"],"colours":["Black","Brown","Red","Green","Blue"],"materal":["Cotton","Denim","Linen","Rayon","Synthetic"]}
        ,"Jeans":{"brands":["Levi's","Pepe Jeans","Spykar","Tommy Hilfiger","KILLER"],"sizes":["S","M","L","XL"],"colours":["Black","Brown","Red","Green","Blue"],"materal":["Cotton","Denim","Linen","Rayon","Synthetic"]},
        "Shorts":{"brands":["Reebok","Jockey","SHIV NARESH","Veirdo","Adidas"],"sizes":["S","M","L","XL"],"colours":["Black","Brown","Red","Green","Blue"],"materal":["Cotton","Denim","Linen","Rayon","Synthetic"]}}
    
    return render_template('online.html',matched_dict = matched_dict , matched_dict_len =new_dict,fil = filters[product],product =product)
    # return redirect('/your_closet')

@app.route('/delete', methods=['POST'])
def delete():
    if request.method=='POST':
        print("in")
        print(request)
        m = request.form["id"]
        print(m)
        os.remove(m)

    return redirect('/your_closet')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__ == "__main__":
    # init()
    app.run(debug=True)