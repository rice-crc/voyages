from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, PUBLISH_STATUS

from django.utils.text import slugify

import logging

#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/voyages.apps.blog/google_auth.json"

logging.info("signals.py")

SOURCE_LANGUAGE = "en"

@receiver(post_save, sender=Post)
def post_saved(sender, instance, **kwargs):
    logging.info("POST_SAVED_HANDLER")
    if instance.status == PUBLISH_STATUS and instance.language == SOURCE_LANGUAGE:
        logging.info(f"POST SAVED: {instance.pk}")
        logging.info(instance.title)
        for lang_code, _ in settings.LANGUAGES:
            if lang_code != SOURCE_LANGUAGE:
                # First check if the target language already has a translation.
                count = Post.objects.filter(slug=instance.slug, language=lang_code).count()
                if count > 0:
                    continue
                logging.info("CREATING for language:")
                logging.info(lang_code)
                clone = Post.objects.get(pk=instance.pk)
                clone.pk = None
                clone.title = translate_text(lang_code, instance.title)
                clone.subtitle = translate_text(lang_code, instance.subtitle)
                clone.content = translate_text(lang_code, instance.content)
                clone.language = lang_code
                clone.save()
    

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
