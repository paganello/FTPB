
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

import os
import sys

sys.path.append('./src')
import DataBaseHandler
import AzureImageProcessor
import other_functions

sys.path.append('./src/openai')
import OpenaiTextProcessor

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I'm a bot that can help you with your exit. read the guide to know how to use me.")


async def manage_text_message(update: Update, context: CallbackContext):  

    # Get Updates and list words
    text = update.message.text
    json_file = other_functions.text_slicer(text)

    # Verify text format
    if(other_functions.verify_formatted_text_input(json_file)):

        # if correct try to update the DB
        if(DataBaseHandler.update(json_file)):
            await update.message.reply_text("Done")
        else:
            await update.message.reply_text("Your input is not valid. Please, read the guide and try again.")

    # If format is wrong
    else:

        # Use GPT-3.5 --> reform text to JSON
        d = await OpenaiTextProcessor.t_make_request_using_custom_model(text)

        jsons = other_functions.json_reformatter(d)

        for json_file in jsons:  

            if(DataBaseHandler.update(json_file)):
                await update.message.reply_text("done")
            else:
                await update.message.reply_text("db error")


async def manage_image_message(update: Update, context: CallbackContext):
    
    # Get update
    file_id = update.message.photo[-1].file_id

    # Get the file object
    file = await context.bot.get_file(file_id)

    # Download the file
    if other_functions.download_file(file.file_path, other_functions.get_settings("IMAGE_NAME")):
        await update.message.reply_text("image received")

    text = await AzureImageProcessor.i_make_request(other_functions.get_settings("IMAGE_NAME"))

    # Start image elaboration
    d = OpenaiTextProcessor.t_make_request_using_custom_model(text)

    jsons = other_functions.json_reformatter(d)

    for json_file in jsons:
        # Verify the list
        if(DataBaseHandler.update(json_file)):
            await update.message.reply_text("done ")
        else:
            await update.message.reply_text("Your input is not valid. Please, read the guide and try again.")

    os.remove(other_functions.get_settings("IMAGE_NAME"))


            
def main():

    application = ApplicationBuilder().token(other_functions.get_credentials('TELEGRAM_TOKEN')).build()

    # Chat commands
    application.add_handler(CommandHandler('start', start))

    # Triggers
    application.add_handler(MessageHandler(filters.TEXT, callback= manage_text_message))
    application.add_handler(MessageHandler(filters.PHOTO, callback= manage_image_message))

    # Run app in background
    application.run_polling()

if __name__=='__main__':
   main()