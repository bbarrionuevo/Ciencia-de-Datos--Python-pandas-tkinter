import pandas as pd
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns

class VentanaGraficos(tk.Frame):
    def __init__(self, master=None, data=None):
        super().__init__(master)
        self.master = master
        self.data = data
        self.fig = None
        self.canvas = None
        
        self.master.title('Selección de Gráficos')
        self.master.geometry('800x600')
        
        self.pack()
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Botones para cada gráfico
        btn_grafico1 = tk.Button(self, text='Cantidad de Delitos por Año', command=self.grafico_cantidad_delitos_por_año)
        btn_grafico1.pack(pady=10)
        
        btn_grafico2 = tk.Button(self, text='TOP 5 Delitos 2022', command=self.grafico_tipo_delitos_2022)
        btn_grafico2.pack(pady=10)
        
        btn_grafico3 = tk.Button(self, text='Cantidad de Víctimas por Género', command=self.grafico_victimas_por_genero)
        btn_grafico3.pack(pady=10)
        
    def grafico_cantidad_delitos_por_año(self):
        self.cerrar_grafico_actual()
        cantidad_hechos_por_año = sumar_cantidad_hechos_por_año(self.data)
        
        self.fig = plt.figure(figsize=(10, 6))
        sns.lineplot(data=cantidad_hechos_por_año, x='anio', y='cantidad_hechos', marker='o')
        plt.title('Cantidad de Delitos por Año')
        plt.xlabel('Año')
        plt.ylabel('Cantidad de delitos (en cientos de miles)')
        plt.grid(True)
        plt.tight_layout()
        self.fig.savefig('cantidad_delitos_por_año.png')  
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
        
    def grafico_tipo_delitos_2022(self):
        self.cerrar_grafico_actual()
        delitos_filtrados = filtrar_delitos_2022(self.data)
        delitos_agrupados = agrupar_delitos_2022(delitos_filtrados)
        
        self.fig = plt.figure(figsize=(10, 8))
        sns.barplot(data=delitos_agrupados, x='cantidad_hechos', y='codigo_delito_snic_nombre', palette='viridis', hue='codigo_delito_snic_nombre', orient='h', legend=False)
        plt.title('TOP 5 Delitos 2022')
        plt.xlabel('Cantidad de Delitos')
        plt.ylabel('Tipo de Delito')
        plt.tight_layout()
        self.fig.savefig('tipo_delitos_2022_filtrados_horizontal.png')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
        
    def grafico_victimas_por_genero(self):
        self.cerrar_grafico_actual()
        victimas_totales = calcular_victimas_totales(self.data)
        
        self.fig = plt.figure(figsize=(8, 8))
        plt.pie(victimas_totales.values(), labels=victimas_totales.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Cantidad de Víctimas por Género')
        plt.tight_layout()
        self.fig.savefig('cantidad_victimas_por_genero.png')
        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
        
    def cerrar_grafico_actual(self):
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.canvas.get_tk_widget().pack_forget()

def leer_datos(file_path):
    try:
        data = pd.read_csv(file_path, delimiter=';', encoding='latin-1')
        return data
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None

def limpiar_datos(data):
    data['tasa_hechos'] = data['tasa_hechos'].str.replace(',', '.').astype(float)
    data['tasa_victimas'] = data['tasa_victimas'].str.replace(',', '.').astype(float)
    data['tasa_victimas_masc'] = data['tasa_victimas_masc'].str.replace(',', '.').astype(float)
    data['tasa_victimas_fem'] = data['tasa_victimas_fem'].str.replace(',', '.').astype(float)
    data['cantidad_hechos'] = pd.to_numeric(data['cantidad_hechos'], errors='coerce')
    return data

def filtrar_datos_por_rango(data):
    return data[(data['anio'] >= 2000) & (data['anio'] <= 2022)]

def sumar_cantidad_hechos_por_año(filtered_data):
    return filtered_data.groupby('anio')['cantidad_hechos'].sum().reset_index()

def filtrar_delitos_2022(data):
    delitos_2022 = data[data['anio'] == 2022]
    return delitos_2022[delitos_2022['codigo_delito_snic_id'].isin(['5', '13', '15', '19', '30'])]

def agrupar_delitos_2022(delitos_filtrados):
    delitos_agrupados = delitos_filtrados.groupby('codigo_delito_snic_nombre')['cantidad_hechos'].sum().reset_index()
    return delitos_agrupados.sort_values(by='cantidad_hechos', ascending=True)

def calcular_victimas_totales(data):
    victimas_totales = {
        'Femeninas': data['cantidad_victimas_fem'].sum(),
        'Masculinas': data['cantidad_victimas_masc'].sum(),
        'Sin definir / no binario': data['cantidad_victimas'].sum() - data['cantidad_victimas_fem'].sum() - data['cantidad_victimas_masc'].sum()
    }
    return victimas_totales
