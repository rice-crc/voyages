# Create your models here.
from django.db import models
from django.utils.translation import ugettext as _

# Left menu item
class LessonPlan(models.Model):
    text = models.CharField(('Title'),max_length=100)
    author = models.CharField(('Author'),max_length=50)
    grade_level = models.CharField(('Grade Level'),max_length=50)
    course = models.CharField(('Course'),max_length=50)
    key_words = models.CharField(('Key Words'),max_length=200)
    
    abstract = models.CharField(('Abstract'),max_length=500)
    
    order = models.IntegerField()
    
    def __unicode__(self):
       return self.text
    
class LessonStandard(models.Model):
    type = models.CharField(('Standard Type'),max_length=100)
    text = models.CharField(('Text'),max_length=100)
    lesson = models.ForeignKey(LessonPlan)