from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

Window.clearcolor = (0.1, 0.1, 0.1, 1)

class CalculatorApp(App):
    def build(self):
        self.operators = ['+', '-', '×', '÷']
        self.last_was_operator = None
        self.last_button = None
        self.expression = ""
        
        # Основной контейнер
        main_layout = GridLayout(cols=1, padding=10, spacing=5)
        
        # Дисплей
        self.display = Label(
            text='0',
            font_size='48sp',
            halign='right',
            valign='middle',
            color=(1, 1, 1, 1),
            size_hint_y=0.3
        )
        self.display.bind(size=self.display.setter('text_size'))
        main_layout.add_widget(self.display)
        
        # Сетка кнопок
        buttons_layout = GridLayout(cols=4, spacing=5)
        
        # Кнопки
        buttons = [
            'C', '←', '÷', '×',
            '7', '8', '9', '-',
            '4', '5', '6', '+',
            '1', '2', '3', '=',
            '0', '.', '', ''
        ]
        
        for label in buttons:
            if label == '':
                # Пустой виджет-заполнитель
                buttons_layout.add_widget(Label())
                continue
                
            btn = Button(
                text=label,
                font_size='24sp',
                background_normal='',
                background_color=self.get_button_color(label)
            )
            btn.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(btn)
        
        main_layout.add_widget(buttons_layout)
        return main_layout
    
    def get_button_color(self, label):
        if label in ['C', '←']:
            return (0.8, 0.2, 0.2, 1)  # Красный
        elif label in self.operators or label == '=':
            return (0.2, 0.4, 0.8, 1)  # Синий
        else:
            return (0.3, 0.3, 0.3, 1)  # Серый
    
    def on_button_press(self, instance):
        current = instance.text
        current_text = self.display.text
        
        if current == 'C':
            self.expression = ""
            self.display.text = '0'
            self.last_was_operator = None
            self.last_button = None
            
        elif current == '←':
            if len(self.expression) > 0:
                self.expression = self.expression[:-1]
                if self.expression == "":
                    self.display.text = '0'
                else:
                    self.display.text = self.expression
            
        elif current == '=':
            try:
                # Заменяем символы для eval
                expr = self.expression.replace('×', '*').replace('÷', '/')
                if expr:
                    result = eval(expr)
                    # Форматируем результат
                    if result == int(result):
                        self.display.text = str(int(result))
                    else:
                        self.display.text = str(round(result, 8))
                    self.expression = self.display.text
            except:
                self.display.text = 'Ошибка'
                self.expression = ""
            self.last_was_operator = None
            self.last_button = None
            
        elif current in self.operators:
            if not self.last_was_operator and self.expression:
                self.expression += current
                self.display.text = self.expression
                self.last_was_operator = True
                self.last_button = current
            elif self.last_was_operator and self.last_button in self.operators:
                # Заменяем последний оператор
                self.expression = self.expression[:-1] + current
                self.display.text = self.expression
                self.last_button = current
                
        elif current == '.':
            if not self.last_was_operator:
                # Проверяем, нет ли уже точки в последнем числе
                parts = self.expression.replace('+', ' ').replace('-', ' ').replace('×', ' ').replace('÷', ' ').split()
                if parts and '.' not in parts[-1]:
                    self.expression += '.'
                    self.display.text = self.expression
                elif not parts:
                    self.expression = '0.'
                    self.display.text = self.expression
                    
        else:  # Цифры
            if self.last_was_operator:
                self.expression += current
                self.display.text = self.expression
                self.last_was_operator = False
            else:
                if self.expression == '0' or self.display.text == '0':
                    self.expression = current
                else:
                    self.expression += current
                self.display.text = self.expression

if __name__ == '__main__':
    CalculatorApp().run()
