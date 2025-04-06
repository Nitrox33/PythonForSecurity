# encoding: utf-8
# inport the necessary libraries (for the UI)
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QTextEdit, QFileDialog, QMessageBox,
    QTabWidget, QMenuBar
)
from PyQt6.QtGui import QIcon # for the icon (if needed)

# import the necessary libraries (for the encryption)
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import random
from Crypto.Util.Padding import pad, unpad

# import the necessary libraries (for the file handling)    
import sys
import os

def int_to_bytes(i:int, size:int=1):
    return i.to_bytes(size, "big")

class EncryptionApp(QWidget):
    """Data Encryption Application using AES
    This application allows users to encrypt and decrypt files using AES encryption.
    
    things to work on:
    - add more encryption methods (DES, 3DES, etc.)
    - add a light/dark mode
    - add a way to change the key size (128, 192, 256 bits)
    - add a way to encrypt multiple files at once / folder (compression)
    - add a way to have how keys (maybe a image.jpg can be a key ? if hashing is used)
    """
    def __init__(self):
        super().__init__()
        
        # creating cipghering method table
        self.ciphers_names = {
            AES.MODE_ECB: "ECB",
            AES.MODE_CBC: "CBC"
        }
        
        # choosing the default ciphering method
        self.ciphering_method = AES.MODE_CBC
        
        # initializing the UI components
        self.init_menu()
        self.init_ui()
        self.init_action()
        
    def change_cipher(self, cipher:int):
        """Change the ciphering method used for encryption/decryption."""
        self.ciphering_method = cipher
    
        self.encrypt_button.setText(f"Encrypt using {self.ciphers_names[self.ciphering_method]}") # update button text
        self.decrypt_button.setText(f"Decrypt using {self.ciphers_names[self.ciphering_method]}") # update button text

    def init_ui(self):
        """Initialize the user interface components."""
        self.setWindowTitle("File Encryption Tool")
        
        # Input fields
        self.input_file_label = QLabel("Name of input file:")
        self.input_file_edit = QLineEdit()
        self.input_file_button = QPushButton("Browse")
        self.input_file_button.clicked.connect(lambda: self.browse_file(self.input_file_edit))
        self.input_file_verification = QLabel("")
        
        # output field
        self.output_file_label = QLabel("Name of output file:")
        self.output_file_edit = QLineEdit()
        self.output_file_button = QPushButton("Browse")
        self.output_file_button.clicked.connect(lambda: self.browse_file(self.output_file_edit))
        self.output_file_verification = QLabel("")
        
        # key file
        self.key_file_label = QLabel("Name of key file:")
        self.key_file_edit = QLineEdit()
        self.key_file_button = QPushButton("Browse")
        self.key_file_button.clicked.connect(lambda: self.browse_file(self.key_file_edit))
        self.key_file_verification = QLabel("")

        # key text
        self.key_txt_label = QLabel("Key value :")
        self.key_txt_edit = QLineEdit()
        self.key_txt_button = QPushButton("Randomize")
        self.key_txt_verification = QLabel("")

        # Buttons
        self.encrypt_button = QPushButton(f"Encrypt using {self.ciphers_names[self.ciphering_method]}")
        self.decrypt_button = QPushButton(f"Encrypt using {self.ciphers_names[self.ciphering_method]}")
        
        # Hex content display
        self.input_content = QTextEdit("Content of input file in hex")
        self.output_content = QTextEdit("Content of output file in hex")
        self.input_content.setReadOnly(True)
        self.output_content.setReadOnly(True)
        
        # Layout setup
        
        # the file layout is the top and middle layout
        file_layout = QVBoxLayout()

        # the top layout deals with the input file button and edit field
        top_layout = QHBoxLayout()
        file_layout.addWidget(self.input_file_label)
        top_layout.addWidget(self.input_file_edit)
        top_layout.addWidget(self.input_file_button)
        file_layout.addLayout(top_layout)
        file_layout.addWidget(self.input_file_verification)

        # the middle layout deals with the output file button and edit field
        middle_layout = QHBoxLayout()
        file_layout.addWidget(self.output_file_label)
        middle_layout.addWidget(self.output_file_edit)
        middle_layout.addWidget(self.output_file_button)
        file_layout.addLayout(middle_layout)
        file_layout.addWidget(self.output_file_verification)

        # the bottom layout deals with the key file and text key
        # the bottom layout is a tab widget with 2 tabs, one for the key file and one for the text key
        self.bot_tab_widget = QTabWidget()
        bot_file_button_layout = QHBoxLayout()
        bot_key_button_layout = QHBoxLayout()
        bot_file_layout = QVBoxLayout()

        # the first tab is for the key file
        bot_file_layout.addWidget(self.key_file_label)
        bot_file_button_layout.addWidget(self.key_file_edit)
        bot_file_button_layout.addWidget(self.key_file_button)
        bot_file_layout.addLayout(bot_file_button_layout)
        bot_file_layout.addWidget(self.key_file_verification)

        ## the second tab is for the text key
        bot_txt_key_layout = QVBoxLayout()
        bot_txt_key_layout.addWidget(self.key_txt_label)
        bot_key_button_layout.addWidget(self.key_txt_edit)
        bot_key_button_layout.addWidget(self.key_txt_button)
        bot_txt_key_layout.addLayout(bot_key_button_layout)
        bot_txt_key_layout.addWidget(self.key_txt_verification)
    
        # add the 2 tabs to the tab widget
        bot_file_key_widget = QWidget()
        bot_txtkey_widget = QWidget()
        bot_file_key_widget.setLayout(bot_file_layout)
        bot_txtkey_widget.setLayout(bot_txt_key_layout)
        self.bot_tab_widget.addTab(bot_file_key_widget, "Key file")
        self.bot_tab_widget.addTab(bot_txtkey_widget, "Text key")

        # add the tab widget to the file layout
        file_layout.addWidget(self.bot_tab_widget)
        
        # create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.encrypt_button)
        button_layout.addWidget(self.decrypt_button)
        
        # create the text layout
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.input_content)
        text_layout.addWidget(self.output_content)
        
        # create the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.menu_bar)
        main_layout.addLayout(file_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(text_layout)
        
        # set the main layout to the window
        self.setLayout(main_layout)

    def init_action(self):
        """Initialize actions for buttons and input fields."""
        # connect the buttons and text inputs to their actions
        self.input_file_edit.textChanged.connect(lambda text: self.check_file(text, self.input_file_verification))
        self.output_file_edit.textChanged.connect(lambda text: self.check_file(text, self.output_file_verification, True))
        self.key_file_edit.textChanged.connect(lambda text: self.check_file(text, self.key_file_verification, False, True))
        self.key_txt_edit.textChanged.connect(lambda text: self.check_file(text, self.key_txt_verification, False, False, True))
        self.key_txt_button.clicked.connect(self.randomize_key)
        
        # connect the buttons to their actions (encrypt and decrypt)
        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.decrypt_button.clicked.connect(self.decrypt_file)

    def init_menu(self):
        """Initialize the menu bar and its items."""
        self.menu_bar = QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("File")
        self.edit_menu = self.menu_bar.addMenu("Edit")
        self.encryption_menu = self.menu_bar.addMenu("Encryption")
        self.encryption_menu.addAction("set AES CBC", lambda : self.change_cipher(AES.MODE_CBC))
        self.encryption_menu.addAction("set AES ECB", lambda : self.change_cipher(AES.MODE_ECB))

        self.help_menu = self.menu_bar.addMenu("Help")
        
    def randomize_key(self) -> None:
        """
        This method generates a random key of 32 bytes and sets it in the key text edit field.
        The key is generated using random ASCII printable characters, excluding certain characters to avoid issues with quotes and slashes.
        """
        output = bytes()
        while len(output) < 32:
            r = random.randint(33, 126) # ASCII printable characters
            if r in [34, 39, 47, 92]: continue
            else: output += bytes([r])
        self.key_txt_edit.setText(output.decode('ascii'))

    def browse_file(self, line_edit:QLineEdit) -> None:
        """Open a file dialog to select a file and set the selected file path in the line edit."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            line_edit.setText(file_path)

    def encrypt_file(self) -> None:
        self.clear_input() # clear previous error messages
        
        # Get input values
        input_file = self.input_file_edit.text()
        output_file = self.output_file_edit.text()

        key_index = self.bot_tab_widget.currentIndex() # we have 2 tabs, key file and text key
        
        key_file = self.key_file_edit.text()
        key_txt = self.key_txt_edit.text()

        # Check if input file exists
        if not os.path.exists(input_file): # input file
            self.input_file_verification.setText("Error : Input file does not exist")
            self.input_file_verification.setStyleSheet("color: red")
            return
        else:
            with open(input_file, "rb") as f:
                original_data = f.read()
        
        # checking key file or text key
        if key_index == 0: # Key file
            if key_file == "":
                self.key_file_verification.setText("Error : Key file name is empty, add a name")
                self.key_file_verification.setStyleSheet("color: red")
                return
            elif not os.path.exists(key_file):
                key = get_random_bytes(32)
                with open(key_file, "wb") as f:
                    f.write(key)
            else:
                with open(key_file, "rb") as f:
                    key = f.read()
        elif key_index == 1: # Text key
            if key_txt == "":
                self.key_txt_verification.setText("Error : Key value is empty, add a value")
                self.key_txt_verification.setStyleSheet("color: red")
                return
            elif len(key_txt) > 32:
                self.key_txt_verification.setText("Error : Key value is too long, must be 32 bytes max")
                self.key_txt_verification.setStyleSheet("color: red")
                return
            else:
                key = key_txt.encode() # convert to bytes
                if len(key) < 32: # if the key is less than 32 bytes, pad it, otherwise no need to pad
                    key = pad(key, 32)
        
        # perform encryption
        iv = get_random_bytes(16) # the iv is generated anyway because we always have IV = [:16] ; data = [16:]
        if self.ciphering_method == AES.MODE_ECB:
            cipher = AES.new(key, self.ciphering_method)
        else:
            cipher = AES.new(key, self.ciphering_method, iv)
            
        ciphertext = cipher.encrypt(pad(original_data, AES.block_size)) #
        
        # output the data in hex format
        if len(original_data) > 500:
            self.input_content.setPlainText(original_data.hex()[:500])
            self.output_content.setPlainText(ciphertext.hex()[:500])
        else:
            self.input_content.setPlainText(original_data.hex())
            self.output_content.setPlainText(ciphertext.hex())

        # check if output file exists
        if output_file == "":
            self.output_file_verification.setText("Error : Output file name is empty, add a name")
            self.output_file_verification.setStyleSheet("color: red")
            return
        
        # putting at the beginning of the file the method used for encryption
        method = int_to_bytes(self.ciphering_method, size=1) # 1 => ECB # 2 => CBC 
    
        with open(output_file, "wb") as f:
            f.write(method + iv + ciphertext)
        
        self.popup("Encryption completed successfully!")
        return
    
    def decrypt_file(self) -> None:
        self.clear_input() # clear previous error messages
        
        # Get input values
        input_file = self.input_file_edit.text()
        output_file = self.output_file_edit.text()
        key_file = self.key_file_edit.text()
        key_txt = self.key_txt_edit.text()
    
        key_index = self.bot_tab_widget.currentIndex() # we have 2 tabs, key file and text key
        
        # Check if input file exists
        if not os.path.exists(input_file):
            self.input_file_verification.setText("Error : Input file does not exist")
            self.input_file_verification.setStyleSheet("color: red")
            return
        else:
            with open(input_file, "rb") as f:
                original_data = f.read()
                if len(original_data) <= 16: # if less that 16 bytes, not encrypted by us
                    self.input_file_verification.setText("Error Decrypting, are you sure about the input ?")
                    self.input_file_verification.setStyleSheet("color: red")
                    return
                
                method = original_data[0] # the first byte is the method used for encryption
                
                # check if the method is valid
                if method != self.ciphering_method:
                    self.input_file_verification.setText("encryption modes are not matching, changing modes...")
                    self.input_file_verification.setStyleSheet("color: orange")
                    if method in self.ciphers_names:
                        self.change_cipher(method) # change the ciphering method to the one used for encryption
                    else: return
                original_data = original_data[1:] # remove the first byte
                
                iv = original_data[:16] # the first 16 bytes are the IV (even if we use ECB, we need to remove it)
                original_data = original_data[16:] # get the rest of the data
        
        # checking key file or text key
        if key_index == 0: # Key file
            if key_file == "":
                self.key_file_verification.setText("Error : Key file name is empty")
                self.key_file_verification.setStyleSheet("color: red")
                return
            if not os.path.exists(key_file):
                self.key_file_verification.setText("Error : Key file does not exist")
                self.key_file_verification.setStyleSheet("color: red")
                return
            else:
                with open(key_file, "rb") as f:
                    key = f.read()
        elif key_index == 1: # Text key
            if key_txt == "":
                self.key_txt_verification.setText("Error : Key value is empty")
                self.key_txt_verification.setStyleSheet("color: red")
                return
            elif len(key_txt) > 32:
                self.key_txt_verification.setText("Error : Key value is too long, must be 32 bytes max")
                self.key_txt_verification.setStyleSheet("color: red")
                return
            else:
                key = key_txt.encode()
                if len(key) < 32:
                    key = pad(key, 32)
    
        # perform decryption
        try: # try to decrypt the file
            if self.ciphering_method == AES.MODE_ECB:
                cipher = AES.new(key, self.ciphering_method)
            else:
                cipher = AES.new(key, self.ciphering_method, iv)
                
            cleartext = cipher.decrypt(original_data)
            cleartext = unpad(cleartext, AES.block_size)
        except: # if the decryption fails, it means the key is wrong or the input file is not encrypted by us
            self.input_file_verification.setText("Error decrypting, wrong input or key")
            self.input_file_verification.setStyleSheet("color: red")
            return
        
        # output the data in hex format
        if len(original_data) > 500:
            self.input_content.setPlainText(original_data.hex()[:500])
            self.output_content.setPlainText(cleartext.hex()[:500])
        else:
            self.input_content.setPlainText(original_data.hex())
            self.output_content.setPlainText(cleartext.hex())

        if output_file == "":
            self.output_file_verification.setText("Decryption successful but no output file provided")
            self.output_file_verification.setStyleSheet("color: orange")
            return

        # writing the decrypted data to the output file
        with open(output_file, "wb") as f:
            f.write(cleartext)
        
        self.popup("Decryption completed successfully!")
        self.clear_input()
        return

    def check_file(self, file_path:str, verification_label:QLabel, is_output:bool=False, is_key_file:bool=False, is_key_txt:bool=False) -> None:
        """method to check if the file exists and update the verification label accordingly."""
        if is_key_txt: # key condition, no need to check if file exists
            if file_path == "": # key file name is empty
                verification_label.setText("Key file name is empty, add a name")
                verification_label.setStyleSheet("color: red")
                return
            else:
                if len(file_path) > 32: # key file name is too long
                    verification_label.setText("Key is too long, must be 32 bytes max")
                    verification_label.setStyleSheet("color: red")
                    return
                else:
                    verification_label.setText("Key is valid")
                    verification_label.setStyleSheet("color: green")
                    return

        if file_path == "" and is_output: # clear the output file name if empty
            verification_label.setText("")
            return
        
        if not os.path.exists(file_path): # file does not exist
            if is_output:
                verification_label.setText("Output file does not exist, will be created")
                verification_label.setStyleSheet("color: orange")
            elif is_key_file:
                verification_label.setText("Key file does not exist, will be created")
                verification_label.setStyleSheet("color: orange")
            else:
                verification_label.setText("File does not exist")
                verification_label.setStyleSheet("color: red")
            return
        else: # file exists
            if is_output:
                verification_label.setText("Output file exists, will be overwritten")
                verification_label.setStyleSheet("color: orange")
            elif is_key_file:
                verification_label.setText("Key file exists, will be used")
                verification_label.setStyleSheet("color: green")
            else:
                verification_label.setText("File exists")
                verification_label.setStyleSheet("color: green")
            return
    
    def popup(self, message:str) -> None:
        """display a popup message."""
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def clear_input(self) -> None:
        """clear the input fields and verification labels."""
        self.input_file_verification.clear()
        self.output_file_verification.clear()
        self.key_file_verification.clear()
        self.key_txt_verification.clear()
        
        

# COLOR THEME ##264653 #4D55CC #7A73D1 #B5A8D5 #F1F6F9

# real color theme : #E1E1E1

if __name__ == "__main__":
    # Create the application and set the style sheet
    app = QApplication(sys.argv)
    
    # set the style sheet for the application (this is very close to css)
    app.setStyleSheet("""
    QMenuBar {
        font-size: 16px;
        color: #E1E1E1;
    }
    QMenuBar::item {
        background-color: #2D2D2D;
        font-size: 16px;
        color: #E1E1E1;
        border: 1px solid #2D2D2D;
        border-radius: 5px;
        padding: 5px;
        margin: 2px;
    }              
    QMenuBar::item:selected {
        background-color: #4D55CC;
        color: #E1E1E1;
    }
    QMenu {
        background-color: #2D2D2D;
        border: 1px solid #2D2D2D;
        border-radius: 6px;
        
    }
    QMenu::item {
        background-color: #2D2D2D;
        color: #E1E1E1;
        padding: 5px;
        margin: 3px;
        border-radius: 5px;
    }
    QMenu::item:selected {
        background-color: #4D55CC;
        color: #E1E1E1;
        padding: 5px;
        margin: 2px;
        border-radius: 5px;
    }
    QWidget {
        font-size: 16px;
    }
    QPushButton {
        font-size: 18px;
    }
    QPushButton:hover {
        border: -1px solid #E1E1E1;
        background-color: #4D55CC;
        border-radius: 7px;

    }
    QLabel {
        font-size: 18px;
    }
    QLineEdit {
        font-size: 16px;
    }
    QTextEdit {
        font-size: 16px;
    }
    QTabWidget {
        font-size: 16px;
        background-color: #1E1E1E;
    }           
    QTabBar::tab {
        padding: 7px;

        border-radius: 5px;
        border: 2px solid #2D2D2D;
    }
    QTabBar::tab:hover {
        background-color: #4D55CC;
        border: -1px solid #E1E1E1;
    }
    QTabBar::tab:selected {
        background-color: #1E1E1E;
        border: 1px solid #E1E1E1;
        border-radius: 5px;
    }
    QTabBar::tab:selected:hover {
        background-color: #4D55CC;
        border: 1px solid #E1E1E1;
        border-radius: 5px;
    }                        
    """)
    window = EncryptionApp()
    window.show()
    sys.exit(app.exec())
