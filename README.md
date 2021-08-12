<h1 align="center"> Description </h1>
This repository analyses the Asian option by modelling the price of both the arithmetic Asian call option and the arithmetic Asian put option in a Black-Scholes market setting. This is done by first deriving a finite difference scheme (FDS) from their PDE's and then by the control variate Monte Carlo (CVMC) method. The analysis consists of comparing the two different methods and also comparing the the modelling from the FDS method to the standard European call and put options. 

<hr>

<h2 align="center">Short introduction to the Asian Options</h2>

Essentially, an option is a financial contract between two parties, giving the right, but not the obligation, to the owner of the contract to either buy or sell a specific underlying asset for a given strike price <i>K</i>. If the right to the owner is to buy the asset, it is a call option and if the right is to sell the asset, it is a put option. The Asian option is specific kind of option that do not share the characteristics of plain vanilla options. Mainly, the Asian option is a path dependent option, meaning that its pay-off are affected by how the price at maturity time <i>T</i> was reached and thus depended on the price path of the underlying asset. This differ from the standard European options, whose pay-off is dependent only on the price at which it is exercised [1].


The path dependence of the Asian option is due to its pay-off includes a time average of the price for the underlying asset and typically there is two types of averaging for Asian options, namely arithmetic avergae and geometric average. It is thus also referred to as average-price options [1]. The pay-off for the Asian call option and Asian put option, given the price, <i>S(t)</i>, of the underlying asset, is therefore given by

<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=Y_{Call}^{Asian}&space;:=&space;\bigg(\frac{1}{T}\int_{0}^{T}S(t)dt&space;-&space;K\bigg)_&plus;,&space;\quad&space;Y_{Put}^{Asian}&space;:=&space;\bigg(K-\frac{1}{T}\int_{0}^TS(t)dt\bigg)_&plus;," target="_blank"><img src="https://latex.codecogs.com/gif.latex?Y_{Call}^{Asian}&space;:=&space;\bigg(\frac{1}{T}\int_{0}^{T}S(t)dt&space;-&space;K\bigg)_&plus;,&space;\quad&space;Y_{Put}^{Asian}&space;:=&space;\bigg(K-\frac{1}{T}\int_{0}^TS(t)dt\bigg)_&plus;," title="Y_{Call}^{Asian} := \bigg(\frac{1}{T}\int_{0}^{T}S(t)dt - K\bigg)_+, \quad Y_{Put}^{Asian} := \bigg(K-\frac{1}{T}\int_{0}^TS(t)dt\bigg)_+," /></a></p>

for arithmetic average and 

<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=Y_{Call}^{Asian}&space;:=&space;\bigg(\exp\big(\frac{1}{T}\int_{0}^{T}\log&space;S(t)dt\big)&space;-&space;K\bigg)_&plus;,&space;\quad&space;Y_{Put}^{Asian}&space;:=&space;\bigg(K-\exp&space;\big(\frac{1}{T}\int_{0}^T\log&space;S(t)dt\big)\bigg)_&plus;," target="_blank"><img src="https://latex.codecogs.com/png.latex?Y_{Call}^{Asian}&space;:=&space;\bigg(\exp\big(\frac{1}{T}\int_{0}^{T}\log&space;S(t)dt\big)&space;-&space;K\bigg)_&plus;,&space;\quad&space;Y_{Put}^{Asian}&space;:=&space;\bigg(K-\exp&space;\big(\frac{1}{T}\int_{0}^T\log&space;S(t)dt\big)\bigg)_&plus;," title="Y_{Call}^{Asian} := \bigg(\exp\big(\frac{1}{T}\int_{0}^{T}\log S(t)dt\big) - K\bigg)_+, \quad Y_{Put}^{Asian} := \bigg(K-\exp \big(\frac{1}{T}\int_{0}^T\log S(t)dt\big)\bigg)_+," /></a></p>

for geometric average. This compared to the pay-off of the European option defined as 

<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=Y_{Call}^{Europ}&space;:=&space;\big(S(T)-K\big)_&plus;,&space;\quad&space;Y_{Put}^{Europ}&space;:=&space;\big(K-S(T)\big)_&plus;," target="_blank"><img src="https://latex.codecogs.com/png.latex?Y_{Call}^{Europ}&space;:=&space;\big(S(T)-K\big)_&plus;,&space;\quad&space;Y_{Put}^{Europ}&space;:=&space;\big(K-S(T)\big)_&plus;," title="Y_{Call}^{Europ} := \big(S(T)-K\big)_+, \quad Y_{Put}^{Europ} := \big(K-S(T)\big)_+," /></a></p>

where <i>T>0</i> is the time of maturity of the underlying asset [2]. 


The financial utility of the Asian option is the reduction of market manipulation at maturity time <i>T</i>, a common problem in European options where the price could be manipulated upwards by speculators before the maturity. Even if prohibited, market manipulation occurs, but with the effect of not being as dependent of the expiration date, Asian options acts as a form of protection from such market manipulation [3]. Also, due to the averaging on the prices, the Asian option has lower volatility than the European options and thus typically making them cheaper than standard European options [4]. Because of this, they are often used by such traders that are being exposed under a period of time by the underlying asset [5]. A possible disadvantage of the Asian option, as previously mentioned is the reduced impact from volatility which implies that the ability to capitalize on the volatility peaks. Therefore, the possible profit from trading Asian options are less than non-averaging option.


<h2 align="center">Bibliography</h2>
[1] Erik Wiklund. <i>Asian Option Pricing and Volatility</i>, 2012. URL: https://www.math.kth.se/matstat/seminarier/reports/M-exjobb12/120412a.pdf. Accessed: 2021-02-11.


[2] Steven E. Shreve. <i>Stochastic Calculus for Finance II</i>, chapter 7.

[3] Amanda Harvey. <i>The Asian Option</i>. URL: https://www.stock-options-made-easy.com/asian-option.html. Accessed: 2021-03-14

[4] Qian Zhang Aleksandra Mraovic. <i>Valuation of Asian Options - with Levy Approximation</i>, 2014. URL: https://lup.lub.lu.se/luur/downloadfunc=downloadFile&recordOId=4301159&fileOId=4301160. Accessed: 2021-02-11

[5] Finpricing. <i>EQUITY ASIAN OPTION</i>, 2019. URL: https://finpricing.com/lib/EqAsian.html.Accessed: 2021-03-14.
