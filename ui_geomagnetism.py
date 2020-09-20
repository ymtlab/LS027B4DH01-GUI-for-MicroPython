from ui import UI

class Ui_geomagnetism(UI):
    def __init__(self, parent):
        super(Ui_geomagnetism, self).__init__(parent.lcd)
        self.parent = parent

        self.append_text(    'text_0',  10,  10, 'Geomagnetism')
        self.append_text(    'text_1',  20,  60, 'X')
        self.append_text(    'text_2',  20, 110, 'Y')
        self.append_text(    'text_3',  20, 160, 'Z')
        self.append_text(    'text_4',  50,  60, '0.000')
        self.append_text(    'text_5',  50, 110, '0.000')
        self.append_text(    'text_6',  50, 160, '0.000')
        self.append_button('button_0', 200, 200, 'back')

        self.buttons['button_0'].set_action( lambda : self.parent.change_state('home') )
        self.buttons['button_0'].selected = True

    def control(self, button):
        
        if button['right']:
            self.buttons['button_0'].action()
            return
        
        mag = self.parent.mpu9250.read_magnet()

        self.texts['text_4'].set_text( str(mag['x']) )
        self.texts['text_5'].set_text( str(mag['y']) )
        self.texts['text_6'].set_text( str(mag['z']) )
