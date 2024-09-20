import pandas as pd
from numpy import nan
import datetime
import openpyxl as opx
def get_user(excel):
    df_param = pd.read_excel(excel, sheet_name="Parametres")
    df_param.set_index("Index", inplace=True)
    dict_user = {df_param.loc["Code", user]: df_param.loc["Prenom", user] for user in df_param.columns if user != 'Index'}

    return df_param, dict_user

def add_nul(df, start, end):
    tous_les_mois = pd.period_range(start, end, freq='M')
    categories = df['Catégorie'].unique()

    # Produit cartésien des mois et catégories pour ajouter les montants nuls
    mois_cat_complet = pd.MultiIndex.from_product([tous_les_mois, categories], names=['MA', 'Catégorie'])

    # Reindexer pour inclure toutes les combinaisons et remplir les montants manquants par 0
    df_complet = df.set_index(['MA', 'Catégorie']).reindex(mois_cat_complet, fill_value=0).reset_index()
    return df_complet



def clean_dep(lien_excel, dict_users,):
    # Récupération des datas dans le excel
    data_dep = pd.read_excel(lien_excel, sheet_name='Suivi dépenses')
    # Récupération des données utilisateurs
    users = [user for _, user in dict_users.items()]
    # Tri des colonnes inutiles et des lignes vides
    df_dep = data_dep.copy()
    df_dep = df_dep.drop(df_dep.columns[6:], axis=1)
    df_dep.dropna(axis=0, how='any', inplace=True)
    # On arrondi les montants
    df_dep["Montant"] = df_dep["Montant"].round(2)
    # On remplace les codes payeurs par les vrais prénoms
    df_dep["Payeur"] = df_dep["Payeur"].map(dict_users)
    #Création de la colonne periode

    df_dep["Date"] = pd.to_datetime(df_dep["Date"])
    df_dep["MA"] = df_dep["Date"].dt.to_period('M')



    # Calcul des dépenses réelles et des dettes en fonction du Partage pour chaque user
    df_dep.loc[df_dep['Payeur'] == users[0], f"Depenses_{users[0]}"] = round(df_dep.Montant * (1 - df_dep.Partage), 2)
    df_dep.loc[df_dep['Payeur'] == users[1], f"Depenses_{users[0]}"] = round(df_dep.Montant * df_dep.Partage, 2)
    df_dep.loc[df_dep['Payeur'] == users[1], f"Depenses_{users[1]}"] = round(df_dep.Montant * (1 - df_dep.Partage), 2)
    df_dep.loc[df_dep['Payeur'] == users[0], f"Depenses_{users[1]}"] = round(df_dep.Montant * df_dep.Partage, 2)
    df_dep.loc[df_dep["Payeur"] == users[1], f"Dette_a_{users[1]}"] = round(df_dep.Montant * df_dep.Partage, 2)
    df_dep.loc[df_dep["Payeur"] == users[0], f"Dette_a_{users[0]}"] = round(df_dep.Montant * df_dep.Partage, 2)
    df_dep.replace(to_replace=nan, value=0, inplace=True)

    # Création des df dépense de chaque user
    dict_df_dep = {"total": df_dep,}
    for user in users:
        df_dep_user = df_dep.loc[df_dep[f"Depenses_{user}"] != 0]
        dict_df_dep[f"{user}"] = df_dep_user


    return dict_df_dep


def clean_rev(lien_excel, dict_users,):
    # Récupération des datas dans le excel
    data_rev = pd.read_excel(lien_excel, sheet_name='Suivi revenus')
    # Récupération des données utilisateurs
    users = [user for _, user in dict_users.items()]
    # Tri des colonnes inutiles et des lignes vides
    df_rev = data_rev.copy()
    df_rev = df_rev.loc[:, df_rev.columns[:5]]
    df_rev.dropna(axis=0, how='any', inplace=True)
    # On arrondie les montants
    df_rev["Montant"] = df_rev["Montant"].round(2)
    # On remplace les codes receveurs par les vrais prénoms
    df_rev["Receveur"] = df_rev["Receveur"].map(dict_users)  # On remplace les codes payeurs par les vrais prénoms
    #Création de la colonne periode
    df_rev["MA"] = df_rev["Date"].dt.to_period('M')
    dict_df_rev = {"total": df_rev, }
    for user in users:
        dict_df_rev[f"{user}"] = df_rev.loc[df_rev[f"Receveur"] == user]

    return dict_df_rev

def calc_epar_user(df_dep_user, df_rev_user, user):
    df_dep = df_dep_user.copy()
    df_rev = df_rev_user.copy()
    # CAlcul des dépenses et revenus sur les mois
    df_dep_month = df_dep.loc[:,["MA", f"Depenses_{user}"]].groupby(["MA"], as_index=False).sum()
    df_rev_month = df_rev.loc[:,["MA", f"Montant"]].groupby(["MA"], as_index=False).sum()
    df_glob_month = pd.merge(left=df_dep_month, right=df_rev_month, on="MA", how="outer",)
    # On remplace les valeurs manquantes par des 0
    df_glob_month.replace(to_replace=nan, value=0, inplace=True)
    # On renomme les colonnes
    df_glob_month.columns = ["MA", f"Depenses_{user}", f"Revenus_{user}"]
    df_glob_month[f"Epargne_{user}"] = df_glob_month[f"Revenus_{user}"] - df_glob_month[f"Depenses_{user}"]
    df_glob_month[f"Taux_epar_{user}"] = df_glob_month[f"Epargne_{user}"] / df_glob_month[f"Revenus_{user}"]
    df_glob_month[f"Epargne_{user}_cumul"] = df_glob_month[f"Epargne_{user}"].cumsum()
    df_glob_month[f"Depenses_{user}_cumul"] = df_glob_month[f"Depenses_{user}"].cumsum()
    df_glob_month[f"Revenus_{user}_cumul"] = df_glob_month[f"Revenus_{user}"].cumsum()


    return df_glob_month





