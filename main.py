from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from tkcalendar import Calendar, DateEntry
from datetime import date
import sys
import os

# Function to get correct path for resources when running as exe
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Import login system
from login import run_login

# Import functions from view.py
from view import *

# Import auth to get user database
from auth import get_user_database

###--COLORS--###

co1 = '#453934'  
co2 = "#55433B" 
co3 = "#301515"
co4 = "#FFFFFF"
co5 = '#644ced'
co6 = '#ed2f2f'
co7 = '#ed722f'
co8 = '#2fed68'
co9 = '#edd12f'
co10 = '#2feda8'

colors = [co5, co6, co7, co8, co9, co10]

##--RUN LOGIN--##

logged_user = run_login()

# If user didn't log in (closed the window), terminate the program
if not logged_user:
    sys.exit()

# Define user-specific database
user_database = get_user_database(logged_user)
set_user_database(user_database)

##--WINDOW--##

window = Tk()
window.title('Expense Calculator')
window.geometry('900x900')
window.configure(background=co3)
window.resizable(width=FALSE, height=FALSE)

style = ttk.Style(window)
style.theme_use('clam')

topPart = Frame(window, width=900, height=50, bg=co1, relief='flat')
topPart.grid(row=0, column=0)

middlePart = Frame(window, width=900, height=361, bg=co2, pady=20, relief='flat')
middlePart.grid(row=1, column=0, pady=0, padx=10, sticky=NSEW)

bottomPart = Frame(window, width=900, height=300, bg=co1, relief='flat')
bottomPart.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

frame_gra_pie = Frame(middlePart, width=580, height=250, bg=co2)
frame_gra_pie.place(x=415, y=5)

##--Top part--##

