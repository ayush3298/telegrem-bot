
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import sqlite3

logging.basicConfig(filename='example.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, DOB ,EMAIL , MOB  , BIO = range(7)

#databse handler can not be created out of method due to diff threads


def start(bot, update):#insert name and chat id into database
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    usr_id = str(user.id)
    name = str(user.first_name)
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    greet = "Hello "
    greet = greet + name
    greet = str(greet)
    update.message.reply_text(greet)

    update.message.reply_text(
        'Hi My name is jarivs created by Ayush. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    cur.execute('insert or ignore into details(name , chat_id) values(? ,?)', (name,usr_id,))
    conn.commit()

    return GENDER


def gender(bot, update):#insert gender into database
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    usr_id = str(user.id)
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    gndr = str(update.message.text)
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like,',
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('or /skip')
    cur.execute('update details set gender = ?  where chat_id = ?', (gndr,usr_id,))
    conn.commit()

    return PHOTO


def photo(bot, update):
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    name = str(user.first_name)
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    img_file = name
    ext = '.jpg'
    full = str(img_file + ext)
    photo_file.download(full)
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, ')
    update.message.reply_text('or simply  /skip')

    return LOCATION


def skip_photo(bot, update):
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    name = user.first_name
    usr_id = str(user.id)
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, ')
    update.message.reply_text('or /skip')
    conn.commit()

    return LOCATION


def location(bot, update):#update location into databse
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    usr_id = str(user.id)
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'Now can you tell me your email id ')
    update.message.reply_text('or /skip')
    loc = user_location.latitude , user_location.longitude
    loc = str(loc)
    cur.execute('update details set location = ?  where chat_id = ?' , (loc,usr_id,))
    conn.commit()
    print(loc)
    return EMAIL

    


def skip_location(bot, update):
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    usr_id = str(user.id)
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me your email id')
    update.message.reply_text('or /skip')

    return EMAIL

def email(bot , update):#update email id into database
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    email = update.message.text
    usr_id = str(user.id)
    email = str(email)
    logger.info("Email of of %s: %s  ", user.first_name, email)
    
    update.message.reply_text('Ayush would love to wish you on your birthday '
                              'can you tell me your date of birth '
                              'please send your date of birth in dd/mm/yyyy format')
    update.message.reply_text('or /skip')
    cur.execute('update details set email = ?  where chat_id = ?' , (email,usr_id,))
    print(email)
    conn.commit()
    return DOB

def skip_email(bot, update):
    update.message.reply_text('ops you didnt shared email but Ayush would love to wish you on your birthday '
                              'can you tell me your date of birth'
                              'please send your date of birth in dd/mm/yyyy format')
    update.message.reply_text('or /skip')
    return DOB
        
    

def dob(bot , update):#update date of birth in database
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    dob = update.message.text
    usr_id = str(user.id)
    dob = update.message.text
    dob = str(dob)
    logger.info("DOB of of %s: %s ", user.first_name, dob)
    cur.execute('update details set dob = ?  where chat_id = ?' , (dob,usr_id,))
    conn.commit()
    update.message.reply_text('Thank you for sharing your date of birth, i would defenately remember that'
                              'can you share your contact number with him?')
    update.message.reply_text('or /skip')
    return MOB

def skip_dob(bot , update):
    update.message.reply_text('You dont want him to wish you... i am feeling sad'
                              'can you share your contact number with him?')
    update.message.reply_text('or /skip')

    return MOB

def mob(bot , update):#insert phone number into database
    conn = sqlite3.connect('C:\\Users\\ADMIN\\Google Drive\\tele_details.sqlite')
    cur = conn.cursor()
    user = update.message.from_user
    mob = update.message.text
    usr_id = str(user.id)
    update.message.reply_text('Thank you for sharing your contact number ,'
                              'it has been a great talk with you ')
   
    logger.info("Email of of %s: %s ", user.first_name, mob)
    cur.execute('update details set mob = ?  where chat_id = ?' , (mob,usr_id,))
    conn.commit()
    
    return ConversationHandler.END

def skip_mob(bot , update):
    update.message.reply_text(' thank you it has been a great talk with you ')
    return ConversationHandler.END

def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(key)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [RegexHandler('^(Boy|Girl|Other)$', gender),
                     MessageHandler(Filters.text , gender)],
            

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],
            
            DOB: [MessageHandler(Filters.text, dob),
                       CommandHandler('skip', skip_dob)],

            EMAIL: [MessageHandler(Filters.text, email),
                       CommandHandler('skip', skip_email)],

            MOB: [MessageHandler(Filters.all, mob),
                       CommandHandler('skip', skip_mob)],
            BIO: [MessageHandler(Filters.text, bio)],
            
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    
    

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


