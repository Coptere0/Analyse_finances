import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import get_data as gd
from plotly.subplots import make_subplots

def create_pie_dep(dict_df_dep, user, mois, annee):
    # Récupération du Dataframe dépenses propre à l'utilisateur
    df_dep_user = dict_df_dep.get(user)
    # Création du DF des dépenses moyennes
    df_dep_user_mean = df_dep_user.groupby(["Catégorie"])[f"Depenses_{user}"].mean().round(0)

    graph = px.pie(
        df_dep_user.loc[(df_dep_user["Date"].dt.month == mois) &
                        (df_dep_user[f"Depenses_{user}"] != 0.0) &
                        (df_dep_user["Date"].dt.year == annee)][
            [f'Depenses_{user}', 'Catégorie']].groupby('Catégorie', as_index=False)[f'Depenses_{user}'].sum().round(),
        values=f'Depenses_{user}',
        names='Catégorie',
        hole=0.5,
        height=440,
        )
    graph.update_layout(
        legend=dict(
            orientation="h",
            xref="container",
            xanchor="center",
            x=0.5,
            yref="container",
            yanchor="bottom",
            y=0,
            bordercolor="rgba(0,0,0,0)",
            borderwidth=1,
            bgcolor="rgba(0,0,0,0)",
            entrywidthmode="pixels",
            entrywidth=0
        ),
        margin=dict(l=20, r=20, t=20, b=20
        ),
        autosize=True,
        paper_bgcolor="rgba(2, 7, 111, 0.26)"
    )
    graph.update_traces(
        textposition='inside',
        texttemplate="%{percent:.2p}",
        textfont=dict(size=14),
        automargin=True,
    )

    return st.plotly_chart(graph, use_container_width=True)

