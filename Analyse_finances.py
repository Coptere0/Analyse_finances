import pandas as pd
import streamlit as st
import datetime

import create_fig as cf
import get_data as gd

# Paramètres de la page streamlit
STREAMLIT_SERVER_ENABLE_STATIC_SERVING = True
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Analyse des finances")

# ---------------------------------------------------------------------------------------------------------------------#
#                                           Paramètres de l'arrière plan                                               #
# ---------------------------------------------------------------------------------------------------------------------#
# background-image: url("data:image/png;base64,{img}"); background: linear-gradient(158deg, rgba(2,0,36,1) 0%, rgba(82,23,135,1) 38%, rgba(0,212,255,1) 100%)
# Arrière plan
page_bg_img = f"""
<style>
[data-testid="stApp"] {{
#background: linear-gradient(158deg, rgba(2,0,36,1) 0%, rgba(82,23,135,1) 38%, rgba(0,212,255,1) 100%);
background-color: rgba(10,13,60,0.5);
background-position: top left;
background-repeat: no-repeat;
background-size: 100%;
background-attachment: scroll;
    }}
[data-testid="stHeader"] {{
background-color: rgba(0,0,0,0);
}}
}}
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------------#
#                                           Paramètres de la sidebar et du titre                                       #
# ---------------------------------------------------------------------------------------------------------------------#

with st.sidebar:
    st.title("Déposez le fichier Excel")
    doc = st.file_uploader("Déposer le fichier excel", type=['xlsx'], label_visibility="collapsed")
    _, dict_users = gd.get_user(doc)
    users = [user for _, user in dict_users.items()][0]
    param = st.expander("Paramètres")
    param.write(dict_users)

    #st.subheader("Utilisateur 1")
   # user_1 = st.text_input("Nom de l'utilisateur", "", key="user_1")
    #code_user_1 = st.text_input("Code de l'utilisateur (Excel)", "", key="code_user_1")
    #st.subheader("Utilisateur 2")
    #user_2 = st.text_input("Nom de l'utilisateur", "", key="user_2")
    #code_user_2 = st.text_input("Code de l'utilisateur (Excel)", "", key="code_user_2")
    #dict_users = {code_user_1: user_1, code_user_2: user_2}
    #st.text(dict_users)
col1, col2 = st.columns([6, 1],)
col1.title("Analyse des finances")
user = col2.selectbox("Utilisateur", dict_users.values(), placeholder="Utilisateur", index=None, label_visibility="collapsed"  )




#----------------------------------------------------------------------------------------------------------------------#
#                                           Récupération des datas                                                     #
# ---------------------------------------------------------------------------------------------------------------------#

# Récupération des paramètres

# Récupération des dépenses
dict_df_dep = gd.clean_dep(doc, dict_users) # Dict avec les différents DF depenses
df_dep_user = dict_df_dep.get(user)  # DF des dépenses de l'user choisit
#Récupération des revenus
dict_df_rev = gd.clean_rev(doc, dict_users) # Dict avec les différents DF revenus
df_rev_user = dict_df_rev.get(user)  # DF des revenus de l'user choisit
df_epar_user = gd.calc_epar_user(df_dep_user, df_rev_user, user)




#Récupération des investissement

# Plage de visualisation possible
plage_mois_user = df_dep_user["MA"].sort_values(ascending=False).unique()

#----------------------------------------------------------------------------------------------------------------------#
#                                           Paramètres des tabs                                                        #
# ---------------------------------------------------------------------------------------------------------------------#
tab_1, tab_2, tab_3 = st.tabs(["Dépenses et Revenus", "Epargne et investissement", "Livret de compte"], )


#----------------------------------------------------------------------------------------------------------------------#
#                                           Dépenses et Revenus                                                        #
# ---------------------------------------------------------------------------------------------------------------------#
with tab_1:
    tab_11, tab_12 = st.tabs(["Analyse mensuelle", "Analyse globale"])

    with tab_11:
        col_titre_mens, col_titre_mois, _ = st.columns([1.5, 1, 5],)
        col_titre_mens.subheader("Analyse mensuelle")
        period_pie = col_titre_mois.selectbox('Mois', plage_mois_user, label_visibility='collapsed', )
        col_cam_depenses, col_prop_depenses, col_cam_revenus = st.columns([1, 1, 1], )

        with col_cam_depenses:
            cf.create_pie_dep(dict_df_dep, user, period_pie.month, period_pie.year)
        with col_prop_depenses:
            cf.create_bar_mois(dict_df_dep, dict_df_rev, user, period_pie.month, period_pie.year)
        with col_cam_revenus:
            cf.create_pie_rev(dict_df_rev, user, period_pie.month, period_pie.year)
        col_bar_dep, col_bar_rev = st.columns([1, 1])
        with col_bar_dep:
            cf.create_bar_dep(dict_df_dep, user, period_pie.month, period_pie.year)
        with col_bar_rev:
            cf.create_bar_rev(dict_df_rev, user, period_pie.month, period_pie.year)

    with tab_12:
        col_glob1, col_glob2, col_glob3 = st.columns([1, 1, 1],)
        col_glob1.subheader("Analyse globale")
        start_glob = col_glob2.selectbox("Début de l'analyse", plage_mois_user[::-1], )

        end_glob = col_glob3.selectbox("Fin de l'analyse", plage_mois_user)
        col_glob_dep, col_glob_rev = st.columns([1, 1])

        with col_glob_dep:
            cf.create_line_dep(dict_df_dep, user, start=start_glob, end=end_glob)
            cat_dep = st.multiselect("Catégories :", df_dep_user["Catégorie"].sort_values(ascending=True, ).unique(),
                                     label_visibility='collapsed')
            cf.create_line_dep_cat(dict_df_dep, user, start=start_glob, end=end_glob, cat=cat_dep)

        with col_glob_rev:
            cf.create_line_rev(dict_df_rev, user, start_glob, end_glob)
            cat_dep = st.multiselect("Catégories :", df_rev_user["Catégorie"].sort_values(ascending=True, ).unique(),
                                     label_visibility='collapsed')
            cf.create_line_rev_cat(dict_df_rev, user, start_glob, end_glob, cat=cat_dep)


        #col_dep, col_rev = st.columns([1, 1],)


with tab_2:
    col1, col2, col3 = st.columns([1.5,1,1])
    with col1:
        cf.create_line_epar(dict_df_dep, dict_df_rev, user, start=start_glob, end=end_glob)
        with col2:
            cf.create_line_tau_epar(dict_df_dep, dict_df_rev, user, start=start_glob, end=end_glob)
    with col3:
        cf.create_line_epar_cumul(dict_df_dep, dict_df_rev, user, start=start_glob, end=end_glob)
with tab_3:
    df_dep_user.dtypes