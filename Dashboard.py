import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Tabac France - Analyse Stratégique",
    page_icon="🚭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #8B0000, #FF6B6B, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        padding: 1rem;
    }
    .section-header {
        color: #8B0000;
        border-bottom: 3px solid #FF6B6B;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-size: 1.8rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #8B0000 0%, #FF6B6B 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .impact-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
    .impact-health { border-left-color: #dc3545; background-color: rgba(220, 53, 69, 0.1); }
    .impact-economic { border-left-color: #28a745; background-color: rgba(40, 167, 69, 0.1); }
    .impact-social { border-left-color: #ffc107; background-color: rgba(255, 193, 7, 0.1); }
    .policy-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .policy-prevention { border-left-color: #28a745; background-color: rgba(40, 167, 69, 0.1); }
    .policy-tax { border-left-color: #007bff; background-color: rgba(0, 123, 255, 0.1); }
    .policy-regulation { border-left-color: #6f42c1; background-color: rgba(111, 66, 193, 0.1); }
    .policy-ban { border-left-color: #dc3545; background-color: rgba(220, 53, 69, 0.1); }
</style>
""", unsafe_allow_html=True)

class TobaccoDashboard:
    def __init__(self):
        self.historical_data = self.initialize_historical_data()
        self.policy_timeline = self.initialize_policy_timeline()
        self.regional_data = self.initialize_regional_data()
        self.international_comparison = self.initialize_international_comparison()
        self.health_impact_data = self.initialize_health_impact_data()
        
    def initialize_historical_data(self):
        """Initialise les données historiques de la consommation de tabac"""
        years = list(range(2000, 2024))
        
        # Données simulées basées sur les tendances historiques réelles
        smoking_prevalence = [
            34.5, 33.8, 33.2, 32.5, 31.8, 31.2, 30.5, 29.9, 29.3, 28.7,  # 2000-2009
            28.1, 27.5, 26.9, 26.3, 25.7, 25.1, 24.5, 24.0, 23.4, 22.9,  # 2010-2019
            22.4, 21.9, 21.4, 20.9  # 2020-2023
        ]
        
        daily_smokers = [
            28.9, 28.3, 27.7, 27.1, 26.5, 25.9, 25.3, 24.8, 24.2, 23.7,  # 2000-2009
            23.2, 22.7, 22.2, 21.7, 21.2, 20.7, 20.2, 19.8, 19.3, 18.9,  # 2010-2019
            18.5, 18.1, 17.7, 17.3  # 2020-2023
        ]
        
        cigarette_consumption = [
            95.2, 92.8, 90.5, 88.2, 86.0, 83.8, 81.7, 79.6, 77.6, 75.6,  # 2000-2009 (milliards)
            73.7, 71.8, 70.0, 68.2, 66.5, 64.8, 63.2, 61.6, 60.1, 58.6,  # 2010-2019
            57.1, 55.7, 54.3, 52.9  # 2020-2023
        ]
        
        average_price = [
            4.20, 4.50, 4.80, 5.10, 5.40, 5.70, 6.00, 6.30, 6.60, 6.90,  # 2000-2009 (€/paquet)
            7.20, 7.50, 7.80, 8.10, 8.40, 8.70, 9.00, 9.50, 10.0, 10.5,  # 2010-2019
            11.0, 11.5, 12.0, 12.5  # 2020-2023
        ]
        
        tax_revenue = [
            10.2, 10.5, 10.8, 11.1, 11.4, 11.7, 12.0, 12.3, 12.6, 12.9,  # 2000-2009 (milliards €)
            13.2, 13.5, 13.8, 14.1, 14.4, 14.7, 15.0, 15.3, 15.6, 15.9,  # 2010-2019
            16.2, 16.5, 16.8, 17.1  # 2020-2023
        ]
        
        return pd.DataFrame({
            'annee': years,
            'prevalence_tabagisme': smoking_prevalence,
            'fumeurs_quotidiens': daily_smokers,
            'consommation_cigarettes': cigarette_consumption,
            'prix_moyen': average_price,
            'recettes_fiscales': tax_revenue
        })
    
    def initialize_policy_timeline(self):
        """Initialise la timeline des politiques anti-tabac"""
        return [
            {'date': '1991-01-01', 'type': 'regulation', 'titre': 'Loi Évin', 
             'description': 'Interdiction de fumer dans les lieux publics et publicité'},
            {'date': '2003-01-01', 'type': 'tax', 'titre': 'Augmentation des taxes', 
             'description': 'Hausse significative du prix du tabac'},
            {'date': '2007-02-01', 'type': 'ban', 'titre': 'Interdiction totale lieux publics', 
             'description': 'Extension de l\'interdiction aux bars, restaurants, hôtels'},
            {'date': '2010-01-01', 'type': 'prevention', 'titre': 'Campagne choc Moi(s) sans tabac', 
             'description': 'Lancement des campagnes nationales de prévention'},
            {'date': '2014-05-20', 'type': 'regulation', 'titre': 'Paquet neutre', 
             'description': 'Loi imposant le paquet de cigarettes neutre'},
            {'date': '2016-01-01', 'type': 'regulation', 'titre': 'Application paquet neutre', 
             'description': 'Mise en œuvre effective du paquet neutre'},
            {'date': '2018-03-01', 'type': 'tax', 'titre': 'Augmentation progressive', 
             'description': 'Programme de hausses annuelles des prix'},
            {'date': '2020-01-01', 'type': 'prevention', 'titre': 'Remboursement substituts nicotiniques', 
             'description': 'Prise en charge à 100% par l\'Assurance Maladie'},
            {'date': '2021-11-01', 'type': 'regulation', 'titre': 'Interdiction arômes', 
             'description': 'Interdiction des cigarettes électroniques aromatisées'},
            {'date': '2023-01-01', 'type': 'tax', 'titre': 'Nouvelle hausse des prix', 
             'description': 'Objectif: paquet à 13€ d\'ici 2027'},
        ]
    
    def initialize_regional_data(self):
        """Initialise les données régionales de consommation"""
        regions = [
            'Île-de-France', 'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 
            'Occitanie', 'Hauts-de-France', 'Provence-Alpes-Côte d\'Azur',
            'Pays de la Loire', 'Bretagne', 'Normandie', 'Grand Est',
            'Bourgogne-Franche-Comté', 'Centre-Val de Loire', 'Corse'
        ]
        
        data = {
            'region': regions,
            'prevalence_2023': [18.5, 22.1, 21.8, 23.2, 25.6, 20.9, 19.7, 18.2, 22.4, 24.1, 22.8, 21.3, 26.7],
            'evolution_2010_2023': [-6.2, -5.8, -5.5, -6.1, -4.9, -5.7, -6.3, -6.8, -5.4, -5.1, -5.6, -5.9, -4.2],
            'fumeurs_quotidiens': [15.2, 18.4, 18.1, 19.3, 21.8, 17.2, 16.1, 14.9, 18.7, 20.2, 18.9, 17.6, 22.5],
            'tabagisme_passif': [12.3, 15.6, 14.9, 16.2, 18.7, 13.8, 12.9, 11.7, 15.4, 17.1, 15.8, 14.3, 19.2]
        }
        
        return pd.DataFrame(data)
    
    def initialize_international_comparison(self):
        """Initialise les données comparatives internationales"""
        countries = ['France', 'Allemagne', 'Royaume-Uni', 'Espagne', 'Italie', 'États-Unis', 'Australie', 'Japon']
        
        data = {
            'pays': countries,
            'prevalence_tabagisme': [20.9, 22.3, 14.1, 24.5, 20.6, 14.0, 11.8, 17.8],
            'prix_paquet_eur': [12.5, 8.0, 15.2, 5.2, 5.8, 9.5, 21.3, 4.8],
            'mortalite_liee_tabac': [75, 121, 78, 52, 83, 480, 21, 130],  # milliers
            'depenses_prevention': [0.8, 0.5, 1.2, 0.3, 0.4, 1.5, 2.1, 0.6],  # € par habitant
            'interdiction_publicite': [1, 0, 1, 1, 1, 0, 1, 0]  # 1 = oui, 0 = non
        }
        
        return pd.DataFrame(data)
    
    def initialize_health_impact_data(self):
        """Initialise les données d'impact sur la santé"""
        years = list(range(2010, 2024))
        
        data = {
            'annee': years,
            'deces_tabac': [73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60],  # milliers
            'cancers_poumon': [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44],  # milliers
            'maladies_cardiovasculaires': [25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12],  # milliers
            'couts_sante': [26.5, 26.8, 27.1, 27.4, 27.7, 28.0, 28.3, 28.6, 28.9, 29.2, 29.5, 29.8, 30.1, 30.4],  # milliards €
            'annees_vie_perdues': [1.8, 1.75, 1.7, 1.65, 1.6, 1.55, 1.5, 1.45, 1.4, 1.35, 1.3, 1.25, 1.2, 1.15]  # millions
        }
        
        return pd.DataFrame(data)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown(
            '<h1 class="main-header">🚭 DASHBOARD STRATÉGIQUE - TABAC EN FRANCE</h1>', 
            unsafe_allow_html=True
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div style="text-align: center; background: linear-gradient(45deg, #8B0000, #FF6B6B); '
                'color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">'
                '<h3>📊 ANALYSE DE LA CONSOMMATION, POLITIQUES ET IMPACTS SANITAIRES</h3>'
                '</div>', 
                unsafe_allow_html=True
            )
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés du tabac en France"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS DU TABAC EN FRANCE</h3>', 
                   unsafe_allow_html=True)
        
        current_data = self.historical_data[self.historical_data['annee'] == 2023].iloc[0]
        previous_data = self.historical_data[self.historical_data['annee'] == 2022].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Prévalence Tabagisme",
                f"{current_data['prevalence_tabagisme']:.1f}%",
                f"{(current_data['prevalence_tabagisme'] - previous_data['prevalence_tabagisme']):+.1f}% vs 2022",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Fumeurs Quotidiens",
                f"{current_data['fumeurs_quotidiens']:.1f}%",
                f"{(current_data['fumeurs_quotidiens'] - previous_data['fumeurs_quotidiens']):+.1f}% vs 2022",
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                "Prix Moyen du Paquet",
                f"{current_data['prix_moyen']:.1f}€",
                f"{(current_data['prix_moyen'] - previous_data['prix_moyen']):+.1f}€ vs 2022"
            )
        
        with col4:
            st.metric(
                "Recettes Fiscales",
                f"{current_data['recettes_fiscales']:.1f}Md€",
                f"{(current_data['recettes_fiscales'] - previous_data['recettes_fiscales']):+.1f}Md€ vs 2022"
            )
    
    def create_historical_analysis(self):
        """Crée l'analyse historique de la consommation"""
        st.markdown('<h3 class="section-header">📈 ÉVOLUTION HISTORIQUE DE LA CONSOMMATION</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Prévalence", "Consommation & Prix", "Impact Santé"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution de la prévalence
                fig = px.line(self.historical_data, 
                             x='annee', 
                             y='prevalence_tabagisme',
                             title='Évolution de la Prévalence du Tabagisme (%) - 2000-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Prévalence (%)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Fumeurs quotidiens vs occasionnels
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=self.historical_data['annee'], 
                                       y=self.historical_data['fumeurs_quotidiens'],
                                       name='Fumeurs quotidiens',
                                       line=dict(color='red')))
                
                occasionnels = self.historical_data['prevalence_tabagisme'] - self.historical_data['fumeurs_quotidiens']
                fig.add_trace(go.Scatter(x=self.historical_data['annee'], 
                                       y=occasionnels,
                                       name='Fumeurs occasionnels',
                                       line=dict(color='orange')))
                
                fig.update_layout(title='Répartition Fumeurs Quotidiens vs Occasionnels',
                                yaxis_title="Pourcentage (%)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Consommation de cigarettes
                fig = px.line(self.historical_data, 
                             x='annee', 
                             y='consommation_cigarettes',
                             title='Consommation de Cigarettes (milliards) - 2000-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Milliards de cigarettes", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Prix vs consommation (double axe)
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Scatter(x=self.historical_data['annee'], 
                             y=self.historical_data['prix_moyen'],
                             name="Prix moyen (€)",
                             line=dict(color='green')),
                    secondary_y=False,
                )
                
                fig.add_trace(
                    go.Scatter(x=self.historical_data['annee'], 
                             y=self.historical_data['consommation_cigarettes'],
                             name="Consommation (milliards)",
                             line=dict(color='red')),
                    secondary_y=True,
                )
                
                fig.update_layout(title='Relation Prix vs Consommation')
                fig.update_yaxes(title_text="Prix moyen (€)", secondary_y=False)
                fig.update_yaxes(title_text="Consommation (milliards)", secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Impact sur la santé
                fig = px.line(self.health_impact_data, 
                             x='annee', 
                             y=['deces_tabac', 'cancers_poumon', 'maladies_cardiovasculaires'],
                             title='Mortalité Liée au Tabac (milliers) - 2010-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Nombre de décès (milliers)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Coûts sanitaires
                fig = px.area(self.health_impact_data, 
                             x='annee', 
                             y='couts_sante',
                             title='Coûts Sanitaires Liés au Tabac (milliards €) - 2010-2023')
                fig.update_layout(yaxis_title="Coûts (milliards €)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
    
    def create_policy_analysis(self):
        """Analyse des politiques anti-tabac"""
        st.markdown('<h3 class="section-header">🏛️ ANALYSE DES POLITIQUES ANTI-TABAC</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Timeline des Politiques", "Impact des Mesures", "Efficacité Comparée"])
        
        with tab1:
            # Timeline interactive des politiques
            policy_df = pd.DataFrame(self.policy_timeline)
            policy_df['date'] = pd.to_datetime(policy_df['date'])
            policy_df['annee'] = policy_df['date'].dt.year
            
            # Fusion avec données historiques
            merged_data = pd.merge(self.historical_data, policy_df, on='annee', how='left')
            
            fig = px.scatter(merged_data, 
                           x='annee', 
                           y='prevalence_tabagisme',
                           color='type',
                           size_max=20,
                           hover_name='titre',
                           hover_data={'description': True, 'type': True},
                           title='Impact des Politiques sur la Prévalence du Tabagisme')
            
            # Ajouter la ligne de tendance
            fig.add_trace(go.Scatter(x=self.historical_data['annee'], 
                                   y=self.historical_data['prevalence_tabagisme'],
                                   mode='lines',
                                   name='Prévalence tabagisme',
                                   line=dict(color='gray', width=2)))
            
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Légende des types de politiques
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="policy-card policy-prevention">Prévention</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="policy-card policy-tax">Fiscalité</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="policy-card policy-regulation">Réglementation</div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="policy-card policy-ban">Interdiction</div>', unsafe_allow_html=True)
        
        with tab2:
            # Analyse d'impact des politiques majeures
            st.subheader("Impact des Politiques Clés")
            
            impact_analysis = [
                {'politique': 'Loi Évin (1991)', 'impact_prevalence': -3.2, 'delai_impact': 2},
                {'politique': 'Interdiction lieux publics (2007)', 'impact_prevalence': -2.8, 'delai_impact': 1},
                {'politique': 'Paquet neutre (2016)', 'impact_prevalence': -1.5, 'delai_impact': 2},
                {'politique': 'Hausse prix 2018-2023', 'impact_prevalence': -4.2, 'delai_impact': 3},
                {'politique': 'Remboursement substituts (2020)', 'impact_prevalence': -0.8, 'delai_impact': 1},
            ]
            
            impact_df = pd.DataFrame(impact_analysis)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(impact_df, 
                            x='politique', 
                            y='impact_prevalence',
                            title='Impact sur la Prévalence Tabagique (points de %)',
                            color='impact_prevalence',
                            color_continuous_scale='RdYlGn')
                fig.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # CORRECTION : Utiliser la valeur absolue pour la taille
                impact_df['impact_absolu'] = impact_df['impact_prevalence'].abs()
                
                fig = px.scatter(impact_df, 
                               x='delai_impact', 
                               y='impact_prevalence',
                               size='impact_absolu',  # Utiliser les valeurs absolues
                               color='politique',
                               hover_name='politique',
                               title='Délai vs Amplitude des Impacts',
                               size_max=30)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Efficacité comparée des politiques
            st.subheader("Efficacité des Différentes Stratégies")
            
            strategies = [
                {'strategie': 'Augmentation des prix', 'efficacite': 9.2, 'cout': 2, 'acceptabilite': 5},
                {'strategie': 'Interdiction publicité', 'efficacite': 7.8, 'cout': 1, 'acceptabilite': 8},
                {'strategie': 'Paquet neutre', 'efficacite': 6.5, 'cout': 1, 'acceptabilite': 6},
                {'strategie': 'Interdiction lieux publics', 'efficacite': 8.4, 'cout': 3, 'acceptabilite': 7},
                {'strategie': 'Campagnes prévention', 'efficacite': 6.2, 'cout': 4, 'acceptabilite': 9},
                {'strategie': 'Aides au sevrage', 'efficacite': 7.1, 'cout': 5, 'acceptabilite': 9},
            ]
            
            strategy_df = pd.DataFrame(strategies)
            
            fig = px.scatter(strategy_df, 
                           x='cout', 
                           y='efficacite',
                           size='acceptabilite',
                           color='strategie',
                           hover_name='strategie',
                           title='Efficacité vs Coût des Stratégies',
                           size_max=30)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_regional_analysis(self):
        """Analyse des disparités régionales"""
        st.markdown('<h3 class="section-header">🗺️ ANALYSE RÉGIONALE ET DÉMOGRAPHIQUE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Cartographie", "Disparités Régionales", "Analyse Démographique"])
        
        with tab1:
            # CORRECTION : Remplacer la carte choroplèthe par une carte scatter_geo
            st.subheader("Prévalence du Tabagisme par Région")
            
            # Ajouter des coordonnées approximatives pour chaque région
            regional_coords = {
                'Île-de-France': {'lat': 48.8566, 'lon': 2.3522},
                'Auvergne-Rhône-Alpes': {'lat': 45.75, 'lon': 4.85},
                'Nouvelle-Aquitaine': {'lat': 44.8378, 'lon': -0.5792},
                'Occitanie': {'lat': 43.6, 'lon': 1.4333},
                'Hauts-de-France': {'lat': 50.6292, 'lon': 3.0573},
                'Provence-Alpes-Côte d\'Azur': {'lat': 43.3, 'lon': 5.37},
                'Pays de la Loire': {'lat': 47.2181, 'lon': -1.5528},
                'Bretagne': {'lat': 48.1173, 'lon': -1.6778},
                'Normandie': {'lat': 49.18, 'lon': -0.37},
                'Grand Est': {'lat': 48.5734, 'lon': 7.7521},
                'Bourgogne-Franche-Comté': {'lat': 47.24, 'lon': 6.02},
                'Centre-Val de Loire': {'lat': 47.9, 'lon': 1.9},
                'Corse': {'lat': 42.15, 'lon': 9.08}
            }
            
            # Créer un DataFrame avec les coordonnées
            coords_df = pd.DataFrame.from_dict(regional_coords, orient='index').reset_index()
            coords_df.columns = ['region', 'lat', 'lon']
            
            # Fusionner avec les données régionales
            regional_with_coords = pd.merge(self.regional_data, coords_df, on='region')
            
            # Créer une carte scatter_geo
            fig = px.scatter_geo(regional_with_coords,
                                lat='lat',
                                lon='lon',
                                color='prevalence_2023',
                                size='prevalence_2023',
                                hover_name='region',
                                hover_data={'prevalence_2023': True, 'evolution_2010_2023': True},
                                title='Prévalence du Tabagisme par Région - 2023',
                                color_continuous_scale='RdYlGn_r')
            
            # Ajuster la vue sur la France
            fig.update_geos(
                visible=False,
                resolution=50,
                scope='europe',
                showcountries=True,
                countrycolor="Black",
                showsubunits=True,
                subunitcolor="Blue",
                lonaxis_range=[-5, 10],
                lataxis_range=[40, 52]
            )
            
            fig.update_layout(
                geo=dict(
                    bgcolor='rgba(0,0,0,0)',
                    lakecolor='#0E1117',
                    landcolor='#0E1117'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Classement des régions
                fig = px.bar(self.regional_data.sort_values('prevalence_2023'), 
                            x='prevalence_2023', 
                            y='region',
                            orientation='h',
                            title='Prévalence du Tabagisme par Région - 2023',
                            color='prevalence_2023',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Évolution régionale
                fig = px.bar(self.regional_data.sort_values('evolution_2010_2023'), 
                            x='evolution_2010_2023', 
                            y='region',
                            orientation='h',
                            title='Évolution de la Prévalence 2010-2023 (points de %)',
                            color='evolution_2010_2023',
                            color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Analyse par catégories socio-démographiques
            st.subheader("Profil des Fumeurs")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 👥 Par Catégorie Socio-professionnelle
                
                **Taux les plus élevés:**
                • Ouvriers: 28.5%  
                • Employés: 24.2%  
                • Chômeurs: 32.1%  
                
                **Taux les plus bas:**
                • Cadres: 15.8%  
                • Professions intermédiaires: 18.9%  
                • Retraités: 12.4%  
                """)
            
            with col2:
                st.markdown("""
                ### 🎂 Par Tranche d'Âge
                
                **15-24 ans:** 21.8%  
                **25-34 ans:** 26.4%  
                **35-44 ans:** 23.9%  
                **45-54 ans:** 21.2%  
                **55-64 ans:** 16.7%  
                **65+ ans:** 8.9%  
                
                **Âge moyen d'initiation:** 14.2 ans
                """)
    
    def create_international_comparison(self):
        """Analyse comparative internationale"""
        st.markdown('<h3 class="section-header">🌍 COMPARAISON INTERNATIONALE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Prévalence", "Politiques", "Performances"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Prévalence comparée
                fig = px.bar(self.international_comparison.sort_values('prevalence_tabagisme'), 
                            x='pays', 
                            y='prevalence_tabagisme',
                            title='Prévalence du Tabagisme - Comparaison Internationale',
                            color='prevalence_tabagisme',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Prix vs prévalence
                fig = px.scatter(self.international_comparison, 
                               x='prix_paquet_eur', 
                               y='prevalence_tabagisme',
                               size='mortalite_liee_tabac',
                               color='pays',
                               hover_name='pays',
                               title='Relation Prix vs Prévalence',
                               size_max=30)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Comparaison des politiques
            st.subheader("Stratégies Nationales de Lutte Anti-Tabac")
            
            policy_comparison = [
                {'pays': 'France', 'paquet_neutre': 1, 'interdiction_pub': 1, 'prix_eleve': 1, 'remboursement_aides': 1},
                {'pays': 'Australie', 'paquet_neutre': 1, 'interdiction_pub': 1, 'prix_eleve': 1, 'remboursement_aides': 1},
                {'pays': 'Royaume-Uni', 'paquet_neutre': 1, 'interdiction_pub': 1, 'prix_eleve': 1, 'remboursement_aides': 1},
                {'pays': 'Allemagne', 'paquet_neutre': 0, 'interdiction_pub': 0, 'prix_eleve': 0, 'remboursement_aides': 0},
                {'pays': 'États-Unis', 'paquet_neutre': 0, 'interdiction_pub': 0, 'prix_eleve': 0, 'remboursement_aides': 0},
            ]
            
            policy_df = pd.DataFrame(policy_comparison)
            
            fig = px.imshow(policy_df.set_index('pays'),
                          title='Comparaison des Politiques Anti-Tabac',
                          color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Performance des stratégies
            st.subheader("Performance des Stratégies Nationales")
            
            performance_data = [
                {'pays': 'Australie', 'reduction_10ans': -8.2, 'investissement_prevention': 2.1, 'classement': 1},
                {'pays': 'Royaume-Uni', 'reduction_10ans': -6.9, 'investissement_prevention': 1.2, 'classement': 2},
                {'pays': 'France', 'reduction_10ans': -5.8, 'investissement_prevention': 0.8, 'classement': 3},
                {'pays': 'Canada', 'reduction_10ans': -5.2, 'investissement_prevention': 1.5, 'classement': 4},
                {'pays': 'États-Unis', 'reduction_10ans': -3.1, 'investissement_prevention': 1.5, 'classement': 5},
                {'pays': 'Allemagne', 'reduction_10ans': -2.8, 'investissement_prevention': 0.5, 'classement': 6},
            ]
            
            perf_df = pd.DataFrame(performance_data)
            
            # CORRECTION : Utiliser une colonne positive pour la taille
            perf_df['reduction_absolue'] = perf_df['reduction_10ans'].abs()
            
            fig = px.scatter(perf_df, 
                           x='investissement_prevention', 
                           y='reduction_10ans',
                           size='reduction_absolue',  # Utiliser les valeurs absolues
                           color='pays',
                           hover_name='pays',
                           title='Investissement vs Réduction de la Prévalence',
                           size_max=30)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_strategic_recommendations(self):
        """Recommandations stratégiques"""
        st.markdown('<h3 class="section-header">🎯 RECOMMANDATIONS STRATÉGIQUES</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Objectifs 2030", "Stratégies Prioritaires", "Feuille de Route"])
        
        with tab1:
            st.subheader("Objectifs Nationaux 2030")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                ### 🎯 Objectif Principal
                
                **Génération sans tabac d'ici 2030**
                
                • Prévalence < 5%  
                • 200 000 fumeurs en moins par an  
                • Prévention dès le plus jeune âge  
                """)
            
            with col2:
                st.markdown("""
                ### 📊 Cibles Intermédiaires
                
                **2025:**
                • Prévalence < 15%  
                • Paquet à 13€  
                • 100% de couverture des aides  
                
                **2027:**
                • Prévalence < 10%  
                • Paquet à 15€  
                • Espace sans tabac généralisé  
                """)
            
            with col3:
                st.markdown("""
                ### 📈 Indicateurs de Suivi
                
                • Prévalence mensuelle  
                • Ventes de tabac  
                • Utilisation des aides  
                • Exposition des jeunes  
                • Inégalités sociales  
                """)
        
        with tab2:
            st.subheader("Stratégies Prioritaires")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🚨 Actions Immédiates (2024-2025)
                
                **1. Augmentation des prix**
                • Objectif: paquet à 13€ en 2025  
                • Hausse progressive mais significative  
                
                **2. Renforcement de la prévention**
                • Campagnes choc renouvelées  
                • Ciblage des populations vulnérables  
                
                **3. Amélioration de l'accès aux aides**
                • Simplification des démarches  
                • Formation des professionnels  
                """)
            
            with col2:
                st.markdown("""
                ### 🏗️ Réformes Structurelles (2026-2030)
                
                **1. Généralisation des espaces sans tabac**
                • Parcs, plages, abribus  
                • Périmètres autour des écoles  
                
                **2. Régulation des nouveaux produits**
                • Cigarettes électroniques  
                • Produits du tabac chauffé  
                
                **3. Lutte contre le commerce illicite**
                • Renforcement des contrôles  
                • Collaboration internationale  
                """)
        
        with tab3:
            st.subheader("Feuille de Route Détaillée")
            
            roadmap = [
                {'periode': '2024', 'actions': ['Hausse prix à 12€', 'Campagne jeunes', 'Extension espaces sans tabac']},
                {'periode': '2025', 'actions': ['Paquet à 13€', 'Généralisation paquet neutre', 'Formation médecins']},
                {'periode': '2026-2027', 'actions': ['Nouvelle hausse prix', 'Interdiction arômes menthol', 'Renforcement contrôles']},
                {'periode': '2028-2030', 'actions': ['Objectif 5% prévalence', 'Évaluation stratégique', 'Adaptation politiques']},
            ]
            
            for step in roadmap:
                with st.expander(f"📅 {step['periode']}"):
                    for action in step['actions']:
                        st.write(f"• {action}")
            
            # Graphique de projection
            years_projection = list(range(2020, 2031))
            prevalence_projection = [21.4, 20.9, 19.5, 18.0, 16.5, 15.0, 13.5, 11.0, 8.5, 6.0, 5.0]
            
            fig = px.line(x=years_projection, y=prevalence_projection,
                         title='Projection de la Prévalence du Tabagisme 2020-2030',
                         markers=True)
            fig.add_hrect(y0=0, y1=5, line_width=0, fillcolor="green", opacity=0.2,
                         annotation_text="Objectif 2030")
            fig.update_layout(yaxis_title="Prévalence (%)", xaxis_title="Année")
            st.plotly_chart(fig, use_container_width=True)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Période d'analyse
        st.sidebar.markdown("### 📅 Période d'analyse")
        annee_debut = st.sidebar.selectbox("Année de début", 
                                         list(range(2000, 2024)), 
                                         index=0)
        annee_fin = st.sidebar.selectbox("Année de fin", 
                                       list(range(2000, 2024)), 
                                       index=23)
        
        # Focus d'analyse
        st.sidebar.markdown("### 🎯 Focus d'analyse")
        focus_analysis = st.sidebar.multiselect(
            "Domaines à approfondir:",
            ['Prévalence', 'Politiques', 'Impact santé', 'Disparités régionales', 'Comparaisons internationales'],
            default=['Prévalence', 'Politiques']
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=False)
        
        # Bouton d'export
        if st.sidebar.button("📊 Exporter l'analyse"):
            st.sidebar.success("Export réalisé avec succès!")
        
        return {
            'annee_debut': annee_debut,
            'annee_fin': annee_fin,
            'focus_analysis': focus_analysis,
            'show_projections': show_projections,
            'auto_refresh': auto_refresh
        }
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Historique", 
            "🏛️ Politiques", 
            "🗺️ Régional", 
            "🌍 International", 
            "🎯 Stratégies",
            "💡 Synthèse"
        ])
        
        with tab1:
            self.create_historical_analysis()
        
        with tab2:
            self.create_policy_analysis()
        
        with tab3:
            self.create_regional_analysis()
        
        with tab4:
            self.create_international_comparison()
        
        with tab5:
            self.create_strategic_recommendations()
        
        with tab6:
            st.markdown("## 💡 SYNTHÈSE STRATÉGIQUE")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### ✅ SUCCÈS ET PROGRÈS
                
                **Baisse continue depuis 20 ans:**
                • Prévalence divisée par 1.5  
                • Paquet neutre généralisé  
                • Interdictions efficaces  
                • Prise de conscience collective  
                
                **Politiques efficaces:**
                • Hausse des prix  
                • Interdiction publicité  
                • Espaces sans tabac  
                • Campagnes choc  
                """)
            
            with col2:
                st.markdown("""
                ### ⚠️ DÉFIS PERSISTANTS
                
                **Inégalités sociales:**
                • Écart ouvriers/cadres: 12 points  
                • Territorialité marquée  
                • Jeunes vulnérables  
                
                **Nouveaux enjeux:**
                • Cigarettes électroniques  
                • Commerce illicite  
                • Industrie du tabac adaptative  
                • Produits nouveaux  
                """)
            
            st.markdown("""
            ### 🚨 ALERTES ET RECOMMANDATIONS
            
            **Niveau d'Alerte: MODÉRÉ**
            
            **Points de Vigilance:**
            • Stagnation possible de la baisse  
            • Résistance des populations vulnérables  
            • Nouveaux produits attractifs pour les jeunes  
            • Commerce parallèle croissant  
            
            **Recommandations Immédiates:**
            1. Accélération des hausses de prix  
            2. Renforcement de la prévention jeune  
            3. Lutte contre les inégalités sociales  
            4. Régulation des nouveaux produits  
            5. Coordination européenne renforcée  
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(300)
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = TobaccoDashboard()
    dashboard.run_dashboard()