from django.db import migrations, models

from django.utils.text import slugify

def add_generic_author (apps, scheme_editor):


    institutionName = "Voyages Team"
    Institution = apps.get_model("blog","Institution")

    institution = Institution(name=institutionName,slug=slugify(institutionName))
    institution.save()


    authorName = "Voyages Team"
    Author = apps.get_model("blog","Author")
        
    author = Author(name=authorName,slug=slugify(authorName),institution=institution, role="Team Member")
    author.save()
   



class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_tags_initial_data'),
    ]

    operations = [
        migrations.RunPython(add_generic_author),
    ]

