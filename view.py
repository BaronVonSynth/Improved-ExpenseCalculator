#--Imports--#
import sqlite3 as lite

#--Database Connection--#
# Global variable to store the user's database path
_user_database = 'data.db'

def set_user_database(database_path):
    """
    Sets the database path for the current user
    Parameter: string with database path
    Example: set_user_database('data/user_finances.db')
    """
    global _user_database
    _user_database = database_path

def get_connection():
    """
    Returns a connection to the current user's database
    """
    return lite.connect(_user_database)

#--INSERT FUNCTIONS--#
def insert_category(i):
    """
    Inserts a new category
    Parameter: tuple with (name,)
    Example: insert_category(('Clothing',))
    """
    con = get_connection()
    with con: 
        cursor = con.cursor()
        query = 'INSERT INTO categories (name) VALUES (?)'
        cursor.execute(query, i)
    con.close()

def insert_revenues(i):
    """
    Inserts a new revenue
    Parameter: tuple with (category, date, value)
    Example: insert_revenues(('Salary', '2026-01-30', 3000.00))
    """
    con = get_connection()
    with con:
        cursor = con.cursor()
        query = 'INSERT INTO revenues (category, date, value) VALUES (?, ?, ?)'
        cursor.execute(query, i)
    con.close()

def insert_expenses(i):
    """
    Inserts a new expense
    Parameter: tuple with (category, date, value)
    Example: insert_expenses(('Food', '2026-01-30', 150.00))
    """
    con = get_connection()
    with con:
        cursor = con.cursor()
        query = 'INSERT INTO expenses (category, date, value) VALUES (?, ?, ?)'
        cursor.execute(query, i)
    con.close()

#--DELETE FUNCTIONS--#
def delete_revenues(d):
    """
    Deletes a revenue by ID
    Parameter: tuple with (id,)
    Example: delete_revenues((1,))
    """
    con = get_connection()
    with con:
        cursor = con.cursor()
        query = 'DELETE FROM revenues WHERE id=?'
        cursor.execute(query, d)
    con.close()

def delete_expenses(d):
    """
    Deletes an expense by ID
    Parameter: tuple with (id,)
    Example: delete_expenses((1,))
    """
    con = get_connection()
    with con:
        cursor = con.cursor()
        query = 'DELETE FROM expenses WHERE id=?'
        cursor.execute(query, d)
    con.close()

#--VIEW FUNCTIONS--#
def view_categories():
    """
    Returns list of all categories
    Return: [(id, name), ...]
    """
    categories_list = []
    con = get_connection()
    with con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM categories')
        rows = cursor.fetchall()
        for i in rows:
            categories_list.append(i)
    con.close()
    return categories_list

def view_revenues():
    """
    Returns list of all revenues
    Return: [(id, category, date, value), ...]
    """
    revenues_list = []
    con = get_connection()
    with con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM revenues')
        rows = cursor.fetchall()
        for i in rows:
            revenues_list.append(i)
    con.close()
    return revenues_list

def view_expenses():
    """
    Returns list of all expenses
    Return: [(id, category, date, value), ...]
    """
    expenses_list = []
    con = get_connection()
    with con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM expenses')
        rows = cursor.fetchall()
        for i in rows:
            expenses_list.append(i)
    con.close()
    return expenses_list

def calculate_totals():
    """
    Calculates totals of revenues, expenses and balance
    Return: [total_revenues, total_expenses, balance]
    """
    revenues = view_revenues()
    expenses = view_expenses()
    
    total_revenues = sum([i[3] for i in revenues]) if revenues else 0
    total_expenses = sum([i[3] for i in expenses]) if expenses else 0
    balance = total_revenues - total_expenses
    
    return [total_revenues, total_expenses, balance]

def calculate_percentage_spent():
    """
    Calculates the percentage of revenue that was spent
    Return: float (0 to 100)
    """
    totals = calculate_totals()
    total_revenue = totals[0]
    total_expenses = totals[1]
    
    if total_revenue > 0:
        return (total_expenses / total_revenue) * 100
    else:
        return 0
