from tkinter import *
from tkinter.ttk import Combobox,Treeview,Style,Scrollbar 
from PIL import Image,ImageTk
from datetime import datetime
import sqlite3
from tkinter import messagebox


con=sqlite3.connect(database="bank.sqlite")
cur=con.cursor()
table1="create table accounts(account_no integer primary key autoincrement,account_name text,account_pass text,account_email text,account_mob text,account_type text,account_bal float,account_opendate text)"
table2="create table txn(txn_account_no int,txn_amt float,txn_update_bal float,txn_date text,txn_type text)"
try:
    cur.execute(table1)
    cur.execute(table2)
    print("Tables created")
except:
    print("something went wrong in db,might be table(s) already exists")
    
con.commit()
con.close()


win=Tk()
win.state("zoomed")
win.configure(bg="steel blue")

lbl_title=Label(win,text="Banking Automation",bg="steel blue",font=('Arial',55,'bold','underline'))
lbl_title.place(relx=0.5, rely=0, anchor='n')

img=Image.open("logo.png").resize((220,155))
imgtk=ImageTk.PhotoImage(img,master=win)

lbl_logo=Label(win,image=imgtk)
lbl_logo.place(x=0,y=0)



def login_screen():
    frm=Frame(win)
    frm.configure(bg="light blue")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)

    def newuser():
        frm.destroy()
        newuser_screen()
    
    def forgot():
        frm.destroy()
        forgotpass_screen()
    
    def reset():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
        
    def login_db():
        acn=e_acn.get()
        pwd=e_pass.get()
        if(acn=="" or pwd==""):
            messagebox.showwarning("login","Please fill both fields")
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from accounts where account_no=? and account_pass=?",(acn,pwd))
            global tup
            tup=cur.fetchone()
            if(tup==None):
                messagebox.showerror("login","Invalid Account no. or Password")
            else:
                frm.destroy()
                welcome_screen()
    lbl_acn=Label(frm,text="Account No.  :",bg='light blue',font=('Arial',20,'bold'))
    lbl_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.1)
    e_acn.focus()
    
    lbl_pass=Label(frm,text="Password      :",bg='light blue',font=('Arial',20,'bold'))
    lbl_pass.place(relx=.3,rely=.25)
    
    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.45,rely=.25)
    
     # Bind Enter key on Account field to move to Password field
    e_acn.bind("<Return>", lambda event: e_pass.focus_set())
    
    btn_login=Button(frm,text="login",command=login_db,width=6,font=('Arial',15,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_login.place(relx=.495,rely=.35)
    
     # Bind Enter key on Password field to move to Login field
    e_pass.bind("<Return>", lambda event: btn_login.invoke())

    
    btn_reset=Button(frm,text="reset",command=reset,width=6,font=('Arial',15,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_reset.place(relx=.555,rely=.35)
    
    btn_fp=Button(frm,text="forgot password",command=forgot,width=16,font=('Arial',15,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_fp.place(relx=.485,rely=.435)
    
    btn_new=Button(frm,text="open new account",command=newuser,width=18,font=('Arial',15,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_new.place(relx=.477,rely=.525)
    

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg="sky blue")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)

    def back():
        frm.destroy()
        login_screen()
     
    
    def openacn_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        acn_type=cb_type.get()
        if(acn_type=="Saving"):
            bal=1000
        else:
            bal=10000
        opendate=str(datetime.now().date())
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into accounts(account_name,account_pass,account_email,account_mob,account_type,account_bal,account_opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,acn_type,bal,opendate))
        con.commit()
        con.close()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select max(account_no) from accounts")
        tup=cur.fetchone()
        con.close()
        messagebox.showinfo("Success",f"Account Opened with ACN :{tup[0]}")
        frm.destroy()
        login_screen()
        
    btn_back=Button(frm,text="back",command=back,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_back.place(relx=0,rely=0)
    
    lbl_name=Label(frm,text="Full Name :",bg='sky blue',font=('Arial',20,'bold'))
    lbl_name.place(relx=.3,rely=.05)
    
    e_name=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_name.place(relx=.45,rely=.05)
    e_name.focus()
    
    lbl_pass=Label(frm,text="Password :",bg='sky blue',font=('Arial',20,'bold'))
    lbl_pass.place(relx=.3,rely=.2)
    
    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_pass.place(relx=.45,rely=.2)

    
    lbl_email=Label(frm,text="Email Id :",bg='sky blue',font=('Arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.35)
    
    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.45,rely=.35)
    
    
    lbl_mob=Label(frm,text="Mobile No.:",bg='sky blue',font=('Arial',20,'bold'))
    lbl_mob.place(relx=.3,rely=.5)
    
    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.45,rely=.5)
    
    lbl_type=Label(frm,text="Account Type :",bg='sky blue',font=('Arial',20,'bold'))
    lbl_type.place(relx=.3,rely=.65)
    
    cb_type=Combobox(frm,values=['Saving','Current'],font=('Arial',20,'bold'))
    cb_type.current(0)
    cb_type.place(relx=.45,rely=.65)
    
    btn_open=Button(frm,text="open",command=openacn_db,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_open.place(relx=.48,rely=.8)
    
    btn_reset=Button(frm,text="reset",font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_reset.place(relx=.57,rely=.8)
    
    
def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg="deep sky blue")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)

    def back():
        frm.destroy()
        login_screen()
     
    def get_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()
        
        if(acn=="" or email=="" or mob==""):
            messagebox.showwarning("Validation","Please fill all fields")
            return
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select account_pass from accounts where account_no=? and account_email=? and account_mob=?",(acn,email,mob))
            tup=cur.fetchone()
            if(tup==None):
                messagebox.showerror("Forgot","Invalid details")
            else:
                messagebox.showinfo("Forgot",f"Your Password is:{tup[0]}")
            
    btn_back=Button(frm,text="back",command=back,font=('Arial',20,'bold'),bd=5,bg="deepskyblue3",cursor="hand2")
    btn_back.place(relx=0,rely=0)
    
    lbl_acn=Label(frm,text="Account No.:",bg='deep sky blue',font=('Arial',20,'bold'))
    lbl_acn.place(relx=.3,rely=.2)
    
    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.2)
    e_acn.focus()
    
    lbl_email=Label(frm,text="Email Id :",bg='deep sky blue',font=('Arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.35)
    
    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.45,rely=.35)
    
    
    lbl_mob=Label(frm,text="Mobile No.:",bg='deep sky blue',font=('Arial',20,'bold'))
    lbl_mob.place(relx=.3,rely=.5)
    
    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.45,rely=.5)
    
    
    btn_get=Button(frm,text="get",command=get_db,font=('Arial',20,'bold'),bd=5,bg="deepskyblue3",cursor="hand2")
    btn_get.place(relx=.48,rely=.65)
    
    btn_reset=Button(frm,text="reset",font=('Arial',20,'bold'),bd=5,bg="deepskyblue3",cursor="hand2")
    btn_reset.place(relx=.56,rely=.65)
    
    
def welcome_screen():
    frm=Frame(win)
    frm.configure(bg="cyan2")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)
    
    def logout():
        frm.destroy()
        login_screen()
       
    def checkbal():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=10,highlightcolor='brown')
        ifrm.configure(bg='cadetblue1')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        
        lbl_page.configure(text="This is Check balance page")
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select account_name,account_bal,account_opendate from accounts where account_no=?",(tup[0],))
        row=cur.fetchone()
        
        lbl_acn=Label(ifrm,text=f"Account Number:\t\t{tup[0]}",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_acn.place(relx=.3,rely=.1)
    
        lbl_name=Label(ifrm,text=f"Holder Name:\t\t{row[0]}",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_name.place(relx=.3,rely=.3)
    
        lbl_bal=Label(ifrm,text=f"Available Bal:\t\t{row[1]}",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_bal.place(relx=.3,rely=.5)
    
        lbl_date=Label(ifrm,text=f"Account open date:\t{row[2]}",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_date.place(relx=.3,rely=.7)
    
    def deposit():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=10,highlightcolor='brown')
        ifrm.configure(bg='cadetblue1')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        
        lbl_page.configure(text="This is Deposit page")
        
        def deposit_db():
            amt=float(e_amt.get())
            acn=tup[0]
            txn_type="CR."
            dt=str(datetime.now())
            
            if(amt<0):
                messagebox.showerror("Deposit","-ve amount can not be deposited")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(acn,))
                bal=cur.fetchone()[0]
                con.close()
                
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("insert into txn values(?,?,?,?,?)",(acn,amt,bal+amt,dt,txn_type))
                cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,acn))         
                con.commit()
                con.close()
                
                messagebox.showinfo("Deposit","Amount deposited")
                
            
        lbl_amt=Label(ifrm,text="Enter Amount :",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_amt.place(relx=.2,rely=.2)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.2)
    
        btn_dep=Button(ifrm,text="deposit",command=deposit_db,font=('Arial',15,'bold'),bd=5,bg="powder blue",cursor="hand2")
        btn_dep.place(relx=.56,rely=.4)
    
    
    def withdraw():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=10,highlightcolor='brown')
        ifrm.configure(bg='cadetblue1')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        
        lbl_page.configure(text="This is Withdraw page")
        
        
        def withdraw_db():
            amt=float(e_amt.get())
            acn=tup[0]
            txn_type="DB."
            dt=str(datetime.now())
            
            if(amt<0):
                messagebox.showerror("Withdraw","-ve amount can not be withdrawn")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(acn,))
                bal=cur.fetchone()[0]
                con.close()
                
                if(bal>=amt):
                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("insert into txn values(?,?,?,?,?)",(acn,amt,bal-amt,dt,txn_type))
                    cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(amt,acn))         
                    con.commit()
                    con.close()

                    messagebox.showinfo("Withdraw","Amount withdrawn")

                else:
                    messagebox.showwarning("Withdraw","Insufficient bal")
        
        lbl_amt=Label(ifrm,text="Enter Amount :",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_amt.place(relx=.2,rely=.2)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.2)
    
        btn_dep=Button(ifrm,text="withdraw",command=withdraw_db,font=('Arial',15,'bold'),bd=5,bg="powder blue",cursor="hand2")
        btn_dep.place(relx=.56,rely=.4)
    
    
    def transfer():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=10,highlightcolor='brown')
        ifrm.configure(bg='cadetblue1')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        
        lbl_page.configure(text="This is Transfer page")
        
        def transfer_db():
            t_acn=e_to.get()
            amt=float(e_amt.get())
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from accounts where account_no=?",(t_acn,))
            row=cur.fetchone()
            con.close()
            
            if(row==None):
                messagebox.showerror("Transfer","To account does not exist")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(tup[0],))
                bal=cur.fetchone()[0]
                con.close()
                
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(t_acn,))
                t_bal=cur.fetchone()[0]
                con.close()
                if(bal>=amt):
                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    dt=str(datetime.now())
                    cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(amt,tup[0]))
                    cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,t_acn))
                    cur.execute("insert into txn values(?,?,?,?,?)",(tup[0],amt,bal-amt,dt,"DB."))
                    cur.execute("insert into txn values(?,?,?,?,?)",(t_acn,amt,t_bal+amt,dt,"CR."))
                    
                    con.commit()
                    con.close()
                    messagebox.showinfo("Transfer","Txn Done")
                else:
                    messagebox.showwarning("Transfer","Insufficient bal")
        
        lbl_to=Label(ifrm,text="Enter To Account :",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_to.place(relx=.2,rely=.2)
        
        e_to=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_to.place(relx=.45,rely=.2)
    
        lbl_amt=Label(ifrm,text="Enter Amount    :",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_amt.place(relx=.2,rely=.4)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.4)
    
    
        btn_dep=Button(ifrm,text="transfer",command=transfer_db,font=('Arial',15,'bold'),bd=5,bg="powder blue",cursor="hand2")
        btn_dep.place(relx=.55,rely=.6)
    
    def update():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=10,highlightcolor='brown')
        ifrm.configure(bg='cadetblue1')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        
        lbl_page.configure(text="This is Update Profile page")
        
        def update_profile():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update accounts set account_name=?,account_pass=?,account_email=?,account_mob=? where account_no=?",(name,pwd,email,mob,tup[0]))
            con.commit()
            con.close()
            messagebox.showinfo("Update","Profile Updated")
        
        
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select * from accounts where account_no=?",(tup[0],))
        row=cur.fetchone()
        con.close()
        
        lbl_name=Label(ifrm,text="Name :",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_name.place(relx=.07,rely=.2)
        
        e_name=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_name.place(relx=.17,rely=.2)
        e_name.insert(0,row[1])

        lbl_pass=Label(ifrm,text="Password  :",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_pass.place(relx=.48,rely=.2)
        
        e_pass=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_pass.place(relx=.64,rely=.2)
        e_pass.insert(0,row[2])
        
        lbl_email=Label(ifrm,text="Email :",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_email.place(relx=.07,rely=.4)
        
        e_email=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_email.place(relx=.17,rely=.4)
        e_email.insert(0,row[3])
        
        lbl_mob=Label(ifrm,text="Mobile No. :",bg='cadetblue1',font=('Arial',15,'bold'),fg='red')
        lbl_mob.place(relx=.48,rely=.4)
        
        e_mob=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_mob.place(relx=.64,rely=.4)
        e_mob.insert(0,row[4])

    
        btn_dep=Button(ifrm,text="update",command=update_profile,font=('Arial',15,'bold'),bd=5,bg="powder blue",cursor="hand2")
        btn_dep.place(relx=.47,rely=.6)
    
    
    def txn_history():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=10,highlightcolor='brown')
        ifrm.configure(bg='cadetblue1')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        
        lbl_page.configure(text="This is Transactions history page")
        
        tv=Treeview(ifrm)
        tv.place(x=0,y=0,relheight=1,relwidth=1)
        
        style = Style()
        style.configure("Treeview.Heading", font=('Arial',10,'bold'),foreground='brown')
        
        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(relx=.98,y=0,relheight=1)
        
        tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')
        
        tv.column('Txn date',width=150,anchor='c')
        tv.column('Txn amount',width=100,anchor='c')
        tv.column('Txn type',width=100,anchor='c')
        tv.column('Updated bal',width=100,anchor='c')

        tv.heading('Txn date',text='Txn date')
        tv.heading('Txn amount',text='Txn amount')
        tv.heading('Txn type',text='Txn type')
        tv.heading('Updated bal',text='Updated bal')
        
        tv['show']='headings'
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txn where txn_account_no=?",(tup[0],))
        for row in cur:
            tv.insert("","end",values=(row[0],row[1],row[2],row[3]))

        
    btn_logout=Button(frm,text="Logout",command=logout,width=6,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_logout.place(relx=.925,rely=0)
    
    btn_homepage=Button(frm,text="Home",command=welcome_screen,width=6,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_homepage.place(relx=0,rely=.0)
    
    lbl_wel=Label(frm,text=f"Welcome,{tup[1]}",bg='cyan2',font=('Arial',30,'bold'),fg='royal blue')
    lbl_wel.place(relx=0.5, rely=0, anchor='n')
    
    lbl_page=Label(frm,text="This is Home Page",bg='cyan2',font=('Arial',20,'bold','underline'),fg='steelblue4')
    lbl_page.place(relx=0.5, rely=.1, anchor='n')
    
    ifrm=Label(frm,text="""Hello Dear,\n\nWelcome to our Banking System! We are delighted to provide you with a simple, secure platform to manage your finances effortlessly.\n
Here, convenience and control are in your hands. You can instantly check your account balance in real-time, deposit funds easily, and review your complete transaction history for total transparency. Our secure platform also allows you to transfer money to other accounts quickly and smoothly.\n
We are committed to making your banking experience reliable and straightforward. Explore our features and manage your money with confidence. Thank you for choosing us as your trusted financial partner.""",bg='cyan2',font=('Arial',15,'bold'),wraplength=930,anchor='nw',justify='left',fg='steelblue4')
    ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
    
    btn_checkbal=Button(frm,text="Check balance",command=checkbal,width=12,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_checkbal.place(relx=0,rely=.17)
    
    btn_deposit=Button(frm,text="Deposit amt",command=deposit,width=12,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_deposit.place(relx=0,rely=.29)
    
    btn_withdraw=Button(frm,text="Withdraw amt",command=withdraw,width=12,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_withdraw.place(relx=0,rely=.41)
    
    btn_transfer=Button(frm,text="Transfer",command=transfer,width=12,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_transfer.place(relx=0,rely=.53)
    
    btn_update=Button(frm,text="Update profile",command=update,width=12,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_update.place(relx=0,rely=.65)
    
    btn_txnhist=Button(frm,text="Txn history",command=txn_history,width=12,font=('Arial',20,'bold'),bd=5,bg="powder blue",cursor="hand2")
    btn_txnhist.place(relx=0,rely=.77)
    
     
login_screen()
win.mainloop()


