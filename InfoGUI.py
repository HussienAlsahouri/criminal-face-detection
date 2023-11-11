import sys
import json
import os
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QToolButton, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QTextBrowser, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import datetime

class Ui_Form5(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1400, 900)

        # Create a horizontal layout for the top bar
        top_bar_layout = QtWidgets.QHBoxLayout()

        # Create a search bar widget and add it to the top bar layout (on the left side)
        self.search_bar = QLineEdit(Form)
        self.search_bar.setObjectName("search_bar")
        self.search_bar.setPlaceholderText("Search for names")

        # Create the search button but initially disable it
        self.search_button = QPushButton("Search", Form)
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.search_names)
        self.search_button.setEnabled(False)  # Initially disabled

        # Connect the textChanged signal of the search bar to enable/disable the search button
        self.search_bar.textChanged.connect(self.toggle_search_button)

        top_bar_layout.addWidget(self.search_bar)
        top_bar_layout.addWidget(self.search_button)

        # Create the scroll area and its contents
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(10, 50, 1381, 831))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1300, 831))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        

        # Load data from a JSON file (replace 'data.json' with your file)
        with open('registration_data.json', 'r') as json_file:
            data = json.load(json_file)

        self.buttons = {}

        for person in data:
            # Check if the folder exists in the "matches" directory
            folder_name = person['Full Name']
            folder_path = os.path.join('matches', folder_name)
            has_folder = os.path.exists(folder_path)

            person_layout = QtWidgets.QHBoxLayout()
            person_layout.setObjectName(f"layout_{person['Full Name']}")

            image_label = QtWidgets.QLabel()
            image_label.setMinimumSize(QtCore.QSize(250, 300))
            image_label.setMaximumSize(QtCore.QSize(250, 300))
            image_label.setAlignment(QtCore.Qt.AlignCenter)
            image_label.setObjectName(f"label_{person['Full Name']}")

            pixmap = QtGui.QPixmap(person['Image Path'])
            pixmap = pixmap.scaledToWidth(320)
            image_label.setPixmap(pixmap)

            info_container = QtWidgets.QWidget()
            info_container.setObjectName(f"info_container_{person['Full Name']}")
            info_container.setStyleSheet("background: white;")

            info_text = QtWidgets.QTextBrowser(info_container)
            info_text.setAlignment(QtCore.Qt.AlignCenter)
            info_text.setObjectName(f"info_{person['Full Name']}")
            info_text.setPlainText(f"Name: {person['Full Name']}\n"
                                    f"Birthday: {person['Birthday']}\n"
                                    f"ID: {person['ID']}\n"
                                    f"Gender: {person['Gender']}\n"
                                    f"Phone Number: {person['Phone Number']}\n"
                                    f"Address: {person['Address']}")

            font = QtGui.QFont()
            font.setPointSize(17)
            info_text.setFont(font)

            spacer_left = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            spacer_right = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

            info_layout = QtWidgets.QVBoxLayout(info_container)
            info_layout.addItem(spacer_left)
            info_layout.addWidget(info_text)
            info_layout.addItem(spacer_right)

            found_button = QtWidgets.QPushButton("Found", Form)
            found_button.setObjectName(f"found_button_{person['Full Name']}")
            found_button.clicked.connect(lambda checked, name=folder_name: self.execute_open(name))

            # Create a button container with a vertical layout
            button_container = QtWidgets.QWidget()
            button_container_layout = QtWidgets.QVBoxLayout(button_container)

            # Create a button for the new empty box
            empty_box_button = QtWidgets.QPushButton("TIME/DATE", Form)
            empty_box_button.setObjectName(f"empty_box_button_{person['Full Name']}")
            empty_box_button.clicked.connect(lambda checked, name=folder_name: self.create_and_show_date_time_box(name))

            delete_button = QtWidgets.QPushButton("Delete", Form)
            delete_button.setObjectName(f"delete_button_{person['Full Name']}")
            delete_button.clicked.connect(lambda checked, name=person['Full Name']: self.delete_person(name))

            not_found_button = QtWidgets.QPushButton("Not Found", Form)
            not_found_button.setObjectName(f"not_found_button_{person['Full Name']}")

            self.buttons[person['Full Name']] = {'found_button': found_button, 'not_found_button': not_found_button,
                                                'empty_box_button': empty_box_button}
            
            button_container_layout.addWidget(found_button)
            button_container_layout.addWidget(delete_button)
            button_container_layout.addWidget(not_found_button)
            button_container_layout.addWidget(empty_box_button)

            person_layout.addWidget(image_label)
            person_layout.addWidget(info_container)
            person_layout.addWidget(button_container)

            self.verticalLayout.addLayout(person_layout)

            if has_folder:
                found_button.setEnabled(True)
                empty_box_button.setEnabled(True)
                not_found_button.setEnabled(False)
            else:
                found_button.setEnabled(False)
                empty_box_button.setEnabled(False)
                not_found_button.setEnabled(True)

        self.scrollArea.setStyleSheet("background-image: url('register.jpg');")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Create a back button and set its properties
        self.back_button = QToolButton(Form)
        self.back_button.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.back_button.setIcon(QIcon("back.png"))
        self.back_button.setIconSize(QtCore.QSize(28, 28))
        self.back_button.setStyleSheet("background-color: white;")
        self.back_button.clicked.connect(self.go_to_GUI)

        # Add the top bar layout to the main layout
        main_layout = QtWidgets.QVBoxLayout(Form)
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(self.scrollArea)
        main_layout.addWidget(self.back_button)

    def scale_to_fit_image_label(self, pixmap, image_label):
        label_size = image_label.size()
        aspect_ratio = pixmap.width() / pixmap.height()

        # Determine the size that fits the label while preserving the aspect ratio
        if label_size.width() / aspect_ratio <= label_size.height():
            new_width = label_size.width()
            new_height = int(label_size.width() / aspect_ratio)
        else:
            new_width = int(label_size.height() * aspect_ratio)
            new_height = label_size.height()

        return pixmap.scaled(new_width, new_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)    
        
    def create_date_time_box(self, person_name):
        date_time_layout = QVBoxLayout()
        date_time_layout.setObjectName(f"date_time_layout_{person_name}")

        date_time_label = QLabel(f"Images for {person_name}")

        image_path = self.get_image_path(person_name)
        if image_path:
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(image_path))

            # Format the date and time in a 12-hour system
            formatted_time = creation_time.strftime("%I:%M %p")
            formatted_date = creation_time.strftime("%B %d, %Y")

            # Extract the percentage from the image filename
            image_filename = os.path.basename(image_path)
            percentage = None
            try:
                percentage = int(image_filename.split("_")[1].split(".")[0])  # Assuming filename format is "name_percentage.jpg"
            except (ValueError, IndexError):
                percentage = None

            percentage_text = QTextBrowser()
            if percentage is not None:
                percentage_text.setPlainText(f"Match Percentage: {percentage}%")
            else:
                percentage_text.setPlainText("Match Percentage: N/A")

            percentage_text.setObjectName(f"percentage_text_{person_name}")

            date_time_text = QTextBrowser()
            date_time_text.setPlainText(f"Image Date and Time: {formatted_date} at {formatted_time}\nLocation: Amman\nMatch Percentage: {percentage}%")
            date_time_text.setObjectName(f"date_time_text_{person_name}")  # Set an object name

            # Create a label for displaying the resized image (400x400)
            image_label = QLabel()
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(400, 400)
            image_label.setPixmap(pixmap)

            date_time_layout.addWidget(image_label)

            # Create right and left buttons to navigate between images
            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)

            right_button = QPushButton("Next")
            right_button.clicked.connect(lambda: self.show_next_image(person_name, image_label, date_time_text, percentage_text))

            left_button = QPushButton("Previous")
            left_button.clicked.connect(lambda: self.show_previous_image(person_name, image_label, date_time_text, percentage_text))

            button_layout.addWidget(left_button)
            button_layout.addWidget(right_button)

            date_time_layout.addWidget(button_container)

            date_time_layout.addWidget(date_time_label)
            date_time_layout.addWidget(date_time_text)

        return date_time_layout
    
    def __init__(self):
        self.current_image_index = {}
        self.time_date_boxes = {} 
        
    def show_next_image(self, person_name, image_label, date_time_text, percentage_text):
        # Get the list of image files for the person
        folder_path = os.path.join('matches', person_name)
        image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        if image_files:
            current_index = self.current_image_index.get(person_name, 0)
            next_index = (current_index + 1) % len(image_files)
            next_image_path = os.path.join(folder_path, image_files[next_index])

            pixmap = QPixmap(next_image_path)
            # Resize the image to 400x400 pixels
            pixmap = pixmap.scaled(400, 400)
            image_label.setPixmap(pixmap)

            # Extract the percentage from the image filename and display it
            percentage = self.extract_percentage_from_filename(image_files[next_index])
            percentage_text.setPlainText(f"Match Percentage: {percentage}%")

            # Update the time and date based on the new image
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(next_image_path))
            formatted_time = creation_time.strftime("%I:%M %p")
            formatted_date = creation_time.strftime("%B %d, %Y")
            date_time_text.setPlainText(f"Image Date and Time: {formatted_date} at {formatted_time}\nLocation: Amman\nMatch Percentage: {percentage}%")

        # Update the current image index for this person
        self.current_image_index[person_name] = next_index

    def show_previous_image(self, person_name, image_label, date_time_text, percentage_text):
        # Get the list of image files for the person
        folder_path = os.path.join('matches', person_name)
        image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        if image_files:
            current_index = self.current_image_index.get(person_name, 0)
            previous_index = (current_index - 1) % len(image_files)
            previous_image_path = os.path.join(folder_path, image_files[previous_index])

            pixmap = QPixmap(previous_image_path)
            # Resize the image to 400x400 pixels
            pixmap = pixmap.scaled(400, 400)
            image_label.setPixmap(pixmap)

            # Extract the percentage from the image filename and display it
            percentage = self.extract_percentage_from_filename(image_files[previous_index])
            percentage_text.setPlainText(f"Match Percentage: {percentage}%")

            # Update the time and date based on the new image
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(previous_image_path))
            formatted_time = creation_time.strftime("%I:%M %p")
            formatted_date = creation_time.strftime("%B %d, %Y")
            date_time_text.setPlainText(f"Image Date and Time: {formatted_date} at {formatted_time}\nLocation: Amman\nMatch Percentage: {percentage}%")

        # Update the current image index for this person
        self.current_image_index[person_name] = previous_index

    def extract_percentage_from_filename(self, filename):
        try:
            percentage = int(filename.split("_")[1].split(".")[0])  # Assuming filename format is "name_percentage.jpg"
            return percentage
        except (ValueError, IndexError):
            return None


    def create_and_show_date_time_box(self, person_name):
        if person_name in self.time_date_boxes and self.time_date_boxes[person_name]:
            # Box is open, so close it
            self.close_date_time_box(person_name)
        else:
            # Box is closed, so create and show it
            date_time_layout = self.create_date_time_box(person_name)
            person_layout = self.verticalLayout.findChild(QtWidgets.QHBoxLayout, f"layout_{person_name}")

            if person_layout:
                person_layout.addLayout(date_time_layout)
                self.time_date_boxes[person_name] = True

    def close_date_time_box(self, person_name):
        # Remove the layout containing time/date information
        person_layout = self.verticalLayout.findChild(QtWidgets.QHBoxLayout, f"layout_{person_name}")
        if person_layout:
            date_time_layout = person_layout.findChild(QtWidgets.QVBoxLayout, f"date_time_layout_{person_name}")
            if date_time_layout:
                for i in reversed(range(date_time_layout.count())):
                    widget = date_time_layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()
                self.time_date_boxes[person_name] = False 
        
    def get_image_path(self, person_name):
        folder_path = os.path.join('matches', person_name)
        if os.path.exists(folder_path):
            image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            if image_files:
                image_files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
                return os.path.join(folder_path, image_files[-1])
        return None
    
    def toggle_search_button(self):
        if self.search_bar.text().strip():
            self.search_button.setEnabled(True)
        else:
            self.search_button.setEnabled(False)

    def delete_person(self, name):
        with open('registration_data.json', 'r') as json_file:
            data = json.load(json_file)

        person_to_delete = None
        for person in data:
            if person['Full Name'] == name:
                person_to_delete = person
                break

        if person_to_delete:
            data.remove(person_to_delete)

            with open('registration_data.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

            image_path = os.path.join('images', f"{name}.jpg")
            if os.path.exists(image_path):
                os.remove(image_path)

            person_layout = self.verticalLayout.findChild(QtWidgets.QHBoxLayout, f"layout_{name}")
            if person_layout:
                for i in reversed(range(person_layout.count())):
                    widget = person_layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()

            self.scrollArea.update()
        else:
            QtWidgets.QMessageBox.information(Form, "Person Not Found", "The person was not found in the data.")

    def search_names(self):
        search_text = self.search_bar.text().strip().lower()

        with open('registration_data.json', 'r') as json_file:
            data = json.load(json_file)

        results_found = False

        for person in data:
            if search_text in person['Full Name'].lower():
                results_found = True

                person_layout = self.verticalLayout.findChild(QtWidgets.QHBoxLayout, f"layout_{person['Full Name']}")
                if person_layout:
                    scroll_pos = person_layout.geometry().top()
                    self.scrollArea.verticalScrollBar().setValue(scroll_pos)

        if not results_found:
            QtWidgets.QMessageBox.information(Form, "No Results", "No results found for the search.")

    def execute_open(self, folder_name):
        directory_path = os.path.join('matches', folder_name)
        if os.path.exists(directory_path):
            operating_system = sys.platform
            try:
                if operating_system.startswith('win'):  # Windows
                    subprocess.Popen(['explorer', directory_path], shell=True)
                elif operating_system.startswith('darwin'):  # macOS
                    subprocess.Popen(['open', directory_path])
                elif operating_system.startswith('linux'):  # Linux
                    subprocess.Popen(['xdg-open', directory_path])
                else:
                    print("Unsupported operating system.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        else:
            QtWidgets.QMessageBox.information(Form, "Directory Not Found", "Directory not found for this person.")

    def go_to_GUI(self):
        Form.close()
        upload_process = subprocess.Popen([sys.executable, "mainGUItest.py"])
        upload_process.wait()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form5()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
