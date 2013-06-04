from django.db import models

# Glossary entry for

class Glossary(models.Model):
    term = models.CharField(('Term'),max_length=50)
    description = models.TextField(('Description'), max_length=1000)

    class Meta:
        ordering = ['term']
        verbose_name_plural = "Glossary Items"

    def __unicode__(self):
        return self.term

class FaqCategory(models.Model):
    text = models.CharField(('Question Category'), max_length=100)
    type_order = models.IntegerField()
    
    class Meta:
        ordering = ['type_order']
        verbose_name_plural = 'Faq categories'
    
    def __unicode__(self):
        return self.text

class Faq(models.Model):
    question = models.TextField(('Question'), max_length=300)
    answer = models.TextField(('Answer'), max_length=2000)
    category = models.ForeignKey(FaqCategory)
    question_order = models.IntegerField()
    
    class Meta:
        ordering = ['question_order']
