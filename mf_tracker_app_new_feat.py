# --- Import libraries ---
import pandas as pd
#from nselib import capital_market
import numpy as np
import matplotlib.pyplot as plt
from mftool import Mftool
from yahooquery import Ticker
from datetime import date
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
#from jugaad_data.nse import index_raw
import yfinance as yf
import re
from typing import List, Optional
from nsetools import Nse
from nsepython import index_history
import streamlit as st
import time
import plotly.express as px

# --- Global Declarations ---
TDY_DATE = pd.to_datetime(datetime.datetime.today()).strftime("%d-%b-%Y")
POINT_TO_POINT_RETURN_PERIODS = ["1M","3M","6M","1Y","3Y","5Y","10Y","All"]
ROLLING_RETURN_PERIODS = ["1Y","3Y","5Y","10Y"]
mf = Mftool()
nse = Nse()

# --- Funds Declerations ---
MULTI_ASSET = {
    "Benchmark": ["NIFTY 500"],
    "Funds": {
        "Kotak Multi Asset Allocation Fund - Direct Plan - Growth Option":"Kotak Multiasset",
        "Axis Multi Asset Allocation Fund - Direct Plan - Growth Option": "Axis Multiasset",
        "Nippon India Multi Asset Allocation Fund - Direct Plan - Growth Option": "Nippon Multiasset",
        "LIC MF Multi Asset Allocation Fund-Direct Plan-Growth": "LIC Multiasset",
        "Mahindra Manulife Multi Asset Allocation Fund- Direct Plan - Growth": "Mahindra Manulife Multiasset",
        "HDFC Multi-Asset Fund - Growth Option - Direct Plan": "HDFC Multiasset",
        "ICICI Prudential Multi-Asset Fund - Direct Plan - Growth": "ICICI Multiasset",
        "Baroda BNP Paribas Multi Asset Fund - Direct Plan - Growth Option": "Baroda BNP Multiasset",
        "Bandhan Multi Asset Allocation Fund - Direct Plan - Growth": "Bandhan Multiasset",
        "Sundaram Multi Asset Allocation Fund Direct Plan Growth": "Sundaram Multiasset",
        "Invesco India Multi Asset Allocation Fund - Direct Plan - Growth": "Invesco Multiasset",
        "Aditya Birla Sun Life Multi Asset Allocation Fund-Direct Growth": "Aditya Birla Multiasset",
        "HSBC Multi Asset Allocation Fund - Direct - Growth": "HSBC Multiasset",
        "Union Multi Asset Allocation Fund- Direct Plan - Growth Option": "Union Multiasset",
        "SBI MULTI ASSET ALLOCATION FUND - DIRECT PLAN - GROWTH": "SBI Multiasset",
        "quant Multi Asset Allocation Fund - IDCW Option - Direct Plan": "Quant Multiasset",
        "Canara Robeco Multi Asset Allocation Fund - Direct Plan - Growth": "Canara Robeco Multiasset",
        "Bank of India Multi Asset Allocation Fund-Direct Plan-Growth": "BoI Multiasset",
        "Edelweiss Multi Asset Allocation Fund - Direct Plan - Growth": "Edelweiss Multiasset",
        "Mirae Asset Multi Asset Allocation Fund - Direct Plan - Growth": "Mirae Asset Multiasset",
        "Tata Multi Asset Allocation Fund-Direct Plan-Growth": "Tata Multiasset",
        "Bajaj Finserv Multi Asset Allocation Fund - Direct Growth":"Bajaj Multiasset",
        "PGIM India Multi Asset Allocation Fund - Direct Plan - Growth Option": "PGIM Multiasset",
        "Franklin India Multi Asset Allocation Fund- Direct-Growth": "Franklin Multiasset",
        "DSP Multi Asset Allocation Fund - Direct - Growth": "DSP Multiasset",
        "WhiteOak Capital Multi Asset Allocation Fund Direct Plan Growth": "Whitoak Mulitasset",
        "UTI Multi Asset Allocation Fund - Direct Plan - Growth Option": "UTI Multiasset",
        "Groww Multi Asset Allocation Fund Direct Growth": "Groww Multiasset",
        "Shriram Multi Asset Allocation Fund - Direct Growth": "Shriram Multiasset",
        "Samco Multi Asset Allocation Fund - Direct Plan - Growth": "Samco Multiasset",
        "Quantum Multi Asset Allocation Fund - Direct Plan Growth Option": "Quantum Multiasset",
        "360 ONE Multi Asset Allocation Fund - Direct Plan - Growth": "360One Multiasset",
    }
}

MULTI_CAP = {
    "Benchmark": ["NIFTY500 MULTICAP"],
    "Funds": {
        "Kotak Multicap Fund-Direct Plan-Growth":"Kotak Multicap",
        "Axis Multicap Fund - Direct Growth": "Axis Multicap",
        "Nippon India Multi Cap Fund - Direct Plan Growth Plan - Growth Option": "Nippon Multicap",
        "LIC MF Multi Cap Fund-Direct Plan-Growth": "LIC Multicap",
        "Mahindra Manulife Multi Cap Fund - Direct Plan -Growth": "Mahindra Manulife Multicap",
        "ITI Multi Cap Fund - Direct Plan - Growth Option": "ITI Multicap",
        "HDFC Multi Cap Fund - Growth Option - Direct Plan": "HDFC Multicap",
        "ICICI Prudential Multicap Fund - Direct Plan -  Growth": "ICICI Multicap",
        "Baroda BNP Paribas MULTI CAP FUND - Direct Plan - Growth Option": "Baroda BNP Multicap",
        "BANDHAN MULTI CAP FUND - GROWTH - DIRECT PLAN": "Bandhan Multicap",
        "Sundaram Multi Cap Fund (Formerly Known as Principal Multi Cap Growth Fund)-Direct Plan - Growth Option": "Sundaram Multicap",
        "Invesco India Multicap Fund - Direct Plan - Growth Option": "Invesco Multicap",
        "Aditya Birla Sun Life Multi-Cap Fund-Direct Growth": "Aditya Birla Multicap",
        "HSBC Multi Cap Fund - Direct - Growth": "HSBC Multicap",
        "Union Multicap Fund - Direct Plan - Growth Option": "Union Multicap",
        "SBI Multicap Fund- Direct Plan- Growth option": "SBI Multicap",
        "quant Multi Cap Fund-GROWTH OPTION-Direct Plan": "Quant Mulitcap",
        "Canara Robeco Multi Cap Fund - Direct Plan - Growth Option": "Canara Robeco Multicap",
        "Bank of India Multi Cap Fund Direct Plan - Growth": "BoI Multicap",
        "Edelweiss Multi Cap Fund - Direct Plan - Growth": "Edelweiss Multicap",
        "Mirae Asset Multicap Fund - Direct Plan - Growth": "Mirae Asset Multicap",
        "Tata Multicap Fund - Direct Plan - Growth": "Tata Multicap",
        "BAJAJ FINSERV MULTI CAP FUND - DIRECT - GROWTH": "Bajaj Multicap",
        "PGIM India Multi Cap Fund - Direct Plan - Growth Option": "PGIM Muticap",
        "Franklin India Multi Cap Fund - Direct - Growth": "Franklin Multicap",
        "DSP Multicap Fund - Direct - Growth": "DSP Multicap",
        "WhiteOak Capital Multi Cap Fund Direct Plan Growth": "Whiteoak Multicap",
        "UTI Multi Cap Fund - Direct Plan - Growth Option": "UTI Multicap",
        "Groww Multicap Fund - Direct - Growth": "Groww Multicap",
        "Motilal Oswal Multi Cap Fund-Direct Plan Growth": "Motilal Multicap",        
    }
}

FLEXI_CAP = {
    "Benchmark": ["NIFTY 500","NIFTY500 FLEXICAP"],
    "Funds": {
        "Parag Parikh Flexi Cap Fund - Direct Plan - Growth":"PPFAS Flexicap",
        "Invesco India Flexi Cap Fund - Direct Plan - Growth": "Invesco Flexicap",
        "Mirae Asset Flexi Cap Fund - Direct Plan - Growth": "Mirae Asset Flexicap",
        "Motilal Oswal Flexi cap Fund Direct Plan-Growth Option": "Motilal Oswal Flexicap",
        "BANK OF INDIA Flexi Cap Fund Direct Plan -Growth": "BoI Flexicap",
        "HDFC Flexi Cap Fund - Growth Option - Direct Plan": "HDFC Flexicap",
        "JM Flexicap Fund (Direct) - Growth Option": "JM Flexicap",
        "WhiteOak Capital Flexi Cap Fund Direct Plan-Growth": "WhiteOak Capital Flexicap",
        "Edelweiss Flexi Cap Fund - Direct Plan - Growth Option": "Edelweiss Flexicap",
        "ICICI Prudential Flexicap Fund - Direct Plan - Growth": "ICICI Flexicap",
        "HSBC Flexi Cap Fund - Direct Growth": "HSBC Flexicap",
        "Aditya Birla Sun Life Flexi Cap Fund - Growth - Direct Plan": "Aditya Birla Flexicap",
        "DSP Flexi Cap Fund - Direct Plan - Growth": "DSP Flexicap",
        "Mahindra Manulife Flexi Cap Fund - Direct Plan -Growth":"Mahindra Manulife Flexicap",
        "Franklin India Flexi Cap Fund - Direct - Growth": "Franklin Flexicap",
        "Tata Flexi Cap Fund-Direct Plan-Growth": "Tata Flexicap",
        "Nippon India Flexi Cap Fund - Direct Plan - Growth Plan - Growth Option": "Nippon Flexicap",
        "Baroda BNP Paribas Flexi Cap Fund - Direct Plan - Growth Option": "Baroda BNP Flexicap",
        "quant Flexi Cap Fund - Growth Option-Direct Plan": "Quant Flexicap",
        "Kotak Flexicap Fund - Growth - Direct": "Kotak Flexicap",
        "CANARA ROBECO FLEXICAP FUND - DIRECT PLAN - GROWTH OPTION": "Canara Robeco Flexicap",
        "BANDHAN Flexi Cap Fund-Direct Plan-Growth": "Bandhan Flexicap",
        "Sundaram Flexicap Fund Direct Growth": "Sundaram Flexicap",
        "Union Flexi Cap Fund - Direct Plan - Growth Option": "Union Flexicap",
        "Axis Flexi Cap Fund - Direct Plan - Growth": "Axis Flexicap",
        "Navi Flexi Cap Fund - Direct Plan - Growth": "Navi Flexicap",
        "SBI Flexicap Fund - DIRECT PLAN - Growth Option": "SBI FLexicap",
        "PGIM India Flexi Cap Fund - Direct Plan - Growth Option":"PGIM Flexicap",
        "360 ONE FLEXICAP FUND-DIRECT PLAN- GROWTH": "360 One Flexicap",
        "Helios Flexi Cap Fund - Direct Plan - Growth Option": "Helios Flexicap",
        "JioBlackRock Flexi Cap Fund - Direct Plan - Growth Option": "Jio Blackrock Flexicap",
        "CAPITALMIND FLEXI CAP FUND DIRECT GROWTH": "CapitalMind Flexicap",
        "Abakkus Flexi Cap Fund - Direct - Growth": "Abakkus Flexicap",
        "Shriram Flexi Cap Fund - Direct Growth": "Shriram Flexicap",
        "UTI Flexi Cap Fund - Direct Plan - IDCW": "UTI Flexicap",
        "Samco Flexi Cap Fund - Direct Plan - Growth Option": "Samco Flexicap",
        "ITI Flexi Cap Fund- Direct Plan- Growth": "ITI Flexicap",
        "Bajaj Finserv Flexi Cap Fund-Direct Plan-Growth": "Bajaj Finserv Flexicap",
        "NJ Flexi Cap Fund - Direct Plan - Growth Option": "NJ Flexicap",
        "TRUSTMF Flexi Cap Fund-Direct Plan- Growth": "TrustMF Flexicap",
        "Unifi Flexi Cap Fund - Direct Growth": "unifi Flexicap",
        "THE WEALTH COMPANY FLEXI CAP FUND - DIRECT GROWTH": "Wealthcomp Flexicap"
    }
}