app_img = Image.open(resource_path('dinheiro.png'))
app_img = app_img.resize((45, 45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(topPart, image=app_img, text=' Expense Calculator', width=700, 
                compound=LEFT, padx=5, relief=FLAT, anchor=NW, font=('Verdana 20 bold'), 
                bg=co1, fg=co4)
app_logo.place(x=0, y=0)

# Show logged user
Label(topPart, text=f'User: {logged_user}', anchor=NE, font=('Verdana 10'), 
      bg=co1, fg=co4).place(x=750, y=15)

###--UPDATE FUNCTIONS--###

def apply_date_filter(revenues, expenses):
    """Filters revenues and expenses based on selected period"""
    from datetime import datetime, timedelta
    
    period = period_var.get()
    
    if period == 'All':
        return revenues, expenses
    
    today = datetime.now().date()
    
    if period == 'Today':
        start_date_filter = today
        end_date_filter = today
    elif period == 'This Week':
        start_date_filter = today - timedelta(days=today.weekday())
        end_date_filter = today
    elif period == 'This Month':
        start_date_filter = today.replace(day=1)
        end_date_filter = today
    elif period == 'This Year':
        start_date_filter = today.replace(month=1, day=1)
        end_date_filter = today
    elif period == 'Custom':
        try:
            start_date_filter = datetime.strptime(start_date.get(), '%d/%m/%Y').date()
            end_date_filter = datetime.strptime(end_date.get(), '%d/%m/%Y').date()
        except:
            return revenues, expenses
    else:
        return revenues, expenses
    
    # Filter revenues
    filtered_revenues = []
    for revenue in revenues:
        try:
            revenue_date = datetime.strptime(revenue[2], '%d/%m/%Y').date()
            if start_date_filter <= revenue_date <= end_date_filter:
                filtered_revenues.append(revenue)
        except:
            # If unable to convert date, include the item
            filtered_revenues.append(revenue)
    
    # Filter expenses
    filtered_expenses = []
    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense[2], '%d/%m/%Y').date()
            if start_date_filter <= expense_date <= end_date_filter:
                filtered_expenses.append(expense)
        except:
            # If unable to convert date, include the item
            filtered_expenses.append(expense)
    
    return filtered_revenues, filtered_expenses

def update_filter(event=None):
    """Updates visualization when filter changes"""
    period = period_var.get()
    
    # Show/hide custom date fields
    if period == 'Custom':
        start_date.place(x=265, y=8)
        label_to.place(x=355, y=10)
        end_date.place(x=380, y=8)
    else:
        start_date.place_forget()
        label_to.place_forget()
        end_date.place_forget()
    
    # Update visualization
    update_all()

def update_all():
    """Updates all visual components"""
    percentage()
    pie_chart()
    bar_chart()
    total_summary()
    show_income()

##--Revenue Percentage--##

def percentage():
    # Clear previous widgets
    for widget in middlePart.winfo_children():
        if isinstance(widget, Label):
            if widget.cget('text') == 'Percentage Of Revenue Spent':
                widget.destroy()
        if isinstance(widget, Progressbar):
            widget.destroy()
    
    l_name = Label(middlePart, text='Percentage Of Revenue Spent', height=1, anchor=NW, 
                   font=('Verdana 12'), bg=co1, fg=co4)
    l_name.place(x=7, y=5)

    # Get data and apply filter
    revenues = view_revenues()
    expenses = view_expenses()
    filtered_revenues, filtered_expenses = apply_date_filter(revenues, expenses)
    
    # Calculate filtered totals
    total_revenues = sum([i[3] for i in filtered_revenues])
    total_expenses = sum([i[3] for i in filtered_expenses])
    
    # Calculate percentage
    if total_revenues > 0:
        percent = (total_expenses / total_revenues) * 100
    else:
        percent = 0

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('black.Horizontal.TProgressbar', background='#35e31e')
    style.configure('TProgressbar', thickness=25)
    
    bar = Progressbar(middlePart, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = percent

    l_percentage = Label(middlePart, text='{:.2f}%'.format(percent), height=1, anchor=NW, 
                         font=('Verdana 12'), bg=co2, fg=co4)
    l_percentage.place(x=200, y=35)

##--Bar chart--##

def bar_chart():
    # Clear previous canvas
    for widget in middlePart.winfo_children():
        try:
            if 'FigureCanvas' in str(type(widget)):
                widget.destroy()
        except:
            pass
    
    # Get data and apply filter
    revenues = view_revenues()
    expenses = view_expenses()
    filtered_revenues, filtered_expenses = apply_date_filter(revenues, expenses)
    
    # Calculate filtered totals
    total_revenues = sum([i[3] for i in filtered_revenues])
    total_expenses = sum([i[3] for i in filtered_expenses])
    balance = total_revenues - total_expenses
    
    category_list = ['Income', 'Expenses', 'Balance']
    values_list = [total_revenues, total_expenses, balance]

    figure = plt.Figure(figsize=(4, 3.45), dpi=60)
    figure.patch.set_facecolor(co1)
    ax = figure.add_subplot(111)
    ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(category_list, values_list, color=colors, width=0.9)

    c = 0
    for i in ax.patches:
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("$ {:,.2f}".format(values_list[c])), fontsize=14, fontstyle='italic', 
                verticalalignment='bottom', color='white')
        c += 1

    ax.set_xticklabels(category_list, fontsize=16, color='white')
    ax.tick_params(axis='y', labelcolor='white')

    ax.patch.set_facecolor(co1)
    ax.spines['bottom'].set_color(co1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color(co1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)

    canvas = FigureCanvasTkAgg(figure, middlePart)
    canvas.get_tk_widget().place(x=10, y=70)

##--Total summary--##

def total_summary():
    # Clear previous widgets
    for widget in middlePart.winfo_children():
        if isinstance(widget, Label) or isinstance(widget, Frame):
            try:
                text = widget.cget('text')
                if any(x in text for x in ['MONTHLY INCOME', 'MONTHLY EXPENSES', 'ACCOUNT BALANCE']) or text.startswith('$'):
                    widget.destroy()
            except:
                # If it's a Frame, it has no 'text', so destroy if in correct position
                if widget.winfo_y() in [52, 110, 170]:
                    widget.destroy()
    
    # Get data and apply filter
    revenues = view_revenues()
    expenses = view_expenses()
    filtered_revenues, filtered_expenses = apply_date_filter(revenues, expenses)
    
    # Calculate filtered totals
    total_revenues = sum([i[3] for i in filtered_revenues])
    total_expenses = sum([i[3] for i in filtered_expenses])
    balance = total_revenues - total_expenses
    
    # Monthly Income
    Frame(middlePart, width=100, height=2, bg=co1).place(x=309, y=52)
    Label(middlePart, text='Monthly Income'.upper(), anchor=NW, font=('Verdana 12'), 
          bg=co2, fg=co4).place(x=309, y=32)
    Label(middlePart, text='$ {:.2f}'.format(total_revenues), anchor=NW, font=('Arial 12'), 
          bg=co2, fg=co4).place(x=309, y=60)

    # Monthly Expenses
    Frame(middlePart, width=100, height=2, bg=co1).place(x=309, y=110)
    Label(middlePart, text='Monthly Expenses'.upper(), anchor=NW, font=('Verdana 12'), 
          bg=co2, fg=co4).place(x=309, y=90)
    Label(middlePart, text='$ {:.2f}'.format(total_expenses), anchor=NW, font=('Arial 12'), 
          bg=co2, fg=co4).place(x=309, y=120)

    # Balance
    Frame(middlePart, width=100, height=2, bg=co1).place(x=309, y=170)
    Label(middlePart, text='Account Balance'.upper(), anchor=NW, font=('Verdana 12'), 
          bg=co2, fg=co4).place(x=309, y=150)
    
    balance_color = co8 if balance >= 0 else co6
    Label(middlePart, text='$ {:.2f}'.format(balance), anchor=NW, font=('Arial 12'), 
          bg=co2, fg=balance_color).place(x=309, y=180)

##--Pie chart--##

def pie_chart():
    global canvas_pie
    
    # Clear old widgets
    for widget in frame_gra_pie.winfo_children():
        widget.destroy()
    
    # Get expenses from database and apply filter
    revenues = view_revenues()
    expenses = view_expenses()
    filtered_revenues, filtered_expenses = apply_date_filter(revenues, expenses)
    
    # If no expenses, don't draw
    if not filtered_expenses:
        Label(frame_gra_pie, text='No expenses recorded', font=('Verdana 12'), 
              bg=co2, fg=co4).place(x=150, y=100)
        return
    
    # Group expenses by category
    expenses_by_category = {}
    for expense in filtered_expenses:
        category = expense[1]  # Category name
        value = expense[3]      # Expense value
        
        if category in expenses_by_category:
            expenses_by_category[category] += value
        else:
            expenses_by_category[category] = value
    
    # Prepare data for chart
    categories_list = list(expenses_by_category.keys())
    values_list = list(expenses_by_category.values())
    
    # Create proportional explosion (highlights largest category)
    max_value = max(values_list)
    explode = [0.1 if v == max_value else 0.05 for v in values_list]
    
    # Create chart
    figure = plt.Figure(figsize=(5, 3), dpi=90)
    figure.patch.set_facecolor(co2)
    ax = figure.add_subplot(111)
    
    # Select colors (cycling if more categories than colors)
    chart_colors = [colors[i % len(colors)] for i in range(len(categories_list))]
    
    ax.pie(
        values_list, 
        explode=explode, 
        wedgeprops=dict(width=0.2), 
        autopct='%1.1f%%', 
        colors=chart_colors,
        shadow=True, 
        startangle=90
    )
    
    legend = ax.legend(categories_list, loc="center right", bbox_to_anchor=(1.55, 0.50))
    legend.get_frame().set_facecolor(co1)
    legend.get_frame().set_edgecolor(co3)
    
    for text in legend.get_texts():
        text.set_color(co4)
    
    # Render in Tkinter
    canvas_pie = FigureCanvasTkAgg(figure, frame_gra_pie)
    canvas_pie.get_tk_widget().grid(row=0, column=0)

##--Date Filter--##

frameFiltering = Frame(bottomPart, bg=co1)
frameFiltering.place(x=5, y=5, width=880, height=35)

##--Bottom frames--##

incomeSection = Frame(bottomPart, width=450, height=250, bg=co1)
incomeSection.place(x=5, y=45)

operationsSection = Frame(bottomPart, width=400, height=250, bg=co1)
operationsSection.place(x=460, y=45)

Label(frameFiltering, text='Filter by period:', font=('Ivy 9'), 
      bg=co1, fg=co4).place(x=5, y=8)

# Period combobox
period_var = StringVar()
combo_period = ttk.Combobox(frameFiltering, width=10, font=('Ivy 9'), textvariable=period_var, state='readonly')
combo_period['values'] = ('All', 'Today', 'This Week', 'This Month', 'This Year', 'Custom')
combo_period.set('All')
combo_period.place(x=130, y=8)

# Revenue section title (moved to the right of filter)
Label(frameFiltering, text='Income and Expenses', anchor=W, font=('Verdana 11 bold'), 
      bg=co1, fg=co4).place(x=550, y=8)

# Custom dates (initially hidden)
Label(frameFiltering, text='From:', font=('Ivy 8'), bg=co1, fg=co4).place(x=240, y=10)
start_date = DateEntry(frameFiltering, width=10, background=co1, foreground=co4, 
                        borderwidth=1, headersbackground=co2, headersforeground=co4,
                        selectbackground=co5, selectforeground=co4, normalbackground=co1,
                        normalforeground=co4, weekendbackground=co2, weekendforeground=co4,
                        date_pattern='dd/MM/yyyy')
start_date.place(x=265, y=8)
start_date.place_forget()  # Hide initially

Label(frameFiltering, text='To:', font=('Ivy 8'), bg=co1, fg=co4).place(x=240, y=10)
label_to = Label(frameFiltering, text='To:', font=('Ivy 8'), bg=co1, fg=co4)
label_to.place(x=355, y=10)
label_to.place_forget()  # Hide initially

end_date = DateEntry(frameFiltering, width=10, background=co1, foreground=co4,
                     borderwidth=1, headersbackground=co2, headersforeground=co4,
                     selectbackground=co5, selectforeground=co4, normalbackground=co1,
                     normalforeground=co4, weekendbackground=co2, weekendforeground=co4,
                     date_pattern='dd/MM/yyyy')
end_date.place(x=380, y=8)
end_date.place_forget()  # Hide initially

##--Table--##

def show_income():
    # Clear previous table
    for widget in incomeSection.winfo_children():
        widget.destroy()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", background=co2, foreground=co4, rowheight=25, fieldbackground=co2)
    style.configure("Treeview.Heading", background=co1, foreground=co4, relief="flat", 
                   font=('Verdana 10 bold'))
    style.map('Treeview', background=[('selected', co5)], foreground=[('selected', co4)])
    
    table_head = ['#Id', 'Type', 'Category', 'Date', 'Amount']
    
    global tree
    tree = ttk.Treeview(incomeSection, selectmode="extended", columns=table_head, show="headings")
    
    vsb = ttk.Scrollbar(incomeSection, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(incomeSection, orient="horizontal", command=tree.xview)
    
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    
    incomeSection.grid_rowconfigure(0, weight=1)
    incomeSection.grid_columnconfigure(0, weight=1)
    
    hd = ["center", "center", "center", "center", "center"]
    h = [30, 60, 100, 100, 100]
    
    for n, col in enumerate(table_head):
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=hd[n])
    
    # Get data
    revenues = view_revenues()
    expenses = view_expenses()
    
    # Apply date filter
    filtered_revenues, filtered_expenses = apply_date_filter(revenues, expenses)
    
    # Insert in table
    for item in filtered_revenues:
        tree.insert('', 'end', values=(item[0], 'Income', item[1], item[2], f'$ {item[3]:.2f}'))
    
    for item in filtered_expenses:
        tree.insert('', 'end', values=(item[0], 'Expense', item[1], item[2], f'$ {item[3]:.2f}'))

##--Form--##

Label(operationsSection, text='Insert new transactions', height=1, anchor=NW, 
      font=('Verdana 10 bold'), bg=co1, fg=co4).place(x=10, y=10)

# Type
Label(operationsSection, text='Type', height=1, anchor=NW, font=('Ivy 10'), 
      bg=co1, fg=co4).place(x=10, y=40)
type_var = StringVar()
combo_type = ttk.Combobox(operationsSection, width=20, font=('Ivy 10'), textvariable=type_var)
combo_type['values'] = ('Income', 'Expense')
combo_type.place(x=110, y=41)

# Category (now with free text input)
Label(operationsSection, text='Category', height=1, anchor=NW, font=('Ivy 10'), 
      bg=co1, fg=co4).place(x=10, y=70)
category_var = StringVar()
combo_category = ttk.Combobox(operationsSection, width=20, font=('Ivy 10'), textvariable=category_var)
combo_category['values'] = ()  # Empty list - doesn't show suggestions
combo_category.place(x=110, y=71)

# Date
Label(operationsSection, text='Date', height=1, anchor=NW, font=('Ivy 10'), 
      bg=co1, fg=co4).place(x=10, y=100)
e_cal = DateEntry(operationsSection, width=22, background='darkblue', foreground='white', 
                 borderwidth=2)
e_cal.place(x=110, y=101)

# Amount
Label(operationsSection, text='Amount', height=1, anchor=NW, font=('Ivy 10'), 
      bg=co1, fg=co4).place(x=10, y=130)
e_value = Entry(operationsSection, width=24, justify='left', relief='solid')
e_value.place(x=110, y=131)

##--Button functions--##

def add_transaction():
    trans_type = type_var.get()
    category = category_var.get().strip()
    date = e_cal.get()
    value = e_value.get()
    
    if not trans_type or not category or not value:
        messagebox.showerror('Error', 'Fill in all fields!')
        return
    
    try:
        value = float(value.replace(',', '.'))
    except:
        messagebox.showerror('Error', 'Invalid value!')
        return
    
    # Validate if value is positive
    if value <= 0:
        messagebox.showerror('Error', 'Value must be greater than zero!')
        return
    
    if trans_type == 'Income':
        insert_revenues((category, date, value))
    else:
        insert_expenses((category, date, value))
    
    type_var.set('')
    category_var.set('')
    e_value.delete(0, END)
    
    update_all()
    messagebox.showinfo('Success', f'{trans_type} added successfully!')

def delete_transaction():
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        
        item_id = values[0]
        trans_type = values[1]
        
        response = messagebox.askyesno('Confirm', f'Do you want to delete this {trans_type}?')
        
        if response:
            if trans_type == 'Income':
                delete_revenues((item_id,))
            else:
                delete_expenses((item_id,))
            
            update_all()
            messagebox.showinfo('Success', f'{trans_type} deleted successfully!')
    except:
        messagebox.showerror('Error', 'Select an item to delete!')

def generate_report():
    """Generates a TXT report with all transactions"""
    import os
    from datetime import datetime
    
    # Create reports folder if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # File name in format: Report {User} {Date}
    current_date = datetime.now().strftime('%d-%m-%Y')
    file_name = f'reports/Report {logged_user} {current_date}.txt'
    
    try:
        # Get data
        revenues = view_revenues()
        expenses = view_expenses()
        
        # Calculate totals
        total_revenues = sum([i[3] for i in revenues])
        total_expenses = sum([i[3] for i in expenses])
        balance = total_revenues - total_expenses
        percent = (total_expenses / total_revenues * 100) if total_revenues > 0 else 0
        
        # Create report
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write('=' * 70 + '\n')
            file.write('FINANCIAL REPORT\n')
            file.write('=' * 70 + '\n\n')
            
            file.write(f'User: {logged_user}\n')
            file.write(f'Generation Date: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n\n')
            
            file.write('-' * 70 + '\n')
            file.write('GENERAL SUMMARY\n')
            file.write('-' * 70 + '\n')
            file.write(f'Total Monthly Income:      $ {total_revenues:>12.2f}\n')
            file.write(f'Total Monthly Expenses:    $ {total_expenses:>12.2f}\n')
            file.write(f'Account Balance:           $ {balance:>12.2f}\n')
            file.write(f'Percentage Spent:          {percent:>12.2f}%\n\n')
            
            # Revenues
            file.write('-' * 70 + '\n')
            file.write('INCOME\n')
            file.write('-' * 70 + '\n')
            if revenues:
                file.write(f'{"ID":<5} {"Category":<20} {"Date":<12} {"Value":>15}\n')
                file.write('-' * 70 + '\n')
                for revenue in revenues:
                    file.write(f'{revenue[0]:<5} {revenue[1]:<20} {revenue[2]:<12} $ {revenue[3]:>10.2f}\n')
            else:
                file.write('No income recorded.\n')
            file.write('\n')
            
            # Expenses
            file.write('-' * 70 + '\n')
            file.write('EXPENSES\n')
            file.write('-' * 70 + '\n')
            if expenses:
                file.write(f'{"ID":<5} {"Category":<20} {"Date":<12} {"Value":>15}\n')
                file.write('-' * 70 + '\n')
                for expense in expenses:
                    file.write(f'{expense[0]:<5} {expense[1]:<20} {expense[2]:<12} $ {expense[3]:>10.2f}\n')
            else:
                file.write('No expenses recorded.\n')
            file.write('\n')
            
            # Expenses by category
            file.write('-' * 70 + '\n')
            file.write('EXPENSES BY CATEGORY\n')
            file.write('-' * 70 + '\n')
            if expenses:
                expenses_by_category = {}
                for expense in expenses:
                    category = expense[1]
                    value = expense[3]
                    if category in expenses_by_category:
                        expenses_by_category[category] += value
                    else:
                        expenses_by_category[category] = value
                
                file.write(f'{"Category":<30} {"Value":>20}\n')
                file.write('-' * 70 + '\n')
                for category, value in sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True):
                    file.write(f'{category:<30} $ {value:>15.2f}\n')
            else:
                file.write('No expenses by category.\n')
            
            file.write('\n')
            file.write('=' * 70 + '\n')
            file.write('END OF REPORT\n')
            file.write('=' * 70 + '\n')
        
        messagebox.showinfo('Success', f'Report generated successfully!\n\nFile: {file_name}')
        
        # Open reports folder
        os.startfile('reports')
        
    except Exception as e:
        messagebox.showerror('Error', f'Error generating report: {str(e)}')

# Bind to update when filter changes
combo_period.bind('<<ComboboxSelected>>', update_filter)
start_date.bind('<<DateEntrySelected>>', update_filter)
end_date.bind('<<DateEntrySelected>>', update_filter)

##--Buttons--##

Button(operationsSection, text='Add', width=10, height=1, bg=co8, fg=co4, 
       font=('Ivy 9 bold'), relief='raised', command=add_transaction).place(x=10, y=165)

Button(operationsSection, text='Delete', width=10, height=1, bg=co6, fg=co4,
       font=('Ivy 9 bold'), relief='raised', command=delete_transaction).place(x=120, y=165)

Button(operationsSection, text='Report', width=10, height=1, bg=co9, fg=co1,
       font=('Ivy 9 bold'), relief='raised', command=generate_report).place(x=230, y=165)

##--Initialize--##

update_all()
window.mainloop()