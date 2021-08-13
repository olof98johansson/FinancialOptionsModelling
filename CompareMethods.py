import CVMCOptions
import AsianOptions
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
sns.set_style('darkgrid')

def cvmc_vs_fds_volatility(volatilities: list, interest_rate: float,
                time_to_maturity: int, strike_price, initial_price) -> defaultdict:
    prices = defaultdict(list)
    for vol in volatilities:
        print(f'Volatility: {vol}')
        # Call options
        CVMC_asian_call = CVMCOptions.CVMCAsianCallOption(initial_price=initial_price, volatility=vol,
                                                          interest_rate=interest_rate, time_to_maturity=time_to_maturity,
                                                          strike_price=strike_price, N=500, n=1000)
        FDS_asian_call = AsianOptions.AsianCallOption(initial_price=initial_price, volatility=vol,
                                                      interest_rate=interest_rate, time_to_maturity=time_to_maturity,
                                                      strike_price=strike_price, time_partition_size=500,
                                                      spatial_partition_size=1000)

        cvmc_call_price, cvmc_call_conf95 = CVMC_asian_call.compute()
        fds_call_price = FDS_asian_call.solve()
        #print(f'PDE Call: {fds_call_price}')
        #print(f'CVMC Call: {cvmc_call_price}')


        # Put options
        CVMC_asian_put = CVMCOptions.CVMCAsianPutOption(initial_price=initial_price, volatility=vol,
                                                          interest_rate=interest_rate,
                                                          time_to_maturity=time_to_maturity,
                                                          strike_price=strike_price, N=500, n=1000)
        FDS_asian_put = AsianOptions.AsianPutOption(initial_price=initial_price, volatility=vol,
                                                      interest_rate=interest_rate, time_to_maturity=time_to_maturity,
                                                      strike_price=strike_price, time_partition_size=500,
                                                      spatial_partition_size=1000)

        cvmc_put_price, cvmc_put_conf95 = CVMC_asian_put.compute()
        fds_put_price = FDS_asian_put.solve()
        #print(f'PDE Put: {fds_put_price}')
        #print(f'CVMC Put: {cvmc_put_price}')
        print('\n')


        # Store prices and 95% confidence values
        prices["FDS call"].append(fds_call_price)
        prices["FDS put"].append(fds_put_price)
        prices["CVMC call"].append(cvmc_call_price)
        prices["CVMC put"].append(cvmc_put_price)
        prices["CVMC call conf95"].append(cvmc_call_conf95)
        prices["CVMC put conf95"].append(cvmc_put_conf95)

    return prices

def cvmc_vs_fds_init_price(initial_prices: list, interest_rate: float,
                time_to_maturity: int, strike_price, volatility) -> defaultdict:
    prices = defaultdict(list)
    for init_price in initial_prices:
        print(f'Init price: {init_price}')
        # Call options
        CVMC_asian_call = CVMCOptions.CVMCAsianCallOption(initial_price=init_price, volatility=volatility,
                                                          interest_rate=interest_rate, time_to_maturity=time_to_maturity,
                                                          strike_price=strike_price, N=500, n=1000)
        FDS_asian_call = AsianOptions.AsianCallOption(initial_price=init_price, volatility=volatility,
                                                      interest_rate=interest_rate, time_to_maturity=time_to_maturity,
                                                      strike_price=strike_price, time_partition_size=500,
                                                      spatial_partition_size=1000)

        cvmc_call_price, cvmc_call_conf95 = CVMC_asian_call.compute()
        fds_call_price = FDS_asian_call.solve()
        #print(f'PDE Call: {fds_call_price}')
        #print(f'CVMC Call: {cvmc_call_price}')

        # Put options
        CVMC_asian_put = CVMCOptions.CVMCAsianPutOption(initial_price=init_price, volatility=volatility,
                                                          interest_rate=interest_rate,
                                                          time_to_maturity=time_to_maturity,
                                                          strike_price=strike_price, N=500, n=1000)
        FDS_asian_put = AsianOptions.AsianPutOption(initial_price=init_price, volatility=volatility,
                                                      interest_rate=interest_rate, time_to_maturity=time_to_maturity,
                                                      strike_price=strike_price, time_partition_size=500,
                                                      spatial_partition_size=1000)

        cvmc_put_price, cvmc_put_conf95 = CVMC_asian_put.compute()
        fds_put_price = FDS_asian_put.solve()
        #print(f'PDE Put: {fds_put_price}')
        #print(f'CVMC Put: {cvmc_put_price}')
        #print('\n')

        # Store prices and 95% confidence values
        prices["FDS call"].append(fds_call_price)
        prices["FDS put"].append(fds_put_price)
        prices["CVMC call"].append(cvmc_call_price)
        prices["CVMC put"].append(cvmc_put_price)
        prices["CVMC call conf95"].append(cvmc_call_conf95)
        prices["CVMC put conf95"].append(cvmc_put_conf95)

    return prices

