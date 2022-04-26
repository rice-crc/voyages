from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, PUBLISH_STATUS

from django.utils.text import slugify



from django.db import transaction

#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/voyages.apps.blog/google_auth.json"



SOURCE_LANGUAGE = "en"

def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


@receiver(post_save, sender=Post)
@on_transaction_commit
def post_saved(sender, instance, **kwargs):
    
    if instance.status == PUBLISH_STATUS and instance.language == SOURCE_LANGUAGE:
        
        for lang_code, _ in settings.LANGUAGES:
            if lang_code != SOURCE_LANGUAGE:
                # First check if the target language already has a translation.
                count = Post.objects.filter(slug=instance.slug, language=lang_code).count()
                if count > 0:
                    continue
                

                clone = Post.objects.get(pk=instance.pk)

                authors = clone.authors.all()
                tags = clone.tags.all()

                clone.pk = None
                clone.title = translate_text(lang_code, instance.title)
                clone.subtitle = translate_text(lang_code, instance.subtitle)
                clone.content = translate_text(lang_code, instance.content)
                clone.language = lang_code

                clone.save()                
                
                clone.authors.set(authors)
                clone.tags.set(tags)



                
    

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
