from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard

class KeyboardDemo(BoxLayout):
    """
    A widget with a permanent virtual keyboard that updates a TextInput.
    Now supports Caps Lock to type uppercase letters.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Track whether Caps Lock is active
        self.caps_lock_active = False

        # ----- TextInput setup -----
        self.text_input = TextInput(
            multiline=False,
            font_size=24,
            size_hint=(1, 0.2),
            hint_text="Click here, then use the virtual keyboard"
        )
        self.add_widget(self.text_input)

        # ----- Virtual keyboard -----
        # Bind the on_key_up event to our custom method
        self.keyboard = VKeyboard(on_key_up=self.key_released)
        self.add_widget(self.keyboard)

    def key_released(self, keyboard, keycode, *args):
        """
        Handle key releases from the virtual keyboard.
        :param keyboard: The VKeyboard instance
        :param keycode: Tuple (scancode, symbol) e.g., (97, 'a')
        """
        # Extract the actual key symbol (e.g., 'a', 'backspace', 'capslock')
        key = keycode[1] if isinstance(keycode, tuple) else keycode
        print("Key pressed:", key)

        # ----- Special keys -----
        if key == 'backspace':
            # Remove last character
            self.text_input.text = self.text_input.text[:-1]

        elif key == 'spacebar':
            self.text_input.text += ' '

        elif key == 'capslock':
            # Toggle Caps Lock state
            self.caps_lock_active = not self.caps_lock_active
            print(f"Caps Lock {'ON' if self.caps_lock_active else 'OFF'}")

        # ----- Regular characters (a-z, 0-9, etc.) -----
        # A single-character key that is not a special key we handled above
        elif len(key) == 1:
            # Apply Caps Lock if active
            char = key.upper() if self.caps_lock_active else key
            self.text_input.text += char

        # Note: This implementation ignores Shift, Ctrl, Alt, and other modifiers.
        # For a more complete keyboard, you would also track Shift and handle
        # uppercase/lowercase accordingly.

class KeyboardApp(App):
    """
    Kivy application that displays the KeyboardDemo widget.
    """
    def build(self):
        return KeyboardDemo()

if __name__ == "__main__":
    KeyboardApp().run()