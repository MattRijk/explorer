from django.db import models

import os
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from Explorer.settings import MEDIA_URL


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Category, self).save(*args, **kwargs)
        else:
            super(Category, self).save(*args, **kwargs)


class Pin(models.Model):
    image = models.ImageField(upload_to="uploads/") # /home/matt/Documents/pinmezz/static/media/uploads
    uuid = models.CharField(max_length=10, unique=True, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    note = models.TextField(max_length=500)
    published = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.uuid

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(self.image).strip(MEDIA_URL).strip('.jpg')
            super(Pin, self).save(*args, **kwargs)
        else:
            super(Pin, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(str(self.uuid))
            super(Pin, self).save(*args, **kwargs)
        else:
            super(Pin, self).save(*args, **kwargs)