LARGE_CAP = {
    "Benchmark": ["NIFTY 50"],
    "Funds": {
        "Nippon India Large Cap Fund - Direct Plan Growth Plan - Growth Option":"Nippon Largecap",
        "CANARA ROBECO LARGE CAP FUND - DIRECT PLAN - GROWTH OPTION": "Canara Robeco Largecap",
        "Invesco India Largecap Fund - Direct Plan - Growth": "Invesco Largecap",
        "DSP Large Cap Fund - Direct Plan - Growth": "DSP Largecap",
        "BANDHAN Large Cap Fund-Direct Plan-Growth": "Bandhan Largecap",
        "ICICI Prudential Large Cap Fund (erstwhile Bluechip Fund) - Direct Plan - Growth": "ICICI Largecap",
        "WhiteOak Capital Large Cap Fund Direct Plan Growth": "WhiteOak Capital Largecap",
        "BARODA BNP PARIBAS LARGE CAP Fund - Direct Plan - Growth Option": "Baroda BNP Largecap",
        "BANK OF INDIA Large Cap Fund Direct Plan Growth": "BoI Largecap",
        "Edelweiss Large Cap Fund - Direct Plan-Growth option": "Edelweiss Largecap",
        "JM Large Cap Fund (Direct) - Growth Option": "JM Largecap",
        "Kotak Large Cap  Fund - Growth - Direct": "Kotak Largecap",
        "HDFC Large Cap Fund - Growth Option - Direct Plan": "HDFC Largecap",
        "quant Large Cap Fund - Growth Option - Direct Plan": "Quant Largecap",
        "Mahindra Manulife Large Cap Fund - Direct Plan -Growth": "Mahindra Manulife Largecap",
        "HSBC Large Cap Fund - Direct Growth": "HSBC Largecap",
        "Tata Large Cap Fund -Direct Plan Growth Option": "Tata Largecap",
        "Franklin India Large Cap Fund- Direct - Growth": "Franklin Largecap",
        "ITI Large Cap Fund - Direct Plan - Growth Option": "ITI Largecap",
        "SBI Large Cap FUND-DIRECT PLAN -GROWTH": "SBI Largecap",
        "Groww Largecap Fund (formerly known as Indiabulls Blue Chip Fund) - Direct Plan - Growth Option": "Groww Largecap",
        "Mirae Asset Large Cap Fund - Direct Plan - Growth": "Mirae Asset Largecap",
        "UTI Large Cap Fund - Direct Plan - Growth Option": "UTI Largecap",
        "PGIM India Large Cap Fund - Direct Plan - Growth": "PGIM Largecap",
        "Sundaram Large Cap Fund (Formerly Known as Sundaram Blue Chip Fund)Direct Plan - Growth": "Sundaram Largecap",
        "Axis Large Cap Fund - Direct Plan - Growth": "Axis Largecap",
        "Motilal Oswal Large Cap Direct Plan Growth": "Motilal Oswal Largecap",
        'JioBlackRock Large Cap Fund - Direct Plan - Growth Option': "Jio Blackrock Largecap",
        'Aditya Birla Sun Life Large Cap Fund - Growth - Direct Plan': "Aditya Birla Largecap",
        'BAJAJ FINSERV LARGE CAP FUND - DIRECT PLAN - GROWTH': "Bajaj Finserv Largecap",
        "LIC MF Large Cap Fund-Direct Plan-Growth": "LIC Largecap",
        "Parag Parikh Large Cap Fund - Direct Plan - Growth": "Parag Parikh Largecap",
        "Samco Large Cap Fund - Direct Plan - Growth Option": "Samco Largecap",
        "Taurus Large Cap Fund - Direct Plan - Growth": "Taurus Largecap"
    }
}

MID_CAP = {
    "Benchmark": ["NIFTY MIDCAP 150","NIFTY MIDCAP 50","NIFTY MIDCAP 100"],
    "Funds": {
        "Invesco India Midcap Fund - Direct Plan - Growth Option":"Invesco Midcap",
        "Motilal Oswal Midcap Fund-Direct Plan-Growth Option": "Motilal Oswal Midcap",
        "WhiteOak Capital Mid Cap Fund Direct Plan Growth": "WhiteOak Capital Midcap",
        "Edelweiss Mid Cap Fund - Direct Plan - Growth Option": "Edelweiss Midcap",
        "HSBC Midcap Fund - Direct Growth": "HSBC Midcap",
        "Canara Robeco Mid Cap Fund- Direct Plan- Growth Option": "Canara Robeco Midcap",
        "Mirae Asset Midcap Fund- Direct Growth Option": "Mirae Asset Midcap",
        "HDFC Mid Cap Fund - Growth Option - Direct Plan": "HDFC Midcap",
        "JM Midcap Fund (Direct) - Growth": "JM Midcap",
        "ITI Mid Cap Fund - Direct Plan - Growth Option": "ITI Midcap",
        "Mahindra Manulife Mid Cap Fund - Direct Plan -Growth": "Mahindra Manulife Midcap",
        "Nippon India Growth Mid Cap Fund - Direct Plan Growth Plan - Growth Option": "Nippon Midcap",
        "Sundaram Mid Cap Fund Direct Plan - Growth": "Sundaram Midcap",
        "ICICI Prudential MidCap Fund - Direct Plan -  Growth": "ICICI Midcap",
        "Tata Mid Cap Fund - Direct Plan- Growth Option": "Tata Midcap",
        "Franklin India Mid Cap Fund - Direct - Growth": "Franklin Midcap",
        "BANDHAN MIDCAP FUND - GROWTH - DIRECT PLAN": "Bandhan Midcap",
        "Kotak Midcap Fund - Direct Plan - Growth": "Kotak Midcap",
        "BARODA BNP PARIBAS Mid Cap Fund - Direct Plan - Growth Option": "Baroda BNP Midcap",
        "DSP Midcap Fund - Direct Plan - Growth": "DSP Midcap",
        "Axis Midcap Fund - Direct Plan - Growth": "Axis Midcap",
        "SBI MIDCAP FUND - DIRECT PLAN - GROWTH": "SBI Midcap",
        "UTI Mid Cap Fund-Growth Option- Direct": "UTI Midcap",
        "quant Mid Cap Fund - Growth Option - Direct Plan": "Quant Midcap",
        "PGIM India Midcap Fund - Direct Plan - Growth Option": "PGIM Midcap",
        "Helios Mid Cap Fund - Direct Plan - Growth Option": "Helios Midcap",
        "Bank of India Mid Cap Fund - Direct Plan Growth": "BoI Midcap",
        'LIC MF Mid Cap Fund-Direct Plan-Growth': "LIC Midcap",
        'Taurus Mid Cap Fund - Direct Plan - Growth': "Taurus Midcap",
        'TRUSTMF MID CAP FUND -DIRECT -GROWTH' : "TrustMF Midcap",
    }
}

SMALL_CAP = {
    "Benchmark": ["NIFTY SMLCAP 250","NIFTY SMLCAP 100","NIFTY SMLCAP 50"],
    "Funds": {
        "BANDHAN SMALL CAP FUND - DIRECT PLAN GROWTH":"Bandhan Smallcap",
        "Nippon India Small Cap Fund - Direct Plan Growth Plan - Growth Option":"Nippon Smallcap",
        "Invesco India Smallcap Fund - Direct Plan - Growth":"Invesco Smallcap",
        "quant Small Cap Fund - Growth Option - Direct Plan":"Quant Smallcap",
        "HDFC Small Cap Fund - Growth Option - Direct Plan":"HDFC Smallcap",
        "ITI Small Cap Fund - Direct Plan - Growth Option":"ITI Smallcap",
        "Edelweiss Small Cap Fund - Direct Plan - Growth":"Edelweiss Smallcap",
        "DSP Small Cap Fund - Direct Plan - Growth":"DSP Smallcap",
        "Sundaram Small Cap Fund Direct Plan - Growth":"Sundaram Smallcap",
        "Franklin India Small Cap Fund - Direct - Growth":"Franklin Smallcap",
        "Axis Small Cap Fund - Direct Plan - Growth":"Axis Smallcap",
        "HSBC Small Cap Fund - Direct Growth":"HSBC Smallcap",
        "BANK OF INDIA Small Cap Fund Direct Plan Growth":"BoI Smallcap",
        "Union Small Cap Fund - Direct Plan - Growth Option":"Union Smallcap",
        "CANARA ROBECO SMALL CAP FUND - DIRECT PLAN - GROWTH OPTION":"Canara Robeco Smallcap",
        "ICICI Prudential Smallcap Fund - Direct Plan - Growth":"ICICI Smallcap",
        "Tata Small Cap Fund-Direct Plan-Growth":"Tata Smallcap",
        "Motilal Oswal Small Cap Fund - Direct - Growth":"Motilal Oswal Smallcap",
        "Mirae Asset Small Cap Fund - Direct Plan - Growth":"Mirae Asset Smallcap",
        "Helios Small Cap Fund - Direct Plan - Growth Option":"Helios Smallcap",
        "Baroda BNP Paribas Small Cap Fund - Direct Plan - Growth option":"Baroda BNP Smallcap",
        "PGIM India Small Cap Fund - Direct Plan- Growth Option":"PGIM Smallcap",
        "UTI Small Cap Fund - Direct Plan - Growth Option":"UTI Smallcap",
        "JM Small Cap Fund (Direct) - Growth Option":"JM Smallcap",
        "Mahindra Manulife Small Cap Fund - Direct Plan - Growth":"Mahindra Manulife Smallcap",
        'Abakkus Small Cap Fund - Direct Plan - Growth':"Abakkus Smallcap",
        'Aditya Birla Sun Life Small Cap Fund - Growth - Direct Plan':"Aditya Birla Smallcap",
        'BAJAJ FINSERV SMALL CAP FUND - DIRECT - GROWTH':"Bajaj Finserv Smallcap",
        'Groww Small Cap Fund-Direct-Growth': "Groww Smallcap",
        'Kotak-Small Cap Fund - Growth - Direct': "Kotak Smallcap",
        'LIC MF Small Cap Fund-Direct Plan-Growth': "LIC Smallcap",
        'SBI Small Cap Fund - Direct Plan - Growth': "SBI Smallcap",
        'The Wealth Company Small Cap Fund- Direct-Growth' : "Wealthcomp Smallcap",
        'TRUSTMF SMALL CAP FUND -DIRECT PLAN-GROWTH' : "TrustMF Smallcap",
    }
}

