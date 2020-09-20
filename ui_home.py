from ui import UI

class Ui_home(UI):
    def __init__(self, parent):
        super(Ui_home, self).__init__(parent.lcd)
        self.parent = parent

        self.append_text(    'text_0', 10,  10, 'GUI Test')
        self.append_button('button_0', 20,  50, 'acceleration')
        self.append_button('button_1', 20,  90, 'gyro')
        self.append_button('button_2', 20, 130, 'geomagnetism')

        self.buttons['button_0'].set_action( lambda : parent.change_state('acceleration') )
        self.buttons['button_1'].set_action( lambda : parent.change_state('gyro') )
        self.buttons['button_2'].set_action( lambda : parent.change_state('geomagnetism') )

        self.buttons['button_0'].selected = True

    def control(self, button):
        if button['up']:
            self.set_select_button(-1)

        if button['down']:
            self.set_select_button(1)

        if button['right']:
            self.selected_button().action()
