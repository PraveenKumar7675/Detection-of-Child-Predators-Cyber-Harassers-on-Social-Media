from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
import matplotlib.pyplot as plt
import re
import numpy as np
from sklearn import svm
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import nltk
from nltk.corpus import stopwords
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn_extensions.extreme_learning_machines.elm import GenELMClassifier
from sklearn_extensions.extreme_learning_machines.random_layer import RBFRandomLayer, MLPRandomLayer
from sklearn.linear_model import LogisticRegression
from django.core.files.storage import FileSystemStorage
import datetime
from numpy.linalg import norm
from numpy import dot

global classifier
global label_count
global X
global Y
corpus = []

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def SendPost(request):
    if request.method == 'GET':
       return render(request, 'SendPost.html', {})
    
def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def AddCyberMessages(request):
    if request.method == 'GET':
       return render(request, 'AddCyberMessages.html', {})

def RunAlgorithms(request):
    if request.method == 'GET':
       return render(request, 'RunAlgorithms.html', {})

def MonitorPost(request):
    if request.method == 'GET':
       strdata = '<table border=1 align=center width=100%><tr><th>Sender Name</th><th>File Name</th><th>Message</th><th>Post Time</th> <th>Status</th></tr><tr>'
       con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'cyber',charset='utf8')
       with con:
          cur = con.cursor()
          cur.execute("select * FROM posts")
          rows = cur.fetchall()
          for row in rows: 
             strdata+='<td>'+str(row[0])+'</td><td><img src=/static/photo/'+str(row[1])+' width=200 height=200></img></td><td>'+str(row[2])+'</td><td>'+str(row[3])+'</td><td>'+str(row[4])+'</td></tr>'
    context= {'data':strdata}
    return render(request, 'MonitorPost.html', context)
    
def AddBullyingWords(request):
    if request.method == 'POST':
      message = request.POST.get('t1', False)
      label = request.POST.get('t2', False)
      message = message.strip('\n')
      message = message.strip()
      message = message.lower()
      message = re.sub(r'[^a-zA-Z\s]+', '', message)
      file = open('dataset.txt','a+')
      file.write(message+","+label+"\n")
      file.close()
      context= {'data':'Cyber Words added to dataset as '+label}
      return render(request, 'AddCyberMessages.html', context)
    
def Signup(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      contact = request.POST.get('t3', False)
      email = request.POST.get('t4', False)
      address = request.POST.get('t5', False)
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'cyber',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO users(username,password,contact_no,email,address,status) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"','Accepted')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)    


def UserLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      index = 0
      con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'cyber',charset='utf8')
      with con:    
          cur = con.cursor()
          cur.execute("select * FROM users")
          rows = cur.fetchall()
          for row in rows: 
             if row[0] == username and password == row[1] and row[5] == 'Accepted':
                index = 1
                break		
      if index == 1:
       file = open('session.txt','w')
       file.write(username)
       file.close()   
       context= {'data':'welcome '+username}
       return render(request, 'UserScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Login.html', context)

def AdminLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'admin' and password == 'admin':
       context= {'data':'welcome '+username}
       return render(request, 'AdminScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Admin.html', context)
    
def ViewUsers(request):
    if request.method == 'GET':
       color='<font size="" color=black>'
       strdata = '<table border=1 align=center width=100%><tr><th>Username</th><th>Password</th><th>Contact No</th><th>Email ID</th><th>Address</th><th>Status</th></tr><tr>'
       con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'cyber',charset='utf8')
       with con:
          cur = con.cursor()
          cur.execute("select * FROM users")
          rows = cur.fetchall()
          for row in rows: 
             strdata+='<td>'+color+row[0]+'</td><td>'+color+row[1]+'</td><td>'+color+row[2]+'</td><td>'+color+str(row[3])+'</td><td>'+color+str(row[4])+'</td><td>'+color+row[5]+'</td></tr>'
    context= {'data':strdata+'</table><br/><br/><br/>'}
    return render(request, 'ViewUsers.html', context)


