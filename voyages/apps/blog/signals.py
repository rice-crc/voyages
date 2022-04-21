from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, PostTranslation

from django.utils.text import slugify

import logging

#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/voyages.apps.blog/google_auth.json"

logging.info("signals.py")

@receiver(post_save,sender = Post)
def post_created(sender, instance, created, **kwargs):
    logging.info("POST_CREATED_HANDLER")
    if created:
        logging.info("POST CREATED:")
        logging.info(instance.title)

        for lang_code, lang_name in settings.LANGUAGES:
            logging.info(lang_code)
            if lang_code != settings.LANGUAGES[settings.DEFAULT_LANGUAGE][0]:
                logging.info("CREATING for language:")
                logging.info(lang_code)

                translatedTitle = translate_text(lang_code,instance.title)

                translatedSubTitle = translate_text(lang_code, instance.title)

                translatedContent = translate_text(lang_code, instance.content)

                translationRecord = PostTranslation(post= instance,title = translatedTitle, subtitle = translatedSubTitle,   slug=slugify(translatedTitle), content = translatedContent,  created_on = instance.created_on, updated_on = instance.updated_on, thumbnail = instance.thumbnail, language = lang_code)
                translationRecord.save()
    

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client.from_service_account_json(
        r'google_auth.json')

    #translate_client = translate.Client()


    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    

    
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    #result = translate_client.translate(text, target_language=target)
    result = translate_client.translate(text, target_language=target)

    #print(u"Text: {}".format(result["input"]))
    #print(u"Translation: {}".format(result["translatedText"]))
    #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result["translatedText"]
