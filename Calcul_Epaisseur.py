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

# Fonction pour calculer l'épaisseur à partir du grammage surfacique
def calcul_epaisseur_inverse(grammage, nb_plis, rho_f, V_f):
    """
    Calcule l'épaisseur d'un composite à partir du grammage surfacique, du nombre de plis,
    de la densité du renfort et du taux volumique des fibres.
    """
    # Conversion du grammage en masse de fibres par unité de surface (kg/m²)
    grammage_kg_m2 = grammage / 1000  # Conversion g/m² en kg/m²

    # Volume total du composite par unité de surface (m³/m²)
    V_total_per_m2 = (grammage_kg_m2 * nb_plis) / (rho_f * V_f)

    # Épaisseur totale du composite (en mm)
    e_mm = V_total_per_m2 * 1000  # Conversion m en mm
    return e_mm

# Titre de l'application
st.title("Détermination de l'épaisseur")

# Curseurs pour la première méthode
st.header("Méthode 1 : Épaisseur à partir de la masse de fibres")
largeur = st.slider("Largeur (mm)", 10, 1000, 200, key="largeur1")
longueur = st.slider("Longueur (mm)", 10, 1000, 200, key="longueur1")
m_f = st.slider("Masse fibres (g)", 10, 1000, 100, key="mf1")
V_f = st.slider("Fraction volumique de fibres (V_f)", 0.3, 0.7, 0.6, step=0.01, key="vf1")
rho_f = st.slider("Densité des fibres (kg/m³)", 1000, 2600, 1780, key="rhof1")
rho_m = st.slider("Densité de la matrice (kg/m³)", 800, 1500, 1200, key="rhom1")

# Calculs pour la première méthode
A = (largeur * longueur) / 1e6  # Surface en m²
épaisseur1 = calcul_epaisseur(m_f / 1000, A, V_f, rho_f)
masse_resine1 = calcul_resine(m_f / 1000, V_f, rho_f, rho_m)

# Affichage des résultats de la première méthode
st.write(f"### Épaisseur calculée : {épaisseur1:.2f} mm")
st.write(f"### Masse de résine nécessaire : {masse_resine1:.2f} g")

# Graphique interactif pour la première méthode
V_f_values = np.linspace(0.3, 0.7, 100)
épaisseur_values = [calcul_epaisseur(m_f / 1000, A, vf, rho_f) for vf in V_f_values]

fig1, ax1 = plt.subplots()
ax1.plot(V_f_values, épaisseur_values, label="Épaisseur (mm)")
ax1.scatter(V_f, épaisseur1, color="red", label="Valeur actuelle")
ax1.set_xlabel("Fraction volumique de fibres (V_f)")
ax1.set_ylabel("Épaisseur (mm)")
ax1.set_title("Variation de l'épaisseur en fonction de V_f")
ax1.legend()
ax1.grid(True)

# Affichage du graphique
st.pyplot(fig1)

# Séparation visuelle
st.write("---")

# Curseurs pour la seconde méthode
st.header("Méthode 2 : Épaisseur à partir du grammage surfacique")
grammage = st.slider("Grammage surfacique (g/m²)", 100, 2000, 300, key="grammage2")
nb_plis = st.slider("Nombre de plis", 1, 20, 5, key="nbplis2")
V_f2 = st.slider("Fraction volumique de fibres (V_f)", 0.3, 0.7, 0.6, step=0.01, key="vf2")
rho_f2 = st.slider("Densité des fibres (kg/m³)", 1000, 2600, 1780, key="rhof2")

# Calculs pour la seconde méthode
épaisseur2 = calcul_epaisseur_inverse(grammage, nb_plis, rho_f2, V_f2)

# Graphique interactif pour la seconde méthode
nb_plis_values = range(1, nb_plis + 5)  # Ajuste dynamiquement la plage des plis (+4 plis supplémentaires)
épaisseur_values2 = [calcul_epaisseur_inverse(grammage, n, rho_f2, V_f2) for n in nb_plis_values]

fig2, ax2 = plt.subplots()

# Tracé des valeurs de l'épaisseur (sans les points bleus)
ax2.plot(nb_plis_values, épaisseur_values2, label="Épaisseur (mm)", color="blue")

# Point rouge pour la valeur actuelle
ax2.scatter(nb_plis, épaisseur2, color="red", label="Valeur actuelle", zorder=5)

# Configuration des axes
ax2.set_xlabel("Nombre de plis")
ax2.set_ylabel("Épaisseur (mm)")
ax2.set_title("Variation de l'épaisseur en fonction du nombre de plis")

# Échelle dynamique pour les abscisses (ajout de 4 plis supplémentaires)
ax2.set_xticks(range(1, nb_plis + 5))  # Ticks de 1 au max + 4
ax2.set_xlim(1, nb_plis + 4)  # Limite dynamique de l'axe x

# Échelle des ordonnées : valeurs régulières 0, 0.5, 1, 1.5, ...
min_y = 0  # Forcer à commencer à 0
max_y = max(épaisseur_values2)
step = 0.5  # Pas fixe de 0.5
y_ticks = np.arange(min_y, max_y + step, step)
ax2.set_yticks(y_ticks)
ax2.set_ylim(min_y, max_y + step)  # Ajout d'une marge en haut

# Ajout de la légende et de la grille
ax2.legend()
ax2.grid(True)

# Affichage du texte de l'épaisseur au-dessus du graphique
st.write(f"### Épaisseur calculée pour {nb_plis} plis : {épaisseur2:.2f} mm")

# Affichage du graphique pour la seconde méthode
st.pyplot(fig2)

