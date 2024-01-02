class Querys:

    def __init__(self):
        pass


    # Método que genera la sentecia SQL de Insertar en una tabla de la base de datos
    def insert_user(self, document_number, names, last_names, face, gender):
        return f"INSERT INTO users (document_number, type_document, names, last_names, face, gender) VALUES ('{document_number}', 1, '{names}', '{last_names}', '{face}', '{gender}')"
    
    
    # Método que genera la sentencia SQL de Consultar todos los registros de una tabla de la base de datos
    def select_user(self, column1, column2):
        return f"SELECT {column1}, {column2} FROM users"