import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st

# First let's define a Black-Scholes function
def black_scholes_european(S,K,T,r,sigma, option_type):
    d1 = (np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == "call":
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    elif option_type == "put":
        return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

# Now, let's define functions to calculate all the Greeks of the option
def greeks_option(S,K,T,r,sigma, option_type, greek_type):
    d1 = (np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == "call":
        delta = norm.cdf(d1) # Partial derivative with respect to underlying asset
        gamma = norm.pdf(d1)/(S*sigma*np.sqrt(T)) # Second partial derivative with respect to underlying asset
        theta = -(sigma*S*norm.pdf(d1))/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2) # Derivative with respect to time
        vega = S*np.sqrt(T)*norm.pdf(d1) # Derivative with respect to sigma
        rho = K*T*np.exp(-r*T)*norm.cdf(d2) # Derivative with respect to r 
    elif option_type == "put":
        delta = norm.cdf(d1)-1
        gamma = norm.pdf(d1)/(S*sigma*np.sqrt(T))
        theta = -(sigma*S*norm.pdf(d1))/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2)
        vega = S*np.sqrt(T)*norm.pdf(d1)
        rho = -K*T*np.exp(-r*T)*norm.cdf(-d2)
    if greek_type == "delta":
        return delta
    elif greek_type == "gamma":
        return gamma
    elif greek_type == "theta":
        return theta
    elif greek_type == "vega":
        return vega
    elif greek_type == "rho":
        return rho
    
# We can now start to define our dashboard 
st.title("Greeks Evolution Dashboard for Black-Scholes Model")
st.text("This dashboard allows you to visualize the evolution of the Greeks of an option in function of the spot price in the Black-Scholes model for a European option.")
st.sidebar.header("Option Calibration Parameters")
spot_min = st.number_input("Spot minimum", value=80, step = 1)
spot_max = st.number_input("Spot maximum", value=120, step = 1)
if spot_min > spot_max:
    st.error("Please enter a valid range : Spot minimum should be less than Spot maximum")
    st.stop()
else:
    spot_linspace = np.linspace(spot_min, spot_max, 100)
    strike = st.sidebar.slider("Strike Price S (in $)", 50, 150, 100)
    maturity = st.sidebar.slider("Time to maturity T (in years)", 0.1, 2.0, 1.0, 0.1)
    risk_free_rate = st.sidebar.slider("Risk-free rate r ", 0.0, 0.1, 0.05, 0.01)
    volatility = st.sidebar.slider("Volatility sigma ", 0.1, 1.0, 0.2, 0.01)
    option_type = st.sidebar.radio("Option  Type", ["Call", "Put"])
    greek_type = st.sidebar.radio("Greek Type", ["Delta", "Gamma", "Theta", "Vega", "Rho"])

    # Calculate the values of the Greek choosen and the prices of the option
    greek_linspace = [greeks_option(spot, strike, maturity, risk_free_rate, volatility, option_type.lower(), greek_type.lower()) for spot in spot_linspace]
    option_linspace = [black_scholes_european(spot, strike, maturity, risk_free_rate, volatility, option_type.lower()) for spot in spot_linspace]
    payoff_linspace = [max(spot - strike, 0) if option_type == "Call" else max(strike-spot, 0) for spot in spot_linspace]
    
    st.write(f"### {greek_type} Evolution")

    # Plot Smile
    colors = plt.get_cmap("tab10").colors
    #colors = px.colors.qualitative.T10
    dic_greek = {"Delta":0, "Gamma":1, "Theta":2, "Vega":3, "Rho":4}
    fig, ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(spot_linspace, option_linspace, color = "y", label="Option Price")
    ax1.plot(spot_linspace, payoff_linspace, color = "k", label="Payoff")
    ax1.axvline(x=strike, color='k', linestyle='--', label="Strike Price")
    ax1.set_xlabel("Strike Price")
    ax1.set_ylabel("Option Price")
    ax2 = ax1.twinx()
    ax2.plot(spot_linspace, greek_linspace, color = colors[dic_greek[greek_type]%len(colors)], label=f"{greek_type} Evolution")
    ax2.set_ylabel("Greek Value")
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title(f"{greek_type} Evolution in function of the strike")
    # fig = go.Figure()
    
    # # Courbe du prix de l'option
    # fig.add_trace(go.Scatter(x=spot_linspace, y=option_linspace, mode='lines', 
    #                          name='Option Price', line=dict(color='yellow')))
    
    # # Courbe du payoff
    # fig.add_trace(go.Scatter(x=spot_linspace, y=payoff_linspace, mode='lines', 
    #                          name='Payoff', line=dict(color='black')))
    
    # # Ligne verticale pour le strike
    # fig.add_trace(go.Scatter(x=[strike, strike], y=[min(option_linspace), max(option_linspace)], 
    #                          mode='lines', name='Strike Price', line=dict(color='black', dash='dash')))
    
    # # Courbe du Greek
    # fig.add_trace(go.Scatter(x=spot_linspace, y=greek_linspace, mode='lines', 
    #                          name=f'{greek_type} Evolution', 
    #                          line=dict(color=colors[dic_greek[greek_type] % len(colors)]),
    #                          yaxis='y2'))
    
    # # Mise en page
    # fig.update_layout(
    #     title=f"{greek_type} Evolution in function of the strike",
    #     xaxis=dict(title="Strike Price"),
    #     yaxis=dict(title="Option Price"),
    #     yaxis2=dict(title="Greek Value", overlaying='y', side='right'),
    #     legend=dict(x=0.02, y=0.98),
    #     template='plotly_white'
    # )
    # st.plotly_chart(fig)
    st.pyplot(plt)
