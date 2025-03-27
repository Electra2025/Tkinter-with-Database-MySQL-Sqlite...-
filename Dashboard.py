from tkinter import *
from employees import employee_form
from supplier import supplier_form
from category import category_form
from products import product_form
from employees import connect_database
from tkinter import messagebox
import time

def update():
    # current_time = time.strftime('%A %I:%M:%S %p')
    # current_date = time.strftime('%d/%m/%Y')
    cursor,connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT * from employee_data')
    emp_records = cursor.fetchall()
    total_emp_count_label.config(text=len(emp_records))

    cursor.execute('SELECT * from supplier_data')
    sup_records = cursor.fetchall()
    total_sup_count_label.config(text=len(sup_records))

    cursor.execute('SELECT * from category_data')
    cat_records = cursor.fetchall()
    total_cat_count_label.config(text=len(cat_records))

    cursor.execute('SELECT * from product_data')
    prod_records = cursor.fetchall()
    total_prod_count_label.config(text=len(prod_records))

    date_time = time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Welcome Admin\t\t\t\t\t\t{date_time}')
    subtitleLabel.after(400,update)


def tax_window():
    def save_tax():
        value = tax_count.get()
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table(id INT primary key, tax DECIMAL(5,2))')
        cursor.execute('SELECT id from tax_table WHERE id=1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table SET tax=%s WHERE id=1',value)
        else:    
            cursor.execute('INSERT INTO tax_table(id,tax)VALUES(1,%s)',value)
        connection.commit()
        messagebox.showinfo('Success',f'Tax is set to {value}% and saved successfully.',parent=tax_root)

    tax_root = Toplevel()
    tax_root.title('Tax Window')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage = Label(tax_root,text='Enter Tax Percentage(%)',font=('arial',12))
    tax_percentage.pack(pady=10)
    tax_count = Spinbox(tax_root,from_=0,to=100,font=('arial',12))
    tax_count.pack(pady=10)
    save_button = Button(tax_root,text=' Save',font=('arial',12,'bold'),bg='white',fg='black',width=10,command=save_tax)
    save_button.pack(pady=20)

current_frame = None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame = form_function(window)

window = Tk()
window.title('Dashboard')
window.geometry('1270x675+0+0')
window.resizable(0,0)
window.config(bg='white')

bg_image = PhotoImage(file='Inventory.png')
titlelabel = Label(window,image=bg_image,compound=LEFT,text=' Inventory Management System',font=('times new roman',40,'bold'),bg='navy',fg='white',anchor='w',padx=20)
titlelabel.place(x=0,y=0,relwidth=1)

logoutButton = Button(window,text='Logout',font=('times new roaman',20,'bold'),fg='black')
logoutButton.place(x=1100,y=10)

subtitleLabel = Label(window,text='Welcome Admin\t\t Date: 08-03-2025\t\t Time: 02:26:03 pm',font=('times new roman',15),bg='brown',fg='white')
subtitleLabel.place(x=0,y=70,relwidth=1)

leftFrame = Frame(window)
leftFrame.place(x=0,y=102,width=135,height=570)

logoImage=PhotoImage(file='logo.png')
imageLabel = Label(leftFrame,image=logoImage)
imageLabel.pack()

# menuLabel = Label(leftFrame,text='Menu',font=('times new roaman',20),bg='green')
# menuLabel.pack(fill=X)

employee_icon = PhotoImage(file='employee.png')
employee_button = Button(leftFrame,image=employee_icon,compound=LEFT,text=' Employees',font=('times new roman',16,'bold'),anchor='w',padx=10,
                         command=lambda : show_form(employee_form))
employee_button.pack(fill=X)

supplier_icon = PhotoImage(file='supplier.png')
supplier_button = Button(leftFrame,image=supplier_icon,compound=LEFT,text=' Suppliers',font=('times new roman',16,'bold'),anchor='w',padx=10,
                         command=lambda : show_form(supplier_form))
supplier_button.pack(fill=X)

category_icon = PhotoImage(file='category.png')
category_button = Button(leftFrame,image=category_icon,compound=LEFT,text=' Categories',font=('times new roman',16,'bold'),anchor='w',padx=10,
                         command=lambda : show_form(category_form))
category_button.pack(fill=X)

