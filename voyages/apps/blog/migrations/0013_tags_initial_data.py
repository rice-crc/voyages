from django.db import migrations, models

from django.utils.text import slugify

def initialize_tags (apps, scheme_editor):
    tags = ["Author Profile","Institution Profile"]
    Tag = apps.get_model("blog","Tag")

    for tag in tags:
        obj = Tag(name=tag,slug=slugify(tag))
        obj.save()



class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20220420_2159'),
    ]

    operations = [
        migrations.RunPython(initialize_tags),
    ]

