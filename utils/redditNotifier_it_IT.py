SKILL_NAME = "Reddit Notifica"
HELP_TEXT = (" Dimmi i subreddit che vorresti seguire per nuovi post. Puoi dire: Controlla italy per nuovi post. \n "
                "Se vuoi sapere se ci sono nuovi post su un tuo subreddit, mi puoi chiedere: Ci sono nuovi post su italy? \n "
                "Mi puoi chiedere se ci sono nuovi post sui tuoi subreddit, dicendo: Ci sono nuovi post? \n "
                "Se desideri rimuovere un subreddit dalla tua lista, mi puoi dire: Rimuovi italy dalla mia lista. \n "
                "Se vuoi sapere quali subreddit stai monitorando, mi puoi dire: Quali sono i miei subreddit? \n "
                "Se desideri controllare i titoli dei post più recenti su un subreddit, ti basta dire: Dimmi i post più recenti su italy. ")
WELCOME_TEXT = "Benvenuto alla skill Reddit Notifica. Per qualsiasi informazione su come utilizzare la skill, ti basta dire: Aiutami, oppure, Guidami. "
WELCOME_REPROMPT_TEXT = "Puoi aggiungere, monitorare e cancellare i tuoi subreddit preferiti. Puoi anche controllare i post più recenti su qualsiasi subreddit. "
GOODBYE_TEXT = "Grazie per aver utilizzato Reddit Notifica. Arrivederci!"

SUBREDDITS_LIST_INITIAL_INTENT_TEXT = "I subreddit che stai attualmente controllando sono: \n"

SUBREDDITS_MONITORING_INTENT_NO_SUBREDDITS_TEXT = ("Attualmente non stai monitorando nessun subreddit. Se desideri monitorare un subreddit, puoi dirmi: "
                "Controlla italy per nuovi post. ")
SUBREDDITS_MONITORING_INTENT_REPROMPT_TEXT = "Mi puoi chiedere se ci sono nuovi post sui tuoi subreddit, dicendo: Ci sono nuovi post? "
SUBREDDITS_MONITORING_INTENT_NO_CHANGES_TEXT = "Non ci sono nuovi post suoi tuoi subreddit. "
SUBREDDITS_MONITORING_INTENT_INITIAL_CHANGES_TEXT = "I subreddit dove nuovi post sono stati pubblicati sono: \n"
SUBREDDITS_MONITORING_INTENT_CHANGES_TEXT = "Da adesso in poi controllerò la loro versione aggiornata."

SINGLE_SUBREDDIT_MONITORING_INTENT_CHANGE_TEXT = "Ci sono nuovi post su r {}! Da adesso in poi controllerò la versione aggiornata del subreddit. "
SINGLE_SUBREDDIT_MONITORING_INTENT_NO_CHANGE_TEXT = "Non ci sono nuovi post su r {}. "
SINGLE_SUBREDDIT_MONITORING_INTENT_UNKNOWN_SUBREDDIT_TEXT = "Non ho ben capito il subreddit da controllare. "
SINGLE_SUBREDDIT_MONITORING_INTENT_REPROMPT_TEXT = "Mi puoi chiedere se ci sono nuovi post su un subreddit, dicendo: Ci sono nuovi posto su italy? "

SUBREDDIT_INSERTION_INTENT_SUCCESS_REPROMPT_TEXT  = "Mi puoi chiedere se ci sono nuovi post sul tuo subreddit, dicendo: Ci sono nuovi post su {}? "
SUBREDDIT_INSERTION_INTENT_SUCCESS_TEXT = "Ora so che desideri controllare  r {} per nuovi post. "
SUBREDDIT_INSERTION_INTENT_UNKNOWN_SUBREDDIT_TEXT = "Non ho ben capito il subreddit da controllare. "
SUBREDDIT_INSERTION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT = "Mi puoi dire un subreddit che desideri monitorare, dicendo: Controlla italy per nuovi post. "

SINGLE_SUBREDDIT_DELETION_INTENT_SUCCESS_TEXT = "Ho rimosso r {} dalla lista dei tuoi subreddit. "
SINGLE_SUBREDDIT_DELETION_INTENT_SUCCESS_REPROMPT_TEXT = "Mi puoi chiedere di monitorare altri subreddit, dicendo: Controlla italy per nuovi post. "
SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_TEXT = "Questo subreddit non fa parte della tua lista di subreddit. "
SINGLE_SUBREDDIT_DELETION_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT = "Mi puoi dire il subreddit che vuoi rimuovere dalla tua lista, dicendo: Rimuovi italy dalla mia lista. "

SUBREDDITS_DELETION_INTENT_TEXT = "La tua lista di subreddit ora è vuota. "
SUBREDDITS_DELETION_INTENT_ADD_SUBREDDITS_TEXT = "Puoi aggiungere subreddit alla tua lista, dicendo: Controlla italy per nuovi post. "

SINGLE_SUBREDDIT_LAST_POSTS_INTENT_SUCCESS_REPROMPT_TEXT = "Mi puoi chiedere i post più recenti per il subreddit scelto, dicendo: Dimmi i post più recenti su {}. "
SINGLE_SUBREDDIT_LAST_POSTS_INSERTION_INTENT_SUCCESS_TEXT = "I titoli dei post più recenti su r {} sono: \n"
SINGLE_SUBREDDIT_LAST_POSTS_INTENT_UNKNOWN_SUBREDDIT_TEXT = "Non ho ben capito di quale subreddit vuoi i post più recenti. "
SINGLE_SUBREDDIT_LAST_POSTS_INTENT_UNKOWN_SUBREDDIT_REPROMPT_TEXT = "Mi puoi chiedere i post più recenti su un subreddit, dicendo: Dimmi i post più recenti su italy. "

EXCEPTION_SUBREDDIT_TEXT = "Purtroppo non ho capito il subreddit che vuoi monitorare. "
EXCEPTION_UNKNOWN_SUBREDDIT_TEXT = "Questo subreddit non fa parte della tua lista di subreddit. Prova ad aggiungerlo, dicendo: Controlla italy per nuovi post. "
EXCEPTION_GENERIC_TEXT = "Ho incontrato un problema. Prova ancora!"
EXCEPTION_REPROMPT_TEXT = "Per qualsiasi informazione su come utilizzare la skill, ti basta dire: Aiutami, oppure, Guidami. "