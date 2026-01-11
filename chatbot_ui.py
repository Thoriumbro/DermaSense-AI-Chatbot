from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QLineEdit, QPushButton, QComboBox, 
                             QRadioButton, QButtonGroup, QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor, QTextCursor, QIcon, QPalette, QLinearGradient, QBrush
import json
import normalizer
import pdf
import DBsetup
import translator
from voice import initialize_engine, speak
import voice
import sys

class ChatBotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.state = {
            "mode": "text",
            "target_lang": "English",
            "engine": initialize_engine(),
            "user_details": {},
            "verified_symptoms": [],
            "current_state": "getting_details",
            "detail_prompts": [
                ("May I know your name?", "Name"),
                ("How old are you?", "Age"),
                ("What is your gender?", "Gender"),
                ("Lastly, can you please provide your phone number?", "Phone_number")
            ],
            "current_prompt": 0,
            "current_symptom_index": 0,
            "current_question_index": 0,
            "followup_responses": {},
            "content": None,
            "all_symptoms": None
        }
        
        self.init_ui()
        self.init_symptoms_data()
        self.show_welcome_message()
        
    def init_ui(self):
        self.setWindowTitle("DERMASENSE")
        self.setWindowIcon(QIcon("icon.png"))  # Replace with your icon
        self.setGeometry(100, 100, 900, 700)
        
        # Set application palette for colorful theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))  # AliceBlue background
        palette.setColor(QPalette.WindowText, QColor(25, 25, 112))  # MidnightBlue text
        palette.setColor(QPalette.Base, QColor(255, 255, 255))  # White for input areas
        palette.setColor(QPalette.AlternateBase, QColor(230, 230, 250))  # Lavender
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(25, 25, 112))
        palette.setColor(QPalette.Text, QColor(25, 25, 112))
        palette.setColor(QPalette.Button, QColor(100, 149, 237))  # CornflowerBlue
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # White
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(65, 105, 225))  # RoyalBlue
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)
        
        # Central widget with gradient background
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Header with gradient background
        header = QLabel("DERMASENSE")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4169E1, stop:0.5 #6A5ACD, stop:1 #9370DB);
                color: white;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #483D8B;
            }
        """)
        main_layout.addWidget(header)
        
        # Settings panel with colorful design
        settings_group = QGroupBox("Settings")
        settings_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #483D8B;
                border: 2px solid #9370DB;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background: #E6E6FA;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(20)
        
        # Mode selection
        mode_group = QGroupBox("Mode")
        mode_group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                color: #4B0082;
                border: 1px solid #9370DB;
                border-radius: 5px;
                background: #F8F8FF;
            }
        """)
        mode_layout = QVBoxLayout()
        self.text_mode = QRadioButton("Text")
        self.voice_mode = QRadioButton("Voice")
        self.text_mode.setChecked(True)
        
        # Style radio buttons
        radio_style = """
            QRadioButton {
                font-size: 13px;
                color: #4B0082;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
        """
        self.text_mode.setStyleSheet(radio_style)
        self.voice_mode.setStyleSheet(radio_style)
        
        mode_layout.addWidget(self.text_mode)
        mode_layout.addWidget(self.voice_mode)
        mode_group.setLayout(mode_layout)
        settings_layout.addWidget(mode_group)
        
        # Language selection
        lang_group = QGroupBox("Language")
        lang_group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                color: #4B0082;
                border: 1px solid #9370DB;
                border-radius: 5px;
                background: #F8F8FF;
            }
        """)
        lang_layout = QVBoxLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(translator.languages.keys())
        self.lang_combo.setCurrentText("English")
        
        # Style combo box
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background: white;
                border: 1px solid #9370DB;
                border-radius: 3px;
                padding: 3px;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)
        settings_layout.addWidget(lang_group)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        # Chat display with colorful design
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 12))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #F5F5FF;
                border: 2px solid #9370DB;
                border-radius: 8px;
                padding: 10px;
                color: #2F4F4F;
            }
        """)
        main_layout.addWidget(self.chat_display)
        
        # Input area with colorful design
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your message here...")
        self.user_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #9370DB;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                color: #2F4F4F;
            }
            QLineEdit:focus {
                border: 2px solid #4169E1;
            }
        """)
        self.user_input.returnPressed.connect(self.process_input)
        input_layout.addWidget(self.user_input, 4)  # 80% width
        
        # Colorful buttons
        button_style = """
            QPushButton {
                border-radius: 15px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid;
                min-width: 80px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #4169E1;
                color: white;
                border-color: #483D8B;
            }
            QPushButton:pressed {
                background-color: #483D8B;
            }
        """)
        self.send_btn.clicked.connect(self.process_input)
        input_layout.addWidget(self.send_btn, 1)  # 20% width
        
        self.voice_btn = QPushButton(QIcon("mic.png"), "")
        self.voice_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #32CD32;
                color: white;
                border-color: #228B22;
            }
            QPushButton:pressed {
                background-color: #228B22;
            }
        """)
        self.voice_btn.clicked.connect(self.voice_input)
        self.voice_btn.setVisible(False)
        input_layout.addWidget(self.voice_btn, 1)  # 20% width
        
        main_layout.addLayout(input_layout)
        
        # Connect signals
        self.text_mode.toggled.connect(self.update_mode)
        self.lang_combo.currentTextChanged.connect(self.update_language)
        
    def init_symptoms_data(self):
        try:
            with open("_newSymptoms.json") as file:
                self.state["content"] = json.load(file)
            self.state["all_symptoms"] = []
            for group in self.state["content"]["dermatology_symptoms"]:
                self.state["all_symptoms"].append([group["category"]])
                self.state["all_symptoms"].extend(group["symptoms"])
        except Exception as e:
            print(f"Error loading symptoms data: {e}")
            self.state["content"] = {"dermatology_symptoms": []}
            self.state["all_symptoms"] = []
    
    def show_welcome_message(self):
        self.display_message("bot", "Welcome to the dermatological healthcare chatbot!")
        self.prompt_next_detail()
    
    def update_mode(self, checked):
        if self.text_mode.isChecked():
            self.state["mode"] = "text"
            self.voice_btn.setVisible(False)
            self.send_btn.setVisible(True)
        else:
            self.state["mode"] = "voice"
            self.voice_btn.setVisible(True)
            self.send_btn.setVisible(False)
    
    def update_language(self, language):
        self.state["target_lang"] = language
    
    def display_message(self, sender, message):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        prefix = "Bot: " if sender == "bot" else "You: "
        color = "#2c3e50" if sender == "bot" else "#3498db"
        
        # Format prefix
        cursor.insertText(prefix)
        fmt = cursor.charFormat()
        fmt.setFontWeight(QFont.Bold)
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        
        # Format message
        cursor.insertText(message + "\n")
        fmt.setFontWeight(QFont.Normal)
        cursor.setCharFormat(fmt)
        
        # Scroll to bottom
        self.chat_display.ensureCursorVisible()
        
        # Speak if bot message and voice mode
        if sender == "bot" and self.state["mode"] == "voice":
            speak(self.state["engine"], message, self.state["target_lang"])
    
    def process_input(self):
        user_text = self.user_input.text()
        if not user_text:
            return
            
        self.display_message("user", user_text)
        self.user_input.clear()
        
        processed_text = self.translate_to_english(user_text)
        if processed_text != user_text and self.state["target_lang"].lower() != "english":
            pass
        if self.state["current_state"] == "getting_details":
            self.handle_user_details(processed_text)
        elif self.state["current_state"] == "getting_symptoms":
            self.handle_symptoms(processed_text)
        elif self.state["current_state"] == "followup_questions":
            self.handle_followup(processed_text)
    
    def voice_input(self):
        self.voice_btn.setEnabled(False)
        self.display_message("bot", "Listening...")
        
        # Use QThread to prevent UI freezing
        self.voice_thread = VoiceThread(self.state["target_lang"])
        self.voice_thread.finished.connect(self.handle_voice_result)
        self.voice_thread.start()
    
    def handle_voice_result(self, result):
        self.voice_btn.setEnabled(True)
        if result:
            self.user_input.setText(result)
            self.process_input()
        else:
            error_msg = translator.translate("Sorry, I didn't catch that. Please try again.", self.state["target_lang"])
            self.display_message("bot", error_msg)
    
    def translate_to_english(self, text):
        if self.state["target_lang"].lower() == "english":
            return text
        try:
            return translator.translate(text, "English", self.state["target_lang"])
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def handle_user_details(self, response):
        try:
            current_prompt, key = self.state["detail_prompts"][self.state["current_prompt"]]
            
            if key == "Name":
                if not response.strip():
                    error_msg = translator.translate("Name is mandatory. Please enter your name.", self.state["target_lang"])
                    self.display_message("bot", error_msg)
                    return
                    
                if not response.replace(" ", "").isalpha():
                    error_msg = translator.translate("Please enter a valid name (letters only, no numbers or special characters).", self.state["target_lang"])
                    self.display_message("bot", error_msg)
                    return
                    
                self.state["user_details"][key] = response.title()
                
            elif key == "Age":
                try:
                    age = int(response)
                    if not (0 < age < 120):
                        raise ValueError("Age out of reasonable range")
                    self.state["user_details"][key] = str(age)
                except ValueError:
                    error_msg = translator.translate("Please enter a valid age between 1 and 120.", self.state["target_lang"])
                    self.display_message("bot", error_msg)
                    return
                
            elif key == "Gender":
                normalized_gender = response.strip().lower()
                valid_genders = ['male', 'female', 'm', 'f', 'man', 'woman', 'boy', 'girl', 'other']
                
                if normalized_gender not in valid_genders:
                    error_msg = translator.translate("Please specify your gender (male/female/other).", self.state["target_lang"])
                    self.display_message("bot", error_msg)
                    return
                    
                if normalized_gender in ['male', 'm', 'man', 'boy']:
                    self.state["user_details"][key] = "Male"
                elif normalized_gender in ['female', 'f', 'woman', 'girl']:
                    self.state["user_details"][key] = "Female"
                else:
                    self.state["user_details"][key] = "Other"
                    
            elif key == "Phone_number":
                if not response.strip():
                    error_msg = translator.translate("Phone number cannot be empty.", self.state["target_lang"])
                    self.display_message("bot", error_msg)
                    return
                self.state["user_details"][key] = response
                
            self.state["current_prompt"] += 1
            
            if self.state["current_prompt"] < len(self.state["detail_prompts"]):
                self.prompt_next_detail()
            else:
                self.state["current_state"] = "getting_symptoms"
                assistance_prompt = translator.translate(
                    "Now, how may I assist you with your dermatological concerns today?", 
                    self.state["target_lang"]
                )
                self.display_message("bot", assistance_prompt)
                
        except Exception as e:
            self.display_message("bot", "Error collecting details. Please restart the conversation.")
            print(f"Error handling user details: {e}")
            self.reset_conversation()
    
    def prompt_next_detail(self):
        try:
            prompt, key = self.state["detail_prompts"][self.state["current_prompt"]]
            
            if key == "Name":
                prompt += " (letters only, no numbers)"
            elif key == "Age":
                prompt += ""
            elif key == "Gender":
                prompt += " (male female other)"
            elif key == "Phone_number":
                prompt += ""
                
            translated_prompt = translator.translate(prompt, self.state["target_lang"])
            self.display_message("bot", translated_prompt)
            
        except IndexError:
            self.display_message("bot", "Error: Conversation flow interrupted. Please restart the chat.")
            self.reset_conversation()
        except Exception as e:
            self.display_message("bot", "Error: Could not prompt for details. Please try again.")
            print(f"Error prompting for details: {e}")
    
    def handle_symptoms(self, user_input):
        try:
            possible_symptoms = normalizer.text_normalizer(user_input)
            self.state["verified_symptoms"] = self.verify_symptoms(possible_symptoms, self.state["all_symptoms"])
            
            if not self.state["verified_symptoms"]:
                error_msg = translator.translate("No symptoms detected. Please try rephrasing your input or providing more details.", self.state["target_lang"])
                self.display_message("bot", error_msg)
                return
                
            self.display_symptoms_list()
            self.prepare_followup_questions()
        except Exception as e:
            self.display_message("bot", "Error processing symptoms. Please try again.")
            print(f"Error handling symptoms: {e}")
    
    def verify_symptoms(self, possibleSymptoms, all_symptoms):
        verified = []
        current_category = all_symptoms[0][0]
        for symptom in all_symptoms:
            if isinstance(symptom, list):
                current_category = symptom
            if symptom in possibleSymptoms:
                verified.append([current_category, symptom])
        return verified
    
    def display_symptoms_list(self):
        try:
            symptoms_list = translator.translate("The identified symptoms are:", self.state["target_lang"])
            self.display_message("bot", symptoms_list)
            
            for symptom in self.state["verified_symptoms"]:
                self.display_message("bot", f"- {translator.translate(symptom[1], self.state['target_lang'])}")
        except Exception as e:
            self.display_message("bot", "Error displaying symptoms. Continuing with conversation...")
            print(f"Error displaying symptoms list: {e}")
    
    def prepare_followup_questions(self):
        self.state["current_state"] = "followup_questions"
        self.state["current_symptom_index"] = 0
        self.state["current_question_index"] = 0
        self.state["followup_responses"] = {}
        self.ask_next_followup()
    
    def ask_next_followup(self):
        try:
            if self.state["current_symptom_index"] >= len(self.state["verified_symptoms"]):
                self.finish_conversation()
                return
                
            symptom = self.state["verified_symptoms"][self.state["current_symptom_index"]]
            category = symptom[0][0]
            
            for cat in self.state["content"]["dermatology_symptoms"]:
                if cat["category"] == category:
                    questions = cat["followup_questions"]
                    if self.state["current_question_index"] < len(questions):
                        self.ask_question(questions[self.state["current_question_index"]])
                        return
                    
            self.store_followup_responses()
        except Exception as e:
            self.display_message("bot", "Error: Could not proceed with questions. Restarting conversation.")
            print(f"Error in followup sequence: {e}")
            self.reset_conversation()
    
    def ask_question(self, question):
        try:
            translated = translator.translate(question, self.state["target_lang"])
            self.display_message("bot", translated)
        except Exception as e:
            self.display_message("bot", "Error: Could not ask the question. Please try again.")
            print(f"Error asking question: {e}")
    
    def store_followup_responses(self):
        try:
            self.state["verified_symptoms"][self.state["current_symptom_index"]].append(self.state["followup_responses"])
            self.state["followup_responses"] = {}
            self.state["current_symptom_index"] += 1
            self.state["current_question_index"] = 0
            self.ask_next_followup()
        except Exception as e:
            self.display_message("bot", "Error storing responses. Continuing with next question...")
            print(f"Error storing followup responses: {e}")
            self.state["current_symptom_index"] += 1
            self.ask_next_followup()
    
    def handle_followup(self, response):
        try:
            symptom = self.state["verified_symptoms"][self.state["current_symptom_index"]]
            category = symptom[0][0]
            
            for cat in self.state["content"]["dermatology_symptoms"]:
                if cat["category"] == category:
                    question = cat["followup_questions"][self.state["current_question_index"]]
                    self.state["followup_responses"][question] = response
                    
                    try:
                        self.provide_feedback(response)
                    except Exception as e:
                        self.display_message("bot", "Thank you for your response.")
                        print(f"Error providing feedback: {e}")
                    
                    self.state["current_question_index"] += 1
                    self.ask_next_followup()
                    return
        except IndexError:
            self.display_message("bot", "Error: Question sequence interrupted. Restarting conversation.")
            self.reset_conversation()
        except Exception as e:
            self.display_message("bot", "An error occurred. Please try again.")
            print(f"Error handling followup: {e}")
    
    def provide_feedback(self, response):
        try:
            replies = [
                "Thank you for sharing this detail. It helps me understand your situation better.",
                "Got it! This information is valuable for assessing your symptoms.",
                "Thanks for letting me know. It's important to track these things carefully."
            ]
            
            if self.state["current_question_index"] == 0 and response:
                reply = translator.translate(
                    f"We're sorry to hear that you have been experiencing it for {response}. Please know that you're not alone.", 
                    self.state["target_lang"]
                )
            elif response:
                reply = translator.translate(replies[self.state["current_question_index"] % len(replies)], self.state["target_lang"])
            else:
                reply = translator.translate(
                    "Thank you for your response. If you'd like to elaborate further, let me know.", 
                    self.state["target_lang"]
                )
            
            self.display_message("bot", reply)
        except Exception as e:
            self.display_message("bot", "Thank you for your response.")
            print(f"Error generating feedback: {e}")
    
    def finish_conversation(self):
        try:
            closing_message = translator.translate(
                "Your information has been recorded and a PDF has been generated. Have a great day!", 
                self.state["target_lang"]
            )
            self.display_message("bot", closing_message)
            self.generate_outputs()
        except Exception as e:
            self.display_message("bot", "Conversation completed. Thank you!")
            print(f"Error finishing conversation: {e}")
        finally:
            self.reset_conversation()
    
    def generate_outputs(self):
        try:
            pdf.final_report(self.state["user_details"], self.state["verified_symptoms"])
            DBsetup.setup_database(self.state["user_details"], self.state["verified_symptoms"])
        except Exception as e:
            self.display_message("bot", "Error generating report. Please contact support.")
            print(f"Error generating outputs: {e}")
    
    def reset_conversation(self):
        self.state["current_state"] = "getting_details"
        self.state["current_prompt"] = 0
        self.state["user_details"] = {}
        self.state["verified_symptoms"] = []
        self.state["current_symptom_index"] = 0
        self.state["current_question_index"] = 0
        self.state["followup_responses"] = {}


class VoiceThread(QThread):
    finished = pyqtSignal(str)
    
    def __init__(self, target_lang):
        super().__init__()
        self.target_lang = target_lang
    
    def run(self):
        heard_text = voice.listen(self.target_lang)
        self.finished.emit(heard_text if heard_text else "")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")
    
    window = ChatBotUI()
    window.show()
    
    sys.exit(app.exec_())