from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

import Db

class SensorApp(App):
    def build(self):
        # Database
        connection_string = 'connection string...'
        self.db = Db.database(connection_string)

        # Crear el diseño principal
        self.layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        # Agregar el ScrollView y el botón a la aplicación
        self.root_layout = BoxLayout(orientation='vertical')
        # Agregar un TextInput para ingresar el ID de la embarcación
        self.input_label = Label(text="ID de Embarcación:")
        self.input_id = TextInput()
        self.root_layout.add_widget(self.input_label)
        self.root_layout.add_widget(self.input_id)

        # Crear un botón para actualizar los datos
        self.update_button = Button(text="Actualizar Datos", on_press=self.update_sensor_labels)

        # Agregar el diseño a un ScrollView para manejar contenido desbordado
        scrollview = ScrollView()
        scrollview.add_widget(self.layout)


        self.root_layout.add_widget(scrollview)
        self.root_layout.add_widget(self.update_button)

        return self.root_layout

    def update_sensor_labels(self, *args):
        # Limpiar el diseño antes de agregar las nuevas etiquetas
        self.layout.clear_widgets()

        # Obtener el ID de la embarcación desde el TextInput
        id_embarcacion = self.input_id.text

        # Obtener los nuevos datos de sensores
        sensor_data = self.db.get_sensor_data(id_embarcacion)

        # Crear etiquetas para los datos de sensores
        sensor_type_label = Label(text=f"Informacion: {sensor_data}", size_hint_y=None, height=40)
        self.layout.add_widget(sensor_type_label)

if __name__ == '__main__':
    SensorApp().run()
