import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger


logger = setup_logger('db_helper')




@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Falguni@1974',
        database='expense_manager'
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("Select * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with {expense_date, amount, category, notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes))
        
def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with {start_date, end_date}")
    with get_db_cursor() as cursor:
        cursor.execute('''SELECT category,sum(amount) as total
                            FROM expenses
                            where expense_date 
                            BETWEEN %s AND %s
                            group by category;''', (start_date,end_date,))
        data  = cursor.fetchall()
        return data
    
def fetch_total_expenses_by_month():
    logger.info(f"fetch_total_expenses_by_month called")
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT 
                MONTH(expense_date) as expense_month, 
                SUM(amount) as total
                from expenses
                GROUP by expense_month
                order by expense_month;
        ''')
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    # delete_expenses_for_date("2024-08-25")
    expenses = fetch_total_expenses_by_month()
    print(expenses)
    # insert_expense("2024-08-25",40,"Food","Eat tasty samso chat")
    # data = fetch_expense_summary('2024-08-01', '2024-08-05')
    # print(data)

    