#!/usr/bin/env python
# coding: utf-8

# In[23]:


#from yahoo_finance import Share
import pandas as pd
import yfinance as yf
#from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt
import datetime as dt
import xlwings as xw

def DCF():
    wb = xw.Book.caller()
    # In[37]:


    wb = xw.Book('DCF Model.xlsm')
    overview = wb.sheets['Overview']
    DCF = wb.sheets['DCF Model']
    WACC = wb.sheets['WACC']
    IS = wb.sheets['Income Statement']
    BS = wb.sheets['Balance Sheet Statement']
    CF = wb.sheets['Cash Flow Statement']
    
    
    code = overview.range('C3').value


    # # Return the full company name

    # In[38]:


    # code = input("Enter Share Code (don't need .ax): ")

    code = code+'.ax'
    ticker = yf.Ticker(code)
    Name = ticker.info['longName']
    print(Name)
    overview.range('F3').clear()
    overview.range('F3').value = Name


    # # Website Link

    # In[39]:


    Website = ticker.info['website']
    print(Website)
    overview.range('I3').clear()
    overview.range('I3').value = Website


    # # Industry

    # In[4]:


    Industry = ticker.info['industry']
    print(Industry)
    overview.range('C5').clear()
    overview.range('C5').value = Industry


    # # Previous Close Price

    # In[5]:


    # print(ticker.info['previousClose'])
    price = ticker.history(period='1d')['Close'][0]
    print(price)
    overview.range('F5').clear()
    overview.range('F5').value = price


    # # Dividend Yield

    # In[6]:


    Div_Yield = ticker.info["dividendYield"]
    print(Div_Yield)
    overview.range('J5').clear()
    overview.range('J5').value = Div_Yield


    # # Company Blurb

    # In[7]:


    Blurb = ticker.info['longBusinessSummary']
    print(Blurb)
    overview.range('B9').clear()
    overview.range('B9').value = Blurb


    # # DCF Model

    # ## Tax Rate

    # In[8]:


    fin_df = ticker.financials
    fin_df = fin_df.fillna(0)
    inc_b4_tax = fin_df.loc['Income Before Tax'][0]
    inc_tax_exp = fin_df.loc['Income Tax Expense'][0]
    # Tax_Rate = inc_tax_exp/inc_b4_tax
    Tax_Rate = 0.3
    print(Tax_Rate)


    # ## Transaction Date

    # In[9]:


    transaction_date = dt.date.today().strftime("%Y-%m-%d")
    print(transaction_date)
    DCF.range('D9').clear()
    DCF.range('D9').value = transaction_date


    # ## Fiscal Year End

    # In[10]:


    fiscal_EOY = (dt.datetime.utcfromtimestamp(int(ticker.info['nextFiscalYearEnd']))-dt.timedelta(days=365)).strftime('%Y-%m-%d')
    print(fiscal_EOY)
    DCF.range('D10').clear()
    DCF.range('D10').value = fiscal_EOY

    # ## Shares Outstanding

    # In[11]:


    shares_out = ticker.info['sharesOutstanding']
    print(shares_out)
    DCF.range('D12').clear()
    DCF.range('D12').value = shares_out


    # ## Total Debt

    # In[12]:


    bal_df = ticker.balance_sheet
    bal_df = bal_df.fillna(0)
    Debt = sum(bal_df.loc[bal_df.index[bal_df.index.str.find('Debt')!=-1]].iloc[:,0])
    print(Debt)
    DCF.range('D13').clear()
    DCF.range('D13').value = Debt


    # ## Total Cash

    # In[13]:


    Cash = bal_df.loc['Cash'][0]
    print(Cash)
    DCF.range('D15').clear()
    DCF.range('D15').value = Cash


    # ## Capital Expenditure

    # In[14]:


    cash_df = ticker.cashflow
    cash_df = cash_df.fillna(0)
    CapEx = cash_df.loc['Capital Expenditures'][0]
    print(CapEx)
    DCF.range('D16').clear()
    DCF.range('D16').value = CapEx


    # ## Shareholder Equity

    # In[15]:


    share_equity = bal_df.loc['Total Stockholder Equity'][0]
    print(share_equity)
    DCF.range('D13').clear()
    DCF.range('D13').value = share_equity


    # ## Cost of Debt

    # In[16]:

    if Debt == 0:
        Cost_Debt = 0
    else:
        Cost_Debt = -fin_df.loc['Interest Expense'][0]/Debt
    print(Cost_Debt)
    WACC.range('C8').clear()
    WACC.range('C8').value = Cost_Debt


    # ## EV/EBITDA Multiple

    # In[17]:


    EBITDA_Mult = ticker.info['enterpriseToEbitda']
    print(EBITDA_Mult)
    DCF.range('D8').clear()
    DCF.range('D8').value = EBITDA_Mult


    # ## Levered Beta

    # In[18]:


    beta = ticker.info['beta']
    print(beta)
    WACC.range('C5').clear()
    WACC.range('C5').value = beta

    # ## Market Cap
    # In[19]:
    mcap = ticker.info['marketCap']
    DCF.range('D17').clear()
    DCF.range('D17').value = mcap

    wb.sheets("Income Statement").clear()
    wb.sheets("Balance Sheet Statement").clear()
    wb.sheets("Cash Flow Statement").clear()
    IS.range('A1').value = fin_df
    BS.range('A1').value = bal_df
    CF.range('A1').value = cash_df
    
if __name__ == '__main__':
    # Expects the Excel file next to this source file, adjust accordingly.
    xw.Book('DCF Model.xlsm').set_mock_caller()
    DCF()

