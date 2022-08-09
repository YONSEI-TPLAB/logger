if(!exists('logger_telegram', mode='function')) source('logger_telegram.r')
if(!exists('logger_teams', mode='function')) source('logger_teams.r')

### PREDEFINE common arguments
logger.title <- 'TPLAB'
logger.type <- c('console', 'telegram', 'teams')

### FUNC logger.info()
logger.info <- function(title=logger.title, message='', ..., FUN, chat_id, verbose=FALSE, type=logger.type){
  if('console' %in% type){
    tryCatch(
      writeLines(message)
    )
  }
  
  if('telegram' %in% type){
    tryCatch(
      logger_telegram(title, message, FUN=FUN, chat_id=chat_id, verbose=verbose)
    )
  }
  
  if('teams' %in% type){
    tryCatch(
      logger_teams(title, message, FUN=FUN)
    )
  }
}
