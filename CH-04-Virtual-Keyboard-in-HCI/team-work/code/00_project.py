from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard

class KeyboardDemo(BoxLayout):
    """
    A simple widget that displays a TextInput and a permanent virtual keyboard.
    The keyboard events are manually handled to update the text input.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Arrange widgets vertically (TextInput on top, keyboard below)
        self.orientation = "vertical"

        # ----- TextInput setup -----
        self.text_input = TextInput(
            multiline=False,          # Only one line of text
            font_size=24,             # Larger font for readability
            size_hint=(1, 0.2),       # Takes 20% of the parent height
            hint_text="Click here, then use the virtual keyboard"
        )
        self.add_widget(self.text_input)

        # ----- Virtual keyboard -----
        # VKeyboard is a Kivy widget that displays an on-screen keyboard.
        # We bind its 'on_key_up' event to our custom method key_released.
        self.keyboard = VKeyboard(on_key_up=self.key_released)
        self.add_widget(self.keyboard)

    def key_released(self, keyboard, keycode, *args):
        """
        Callback for VKeyboard's 'on_key_up' event.
        :param keyboard: The VKeyboard instance that emitted the event.
        :param keycode: A tuple (scancode, symbol) e.g., (97, 'a').
        :param args: Additional arguments (not used here).
        """
        # Extract the actual key symbol from the tuple
        # For example: (97, 'a') -> 'a'
        key = keycode[1] if isinstance(keycode, tuple) else keycode
        print("Key pressed:", key)   # Debug output

        # Handle special keys that are not single characters
        if key == 'backspace':
            # Remove the last character from the text input
            self.text_input.text = self.text_input.text[:-1]
        elif key == 'spacebar':
            # Append a space character
            self.text_input.text += ' '
        # For any other single-character key (e.g., 'a', 'b', '1', etc.)
        elif len(key) == 1:
            self.text_input.text += key
        # Note: Keys like 'enter', 'shift', 'capslock', etc. are ignored here.
        # For a more complete implementation you would handle them appropriately.

class KeyboardApp(App):
    """
    The Kivy application class. It simply builds and returns the KeyboardDemo widget.
    """
    def build(self):
        return KeyboardDemo()

if __name__ == "__main__":
    KeyboardApp().run()