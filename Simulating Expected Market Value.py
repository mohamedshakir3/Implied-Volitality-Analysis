
################################################################################################################
# Simulates the expected fair market value of European Call option using generic Monte Carlo price simulation  #
# Notes - Assuming the underlying follows a geometric Brownian motion                                          #
################################################################################################################


###################### Libraries #############################
import math
import numpy as np
#############################################################


class StochasticProcess:

    def time_step(self):

        dW = np.random.normal(0, math.sqrt(self.delta_t))
        dS = self.drift*self.current_asset_price*self.delta_t + self.asset_volatility*self.current_asset_price*dW
        self.asset_prices.append(self.current_asset_price + dS)
        self.current_asset_price = self.current_asset_price + dS

    def __init__(self, asset_price, drift, delta_t, asset_volatility):
        self.current_asset_price = asset_price
        self.asset_prices = []
        self.asset_prices.append(asset_price)
        self.drift = drift
        self.delta_t = delta_t
        self.asset_volatility = asset_volatility


class EuroCall:

    def __init__(self, strike):
        self.strike = strike


class EuroCallSimulation:

    def __init__(self, EuroCall, n_options, initial_asset_price, drift, delta_t, asset_volatility, time_to_expiration, risk_free_rate):
        stochastic_processes = []
        for i in range(n_options):
            stochastic_processes.append(StochasticProcess(initial_asset_price, drift, delta_t, asset_volatility))

        for stochastic_process in stochastic_processes:
            tte = time_to_expiration
            while((tte-stochastic_process.delta_t) > 0):
                tte = tte - stochastic_process.delta_t
                stochastic_process.time_step()

        payoffs = []
        for stochastic_process in stochastic_processes:
            payoff = stochastic_process.asset_prices[len(stochastic_process.asset_prices)-1] - EuroCall.strike
            z = payoff if payoff > 0 else 0
            payoffs.append(z)
        self.price = np.average(payoffs)*math.exp(-time_to_expiration*risk_free_rate)

print('Simulated Monte Carlo Euro Call price: ', EuroCallSimulation(EuroCall(333), 1000, 332.37, -.05, 1/365, .25, 17/365, .004).price)
