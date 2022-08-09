import logging
import logger_telegram
import logger_teams

class logger:
  def __init__(self, title, *, telegram_chat_id=None, type=['console', 'telegram', 'teams']):
    self.__title = title
    self.__telegram_chat_id = telegram_chat_id
    self.__type = type
    self.__console_logger = logging.getLogger(title)
    self.__console_logger.setLevel(logging.INFO)

  def info(self, message, *, type=None):
    self.__message = message

    if type is not None:
      self.__type = type

    if 'console' in self.__type: 
      self.__console_logger.info(message)
      print(message)
    
    if 'telegram' in self.__type:
      try:
        logger_telegram.logger_telegram(self.__title, self.__message, chat_id=self.__telegram_chat_id)
      except:
        pass
    
    if 'teams' in self.__type:
      try:
        logger_teams.logger_teams(self.__title, self.__message)
      except:
        pass
  
  def get_telegram_recent_chat_id(self, verbose=False):
    logger_telegram.get_recent_chat_id(verbose=verbose)

  @property
  def title(self):
    return self.__title
  
  @property
  def telegram_chat_id(self):
    return self.__telegram_chat_id
  
  @property
  def type(self):
    return self.__type
  
  @title.setter
  def title(self, title):
    self.__title = title
  
  @telegram_chat_id.setter
  def telegram_chat_id(self, telegram_chat_id):
    self.__telegram_chat_id = telegram_chat_id

  @type.setter
  def type(self, type):
    self.__type = type