import os
from os.path import join, dirname
import sys
import traceback
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
  import pymsteams
  from dotenv import load_dotenv
except ImportError:
  install('pymsteams')
  install('python-dotenv')
  import pymsteams
  from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path) ## to seperate private contents to .env file

TEAMS_CONNECTCARD_WEBHOOK_URL = os.environ.get('TEAMS_CONNECTCARD_WEBHOOK_URL')


def logger_teams(title, message=None):
  """
  Args:
      title ([String]): text to be added on card's title
      message ([String], optional): any message as a card's text. Defaults to None.
  """

  # MSTEAMS: Create the CONNECTORCARD object with the Microsoft Webhook URL
  myTeamsMessage = pymsteams.connectorcard(TEAMS_CONNECTCARD_WEBHOOK_URL)

  # TRACEBACK: Get current system exception
  ex_type, ex_value, ex_traceback = sys.exc_info()
  if ex_type is not None:
    # TRACEBACK: Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)
    
    # MSTEAMS: Add text to the CARD and summary to the NOTIFICATION
    myTeamsMessage.title("%s: %s" % (title, ex_type.__name__))
    myTeamsMessage.summary("%s: %s" % (title, ex_type.__name__))

    # create the section and add it to the connector card object
    myMessageSection = pymsteams.cardsection()
    myMessageSection.title(str(ex_value))
    myTeamsMessage.addSection(myMessageSection)

    # TRACEBACK: Format stacktrace
    for trace in trace_back:
      # create the section and add it to the connector card object
      myMessageSection = pymsteams.cardsection()
      myMessageSection.title("Traceback (most recent call last):")
      myMessageSection.addFact("File", trace[0])
      myMessageSection.addFact("Line", trace[1])
      myMessageSection.addFact("Func.Name", trace[2])
      myMessageSection.text(trace[3])
      myTeamsMessage.addSection(myMessageSection)
  
  else: # If traceback is None
    # MSTEAMS: Add text to the CARD and summary to the NOTIFICATION
    myTeamsMessage.title("%s" % title)
  
  # MSTEAMS: Add text to the CARD
  if message is not None: 
    myTeamsMessage.text(message)
    myTeamsMessage.summary("%s: %s" % (title, message))
    # print("%s: %s" % (title, message))
  else:
    myTeamsMessage.summary("%s" % title)
    # print("%s" % title)

  # send the message.
  myTeamsMessage.send()