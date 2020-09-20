class UI(object):
    def __init__(self, lcd):
        self.lcd, self.buttons, self.texts = lcd, {}, {}

    def append_button(self, name, x, y, text):
        self.buttons[name] = Button(self, x, y, text)

    def append_text(self, name, x, y, text):
        self.texts[name] = Text(self, x, y, text)

    def draw(self):
        self.lcd.data_reset()

        for text in self.texts:
            self.texts[text].draw()
        
        for button in self.buttons:
            self.buttons[button].draw()
        
        self.lcd.data_update_all_line()

    def reset(self):
        self.lcd.data_reset()
        
    def set_select_button(self, direction):
        buttons = self.buttons
        keys = list( buttons.keys() )
        selected_list = [ buttons[key].selected for key in keys ]
        selected_index = selected_list.index(True)
        buttons[ keys[selected_index] ].selected = False

        selected_index += direction
        
        if selected_index < 0:
            buttons[ keys[-1] ].selected = True
            return

        if selected_index > len(buttons) - 1:
            buttons[ keys[0] ].selected = True
            return

        buttons[ keys[selected_index] ].selected = True

    def selected_button(self):
        for key in self.buttons:
            button = self.buttons[key]
            if button.selected is True:
                return button
        return None

class Button(object):
    def __init__(self, parent, x, y, text):
        self.parent, self.x, self.y, self.text = parent, x, y, text
        self.selected, self.action = False, None

    def draw(self):
        self.parent.lcd.string(self.x + 10, self.y, self.text)
        if self.selected:
            self.parent.lcd.rect(
                self.x, self.y, 
                self.x + len(self.text) * 16 + 10, 
                self.y + 30
            )

    def set_text(self, text):
        self.text = text

    def set_action(self, action):
        self.action = action

class Text(object):
    def __init__(self, parent, x, y, text):
        self.parent, self.x, self.y, self.text = parent, x, y, text

    def draw(self):
        self.parent.lcd.string(self.x, self.y, self.text)

    def set_text(self, text):
        self.text = text
