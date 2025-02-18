# Options-Dashboard
This repository contains different dashboards made to price options, to see the evolution of options' greeks etc... 

1. The first project of this repository is the Vanilla_Greeks_Dashboard.py. To run it, you have to input the command "python3 -m streamlit run Vanilla_Greeks_Dashboard.py" into the terminal of your interpreter. It will open a window of your internet explorer showcasing the dashboard. Here is a picture of what you will obtain (if you unzoom to see everything at the same time) :
   
![image](https://github.com/user-attachments/assets/2e18daab-17fe-44de-a7b6-6b2095223ad8)

![image](https://github.com/user-attachments/assets/02087e3e-9f46-4973-910e-019bdf7a0106)


You can change the parameters of the simplest Black-Scholes model for European Options : the strike of the option, its maturity, the risk-free rate and the volatility. You can also choose either a call or a put and observe one of the 5 main Greeks usually calculated in Financial Markets : Delta, Gamma, Theta, Vega or Rho. 
The graph displays the option price and the payoff on the left y-axis and the considered Greek on the right y-axis. 
Finally, you can update the minimum and maximum of the spot prices considered when plotting. 

2. The second project of the repository will try to improve the previous Greeks Dashboard by adding more Greeks, and different variants of European options.
   