CONTRA = {"Benchmark": ["NIFTY500 VALUE 50","NIFTY50 VALUE 20"],
    "Funds": {
        "Kotak Contra Fund - Direct Plan - Growth":"Kotak Contra",
        "Invesco India Contra Fund - Direct Plan - Growth": "Invesco Contra",
        "SBI CONTRA FUND - DIRECT PLAN - GROWTH": "SBI Contra",
        "Canara Robeco Value Fund - Direct Plan - Growth Option": "Canara Robeco Value",
        "Mahindra Manulife Value Fund - Direct Plan - Growth": "Mahindra Manulife Value",
        "Baroda BNP Paribas Value Fund - Direct Plan - Growth option": "Baroda BNP Value",
        "LIC MF Value Fund-Direct Plan-Growth": "LIC Value",
        "Groww Value Fund (formerly known as Indiabulls Value Fund) - Direct Plan - Growth Option": "Groww Value",
        "Quantum Value Fund - Direct Plan Growth Option": "Quantum Value",
        "HSBC Value Fund - Direct Growth": "HSBC Value",
        "UTI Value Fund - Direct Plan - Growth Option": "UTI Value",
        "Union Value Fund - Direct Plan - Growth Option": "Union Value",
        "Bandhan Value Fund - Direct Plan - Growth": "Bandhan Value",
        "HDFC Value Fund - Growth Option - Direct Plan": "HDFC Value",
        "ITI Value Fund - Direct Plan - Growth Option": "ITI Value",
        "DSP Value Fund - Direct Plan - Growth": "DSP Value",
        "Tata Value Fund -Direct Plan Growth Option": "Tata Value",
        "ICICI Prudential Value Fund (erstwhile Value Discovery Fund) - Direct Plan - Growth": "ICICI Value",
        "Aditya Birla Sun Life Value Fund - Growth - Direct Plan": "Aditya Birla Value",
        "JM Value Fund (Direct) - Growth Option": "JM Value",
        "Nippon India Value Fund - Direct Plan Growth Plan": "Nippon Value",
        "Quant Value Fund - Growth Option  - Direct Plan": "Quant Value",
        "Axis Value Fund - Direct Plan - Growth":"Axis Value",        
    }
}

FOCUSED = {"Benchmark": ["NIFTY500 VALUE 50"],
    "Funds": {
        "ICICI Prudential Focused Equity Fund - Direct Plan - Growth":"ICICI Focused",
        "Invesco India Focused Fund - Direct Plan - Growth": "Invesco India Focused",
        "HDFC Focused Fund - Growth Option - Direct Plan": "HDFC Focused",
        "HSBC Focused Fund - Direct Growth": "HSBC Focused",
        "Bandhan Focused Fund - Direct Plan - Growth": "Bandhan Focused",
        "Mahindra Manulife Focused Fund - Direct Plan -Growth": "Mahindra Manulife Focused",
        "DSP Focused Fund - Direct Plan - Growth": "DSP Focused",
        "UTI Focused Fund - Direct Plan - Growth Option": "UTI Focused",
        "Edelweiss Focused Fund - Direct Plan - Growth": "Edelweiss Focused",
        "SBI FOCUSED FUND - DIRECT PLAN -GROWTH": "SBI Focused",
        "JM Focused Fund (Direct)  - Growth Option": "JM Focused",
        "Canara Robeco Focused Fund - Direct Plan - Growth Option": "Canara Robeco Focused",
        "Kotak Focused Fund- Direct Plan- Growth option": "Kotak Focused",
        "Motilal Oswal Focused Fund - Direct Plan Growth Option": "Motilal Focused",
        "Aditya Birla Sun Life Focused Fund - Growth - Direct Plan": "Aditya Birla Focused",
        "360 ONE Focused Fund-Direct Plan-Growth": "360 One Focused",
        "BARODA BNP PARIBAS Focused Fund - Direct Plan - Growth Option": "Baroda BNP focused",
        "Franklin India Focused Equity Fund - Direct - Growth": "Franklin Focused",
        "Tata Focused Fund-Direct Plan-Growth": "Tata Focused",
        "Nippon India Focused Fund - Direct Plan Growth Plan - Growth Option": "Nippon Focused",
        "quant Focused Fund - Growth Option-Direct Plan": "Quant Focused",
        "Sundaram Focused Fund (Formerly Known as Principal Focused Multicap Fund)- Direct Plan - Growth Option": "Sundaram Focused",
        "Mirae Asset Focused Fund Direct Plan Growth": "Mirae Asset Focused",
        "Axis Focused Fund - Direct Plan - Growth Option": "Axis Focused",
        "Union Focused Fund - Direct Plan - Growth Option": "Union Focused",
        "ITI Focused Fund - Direct Plan - Growth": "ITI Focused"
    }
}

OTHER = {
    "Benchmark": ["NIFTY SMLCAP 250"],
    "Funds": {
        "Edelweiss Recently Listed IPO Fund Direct Plan Growth":"Edelweiss Recent IPO",
        "Kotak Special Opportunities Fund - Direct Plan - Growth Option":"Kotak Special Opp"
    }
}

BUSINESS_CYCLE = {
    "Benchmark": ["NIFTY 500"],
    "Funds": {
        "Axis Business Cycles Fund - Direct Plan - Growth": "Axis Business Cycle",
        "Edelweiss Business Cycle Fund - Direct Plan - Growth": "Edelweiss Business Cycle",
        "Kotak Business Cycle - Direct Plan - Growth": "Kotak Business Cycle",
        "Invesco India Business Cycle Fund - Direct Plan - Growth": "Invesco Business Cycle",
        "Sundaram Business Cycle Fund Direct Plan Growth": "Sundaram Business Cycle",
        "Bandhan Business Cycle Fund - Direct Plan - Growth": "Bandhan Business Cycle",
        "quant Business Cycle Fund - Growth Option - Direct Plan": "Quant Business Cycle",
        "Motilal Oswal Business Cycle Fund - Direct Plan- Growth": "Motilal Business Cycle",
        "ICICI Prudential Business Cycle Fund Direct Plan Growth": "ICICI Business Cycle",
        "Tata Business Cycle Fund-Direct Plan-Growth": "Tata Business Cycle",
        "HDFC Business Cycle Fund - Growth Option": "HDFC Business Cycle",
        "Aditya Birla Sun Life Business Cycle Fund-Direct Growth": "Aditya Birla Business Cycle",
    }
}

ACTIVE_MOMETUM = {
    "Benchmark": ["NIFTY200MOMENTM30","NIFTY500MOMENTM50"],
    "Funds": {
        "ICICI Prudential Active Momentum Fund - Direct Plan - Growth": "ICICI Active Momentum",
        'Kotak Active Momentum Fund - Direct Plan - Growth option': "Kotak Active Momentum",
        'Motilal Oswal Active Momentum Fund- Direct-Growth': "Motilal Active Momentum",
        'Nippon India Active Momentum Fund-Direct Plan - Growth Option': "Nippon Active Momentum",
        'Samco Active Momentum Fund - Direct Plan - Growth Option': "Samco Active Momentum",
        'Union Active Momentum Fund - Direct Plan - Growth Option': "Union Active Momentum"
    }
}

QUANT = {
    "Benchmark": ["NIFTY 50","NIFTY 500"],
    "Funds": {
        '360 ONE QUANT FUND DIRECT GROWTH': "360 One Quant",
        'Aditya Birla Sun Life Quant Fund - Direct Growth': "Aditya Birla Quant",
        'Axis Quant Fund - Direct Plan - Growth': "Axis Quant",
        'DSP Quant Fund - Direct Plan - Growth': "DSP Quant",
        'ICICI Prudential Quant Fund Direct Plan Growth': "ICICI Quant",
        'Kotak Quant Fund - Direct Plan - Growth Option': "Kotak Quant",
        'Motilal Oswal Quant Fund - Direct - Growth': "Motilal Oswal Quant",
        'Nippon India Quant Fund - Direct Plan Growth Plan - Growth Option': "Nippon Quant",
        'SBI Quant Fund- Direct Plan- Growth': "SBI Quant",
        'Tata Quant Fund-Direct Plan-Growth': "Tata Quant",
        'UTI Quant Fund - Direct Plan - Growth Option': "UTI Quant"
    }
}

INTERNATIONAL = {
    "Benchmark": ["NIFTY 500"],
    "Funds": {
        "Edelweiss US Technology Equity Fund of Fund- Direct Plan- Growth": "Edelweiss US Tech",
        "Edelweiss Greater China Equity Off-shore Fund - Direct Plan - Growth Option": "Edelweiss China Equity",
        "Edelweiss US Value Equity Offshore Fund - Direct Plan - Growth Option": "Edelweiss US Value Equity",
        "Edelweiss Europe Dynamic Equity Offshore Fund - Growth Option - Direct Plan": "Edelweiss Europe Dynamic Equity",
        "Edelweiss Emerging Markets Opportunities Equity Offshore Fund - Direct Plan - Growth Option": "Edelweiss Emerging Market",
        "Edelweiss ASEAN Equity Off-shore Fund - Direct Plan - Growth Option": "Edelweiss ASEAN Equity",
        
        "Invesco India - Invesco EQQQ Nasdaq-100 ETF Fund of Fund - Direct Plan - Growth": "Invesco EQQQ Nasdaq 100",
        "Invesco India - Invesco Global Consumer Trends Fund of Fund - Direct Plan - Growth": "Invesco Global Consumer",
        "Invesco India - Invesco Global Equity Income Fund of Fund - Direct Plan - Growth": "Invesco Global Equity",
        "Invesco India - Invesco Pan European Equity Fund of Fund - Direct Plan - Growth Option": "Invesco Europe Equity",
        
        "Franklin U.S. Opportunities Equity Active Fund of Funds - Direct - Growth": "Franklin US Opp",
        
        "Kotak US Equity Fund - Direct Plan - Growth option": "Kotak US Equities",
        "Kotak International REIT Overseas Equity Omni FOF - Direct Plan - Growth": "Kotak Int. REIT",
        "Kotak Global Innovation Overseas Equity Omni FOF- Direct Plan -Growth": "Kotak Global Innov",
        "Kotak Global Emerging Market overseas Equity Omni FOF - Growth - Direct": "Kotak Global Emerg Market",

        #"Axis US Specific Equity Passive FOF - Direct Plan - Growth": "Axis US Equity",
        "Axis Greater China Equity Fund of Fund - Direct Plan - Growth Option": "Axis Greater China",
        "Axis Global Innovation Fund of Fund - Direct Plan - Growth": "Axis Global Innov",
        "Axis Global Equity Alpha Fund of Fund - Direct Plan - Growth Option": "Axis Global Alpha",
        
        "Sundaram Global Brand Theme-Equity Active FOF - Direct Growth": "Sundaram Global Brand",

        "Baroda BNP Paribas Aqua Fund of Fund - Direct Plan - Growth Option": "Baroda BNP Aqua",

        "Nippon India Taiwan Equity Fund- Direct Plan- Growth Option": "Nippon Taiwan",

        "PGIM India Emerging Markets Equity Fund of Fund - Direct Plan - Growth": "PGIM Emerging Market",
        "PGIM India Global Equity Opportunities Fund of Fund- Direct Plan - Growth": "PGIM Global Equity",
        "PGIM India Global Select Real Estate Securities Fund of Fund - Direct Plan - Growth Option": "PGIM Global Real Estate",

        'Mirae Asset Global Electric & Autonomous Vehicles Equity Passive FOF - Direct Plan - Growth': "Mirae Asset Global Auto and EV"
    }
}

