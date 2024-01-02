from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from methods import Register, Recognition
import sys

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.register = Register()
        self.recognition = Recognition()

        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)

        self.btn_register = QPushButton('Registrar persona', self)
        self.btn_register.clicked.connect(self.show_register_form)
        self.main_layout.addWidget(self.btn_register)

        self.btn_identify = QPushButton('Identificar personas', self)
        self.btn_identify.clicked.connect(self.identify_face)
        self.main_layout.addWidget(self.btn_identify)

        self.btn_exit = QPushButton('Salir', self)
        self.btn_exit.clicked.connect(self.close)
        self.main_layout.addWidget(self.btn_exit)

        self.setWindowTitle('Sistema de Registro e Identificación')
        self.show()

    def show_register_form(self):
        self.form_layout = QVBoxLayout()

        self.document_number_input = QLineEdit(self)
        self.names_input = QLineEdit(self)
        self.last_names_input = QLineEdit(self)
        self.gender_input = QLineEdit(self)

        self.set_input_field_size(self.document_number_input)
        self.set_input_field_size(self.names_input)
        self.set_input_field_size(self.last_names_input)
        self.set_input_field_size(self.gender_input)

        self.setup_input_field(self.form_layout, 'Número de documento:', self.document_number_input)
        self.setup_input_field(self.form_layout, 'Nombres:', self.names_input)
        self.setup_input_field(self.form_layout, 'Apellidos:', self.last_names_input)
        self.setup_input_field(self.form_layout, 'Género:', self.gender_input)

        btn_register_submit = QPushButton('Registrar', self)
        btn_register_submit.clicked.connect(self.register_user)
        self.form_layout.addWidget(btn_register_submit)

        self.main_layout.addLayout(self.form_layout)
        self.btn_register.setDisabled(True)

    def set_input_field_size(self, input_widget):
        input_widget.setFixedWidth(200)  # Ajusta el ancho aquí según tus necesidades

    def setup_input_field(self, layout, label_text, input_widget):
        row = QHBoxLayout()
        label = QLabel(label_text, self)
        row.addWidget(label)
        row.addWidget(input_widget)
        layout.addLayout(row)

    def register_user(self):
        document_number = self.document_number_input.text()
        names = self.names_input.text()
        last_names = self.last_names_input.text()
        gender = self.gender_input.text()
        
        success = self.register.create_register_user(document_number, names, last_names, gender)
        if success:
            QMessageBox.information(self, 'Registro Exitoso', '¡Persona registrada exitosamente!')
        else:
            QMessageBox.critical(self, 'Error en el Registro', 'Error al intentar registrar la persona.')

        self.clear_register_form()

    def clear_register_form(self):
        for i in reversed(range(self.form_layout.count())): 
            widget = self.form_layout.itemAt(i).widget()
            if widget is not None: 
                widget.deleteLater()
        self.btn_register.setEnabled(True)

    def identify_face(self):
        success, result = self.recognition.catch_face()
        if success:
            QMessageBox.information(self, 'Identificación Exitosa', f'Identificación exitosa. Resultado: {result}')
        else:
            QMessageBox.warning(self, 'Error en la Identificación', 'No se encontró un rostro.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec())
