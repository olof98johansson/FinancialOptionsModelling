import AsianOptions
import StandardEuropeanOptions
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
from collections import defaultdict
import numpy as np


def different_volatilities(volatilities: list, interest_rate=0.05,
                           time_to_maturity=1, strike_price=12, initial_price=10):
    if not isinstance(volatilities, list):
        raise ValueError(f'"volatilities" is not of type list!')

    prices = defaultdict(list)
    for vol in volatilities:
        # Call options for different volatilities
        asian_call = AsianOptions.AsianCallOption(initial_price=initial_price,
                                                  strike_price=strike_price,
                                                  interest_rate=interest_rate,
                                                  volatility=vol,
                                                  time_to_maturity=time_to_maturity,
                                                  time_partition_size=100,
                                                  spatial_partition_size=500)

        standard_call = StandardEuropeanOptions.StandardCallOption(initial_price=initial_price,
                                                                   strike_price=strike_price,
                                                                   interest_rate=interest_rate,
                                                                   volatility=vol,
                                                                   time_to_maturity=time_to_maturity)
        asian_call_price = asian_call.solve()
        standard_call_price = standard_call.compute()

        # Put options for different volatilities
        asian_put = AsianOptions.AsianPutOption(initial_price=initial_price,
                                                  strike_price=strike_price,
                                                  interest_rate=interest_rate,
                                                  volatility=vol,
                                                  time_to_maturity=time_to_maturity,
                                                  time_partition_size=100,
                                                  spatial_partition_size=500)
        standard_put = StandardEuropeanOptions.StandardPutOption(initial_price=initial_price,
                                                                   strike_price=strike_price,
                                                                   interest_rate=interest_rate,
                                                                   volatility=vol,
                                                                   time_to_maturity=time_to_maturity)

        asian_put_price = asian_put.solve()
        standard_put_price = standard_put.compute()

        # Store prices
        prices["Asian call"].append(asian_call_price)
        prices["Asian put"].append(asian_put_price)
        prices["Standard call"].append(standard_call_price)
        prices["Standard put"].append(standard_put_price)

    return prices


def different_initial_prices(initial_prices: list, strike_price, interest_rate=0.05,
                             time_to_maturity=1,  volatility=0.5):
    if not isinstance(initial_prices, list):
        raise ValueError(f'"initial_prices" is not of type list!')

    prices = defaultdict(list)
    for pr_idx, init_pr in enumerate(initial_prices):
        # Call options for different volatilities
        asian_call = AsianOptions.AsianCallOption(initial_price=init_pr,
                                                  strike_price=strike_price,
                                                  interest_rate=interest_rate,
                                                  volatility=volatility,
                                                  time_to_maturity=time_to_maturity,
                                                  time_partition_size=100,
                                                  spatial_partition_size=500)

        standard_call = StandardEuropeanOptions.StandardCallOption(initial_price=init_pr,
                                                                  strike_price=strike_price,
                                                                  interest_rate=interest_rate,
                                                                  volatility=volatility,
                                                                  time_to_maturity=time_to_maturity)
        asian_call_price = asian_call.solve()
        standard_call_price = standard_call.compute()

        # Put options for different volatilities
        asian_put = AsianOptions.AsianPutOption(initial_price=init_pr,
                                                  strike_price=strike_price,
                                                  interest_rate=interest_rate,
                                                  volatility=volatility,
                                                  time_to_maturity=time_to_maturity,
                                                  time_partition_size=100,
                                                  spatial_partition_size=500)
        standard_put = StandardEuropeanOptions.StandardPutOption(initial_price=init_pr,
                                                                  strike_price=strike_price,
                                                                  interest_rate=interest_rate,
                                                                  volatility=volatility,
                                                                  time_to_maturity=time_to_maturity)

        asian_put_price = asian_put.solve()
        standard_put_price = standard_put.compute()

        # Store prices
        prices["Asian call"].append(asian_call_price)
        prices["Asian put"].append(asian_put_price)
        prices["Standard call"].append(standard_call_price)
        prices["Standard put"].append(standard_put_price)

    return prices

