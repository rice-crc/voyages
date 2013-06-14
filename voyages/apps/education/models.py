# Create your models here.
from django.db import models
from django.utils.translation import ugettext as _

class LessonPlan(models.Model):
    """
    A single lesson plan written by some authors, containing abstract,
     grade-level, title (known as text attribute), course level, keywords and etc

    """
    text = models.CharField(_('Title'),max_length=100)
    author = models.CharField(_('Author'),max_length=50)
    grade_level = models.CharField(_('Grade Level'),max_length=50)
    course = models.CharField(_('Course'),max_length=50)
    key_words = models.CharField(_('Key Words'),max_length=200)
    
    abstract = models.TextField(_('Abstract'),max_length=1000)
    
    order = models.IntegerField()
    
    class Meta:
        ordering = ['order']
    
    def __unicode__(self):
       return self.text

class LessonStandardType(models.Model):
    """
    A type of lesson standards (such as NCHS or NCSS standards)
    related to :model:`voyages.apps.education.LessonStandard`

    """
    type = models.CharField(_('Standard Type'),max_length=100)
    def __unicode__(self):
       return self.type

class LessonStandard(models.Model):
    """
    An actual standard or group of standards of a lesson plan
      belonging to the same lesson standard type
    related to :model:`voyages.apps.education.LessonStandardType`
    related to :model:`voyages.apps.education.LessonPlan`
    """
    type = models.ForeignKey(LessonStandardType)
    text = models.CharField(_('Text'),max_length=100)
    lesson = models.ForeignKey(LessonPlan)
    
    def __unicode__(self):
       return self.text

class LessonPlanFile(models.Model):
    """
    An attached file (presentation or pdf) to a lesson plan
    related to :model:`voyages.apps.education.LessonStandard`
    """
    file = models.FileField(upload_to='lessonplan')
    filetitle = models.CharField(('File name'),max_length=50)
    lesson = models.ForeignKey(LessonPlan)
    
    def __unicode__(self):
       return self.filetitle