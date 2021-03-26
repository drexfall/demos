from kivy.animation import Animation
from kivy.clock import Clock
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang.builder import Builder

app = None

Builder.load_string("""
<Check@RelativeLayout>:
    id: checkbox
    text: ''
    active: False
    MDCheckbox:
        id: check
        size_hint: None, None
        size: dp(48), dp(48)
        active: root.active
        pos_hint: {'center_x': .3, 'center_y': .5}
        on_release: setattr(root,'active',self.active)
    MDLabel:
        id: label
        text: root.text
        pos_hint: {'center_x': 0.9, 'center_y': .5}
        font_style: 'H6'

<Field@MDTextField>:
    index: 1
    size_hint_x: 0.2
    pos_hint: {'center_x': 1.5, 'center_y': (5-root.index)/10}
    on_text: root.parent.parent.color_text(self,self.text)

<Main>:
    
    MDSpinner:
        id: spinner
        size_hint: None, None
        size: dp(48), dp(48)
        pos_hint: {'center_x': .5, 'center_y': .7}
        active: True if state_check.active else False

    MDFloatLayout:
        id: mainfloat
        Check:
            id: state_check
            text:'Start'
            pos_hint: {'center_x': .5, 'center_y': .4}
            active: True

        Check:
            id: prim_check
            text:'Primary Pallete'
            pos_hint: {'center_x': .5, 'center_y': .3}
            active: True
        
        Check:
            id: dark_check
            text:'Dark Mode'
            pos_hint: {'center_x': .5, 'center_y': .2}
            active: False

        Check:
            id: custom_color
            text:'Custom Color'
            pos_hint: {'center_x': .5, 'center_y': .1}
            active: False
    MDFloatLayout:
        id: textfloat
        Field:
            index: 1
            hint_text: 'Color of spinner'
        Field:
            index: 2
            hint_text: 'First color in palette'
        Field:
            index: 3
            hint_text: 'Second color in palette'
        Field:
            index: 4
            hint_text: 'Third color in palette'
        

"""
)

class Main(MDFloatLayout):
    def color_text(self, instance, value):
        if value:
            if value[0]!='#':
                instance.text = '#'+value
                Clock.schedule_once(lambda dt:instance.do_cursor_movement('cursor_end'),0.1)
            else:
                if len(value[1:])>6:
                    instance.text = value[:-1]
                else:
                    if len(value[1:])!=6:
                        value+=(6-len(value[1:]))*'0'
                    color = get_color_from_hex(value)
                    
                    if instance.index == 1:
                        self.spinner.color = color
                    else:
                        if len(self.spinner.palette)<=3:
                            self.spinner.palette.append(color)
                        else:
                            self.spinner.palette[instance.index-2] = color
                    

    def toggle_color(self, button):
        if button ==  self.custom_color:
            self.prim_check.state = 'normal' if button.state == 'down' else 'down'
        else:
            self.custom_color.state = 'normal' if button.state == 'down' else 'down'
            self.custom_color_func(self.custom_color)

        if self.prim_check.state == 'down':
            for text in self.ids["textfloat"].children:
                text.text = get_hex_from_color(app.theme_cls.primary_color)[1:]

    def custom_color_func(self, button):
        
        for index,opt in enumerate(self.ids["mainfloat"].children):
            Animation(pos_hint={'center_x': 0.3 if button.state =='down' else 0.5}, t='in_out_quad',d=(index+1)/3).start(opt)
        
        for index,opt in enumerate(self.ids["textfloat"].children):
            Animation(pos_hint={'center_x': 0.8 if button.state =='down' else 1.5}, t='in_out_quad',d=(index+1)/3).start(opt)
            

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.spinner = self.ids["spinner"]
        self.dark_check = self.ids["dark_check"].ids["check"]
        self.prim_check = self.ids["prim_check"].ids["check"]
        self.custom_color = self.ids["custom_color"].ids["check"]

        self.dark_check.bind(on_release = lambda bt: setattr(app.theme_cls,'theme_style', 'Dark' if bt.state == 'down' else 'Light'))
        self.prim_check.bind(on_release = self.toggle_color)
        self.custom_color.bind(on_release = self.toggle_color)
        self.custom_color.bind(on_release = self.custom_color_func)
        

        Clock.schedule_once(lambda dt:self.toggle_color(self.prim_check),0.1)
class MainApp(MDApp):
    def build(self):
        global app
        app = self
        return Main()

MainApp().run()
