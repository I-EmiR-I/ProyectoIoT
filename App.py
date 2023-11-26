
#libreria para la interfaz
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget,QMessageBox,QDialog, QVBoxLayout, QLabel
import sys
import Db
from datetime import datetime

# Clase base para MicroControladores
class MicroControladores:
    def __init__(self, MicroControladoresID, EmbarcacionID, Funcionamiento, modelo):
        self.MicroControladoresID = MicroControladoresID
        self.EmbarcacionID = EmbarcacionID
        self.Funcionamiento = Funcionamiento
        self.modelo = modelo


    def DesplegarDatosSensores(self):
        # Implementa la lógica para desplegar los datos de los sensores
        pass

    def EnviarDatosEmbarcacion(self):
        # Implementa la lógica para enviar datos a la embarcación
        pass

    def EvaluarProblema(self):
        # Implementa la lógica para evaluar problemas
        pass

    def ListaSensores(self):
        # Implementa la lógica para obtener la lista de sensores
        pass

# Clase SensorInfrarrojo heredando de MicroControladores
class SensorInfrarrojo:
    def __init__(self, IDInfrarojo, microcontrolador, modelo):
        self.IDInfrarojo = IDInfrarojo
        self.Distancia = 0
        self.Estado = False
        self.microcontrolador = microcontrolador  # Asigna el microcontrolador al sensor
        self.modelo = modelo

    def isActivo(self):
        return self.Estado

    def Activar(self):
        self.Estado = True

    def Desactivar(self):
        self.Estado = False

    def medirDistancia(self):
        # Implementa la lógica para medir la distancia
        pass

    def VerificarSeguridad(self):
        # Implementa la lógica para verificar la seguridad
        pass

# Clase SensorMovimiento heredando de MicroControladores
class SensorMovimiento:
    def __init__(self, IDUltrasonico, microcontrolador, modelo):
        self.IDUltrasonico = IDUltrasonico
        self.LED = False
        self.Estado = False
        self.microcontrolador = microcontrolador  # Asigna el microcontrolador al sensor
        self.modelo = modelo

    def isActivo(self):
        return self.Estado

    def Activar(self):
        self.Estado = True

    def Desactivar(self):
        self.Estado = False

    def EncenderLED(self):
        self.LED = True

    def ApagarLED(self):
        self.LED = False

    def detectar_movimiento(self):
        #logica para detectar movimiento
        pass

# Clase SensorUltrasonico heredando de MicroControladores
class SensorUltrasonico:
    def __init__(self, IDUltrasonico, microcontrolador, modelo):
        self.IDUltrasonico = IDUltrasonico
        self.LED = False
        self.Estado = False
        self.microcontrolador = microcontrolador  # Asigna el microcontrolador al sensor
        self.modelo = modelo

    def isActivo(self):
        return self.Estado

    def Activar(self):
        self.Estado = True

    def Desactivar(self):
        self.Estado = False

    def leerDistancia(self):
        # Implementa la lógica para leer la distancia
        pass

    def EncenderLED(self):
        self.LED = True

    def ApagarLED(self):
        self.LED = False

class Embarcacion:
    def __init__(self, embarcacion_id, nombre, tipo, capacidad, año_fabricacion,):
        self.embarcacion_id = embarcacion_id
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        self.año_fabricacion = año_fabricacion
        self.microcontroladores = []  # Lista de microcontroladores

        # Crea un microcontrolador predeterminado y lo agrega a la lista
        microcontrolador_default = MicroControladores(0, self.embarcacion_id, True, "ControladorDefault")
        self.microcontroladores.append(microcontrolador_default)

    def cantidad_microcontroladores(self):
        return len(self.microcontroladores)
    def desplegar_datos(self):
        print(f"ID: {self.embarcacion_id}, Nombre: {self.nombre}, Tipo: {self.tipo}, Capacidad: {self.capacidad}")

    def crear_microcontrolador(self, MicroControladoresID, Funcionamiento, modelo):
        microcontrolador = MicroControladores(MicroControladoresID, self.embarcacion_id, Funcionamiento, modelo)
        self.microcontroladores.append(microcontrolador)
        return microcontrolador

    def listar_microcontroladores(self):
        print("Microcontroladores en la embarcación:")
        for mc in self.microcontroladores:
            print(f"ID: {mc.MicroControladoresID}, Modelo: {mc.modelo}")
            mc.ListaSensores()
            mc.DesplegarDatosSensores()

    def diagnostico_microcontroladores(self):
        for mc in self.microcontroladores:
            mc.EvaluarProblema()

class InstalacionPortuaria:
    def __init__(self, instalacion_id, nombre, ubicacion, capacidad, tipo):
        self.instalacion_id = instalacion_id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.capacidad = capacidad
        self.tipo = tipo

        connection_string = 'connection string'
        self.db = Db.database(connection_string)

    def desplegar_datos(self):
        print(
            f"ID: {self.instalacion_id}, Nombre: {self.nombre}, Ubicación: {self.ubicacion}, Capacidad: {self.capacidad}")

    def embarcaciones(self):
        self.embarcaciones = self.db.get_embarcaciones()
        return self.embarcaciones
    def eliminar_embarcacion(self, embarcacion):
        if embarcacion in self.embarcaciones:
            self.embarcaciones.remove(embarcacion)
