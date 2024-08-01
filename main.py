
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

from src import DataBaseHandler, AzureImageProcessor, OpenaiTextProcessor
from src.utils import download_utils, dir_and_data_getters, json_consistency_helper, TextFormatter
from src.utils.TextFormatter import TextFormatter

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("ready")


async def manage_text_message(update: Update, context: CallbackContext):  

    # Get Updates and list words
    text = update.message.text
    json_file = json_consistency_helper.text_slicer(text)

    # Initilize a text formatter object
    status = TextFormatter()

    # Store chat ID for later use 
    chat_id = update.message.chat_id

    # Verify text format
    formatting_status = json_consistency_helper.verify_formatted_text_input(json_file)

    if formatting_status is not False:
        # if correct try to update the DB
        DB_status = DataBaseHandler.update(json_file)
        update.message.reply_text(TextFormatter.printSummary(json_file, DB_status))

    else:
        status.add("<i>AI text elaboration :</i>", "⌛")
        context.user_data['msg'] = await context.bot.send_message(chat_id=chat_id, text=status.format(), parse_mode='HTML')
        status.remove_last()

        # Use GPT-3.5 --> reform text to JSON
        elaborated_text = OpenaiTextProcessor.t_make_request_using_custom_model(text)

        if elaborated_text is not None:
            status.add("<i>AI text elaboration :</i>", "👌")
            await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=status.format(), parse_mode='HTML')
        else:
            status.add("<i>AI text elaboration :</i>", "❌")
            await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=status.format(), parse_mode='HTML')
            return

        jsons = json_consistency_helper.json_reformatter(elaborated_text)
        summary_datas = jsons[0]

        DB_status = DataBaseHandler.update(jsons)
        if DB_status is not False:
            status.add("<i>DB Updated :</i>", "👌")
            await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=status.format(), parse_mode='HTML')
        else:
            status.add("<i>DB_Updated :</i>", "❌")
            await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=status.format(), parse_mode='HTML')
    
        await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=TextFormatter.printSummary(summary_datas, DB_status), parse_mode='HTML')
    



async def manage_image_message(update: Update, context: CallbackContext):

    # Get update
    file_id = update.message.photo[-1].file_id

    # Get the file object
    file = await context.bot.get_file(file_id)

    # Get the last image name and dir
    last_img_name = dir_and_data_getters.create_timebased_img_name()
    last_img_dir = dir_and_data_getters.get_current_dir() + "/../images/" + last_img_name

    # Initilize a text formatter object
    status = TextFormatter()

    # Store chat ID for later use 
    chat_id = update.message.chat_id

    # Download the file
    download_status = download_utils.download_file(file.file_path, last_img_dir)
    if download_status is not False:
        status.add("<i>Image received :</i>", "👌")
        context.user_data['msg'] = await context.bot.send_message(chat_id=chat_id, text=status.format(), parse_mode='HTML')    # Save the message info to edit it later
    else:
        status.add("<i>Image received :</i>", "❌")
        await context.bot.send_message(chat_id=chat_id, text=status.format())
        return
    
    # Image to text conversion
    image_to_text= await AzureImageProcessor.i_make_request(last_img_dir)
    if image_to_text is not False:
        status.add("<i>Translation :</i>", "👌")
        await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=status.format(), parse_mode='HTML')
    else:
        #print(context.user_data)
        status.add("<i>Translation :</i>", "❌")
        await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=status.format(), parse_mode='HTML')
        return

    # Start image elaboration
    elaborated_text = OpenaiTextProcessor.t_make_request_using_custom_model(image_to_text)

    jsons = json_consistency_helper.json_reformatter(elaborated_text)
    summary_datas = jsons[0]

    DB_status = DataBaseHandler.update(jsons, last_img_name)
    if DB_status is not False:
        status.add("<i>DB Updated :</i>", "👌")
        await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=status.format(), parse_mode='HTML')
    else:
        status.add("<i>DB_Updated :</i>", "❌")
        await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=status.format(), parse_mode='HTML')
    
    await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data['msg'].message_id, text=TextFormatter.printSummary(summary_datas, DB_status), parse_mode='HTML')
    

def main():

    application = ApplicationBuilder().token(dir_and_data_getters.get_credentials('TELEGRAM_TOKEN')).build()

    # Chat commands
    application.add_handler(CommandHandler('start', start))

    # Triggers
    application.add_handler(MessageHandler(filters.TEXT, callback= manage_text_message))
    application.add_handler(MessageHandler(filters.PHOTO, callback= manage_image_message))

    # Run app in background
    application.run_polling()

if __name__=='__main__':
   main() 