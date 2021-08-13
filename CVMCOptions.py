import numpy as np
import scipy.stats as stats
def geometric_brownian_motion(s, sigma, r, T, N, n):
    ''' Path of the stock price
        Have uniform partition of size N for the time interval [0,T]
        and thus generate N paths of the geometric Brownian motion
    '''
    h = T / N
   # print(f'h: {h}')
    W = np.random.randn(n, N)
   # print(f'W: {W}')
    q = np.ones((n, N))
   # print(f'q: {q}')
   # asd
    path = s * np.exp((r - sigma ** 2 / 2) * h * np.cumsum(q.T, axis=0) + sigma * np.sqrt(h) * np.cumsum(W.T, axis=0))

    path = np.concatenate((s * np.ones((1, n)), path))

    return path

class CVMCAsianCallOption(object):
    '''
        Compute risk-neutral price of Asian call with control variate MC with geometric price as CV
    '''
    def __init__(self, initial_price, volatility, interest_rate, time_to_maturity, strike_price, N, n):
        super(CVMCAsianCallOption, self).__init__()
        self.initial_price = initial_price
        self.volatility = volatility
        self.interest_rate = interest_rate
        self.time_to_maturity = time_to_maturity
        self.strike_price = strike_price
        self.N = N
        self.n = n

    def compute(self):
        q = 0.5 * (self.interest_rate - (self.volatility**2 / 6))
        d1 = (np.log(self.initial_price / self.strike_price) + (q * self.time_to_maturity)) /\
             (self.volatility * np.sqrt(self.time_to_maturity / 3))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity / 3)


        geometric_call_price = np.exp(-self.interest_rate * self.time_to_maturity) * (np.exp(q * self.time_to_maturity) * \
            self.initial_price * stats.norm.cdf(d1) - self.strike_price * stats.norm.cdf(d2))

        stockpath = geometric_brownian_motion(self.initial_price, self.volatility, self.interest_rate,
                                              self.time_to_maturity, self.N, self.n)


        arithmetic_payoff = np.array([np.max([0, np.mean(stockpath[:, i])-self.strike_price]) for i in range(np.shape(stockpath)[1])])
        geometric_payoff = np.array([np.max([0, stats.mstats.gmean(stockpath[:, i])-self.strike_price]) for i in range(np.shape(stockpath)[1])])

        price = np.exp(-self.interest_rate * self.time_to_maturity) * np.mean(arithmetic_payoff - geometric_payoff) + geometric_call_price
        conf95 = 1.96 * np.std(arithmetic_payoff - geometric_payoff) / np.sqrt(self.n)
        return price, conf95



class CVMCAsianPutOption(object):
    '''
        Compute risk-neutral price of Asian put with control variate MC with geometric price as CV
    '''
    def __init__(self, initial_price, volatility, interest_rate, time_to_maturity, strike_price, N, n):
        super(CVMCAsianPutOption, self).__init__()
        self.initial_price = initial_price
        self.volatility = volatility
        self.interest_rate = interest_rate
        self.time_to_maturity = time_to_maturity
        self.strike_price = strike_price
        self.N = N
        self.n = n

    def compute(self):
        q = 0.5 * (self.interest_rate - (self.volatility ** 2 / 6))
        d1 = (np.log(self.initial_price / self.strike_price) + (q * self.time_to_maturity)) / \
             (self.volatility * np.sqrt(self.time_to_maturity / 3))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity / 3)

        geometric_put_price = np.exp(-self.interest_rate * self.time_to_maturity) * (self.strike_price *
                    stats.norm.cdf(-d2) - np.exp(q * self.time_to_maturity) * self.initial_price * stats.norm.cdf(-d1))

        stockpath = geometric_brownian_motion(self.initial_price, self.volatility, self.interest_rate,
                                              self.time_to_maturity, self.N, self.n)

        arithmetic_payoff = np.array([np.max([0, self.strike_price - np.mean(stockpath[:, i])]) for i in range(np.shape(stockpath)[1])])
        geometric_payoff = np.array([np.max([0, self.strike_price - stats.mstats.gmean(stockpath[:, i])]) for i in range(np.shape(stockpath)[1])])

        price = np.exp(-self.interest_rate * self.time_to_maturity) * np.mean(arithmetic_payoff - geometric_payoff) + geometric_put_price
        conf95 = 1.96 * np.std(arithmetic_payoff - geometric_payoff) / np.sqrt(self.n)
        return price, conf95





