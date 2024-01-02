import pymysql

class DataBase:

    # Parámetros para establecer la conexión con la base de datos
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "srf"
        self.connection = None
        self.cursor = None


    # Método para establecer la conexión con la base de datos
    def connect(self):
        try:
            self.connection = pymysql.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database 
            )
            self.cursor = self.connection.cursor()
            # print("Conexión exitosa a la base de datos.")
        except pymysql.Error  as e:
            print(f"Error de conexión: {e}")


    # Método que retorna el cursor con el que se ejecutan las sentencias SQL
    def get_cursor(self):
        if self.cursor:
            return self.cursor
        else:
             print("No hay un cursor disponible. Debes conectarte primero.")


    # Método para terminar la conexión con la base de datos
    def disconnect(self):
        if self.connection:
            self.connection.close()
            # print("Conexión cerrada.")
        else:
            print("No hay conexión a la base de datos.")