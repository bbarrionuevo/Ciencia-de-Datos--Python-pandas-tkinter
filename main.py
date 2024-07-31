import pandas as pd
import tkinter as tk
from Recursos.Funciones import VentanaGraficos, leer_datos, limpiar_datos

def main():
    # Define la ruta al archivo CSV
    file_path = '.\\snic-pais.csv'

    # Leer y limpiar los datos
    data = leer_datos(file_path)
    if data is None:
        exit()

    data = limpiar_datos(data)

    # Crear ventana principal de Tkinter
    root = tk.Tk()
    root.title('Selección de Gráficos Principal')
    
    # Maximizar la ventana principal
    root.state('zoomed')  # Esta línea maximiza la ventana al iniciar

    # Mostrar la ventana de gráficos
    ventana_graficos = VentanaGraficos(master=root, data=data)
    ventana_graficos.mainloop()

if __name__ == "__main__":
    main()