ARBITRAGE = {
    "Benchmark": ["NIFTY GS 10YR"],
    "Funds": {
        "Invesco India Arbitrage Fund - Direct Plan - Growth Option": "Invesco Arbitrage",
        "Kotak Arbitrage Fund - Direct Plan - Growth": "Kotak Arbitrage",
        "SBI Arbitrage Opportunities Fund - Direct Plan - Gr":"SBI Arbitrage",
        "UTI Arbitrage Fund - Direct Plan - Growth Option": "UTI Arbitrage",
        "ICICI Prudential Equity Arbitrage Fund - Direct Plan - Growth": "ICICI Arbitrage",
        "Edelweiss Arbitrage Fund- Direct Plan- Growth Option":"Edelweiss Arbitrage",
        "Aditya Birla Sun Life Arbitrage Fund - Growth - Direct Plan":"Aditya Biral Arbitrage",
        "Tata Arbitrage Fund-Direct Plan-Growth":"Tata Arbitrage",
        "Axis Arbitrage Fund - Direct Plan - Growth":"Axis Arbitrage",
        "BANDHAN Arbitrage Fund-Direct Plan- Growth":"Bandhan Arbitrage",
        "Nippon India Arbitrage Fund - Direct Plan Growth Plan - Growth Option":"Nippon Arbitrage",
        "HDFC ARBITRAGE FUND - Growth Option - Direct Plan":"HDFC Arbitrage",
        "DSP Arbitrage Fund - Direct - Growth":"DSP Arbitrage",
        "Mirae Asset Arbitrage Fund Direct Growth":"Mirae Asset Arbitrage",
        "HSBC Arbitrage Fund - Direct Growth":"HSBC Arbitrage",
        "BARODA BNP PARIBAS ARBITRAGE FUND-DIRECT PLAN-GROWTH OPTION":"Baroda BNP Arbitrage",
        "Union Arbitrage Fund - Direct Plan - Growth Option":"Union Arbitrage",
        "LIC MF Arbitrage Fund-Direct Plan-Growth":"LIC Arbitrage",
        "Sundaram Arbitrage Fund (Formerly Known as Prinicpal Arbitrage Fund) - Direct Plan - Growth":"Sundaram Arbitrage",
        "ITI Arbitrage Fund - Direct Plan - Growth Option":"ITI Arbitrage",
        "JM Arbitrage Fund (Direct) - Growth Option":"JM Arbitrage",
        "PGIM India Arbitrage Fund - Direct Plan - Growth":"PGIM Arbitrage",
        "BANK OF INDIA Arbitrage Fund Direct Plan Growth":"BoI Arbitrage",
        "Mahindra Manulife Arbitrage Fund - Direct Plan -Growth":"Mahindra Manulife Arbitrage",
        "Bajaj Finserv Arbitrage Fund-Direct Plan-Growth":"Bajaj Finserv Arbitrage",
        "Franklin India Arbitrage Fund - Direct - Growth":"Franklin Arbitrage",
        "Motilal Oswal Arbitrage Fund-Direct Plan-Growth":"Motilal Arbitrage",
        "Old Bridge Arbitrage Fund Direct Growth":"Old Bridge Arbitrage",
        "Parag Parikh Arbitrage Fund - Direct Plan Growth":"PPFAS Arbitrage",
        "quant Arbitrage Fund - Growth Option - Direct Plan":"Quant Arbitrage",
        "Samco Arbitrage Fund - Direct Plan - Growth":"Samco Arbitrage",
        "THE WEALTH COMPANY ARBITRAGE FUND DIRECT GROWTH":"Wealth Comp Arbitrage",
        "WhiteOak Capital Arbitrage Fund Direct Plan Growth":"Whiteoak Arbitrage",
        "JioBlackRock Arbitrage Fund - Direct Plan - Growth Option":"Jio Arbitrage"
    }
}

EQ_SAVING = {
    "Benchmark": ["NIFTY GS 10YR"],
    "Funds": {
        "HSBC Equity Savings Fund - Direct Growth": "HSBC Eq Saving",
        "Kotak Equity Savings Fund - Direct - Growth":"Kotak Eq Saving",
        "Mirae Asset Equity Savings Fund- Direct Plan- Growth":"Mirae Asset Eq Saving",
        "Edelweiss Equity Savings Fund - Direct Plan - Growth Option":"Edelweiss Eq Saving",
        "UTI Equity Savings Fund - Direct Plan - Growth Option":"UTI Eq Saving",
        "Sundaram Equity Savings Fund (Formerly Known as Principal Equity Savings Fund) - Direct Plan - Growth Option":"Sundaram Eq Saving",
        "SBI Equity Savings Fund - Direct Plan - Growth":"SBI Eq Saving",
        "HDFC Equity Savings Fund - Growth Option - Direct Plan":"HDFC Eq Saving",
        "Mahindra Manulife Equity Savings Fund - Direct Plan -Growth": "Mahindra Manulife Eq Saving",
        "Baroda BNP Paribas Equity Savings Fund - Direct Plan - Growth": "Baroda BNP Eq Saving",
        "DSP Equity Savings Fund - Direct Plan - Growth":"DSP Eq Saving",
        "Tata Equity Savings Fund- Direct Plan- Growth Option": "Tata Eq Saving",
        "Axis Equity Savings Fund - Direct Plan - Growth":"Axis Eq Saving",
        "Aditya Birla Sun Life Equity Savings Fund - Direct Plan - Growth": "Aditya Birla Eq Saving",
        "ICICI Prudential Equity Savings Fund - Direct Plan - Cumulative option": "ICICI Eq Saving",
        "Nippon India Equity Savings Fund- Direct Plan- Growth Plan-Growth Option": "Nippon Eq Saving",
        "Franklin India Equity Savings Fund- Growth Direct": "Franklin Eq Saving",
        "Invesco India Equity Savings Fund - Direct Plan - Growth": "Invesco Eq Saving",
        "Union Equity Savings Fund - Direct Plan - Growth Option": "Union Eq Saving",
        "BANDHAN Equity Savings Fund-Direct Plan-Growth": "Bandhan Eq Saving",
        "PGIM India Equity Savings Fund - Direct Plan - Growth": "PGIM India Eq Saving",
        "BAJAJ FINSERV EQUITY SAVINGS FUND - DIRECT - GROWTH": "Bajaj Finserv Eq Saving",
        "quant Equity Savings Fund - Growth Option - Direct Plan": "Quant Eq Saving",
        "WhiteOak Capital Equity Savings Fund Direct Plan Growth": "WhiteOak Eq Saving"
    }
}

HEALTHCARE = {
    "Benchmark": ["NIFTY PHARMA","NIFTY HEALTHCARE","NIFTY MIDSML HLTH"],
    "Funds": {
        "ICICI Prudential Pharma Healthcare and Diagnostics (P.H.D) Fund - Direct Plan - Cumulative Option":"ICICI Healthcare",
        "SBI HEALTHCARE OPPORTUNITIES FUND - DIRECT PLAN -GROWTH": "SBI Healthcare",
        "UTI Healthcare Fund - Direct Plan - Growth Option": "UTI Healthcare",
        "Tata India Pharma & Healthcare Fund-Direct Plan-Growth": "Tata Healthcare",
        "DSP Healthcare Fund - Direct Plan - Growth": "DSP Healthcare",
        "Mirae Asset Healthcare Fund Direct Growth": "Mirae Asset Helathcare",
        "Nippon India Pharma Fund - Direct Plan Growth Plan - Growth Option": "Nippon Healthcare",
        "Aditya Birla Sun Life Pharma and Healthcare Fund-Direct-Growth": "Aditya Birla Healthcare",
        "LIC MF Healthcare Fund-Direct Plan-Growth": "LIC Healthcare",
        "BAJAJ FINSERV HEALTHCARE FUND - DIRECT - GROWTH": "Bajaj Healthcare",
        "Bandhan Healthcare Fund - Direct Plan - Growth": "Bandhan Healthcare",
        "Baroda BNP Paribas Health and Wellness Fund Direct Growth": "Baroda BNP Healthcare",
        "Kotak Healthcare Fund - Direct Plan - Growth Option": "Kotak Healthcare",
        "HDFC Pharma and Healthcare Fund - Growth Option": "HDFC Healthcare",
        "ITI Pharma and Healthcare Fund - Direct Plan - Growth Option": "ITI Healthcare",
        "PGIM India Healthcare Fund - Direct Plan - Growth Option": "PGIM Healthcare",
        "quant Healthcare Fund - Growth Option - Direct Plan": "Quant Healthcare",
        "WhiteOak Capital Pharma and Heathcare Fund Direct Plan Growth": "Whiteoak Healthcare",
        "ICICI Prudential Nifty Pharma Index Fund - Direct Plan - Growth": "ICICI NIFTY Pharma",
        "Motilal Oswal Nifty MidSmall Healthcare Index Fund- Direct Plan-Growth": "Motilal NIFTY Midsmall Helathcare"
    }
}

FINANCIALS = {
    "Benchmark": ["NIFTY BANK","NIFTY FIN SERVICE","NIFTY PSU BANK","NIFTY PVT BANK","NIFTY FINSRV25 50"],
    "Funds": {
        "Invesco India Financial Services Fund - Direct Plan - Growth":"Invesco Financial",
        "SBI BANKING & FINANCIAL SERVICES FUND - DIRECT PLAN - GROWTH": "SBI Financial",
        "Nippon India Banking & Financial Services Fund - Direct Plan Growth Plan - Growth Option": "Nippon Financial",
        "Sundaram Financial Services Opportunities Fund Direct Plan - Growth": "Sundaram Financial",
        "Mirae Asset Banking and Financial Services Fund Direct Growth": "Mirae Asset Financial",
        "Tata Banking And Financial Services Fund-Direct Plan-Growth": "Tata Financial",
        "Aditya Birla Sun Life Banking and Financial Services Fund - Direct Plan - Growth": "Aditya Birla Financial",
        "Baroda BNP Paribas Banking and Financial Services Fund - Direct - Growth Option": "Baroda BNP Financial",
        "UTI Banking and Financial Services Fund - Direct Plan - Growth Option": "UTI Financial",
        "ICICI Prudential Banking and Financial Services Fund - Direct Plan -  Growth": "ICICI Financial",
        "LIC MF Banking and Financial Services Fund-Direct Plan-Growth": "LIC Financial",
        "Bajaj Finserv Banking and Financial Services Fund - Direct - Growth": "Bajaj Financial",
        "DSP Banking & Financial Services Fund - Direct - Growth": "DSP Financial",
        "BANDHAN FINANCIAL SERVICES FUND - DIRECT PLAN - GROWTH": "Bandhan Financial",
        "HDFC Banking & Financial Services Fund - Growth Option": "HDFC Financial",
        "HSBC Financial Services Fund - Direct Growth": "HSBC Financial",
        "Helios Financial Services Fund - Direct Plan - Growth Option": "Helios Financial",
        "ITI Banking and Financial Services Fund - Direct Plan - Growth Option": "ITI Financial",
        "Mahindra Manulife Banking & Financial Services Fund - Direct - Growth": "Mahindra Manulife Financial",
        "quant BFSI Fund - Growth Option - Direct Plan": "Quant BFSI",
        "WhiteOak Capital Banking & Financial Services Fund - Direct Growth": "Whiteoak Financial",
        "Tata Nifty Financial Services Index Fund - Direct Plan - Growth": "Tata Index NIFTY Financial",
        "Kotak Nifty Financial Services Ex-Bank Index Fund - Direct Plan - Growth option": "Kotak NIFTY Financial",
        "Motilal Oswal Nifty MidSmall Financial Services Index Fund - Direct Plan- Growth": "Motilal NIFTY Midsmall Financial"
    }
}

