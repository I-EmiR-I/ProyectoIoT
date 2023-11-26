import pyodbc
import requests

class database:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def execute_query(self,query):
        try:
            # Crear una conexión a la base de datos
            connection = pyodbc.connect(self.connection_string)

            # Crear un cursor para ejecutar comandos SQL
            cursor = connection.cursor()

            # tabla information


            cursor.execute(query)

            # Confirmar y cerrar la conexión
            connection.commit()
            connection.close()
            return True
        except Exception as e:
            print(f'Error al ejecutar la query: {str(e)}')
            return False

    def show_tables(self,query):
        # Crear una conexión a la base de datos
        connection = pyodbc.connect(self.connection_string)

        # Crear un cursor para ejecutar comandos SQL
        cursor = connection.cursor()

        for query in queries:
            print(f"Resultados para la consulta: {query}")
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def request_php(self,sensor,params):

        # URL de tu script PHP
        url = f"http://localhost/Php_Iot/{sensor}.php"
        print(url)

        # Realizar una solicitud GET con los parámetros
        response = requests.get(url, params=params)

        # Imprimir la respuesta del servidor
        print(response.text)

    def get_sensor_data(self, embarcacion_id):
        queries = [
            "SELECT 'Temperatura' as SensorType, Temperatura, FechaMedicion FROM SensoresTemperatura WHERE EmbarcacionID = ?",
            "SELECT 'Ultrasonico' as SensorType, DistanciaMedida, FechaMedicion FROM SensoresUltrasonicos WHERE EmbarcacionID = ?",
            "SELECT 'Movimiento' as SensorType, MovimientoDetectado, FechaMedicion FROM SensoresMovimiento WHERE EmbarcacionID = ?",
            "SELECT 'GPS' as SensorType, Latitud, Longitud, FechaMedicion FROM SensoresGPS WHERE EmbarcacionID = ?"
        ]

        # Crear una conexión a la base de datos
        connection = pyodbc.connect(self.connection_string)

        # Crear un cursor para ejecutar comandos SQL
        cursor = connection.cursor()

        sensor_data = []

        for query in queries:
            cursor.execute(query, embarcacion_id)
            results = cursor.fetchall()

            # Obtener el último resultado (el más reciente)
            latest_result = results[-1]

            # Si es un sensor de tipo 'GPS', combinar las coordenadas
            if latest_result[0] == 'GPS':
                latitud = latest_result[1]
                longitud = latest_result[2]
                coordenadas = f"{latitud}, {longitud}"
                sensor_data.append(('GPS', coordenadas, latest_result[3]))
            else:
                # Agregar el resultado tal como está para otros tipos de sensores
                sensor_data.append(latest_result)

        return sensor_data

    def get_embarcaciones(self):
        print('asd')
        # Crear una conexión a la base de datos
        connection = pyodbc.connect(self.connection_string)

        # Crear un cursor para ejecutar comandos SQL
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Embarcaciones")
        results = cursor.fetchall()

        return results

connection_string = 'connection string...'
db = database(connection_string)

#tablas
tabla_embarcaciones = """CREATE TABLE Embarcaciones (
    id INT PRIMARY KEY,
    Nombre VARCHAR(255),
    FechaRegistro DATE
)
"""

tabla_temperatura = """CREATE TABLE SensoresTemperatura (
    id INT,
    Temperatura FLOAT,
    FechaMedicion DATE,
    EmbarcacionID INT,
    FOREIGN KEY (EmbarcacionID) REFERENCES Embarcaciones(id)
)"""

tabla_gps = """CREATE TABLE SensoresGPS (
    id INT,
    Latitud FLOAT,
    Longitud FLOAT,
    FechaMedicion DATE,
    EmbarcacionID INT,
    FOREIGN KEY (EmbarcacionID) REFERENCES Embarcaciones(id)
)"""

