# Number Info Bot

Telegram bot - 10 digit number se info nikalta hai.

## Deploy (Railway - Recommended)

1. Is folder ko GitHub pe upload karo
2. https://railway.app pe jao → New Project → Deploy from GitHub
3. Variables mein add karo:
   - Name: `BOT_TOKEN`
   - Value: apna BotFather token
4. Deploy ho jayega

## Local run

```bash
export BOT_TOKEN="your_token_here"
pip install -r requirements.txt
python bot.py
```
