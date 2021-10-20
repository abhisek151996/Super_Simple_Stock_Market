import pandas as pd
import time
from datetime import datetime

class SimpleStockMarket:
    ## stockrecords is the static data of each stock and it contains columns as stock symbol, type, last dividend, fixed dividend and par value
    ## we are converting the static data into pandas datframe
    stockrecords = pd.read_csv("Stockrecords.csv")
    stockrecords["Stock Symbol"] = stockrecords["Stock Symbol"].str.strip()
    stockrecords["Type"] = stockrecords["Type"].str.strip()
    #stockrecords["Fixed Dividend"]=str(stockrecords["Fixed Dividend"]).replace('%','')

    def __init__(self):
        pass
    def DivindendYield(self,stocksymbol,price):
        '''The function will give us dividend yield of a stock using  last dividend
        for common type of stock and par value for preffred type of stock <Point 2.a.1>'''
        
        if price>0:
            if str(stocksymbol) in list(SimpleStockMarket.stockrecords["Stock Symbol"]):
                stocktype = list(SimpleStockMarket.stockrecords[SimpleStockMarket.stockrecords["Stock Symbol"]==str(stocksymbol)]["Type"])
                if 'Common' in stocktype:
                    lastDividend = float(SimpleStockMarket.stockrecords[SimpleStockMarket.stockrecords["Stock Symbol"]==str(stocksymbol)]["Last Dividend"])
                    divyield = lastDividend/float(price)
                    return divyield
                elif 'Preferred' in stocktype:
                    fixedDividend = list(SimpleStockMarket.stockrecords[SimpleStockMarket.stockrecords["Stock Symbol"]==str(stocksymbol)]["Fixed Dividend"])[0].replace('%','')
                    parValue = float(SimpleStockMarket.stockrecords[SimpleStockMarket.stockrecords["Stock Symbol"]==str(stocksymbol)]['Par Value'])
                    divyield = (float(fixedDividend)*parValue)/float(price)
                    return divyield
                else:
                    return 'Stock Type is not matched with the stock type of given stock'
            else:
                return 'Stock Symbol is not in static database'
        else:
            return 'Price should be numeric value and greater than zero'

    def PEratio(self,stocksymbol,price):
        '''The function will calculate P/E ratio using price and dividend of a stock.
        Dividend is calculated using the function DivindendYield(self,stocksymbol,price) of class SimpleStockMarket <2.a.ii>'''
        dividend_obj = SimpleStockMarket().DivindendYield(stocksymbol,price)
        perat = price/dividend_obj
        return perat

    def recordtrade(self,stocksymbol,quantity,indicator,price):
        '''The function will store data in Transaction_data.csv file. It will store current timestamp, Stock Symbol which will be bought or sold, How much of the stock will be bough or sold,
        Indicator will contain either of two string BUY or SOLD, Price will contain the amount involved during that transaction <2.a.iii>'''

        now = datetime.now()
        current_time = now.strftime("%y-%m-%d %H:%M:%S")
        timestamp = time.mktime(datetime.strptime(current_time,"%y-%m-%d %H:%M:%S").timetuple())
        if str(stocksymbol) not in list(SimpleStockMarket.stockrecords["Stock Symbol"]):
            return 'Stock Symbol is not in static database'
        if isinstance(quantity, int) or isinstance(quantity, float):
            pass
        else:
            return 'Quantity of the stock must be numeric'
        if quantity>0:
            pass
        else:
            return 'Quantity of the stock must be positive value'
        if indicator not in ['BUY', 'SELL']:
            return 'Indicator must be either of two string BUY or SELL'
        if isinstance(price, int) or isinstance(price, float):
            pass
        else:
            return 'Price of the stock must be numeric'
        if price>=0:
            pass
        else:
            return 'price must be greater than equal zero'
             
        row={"Timestamp":[timestamp],"Stock Symbol":[str(stocksymbol)],"Quantity":[quantity],"Indicator":[indicator],"Price":[price]}
        transaction = pd.read_csv("Transaction_data.csv")
        transac = pd.DataFrame(row)
        transaction = transaction.append(transac)
        transaction.to_csv('Transaction_data.csv', index=False)

        return 'One transaction has been made for stock',stocksymbol
    
    def VolumeWeightedPrice(self,stocksymbol,time_gap=300):
        '''This function will take the stock symbol as parameter and it will find volume weighted stock price of transaction.
        It will take quantity and prices to calculate volume weighted stock price from Transaction_data.csv file
        Default value for time period to check volume weighted stock price is 5 minutes <2.a.iv>'''

        now = datetime.now()
        current_time = now.strftime("%y-%m-%d %H:%M:%S")
        timestamp = time.mktime(datetime.strptime(current_time,"%y-%m-%d %H:%M:%S").timetuple())
        time_to_check = int(timestamp)-int(time_gap)

        transaction = pd.read_csv("Transaction_data.csv")
        transaction_five_mins = transaction[(transaction["Stock Symbol"]==str(stocksymbol)) & (transaction["Timestamp"]>time_to_check)]
        if transaction_five_mins.shape[0]>0:
            transaction_five_mins["Quantity_Price"] = transaction_five_mins["Quantity"]*transaction_five_mins["Price"]
            Total_quantity = transaction_five_mins["Quantity"].sum()
            Total_quantity_price = transaction_five_mins["Quantity_Price"].sum()
            VWPrice = Total_quantity_price/Total_quantity
            return VWPrice
        else:
            return "No trasaction has occured in last 5 minutes for given stock"
        
    
    def GeoMeanVolWeightedPrice(self):
        '''This function will give us geometric mean of volume weighted price of all the stocks <2.b>'''
        
        transaction = pd.read_csv("Transaction_data.csv")
        transaction["Quantity_Price"] = transaction["Quantity"]*transaction["Price"]
        transaction_Vol_Weight = transaction.groupby("Stock Symbol")[["Quantity", "Quantity_Price"]].sum()
        transaction_Vol_Weight["VolWeightPrice"] = transaction_Vol_Weight["Quantity_Price"]/transaction_Vol_Weight["Quantity"]
        total_multi_VWP=transaction_Vol_Weight["VolWeightPrice"].product()
        GeoMeanStocks = total_multi_VWP**(1/len(transaction_Vol_Weight["VolWeightPrice"]))

        return GeoMeanStocks