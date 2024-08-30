import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler
from data_preparation import process_person
from constants import BOT_TOKEN, bot_chatID

# Function to send text messages and images to a Telegram bot
def telegram_bot_sendtext(bot_message, path=None):
    # Sending the text message
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    
    # If an image path is provided, send the image
    if path is not None:
        url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendPhoto"
        files = {'photo': open(path, 'rb')}
        data = {'chat_id': bot_chatID}
        res = requests.post(url, files=files, data=data)

# Function to create a new entry in the system
def createEntry(update: Update, context: CallbackContext) -> None:
    details = update.message.text
    user = details.split(",")
    
    # Extracting details from the message
    name, role, start_time, end_time = user[0], user[1], user[2], user[3]
    start_time = int(start_time)
    end_time = int(end_time)

    # Processing the person entry
    process_person(name, role, start_time, end_time)

# Function to prompt the user to save the visitor's details
def save(update: Update, context: CallbackContext) -> None:
    save = update.message.text
    if save.lower() == "yes":
        update.message.reply_text("If they are a family member, enter their details like:\n Name,Family\nOtherwise, enter visitor details like:\n Name,OneTime,12AM(time).")

# Function to handle the permission to allow or deny entry for an unknown person
def permission(update: Update, context: CallbackContext) -> None:
    allow = update.message.text
    print(allow)
    if allow.lower() == "allow":
        update.message.reply_text("Is this a frequent visitor?\n Should I save their details: Yes / No.")
    else:
        update.message.reply_text("The visitor has been denied entry.")

# Function to handle the permission to allow or deny entry for a known person at the wrong time
def known_person_permission(update: Update, context: CallbackContext) -> None:
    allow = update.message.text
    print(allow)
    if allow.lower() == "allow":
        update.message.reply_text("Granting access.")
    else:
        update.message.reply_text("The visitor has been denied entry.")

# Function to handle cases where a known person tries to enter at an unauthorized time
def known_person_wrong_time(text):
    global updater
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Send a notification to the user via Telegram
    telegram_bot_sendtext(text)
    
    # Add handler to respond to user's permission decision
    dispatcher.add_handler(MessageHandler(filters.regex('^(Allow|allow|Deny|deny)$'), known_person_permission))
    
    # Start polling for updates
    updater.start_polling()
    updater.idle()

# Function to handle messaging and image sending
def messaging(text, image=None):
    global updater
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Send a message and optionally an image to the user via Telegram
    telegram_bot_sendtext(text, image)
    
    # Add handlers for different types of user input
    dispatcher.add_handler(MessageHandler(filters.regex('^.*[,].*$'), createEntry))
    dispatcher.add_handler(MessageHandler(filters.regex('^(yes|Yes|no|No)$'), save))
    dispatcher.add_handler(MessageHandler(filters.regex('^(Allow|allow|deny|Deny)$'), permission))
    
    # Start polling for updates
    updater.start_polling()
    updater.idle()

# Main function to start the bot and test specific scenarios
def main():
    # Example usage: Known person tries to enter at the wrong time
    known_person_wrong_time("Someone recognized, but at the wrong time. Should I allow or deny?")

if __name__ == "__main__":
    main()