tabla_ultrasonico = """CREATE TABLE SensoresUltrasonicos (
    id INT,
    DistanciaMedida FLOAT,
    FechaMedicion DATE,
    EmbarcacionID INT,
    FOREIGN KEY (EmbarcacionID) REFERENCES Embarcaciones(id)
)"""

tabla_movimiento = """CREATE TABLE SensoresMovimiento (
    id INT,
    MovimientoDetectado INT,
    FechaMedicion DATE,
    EmbarcacionID INT,
    FOREIGN KEY (EmbarcacionID) REFERENCES Embarcaciones(id)
)"""

#Crea las tablas
db.execute_query(tabla_embarcaciones)
db.execute_query(tabla_movimiento)
db.execute_query(tabla_gps)
db.execute_query(tabla_temperatura)
db.execute_query(tabla_ultrasonico)

#Datos de prueba
prueba = """INSERT INTO Embarcaciones (id, Nombre, FechaRegistro) VALUES
(1, 'Embarcacion1', '2023-01-01'),
(2, 'Embarcacion2', '2023-01-02'),
(3, 'Embarcacion3', '2023-01-03');

-- Para la tabla de SensoresTemperatura
INSERT INTO SensoresTemperatura (id, Temperatura, FechaMedicion, EmbarcacionID) VALUES
(1, 25.5, '2023-01-01', 1),
(2, 26.0, '2023-01-02', 2),
(3, 24.8, '2023-01-03', 3);

-- Para la tabla de SensoresGPS
INSERT INTO SensoresGPS (id, Latitud, Longitud, FechaMedicion, EmbarcacionID) VALUES
(1, 35.6895, 139.6917, '2023-01-01', 1),
(2, 40.7128, -74.0060, '2023-01-02', 2),
(3, 51.5074, -0.1278, '2023-01-03', 3);

-- Para la tabla de SensoresUltrasonicos
INSERT INTO SensoresUltrasonicos (id, DistanciaMedida, FechaMedicion, EmbarcacionID) VALUES
(1, 10.5, '2023-01-01', 1),
(2, 9.8, '2023-01-02', 2),
(3, 11.2, '2023-01-03', 3);

-- Para la tabla de SensoresMovimiento
INSERT INTO SensoresMovimiento (id, MovimientoDetectado, FechaMedicion, EmbarcacionID) VALUES
(1, 1, '2023-01-01', 1),
(2, 0, '2023-01-02', 2),
(3, 1, '2023-01-03', 3);"""

#Ver datos de prueba
queries = [
    "SELECT * FROM Embarcaciones;",
    "SELECT * FROM SensoresTemperatura;",
    "SELECT * FROM SensoresGPS;",
    "SELECT * FROM SensoresUltrasonicos;",
    "SELECT * FROM SensoresMovimiento;"
]
#inserta los datos de prueba
#db.execute_query(prueba)

#Ejecutar las consultas y mostrar los resultados
db.show_tables(queries)

# Parámetros para el sensor de GPS
params_gps = {'latitud': 12.32,'longitud': -56.76,'embarcacionID': 3,'idSensor': 2}

# Parametros para el sensor de movimiento
params_movimiento = {'movimientoDetectado': 0,'embarcacionID': 3,'idSensor': 4}

# Parametros para el sensor de temperatura
params_temperatura = {'temperatura': 20.5,'embarcacionID': 3,'idSensor': 1}

# Parametros para el sensor ultrasonico
params_ultrasonico = {'distanciaMedida': 40.5,'embarcacionID': 3,'idSensor': 3}

# Simualcion de request send para cada sensor
db.request_php(sensor="SendDataTemperatura",params=params_temperatura)
db.request_php(sensor="SendDataUltrasonico",params=params_ultrasonico)
db.request_php(sensor="SendDataMovimiento",params=params_movimiento)
db.request_php(sensor="SendDataGPS",params=params_gps)

#Muestra los datos nuevamente para verificar que funciono
db.show_tables(queries)

#Obtener todos los sensores relacionados a cierta embarcacion por ID
print(db.get_sensor_data(embarcacion_id=3))
