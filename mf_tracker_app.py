# --- Import libraries ---
import pandas as pd
from nselib import capital_market
import numpy as np
import matplotlib.pyplot as plt
from mftool import Mftool
from yahooquery import Ticker
from datetime import date
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import index_raw
import yfinance as yf
import re
from typing import List, Optional
from nsetools import Nse
from nsepython import index_history
import streamlit as st

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
        "Aditya Birla Sun Life Multi Asset Allocation Fund-Direct Growth": "Aditya Biral Multiasset",
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
        "Aditya Birla Sun Life Multi-Cap Fund-Direct Growth": "Aditya Biral Multicap",
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
        "CAPITALMIND FLEXI CAP FUND DIRECT GROWTH": "CapitalMind Flexicap"
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
        "WhiteOak Capital Large Cap Fund Regular Plan Growth": "WhiteOak Capital Largecap",
        "BARODA BNP PARIBAS LARGE CAP Fund - Direct Plan - Growth Option": "Baroda BNP Largecap",
        "BANK OF INDIA Large Cap Fund Direct Plan Growth": "BoI Largecap",
        "Edelweiss Large Cap Fund - Direct Plan-Growth option": "Edelweiss Largecap",
        "JM Large Cap Fund (Direct) - Growth Option": "JM Largecap",
        "Kotak Large Cap  Fund - Growth - Direct": "Kotak Largecap",
        "CANARA ROBECO LARGE CAP FUND - DIRECT PLAN - GROWTH OPTION": "Canara Robeco Largecap",
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
        "Motilal Oswal Large Cap Direct Plan Growth": "Motilal Oswal Largecap"
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
        "Bank of India Mid Cap Fund - Direct Plan Growth": "BoI Midcap"
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
        "Mahindra Manulife Small Cap Fund - Direct Plan - Growth":"Mahindra Manulife Smallcap"
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
        "HSBC Value Fund - Direct Growth": "HSBC Value",
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
        "Motilal Oswal Focused 25 Fund (MOF25)- Direct Plan Growth Option": "Motilal Focused",
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
        "Kotak Nifty Financial Services Ex-Bank Index Fund - Direct Plan - Growth option": "Kotak NIFTY (ex-bank)Financial",
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
        "Nippon India Nifty IT Index Fund - Direct Plan - Growth Option": "Nipppon NIFTY Tech"
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
    "HEALTHCARE":HEALTHCARE,
    "FINANCIALS":FINANCIALS,
    "CONSUMER":CONSUMER,
    "IT":IT
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

def fetch_benchmark_index_data(ticker,start_date="01-Jan-2010",end_date=TDY_DATE):
    historical_data = index_history(ticker,start_date=start_date,end_date=end_date)
    historical_data = pd.DataFrame(historical_data)
    #print(historical_data.head())
    rolling_ret_df = hybrid_returns_table( df = historical_data[["HistoricalDate","CLOSE"]].set_index("HistoricalDate"),
               periods = ROLLING_RETURN_PERIODS,
               name=ticker,
               nav_col="CLOSE",
               date_format="%d %b %Y"
            )
    pp_ret_df = compute_period_returns( df = historical_data[["HistoricalDate","CLOSE"]].set_index("HistoricalDate"),
                periods = POINT_TO_POINT_RETURN_PERIODS,
                name=ticker,
                nav_col="CLOSE",
                date_format="%d %b %Y"
                )
    return pd.concat([rolling_ret_df,pp_ret_df],axis=1)

def compute_index_funds_returns(index_dict):
    all_returns_df = pd.DataFrame()

    for x,y in index_dict.items():
        if x == "Benchmark":
            for idx in y:
                #print(y)
                ret_df = fetch_benchmark_index_data(ticker=idx)
                all_returns_df = pd.concat([all_returns_df,ret_df])
        
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

st.set_page_config(page_title="Sector Returns", layout="wide")
st.title("Sector Returns Dashboard")
st.sidebar.header("Inputs")
sectors = sorted(["SMALL_CAP","MULTI_ASSET","MULTI_CAP","FLEXI_CAP",
                  "LARGE_CAP","MID_CAP","CONTRA","FOCUSED","OTHER",
                  "HEALTHCARE","FINANCIALS","CONSUMER","IT"
                  ])

sector = st.sidebar.selectbox("Select sector", sectors, index=0)
run = st.sidebar.button("Compute returns", type="primary")

if run:
    returns_df = compute_index_funds_returns(SECTOR_DICT_MAP[sector])
    st.subheader(f"Returns — {sector} (as of {TDY_DATE})")
    def flatten_columns(df):
        if isinstance(df.columns, pd.MultiIndex):
            df = df.copy()
            df.columns = [
                " - ".join([str(x) for x in col if x is not None and str(x) != ""])
                for col in df.columns
            ]
        return df

    st.dataframe(flatten_columns(returns_df), use_container_width=True)
else:
    st.info("Choose a sector and click **Compute returns**.")