CONSUMER = {
    "Benchmark": ["NIFTY CONSUMPTION","NIFTY CONSR DURBL","NIFTY NEW CONSUMP","NIFTY MS IND CONS","NIFTY NONCYC CONS"],
    "Funds": {
        "Tata India Consumer Fund-Direct Plan-Growth":"Tata Consumption",
        "Mirae Asset Great Consumer Fund - Direct Plan - Growth": "Mirae Asset Great Consumption",
        "ICICI Prudential Bharat Consumption Fund - Direct Plan - Growth Option": "ICICI Consumption",
        "Nippon India Consumption Fund - Direct Plan Growth Plan - Growth Option": "Nippon Consumption",
        "CANARA ROBECO CONSUMER TRENDS FUND - DIRECT PLAN - GROWTH OPTION": "Canara Robeco Consumption",
        "Sundaram Consumption Fund (Formerly Known as Sundaram Rural and Consumption Fund Direct Plan - Growth)": "Sundaram Consumption",
        "BARODA BNP PARIBAS India Consumption Fund - Direct Plan - Growth Option": "Baroda BNP Consumption",
        "SBI CONSUMPTION OPPORTUNITIES FUND - DIRECT PLAN - GROWTH": "SBI Consumption",
        "Aditya Birla Sun Life Consumption Fund - Growth - Direct Plan": "Aditya Birla Consumption",
        "Mahindra Manulife Consumption Fund - Direct Plan -Growth": "Mahindra Manulife Consumption",
        "UTI India Consumer Fund - Direct Plan - Growth Option": "UTI Consumption",
        "Axis Consumption Fund Direct Plan - Growth": "Axis Consumption",
        "BAJAJ FINSERV CONSUMPTION FUND - DIRECT - GROWTH": "Bajaj Consumption",
        "Bank of India Consumption Fund - Direct - Growth": "BoI Consumption",
        "Edelweiss Consumption Fund - Direct - Growth": "Edelweiss Consumption",
        "HDFC Non-Cyclical Consumer Fund - Growth Option - Direct Plan": "HDFC non-cyclical Consumption",
        "HSBC Consumption Fund - Direct Growth": "HSBC Consumption",
        "Invesco India Consumption Fund - Direct Plan - Growth": "Invesco Consumption",
        "Kotak Consumption Fund - Direct plan - Growth Option": "Kotak Consumption",
        "LIC MF Consumption Fund-Direct Plan-Growth": "LIC Consumption",
        "Motilal Oswal Consumption Fund-Direct-Growth": "Motilal Consumption",
        "quant Consumption Fund - Growth Option - Direct Plan": "Quant Consumption",
        "Groww Nifty Non-Cyclical Consumer Index Fund - Direct Plan Growth": "Groww NIFTY non-cyclical Consumption",
        "SBI Nifty India Consumption Index Fund- Direct Plan- Growth": "SBI NIFTY Consumption",
        "Mirae Asset Nifty India New Age Consumption ETF Fund of Fund - Direct Plan - Growth": "Mirae Asset NIFTY New Age Consumption",
        "Motilal Oswal Nifty MidSmall India Consumption Index Fund - Direct Plan- Growth": "Motilal NIFTY Midsmall Consumption"
    }
}

IT = {
    "Benchmark": ["NIFTY IT","NIFTY MS IT TELCM","NIFTY IND DIGITAL"],
    "Funds": {
        "Franklin India Technology Fund - Direct - Growth": "Franklin Tech",
        "SBI TECHNOLOGY OPPORTUNITIES FUND - DIRECT PLAN - GROWTH": "SBI Tech",
        "ICICI Prudential Technology Fund - Direct Plan -  Growth": "ICICI Tech",
        "Tata Digital India Fund-Direct Plan-Growth": "Tata Digital Tech",
        "Aditya Birla Sun Life Digital India Fund - Growth - Direct Plan": "Aditya Birla Digital Tech",
        "Edelweiss Technology Fund - Direct Plan - Growth": "Edelweiss Tech",
        "HDFC Technology Fund - Growth Option - Direct Plan": "HDFC Tech",
        "Invesco India Technology Fund - Direct Plan - Growth": "Invesco Tech",
        "Kotak Technology Fund - Direct Plan - Growth Option": "Kotak Tech",
        "Motilal Oswal Digital India Fund - Direct Plan - Growth": "Motilal Digital Tech",
        "quant Teck Fund - Growth Option - Direct Plan": "Quant Tech",
        "WhiteOak Capital Digital Bharat Fund Direct Plan Growth": "Whiteoak Digital Tech",
        "Motilal Oswal Nifty MidSmall IT and Telecom Index Fund - Direct Plan- Growth": "Motilal NIFTY Midsmall Tech",
        "Tata Nifty India Digital ETF Fund of Fund-Direct Plan-Growth": "Tata NIFTY Digital Tech",
        "HDFC Nifty India Digital Index Fund - Growth Option - Direct": "HDFC NIFTY Digital Tech",
        "Nippon India Nifty IT Index Fund - Direct Plan - Growth Option": "Nippon NIFTY Tech"
    }
}

INFRA = {
    "Benchmark": ["NIFTY INFRA","NIFTY MULTI INFRA"],
    "Funds": {
        "Aditya Birla Sun Life Infrastructure Fund - Growth - Direct Plan": "Aditya Birla Infra",
        "BANDHAN Infrastructure Fund-Direct Plan-Growth": "Bandhan Infra",
        "CANARA ROBECO INFRASTRUCTURE FUND - DIRECT PLAN - GROWTH OPTION": "Canara Robeco Infra",
        "DSP India T.I.G.E.R. Fund - Direct Plan - Growth": "DSP Infra",
        "Franklin Build India Fund - Direct - Growth": "Franklin Infra",
        "HDFC Infrastructure Fund - Growth Option - Direct Plan": "HDFC Infra",
        "HSBC Infrastructure Fund - Direct Growth": "HSBC Infra",
        "ICICI Prudential Infrastructure Fund - Direct Plan -  Growth": "ICICI Infra",
        "Invesco India Infrastructure Fund - Direct Plan - Growth Option": "Invesco Infra",
        "Kotak Infrastructure & Economic Reform Fund- Direct Plan- Growth Option": "Kotak Infra",
        "LIC MF Infrastructure Fund-Direct Plan-Growth": "LIC Infra",
        "Mirae Asset Infrastructure Fund - Direct Plan - Growth": "Mirae Asset Infra",
        "Motilal Oswal Infrastructure Fund-Direct-Growth": "Motilal Infra",
        "Nippon India Power & Infra Fund - Direct Plan Growth Plan - Growth Option": "Nippon Infra",
        "quant Infrastructure Fund - Growth Option-Direct Plan": "Quant Infra",
        "SBI INFRASTRUCTURE FUND -  DIRECT PLAN - GROWTH": "SBI Infra",
        "Sundaram Infrastructure Advantage Fund Direct Plan - Growth": "Sundaram Infra",
        "Tata Infrastructure Fund -Direct Plan -Growth Option": "Tata Infra",
        'Taurus Infrastructure Fund - Direct Plan - Growth ': "Taurus Infra",
        'UTI Infrastructure Fund-Growth Option- Direct': "UTI Infra",
        "Tata Nifty500 Multicap Infrastructure 50:30:20 Index Fund - Direct Plan - Growth": "Tata NIFTY500 Multicap Infra",

    }
}

ENERGY = {
    "Benchmark": ['NIFTY ENERGY'],
    "Funds": {
        "Baroda BNP Paribas Energy Opportunities Fund - Direct Plan - Growth Option": "Baroda BNP Energy",
        "DSP Natural Resources and New Energy Fund - Direct Plan - Growth": "DSP Natural Resource and Energy",
        'ICICI PRUDENTIAL ENERGY OPPORTUNITIES FUND - Direct Plan - Growth': "ICICI Energy",
        'Kotak Energy Opportunities Fund-Direct-Growth': "Kotak Energy",
        'SBI Energy Opportunities Fund - Direct Plan - Growth': "SBI Energy",
        'Tata Resources & Energy Fund-Direct Plan-Growth': "Tata Resources and Energy",
        'DSP Global Clean Energy Overseas Equity Omni FoF Direct Plan - Growth': "DSP Global Clean Energy",
        'ICICI Prudential Strategic Metal and Energy Equity Fund of Fund - Direct Plan Growth': "ICICI Strategic Metal and Energy",
    }
}

INNOVATION = {
    "Benchmark": ['NIFTY IT'],
    "Funds": {
        'Axis Innovation Fund - Direct Plan - Growth Option': "Axis Innovation",
        'Bandhan Innovation Fund - Direct Plan - Growth': "Bandhan Innovation",
        'Baroda BNP Paribas Innovation Fund Direct plan - Growth Option': "Baroda BNP Innovation",
        'HDFC INNOVATION FUND - DIRECT PLAN - GROWTH OPTION': "HDFC Innovation",
        'ICICI Prudential Innovation Fund - Direct Plan - Growth': "ICICI Innovation",
        'Mahindra Manulife Innovation Opportunities Fund - Direct - Growth': "Mahindra Manulife Innovation",
        'Motilal Oswal Innovation Opportunities Fund - Direct Plan- Growth': "Motilal Innovation",
        'Nippon India Innovation Fund-Direct Plan-Growth Option': "Nippon Innovation",
        'Tata India Innovation Fund- Direct Growth': "Tata Innovation",
        'Union Innovation & Opportunities Fund - Direct Plan - Growth Option': "Union Innovation",
        'UTI Innovation Fund - Direct Plan - Growth Option': "UTI Innovation",
    }
}

