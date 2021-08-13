import numpy as np
from scipy.stats import norm

class StandardCallOption(object):
    def __init__(self,
                 initial_price,
                 strike_price,
                 interest_rate,
                 volatility,
                 time_to_maturity):
        super(StandardCallOption, self).__init__()
        self.initial_price = initial_price
        self.strike_price = strike_price
        self.interest_rate = interest_rate
        self.volatility = volatility
        self.time_to_maturity = time_to_maturity

    def compute(self):
        d2 = (np.log(self.initial_price / self.strike_price) + (
                    self.interest_rate - 0.5 * self.volatility ** 2) * self.time_to_maturity) / (
                         self.volatility / np.sqrt(self.time_to_maturity))
        d1 = d2 + self.volatility * np.sqrt(self.time_to_maturity)

        # From formula in Black-Scholes market
        price = self.initial_price * norm.cdf(d1) - \
                self.strike_price * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2)

        return price

class StandardPutOption(object):
    def __init__(self,
                 initial_price,
                 strike_price,
                 interest_rate,
                 volatility,
                 time_to_maturity):
        super(StandardPutOption, self).__init__()
        self.initial_price = initial_price
        self.strike_price = strike_price
        self.interest_rate = interest_rate
        self.volatility = volatility
        self.time_to_maturity = time_to_maturity

    def compute(self):
        d2 = (np.log(self.initial_price / self.strike_price) + (
                    self.interest_rate - 0.5 * self.volatility ** 2) * self.time_to_maturity) / (
                         self.volatility / np.sqrt(self.time_to_maturity))
        d1 = d2 + self.volatility * np.sqrt(self.time_to_maturity)

        # From formula in Black-Scholes market
        price = self.strike_price * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2) - \
                self.initial_price * norm.cdf(-d1)

        return price
