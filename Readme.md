Description:

    This chatbot is designed to provide users with a convenient way to view 
    the history of all their incoming transactions on the bscscan exchange.
    
    The bot provides information about transaction details such as:
    date, type, amount of cryptocurrency, exchange rate (if any), 
    and other additional data.
    
    Interaction with the bscscan exchange API:
    The bot accesses the exchange's API to obtain information about user 
    transactions. It interacts with the exchange's API to get transaction 
    data and details.

TECHNOLOGY STACK:

    python-telegram-bot
    requests
    api for bscscan.com
    docker

to start:

    clone this repo
    
    run command in virtual envoriment "pip install -r requirements.txt"
    
    run in terminal "python bot.py"

bot address :

    https://t.me/BscScanTestTask_bot

optional you can run it by docker:

    docker build -t bsc_bot .
    docker run bsc_bot
