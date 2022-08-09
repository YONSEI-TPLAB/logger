import subprocess
import sys
import os
from os.path import join, dirname

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
  import telegram
  from dotenv import load_dotenv
except ImportError:
  install('python-telegram-bot')
  install('python-dotenv')
  import telegram
  from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path) ## to seperate private contents to .env file

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') if 'TELEGRAM_CHAT_ID' in os.environ else None

def get_recent_chat_id(*, verbose=False):

  # TELEGRAM: CONNECT with Telegram Bot
  bot = telegram.Bot(TELEGRAM_BOT_TOKEN)

  # Get Chat ID
  updates = bot.getUpdates()

  if len(updates) > 0:
    if verbose: print(f'Chat ID is set as {updates[-1].message.chat_id}, whose first name is {updates[-1].message.chat.first_name}')
    return updates[-1].message.chat_id
  else:
    raise Exception('Chat ID not found, please send any message to bot to get your chat ID')


def logger_telegram(title, message=None, *, chat_id=None, verbose=False):
  """
  Args:
      title ([String]): text to be added on card's title
      message ([String], optional): any message as a card's text. Defaults to None.
  """
    
  # TELEGRAM: CONNECT with Telegram Bot
  bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
  
  if chat_id is None:
    if TELEGRAM_CHAT_ID is not None:
      chat_id = TELEGRAM_CHAT_ID
    else:
      try:
        chat_id = get_recent_chat_id()
      except:
        raise Exception('Chat ID not found, please send any message to bot to get your chat ID')

  ls_message = []

  ls_message.append("\U0001F1F5 %s" % title)
  if message is not None: ls_message.append("%s" % message)
  ls_message.append("\n")

  # TRACEBACK: Get current system exception
  ex_type, ex_value, ex_traceback = sys.exc_info()
  if ex_type is not None:
    # TRACEBACK: Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)
    
    # TELEGRAM: Add text to the CARD and summary to the NOTIFICATION
    ls_message.append("\u2757\uFE0F %s: %s" % (ex_type.__name__, ex_value))

    # TRACEBACK: Format stacktrace
    for trace in trace_back:
      # create the section and add it to the connector card object
      ls_message.append("\n")
      ls_message.append("Traceback (most recent call last):")
      ls_message.append("File: %s,  Line %d,  Func.Name %s,  Message: %s" % (trace[0], trace[1], trace[2], trace[3]))

  text_message='\n'.join(ls_message)
  bot.send_message(chat_id, text=text_message)
  # print(text_message)