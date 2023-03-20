import pandas as pd
import streamlit as st
from global_var import crop_list



def generar_df_desde_diccionario_parcelas(parcelas_dict):
    names_series = pd.Series(parcelas_dict.keys())
    surface_series = pd.Series(parcelas_dict.values())

    df = pd.DataFrame({'PARCELA':names_series, 'SUPERFICIE':surface_series})
    
    return df



def set_crop_for_field(st_column ,field , last_crop):
    crop = st_column.selectbox('' , tuple(crop_list) , index=crop_list.index(last_crop) , key=field)
    
    return crop

def set_default_crops(columns_to_take , exploitation_df , season):
    
    if len(columns_to_take)>2:

        last_crops = exploitation_df[str(season-1)]
        
    else:
        last_crops= ['Ajo']*len(exploitation_df)
        
    return last_crops

from streamlit.delta_generator import DeltaGenerator


def display_centered_text(text: str, container):
    
    container.markdown(
        f"<div style='text-align: center;'>{text}",
        unsafe_allow_html=True)


def check_for_rotation_requissite(field_df_index , actual_crop):
    
    if len(field_df_index) == 5:
        last_3_crops = field_df_index[-3:]
        
        if len(set(last_3_crops)) == 1 and list(set(last_3_crops))[0] == actual_crop:
            return False
        else:
            return True
    
    else:
        return True
    
    
