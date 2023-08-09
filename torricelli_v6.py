# Import Streamlit and Plotly
import streamlit as st
import plotly.graph_objects as go

# Keep the other imports
import numpy as np

# Initial parameters
h0 = 10  # initial height of the water (in meters)
g = 9.81  # acceleration due to gravity (in meters per second squared)

# Function that calculates the height of the water as a function of time
def altezza_acqua(t, A, a):
    h = np.sqrt(h0**2 - 2*g*a*t/A)
    h = np.maximum(h, 0)  # the height cannot be negative
    return h

# Function that calculates the trajectory of the water flow
def traiettoria_flusso(x, v):
    return - (g*x**2) / (2*v**2)

# Function that creates the plots
def plot_altezza_acqua(D, d, h_orifizio, T):
    """
    Questa funzione crea un grafico dell'altezza dell'acqua in un recipiente che si svuota attraverso un orifizio.

    Args:
        D: Il diametro del recipiente (m).
        d: Il diametro dell'orifizio (m).
        h_orifizio: L'altezza dell'orifizio (m).
        T: Il tempo massimo (s).

    Returns:
        None.
    """

    # Calculate the areas of the container and the orifice
    A = np.pi * (D/2)**2
    a = np.pi * (d/2)**2

    # Create an array of times and calculate the corresponding water height
    t = np.linspace(0, T, 1000)
    h_acqua = altezza_acqua(t, A, a)
    h_acqua_above_orifizio = np.maximum(h_acqua - h_orifizio, 0)

    # Calculate the exit velocity of the water
    v = np.sqrt(2*g*h_acqua_above_orifizio)

    # Calculate the time when the water reaches the ground and the maximum water range
    t_impact = np.sqrt(2*h_orifizio/g)
    gittata_max = v*t_impact

    # Calculate the flow rate of the orifice and the total liters contained in the container
    portata = a*v
    litri_totali = A*h0*1000

    # Display the results using Streamlit
    st.sidebar.markdown(f'**Velocità dell\'acqua:** {v[0]:.2f} m/s')
    st.sidebar.markdown(f'**Gittata massima:** {gittata_max[0]:.2f} m')
    st.sidebar.markdown(f'**Portata dell\'orifizio:** {portata[0]:.2f} m³/s')
    st.sidebar.markdown(f'**Litri totali contenuti nel recipiente:** {litri_totali:.2f} l')

    # Create the plot of the water height
    fig1 = go.Figure(data=go.Scatter(x=t, y=h_acqua_above_orifizio, mode='lines', hovertemplate='Tempo: %{x:.2f}s<br>Altezza: %{y:.2f}m'))
    fig1.update_layout(title='Altezza dell\'acqua sopra l\'orifizio in funzione del tempo', xaxis_title='Tempo (s)', yaxis_title='Altezza dell\'acqua sopra l\'orifizio (m)')
    st.plotly_chart(fig1)

    # Add the plot for the water range over time
    fig2 = go.Figure(data=go.Scatter(x=t, y=gittata_max, mode='lines', hovertemplate='Tempo: %{x:.2f}s<br>Gittata: %{y:.2f}m'))
    fig2.update_layout(title='Gittata dell\'acqua in funzione del tempo', xaxis_title='Tempo (s)', yaxis_title='Gittata dell\'acqua (m)')
    st.plotly_chart(fig2)

    # Create the plot of the container with the water and the outflow
    fig3 = go.Figure()
    fig3.add_shape(type="rect", x0=-1, y0=0, x1=0, y1=h0, line=dict(color="black"), fillcolor="blue", opacity=0.5)
    x_vals = np.linspace(0, gittata_max[0], 400)
    y_vals = h_orifizio + traiettoria_flusso(x_vals, v[0])
    fig3.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Traiettoria del flusso'))
    fig3.update_layout(title='Recipiente con flusso d\'acqua', xaxis_title='Distanza orizzontale (m)', yaxis_title='Altezza (m)', yaxis_range=[0, 10])
    st.plotly_chart(fig3)

    # Add the plots for the water trajectory at different times
    fig4 = go.Figure()

    # Percentuali desiderate
    percentuali = [1, 0.75, 0.5, 0.25]

    for perc in percentuali:
        # Calcolo diretto dell'altezza basata sulla percentuale
        h_attuale = h0 * perc
        
        # Se l'altezza attuale è sopra l'orifizio, calcola la traiettoria
        if h_attuale > h_orifizio:
            v_attuale = np.sqrt(2 * g * (h_attuale - h_orifizio))
            x_flusso_perc = np.linspace(0, v_attuale * np.sqrt(2 * h_orifizio / g), 100)
            y_flusso_perc = h_orifizio + traiettoria_flusso(x_flusso_perc, v_attuale)
            fig4.add_trace(go.Scatter(x=x_flusso_perc, y=y_flusso_perc, mode='lines', name=f'{perc*100:.0f}% dell\'altezza'))
    fig4.update_layout(title='Traiettoria dell\'acqua a diverse altezze', xaxis_title='Distanza orizzontale (m)', yaxis_title='Altezza dell\'acqua (m)', yaxis_range=[0, 10])
    st.plotly_chart(fig4)

# Create interactive sliders using Streamlit
D = st.sidebar.slider('Diametro recipiente (m)', min_value=0.1, max_value=1.0, value=0.5, step=0.01)
d = st.sidebar.slider('Diametro orifizio (m)', min_value=0.001, max_value=0.05, value=0.005, step=0.001)
h_orifizio = st.sidebar.slider('Altezza orifizio (m)', min_value=0.1, max_value=10.0, value=0.1, step=0.01)
T = st.sidebar.slider('Tempo massimo (s)', min_value=5, max_value=1000, value=30, step=1)

# Run the main function
plot_altezza_acqua(D, d, h_orifizio, T)
