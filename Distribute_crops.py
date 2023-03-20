import streamlit as st


from functions import *
from global_var import *

from create_exploitation import *
from new_season import *







# STREAMLIT SESSION STATES

st.session_state.mayus = False


if st.sidebar.checkbox('LETRAS MAYUSCULAS'):
    st.session_state.mayus = True

if st.session_state.mayus:
    crop_list = [crop.upper() for crop in crop_list]
    main_menu_option_list = [option.upper() for option in main_menu_option_list]
    
    field_input = field_input.upper()
    surface_input = surface_input.upper()
    no_field_warning = no_field_warning.upper()
    
    no_dataframe_loaded = no_dataframe_loaded.upper()



main_menu = st.sidebar.selectbox('Selecione opción' , tuple(main_menu_option_list))

if main_menu.lower() == 'bienvenido':
    st.header('DISTRIBUCION DE CULTIVOS BAJO NORMAS PAC (> 2023)')

    
elif main_menu.lower() == 'crear explotación':
    
    create_exploitation()
    generate_and_download_df()
    
        
        
elif main_menu.lower() == 'nueva temporada':

    st.header('Nueva temporada')
    
    exploitation_df= set_exploitation_df()
    
    try:
        last_season = st.session_state.last_season
        exploitation_in_kernel = True
    except(AttributeError):
        exploitation_in_kernel , last_season = check_for_last_season(exploitation_df)
    

    if exploitation_in_kernel:
        season = st.number_input('TEMPORADA' , last_season+1)
        
    
        
    columns_to_take = get_season_columns(exploitation_df , season)
    
    for pos , column in enumerate(st.columns([6 , 3 , 4 , 4 , 4 , 6 , 2])):
        try:
            col = columns_to_take[pos]
            if col == 'SUPERFICIE':
                col = 'HC'

            column.subheader(col)
            
        except(IndexError):

            if pos == 6:
                column.subheader('R')
            elif pos == 5:
                column.subheader(season)
            else:
                pass
    
    
    try:
        
        last_crops = set_default_crops(columns_to_take , exploitation_df , season)
            
        displaying_df = exploitation_df[columns_to_take]
        
        empty_spaces = [st.empty() for i in range(len(displaying_df))]
        
        crops = []
        for pos , value in enumerate(displaying_df.values):
            
            with empty_spaces[pos]:
            
                c1 , c2 , c3 , c4 , c5 , c6 , c7 = empty_spaces[pos].columns([6 , 3 , 4 , 4 , 4 , 6 , 2])
            
                display_centered_text('''
                                      
                                      {0}'''.format(value[0]) , c1)
                
                display_centered_text('''
                                      
                                      {0}'''.format(str(value[1])) , c2)
                
                
                try:
                    display_centered_text('''
                                      
                                      {0}'''.format(str(value[2])) , c3)
                    try:
                        display_centered_text('''
                                      
                                      {0}'''.format(str(value[3])) , c4)
                        try:
                            display_centered_text('''
                                      
                                      {0}'''.format(str(value[4])) , c5)
                        except(IndexError):
                            c5.write('---')
                    except(IndexError):
                        c4.write('---')
                        c5.write('---')
                except(IndexError):
                    c3.write('---')
                    c4.write('---')
                    c5.write('---')
                
                crop = set_crop_for_field(c6 , value[0] , last_crops[pos])
                crops.append(crop)
                
                rotation_check = check_for_rotation_requissite(value , crop)
                if rotation_check:
                    c7.image('https://raw.githubusercontent.com/jor-arrgar/PAC_APP/master/images/rectangle_green.png')
                else:
                    c7.image('https://raw.githubusercontent.com/jor-arrgar/PAC_APP/master/images/rectangle_red.png')
                
                
                
        fig , crops_surface_df = season_pie_chart(crops , displaying_df['SUPERFICIE'])
        
        diversification , error_type = check_for_diversification(crops_surface_df)
        if not diversification:
            st.sidebar.error('No cumple el requisito de diversificación por {0}'.format(error_type))
        
        st.sidebar.plotly_chart(fig)
        st.sidebar.table(crops_surface_df)
        
###################################################################################################

        if st.button('AÑADIR NUEVA TEMPORADA'):
            
            exploitation_df[str(season)] = crops
            st.session_state.exploitation_df = exploitation_df
            st.session_state.last_season = season
            st.experimental_rerun()

            
        exploitation_df_encoded = exploitation_df.to_csv(index=False , sep=';').encode('latin_1')
        
        
        exploitation_name = st.text_input('Nombre de archivo') + '.csv'
        if len(exploitation_name) > 0:
            st.download_button(download_updated_file , exploitation_df_encoded , exploitation_name , mime='text/plain')
        
        if st.checkbox('TABLA COMPLETA'):
            st.write(exploitation_df) 
        
    except(NameError):
        st.warning(no_dataframe_loaded)

        
    


    