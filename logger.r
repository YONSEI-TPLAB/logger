script.dir <- dirname(sys.frame(1)$ofile) ### work in source()
# script.dir <- getwd() ### not work when direct commanding in rstudio
if(!exists('logger_telegram', mode='function')) source(file.path(script.dir, 'logger_telegram.r'))
if(!exists('logger_teams', mode='function')) source(file.path(script.dir, 'logger_teams.r'))

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
