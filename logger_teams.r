tryCatch(library(teamr),
         error=function(e){
           install.packages('teamr')
           library(teamr)
         }
)

script.dir <- dirname(sys.frame(1)$ofile) ### work in source()
# script.dir <- getwd() ### not work when direct commanding in rstudio
readRenviron(file.path(script.dir, '.env'))
TEAMS_CONNECTCARD_WEBHOOK_URL <- Sys.getenv('TEAMS_CONNECTCARD_WEBHOOK_URL_R')

logger_teams <- function(title, message='', ..., FUN){
  "
  Args:
      title ([String]): text to be added on card's title
      message ([String], optional): any message as a card's text. Defaults to None. 
      FUN ([function], optional): funtion to try
  "
  library(teamr)
  
  # MSTEAMS: Create the CONNECTORCARD object with the Microsoft Webhook URL
  myTeamsMessage <- connector_card$new(hookurl=TEAMS_CONNECTCARD_WEBHOOK_URL)

  # MSTEAMS: Add text to the CARD and summary to the NOTIFICATION
  myTeamsMessage$title(title)
  # MSTEAMS: Add text to the CARD
  myTeamsMessage$text(message)
  # MSTEAMS: Add summary to the NOTIFICATION
  myTeamsMessage$summary(paste(title, ': ', message))
  
  # TRYCATCH
  if(!missing(FUN)){
    myMessageSection <- card_section$new()
    tryCatch(FUN(),
      warning = function(w) {
        myMessageSection$title(sec_title=as.character(w))
        # ls_message <- c(ls_message, sprintf("\u2757\uFE0F %s", as.character(w)))
      },
      error = function(e) {
        myMessageSection$title(sec_title=as.character(e))
        # ls_message <- c(ls_message, sprintf("\u2757\uFE0F %s", as.character(e)))
      }
    )
    myTeamsMessage$add_section(new_section=myMessageSection)
  }
  myTeamsMessage$send()
}