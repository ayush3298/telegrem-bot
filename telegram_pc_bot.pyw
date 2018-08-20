
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import subprocess
import ctypes
import telegram
import pyautogui
bot = telegram.Bot(token="462995021:AAFYoHb0-yZR25ybK_4kZSrfVxwFr4ZGEXA")
bot.send_message(chat_id=501091989, text="Hello sir your pc was logged in")

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello sir here are set of commands \n'
                              'shutdown = /shutdown \n'
                              'lock your pc  - /lock \n'
                              'screenshoot = /screenshoot \n')
def take_screenshoot(bot,update):
    pic = pyautogui.screenshot()
    pic.save('C:\\Users\\ADMIN\\Google Drive\\python\\coursera\\Screenshot.png')
    update.message.reply_text('Saving Screenshoot')
    bot.send_photo(chat_id=501091989, photo=open('C:\\Users\\ADMIN\\Google Drive\\python\\coursera\\Screenshot.png', 'rb'))


def shutdown(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('do you really want to shut down?')
    update.message.reply_text('ok sir , we will shutdown the pc')
    subprocess.call(["shutdown", "/s"])


    
def lock(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('ok sir , we will lock the pc')
    ctypes.windll.user32.LockWorkStation()
    
def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)




def main():
    
    updater = Updater("462995021:AAFYoHb0-yZR25ybK_4kZSrfVxwFr4ZGEXA")

    
    dp = updater.dispatcher

    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("shutdown", shutdown))
    dp.add_handler(CommandHandler("lock", lock))
    dp.add_handler(CommandHandler("screenshoot", take_screenshoot))


    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
   

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    