def ViewUserPost(request):
    if request.method == 'GET':
       strdata = '<table border=1 align=center width=100%><tr><th>Sender Name</th><th>File Name</th><th>Message</th><th>Post Time</th> <th>Status</th></tr><tr>'
       con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'cyber',charset='utf8')
       with con:
          cur = con.cursor()
          cur.execute("select * FROM posts")
          rows = cur.fetchall()
          for row in rows: 
             strdata+='<td>'+str(row[0])+'</td><td><img src=/static/photo/'+str(row[1])+' width=200 height=200></img></td><td>'+str(row[2])+'</td><td>'+str(row[3])+'</td><td>'+str(row[4])+'</td></tr>'
    context= {'data':strdata}
    return render(request, 'ViewUserPost.html', context)

def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts
def prediction(X_test, cls):  #prediction done here
    y_pred = cls.predict(X_test) 
    for i in range(len(X_test)):
      print("X=%s, Predicted=%s" % (X_test[i], y_pred[i]))
    return y_pred

def cal_accuracy(y_test, y_pred, details):
    msg = ''
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test,y_pred)*100
    msg+=details+"<br/>"
    msg+="Accuracy : "+str(accuracy)+"<br/>"
    #msg+="Report : "+str(classification_report(y_test, y_pred))+"<br/>"
    #msg+="Confusion Matrix : "+str(cm)+"<br/>"
    return msg

def classifyPost(vec1, vec2):
    vector1 = np.asarray(vec1)
    vector2 = np.asarray(vec2)
    return dot(vector1, vector2)/(norm(vector1)*norm(vector2))

def PostSent(request):
    if request.method == 'POST' and request.FILES['t2']:
        output = ''
        myfile = request.FILES['t2']
        msg = request.POST.get('t1', False)
        fs = FileSystemStorage()
        filename = fs.save('E:/venkat/2021/May21/Cyber/CyberBullying/static/photo/'+str(myfile), myfile)
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        text = 'msg,label\n'+msg+",?"
        f = open("test.txt", "w")
        f.write(text)
        f.close()
        df = pd.read_csv('test.txt') 
        X1 = df.iloc[:, :-1].values

        dataset = ''            
        for k in range(len(corpus)):
            dataset+=corpus[k]+","

        dataset = dataset[0:len(dataset)-1]
        dataset+="\n"

        for i in range(len(X1)):
            line = str(X1[i]).strip('\n')
            line = line.strip()
            line = line.lower()
            line = re.sub(r'[^a-zA-Z\s]+', '', line)
            print(line)
            wordCount = word_count(line.strip())
            value = ''
            for j in range(len(corpus)):
                if corpus[j] in wordCount.keys():
                    value+=str(wordCount[corpus[j]])+","
                else:
                    value+="0,"
            value = value[0:len(value)-1]        
            dataset+=value+"\n"
    
        print(dataset)
        f = open("test.txt", "w")
        f.write(dataset)
        f.close()
        test = pd.read_csv("test.txt")
        X1 = test.values[:, 0:label_count]
        result = classifier.predict(X1)
        #classify = 0
        #score = 0
        #for i in range(len(X)):
        #    cosine = classifyPost(X[i], X1)
         #   if cosine > score:
        #        score = cosine
        #        classify = Y[i]
        status = 'Non-Cyber Harassers'
        print(result)
        if result[0] == 0:
            status = 'Non-Cyber Harassers'
        else:
            status = 'Cyber Harassers'

        user = ''
        with open("session.txt", "r") as file:
          for line in file:
             user = line.strip('\n')    
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'cyber',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO posts(sender,filename,msg,posttime,status) VALUES('"+user+"','"+str(myfile)+"','"+msg+"','"+current_time+"','"+status+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Posts details added'}
            return render(request, 'SendPost.html', context)
        else:
            context= {'data':'Error in adding post details'}
            return render(request, 'SendPost.html', context) 
        
