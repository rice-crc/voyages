from distutils.command.config import LANG_EXT
from django.conf import settings
from django.db import models

from django.contrib.auth.models import User

from filebrowser.fields import FileBrowseField


DRAFT_STATUS = 0
PUBLISH_STATUS = 1

STATUS = (
    (DRAFT_STATUS,"Draft"),
    (PUBLISH_STATUS, "Publish")
)



class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=600,null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='images',null=True, blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=600,null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images',null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete= models.CASCADE)

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, unique=False)
    language = models.CharField(max_length=2, null = True, blank=False, default='en', choices=settings.LANGUAGES)
    subtitle = models.CharField(max_length=200, null = True, blank = True)
    slug = models.SlugField(max_length=200)
    authors = models.ManyToManyField(Author)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    tags = models.ManyToManyField(Tag)
    
    thumbnail = FileBrowseField("Thumbnail", format="Image", max_length=300,directory="images/", extensions=[".jpg",".png",".wep", ".gif"], blank=True)

    class Meta:
        ordering = ['-created_on']
        unique_together = ['slug', 'language']

    def __str__(self):
        return self.title

    def get_snippet(self):

        page_break = self.content.find('<!-- pagebreak -->')
        if page_break != -1:
            return self.content[:page_break]

        return self.content