def create_pie_rev(dict_df_rev, user, mois, annee):
    # Récupération du Dataframe revenus propre à l'utilisateur
    df_rev_user = dict_df_rev.get(user)
    graph = px.pie(
        df_rev_user.loc[(df_rev_user["Date"].dt.month == mois) &
                        (df_rev_user[f"Montant"] != 0.0) &
                        (df_rev_user["Date"].dt.year == annee)][
            [f'Montant', 'Catégorie']].groupby('Catégorie', as_index=False)[f'Montant'].sum().round(),
        values=f'Montant',
        names='Catégorie',
        hole=0.5,
        height=440,
    )

    graph.update_layout(
        legend=dict(
            orientation="h",
            xref="container",
            xanchor="center",
            x=0.5,
            yref="container",
            yanchor="bottom",
            y=0,
            bordercolor="rgba(0,0,0,0)",
            borderwidth=1,
            bgcolor="rgba(0,0,0,0)",
            entrywidthmode="pixels",
            entrywidth=0
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
        paper_bgcolor="rgba(2, 7, 111, 0.26)"
    )
    graph.update_traces(
        textposition='inside',
        texttemplate="%{percent:.2p}",
        textfont=dict(size=14),
        automargin=True,
    )
    return st.plotly_chart(graph, use_container_width=True)

def create_bar_mois(dict_df_dep, dict_df_rev, user, mois, annee):
    # Récupération du Dataframe  propre à l'utilisateur
    df_dep_user = dict_df_dep.get(user)
    df_rev_user = dict_df_rev.get(user)

    dep_mois = df_dep_user.loc[(df_dep_user["Date"].dt.month == mois) &
                        (df_dep_user[f"Depenses_{user}"] != 0.0) &
                        (df_dep_user["Date"].dt.year == annee)][f'Depenses_{user}'].sum().round()

    rev_mois = df_rev_user.loc[(df_rev_user["Date"].dt.month == mois) &
                        (df_rev_user[f"Montant"] != 0.0) &
                        (df_rev_user["Date"].dt.year == annee)][f'Montant'].sum().round()

    epar_mois = round(rev_mois - dep_mois,2)

    df_mois = pd.DataFrame({"x": ["Depenses", "Revenus", "Epargne"], "y": [dep_mois, rev_mois, epar_mois]})

    graph = px.bar(df_mois, y="y", x="x",
                      text="y", labels={"x": "", "y": ""},
                      height=440)
    graph.update_xaxes(visible=True, tickfont=dict(size=15))
    graph.update_yaxes(visible=False)

    graph.update_traces(textposition='outside', textfont_size=15, textangle=0, cliponaxis=False, texttemplate="%{y:.2f}€")


    graph.update_layout(paper_bgcolor="rgba(8, 13, 159, 0.14)",
                           plot_bgcolor="rgba(8, 13, 159, 0)",
                           )

    return st.plotly_chart(graph, use_container_width=True)

def create_bar_dep(dict_df_dep, user, mois, annee):
    # Récupération du Dataframe  propre à l'utilisateur
    df_dep_user = dict_df_dep.get(user)

    dep_mois = df_dep_user.loc[(df_dep_user["Date"].dt.month == mois) &
                               (df_dep_user[f"Depenses_{user}"] != 0.0) &
                               (df_dep_user["Date"].dt.year == annee),[f'Depenses_{user}', 'Catégorie']].groupby('Catégorie', as_index=False)[f'Depenses_{user}'].sum().round()

    graph = go.Figure()
    graph.add_trace(go.Bar(x=dep_mois['Catégorie'], y=dep_mois[f'Depenses_{user}'],
                              name="Dépenses du mois"))

    graph.update_layout(
        paper_bgcolor="rgba(2, 7, 111, 0.26)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        height=400,
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            yref="container",
            y=0.95,
            xanchor="center",
            xref="container",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    graph.update_traces(textposition='outside',
                           textfont_size=11,
                           textangle=90,
                           cliponaxis=False,
                            )

    return st.plotly_chart(graph, use_container_width=True, use_container_height=False)

def create_bar_rev(dict_df_rev, user, mois, annee):
    # Récupération du Dataframe  propre à l'utilisateur
    df_rev_user = dict_df_rev.get(user)
    rev_mois = df_rev_user.loc[(df_rev_user["Date"].dt.month == mois) &
                               (df_rev_user[f"Montant"] != 0.0) &
                               (df_rev_user["Date"].dt.year == annee),[f'Montant', 'Catégorie']].groupby('Catégorie', as_index=False)[f'Montant'].sum().round()

    graph = go.Figure()
    graph.add_trace(go.Bar(x=rev_mois['Catégorie'], y=rev_mois[f'Montant'],
                              name="Revenus du mois"))
    graph.update_layout(
        paper_bgcolor="rgba(2, 7, 111, 0.26)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        height=400,
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            yref="container",
            y=0.95,
            xanchor="center",
            xref="container",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    graph.update_traces(textposition='outside',
                           textfont_size=11,
                           textangle=90,
                           cliponaxis=False,
                           )
    return st.plotly_chart(graph, use_container_width=True, use_container_height=True)

def create_line_dep(dict_df_dep, user, start, end):
    df_dep_user = dict_df_dep.get(user).copy()
    df_dep_user["Date"] = pd.to_datetime(df_dep_user["Date"]).dt.date

    mask = (df_dep_user["MA"] >= start) & (df_dep_user["MA"] <= end)
    df = df_dep_user.loc[mask,["Catégorie", "MA", f"Depenses_{user}"]].groupby(["MA"], as_index=False).sum()
    df["MA"] = df["MA"].astype(str)

    graph = px.line(df, x='MA', y=f'Depenses_{user}',
                       title=f"Dépenses totales :",
                       labels={'MA': '', f'Depenses_{user}': 'Dépenses mensuelles (€)'}, markers=True, height=300, )

    graph.update_layout(paper_bgcolor="rgba(8, 13, 159, 0.14)",
                        plot_bgcolor="rgba(8, 13, 159, 0)",
                        legend_bgcolor="rgba(8, 13, 159, 0)",
                        yaxis=dict(range=[-50, df[f'Depenses_{user}'].max()+100])
                        )

    return st.plotly_chart(graph, use_container_width=True, use_container_height=True)

def create_line_rev(dict_df_rev, user, start, end):
    df_rev_user = dict_df_rev.get(user).copy()
    df_rev_user["Date"] = pd.to_datetime(df_rev_user["Date"]).dt.date
    mask = (df_rev_user["MA"] >= start) & (df_rev_user["MA"] <= end)
    df = df_rev_user.loc[mask,["Catégorie", "MA", f"Montant"]].groupby(["MA"], as_index=False).sum()
    df["MA"] = df["MA"].astype(str)

    graph = px.line(df, x='MA', y=f'Montant',
                       title=f"Revenus totaux :",
                       labels={'MA': '', "Montant": 'Revenus mensuels (€)'}, markers=True, height=300, )

    graph.update_layout(paper_bgcolor="rgba(8, 13, 159, 0.14)",
                        plot_bgcolor="rgba(8, 13, 159, 0)",
                        legend_bgcolor="rgba(8, 13, 159, 0)",
                        yaxis=dict(range=[-50, df['Montant'].max()+500])
                        )

    return st.plotly_chart(graph, use_container_width=True, use_container_height=True)


def create_line_dep_cat(dict_df_dep, user, start, end, cat):
    df_dep_user = dict_df_dep.get(user).copy()
    df_dep_user["Date"] = pd.to_datetime(df_dep_user["Date"]).dt.date
    mask = (df_dep_user["MA"] >= start) & (df_dep_user["MA"] <= end) & (df_dep_user["Catégorie"].isin(cat))
    df = df_dep_user.loc[mask,["Catégorie", "MA", f"Depenses_{user}"]]
    df = df.groupby(["Catégorie", "MA"], as_index=False).sum()
    df = gd.add_nul(df, start, end)
    df["MA"] = df["MA"].apply(lambda x: str(x))

    graph = px.line(df, x='MA', y=f'Depenses_{user}',
                       title=f"Dépenses totales par catégorie :",
                       labels={'MA': '', f'Depenses_{user}': 'Dépenses mensuelles (€)'}, markers=True, height=300,
                    color="Catégorie")

    graph.update_layout(paper_bgcolor="rgba(8, 13, 159, 0.14)",
                        plot_bgcolor="rgba(8, 13, 159, 0)",
                        legend_bgcolor="rgba(8, 13, 159, 0)",
                        yaxis=dict(range=[-50, df[f'Depenses_{user}'].max() + 100])
                        )

    return st.plotly_chart(graph, use_container_width=True, use_container_height=True)


def create_line_rev_cat(dict_df_rev, user, start, end, cat):
    df_dep_user = dict_df_rev.get(user).copy()
    df_dep_user["Date"] = pd.to_datetime(df_dep_user["Date"]).dt.date

    mask = (df_dep_user["MA"] >= start) & (df_dep_user["MA"] <= end) & (df_dep_user["Catégorie"].isin(cat))
    df = df_dep_user.loc[mask,["Catégorie", "MA", f"Montant"]].groupby(["Catégorie","MA"], as_index=False).sum()
    df = gd.add_nul(df, start, end)
    df["MA"] = df["MA"].astype(str)
    graph = px.line(df, x='MA', y=f'Montant',
                       title=f"Revenus totaux par catégories :",
                       labels={'MA': '', f'Montant': 'Revenus mensuels (€)'}, height=300, markers=True,
                    color="Catégorie")

    graph.update_layout(paper_bgcolor="rgba(8, 13, 159, 0.14)",
                        plot_bgcolor="rgba(8, 13, 159, 0)",
                        legend_bgcolor="rgba(8, 13, 159, 0)",
                        yaxis=dict(range=[-50, df[f'Montant'].max() + df[f'Montant'].mean()]),
                        )

    return st.plotly_chart(graph, use_container_width=True, use_container_height=True)

def create_line_epar(dict_df_dep, dict_df_rev, user, start, end):
    df_dep_user = dict_df_dep.get(user).copy()
    df_rev_user = dict_df_rev.get(user).copy()
    df = gd.calc_epar_user(df_dep_user, df_rev_user, user)
    df["MA"] = df["MA"].apply(lambda x: str(x))
    graph = go.Figure()
    graph.add_scatter( x=df["MA"], y=df[f"Depenses_{user}"], name="Dépenses",)
    graph.add_scatter( x=df["MA"], y=df[f"Revenus_{user}"], name="Revenus")
    graph.update_traces(line_width=1, line=dict(dash='dot',))
    graph.add_scatter(x=df["MA"], y=df[f"Epargne_{user}"], name="Epargne")

    graph.update_layout(paper_bgcolor="rgba(8, 13, 159, 0.14)", plot_bgcolor="rgba(8, 13, 159, 0)",
                        legend_bgcolor="rgba(8, 13, 159, 0)",
                        yaxis=dict(zeroline=True, zerolinewidth=0.01, zerolinecolor='grey', ),
                        title="Evolution de l'épargne mensuelle"
                        )

    graph.update_legends()

    return st.plotly_chart(graph, use_container_width=True, use_container_height=True)


def create_line_epar_cumul(dict_df_dep, dict_df_rev, user, start, end):
    df_dep_user = dict_df_dep.get(user).copy()
    df_rev_user = dict_df_rev.get(user).copy()
    df = gd.calc_epar_user(df_dep_user, df_rev_user, user)
    df["MA"] = df["MA"].apply(lambda x: str(x))
    graph = go.Figure()
    graph.add_scatter( x=df["MA"], y=df[f"Depenses_{user}_cumul"], name="Dépenses cumulées",)
    graph.add_scatter( x=df["MA"], y=df[f"Revenus_{user}_cumul"], name="Revenus cumulés")
    graph.update_traces(line_width=1, line=dict(dash='dot',))
    graph.add_scatter(x=df["MA"], y=df[f"Epargne_{user}_cumul"], name="Epargne cumulée")

    graph.update_layout(paper_bgcolor="rgba(8, 13, 159, 0.14)", plot_bgcolor="rgba(8, 13, 159, 0)",
                        legend_bgcolor="rgba(8, 13, 159, 0)",
                        yaxis=dict(zeroline=True, zerolinewidth=0.01, zerolinecolor='grey', ),
                        title="Evolution de l'épargne mensuelle cumullée"
                        )

    graph.update_legends()

    return st.plotly_chart(graph, use_container_width=True, use_container_height=True)

def create_line_tau_epar(dict_df_dep, dict_df_rev, user, start, end):
    df_dep_user = dict_df_dep.get(user).copy()
    df_rev_user = dict_df_rev.get(user).copy()
    df = gd.calc_epar_user(df_dep_user, df_rev_user, user)
    df["MA"] = df["MA"].apply(lambda x: str(x))
    df["Taux_mean"] = df[f"Taux_epar_{user}"].rolling(window=3).mean()
    graph = go.Figure()
    graph.add_bar( x=df["MA"], y=df[f"Taux_epar_{user}"], name="Taux mensuel")
    graph.add_scatter(x=df["MA"], y=df[f"Taux_mean"], name="Taux moyen sur 3 mois", mode="lines")

    graph.update_layout(paper_bgcolor="rgba(8, 13, 159, 0.14)", plot_bgcolor="rgba(8, 13, 159, 0)",
                        legend_bgcolor="rgba(8, 13, 159, 0)",
                        yaxis=dict(zeroline=True, zerolinewidth=0.01, zerolinecolor='grey', ),
                        title="Evolution du taux d'épargne"
                        )

    return st.plotly_chart(graph, use_container_width=True, use_container_height=True)