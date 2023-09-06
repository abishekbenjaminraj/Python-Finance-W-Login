from flask import Flask,render_template,request,session,url_for,redirect
import sqlite3 as sql

app=Flask(__name__)

app.secret_key="abi123"

# def isloggedin():
#     return "username" in session

@app.route('/',methods=["GET","POST"])
def login():
    if request.method == "POST":
        conn=sql.connect("user.db")
        curr=conn.cursor()
        username=request.form.get("name")
        password=request.form.get("pass")
        curr.execute("SELECT * FROM DETAILS WHERE name=? and password=?",(username,password))
        results=curr.fetchall()
        for i in results:
            if username in i and password == i[1]:
                session["username"] = username
                return redirect(url_for("home"))
            else:
                return "Invalid Credentials"
        # if len(results)==0:
        #     return "Sorry Invalid Credentials.Try Again"
        # else:
        #     return render_template("index.html")
    return render_template("login.html")

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "POST":
        conn=sql.connect("user.db")
        curr=conn.cursor()
        curr.execute("INSERT INTO DETAILS (name,password) VALUES (?,?)",(request.form.get("name_1"),request.form.get("pass_1")))
        conn.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/a')
def home():
        if "username" in session:
            conn=sql.connect("user.db")
            conn.row_factory=sql.Row
            curr=conn.cursor()
            curr.execute("SELECT * FROM STUDENT WHERE Name=?",(session["username"],))
            results=curr.fetchall()
            return render_template("index.html",abi=results)
        return render_template("index.html")
@app.route('/logout')
def logout():
    session.pop("username",None)
    return redirect (url_for("login"))

if __name__=="__main__":
    app.run(debug=True,port=5005)