def put_call_parity(initial_price=20, strike_price=12, interest_rate=0.05,
                    volatility=0.5, time_to_maturity=1, confidence=0.05):

    # Numerical prices
    asian_call = AsianOptions.AsianCallOption(initial_price=initial_price,
                                              strike_price=strike_price,
                                              interest_rate=interest_rate,
                                              volatility=volatility,
                                              time_to_maturity=time_to_maturity,
                                              time_partition_size=100,
                                              spatial_partition_size=500)
    asian_put = AsianOptions.AsianPutOption(initial_price=initial_price,
                                              strike_price=strike_price,
                                              interest_rate=interest_rate,
                                              volatility=volatility,
                                              time_to_maturity=time_to_maturity,
                                              time_partition_size=100,
                                              spatial_partition_size=500)
    asian_call_price = asian_call.solve()
    asian_put_price = asian_put.solve()

    numerical_pcp = asian_call_price - asian_put_price

    # Analytical formula
    analytical_pcp = initial_price / (interest_rate * time_to_maturity) * \
                     (1 - np.exp(-interest_rate * time_to_maturity)) - strike_price * np.exp(-interest_rate*time_to_maturity)

    ratio = 1 - numerical_pcp / analytical_pcp

    if ratio <= confidence:
        print(f'Put-call parity ratio is within confidence! ({ratio:.4f} < {confidence})')
    else:
        print(f'Put-call parity not fulfilled, ratio is outside of confidence! ({ratio:.4f} > {confidence})')


def plot_prices(prices: defaultdict, x_values: list, varying_factor: str, strike_price=None):
    asian_call_prices = prices["Asian call"]
    asian_put_prices = prices["Asian put"]
    standard_call_prices = prices["Standard call"]
    standard_put_prices = prices["Standard put"]

    plt.figure(figsize=(14, 10))
    plt.plot(x_values, asian_call_prices, color='#b00b69', label='Asian Call')
    plt.plot(x_values, asian_put_prices, color='#b00b69', linestyle='--', label='Asian Put')
    plt.plot(x_values, standard_call_prices, color='#5c04a5', label='Standard Call')
    plt.plot(x_values, standard_put_prices, color='#5c04a5', linestyle='--', label='Standard Put')
    if varying_factor.lower() in ['volatility', 'vol', 'sigma']:
        plt.xlabel(r'$\sigma$', fontsize=14)
    elif varying_factor.lower() in ['s0', 'initial_stock_price', 'initial_price', 'initial price', 'initial stock price']:
        plt.xlabel(r'$S_0$', fontsize=14)
        if strike_price:
            plt.vlines(strike_price, 0, 0.75*max(standard_call_prices), linestyles='dashed')
            plt.text(x=strike_price, y=0.8*max(standard_call_prices), s='At the money (S = K)', ha='center', va='center')
            plt.text(x=0.6*strike_price, y=0.8 * max(standard_call_prices), s='Out of the money (OTM) for call', ha='center', va='center')
            plt.text(x=0.6 * strike_price, y=0.7 * max(standard_call_prices), s='In the money (ITM) for put', ha='center', va='center')
            plt.text(x=1.4 * strike_price, y=0.8 * max(standard_call_prices), s='In of the money (ITM) for call', ha='center', va='center')
            plt.text(x=1.4 * strike_price, y=0.7 * max(standard_call_prices), s='Out of the money (OTM) for put', ha='center', va='center')
    plt.title(f'Comparison between Asian options and Standard European options for different {varying_factor}')
    plt.legend()
    plt.ylabel(r'Price function $\Pi(0)$')
    plt.savefig(f'./Results/comparison_{varying_factor.split(" ")[0]}.png')
    plt.show()


if __name__ == '__main__':
    vol_prices = different_volatilities([0+0.2*i for i in range(50)], interest_rate=0.05,
                           time_to_maturity=1, strike_price=12, initial_price=10)
    s0_prices = different_initial_prices([10+i*5 for i in range(18)], strike_price=50,
                             interest_rate=0.05, time_to_maturity=1,  volatility=0.5)
    plot_prices(vol_prices, [0+0.2*i for i in range(50)], 'volatility')
    plot_prices(s0_prices, [10+i*5 for i in range(18)], 'initial price', strike_price=50)
    put_call_parity()
    