from re import S
import streamlit as st
from datetime import datetime, date
from pathlib import Path
import time
from yahooquery import Ticker
import pandas as pd
import matplotlib.pyplot as plt

import src.models.strategy as s1
from src.tools import functions as f0
from src.tools import lists as l0

plt.style.use("ggplot")
sm, med, lg = "20", "25", "30"
plt.rcParams["font.size"] = sm  # controls default text sizes
plt.rc("axes", titlesize=med)  # fontsize of the axes title
plt.rc("axes", labelsize=med)  # fontsize of the x & y labels
plt.rc("xtick", labelsize=sm)  # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)  # fontsize of the tick labels
plt.rc("legend", fontsize=sm)  # legend fontsize
plt.rc("figure", titlesize=lg)  # fontsize of the figure title
plt.rc("axes", linewidth=2)  # linewidth of plot lines
plt.rcParams["figure.figsize"] = [15, 13]
plt.rcParams["figure.dpi"] = 113
plt.rcParams["axes.facecolor"] = "silver"


class Strategy(object):

    def __init__(self, today_stamp):
        self.today_stamp = str(today_stamp)[:10]
        self.saveMonth = str(datetime.now())[:7]
        self.saveDay = str(datetime.now())[8:10]
        
        
        st.header("โพ ๐๐๐๐๐ ยท Strategy ยท ๐๐๐๐๐ โพ")
        st.header(f"{' '*25}")


    def run_the_strats(self):
        method_strat = st.sidebar.selectbox("Select Method", ("Individual Strategy", "Run All Strategies"))
        
        
        if method_strat == "Run All Strategies":
            self.stock_ticker = st.sidebar.text_input(label="Enter Stock In ALL CAPS [example: TSLA]", value="")
            st.sidebar.write(" *" * 25)            
            if st.sidebar.button("Run Strategies"):
                self.run_movAvg_sma_ema(self.stock_ticker)
                self.run_optimal_sma(self.stock_ticker)
                self.run_overBought_overSold(self.stock_ticker)
                self.run_supportResistance(self.stock_ticker)
                # self.run_strategyII(self.stock_ticker)


        if method_strat == "Individual Strategy":
            model = st.sidebar.selectbox("Select Model", l0.feature_strategy, index=0)
            self.stock_ticker = st.sidebar.text_input(label="Enter Stock In ALL CAPS [example: TSLA]", value="TSLA")

            if model == "-Select-Model-":
                self.run_homePage()
                
            else:
                if st.sidebar.button("Implement Strategy"):

                    if model == "Moving-Average":
                        st.sidebar.write("__" * 25)
                        self.run_movAvg_sma_ema(self.stock_ticker)

                    if model == "Optimal SMA":
                        self.run_optimal_sma(self.stock_ticker)

                    if model == "OverBought & OverSold":
                        self.run_overBought_overSold(self.stock_ticker)

                    if model == "Support & Resistance Lines":
                        self.run_supportResistance(self.stock_ticker)

                    if model == "Strategy II":
                        self.run_strategyII(self.stock_ticker)
                        
                    if model == "Indicators":
                        self.run_indicators(self.stock_ticker)


    def run_homePage(self):       
        cols = st.columns(2)
        with cols[0]:        
            with st.expander("โณ Details", expanded=False):
                st.caption(" ")
                st.write("โฟ Moving Averages")
                st.caption(
                    """
                    * Double Moving Averages
                    * Exponential Moving Average (EMA)
                    * Simple Moving Average (SMA)
                    * Bollinger Bands
                    * MOM
                    * MACD
                    * RSI
                    * APO
                    """
                    )
                st.caption(" ")
                st.caption("_"*13)
                st.write("โฟ Regression")
                st.caption(" \n\
                    * Linear Regression \n\
                    * Quadratic Regression 2 & 3 \n\
                    * KNN \n\
                    * Lasso \n\
                    * Ridge \n\
                    * Logistic Regression \n\
                    "
                    )
                st.caption(" ")
                st.caption("_"*13)
                st.write("โฟ Speciality Trading")
                st.caption(
                    """
                    * naive momentum
                    * Pairs Correlation Trading
                    * Support & Resistance
                    * Turtle Trading
                    * Mean Reversion & Trend Following
                    * Volatility Mean Reversion & Trend Following
                    * OverBought & OverSold
                    """
                   )
                st.caption(" ")
                st.caption("_"*13)
                st.write("โฟ Strategy Backtesting")
                st.caption("* xgboost sim/backtesting")
                st.caption("* backtrader backtesting")
                st.caption(" ")


    def run_movAvg_sma_ema(self, stock_ticker):
        st.header("๐๐๐๐๐ Optimal Double Moving Average ๐๐๐๐๐")
        st.header(f"{' '*25}")
        S, L = s1.optimal_2sma(stock_ticker).grab_data(self.today_stamp)
        s1.movAvg_sma_ema(stock_ticker, S, L, self.today_stamp, 'SMA')
        st.write('*'*34)
        s1.movAvg_sma_ema(stock_ticker, S, L, self.today_stamp, 'EWMA')
        st.subheader("๐๐๐๐๐ Strategy Complete")
        

    def run_optimal_sma(self, stock_ticker, graphit=True, cc=0.0, ccc=0.0):
        st.header("๐๐๐๐๐ Optimal Single Moving Averages ๐๐๐๐๐")
        st.header(f"{' '*25}")
        s1.optimal_sma(stock_ticker, self.today_stamp).build_optimal_sma(graphit, cc, ccc)
        
    def run_indicators(self, stock_ticker):
        st.header("๐๐๐๐๐ Indicator Analysis ๐๐๐๐๐")
        st.header(f"{' '*25}")
        # s1.Indicator_Ike(stock_ticker).kingpin()

    def run_overBought_overSold(self, stock_ticker):
        st.header("๐๐๐๐๐๐๐ Over Bought & Over Sold Analysis ๐๐๐๐๐๐๐")
        st.header(f"{' '*25}")
        s1.overBought_overSold(stock_ticker).generate()

    def run_supportResistance(self, stock_ticker):
        st.header("๐๐๐๐๐๐๐ Support & Resistance Analysis ๐๐๐๐๐๐๐")
        st.header(f"{' '*25}")
        s1.support_resistance(stock_ticker).level()

    def run_strategyII(self, stock_ticker):
        st.header("๐๐๐๐๐๐๐๐๐๐ Strategy II Analysis ๐๐๐๐๐๐๐๐๐๐")
        st.header(f"{' '*25}")
        s1.Trading_Technicals(stock_ticker).trading_technicals()
