import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Fonction pour calculer l'épaisseur
def calcul_epaisseur(m_f, A, V_f, rho_f):
    V_fibres = m_f / rho_f  # volume des fibres en m³
    V_total = V_fibres / V_f  # volume total en m³
    e = V_total / A  # épaisseur en m
    e_mm = e * 1000  # conversion en mm
    return e_mm

# Fonction pour calculer la quantité de résine nécessaire
def calcul_resine(m_f, V_f, rho_f, rho_m):
    V_fibres = m_f / rho_f  # volume des fibres en m³
    V_total = V_fibres / V_f  # volume total en m³
    V_resine = V_total * (1 - V_f)  # volume de résine en m³
    m_resine = V_resine * rho_m  # masse de résine en kg
    return m_resine * 1000  # conversion en g

# Titre de l'application
st.title("Calcul de l'épaisseur et de la résine nécessaire")

# Curseurs pour ajuster les paramètres
largeur = st.slider("Largeur (mm)", 10, 500, 200)
longueur = st.slider("Longueur (mm)", 10, 500, 200)
m_f = st.slider("Masse fibres (g)", 10, 1000, 100)
V_f = st.slider("Fraction volumique de fibres (V_f)", 0.3, 0.7, 0.6, step=0.01)
rho_f = st.slider("Densité des fibres (kg/m³)", 1000, 2500, 1780)
rho_m = st.slider("Densité de la matrice (kg/m³)", 800, 1500, 1200)

# Calculs
A = (largeur * longueur) / 1e6  # Surface en m²
épaisseur = calcul_epaisseur(m_f / 1000, A, V_f, rho_f)
masse_resine = calcul_resine(m_f / 1000, V_f, rho_f, rho_m)

# Affichage des résultats
st.write(f"### Épaisseur calculée : {épaisseur:.2f} mm")
st.write(f"### Masse de résine nécessaire : {masse_resine:.2f} g")

# Graphique interactif
V_f_values = np.linspace(0.3, 0.7, 100)
épaisseur_values = [calcul_epaisseur(m_f / 1000, A, vf, rho_f) for vf in V_f_values]

fig, ax = plt.subplots()
ax.plot(V_f_values, épaisseur_values, label="Épaisseur (mm)")
ax.scatter(V_f, épaisseur, color="red", label="Valeur actuelle")
ax.set_xlabel("Fraction volumique de fibres (V_f)")
ax.set_ylabel("Épaisseur (mm)")
ax.set_title("Variation de l'épaisseur en fonction de V_f")
ax.legend()
ax.grid(True)

# Affichage du graphique
st.pyplot(fig)
