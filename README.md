# Slack-Bot-Wallet-Tracker
Slack Bot sends message in channel when notified of an address transfer from Alchemy Webhook

## Create Python Environment (use pip for installs)
1. Install flask
2. Install ngrok
3. Install dotenv
4. Install flask_ngrok
5. Install requests


## Create Webhook Using Alchemy Webhook Dashboard 
1. Address Activity
2. Choose network and chain (testnet/mainnet) and (ethereum or l2)
3. Input address (or addresses) to track activity on
4. throw ngrok url in for testing webhook (https://dashboard.ngrok.com/endpoints)


## Slack Bot
1. Create app
2. From scratch
3. Add the bot to your channel
4. Add necessary OAuth settings (incoming webhooks and write to channel)
5. Find slack URL to use in your script (create .env file and put it there)

## To run the process
1. Start python environment
2. Run script "python script.py"
3. Run "ngrok http 5000"
4. Open ngrok dashboard to grab endpoint URL and use that for Alchemy Webhook URL
   
