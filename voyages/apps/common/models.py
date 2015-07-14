from django.db import models

# Create your models here.
class SavedQuery(models.Model):
    """
    Used to store a query for later use in a permanent link.
    """

    ID_LENGTH = 8

    # This is the short sequence of characters that will be used when repeating the query.
    id = models.CharField(max_length=ID_LENGTH, primary_key=True)
    # A hash string so that the query can be quickly located.
    hash = models.CharField(max_length=255, db_index=True, default='')
    # The actual query string.
    query = models.TextField()

    def get_post(self):
        """
        Parse the stored query string and return a dict which is compatible
        with the original post that generated the permalink.
        :return: dict with stored POST data.
        """
        from urlparse import parse_qsl
        return {name: value for name, value in parse_qsl(self.query, keep_blank_values=True)}

    def save(self, *args, **kwargs):
        import hashlib
        hash_object = hashlib.sha1(self.query)
        self.hash = hash_object.hexdigest()
        pre_existing = list(SavedQuery.objects.filter(hash=self.hash).filter(query=self.query))
        if len(pre_existing) > 0:
            self.id = pre_existing[0].id
        else:
            import random
            import string
            self.id = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
                range(self.ID_LENGTH))
            super(SavedQuery, self).save(*args, **kwargs)
