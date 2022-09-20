import pymysql
from flask import Flask,render_template,request,redirect,url_for
db_connection=None
db_cursor=None
app = Flask(__name__)



def db_connet():
    global db_connection,db_cursor
    try:
            db_connection = pymysql.connect(host="localhost",user="root",passwd="",database="bms",port=3306)
            print("Connected")
            db_cursor=db_connection.cursor()
            return True
    except:
        print("some error occure, cant connect to database")
        return False

def db_disconnect():
    global db_connection,db_cursor
    db_connection.close()
    db_cursor.close()

#function to fetch data from database
def getAllStudents():
    isConnected = db_connet()  
    if(isConnected):
        print("yes connected")
        getQuery = "select * from bank;"  #writting query
        db_cursor.execute(getQuery)           #executing query
        allData = db_cursor.fetchall()        #fetching data from query
        #print(allData)
        db_disconnect()
        return allData

@app.route("/")
def index():
    # return "hello python"
    allData = getAllStudents()
    return render_template("index.html",data=allData)    

@app.route("/add",methods=["GET","POST"])
def addStudent():
    if request.method == "POST":

        data=request.form
        name=data["name"]
        account_no=data["account_no"]
        pin=data["pin"]
        address=data["address"]
        phone=data["phone"]
        
        isConnected = db_connet()
        if(isConnected):
            insertQuery = "insert into bank(name,account_no,pin,address,phone)values(%s,%s,%s,%s,%s);"  #writting query
            db_cursor.execute(insertQuery,(name,account_no,pin,address,phone)) #executing query
            db_connection.commit()
            print("Data inserted")
            db_disconnect()
            return redirect(url_for("index"))
    return render_template("add.html")

def getStudentById(id):
    isConnected = db_connet()
    if(isConnected):
        selectQuery = "select * from bank where id=%s;"  #writting query
        db_cursor.execute(selectQuery,(id)) #executing query
        current_student=db_cursor.fetchone()
        db_connection.commit()
        db_disconnect()
        return current_student
    else:
        return False

def updateStudent(name,account_no,pin,address,phone,id):
    isConnected = db_connet()
    if(isConnected):
        updateQuery = "update bank set name=%s,account_no=%s,pin=%s,address=%s,phone=%s where id=%s;"  #writting query
        db_cursor.execute(updateQuery,(name,account_no,pin,address,phone,id)) #executing query
        db_connection.commit()
        db_disconnect()
        return True
    else:
        return False
@app.route("/update",methods=["GET","POST"])
def update():
    id=request.args.get("ID",type=int,default=1)
    print(id)
    actual_data = getStudentById(id)   
    #print(actual_data)
    
    if request.method=="POST":
        data=request.form
        print("data----->",data)
        isUpdated=updateStudent(data["name"],data["account_no"],data["pin"],data["address"],data["phone"],id) 
        if(isUpdated): 
            return redirect(url_for("index")) 
    return render_template("update.html",data=actual_data)

def deleteStudent(id):
    isConnected = db_connet()
    if(isConnected):
        deleteQuery = "delete from bank where id=%s ;"  #writting query
        db_cursor.execute(deleteQuery,(id)) #executing query
        db_connection.commit()
        db_disconnect()
        return True
    else:
        return False

@app.route("/delete")
def delete():
    id=request.args.get("ID",type=int,default=1)
    isDeleted=deleteStudent(id) 
    if(isDeleted): 
        return redirect(url_for("index")) 
    return render_template("index.html")           



if __name__=="__main__":
    app.run(debug=True)