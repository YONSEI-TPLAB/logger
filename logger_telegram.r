tryCatch(library(telegram.bot),
         error=function(e){
           install.packages('telegram.bot')
           library(telegram.bot)
         }
)

script.dir <- dirname(sys.frame(1)$ofile) ### work in source()
# script.dir <- getwd() ### not work when direct commanding in rstudio
readRenviron(file.path(script.dir, '.env'))
TELEGRAM_BOT_TOKEN <- Sys.getenv('TELEGRAM_BOT_TOKEN_R')
TELEGRAM_CHAT_ID <- Sys.getenv('TELEGRAM_CHAT_ID')

get_recent_chat_id <- function(verbose=FALSE){
  library(telegram.bot)
  
  # TELEGRAM: CONNECT with Telegram Bot
  bot <- Bot(TELEGRAM_BOT_TOKEN)
  
  # Get Chat ID
  updates <- bot$getUpdates()

  if(length(updates) > 0){
    if(verbose) print(paste0('Chat ID is set as ', updates[[1L]]$from_chat_id(), ', whose first name is ', updates[[1L]]$effective_user()$first_name))
    return(updates[[1L]]$from_chat_id())
  } else {
    stop('Chat ID not found, please send any message to bot to get your chat ID')
  }
}


logger_telegram <- function(title, message='', ..., FUN, chat_id, verbose=FALSE){
  "
  Args:
      title ([String]): text to be added on card's title
      message ([String], optional): any message as a card's text. Defaults to None. 
      FUN ([function], optional): funtion to try
  "
  library(telegram.bot)

  # TELEGRAM: CONNECT with Telegram Bot
  bot = Bot(TELEGRAM_BOT_TOKEN)
  
  if(missing(chat_id)){
    if(!exists(TELEGRAM_CHAT_ID)){
      chat_id <- TELEGRAM_CHAT_ID
    } else {
      tryCatch(
        chat_id <- get_recent_chat_id(verbose=verbose),
        error = function(e) {
          stop('Chat ID not found, please send any message to bot to get your chat ID')
        }
      )
    }      
  }

  ls_message = c()
  
  ls_message <- c(ls_message, sprintf("\U0001F1F5 %s", title))
  if(!missing(message)){ls_message <- c(ls_message, message)}
  ls_message <- c(ls_message, "\n")

  # TRYCATCH
  if(!missing(FUN)){
    tryCatch(FUN(),
      warning = function(w) {
        ls_message <- c(ls_message, sprintf("\u2757\uFE0F %s", as.character(w)))
        bot$sendMessage(chat_id, text=paste(ls_message, collapse="\n"))
      },
      error = function(e) {
        ls_message <- c(ls_message, sprintf("\u2757\uFE0F %s", as.character(e)))
        bot$sendMessage(chat_id, text=paste(ls_message, collapse="\n"))
      }
    )
  } else {
    bot$sendMessage(chat_id, text=paste(ls_message, collapse="\n"))
  }
}
