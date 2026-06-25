# etf-princing-mm-project
### ETF pricing and market making project

#### 21/06/26

- Made the Repo on Github
- Created the venv and downloaded the main libraries (see requirements.txt)
- Created the folder and file skeleton
    - src/ is the production code (reusable logic you'll import from notebooks or scripts, it keeps notebooks thin)
        - config.py is a central place for constants (to avoid hard coding everywhere). It contains ETF tickers, date ranges, files paths, maybe config.
        - __init__.py makes src/ and data as a Python package so I can import from it
        - data are functions to pull data (like from yfinance) and save it under data/raw/
    - data/ are files on disk (it separates code from data)
        - raw/ is for untouched downloads (CSV, Parquets, etc.). You can always re-fetch or re-process from here
        - processed/ is for cleaned outputs like adjusted prices, returns, spreads, features, etc.
    - notebook/ is for exploration where you experiment, visualize, and test ideas before moving stable code into src/. The 00_ prefix suggests this is the first checkpoint: "can I fetch and load data?"
    - requirements.txt for what to pip install to reproduce the environment
    - README is for the explanation of what the project is, how to run it, the observations and conclusions.
    - gitignore is the list of what to ignore before pushing on git so the repository stays clean and light
- Modified the gitignore to ignore many things.


#### 25/06/26

- Added the dates and ETF tickers in the config.
    - ^NDX is the BS underlying as QYLD (the etf we price) writes the call on the Nasdaq-100 index itself (European, cash-settle)
    - QYLD is the ETF I'm pricing and my validation target. Myst be auto_adjust = False to not corrupt the premium/discount with monthly distribution and adjusted closes.
    - ^VXN is the sigma for the BS formula. It's the 30-day implied vol. on the Nasdaq-100 which is exactly the option QYLD writes, so we get market implied vol. for free instead of buying option data (sigma = VXN/100).
    - ^IRX is the risk-free rate (r=IRX/100). The risk-free input uses the 13-week T-bill discount yield directly; at one-month tenor the discount-basis and compounding conventions affect the option price below the level of one tick, so no conversion is applied.
    - QQQ is sanity cross-check only. It confirms that ^NDX is behaving. Should not price off it.

#### 