MANUFACTURING = {
    "Benchmark": ['NIFTY MULTI MFG','NIFTY INDIA MFG'],
    "Funds": {
        'Aditya Birla Sun Life Manufacturing Equity Fund - Direct Plan - Growth': "Aditya Birla Mfg",
        'Axis India Manufacturing Fund - Direct Plan - Growth': "Axis Mfg",
        'BANK OF INDIA Manufacturing & Infrastructure Fund-Direct Plan-Growth': "BOI Mfg",
        'Baroda BNP Paribas Manufacturing Fund - Direct Plan - Growth Option': "Baroda BNP Mfg",
        'Canara Robeco Manufacturing Fund - Direct Plan - Growth Option': "Canara Robeco Mfg",
        'HDFC Manufacturing fund - Growth Option - Direct Plan': "HDFC Mfg",
        'Invesco India Manufacturing Fund - Direct Plan - Growth'  : "Invesco Mfg",
        'Kotak Manufacture in India Fund - Direct Plan Growth': "Kotak Mfg",
        'LIC MF Manufacturing Fund-Direct Plan-Growth': "LIC Mfg",
        'Mahindra Manulife Manufacturing Fund - Direct Plan - Growth': "Mahindra Manulife Mfg",
        'Motilal Oswal Manufacturing Fund - Direct Plan- Growth': "Motilal Mfg",
        'quant Manufacturing Fund - Growth Option - Direct Plan': "Quant Mfg",
        'Mirae Asset Nifty India Manufacturing ETF FOF - Direct Plan - Growth': "Mirae Asset NIFTY Mfg",
        'Navi Nifty India Manufacturing Index Fund- Direct Plan- Growth': "Navi NIFTY Mfg",
        'Nippon India Nifty India Manufacturing Index Fund- Direct Plan- Growth Option': "Nippon NIFTY Mfg",
        'Tata Nifty500 Multicap India Manufacturing 50:30:20 Index Fund -Direct Plan-Growth': "Tata NIFTY500 Mfg",
        'UTI Nifty India Manufacturing Index Fund - Direct Plan - Growth Option': "UTI NIFTY Mfg",
    }
}

SPECIAL_OPP = {
    "Benchmark": ["NIFTY 50","NIFTY 500"],
    "Funds": {
            'Aditya Birla Sun Life Special Opportunities Fund-Direct-Growth': "Aditya Birla Special Opp",
            'Kotak Special Opportunities Fund - Direct Plan - Growth Option': "Kotak Special Opp",
            'Motilal Oswal Special Opportunities Fund - Direct - Growth': "Motilal Special Opp",
            'Samco Special Opportunities Fund - Direct Plan - Growth': "Samco Special Opp",
            'WhiteOak Capital Special Opportunities Fund - Direct Growth': "WhiteOak Special Opp"
    }
}

TRANSP = {
    "Benchmark": ['NIFTY TRANS LOGIS'],
    "Funds": {
            'Aditya Birla Sun Life Transportation and Logistics Fund-Direct Growth': "Aditya Birla Transp",
            'BANDHAN TRANSPORTATION AND LOGISTICS FUND - GROWTH - DIRECT PLAN': "Bandhan Transp",
            'HDFC Transportation and Logistics Fund - Growth Option - Direct Plan': "HDFC Transp",
            'ICICI PRUDENTIAL TRANSPORTATION AND LOGISTICS FUND - Direct Plan - Growth': "ICICI Transp",
            'Kotak Transportation & Logistics Fund-Direct Growth': "Kotak Transp",
            'UTI-Transportation and Logistics  Fund-Growth Option- Direct': "UTI Transp"
    }
}

AUTO = {
    "Benchmark": ['NIFTY AUTO'],
    "Funds": {
            'SBI Automotive Opportunities Fund - Direct Plan - Growth': "SBI Auto",
            'Groww Nifty EV & New Age Automotive ETF FOF- Direct Plan - Growth': "Groww NIFTY Auto",
            'ICICI Prudential Nifty EV & New Age Automotive ETF FOF - Direct Plan - Growth': "ICICI NIFTY EV and new age Auto",
            'ICICI Prudential Nifty Auto Index Fund - Direct Plan - Growth': "ICICI NIFTY Auto",
            'Nippon India Nifty Auto Index Fund - Direct Plan- Growth Option': "Nippon NIFTY Auto",
            'Tata Nifty Auto Index Fund - Direct Plan - Growth': "Tata NIFTY Auto"
    }
}

SECTOR_DICT_MAP = {
    "MULTI_CAP":MULTI_CAP,
    "SMALL_CAP":SMALL_CAP,
    "MULTI_ASSET":MULTI_ASSET,
    "FLEXI_CAP":FLEXI_CAP,
    "LARGE_CAP":LARGE_CAP,
    "MID_CAP":MID_CAP,
    "CONTRA":CONTRA,
    "CONSUMER":CONSUMER,
    "FOCUSED":FOCUSED,
    "OTHER":OTHER,
    "ACTIVE_MOMETUM":ACTIVE_MOMETUM, # new
    "QUANT":QUANT, # new
    "INTERNATIONAL":INTERNATIONAL,
    "BUSINESS_CYCLE": BUSINESS_CYCLE,
    "HEALTHCARE":HEALTHCARE,
    "FINANCIALS":FINANCIALS,
    "CONSUMER":CONSUMER,
    "IT":IT,
    "INFRA":INFRA, # new
    "ENERGY":ENERGY, # new
    "INNOVATION":INNOVATION, # new
    "MANUFACTURING":MANUFACTURING, # new
    "SPECIAL_OPP":SPECIAL_OPP, # new
    "TRANSP":TRANSP, # new
    "AUTO":AUTO, # new
    "ARBITRAGE":ARBITRAGE,
    "EQ_SAVING":EQ_SAVING
}

# --- UDFs ---

def fetch_mftool_scheme_code(fund_name):
    schemes = mf.get_available_schemes(fund_name)
    return next(iter(schemes), None)

def fetch_fund_historical_nav(fund_name):
    fund_scheme_code = fetch_mftool_scheme_code(fund_name)
    df = mf.get_scheme_historical_nav(fund_scheme_code,as_Dataframe=True)
    return df.drop(columns=["dayChange"])

def compute_period_returns(
    df: pd.DataFrame,
    periods: List[str],
    name: str,
    nav_col: str = "nav",
    date_format: str = "%d-%m-%Y",
    as_of: Optional[str] = None,
    min_obs: int = 2
) -> pd.DataFrame:

    # Parse and sort index
    s = df.copy()
    idx = pd.to_datetime(s.index.astype(str), format=date_format, errors="coerce")
    s = s.loc[~idx.isna()].copy()
    s.index = idx[~idx.isna()]
    s = s.sort_index()

    nav = pd.to_numeric(s[nav_col], errors="coerce").dropna()
    if len(nav) < min_obs:
        return pd.DataFrame(index=[name], columns=periods, dtype=float)

    # As-of date
    if as_of is not None:
        as_of_dt = pd.to_datetime(as_of, format=date_format)
        nav = nav.loc[:as_of_dt]

    end_date = nav.index[-1]
    end_nav = nav.iloc[-1]

    def nav_on_or_before(target):
        loc = nav.index.searchsorted(target, side="right") - 1
        return None if loc < 0 else nav.iloc[loc]

    def date_on_or_before(target):
        loc = nav.index.searchsorted(target, side="right") - 1
        return None if loc < 0 else nav.index[loc]

    results = {}

    for p in periods:
        p = p.strip()

        # -------- All --------
        if p.lower() == "all":
            start_nav = nav.iloc[0]
            start_dt = nav.index[0]
            days = (end_date - start_dt).days
            years = days / 365.25

            if years >= 1:
                results[p] = ((end_nav / start_nav) ** (1 / years) - 1)*100
            else:
                results[p] = (end_nav / start_nav - 1)*100
            continue

        m = re.fullmatch(r"(\d+)([MY])", p.upper())
        if not m:
            results[p] = np.nan
            continue

        n, unit = int(m.group(1)), m.group(2)

        # -------- Months (simple return) --------
        if unit == "M":
            start_nav = nav_on_or_before(end_date - pd.DateOffset(months=n))
            results[p] = np.nan if start_nav is None else (end_nav / start_nav - 1)*100

        # -------- Years (annualized) --------
        elif unit == "Y":
            start_date = end_date - pd.DateOffset(years=n)
            start_nav = nav_on_or_before(start_date)
            actual_start = date_on_or_before(start_date)

            if start_nav is None or actual_start is None:
                results[p] = np.nan
            else:
                years = (end_date - actual_start).days / 365.25
                results[p] = ((end_nav / start_nav) ** (1 / years) - 1)*100

    # index = name, columns = periods
    out = pd.DataFrame(results, index=[name])
    out.columns = pd.MultiIndex.from_product(
        [["PtP Ret"],out.columns]
    )
    return out

def hybrid_returns_table(
    df: pd.DataFrame,
    periods: List[str],
    name: str,
    nav_col: str = "nav",
    date_format: str = "%d-%m-%Y",
    as_of: Optional[str] = None,        # optional end date string in dd-mm-yyyy
    yearly_annualized: bool = True,     # True -> rolling CAGR; False -> rolling total return over nY
    min_windows: int = 3                # require at least this many rolling windows for mean
) -> pd.DataFrame:
    """
    Rules:
      1) nM (1M/3M/6M): latest simple return.
      2) nY (1Y/3Y/5Y): mean of rolling nY returns (rolling windows until latest date).
         - Each rolling window uses start NAV at the closest available date ON/BEFORE (end_date - nY).
         - If yearly_annualized=True: compute rolling annualized (CAGR) using actual day count.
           Else: compute rolling total return over the window.
      3) All: total since inception annualized return (CAGR), no rolling.

    Output:
      index = [name], columns = periods (same order).
    """

    if df.empty or nav_col not in df.columns:
        raise ValueError("df is empty or nav_col not found in df.columns")

    # Parse and sort index to DatetimeIndex
    s = df.copy()
    idx = pd.to_datetime(s.index.astype(str), format=date_format, errors="coerce")
    s = s.loc[~idx.isna()].copy()
    s.index = idx[~idx.isna()]
    s = s.sort_index()

    nav = pd.to_numeric(s[nav_col], errors="coerce").dropna()
    if nav.empty:
        return pd.DataFrame(index=[name], columns=[str(p).strip() for p in periods], dtype=float)

    # Optional as-of trimming
    if as_of is not None:
        as_of_dt = pd.to_datetime(as_of, format=date_format)
        nav = nav.loc[:as_of_dt]
        if nav.empty:
            return pd.DataFrame(index=[name], columns=[str(p).strip() for p in periods], dtype=float)

    end_date = nav.index[-1]
    end_nav = float(nav.iloc[-1])

    # Helper: NAV at last available date <= target_date
    def nav_on_or_before(target_date: pd.Timestamp):
        loc = nav.index.searchsorted(target_date, side="right") - 1
        if loc < 0:
            return None, None
        return float(nav.iloc[loc]), nav.index[loc]

    results = {}

    for p in periods:
        p_clean = str(p).strip()

        # -------- All: since inception CAGR (no rolling) --------
        if p_clean.lower() == "all":
            start_nav = float(nav.iloc[0])
            start_dt = nav.index[0]
            days = (end_date - start_dt).days
            years = days / 365.25

            if start_nav <= 0 or end_nav <= 0 or days <= 0:
                results[p_clean] = np.nan
            else:
                # annualized since inception
                results[p_clean] = (end_nav / start_nav) ** (1.0 / years) - 1.0 if years > 0 else np.nan
            continue

        m = re.fullmatch(r"(\d+)\s*([MY])", p_clean.upper())
        if not m:
            results[p_clean] = np.nan
            continue

        n = int(m.group(1))
        unit = m.group(2)

        # -------- Monthly: latest simple return --------
        if unit == "M":
            target_start = end_date - pd.DateOffset(months=n)
            start_nav, _start_dt = nav_on_or_before(target_start)

            if start_nav is None or start_nav <= 0:
                results[p_clean] = np.nan
            else:
                results[p_clean] = end_nav / start_nav - 1.0
            continue

        # -------- Yearly: mean of Roll Ret over all possible windows --------
        if unit == "Y":
            # For each end date t, compute return from start = (t - n years) aligned to prev available date
            rolled_vals = []

            for t, nav_t in nav.items():
                target_start = t - pd.DateOffset(years=n)
                start_nav, start_dt = nav_on_or_before(target_start)
                if start_nav is None or start_dt is None:
                    continue
                if start_nav <= 0 or nav_t <= 0:
                    continue

                if yearly_annualized:
                    days = (t - start_dt).days
                    if days <= 0:
                        continue
                    yrs = days / 365.25
                    rolled = (nav_t / start_nav) ** (1.0 / yrs) - 1.0
                else:
                    rolled = (nav_t / start_nav) - 1.0

                rolled_vals.append(rolled)

            if len(rolled_vals) < min_windows:
                results[p_clean] = np.nan
            else:
                results[p_clean] = float(np.median(rolled_vals))

    # Output table with index=name and columns=periods (preserve order)
    col_order = [str(p).strip() for p in periods]
    out = pd.DataFrame([[results.get(c, np.nan) for c in col_order]], index=[name], columns=col_order)
    out.index.name = None
    out.columns = pd.MultiIndex.from_product(
        [["Roll Ret"],out.columns]
    )    
    return out.mul(100)

