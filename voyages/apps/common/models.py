from django.db import models

# Create your models here.
class SavedQuery(models.Model):
    """
    Used to store a query for later use in a permanent link.
    """

    ID_LENGTH = 8

    # This is the short sequence of characters that will be used when repeating the query.
    id = models.CharField(max_length=ID_LENGTH, primary_key=True)
    # The actual query string.
    query = models.TextField(unique=True)

    def get_post(self):
        """
        Parse the stored query string and return a dict which is compatible
        with the original post that generated the permalink.
        :return: dict with stored POST data.
        """
        from urlparse import parse_qsl
        return {name: value for name, value in parse_qsl(self.query, keep_blank_values=True)}

    def save(self, *args, **kwargs):
        pre_existing = list(SavedQuery.objects.filter(query=self.query))
        if len(pre_existing) > 0:
            self.id = pre_existing[0].id
        else:
            import random
            import string
            self.id = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
                range(self.ID_LENGTH))
            super(SavedQuery, self).save(*args, **kwargs)
