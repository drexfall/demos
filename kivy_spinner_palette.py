from kivy.animation import Animation
from kivy.clock import Clock
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang.builder import Builder
from kivymd.color_definitions import palette
get_color_from_hex
app = None

Builder.load_string("""
#: import color kivy.utils.get_color_from_hex
#: import colors kivymd.color_definitions.colors
#: import MDRaisedButton kivymd.uix.button.MDRaisedButton
<Main>:
    
    MDSpinner:
        id: spinner
        size_hint: None, None
        size: dp(48), dp(48)
        color: color('000000')
        pos_hint: {'center_x': .5, 'center_y': .7}

    MDFloatLayout:
        id: mainfloat
        hue: "500"
        on_kv_post:
            [self.add_widget(MDRaisedButton(text = text, 
            pos_hint = {"center_x":0.5,"center_y":(index+1)/10}, 
            md_bg_color = color(colors[text][self.hue]),
            on_release = self.parent.apply_palette)) for index,text in enumerate(('Blue','Red',"Green","Yellow"))]
        
        

"""
                    )


class Main(MDFloatLayout):

    def apply_palette(self, button):
        global app
        app.theme_cls.primary_palette = button.text

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(app.theme_cls.primary_hue)


class MainApp(MDApp):
    def build(self):
        global app
        app = self
        return Main()


MainApp().run()