class AlertaMarina:
    def __init__(self, alerta_id, fecha, hora, tipo, gravedad, embarcacion, instalacion):
        self.alerta_id = alerta_id
        self.fecha = fecha
        self.hora = hora
        self.tipo = tipo
        self.gravedad = gravedad
        self.embarcacion = embarcacion
        self.instalacion = instalacion

    def desplegar_alerta(self):
        print(f"ID de Alerta: {self.alerta_id}")
        print(f"Fecha: {self.fecha}")
        print(f"Hora: {self.hora}")
        print(f"Tipo: {self.tipo}")
        print(f"Gravedad: {self.gravedad}")
        print("Embarcación relacionada:")
        self.embarcacion.desplegar_datos()
        print("Instalación Portuaria relacionada:")
        self.instalacion.desplegar_datos()

    def informar_ubicacion(self):
        print("Ubicación de la alerta:")
        self.embarcacion.desplegar_datos()

    def desplegar_hora_alerta(self):
        print(f"Hora de la alerta: {self.hora}")

class VentanaSensores(QDialog):
    def __init__(self, id_embarcacion, sensor_data):
        super().__init__()

        self.setWindowTitle(f"Sensores de Embarcación {id_embarcacion}")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Mostrar la información de los sensores
        print(sensor_data)

        for i in range(0, len(sensor_data)):
            sensor_type = sensor_data[i][0]
            value = sensor_data[i][1]
            fecha = sensor_data[i][2]
            print('a')
            # Formatear la fecha si es necesario
            if isinstance(fecha, datetime):
                fecha = fecha.strftime('%Y-%m-%d %H:%M:%S')
            print('b')
            label_text = f"{sensor_type}: {value} ({fecha})"
            label = QLabel(label_text)
            layout.addWidget(label)
            print(fecha,'asd')
        print('c')
        self.setLayout(layout)
class InterfazEmbarcaciones(QMainWindow):
    def __init__(self,puerto=InstalacionPortuaria):
        super().__init__()
        connection_string = ''
        self.db = Db.database(connection_string)

        self.setWindowTitle("Gestión de Embarcaciones")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Crear una tabla para mostrar la lista de embarcaciones
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # Cuatro columnas para ID, Nombre
        self.table_widget.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.layout.addWidget(self.table_widget)

        # Botones para seleccionar, eliminar y agregar embarcaciones
        self.btn_seleccionar = QPushButton("Seleccionar Embarcación")

        self.layout.addWidget(self.btn_seleccionar)

        self.central_widget.setLayout(self.layout)

        # Conectar botones a funciones de manejo de eventos
        self.btn_seleccionar.clicked.connect(self.seleccionar_embarcacion)

        self.mostrar_embarcaciones()
    def mostrar_embarcaciones(self):
        # Obtener la lista de embarcaciones
        embarcaciones = self.db.get_embarcaciones()
        print(embarcaciones)

        # Limpiar la tabla antes de mostrar los datos
        self.table_widget.setRowCount(0)

        # Agregar las filas con los datos de las embarcaciones
        index=0
        for embarcacion in embarcaciones:
            self.table_widget.insertRow(index)
            self.table_widget.setItem(index, 0, QTableWidgetItem(str(embarcacion[0])))
            self.table_widget.setItem(index, 1, QTableWidgetItem(embarcacion[1]))
            index+=1

    def seleccionar_embarcacion(self):
        # Obtén la fila seleccionada
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            # Obtén la información de sensores para la embarcación seleccionada
            id_embarcacion = int(self.table_widget.item(selected_row, 0).text())
            sensor_data = self.db.get_sensor_data(id_embarcacion)

            # Abre la nueva ventana para mostrar los sensores
            ventana_sensores = VentanaSensores(id_embarcacion, sensor_data)
            ventana_sensores.exec_()
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona una embarcación para ver los sensores")


#Test
if __name__ == "__main__":
    # Crear una instancia de MicroControladores
    microcontrolador = MicroControladores(1, 1, True, "Controlador1")

    # Crear una embarcación y agregar un microcontrolador
    embarcacion = Embarcacion(1, "Embarcacion1", "Tipo1", 100, 2022)
    microcontrolador_embarcacion = embarcacion.crear_microcontrolador(1, True, "Controlador2")

    # Crear un sensor infrarrojo y asignar el microcontrolador
    sensor_infrarrojo = SensorInfrarrojo(1, microcontrolador_embarcacion, "ModeloSensor1")

    # Agregar el sensor infrarrojo a la lista de sensores de la embarcación
    embarcacion.listar_microcontroladores()

    # Crear una instalación portuaria y agregar la embarcación
    puerto = InstalacionPortuaria(1, "Puerto1", "Ubicación1", 1000, "TipoA")
    puerto.embarcaciones

    app = QApplication(sys.argv)
    ventana = InterfazEmbarcaciones(puerto)
    ventana.show()
    sys.exit(app.exec_())
