# SUTDKindnessBot
Bot allows user to input a quote that saves to Quotes.txt. Bot also allows user to get a kind message from Quotes.txt together with a mental wellness comic. Bot holds a conversation with user that ultimately shares resource packs in user's preferred media choice. 


## API
ApI used: Python-Telegram-Bot <br />
Bot incorporates two Handlers  <br />
1. MessageHandler  - process and obtain user's text input after a specific command <br />
  - called upon by */share telegram command 
2. ConversationHandler  - holds a conversation with user and send resources <br />
  - utilise inbuilt keyboard with keywords like videos, musics, platforms etc. to ensure bot-user communicatons


## Installation: 
1. Install python-telegram-bot via (https://pypi.org/project/python-telegram-bot/) <br />
`pip install python-telegram-bot`
2. Register your own bot with BotFather on Telegram, obtain the API token <br />
3. Replace API token with your bot's token  <br />
4. Run the file on command prompt <br />
