import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
import numpy as np

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

# Configuration initiale
largeur_initial = 200  # en mm
longueur_initial = 200  # en mm
m_f_initial = 100  # Masse des fibres initiale en g
V_f_initial = 0.6  # Taux volumique de fibres initial
rho_f_initial = 1780  # Densité des fibres initiale en kg/m³
rho_m_initial = 1200  # Densité de la résine initiale en kg/m³

# Données pour le tracé
V_f_values = np.linspace(0.3, 0.7, 100)

# Création du graphique principal
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.6)

A_initial = (largeur_initial * longueur_initial) / 1e6  # Surface en m²
e_values = [calcul_epaisseur(m_f_initial / 1000, A_initial, V_f, rho_f_initial) for V_f in V_f_values]
l, = plt.plot(V_f_values, e_values, label="Épaisseur (mm)")
point, = plt.plot(V_f_initial, calcul_epaisseur(m_f_initial / 1000, A_initial, V_f_initial, rho_f_initial), 'ro', label="Valeur actuelle")
text = ax.text(V_f_initial, calcul_epaisseur(m_f_initial / 1000, A_initial, V_f_initial, rho_f_initial) + 0.2, 
               f"{calcul_epaisseur(m_f_initial / 1000, A_initial, V_f_initial, rho_f_initial):.2f} mm", color="red", fontsize=10)
plt.xlabel("Fraction volumique de fibres (V_f)")
plt.ylabel("Épaisseur (mm)")
plt.title("Variation de l'épaisseur en fonction du taux de fibres")
plt.ylim(0, 6)
plt.legend()
plt.grid(True)

# Curseurs
ax_largeur = plt.axes([0.2, 0.5, 0.65, 0.03], facecolor="lightgray")
slider_largeur = Slider(ax_largeur, "Largeur (mm)", 10, 500, valinit=largeur_initial)

ax_longueur = plt.axes([0.2, 0.45, 0.65, 0.03], facecolor="lightgray")
slider_longueur = Slider(ax_longueur, "Longueur (mm)", 10, 500, valinit=longueur_initial)

ax_m_f = plt.axes([0.2, 0.4, 0.65, 0.03], facecolor="lightgray")
slider_m_f = Slider(ax_m_f, "Masse fibres (g)", 10, 1000, valinit=m_f_initial)

ax_rho_f = plt.axes([0.2, 0.35, 0.65, 0.03], facecolor="lightgray")
slider_rho_f = Slider(ax_rho_f, "Densité renfort (kg/m³)", 1000, 2500, valinit=rho_f_initial)

ax_vf = plt.axes([0.2, 0.3, 0.65, 0.03], facecolor="lightgray")
slider_vf = Slider(ax_vf, "Taux de fibres (V_f)", 0.3, 0.7, valinit=V_f_initial, valstep=0.01)

# Curseur pour la densité de la matrice
ax_rho_m = plt.axes([0.2, 0.25, 0.65, 0.03], facecolor="lightgray")
slider_rho_m = Slider(ax_rho_m, "Densité matrice (kg/m³)", 800, 1500, valinit=rho_m_initial, valstep=1)

# Zone pour afficher la masse de résine nécessaire
ax_resine = plt.axes([0.2, 0.1, 0.65, 0.1], facecolor="white")
text_resine = TextBox(ax_resine, "Masse résine nécessaire (g):", initial=f"{calcul_resine(m_f_initial / 1000, V_f_initial, rho_f_initial, rho_m_initial):.2f}")

# Fonction de mise à jour
def update(val):
    largeur = slider_largeur.val
    longueur = slider_longueur.val
    m_f = slider_m_f.val
    V_f = slider_vf.val
    rho_f = slider_rho_f.val
    rho_m = slider_rho_m.val
    A = (largeur * longueur) / 1e6  # Surface en m²

    # Recalculer les valeurs d'épaisseur
    e_values = [calcul_epaisseur(m_f / 1000, A, vf, rho_f) for vf in V_f_values]
    l.set_ydata(e_values)

    # Mettre à jour le point rouge et le texte en fonction du curseur V_f
    e_current = calcul_epaisseur(m_f / 1000, A, V_f, rho_f)
    point.set_data([V_f], [e_current])
    text.set_position((V_f, e_current + 0.2))
    text.set_text(f"{e_current:.2f} mm")

    # Mettre à jour la masse de résine nécessaire
    m_resine = calcul_resine(m_f / 1000, V_f, rho_f, rho_m)
    text_resine.set_val(f"{m_resine:.2f}")

    fig.canvas.draw_idle()

# Liaison des curseurs à la fonction
slider_largeur.on_changed(update)
slider_longueur.on_changed(update)
slider_m_f.on_changed(update)
slider_rho_f.on_changed(update)
slider_vf.on_changed(update)
slider_rho_m.on_changed(update)

plt.show()

