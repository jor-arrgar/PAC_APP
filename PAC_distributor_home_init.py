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
        
############################################################################################################    
tierras = {'el briz':1.76,
           'el monte':0.46,
           'la torre':0.49,
           'langayo_71':1.74,
           'langayo_72':0.52,
           'langayo_76':0.86,
           'picacho_41':4.06,
           'picacho_57':4.03,
           'picaho_58':3.94,
           'crucillas_52':0.68,
           'crucillas_83':4.15,
           'crucillas_84':4.17,
           'crucillas_85':4.20,
           'crucillas_43':4.08,
           'molino':0.62,
           'yunta_57':2.98,
           'yunta_22':1.50,
           'cogeces_63':2.67,
           'cogeces_64':0.6,
           'moraleja_92':1.59,
           'moraleja_98':0.3,
           'moraleja_52':0.39,
           'apisquillos':0.07,
           'lancha_96':0.31,
           'lancha_27':0.29,
           'lancha_69':0.26,
           'lancha_72':0.2,
           'perosillo':0.3}


cultivos = ['trigo', 'cebada' , 'guisante']

tierras_manual = {'el briz':'trigo',
                  'el monte':'trigo',
                  'la torre':'trigo',
                  'langayo_71':'trigo',
                  'langayo_72':'trigo',
                  'picacho_41':'cebada',}


############################################################################################################


############################################################################################################

def get_crop_surface(lista_parcelas , superficie_total , prioridad , superficie_ocupada):
    crop_surface=superficie_ocupada
    parcelas_escogidas = []
    
    if prioridad == 0:
        valor_maximo = 0.7
        
    elif prioridad == 1:
        valor_maximo = 0.9
    
    
    while crop_surface/superficie_total < valor_maximo:
        
        parcela = lista_parcelas.pop(0)
        
        crop_surface += parcela[1]
        shuffle(lista_parcelas)
        parcelas_escogidas.append(parcela)
        
    
    parcela_devuelta = parcelas_escogidas.pop(-1)
    crop_surface -= parcela_devuelta[1]
    

    parcelas_sin_asignar = lista_parcelas+[parcela_devuelta]
    
    return crop_surface-superficie_ocupada , parcelas_escogidas , parcelas_sin_asignar




def generar_distribucion_aleatoria(tierras_dict , cultivos ,cultivos_manual, cultivos_manual_ordenados):
    while True:

        list_tierras = list(tierras_dict.keys())

        [list_tierras.remove(tierra) for tierra in cultivos_manual.keys()]
        tierras_for_mixin = list(zip(list_tierras , [tierras_dict.get(tierra) for tierra in list_tierras]))
        shuffle(tierras_for_mixin)
        
        print('---------------------------' , 'mixin' , '---------------------------')
        print(tierras_for_mixin)
        
        superficies_ocupadas = [cultivo_manual[2] for cultivo_manual in cultivos_manual_ordenados]
        superficie_ocupada = sum(superficies_ocupadas)
        
        superficie_total = sum(list(tierras_dict.values()))
        parcelas_repartidas = []
        
        for pos , cultivo in enumerate(cultivos):
            
            if pos != len(cultivos)-1:
                print('---------------------------' , pos , '---------------------------')
                print(tierras_for_mixin)
                crop_surface , parcelas , sin_asignar = get_crop_surface(tierras_for_mixin , superficie_total , pos , superficies_ocupadas[pos])
                
                superficie_ocupada += crop_surface
                tierras_for_mixin = sin_asignar
            else:
                parcelas = tierras_for_mixin            
                crop_surface = superficie_total - superficie_ocupada
            
            proporcion = crop_surface/superficie_total
            
            parcelas_repartidas.append([cultivo , crop_surface , proporcion , parcelas])
                
                
        #[print(cultivo) for cultivo in parcelas_repartidas]
        
        proportions = [cultivo[2] for cultivo in parcelas_repartidas]

        if all([prop > 0.1 for prop in proportions]):
            break
        
    return parcelas_repartidas


############################################################################################################

names_series = pd.Series(tierras.keys())
surface_series = pd.Series(tierras.values())

df_general = pd.DataFrame({'name':names_series, 'surface':surface_series}).set_index('name')

cultivos_manual = set(tierras_manual.values())
preference = [cultivos.index(cultivo) for cultivo in cultivos_manual]
superficie_manual_por_cultivos = []

for cultivo in cultivos_manual:
    superficie_por_cultivo = []
    for tierra, cultivo_tierra in tierras_manual.items():
        if cultivo == cultivo_tierra:
            superficie_por_cultivo.append(tierras[tierra])
    superficie_manual_por_cultivos.append(sum(superficie_por_cultivo))

cultivos_manual_ordenados = sorted(zip(preference , cultivos_manual, superficie_manual_por_cultivos), key=lambda x: x[0])
reparto = generar_distribucion_aleatoria(tierras , cultivos ,tierras_manual, cultivos_manual_ordenados)

[print(cultivo , '\n') for cultivo in reparto]


############################################################################################################

season_df = pd.DataFrame(columns = ['name' , 'year'])
for cultivo in reparto:
    crop_list = [cultivo[0]] * len(cultivo[3])
    field_list = [cultivo[3][i][0] for i in range(len(cultivo[3]))]
    
    df = pd.DataFrame({'name' : field_list , 'year' : crop_list})
    
    season_df = season_df.append(df)

season_df = season_df.set_index('name')

updated_df = pd.concat([df_general , season_df] , axis = 1)

updated_df.to_csv('crop_historical.csv' , sep=';')