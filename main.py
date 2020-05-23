from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import requests
import logging
import random
import re

token = 'insert token http api'

logger = logging.getLogger(__name__)
CHECK, WAIT = range(2)

def start(update, context):
    user = update.message.from_user
    name = user['username']
    chat_id = update.message.chat_id
    welcome = 'Welcome {}! I am Cloud, a messenger for kind messages. I hope to make you feel less alone in these tough times. You can receive a kind message from a stranger (use /get) or send one of your own (use /share). To access some useful resources and tips, use /more'.format(name)
    context.bot.send_message(chat_id, welcome)
    
def sendhelp(update, context):
    chat_id = update.message.chat_id
    sendhelp = "May is Mental Health Awareness Month. You can receive a kind message from a stranger (use /get) or send one of your own (use /share). \n\n Use /more to access a compilation of useful resources and tips to empower you to take charge and take care of your mental health. I'm here for you!"
    context.bot.send_message(chat_id, sendhelp)

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def bop(update, context):
    url = get_url()
    # get receipient chat id
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo=url)

def jang(update,context):
    randnum = random.randrange(0, 31)
    link = str(randnum) + ".jpg"
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo=open(link, 'rb'))

def get(update, context):
    f = open('Quotes.txt', 'r')
    quotes = []
    for lines in f: 
        quote = lines.strip()
        quotes.append(quote)
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, "From a kind stranger~")
    randnum = random.randrange(1, len(quotes))
    context.bot.send_message(chat_id, quotes[randnum])
    # bop(update, context)
    jang(update,context)
      
def share(update, context): 
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, "Send your quote here! You can send as many as you like. Use /cancel to stop sharing.")
    global echo_handler
    echo_handler = MessageHandler(Filters.text & (~Filters.command), save)
    dp.add_handler(echo_handler, group=1)
    
def save(update, context): 
    user = update.message.from_user
    name = user['username']
    chat_id = update.message.chat_id
    with open('Quotes.txt', 'a') as f: 
        f.write('\n' + update.message.text )
    logger.info("Quote of %s: %s", name, update.message.text)    
    context.bot.send_message(chat_id, "Thank you kind stranger for spreading love~")
    
def cancel(update, context): 
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, "Bye! Thanks for sharing. Take care~ Love, Cloud ")
    try: 
        dp.remove_handler(echo_handler, group=1)
        context.update_queue.append(update)
        return ConversationHandler.END
    except: 
        pass

def platforms(update,context):
    chat_id = update.message.chat_id
    links = """Platforms: \n\n <a href="https://www.chat.mentalhealth.sg/downloads/">CHAT</a>
      <em>- A national outreach programme for Youth Mental Health</em>
            \n <a href="https://www.healthhub.sg/live-healthy/561/mentalillnessesfacedbyadults">HealthHub</a>
      <em>- A platform to read about Health articles and take part in Health Events</em>
             """
    context.bot.send_message(chat_id, links, parse_mode = ParseMode.HTML)
    return ConversationHandler.END

def videos(update,context):
    chat_id = update.message.chat_id
    links = """Interesting Videos: \n\n <a href="https://www.youtube.com/watch?v=VQoiz4wfV_c">A Social Experiment on Mental Health Stigma</a>
            <em>- National Council of Social Service</em>
            \n <a href="https://www.youtube.com/watch?v=yikyGL5XT84">Unboxing Depression</a>
            <em>- Singapore Association for Mental Health</em>
            """
    context.bot.send_message(chat_id, links, parse_mode = ParseMode.HTML)
    return ConversationHandler.END

def music(update, context): 
    chat_id = update.message.chat_id
    links = """Songs: \n\n<a href = "https://www.huffpost.com/entry/songs-about-mental-health_l_5e326e79c5b69a19a4a9f977">16 Powerful Songs</a>
            <em>- to make you feel less alone </em>
            """
    context.bot.send_message(chat_id, links, parse_mode = ParseMode.HTML)
    return ConversationHandler.END

def resources(update, context): 
    chat_id = update.message.chat_id
    links = """Resources: \n  <a href = "https://blog.moneysmart.sg/healthcare/counselling-singapore-free-affordable/"> Free and Affordable Help for Mental Healthcare</a>
            """
    context.bot.send_message(chat_id, links, parse_mode = ParseMode.HTML)
    return ConversationHandler.END

def reads(update, context): 
    chat_id = update.message.chat_id
    links = """Interesting Articles: \n\n<a href="https://www.channelnewsasia.com/news/singapore/mental-health-youths-suicide-depression-listen-11994612">[Youth]Let's Talk about Mental Health</a>
            <em>- Channel News Asia</em>
            \n<a href="https://www.aic.sg/sites/silverpagesassets/SilverPages%20Assets/Content%20Images/Mental%20Health/Magnet.JPG">[Residents]Caring for those around you</a>
            <em>- Agency for Integrated Care</em>
            \n<a href="https://www.mentalhealth.org.uk/your-mental-health/looking-after-your-mental-health">[Self]Looking after your mental health</a>
            <em>- Mental Health Foundation UK </em>          
            """
    context.bot.send_message(chat_id, links, parse_mode = ParseMode.HTML)
    return ConversationHandler.END
    
def more(update,context): 
    chat_id = update.message.chat_id
    reply_keyboard = [['videos', 'music', 'reads']
    ,['platforms', 'resources']]
    text = "What is your preferred Media Type?"
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHECK
    
def check(update, context): 
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    choice = update.message.text
    waste = ['Unlocking path to knowledge...', 'Finding way to Nirvana...', 'Buying a Bigger brain...', 'Searching for soul...','Loading Unloading']
    num = random.randrange(0, len(waste))
    update.message.reply_text(waste[num],
                              reply_markup=ReplyKeyboardRemove())
    if choice == 'videos':
        videos(update,context)
    elif choice == 'music':
        music(update,context)
    elif choice == 'reads':
        reads(update,context)
    elif choice == 'platforms':
        platforms(update,context)
    elif choice == 'resources':
        resources(update, context)
    return WAIT

def wait(update, context): 
    if update.message.text == "/more":
        more(update, context)
    else:
        pass

def main():
    updater = Updater(token, use_context=True)
    global dp
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    dp.add_handler(CommandHandler('share',share))
    dp.add_handler(CommandHandler('get',get))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',sendhelp))
    dp.add_handler(CommandHandler('cancel',cancel))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('more', more)],

        states={
            CHECK:[MessageHandler(Filters.text, check)],
            WAIT: [MessageHandler(Filters.command, wait)]
            },

        fallbacks=[CommandHandler('cancel', cancel)], 
        allow_reentry=True
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
