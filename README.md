# Super_Simple_Stock_Market
Assignment Super Simple Stock Market
Requirements
1. The Global Beverage Corporation Exchange is a new stock market trading in drinks companies.
a. Your company is building the object-oriented system to run that trading.
b. You have been assigned to build part of the core object model for a limited phase 1
2. Provide the complete source code that will:-
a. For a given stock,
i. Given any price as input, calculate the dividend yield
ii. Given any price as input, calculate the P/E Ratio
iii. Record a trade, with timestamp, quantity, buy or sell indicator and price
iv. Calculate Volume Weighted Stock Price based on trades in past 5 minutes
b. Calculate the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks


One class is created with class name "SimpleStockMarket"
Class has total 5 methods for each point mentioned in the question.

Method "DivindendYield" : The function will give us dividend yield of a stock using  last dividend
        for common type of stock and par value for preffred type of stock <Point 2.a.1>

Method "PEratio" : The function will calculate P/E ratio using price and dividend of a stock.
        Dividend is calculated using the function DivindendYield(self,stocksymbol,price) of class SimpleStockMarket <2.a.ii>

Method "recordtrade" : The function will store data in Transaction_data.csv file. It will store current timestamp, Stock Symbol 
                        which will be bought or sold, How much of the stock will be bough or sold,
                        Indicator will contain either of two string BUY or SOLD, Price will contain the amount involved during that transaction <2.a.iii>

Method "VolumeWeightedPrice" : This function will take the stock symbol as parameter and it will find volume weighted stock price of transaction.
        It will take quantity and prices to calculate volume weighted stock price from Transaction_data.csv file
        Default value for time period to check volume weighted stock price is 5 minutes <2.a.iv>

Method "GeoMeanVolWeightedPrice" : This function will give us geometric mean of volume weighted price of all the stocks <2.b>
