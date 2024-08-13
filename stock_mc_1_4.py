# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:58:34 2024

@author: arvind.prasad
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns
from scipy.stats import norm


class montecarlo:
    
    
    def __init__(self,stock_data_frame,days=50,trials=100):
        
        self.days=days
        self.trials=trials
        self._stock_data_frame=stock_data_frame
        
    
    
    
    
    def simulation(self):
        
        self._log_return=np.log(1+self._stock_data_frame.pct_change().iloc[1:])
        
        self._ret_mean=self._log_return.mean().values
        
        self._ret_var=self._log_return.var().values
        
        self._ret_std=self._log_return.std().values
        
        self._drift=self._ret_mean-0.5*self._ret_var
        
        #print(self.ret_mean,self.ret_std,self.ret_var)
        
        self._volatility=self._ret_std*norm.ppf(np.random.rand(self.days,self.trials))
        
        self._daily_return=np.exp(self._drift+self._volatility)
        
        
        self._price_list = np.zeros_like(self._daily_return)
        
        # Put the last actual price in the first row of matrix. 
        
        self._price_list[0] = self._stock_data_frame.iloc[-1]

        
        #Calculate the price of each day
        

        for self._day_progress in range(1,self.days):
            
            
            self._price_list[self._day_progress] = self._price_list[self._day_progress-1]*self._daily_return[self._day_progress]
        
        
        return pd.DataFrame(self._price_list)
            
        
    def prob_lt_ret(self,exp_ret=10):
        
        self._fut_ret=exp_ret
        
        self._stock_unit_price=pd.DataFrame(self._price_list)

        self._lt_count=0
        
        self._predicted_ret=100*(self._stock_unit_price.iloc[-1]-self._stock_unit_price.iloc[0])/self._stock_unit_price.iloc[0]
    
        for self._ret in range(self._predicted_ret.count()):
            if self._predicted_ret.iloc[self._ret] < exp_ret:
                self._lt_count+=1
        
        self._p_lt=self._lt_count/self._predicted_ret.count()

        return self._p_lt
          
        
    
   
    
 





    

class stock:
    def __init__(self,ticker):
        
        
        self.ticker=ticker
        
        
        self._raw_data=yf.download(self.ticker,period="5y",interval="1d")['Adj Close']
        self._stock_data_frame=pd.DataFrame(self._raw_data)
        self._stock_unit_download=self._stock_data_frame
        self._stock_unit_download[self.ticker]=self._stock_unit_download
        
        del self._stock_unit_download['Adj Close']
        self.stock_list_price=self._stock_unit_download
        
        
    
    def plot(self):
        
        self._stock_price=self._stock_data_frame
        self._stock_price.plot()
        plt.grid()
    
    
    
   
    def plr(self):
        
        self._stock_return=np.log(1+self._stock_data_frame.pct_change().iloc[1:])
        self._stock_return.plot()
        plt.grid()
   
    
   
    def plrhist(self):
        
        self._stock_return=np.log(1+self._stock_data_frame.pct_change().iloc[1:])
        sns.histplot(self._stock_return)
        plt.grid()
   
    