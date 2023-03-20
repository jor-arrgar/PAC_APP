import pandas as pd
import numpy as np
from random import shuffle
from pathlib import Path
from time import sleep


class PACDistributionError(Exception):
    def __init__(self, error_message):
        if error_message:
            self.message = error_message
        else:
            self.type_ = None
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Undefined PACDistributionError error raised'
        
        
        
def mensaje_instrucciones_añadir_parcelas():
    print('''Introduzca los nombres y la superficie de sus parcelas (en hectáreas) en el siguiente formato:
              
    parcela , superficie (indiferente a mayus y minus)
    
En caso de que se quiera utilizar el mismo nombre para varias parcelas, use el siguiente formato:

    parcela_1*, superficie
    parcela_2*, superficie
    
    * Se recomienda utilizar el número de la parcela en el registro catastral como sufijo
    
Para acceder al conjunto de ellas, basta con introducir el nombre general de la parcela (sin "_1"), y el programa automaticamente 
detectará el resto de parcelas asociadas al mismo nombre

Si el nombre se compone de dos o más palabras (por ejemplo, "campo alto"), es necesario utilizar el separador "."\
    (por ejemplo, "campo.alto")''')
    
    
    
def introducir_parcelas():
    tierras = {}
    while True:
        info = input('Introduzca la información de la parcela ("salir" para finalizar): ')
        
        if info.lower() == 'salir':
            break
        
        try:
            info = info.replace(' ' , '')
            info = info.split(',')
            
            tierras[info[0]] = float(info[1])
            
        except:
            print('==>  Introduzca los datos en el formato correcto\n')
            
    return tierras



def generar_df_desde_diccionario_parcelas(parcelas_dict):
    names_series = pd.Series(parcelas_dict.keys())
    surface_series = pd.Series(parcelas_dict.values())

    df = pd.DataFrame({'name':names_series, 'surface':surface_series})
    
    return df


def proceder_con_proceso(input_message):
    while True:
        create = input(input_message)

        if create.lower() == 's':
            return  True

        elif create.lower() == 'n':
            return  False

        else:
            print('==> Opción no válida, por favor introduzca "s" o "n"')
            
            
            
csv_path = [str(path) for path in (Path('.').glob('*.csv'))]

if len(csv_path) > 1:
    print('Se han encontrado varios archivos csv en la carpeta actual, por favor, elimine los que no sean necesarios, \
        deje solo el archivo con el resgistro historico de cultivos y vuelva a ejecutar el programa\n')
    print('··· El programa se cerrará en 10 segundos ···')
    sleep(10)
    
    raise PACDistributionError('Multiple csv files found in the current directory, only one is allowed')



try:
    df_historic = pd.read_csv(csv_path[0], sep=';')
    
    print('Parcelas registradas\n' , len(df_historic))
    
    add = proceder_con_proceso('¿Desea añadir más parcelas al registro histórico? (s/n): ')
           
            
    if add:
        mensaje_instrucciones_añadir_parcelas()
        
        nuevas_parcelas_dict = introducir_parcelas()
        nuevas_parcelas_df = generar_df_desde_diccionario_parcelas(nuevas_parcelas_dict)
        print(nuevas_parcelas_df)
        
        df_historic = pd.concat([df_historic, nuevas_parcelas_df], ignore_index=True)
        
    print('Parcelas para este año: ')
    print(df_historic)
    
        
    
except:
    print('No se ha encontrado el archivo csv con los registros históricos\n------------------')
    
    generate_new = proceder_con_proceso('¿Desea crear un archivo csv con los registros históricos desde cero? (s/n): ')
            
            
    if generate_new:
        mensaje_instrucciones_añadir_parcelas()
        
        parcelas_dict = introducir_parcelas()
        parcelas_df = generar_df_desde_diccionario_parcelas(parcelas_dict)
        print(parcelas_df)
        
    else:
        print('Por favor, introduzca el archivo csv con los registros históricos en la misma carpeta que la aplicación\
y vuelva a ejecutar el programa\n')