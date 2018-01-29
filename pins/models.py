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
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    note = models.TextField(max_length=500)
    published = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = str(self.image).strip('home/matt/Documents/Explorer/media/').strip('.jpg')
            self.slug = slugify(str(slug))
            super(Pin, self).save(*args, **kwargs)
        else:
            super(Pin, self).save(*args, **kwargs)




