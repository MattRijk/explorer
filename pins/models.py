from django.db import models

import os

import uuid
import os


from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from Explorer.settings import MEDIA_ROOT




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


def get_file_path(instance, filename):
    jpg = filename.split('.')[-1]
    filename = "%s.%s" % (filename, jpg)
    return os.path.join('uploads/', filename)


class Pin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='uploads/')
    slug = models.SlugField(max_length=200, blank=True, unique=False)
    note = models.TextField(max_length=500, blank=False)
    published = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            # self.slug = slugify(self.image).strip(MEDIA_ROOT+'uploads/')
            self.slug = slugify(self.id)
            super(Pin, self).save(*args, **kwargs)
        else:
            super(Pin, self).save(*args, **kwargs)






    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         slug = str(self.image).strip('home/matt/Documents/Explorer/media/').strip('.jpg')
    #         self.slug = slugify(str(slug))
    #         super(Pin, self).save(*args, **kwargs)
    #     else:
    #         super(Pin, self).save(*args, **kwargs)




