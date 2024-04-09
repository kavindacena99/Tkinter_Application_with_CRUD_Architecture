import tkinter as tk
from tkinter import ttk
import mysql.connector

font_style = ("Arial",14)

Myuser = "d"

def onUsersPageClose(usersroot):
    usersroot.destroy()
    loginBtn.configure(state="normal")

def selectedItem(event):
    global Myuser

    Myuser = table.item(table.selection())['values'][2]
    #print(table.item(table.selection())['values'][0])

def deleteUser():
    try:
        connection = mysql.connector.connect(host='localhost',database='ums',user='root',password='')
        cursor = connection.cursor()

        cursor.execute("DELETE FROM users WHERE username = %s",(Myuser,))
        connection.commit()

        table.selection_remove(table.selection())

        table.delete(*table.get_children())
        cursor.execute("SELECT firstname, lastname, username FROM users;")
        data = cursor.fetchall()
        for row in data:
            table.insert('', 'end', values=row)

    except mysql.connector.Error as err:
        print(err)

def pswdChanged(p):
    try:
        connection = mysql.connector.connect(host='localhost',database='ums',user='root',password='')
        cursor = connection.cursor()

        cursor.execute("UPDATE users SET pswd = %s WHERE username = %s",(p.get(),Myuser))
        connection.commit()

        updatePswdroot.destroy()

    except mysql.connector.Error as err:
        print(err)

def updatePassword():
    global updatePswdroot
    updatePswdroot = tk.Tk()

    updatePswdroot.geometry('400x200')
    updatePswdroot.title("Update your Password")
    updatePswdroot.resizable(False,False)

    updatePswd = ttk.Label(updatePswdroot,text="Enter Your New Password",font=font_style,foreground="Blue")
    updatePswd.pack()

    updateEntry = ttk.Entry(updatePswdroot,font=font_style)
    updateEntry.pack(pady=(10,2))

    updateBtn = ttk.Button(updatePswdroot,text="Update",command=lambda:pswdChanged(updateEntry))
    updateBtn.pack(pady=(5,5))

    updatePswdroot.mainloop()
    
def userAdded(f,l,u,p):
    try:
        connection = mysql.connector.connect(host='localhost',database='ums',user='root',password='')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users(firstname,lastname,username,pswd) VALUES(%s,%s,%s,%s)",(f.get(),l.get(),u.get(),p.get()))
        connection.commit()

        table.delete(*table.get_children())

        cursor.execute("SELECT firstname, lastname, username FROM users;")
        data = cursor.fetchall()
        for row in data:
            table.insert('', 'end', values=row)

        newUserroot.destroy()

    except mysql.connector.Error as err:
        print(err)

def newUser():
    global newUserroot
    newUserroot = tk.Tk()

    newUserroot.geometry('500x500')
    newUserroot.resizable(False,False)
    newUserroot.title("Add New User")

    label1 = ttk.Label(newUserroot,text="Enter First Name",font=font_style,foreground="Blue")
    label1.pack(pady=(40,5))

    fname = ttk.Entry(newUserroot,font=font_style)
    fname.pack()

    label2 = ttk.Label(newUserroot,text="Enter Second Name",font=font_style,foreground="Blue")
    label2.pack(pady=(40,5))

    lname = ttk.Entry(newUserroot,font=font_style)
    lname.pack()

    label3 = ttk.Label(newUserroot,text="Enter Username",font=font_style,foreground="Blue")
    label3.pack(pady=(40,5))

    username = ttk.Entry(newUserroot,font=font_style)
    username.pack()

    label4 = ttk.Label(newUserroot,text="Enter a Password",font=font_style,foreground="Blue")
    label4.pack(pady=(40,5))

    pswd = ttk.Entry(newUserroot,font=font_style)
    pswd.pack()

    addUserBtn = ttk.Button(newUserroot,text="Add User",command=lambda:userAdded(fname,lname,username,pswd))
    addUserBtn.pack(pady=5)

    newUserroot.mainloop()

def intoUsers():
    usersroot = tk.Tk()

    usersroot.geometry('800x400')
    usersroot.title('Users')
    usersroot.resizable(False,False)
    #I programmed this, when I closed the users page login button of login window is enabled
    usersroot.protocol("WM_DELETE_WINDOW",lambda: onUsersPageClose(usersroot))

    try:
        connection = mysql.connector.connect(host='localhost',database='ums',user='root',password='')
        cursor = connection.cursor()
    except mysql.connector.Error as err:
        print(err)

    global table
    table = ttk.Treeview(usersroot,columns=('First Name','Last Name','Username'),show='headings')
    table.heading('First Name',text='First Name')
    table.heading('Last Name',text='Last Name')
    table.heading('Username',text='Username')
    #table.column('Name',width=200)
    table.pack()

    try:
        cursor.execute("SELECT firstname,lastname,username FROM users;")
        data = cursor.fetchall()
        for row in data:
            table.insert('','end',values=row)

        table.bind('<<TreeviewSelect>>', lambda event:selectedItem(event))
    except:
        print("error")

    deleteBtn = ttk.Button(usersroot,text="Delete User",command=deleteUser)
    deleteBtn.pack()

    newBtn = ttk.Button(usersroot,text="Add New User",command=newUser)
    newBtn.pack()

    UpdateBtn = ttk.Button(usersroot,text="Update User Password",command=updatePassword)
    UpdateBtn.pack()

    usersroot.mainloop()

def authenticate(u,p):
    try:
        connection = mysql.connector.connect(host='localhost',database='ums',user='root',password='')
        cursor = connection.cursor()

        myUsername = u.get()
        myPassword = p.get()

        cursor.execute("SELECT * FROM users WHERE username = %s AND pswd = %s",(myUsername,myPassword))
        result = cursor.fetchone()

        if result:
            loginBtn.configure(state="disabled")
            intoUsers()
        else:
            warn.pack()

    except mysql.connector.Error as err:
        print(err)

def login():
    loginroot = tk.Tk()

    loginroot.geometry('400x400')
    loginroot.title("User Management System Login")
    loginroot.resizable(False,False)

    global warn
    warn = ttk.Label(loginroot,text="Enter Correct Details",foreground="Red",font=("Arial",10))
    warn.pack_forget()
    #warn.pack(pady=10)

    label1 = ttk.Label(loginroot,text="Enter Your Username",font=font_style,foreground="Blue")
    label1.pack(pady=(40,5))

    username1 = ttk.Entry(loginroot,width=30,font=font_style)
    username1.pack()

    label2 = ttk.Label(loginroot,text="Enter Your Password",font=font_style,foreground="Blue")
    label2.pack(pady=(50,5))

    pswd1 = ttk.Entry(loginroot,width=30,font=font_style)
    pswd1.pack()

    global loginBtn
    loginBtn = ttk.Button(loginroot,text="Login",command=lambda:authenticate(username1,pswd1))
    loginBtn.pack(pady=5)

    loginroot.mainloop()

login()