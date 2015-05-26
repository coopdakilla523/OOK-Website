#!/usr/bin/env python


import time
import sqlite3
import cgi
import cgitb;
import hashlib
import json


cgitb.enable()

print("Monkey 1.0 is ready to fling!")


def init():
    try:
        conn = sqlite3.connect("mydb.dat")
        c = conn.cursor()
        c.execute("create table ooks(uid integer,timeOf integer,ook text);")
        c.execute("create table users(uid integer primary key autoincrement, username text ,password text,email text,salt integer);")
        conn.commit();
        conn.close();
    except:
        pass

def writeOOKS(self):
    conn = sqlite3.connect("mydb.dat")
    c = conn.cursor()
    c.execute("select ook,timeOf from ooks Order By timeOf DESC LIMIT 5")
    L=c.fetchall()
    temp = []
    print(len(L))
    if len(L) > 0:
        for ook,daTime in L:
            #self.remote.write("<div class=posts>" + "<legend>" + daTime + "</legend>" + ook + " </div>")
            temp.append({"header":daTime,"ook":ook})
    else:
            temp.append({"header":"None","ook":"No ooks at this time!"})
    print("temp: " ,temp)
    json.dump(temp,self.remote)
    conn.close()


def addOOK(self):
    cook = self.headers['Cookie']
    if cook != None:
        name = (cook.split('=')[1]).split(';')[0]
        if name == "None":
            return False
        ooke = self.fs.getfirst('ooks',None)
        header = time.strftime("%a %B %d %I:%M:%S %Y(" + name + ")")
        conn = sqlite3.connect("mydb.dat")
        c = conn.cursor()
        c.execute("insert into ooks(ook,timeOf) values (?,?);",(ooke,header))
        conn.commit()
        conn.close()
        return True
    else:
        return False


def signup(self):
    h = hashlib.sha1()
    uname = self.fs.getfirst('username',None)
    password = self.fs.getfirst('password1',None)
    if password == None or uname == None:
        conn.close()
        return True
    salt = time.time()
    h.update(str(salt).encode())
    h.update(password.encode())
    hashPass = h.hexdigest()
    email = self.fs.getfirst('email',None)
    conn = sqlite3.connect("mydb.dat")
    c = conn.cursor()
    c.execute("select username,email from users where username=? or email=?",(uname,email))
    L=c.fetchall()
    if(len(L)>0):
        conn.close()
        return True
    c.execute("insert into users(username,password,email,salt) values (?,?,?,?)",(uname,hashPass,email,salt))
    conn.commit()
    conn.close()
    return False

def login(self):
    h = hashlib.sha1()
    uname = self.fs.getfirst('username',None)
    password = self.fs.getfirst('password',None)
    conn = sqlite3.connect("mydb.dat")
    c = conn.cursor()
    c.execute("select salt from users where username=?",(uname,));
    L = c.fetchall()
    if(len(L) < 1) or password == None or uname == None:
        #self.remote.write("You should sign up!")
        conn.close()
        return True
    salt = L[0][0]
    h.update(str(salt).encode())
    h.update(password.encode())
    hashPass = h.hexdigest()
    c.execute("select username,password from users where username=? and password=?",(uname,hashPass))
    L2 = c.fetchall()
    if(len(L2) < 1):
        conn.close()
        print("passwords don't match")
        return True
    self.send_header("Set-Cookie"," user=" + uname + ";")
    self.send_header("Set-Cookie","hasLogged=" + "True;")
    self.username = uname
    self.hasLogged = True
    return False

def logout(self):
    self.send_header('Set-Cookie',"user=None;")
    self.send_header("Set-Cookie","hasLogged=" + "False;")
    self.hasLogged = False
    self.username = "None"