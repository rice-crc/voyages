from settings import *

# override the signal processor so haystack does not send result to Solr
del(HAYSTACK_SIGNAL_PROCESSOR)
