from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # null=True means that user can be an empty field, and if user submits a form, blank=True is possible.
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    # order query set
    class Meta:
        ordering = ['complete']
        User._meta.get_field('email')._unique = True