def RunAlgorithm(request):
    global classifier
    global label_count
    global X
    global Y
    msg = ''
    if request.method == 'POST':
      name = request.POST.get('t1', False)
      stop_words = set(stopwords.words('english'))
      corpus.clear()
      posts = []
      df = pd.read_csv('dataset.txt') 
      X = df.iloc[:, :-1].values 
      Y = df.iloc[:, -1].values
      for i in range(len(Y)):
          if Y[i] == 'Non-Bullying':
              Y[i] = 0
          else:
              Y[i] = 1

      for i in range(len(X)):
          line = str(X[i]).strip('\n')
          line = line.strip()
          line = line.lower()
          line = re.sub(r'[^a-zA-Z\s]+', '', line)
          arr = line.split(" ")
          for k in range(len(arr)):
              word = arr[k].strip("\n").strip()
              if len(word) > 2 and word not in corpus and word not in stop_words:
                  corpus.append(word)
          posts.append(line)        
          dataset = ''
      for k in range(len(corpus)):
          dataset+=corpus[k]+","
      dataset+='Label\n'        

      for k in range(len(posts)):
          text = posts[k];
          wordCount = word_count(text.strip())
          for j in range(len(corpus)):
              if corpus[j] in wordCount.keys():
                  dataset+=str(wordCount[corpus[j]])+","
              else:
                  dataset+="0,"
          dataset+=str(Y[k])+"\n"

      f = open("features.txt", "w")
      f.write(dataset)
      f.close()

      train = pd.read_csv("features.txt")
      cols = train.shape[1]
      features = cols - 2
      label = cols - 1
      label_count = label
      X = train.values[:, 0:label] 
      Y = train.values[:, label]
      print(Y)
      X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

      
      output = ""
      if name == "SVM Algorithm":
          cls = svm.SVC(C=2.0,gamma='scale',kernel = 'rbf', random_state = 2)
          cls.fit(X_train, y_train) 
          prediction_data = prediction(X_test, cls)
          msg = cal_accuracy(y_test, prediction_data,'SVM Accuracy')
          output = 'SVM Algorithm Output details<br/><br/>'+msg
          classifier = cls

      if name == "Decision Tree":
          cls = DecisionTreeClassifier(max_depth=None, min_samples_split=2,random_state=0) 
          cls.fit(X_train, y_train) 
          prediction_data = prediction(X_test, cls)
          msg = cal_accuracy(y_test, prediction_data,'Decision Tree Accuracy')
          output = 'Decision Tree Algorithm Output details<br/><br/>'+msg

      if name == "KNearest Neighbors":
          cls = BaggingClassifier(KNeighborsClassifier(),max_samples=0.5, max_features=0.5)
          cls.fit(X_train, y_train) 
          prediction_data = prediction(X_test, cls)
          msg = cal_accuracy(y_test, prediction_data,'KNearest Neighbor Accuracy')
          output = 'KNearest Neighbor Algorithm Output details<br/><br/>'+msg

      if name == "Random Forest":
          cls = RandomForestClassifier(n_estimators=1,max_depth=0.9,random_state=None)
          cls.fit(X_train, y_train) 
          prediction_data = prediction(X_test, cls)
          msg = cal_accuracy(y_test, prediction_data,'Random Forest Accuracy')
          output = 'Random Forest Algorithm Output details<br/><br/>'+msg

      if name == "Naive Bayes":
          cls = MultinomialNB()
          cls.fit(X_train, y_train) 
          prediction_data = prediction(X_test, cls)
          msg = cal_accuracy(y_test, prediction_data,'Naive Bayes Accuracy')
          output = 'Naive Bayes Algorithm Output details<br/><br/>'+msg

      
      context= {'data':''+output}   
      return render(request, 'RunAlgorithms.html', context)    
    



    
