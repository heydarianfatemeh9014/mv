from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup


def sound_play():
    sound = SoundLoader.load("bib.mp3")
    if sound:
        sound.play()


class ResistivityLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background image
        self.bg = Image(source="imagess/wall7.jpg",
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"x": 0, "y": 0})
        self.add_widget(self.bg)

        # Instruction label
        self.instr_label = Label(text="Enter any three values and leave the desired one empty",
                                 font_size=18,
                                 color=(0, 0.5, 0, 1),  # green
                                 size_hint=(0.9, 0.1),
                                 pos_hint={"x": 0.05, "y": 0.9})
        self.add_widget(self.instr_label)

        # Resistivity (ρ)
        self.P_label = Label(text="Resistivity (ρ):",
                             font_size=20,
                             color=(1, 0, 0, 1),  # red
                             size_hint=(0.4, 0.1),
                             pos_hint={"x": 0.05, "y": 0.75})
        self.add_widget(self.P_label)
        self.P_ent = TextInput(multiline=False,
                               font_size=20,
                               size_hint=(0.4, 0.1),
                               pos_hint={"x": 0.55, "y": 0.75})
        self.add_widget(self.P_ent)

        # Length (L)
        self.L_label = Label(text="Length (L):",
                             font_size=20,
                             color=(1, 0, 0, 1),
                             size_hint=(0.4, 0.1),
                             pos_hint={"x": 0.05, "y": 0.6})
        self.add_widget(self.L_label)
        self.L_ent = TextInput(multiline=False,
                               font_size=20,
                               size_hint=(0.4, 0.1),
                               pos_hint={"x": 0.55, "y": 0.6})
        self.add_widget(self.L_ent)

        # Cross-sectional Area (A)
        self.A_label = Label(text="Cross-sectional Area (A):",
                             font_size=20,
                             color=(1, 0, 0, 1),
                             size_hint=(0.4, 0.1),
                             pos_hint={"x": 0.05, "y": 0.45})
        self.add_widget(self.A_label)
        self.A_ent = TextInput(multiline=False,
                               font_size=20,
                               size_hint=(0.4, 0.1),
                               pos_hint={"x": 0.55, "y": 0.45})
        self.add_widget(self.A_ent)

        # Resistance (R)
        self.R_label = Label(text="Resistance (R):",
                             font_size=20,
                             color=(1, 0, 0, 1),
                             size_hint=(0.4, 0.1),
                             pos_hint={"x": 0.05, "y": 0.3})
        self.add_widget(self.R_label)
        self.R_ent = TextInput(multiline=False,
                               font_size=20,
                               size_hint=(0.4, 0.1),
                               pos_hint={"x": 0.55, "y": 0.3})
        self.add_widget(self.R_ent)

        # Formula display
        self.formula_label = Label(text="R = (ρ × L) ÷ A",
                                   font_size=18,
                                   color=(0, 0, 1, 1),  # blue
                                   size_hint=(0.9, 0.1),
                                   pos_hint={"x": 0.05, "y": 0.2})
        self.add_widget(self.formula_label)

        # Submit button
        self.sub_btn = Button(text="Calculate",
                              font_size=20,
                              background_color=(0.6, 1, 0.6, 1),  # light green
                              color=(0, 0, 0, 1),
                              size_hint=(0.4, 0.1),
                              pos_hint={"x": 0.3, "y": 0.1})
        self.sub_btn.bind(on_press=self.calculate)
        self.add_widget(self.sub_btn)

        # Result labels
        self.result_label = None
        self.detail_label = None

    def calculate(self, instance):
        sound_play()

        P = self.P_ent.text
        L = self.L_ent.text
        A = self.A_ent.text
        R = self.R_ent.text

        # Remove previous results
        if self.result_label:
            self.remove_widget(self.result_label)
        if self.detail_label:
            self.remove_widget(self.detail_label)

        try:
            if R == "" and L != "" and A != "" and P != "":
                result = (float(P) * float(L)) / float(A)
                self.show_result(f"Resistance (R): {result}",
                                 f"R = (ρ × L) ÷ A\nR = ({P} × {L}) ÷ {A} = {result}")
            elif R != "" and L != "" and A != "" and P == "":
                result = (float(A) * float(R)) / float(L)
                self.show_result(f"Resistivity (ρ): {result}",
                                 f"ρ = (A × R) ÷ L\nρ = ({A} × {R}) ÷ {L} = {result}")
            elif R != "" and L == "" and A != "" and P != "":
                result = (float(A) * float(R)) / float(P)
                self.show_result(f"Length (L): {result}",
                                 f"L = (A × R) ÷ ρ\nL = ({A} × {R}) ÷ {P} = {result}")
            elif R != "" and L != "" and A == "" and P != "":
                result = (float(P) * float(L)) / float(R)
                self.show_result(f"Cross-sectional Area (A): {result}",
                                 f"A = (ρ × L) ÷ R\nA = ({P} × {L}) ÷ {R} = {result}")
            else:
                self.show_error("Invalid or insufficient input!")

        except Exception as e:
            self.show_error(f"Calculation error: {e}")

    def show_result(self, ans_text, detail_text):
        self.result_label = Label(text=ans_text,
                                  font_size=20,
                                  color=(1, 0, 0, 1),  # red
                                  size_hint=(0.9, 0.1),
                                  pos_hint={"x": 0.05, "y": 0.0001})
        self.add_widget(self.result_label)

        self.detail_label = Label(text=detail_text,
                                  font_size=16,
                                  color=(0, 0, 0, 1),  # black
                                  size_hint=(0.9, 0.2),
                                  pos_hint={"x": 0.05, "y": 0.0001})
        self.add_widget(self.detail_label)

    def show_error(self, msg):
        popup = Popup(title="Error",
                      content=Label(text=msg, font_size=18),
                      size_hint=(0.8, 0.3),
                      auto_dismiss=True)
        popup.open()


class MVVApp(App):
    def build(self):
        return ResistivityLayout()


if __name__ == "__main__":
    MVVApp().run()