def fetch_benchmark_index_data(
    ticker,
    start_date="01-Jan-2010",
    end_date=TDY_DATE,
    max_retries=3,
    retry_delay=2  # seconds
):
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            historical_data = index_history(
                ticker,
                start_date=start_date,
                end_date=end_date
            )
            break  # success → exit loop
        except Exception as e:
            last_exception = e
            print(f"[{ticker}] Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
    else:
        # runs only if loop never breaks
        raise RuntimeError(
            f"Failed to fetch index history for {ticker} after {max_retries} attempts"
        ) from last_exception

    historical_data = pd.DataFrame(historical_data)
    #print(historical_data.head())

    return historical_data

def compute_index_funds_returns(index_dict):
    all_returns_df = pd.DataFrame()
    for x,y in index_dict.items():
        if x == "Benchmark":
            try:
                for idx in y:
                    #print(idx)
                    ret_df = fetch_benchmark_index_data(ticker=idx)
                    rolling_ret_df = hybrid_returns_table(
                        df=ret_df[["HistoricalDate", "CLOSE"]].set_index("HistoricalDate"),
                        periods=ROLLING_RETURN_PERIODS,
                        name=idx,
                        nav_col="CLOSE",
                        date_format="%d %b %Y"
                    )

                    pp_ret_df = compute_period_returns(
                        df=ret_df[["HistoricalDate", "CLOSE"]].set_index("HistoricalDate"),
                        periods=POINT_TO_POINT_RETURN_PERIODS,
                        name=idx,
                        nav_col="CLOSE",
                        date_format="%d %b %Y"
                    )
                    ret_df =  pd.concat([rolling_ret_df, pp_ret_df], axis=1)                
                    all_returns_df = pd.concat([all_returns_df,ret_df])
            except Exception as e:
                print(f"Skipping benchmark index {idx}. Error occurred while processing: {e}")

        elif x == "Funds":
            for fund_name, norm_name in y.items():
                #print(fund_name)
                t_df = fetch_fund_historical_nav(fund_name=fund_name)
                rolling_ret_df = hybrid_returns_table(df=t_df,
                                        periods=ROLLING_RETURN_PERIODS,
                                        name=norm_name
                                        )
                pp_ret_df = compute_period_returns(df=t_df,
                                        periods=POINT_TO_POINT_RETURN_PERIODS,
                                        name=norm_name
                                        )
                ret_df = pd.concat([pp_ret_df,rolling_ret_df],axis=1)
                all_returns_df = pd.concat([all_returns_df,ret_df])
    return all_returns_df.round(2).sort_values(by=[("PtP Ret","3Y")],ascending=False)

def rolling_yearly_returns_timeseries(
    df: pd.DataFrame,
    yearly_periods: List[str],
    nav_col: str = "nav",
    date_format: str = "%d-%m-%Y",
    as_of: Optional[str] = None,        # optional end date string in dd-mm-yyyy
    yearly_annualized: bool = True      # True -> rolling CAGR; False -> rolling total return over nY
) -> pd.DataFrame:
    """
    Returns a DataFrame of rolling yearly returns for each date, for the requested yearly periods.

    - Supports only periods like ["1Y","3Y","5Y", ...]
    - For each end date t, start date is aligned to the closest available date ON/BEFORE (t - n years)
    - If yearly_annualized=True: rolling CAGR using actual day count (days/365.25)
      else: rolling total return over the window
    - Keeps dates where at least ONE requested rolling return is available.
      (i.e., allows NaN in longer tenors while shorter tenors exist)
    - Output values are in decimal form (e.g., 0.12 = 12%).
    """

    if df is None or df.empty or nav_col not in df.columns:
        raise ValueError("df is empty or nav_col not found in df.columns")

    # Parse/sort index to DatetimeIndex
    s = df.copy()
    idx = pd.to_datetime(s.index.astype(str), format=date_format, errors="coerce")
    s = s.loc[~idx.isna()].copy()
    s.index = idx[~idx.isna()]
    s = s.sort_index()

    nav = pd.to_numeric(s[nav_col], errors="coerce").dropna()
    if nav.empty:
        return pd.DataFrame()

    # Optional as-of trimming
    if as_of is not None:
        as_of_dt = pd.to_datetime(as_of, format=date_format)
        nav = nav.loc[:as_of_dt]
        if nav.empty:
            return pd.DataFrame()

    # Validate + parse yearly periods
    parsed = []
    for p in yearly_periods:
        p_clean = str(p).strip().upper()
        m = re.fullmatch(r"(\d+)\s*Y", p_clean)
        if not m:
            raise ValueError(f"Invalid yearly period '{p}'. Expected like '1Y', '3Y', etc.")
        parsed.append((p_clean, int(m.group(1))))

    # Helper: NAV at last available date <= target_date
    def nav_on_or_before(target_date: pd.Timestamp):
        loc = nav.index.searchsorted(target_date, side="right") - 1
        if loc < 0:
            return None, None
        return float(nav.iloc[loc]), nav.index[loc]

    out = pd.DataFrame(index=nav.index)

    for label, n_years in parsed:
        col = []
        for t, nav_t in nav.items():
            target_start = t - pd.DateOffset(years=n_years)
            start_nav, start_dt = nav_on_or_before(target_start)

            if start_nav is None or start_dt is None:
                col.append(np.nan)
                continue
            if start_nav <= 0 or nav_t <= 0:
                col.append(np.nan)
                continue

            if yearly_annualized:
                days = (t - start_dt).days
                if days <= 0:
                    col.append(np.nan)
                    continue
                yrs = days / 365.25
                col.append((nav_t / start_nav) ** (1.0 / yrs) - 1.0)
            else:
                col.append((nav_t / start_nav) - 1.0)

        out[label] = col

    # Keep rows where at least one tenor is available
    out = out.dropna(how="all")

    return out

def plot_rolling_returns_from_index_dict(
    index_dict: dict,
    yearly_periods=("1Y", "2Y", "3Y", "5Y", "10Y"),
    yearly_annualized: bool = True,
    max_workers: int = 5,
    # Assumes these exist in scope:
    # fetch_benchmark_index_data, fetch_fund_historical_nav, rolling_yearly_returns_timeseries
) -> dict:
    
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def _compute_rolling_for_series(df_nav: pd.DataFrame, name: str, nav_col: str, date_format: str):
        rr = rolling_yearly_returns_timeseries(
            df=df_nav,
            yearly_periods=list(yearly_periods),
            nav_col=nav_col,
            date_format=date_format,
            as_of=None,
            yearly_annualized=yearly_annualized,
        )
        rr = rr.reset_index()
        # Normalize column names
        rr.columns = [c.lower() if c in ['index', 'Date', 'HistoricalDate'] else c for c in rr.columns]
        rr["Series"] = name
        return rr

    def fetch_and_compute(task):
        task_type, source, name = task
        try:
            if task_type == "benchmark":
                hist = fetch_benchmark_index_data(ticker=source)
                bench_nav = hist[["HistoricalDate", "CLOSE"]].set_index("HistoricalDate")
                result = _compute_rolling_for_series(bench_nav, f"Benchmark: {source}", "CLOSE", "%d %b %Y").rename(columns={"historicaldate": "date"})
            else:
                t_df = fetch_fund_historical_nav(fund_name=source)
                result = _compute_rolling_for_series(t_df, name, "nav", "%d-%m-%Y")
            return result
        except Exception as e:
            if task_type == "benchmark":
                print(f"Skipping benchmark {source}: {e}")
            else:
                print(f"Skipping {source}: {e}")
            return None

    tasks = []
    if "Benchmark" in index_dict:
        for ticker in index_dict["Benchmark"]:
            tasks.append(("benchmark", ticker, None))
    if "Funds" in index_dict:
        for fund_name, norm_name in index_dict["Funds"].items():
            tasks.append(("fund", fund_name, norm_name))

    all_long = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_and_compute, task): task for task in tasks}
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                all_long.append(result)

    if not all_long:
        return {}

    long_df = pd.concat(all_long, ignore_index=True)
    #print(long_df.head())
    long_df["date"] = pd.to_datetime(long_df["date"])
    long_df = long_df.sort_values("date")

    figs = {}

    # 3. Plotting
    for tenor in yearly_periods:
        if tenor not in long_df.columns:
            continue

        plot_df = long_df[["date", "Series", tenor]].dropna(subset=[tenor])
        if plot_df.empty:
            continue

        fig = px.line(
            plot_df,
            x="date",
            y=tenor,
            color="Series",
            title=f"Rolling Returns ({tenor})" + (" - Annualized (CAGR)" if yearly_annualized else " - Total Return"),
            # Use a large color palette (Alphabet or Dark24) to avoid repeating colors for many funds
            color_discrete_sequence=px.colors.qualitative.Dark24, 
            template="plotly_white",
        )

        # --- KEY FIXES HERE ---
        fig.update_layout(
            hovermode="x unified",
            # Move Legend to the Right (Vertical)
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,           # Align to top of chart
                xanchor="left",
                x=1.02,        # Push slightly outside the right edge
                font=dict(size=10) # Smaller font if you have many series
            ),
            # Add right margin to accommodate the legend
            margin=dict(r=150, b=50, t=80),
            yaxis_title="Return",
            xaxis_title="Date",
        )
        
        fig.update_yaxes(tickformat=".2%")
        fig.update_traces(hovertemplate="%{y:.2%}")

        figs[tenor] = fig

    return figs


