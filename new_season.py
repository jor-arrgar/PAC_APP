import streamlit as st
from pandas.io.parsers import read_csv
import pandas as pd
import plotly.graph_objects as go

from global_var import *



def set_exploitation_df():
        
    try:
        exploitation_df = st.session_state.exploitation_df
        
    except:
        
        uploaded_file = st.sidebar.file_uploader(file_uploading , type='.csv')
        if uploaded_file is not None:
            exploitation_df = read_csv(uploaded_file , sep=';')
            st.session_state.exploitation_df = exploitation_df

    try: 
        return exploitation_df

    except(NameError):
        st.warning('SIN DATOS')
        st.stop()


def check_for_last_season(exploitation_df):
    exploitation_in_kernel = True
    st.write(type(exploitation_df))
    try:
        last_season = int(exploitation_df.columns[2:][-1])
        st.write('taking value from columns')
    except(IndexError):
            last_season = 1999
            st.write('setting 1999')

    except(NameError):
        exploitation_in_kernel = False
        last_season = None
        st.write('No expl')
        
    return exploitation_in_kernel , last_season


    

    
def get_season_columns(exploitation_df , season):
    
    columns_to_take = ['PARCELA' , 'SUPERFICIE']
    
    try:
        test = exploitation_df[str(season-1)] 
        try:
            test = exploitation_df[str(season-2)] 
            try:
                test = exploitation_df[str(season-3)] 
                columns_to_take += [str(season-3) , str(season-2) , str(season-1)]
            except:
                columns_to_take += [str(season-2) , str(season-1)]
        except:
            columns_to_take += [str(season-1)]
    except:
        pass 
    
    return columns_to_take

def season_pie_chart(crops , superficie):
    

    df = pd.DataFrame()
    df['SUPERFICIE'] = superficie
    df['CULTIVO'] = crops
    
    crops_surface_df = df.groupby('CULTIVO').sum()


    fig = go.Figure(data=[go.Pie(labels=crops_surface_df.index, values=crops_surface_df['SUPERFICIE'],
                                textinfo='percent',
                                insidetextorientation='radial'
                                )])
    fig.update_layout(width=300 , height=300)
    
    return fig , crops_surface_df.sort_values('SUPERFICIE' , ascending=False)

def check_for_diversification(crops_df):
    
    surface_sum = sum(crops_df['SUPERFICIE'])
    main_crop = crops_df.values[0] / surface_sum
    try:
        secondary_crop = crops_df.values[1] / surface_sum
    except(IndexError):
        secondary_crop = 0
    
    upgradring_crops = [crop for crop in crops_df.index if crop in up_crops]
    legumes = [crop for crop in crops_df.index if crop in leguminous_crops]
    
    if  len(legumes) == 0:
        return False , 'no legumes'
    
    elif main_crop > 0.7:
        return False , 'main crop'
    
    elif main_crop + secondary_crop > 0.9:
        return False , 'main + second'
    
    else:
        return True , ''
    
    