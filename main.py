from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from database import DataBase
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

class MainWindow(Screen):
        def __init__(self, **kwargs):
            super(MainWindow, self).__init__(**kwargs)
            #self.grid = GridLayout(cols=1)
            self.layout = FloatLayout()
            self.btn1 = Button(font_size=14, text='New expense', size_hint=(0.3,0.2),
                               pos_hint={'x': 0.1, 'top': 0.9}, color=(0,1,0,1), background_color=(0,1,1,1))
            self.btn2 = Button(font_size=14, text='My expenses1', size_hint=(0.3, 0.2),
                               pos_hint={'x': 0.1, 'top': 0.7}, color=(0,1,0,1), background_color=(0, 1, 1, 1))
            self.btn3 = Button(font_size=14, text='My expenses2', size_hint=(0.3, 0.2),
                               pos_hint={'x': 0.1, 'top': 0.5}, color=(0, 1, 0, 1), background_color=(0, 1, 1, 1))
            self.layout.add_widget(self.btn1)
            self.layout.add_widget(self.btn2)
            self.layout.add_widget(self.btn3)
            self.add_widget(self.layout)
            self.btn1.bind(on_press=self.screen_transition1)
            self.btn2.bind(on_press=self.screen_transition2)
            self.btn3.bind(on_press=self.screen_transition3)

        def screen_transition1(self, *args):
            self.manager.current = 'new_expense'

        def screen_transition2(self, *args):
            self.manager.current = 'my_expenses1'

        def screen_transition3(self, *args):
            self.manager.current = 'my_expenses2'

class NewExpense(Screen):
    def __init__(self, **kwargs):
        super(NewExpense, self).__init__(**kwargs)

        self.grid1 = GridLayout(cols=1)
        self.grid2 = GridLayout(cols=2)

        self.grid2.add_widget(Label(text='Import: '))
        self.amount = TextInput(multiline=False)
        self.grid2.add_widget(self.amount)
        self.grid2.add_widget(Label(text='Category: '))
        self.category = TextInput(multiline=False)
        self.grid2.add_widget(self.category)

        self.grid1.add_widget(self.grid2)

        self.btn1 = Button(text='Submit', font_size=20)
        self.btn2 = Button(text='Go back', font_size=20)
        self.grid1.add_widget(self.btn1)
        self.grid1.add_widget(self.btn2)
        self.btn1.bind(on_press=self.submit)
        self.btn2.bind(on_press=self.screen_transition)
        self.add_widget(self.grid1)

    def check(self):
        if self.amount.text != '':
            for c in self.amount.text:
                if c not in '0123456789.,':
                    invalidForm()
                    return False
            if self.amount.text.count(',') + self.amount.text.count('.') > 1:
                invalidForm()
                return False
            return True
        else:
            invalidForm()
            return False

    def submit(self, *args):
        if self.check():
            if ',' in self.amount.text:
                self.amount.text = self.amount.text.replace(',', '.')
            self.amount.text = str(round(float(self.amount.text), 2))
            self.category.text = self.category.text.lower()
            db.add_expense(self.amount.text, self.category.text)
            self.reset()
            self.manager.current = 'main'
        else:
            pass

    def reset(self):
        self.amount.text = ''
        self.category.text = ''

    def screen_transition(self, *args):
        self.manager.current = 'main'

