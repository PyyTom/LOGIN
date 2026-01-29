import sqlite3,hashlib  # import sqlite3 for DB and hashlib for hashing passwords
db=sqlite3.connect('db.db')  # open (or create) SQLite database file
db.execute('create table if not exists USERS(USER,PWD)')  # create table if not exists
db.close()  # close DB connection
from flet import app,Page,AlertDialog,Row,Switch,IconButton,Divider,Column,Dropdown,DropdownOption,TextField,ElevatedButton,Text  # import Flet UI components
def main(page:Page):  # main entry point for the Flet app, receives a Page object
    def theme(e):  # color theme handler
        page.theme_mode='dark' if page.theme_mode=='light' else 'light'  # switch between light and dark modes
        page.update()  # refresh the UI
    def submit(e,user,pwd,re_pwd):  # handler for LOGIN/REGISTER/UNREGISTER actions
        def hash_pwd(pwd):  # simple hashing helper
            return hashlib.sha256(pwd.encode()).hexdigest()  # returns SHA-256 hex digest
        db=sqlite3.connect('db.db')
        match e.control.text:  # branch based on the button text (requires Python 3.10+)
            case 'LOGIN':  # login flow
                if not user.strip() or not pwd.strip():alert.title=Text('EMPTY FIELDS')  # check empty fields
                elif db.execute('select 1 from USERS where USER=? and PWD=?',(user,hash_pwd(pwd))).fetchone() is not None:
                    alert.title=Text(f'USER {user} LOGGED IN SUCCESSFULLY')  # success message
                    d_user.value=t_pwd.value=''  # clear selected user and password fields
                    #page.go('/HOME')  # placeholder for navigation to home
                else:alert.title=Text(f'USER {user} NOT FOUND')  # user not found message
            case 'REGISTER':  # registration flow
                if not user.strip() or not pwd.strip() or not re_pwd.strip():alert.title=Text('EMPTY FIELDS')  # check empty fields
                elif pwd!=re_pwd:alert.title=Text('PASSWORDS DO NOT MATCH')  # password confirmation mismatch
                elif db.execute('select 1 from USERS where USER=?',(user,)).fetchone() is not None:alert.title=Text(f'USER {user} ALREADY EXISTS')  # user exists
                else:
                    db.execute('insert into USERS(USER,PWD) values(?,?)',(user,hash_pwd(pwd)))  # insert new user with hashed password
                    db.commit()  # commit transaction
                    alert.title=Text(f'USER {user} REGISTERED SUCCESSFULLY')  # success message
                    t_user.value=t_pwd.value=t_re_pwd.value=''  # clear input fields
            case 'UNREGISTER':  # unregister flow
                if not user.strip():alert.title=Text('EMPTY FIELDS')  # require username
                else:
                    db.execute('delete from USERS where USER=?',(user,))  # delete user
                    db.commit()
                    alert.title=Text(f'USER {user} UNREGISTERED SUCCESSFULLY')  # success message
                    d_user.value=''  # clear dropdown selection
        db.close()
        page.update()  # refresh UI to show alert changes
        page.open(alert)  # open the alert dialog
    def show_content(e):  # update the central content area depending on selected action
        for i in r_buttons.controls:i.color='lightgrey'  # attempt to reset button colors
        e.control.color='green'  # highlight the clicked button
        db=sqlite3.connect('db.db')  # open DB to populate dropdown
        if db.execute('select 1 from USERS').fetchone() is not None:d_user.options=[DropdownOption(i[0]) for i in db.execute('select USER from USERS').fetchall()]  # populate users list
        else:d_user.options=[]  # empty list if no users
        db.close()
        match e.control.text:  # set content based on selected action
            case 'LOGIN':c_content.controls=[d_user,t_pwd,ElevatedButton('LOGIN',on_click=lambda e:submit(e,d_user.value,t_pwd.value,None))]  # login UI
            case 'REGISTER':c_content.controls=[t_user,t_pwd,t_re_pwd,ElevatedButton('REGISTER',on_click=lambda e:submit(e,(t_user.value).upper(),t_pwd.value,t_re_pwd.value))]  # register UI (username uppercased here)
            case 'UNREGISTER':c_content.controls=[d_user,ElevatedButton('UNREGISTER',on_click=lambda e:submit(e,d_user.value,None,None))]  # unregister UI
        page.update()  # refresh UI to show new content
    alert=AlertDialog(title=Text(''))  # create an AlertDialog with an empty title
    d_user=Dropdown(label='USER',options=[],width=300)  # dropdown for selecting existing users
    t_user=TextField(label='USER',width=300)  # new username input field
    t_pwd=TextField(label='PASSWORD',password=True,can_reveal_password=False,width=300)  # password input field
    t_re_pwd=TextField(label='REPEAT PASSWORD',password=True,can_reveal_password=False,width=300)  # repeat password field
    r_buttons=Row([ElevatedButton('LOGIN',on_click=show_content),
                   ElevatedButton('REGISTER',on_click=show_content),
                   ElevatedButton('UNREGISTER',on_click=show_content)],alignment='center')  # row of action buttons
    c_content=Column([],height=300,horizontal_alignment='center')  # central content area to swap forms
    page.add(Row([Switch(on_change=theme),IconButton(icon='exit_to_app',icon_color='red',icon_size=50,on_click=lambda e:page.window.destroy())],alignment='center'),
             Divider(),
             r_buttons,
             Row([c_content],alignment='center'))  # assemble and add UI elements to the page
app(main)  # run the Flet app