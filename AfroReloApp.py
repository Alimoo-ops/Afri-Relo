from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import webbrowser  # ✅ Added to handle clickable link

ASSETS = 'assets/'

def play_intro_sound(*args):
    sound = SoundLoader.load(ASSETS + 'afri_intro.mp3')
    if sound:
        sound.loop = True
        sound.play()
    else:
        print("❌ Could not load intro sound.")

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source=ASSETS + 'afri_bg.jpg', allow_stretch=True, keep_ratio=False), index=0)
        layout.add_widget(Image(source=ASSETS + 'afri_logo.png', size_hint=(.4, .4), pos_hint={'center_x': .5, 'top': 1}))
        
        welcome_label = Label(
            text=(
                "[b]Welcome to Afri Relo[/b]\n"
                "Dear Friend,\n\n"
                "In these uncertain times of global war threats, we understand your fears and your search for safety.\n\n"
                "Kenya welcomes you — a peaceful and stable country in the heart of Africa.\n\n"
                "Through Afri Relo, we guide you towards a fresh start.\n\n"
                "You are not alone. This is your safe path forward.\n\n"
                "[i]Karibu Kenya.[/i]"
            ),
            markup=True,
            font_size='22sp' ,
            size_hint=(.9, .6),
            pos_hint={'center_x': .5, 'center_y': .45},
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        welcome_label.bind(size=lambda s, v: setattr(s, 'text_size', (s.width, None)))
        layout.add_widget(welcome_label)

        skip_button = Button(text="Next", size_hint=(.3, .1), pos_hint={'center_x': .5, 'y': 0.05})
        skip_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'form'))
        layout.add_widget(skip_button)

        self.add_widget(layout)

class FormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source=ASSETS + 'afri_bg.jpg', allow_stretch=True, keep_ratio=False), index=0)

        scroll = ScrollView(size_hint=(1, 0.9), pos_hint={'x': 0, 'top': 1})
        form_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        intro_label = Label(
            text="Please fill in the form below accurately.\nAll information is confidential.",
            font_size='19sp' ,
            size_hint_y=None, height=80, color=(0, 0, 0, 1),
            halign='center', valign='middle'
        )
        intro_label.bind(size=lambda s, v: setattr(s, 'text_size', (s.width, None)))
        form_layout.add_widget(intro_label)

        self.inputs = {}
        questions = [
            "Full Name",
            "Country of Origin",
            "Reason for Relocation",
            "Do you have a criminal record? (Yes/No)",
            "Do you have a valid passport?",
            "Preferred Kenyan city or town?",
            "Any health conditions we should know?"
        ]

        for question in questions:
            lbl = Label(text=question, font_size='20sp' ,
            size_hint_y=None, height=30, color=(0, 0, 0, 1),
                        halign='left', valign='middle')
            lbl.bind(size=lambda s, v: setattr(s, 'text_size', (s.width, None)))
            ti = TextInput(size_hint_y=None, height=40)
            form_layout.add_widget(lbl)
            form_layout.add_widget(ti)
            self.inputs[question] = ti

        scroll.add_widget(form_layout)
        layout.add_widget(scroll)

        next_btn = Button(text="Next", size_hint=(.3, .1), pos_hint={'center_x': .5, 'y': 0})
        next_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'terms'))
        layout.add_widget(next_btn)

        self.add_widget(layout)

class TermsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source=ASSETS + 'afri_bg.jpg', allow_stretch=True, keep_ratio=False), index=0)

        terms_text = (
            "[b]Terms and Conditions[/b]\n\n"
            "1. Arrival: A designated representative will meet you at the airport.\n"
            "2. Payment: Relocation fee must be paid before travel.\n"
            "3. Verification: Confirm home of interest via images before payment.\n"
            "4. Refunds: Refunds allowed (minus transaction fee).\n"
            "5. Payment: Via PayPal (link & QR provided).\n"
            "6. Contact: WhatsApp +254718357737 (Alimoo)."
        )

        label = Label(text=terms_text, markup=True,
                      font_size='22sp' ,
                      size_hint=(.9, .8), pos_hint={'center_x': .5, 'center_y': .55},
                      halign='left', valign='top',
                      color=(0, 0, 0, 1))
        label.bind(size=lambda s, v: setattr(s, 'text_size', (s.width, None)))
        layout.add_widget(label)

        btn = Button(text="Next", size_hint=(.3, .1), pos_hint={'center_x': .5, 'y': 0.05})
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'payment'))
        layout.add_widget(btn)

        self.add_widget(layout)

class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source=ASSETS + 'afri_bg.jpg', allow_stretch=True, keep_ratio=False), index=0)

        label = Label(text=(
            "[b]Payment Instructions[/b]\n\n"
            "Use the following PayPal link to complete your relocation fee:\n\n"
            "[ref=paypal][i]https://www.paypal.com/ncp/payment/FLCB46N9ZTERE[/i][/ref]\n\n"
            "Make sure to screenshot your transaction for reference."
        ),
            markup=True, font_size='18sp' ,
            size_hint=(.9, .8),
            pos_hint={'center_x': .5, 'center_y': .55},
            halign='left', valign='top',
            color=(0, 0, 0, 1)
        )
        label.bind(size=lambda s, v: setattr(s, 'text_size', (s.width, None)))
        label.bind(on_ref_press=lambda instance, ref: webbrowser.open("https://www.paypal.com/ncp/payment/FLCB46N9ZTERE"))
        layout.add_widget(label)

        btn = Button(text="View QR", size_hint=(.3, .1), pos_hint={'center_x': .5, 'y': 0.05})
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'qr'))
        layout.add_widget(btn)

        self.add_widget(layout)

class QRScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Image(source=ASSETS + 'afri_bg.jpg', allow_stretch=True, keep_ratio=False), index=0)

        qr = Image(source=ASSETS + 'afri_qr.png', size_hint=(.6, .6),
                   pos_hint={'center_x': .5, 'center_y': .6})
        layout.add_widget(qr)

        back_btn = Button(text="Done", size_hint=(.3, .1), pos_hint={'center_x': .5, 'y': 0.05})
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'welcome'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

# ✅ Screen Manager
screen_manager = ScreenManager(transition=FadeTransition())
screen_manager.add_widget(WelcomeScreen(name='welcome'))
screen_manager.add_widget(FormScreen(name='form'))
screen_manager.add_widget(TermsScreen(name='terms'))
screen_manager.add_widget(PaymentScreen(name='payment'))
screen_manager.add_widget(QRScreen(name='qr'))

class AfriReloApp(App):
    def build(self):
        Clock.schedule_once(play_intro_sound, 1.0)
        return screen_manager

if __name__ == '__main__':
    AfriReloApp().run()