class MyExpenses1(Screen):
    def __init__(self, **kwargs):
        super(MyExpenses1, self).__init__(**kwargs)

        self.grid1 = GridLayout(cols=1)
        self.grid2 = GridLayout(cols=2)

        #self.grid2.bind(minimum_height=self.grid1.setter('height'))
        self.grid2.add_widget(Label(text='Year'))
        self.year = TextInput(multiline=False)
        self.grid2.add_widget(self.year)
        self.grid2.add_widget(Label(text='Month'))
        self.month = TextInput(multiline=False)
        self.grid2.add_widget(self.month)
        self.grid2.add_widget(Label(text='Day'))
        self.day = TextInput(multiline=False)
        self.grid2.add_widget(self.day)
        self.grid2.add_widget(Label(text='Category'))
        self.category = TextInput(multiline=False)
        self.grid2.add_widget(self.category)
        self.grid1.add_widget(self.grid2)

        self.btn1 = Button(text='Calculate')
        self.btn1.bind(on_press=self.calculate)
        self.grid1.add_widget(self.btn1)

        self.result = Label()
        self.grid1.add_widget(self.result)

        self.btn2 = Button(text='Go back', font_size=20)
        self.grid1.add_widget(self.btn2)
        self.btn2.bind(on_press=self.screen_transition)

        self.add_widget(self.grid1)

    def calculate(self, *args):
        result = db.find_expense(self.year.text, self.month.text, self.day.text, self.category.text)
        print(result[0])
        self.result.text = f'The total amount is {result[1]}'

    def reset(self):
        self.year.text = ''
        self.month.text = ''
        self.day.text = ''
        self.category.text = ''
        self.result.text = ''

    def screen_transition(self, *args):
        self.reset()
        self.manager.current = 'main'

class MyExpenses2(Screen):
    def __init__(self, **kwargs):
        super(MyExpenses2, self).__init__(**kwargs)

        self.box = BoxLayout(orientation='vertical')

        self.grid1 = GridLayout(cols=4, size_hint_y=None)
        self.grid1.bind(minimum_height=self.grid1.setter('height'))
        self.grid1.add_widget(Label(text='Date', size_hint_y=None))
        self.grid1.add_widget(Label(text='Import', size_hint_y=None))
        self.grid1.add_widget(Label(text='Concept', size_hint_y=None))
        self.btn1 = Button(text='Update', size_hint_y=None)
        self.grid1.add_widget(self.btn1)
        self.btn1.bind(on_press=self.update_grid)

        self.box.add_widget(self.grid1)

        self.create_grid()

        self.btn2 = Button(text='Go back', font_size=20)
        self.box.add_widget(self.btn2)
        self.btn2.bind(on_press=self.screen_transition)
        self.add_widget(self.box)

    def create_grid(self):

        self.grid2 = GridLayout(cols=4, size_hint_y=None)
        self.grid2.bind(minimum_height=self.grid2.setter('height'))
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.expenses = db.all_expenses()
        for i in range(len(self.expenses)):
            self.grid2.add_widget(Label(text=self.expenses[i][0], size_hint_y=None))
            self.grid2.add_widget(Label(text=self.expenses[i][1], size_hint_y=None, color=(1,0,0,1)))
            self.grid2.add_widget(Label(text=self.expenses[i][2], size_hint_y=None))
            self.grid2.add_widget(Button(text='Delete', size_hint_y=None))

        scroll.add_widget(self.grid2)
        self.box.add_widget(scroll)

    def update_grid(self, *args):
        new_expenses = db.all_expenses()
        l1 = len(self.expenses)
        l2 = len(new_expenses)
        if l2 > l1:
            self.expenses = new_expenses
            for i in range(l1, l2):
                self.grid2.add_widget(Label(text=self.expenses[i][0], size_hint_y=None))
                self.grid2.add_widget(Label(text=self.expenses[i][1], size_hint_y=None))
                self.grid2.add_widget(Label(text=self.expenses[i][2], size_hint_y=None))
                self.grid2.add_widget(Button(text='Delete', size_hint_y=None))

    def screen_transition(self, *args):
        self.manager.current = 'main'

def invalidForm():
    pop = Popup(title='Invalid form', content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()

db = DataBase('myexpenses.txt')
sm = WindowManager(transition=FadeTransition())

screens = [MainWindow(name='main'), NewExpense(name='new_expense'),
           MyExpenses1(name='my_expenses1'), MyExpenses2(name='my_expenses2')]
for screen in screens:
          sm.add_widget(screen)

sm.current = 'main'

class MyFinancesApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyFinancesApp().run()