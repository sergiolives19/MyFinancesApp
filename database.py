import datetime

class DataBase:
    def __init__(self, filename):
        self.filename = filename

    def add_expense(self, amount, category):
        with open(self.filename, 'a') as f:
            date = str(datetime.datetime.now()).split(' ')[0].replace('-','/')
            f.write(date + ' ' + amount + ' ' + category + '\n')
        f.close()

    def all_expenses(self):
        f = open(self.filename, 'r')
        expenses = []
        for expense in f:
            expense = expense.replace('\n', '')
            expense = expense.split(' ')
            expenses.append(expense)
        return expenses

    def expenses(self, year, month, day):
        f = open(self.filename, 'r')
        expenses = {}
        for expense in f:
            expense = expense.replace('\n', '')
            expense = expense.split(' ')
            date = expense[0].split('/')
            if year == '' or int(year) == int(date[0]):
                if month == '' or int(month) == int(date[1]):
                    if day == '' or int(day) == int(date[2]):
                        if expense[2] in expenses:
                            expenses[expense[2]] += float(expense[1])
                            expenses[expense[2]] = round(expenses[expense[2]], 2)
                        else:
                            expenses[expense[2]] = float(expense[1])
        f.close()
        return expenses

    def find_expense(self, year, month, day, category):
        f = open(self.filename, 'r')
        total_expense = 0
        expenses = []
        for expense in f:
            expense = expense.replace('\n', '')
            expense = expense.split(' ')
            date = expense[0].split('/')
            if category == '' or expense[2] == category:
                if year == '' or int(year) == int(date[0]):
                    if month == '' or int(month) == int(date[1]):
                        if day == '' or int(day) == int(date[2]):
                            total_expense += float(expense[1])
                            expenses.append(expense)
        return expenses, round(total_expense, 2)