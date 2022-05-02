from django.db import migrations, models

from django.utils.text import slugify

def add_news_tag (apps, scheme_editor):
    tagName = "News"
    Tag = apps.get_model("blog","Tag")

    obj = Tag(name=tagName,slug=slugify(tagName))
    obj.save()
    


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_generic_author_records'),
    ]

    operations = [
        migrations.RunPython(add_news_tag),
    ]