def plot_prices(prices: defaultdict, x_values: list, varying_factor: str, strike_price=None):
    fds_call_prices = prices["FDS call"]
    fds_put_prices = prices["FDS put"]
    cvmc_call_prices = prices["CVMC call"]
    cvmc_put_prices = prices["CVMC put"]

    plt.figure(figsize=(14, 10))
    plt.plot(x_values, fds_call_prices, color='#b00b69', label='FDS Call Option')
    plt.plot(x_values, fds_put_prices, color='#b00b69', linestyle='--', label='FDS Put Option')
    plt.plot(x_values, cvmc_call_prices, color='#5c04a5', label='CVMC Call Option')
    plt.plot(x_values, cvmc_put_prices, color='#5c04a5', linestyle='--', label='CVMC Put Option')
    if varying_factor.lower() in ['volatility', 'vol', 'sigma']:
        plt.xlabel(r'$\sigma$', fontsize=14)
    elif varying_factor.lower() in ['s0', 'initial_stock_price', 'initial_price', 'initial price', 'initial stock price']:
        plt.xlabel(r'$S_0$', fontsize=14)
        if strike_price:
            plt.vlines(strike_price, 0, 0.75*max(fds_call_prices), linestyles='dashed')
            plt.text(x=strike_price, y=0.8*max(fds_call_prices), s='At the money (S = K)', ha='center', va='center')
            plt.text(x=0.6*strike_price, y=0.8 * max(fds_call_prices), s='Out of the money (OTM) for call', ha='center', va='center')
            plt.text(x=0.6 * strike_price, y=0.7 * max(fds_call_prices), s='In the money (ITM) for put', ha='center', va='center')
            plt.text(x=1.4 * strike_price, y=0.8 * max(fds_call_prices), s='In of the money (ITM) for call', ha='center', va='center')
            plt.text(x=1.4 * strike_price, y=0.7 * max(fds_call_prices), s='Out of the money (OTM) for put', ha='center', va='center')

    # Add table of 95% confidence values
    #columns = tuple([x_values])
    #rows = ['CVMC Call option', 'CVMC Put option']
    #texts = [prices["CVMC call conf95"], prices["CVMC put conf95"]]
    #the_table = plt.table(cellText=texts,
    #                      rowLabels=rows,
    #                      rowColours=plt.cm.BuPu(np.linspace(0, 0.5, len(rows))),
    #                      colLabels=columns,
    #                      loc='bottom')

    plt.title(f'Comparison between the CVMC method and FDS method for the Asian Options for varying {varying_factor}')
    plt.legend()
    plt.ylabel(r'Price function $\Pi(0)$')
    plt.savefig(f'./Results/comparison_method_{varying_factor.split(" ")[0]}.png')
    plt.show()



if __name__ == '__main__':
    vol_prices = cvmc_vs_fds_volatility(volatilities=[0.1 + 0.1 * i for i in range(49)], interest_rate=0.05,
                                        time_to_maturity=1, strike_price=50, initial_price=50)
    print(f'Done with volatility')
    s0_prices = cvmc_vs_fds_init_price(initial_prices=[10 + i * 5 for i in range(18)], interest_rate=0.05,
                                        time_to_maturity=1, strike_price=50, volatility=0.5)
    print(f'Done with prices')



    plot_prices(vol_prices, [0.1 + 0.1 * i for i in range(49)], 'volatility')
    plot_prices(s0_prices, [10 + i * 5 for i in range(18)], 'initial price', strike_price=50)