def compute_all_funds_returns(sector_dict_map: dict, periods: List[str] = ["3M", "6M", "1Y", "2Y", "3Y"], max_workers: int = 5) -> pd.DataFrame:
    """
    Iterates through all sectors in SECTOR_DICT_MAP, fetches NAV for each fund,
    computes point-to-point returns for the given periods using parallel execution,
    and returns a combined DataFrame with all funds sorted by the specified periods.
    
    Args:
        sector_dict_map: Dictionary containing sector definitions with "Funds" key
        periods: List of periods to compute returns for (default: ["3M", "6M", "1Y", "2Y", "3Y"])
        max_workers: Number of parallel workers for ThreadPoolExecutor (default: 4)
    
    Returns:
        DataFrame with fund names as index and returns for each period as columns
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    def process_fund(fund_task):
        """Process a single fund and return results or None on error"""
        sector_name, fund_name, norm_name = fund_task
        try:
            # Fetch historical NAV for the fund
            t_df = fetch_fund_historical_nav(fund_name=fund_name)
            
            if t_df.empty or "nav" not in t_df.columns:
                print(f"Skipping {fund_name}: No NAV data")
                return None
            
            # Compute point-to-point returns
            ret_df = compute_period_returns(
                df=t_df,
                periods=periods,
                name=norm_name,
                nav_col="nav",
            )
            
            # Add sector information to the fund name for tracking
            ret_df.index = [f"({sector_name}) {norm_name}"]
            
            return ret_df
            
        except Exception as e:
            print(f"Skipping {fund_name}: {e}")
            return None
    
    # Flatten all funds into a single list of tasks
    all_fund_tasks = []
    for sector_name, sector_data in sector_dict_map.items():
        if "Funds" not in sector_data:
            continue
        for fund_name, norm_name in sector_data["Funds"].items():
            all_fund_tasks.append((sector_name, fund_name, norm_name))
    
    # Process funds in parallel
    all_funds_returns = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and process results as they complete
        futures = {executor.submit(process_fund, task): task for task in all_fund_tasks}
        
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                all_funds_returns.append(result)
    
    # Combine all results
    if not all_funds_returns:
        return pd.DataFrame()
    
    all_funds_returns = pd.concat(all_funds_returns, ignore_index=False)
    
    # Flatten multi-index columns if present
    if isinstance(all_funds_returns.columns, pd.MultiIndex):
        all_funds_returns.columns = [
            " - ".join([str(x) for x in col if x is not None and str(x) != ""])
            for col in all_funds_returns.columns
        ]
    
    return all_funds_returns.round(2)


def get_top_performers(all_returns_df: pd.DataFrame, periods: List[str] = ["3M", "6M", "1Y", "2Y", "3Y"], top_n: int = 10) -> dict:
    """
    Returns the top performing funds for each period.
    
    Args:
        all_returns_df: DataFrame with fund returns
        periods: List of periods to get top performers for
        top_n: Number of top performers to return per period
    
    Returns:
        Dictionary with period as key and DataFrame of top performers as value
    """
    top_performers = {}
    
    for period in periods:
        # Find the column that contains this period
        period_cols = [col for col in all_returns_df.columns if period in col]
        if not period_cols:
            continue
        
        col = period_cols[0]
        # Sort by the period column descending and get top N
        top_df = all_returns_df[[col]].dropna().sort_values(by=col, ascending=False).head(top_n)
        top_performers[period] = top_df
    
    return top_performers


def get_sector_summary(top_performers: dict, all_returns_df: pd.DataFrame, top_n: int) -> dict:
    """
    Returns a summary of sectors for the top X performers.
    
    Args:
        top_performers: Dictionary with period as key and DataFrame of top performers as value
        all_returns_df: DataFrame with all fund returns (includes sector info in index)
        top_n: Number of top performers
    
    Returns:
        Dictionary with period as key and DataFrame (sector, ratio, avg_return) as value
    """
    # Calculate total funds per sector from all_returns_df
    total_funds_per_sector = {}
    for fund_name in all_returns_df.index:
        if "(" in fund_name and ")" in fund_name:
            sector = fund_name.split(")")[0].replace("(", "").strip()
        else:
            sector = "Unknown"
        
        if sector not in total_funds_per_sector:
            total_funds_per_sector[sector] = 0
        total_funds_per_sector[sector] += 1
    
    sector_summary = {}
    
    for period, top_df in top_performers.items():
        # Extract sector from the fund name (format: "FundName (SECTOR)")
        sector_counts = {}
        sector_returns = {}
        
        for fund_name in top_df.index:
            # Parse sector from fund name
            if "(" in fund_name and ")" in fund_name:
                sector = fund_name.split(")")[0].replace("(", "").strip()
            else:
                sector = "Unknown"
            
            # Get the return value
            return_col = [col for col in all_returns_df.columns if period in col][0]
            return_val = all_returns_df.loc[fund_name, return_col]
            
            if sector not in sector_counts:
                sector_counts[sector] = 0
                sector_returns[sector] = []
            
            sector_counts[sector] += 1
            sector_returns[sector].append(return_val)
        
        # Create summary DataFrame with ratio format (e.g., "15/25")
        summary_data = []
        for sector in sector_counts:
            count_in_top = sector_counts[sector]
            total_in_sector = total_funds_per_sector.get(sector, 0)
            summary_data.append({
                "Sector": sector,
                "Funds in Top " + str(top_n): f"{count_in_top}/{total_in_sector}",
                "Avg Return (%)": round(np.mean(sector_returns[sector]), 2)
            })
        
        summary_df = pd.DataFrame(summary_data)
        # Sort by the count in top (extract numerator from ratio)
        summary_df["_sort_key"] = summary_df["Funds in Top " + str(top_n)].apply(lambda x: int(x.split("/")[0]))
        summary_df = summary_df.sort_values(by="_sort_key", ascending=False).drop(columns=["_sort_key"])
        sector_summary[period] = summary_df
    
    return sector_summary


# --- App code ---
st.set_page_config(page_title="MF Tracker", layout="wide")
st.title("MF Tracker")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Sector Returns", "Index Charts", "Top Performers"])

# --- Tab 1: Sector Returns Dashboard ---
with tab1:
    st.subheader("Sector Returns Dashboard")
    
    # Initialize session state for tab1
    if "tab1_sector" not in st.session_state:
        st.session_state.tab1_sector = None
    if "tab1_returns_df" not in st.session_state:
        st.session_state.tab1_returns_df = None
    
    # Left column for inputs
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### Select Sector")
        sectors = sorted(SECTOR_DICT_MAP.keys())
        sector = st.selectbox("Choose sector", sectors, index=0, key="sector_tab1")
        run = st.button("Compute Returns", type="primary")
    
    with col2:
        if run:
            with st.spinner("Computing returns..."):
                returns_df = compute_index_funds_returns(SECTOR_DICT_MAP[sector])
                # Cache in session state
                st.session_state.tab1_sector = sector
                st.session_state.tab1_returns_df = returns_df
                st.rerun()
        
        # Display cached results if available
        if st.session_state.tab1_returns_df is not None:
            st.subheader(f"Returns — {st.session_state.tab1_sector} (as of {TDY_DATE})")
            def flatten_columns(df):
                if isinstance(df.columns, pd.MultiIndex):
                    df = df.copy()
                    df.columns = [
                        " - ".join([str(x) for x in col if x is not None and str(x) != ""])
                        for col in df.columns
                    ]
                return df
            st.dataframe(flatten_columns(st.session_state.tab1_returns_df), use_container_width=True)
        else:
            st.info("Select a sector and click **Compute Returns**.")

# --- Tab 2: Index Charts ---
with tab2:
    st.subheader("Index Return Chart")
    
    # Initialize session state for tab2
    if "tab2_sector" not in st.session_state:
        st.session_state.tab2_sector = None
    if "tab2_figs" not in st.session_state:
        st.session_state.tab2_figs = None
    
    # Left column for inputs
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### Select Index")
        sectors = sorted(SECTOR_DICT_MAP.keys())
        chart_sector = st.selectbox("Choose sector", sectors, index=0, key="chart_tab2")
        run_chart = st.button("Plot Rolling Returns", type="primary")
    
    with col2:
        if run_chart:
            with st.spinner("Fetching data and plotting..."):
                figs = plot_rolling_returns_from_index_dict(SECTOR_DICT_MAP[chart_sector])
                # Cache in session state
                st.session_state.tab2_sector = chart_sector
                st.session_state.tab2_figs = figs
                st.rerun()
        
        # Display cached results if available
        if st.session_state.tab2_figs is not None:
            for tenor, fig in st.session_state.tab2_figs.items():
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select an index and click **Plot Rolling Returns**.")

# --- Tab 3: Top Performers ---
with tab3:
    st.subheader("Top Performers Across All Sectors")
    
    # Initialize session state for tab3
    if "tab3_top_performers" not in st.session_state:
        st.session_state.tab3_top_performers = None
    if "tab3_sector_summary" not in st.session_state:
        st.session_state.tab3_sector_summary = None
    if "tab3_periods" not in st.session_state:
        st.session_state.tab3_periods = None
    if "tab3_top_n" not in st.session_state:
        st.session_state.tab3_top_n = 100
    
    # Left column for inputs
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### Settings")
        top_n = st.number_input("Number of top performers", min_value=1, max_value=1000, value=100, key="top_n")
        periods_input = st.text_input("Enter periods (comma-separated)", value="1M, 3M, 6M, 1Y, 2Y, 3Y", key="top_perf_periods")
        # Parse the input into a list
        selected_periods = [p.strip() for p in periods_input.split(",") if p.strip()]
        run_top = st.button("Find Top Performers", type="primary")
    
    with col2:
        if run_top:
            if not selected_periods:
                st.warning("Please select at least one period.")
            else:
                with st.spinner("Computing returns for all funds..."):
                    # Compute all funds returns
                    all_returns = compute_all_funds_returns(SECTOR_DICT_MAP, periods=selected_periods)
                    
                    if all_returns.empty:
                        st.warning("No data available.")
                    else:
                        # Get top performers
                        top_performers = get_top_performers(all_returns, periods=selected_periods, top_n=top_n)
                        
                        # Get sector summary
                        sector_summary = get_sector_summary(top_performers, all_returns, top_n)
                        
                        # Cache in session state
                        st.session_state.tab3_top_performers = top_performers
                        st.session_state.tab3_sector_summary = sector_summary
                        st.session_state.tab3_periods = selected_periods
                        st.session_state.tab3_top_n = top_n
                        st.rerun()
        
        # Display cached results if available
        if st.session_state.tab3_top_performers is not None:
            for period in st.session_state.tab3_periods:
                if period in st.session_state.tab3_top_performers:
                    st.markdown(f"#### Top {st.session_state.tab3_top_n} Performers - {period}")
                    st.dataframe(st.session_state.tab3_top_performers[period], use_container_width=True)
                                
                    # Display sector summary
                    if st.session_state.tab3_sector_summary is not None and period in st.session_state.tab3_sector_summary:
                        st.markdown(f"**Sector Summary - {period}**")
                        st.dataframe(st.session_state.tab3_sector_summary[period], use_container_width=True)
                    st.markdown("---")
        else:
            st.info("Select the number of top performers and periods, then click **Find Top Performers**.")