product_icon = PhotoImage(file='product.png')
product_button = Button(leftFrame,image=product_icon,compound=LEFT,text=' Products',font=('times new roman',16,'bold'),anchor='w',padx=10,
                        command=lambda : show_form(product_form))
product_button.pack(fill=X)

sale_icon = PhotoImage(file='sale.png')
sale_button = Button(leftFrame,image=sale_icon,compound=LEFT,text=' Sales',font=('times new roman',16,'bold'),anchor='w',padx=10)
sale_button.pack(fill=X)

tax_icon = PhotoImage(file='tax.png')
tax_button = Button(leftFrame,image=tax_icon,compound=LEFT,text=' Tax',font=('times new roman',16,'bold'),anchor='w',padx=10,
                    command=tax_window)
tax_button.pack(fill=X)

exit_icon = PhotoImage(file='exit.png')
exit_button = Button(leftFrame,image=exit_icon,compound=LEFT,text=' Exit',font=('times new roman',16,'bold'),anchor='w',padx=10)
exit_button.pack(fill=X)

emp_frame = Frame(window,bg='grey',bd=3,relief=RIDGE)
emp_frame.place(x=400,y=125,height=170,width=200)
total_emp_icon=PhotoImage(file='total_emp.png')
total_emp_icon_label=Label(emp_frame,image=total_emp_icon,bg='grey')
total_emp_icon_label.pack(pady=10)

total_emp_label=Label(emp_frame,text='Total Employees',bg='grey',fg='white',font=('times new roman',15,'bold'))
total_emp_label.pack()

total_emp_count_label=Label(emp_frame,text='0',bg='grey',fg='white',font=('times new roman',30,'bold'))
total_emp_count_label.pack()

sup_frame = Frame(window,bg='purple',bd=3,relief=RIDGE)
sup_frame.place(x=800,y=125,height=170,width=200)
total_sup_icon=PhotoImage(file='total_sup.png')
total_sup_icon_label=Label(sup_frame,image=total_sup_icon,bg='purple')
total_sup_icon_label.pack(pady=10)

total_sup_label=Label(sup_frame,text='Total Suppliers',bg='purple',fg='white',font=('times new roman',15,'bold'))
total_sup_label.pack()

total_sup_count_label=Label(sup_frame,text='0',bg='purple',fg='white',font=('times new roman',30,'bold'))
total_sup_count_label.pack()

cat_frame = Frame(window,bg='green3',bd=3,relief=RIDGE)
cat_frame.place(x=400,y=310,height=170,width=200)
total_cat_icon=PhotoImage(file='total_cat.png')
total_cat_icon_label=Label(cat_frame,image=total_cat_icon,bg='green3')
total_cat_icon_label.pack(pady=10)

total_cat_label=Label(cat_frame,text='Total Categories',bg='green3',fg='white',font=('times new roman',15,'bold'))
total_cat_label.pack()

total_cat_count_label=Label(cat_frame,text='0',bg='green3',fg='white',font=('times new roman',30,'bold'))
total_cat_count_label.pack()

prod_frame = Frame(window,bg='chocolate1',bd=3,relief=RIDGE)
prod_frame.place(x=800,y=310,height=170,width=200)
total_prod_icon=PhotoImage(file='total_prod.png')
total_prod_icon_label=Label(prod_frame,image=total_prod_icon,bg='chocolate1')
total_prod_icon_label.pack(pady=10)

total_prod_label=Label(prod_frame,text='Total Products',bg='chocolate1',fg='white',font=('times new roman',15,'bold'))
total_prod_label.pack()

total_prod_count_label=Label(prod_frame,text='0',bg='chocolate1',fg='white',font=('times new roman',30,'bold'))
total_prod_count_label.pack()

sale_frame = Frame(window,bg='deep sky blue',bd=3,relief=RIDGE)
sale_frame.place(x=600,y=495,height=170,width=200)
total_sale_icon=PhotoImage(file='total_sale.png')
total_sale_icon_label=Label(sale_frame,image=total_sale_icon,bg='deep sky blue')
total_sale_icon_label.pack(pady=10)

total_sale_label=Label(sale_frame,text='Total Sales',bg='deep sky blue',fg='white',font=('times new roman',15,'bold'))
total_sale_label.pack()

total_sale_count_label=Label(sale_frame,text='0',bg='deep sky blue',fg='white',font=('times new roman',30,'bold'))
total_sale_count_label.pack()

update()

window.mainloop()