from django.db import models

from django.contrib.auth.models import User

from filebrowser.fields import FileBrowseField


STATUS = (
    (0,"Draft"),
    (1,"Publish")
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
    title = models.CharField(max_length=200, unique=True)
    subtitle = models.CharField(max_length=200, null = True, blank = True)
    slug = models.SlugField(max_length=200, unique=True)
    #author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    authors = models.ManyToManyField(Author)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    tags = models.ManyToManyField(Tag)
    #thumbnail = models.ImageField(upload_to='images',null=True, blank=True)
    thumbnail = FileBrowseField("Thumbnail", max_length=300, directory="blog/", extensions=[".jpg",".png",".wep", ".gif"], null=True,  blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title



