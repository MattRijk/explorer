from django.contrib import admin
from pins.models import Category, Pin


admin.site.register(Category)


# title = models.CharField(max_length=500)  # abbreviated note
# image = models.ImageField(upload_to='images/')
# slug = models.SlugField(max_length=1000, blank=True, unique=False)
# note = models.TextField(max_length=500, blank=False)
# source = models.URLField()
# published = models.DateTimeField(default=timezone.now)
# category = models.ForeignKey(Category)
# tags = TaggableManager()

class PinModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'slug', 'note', 'source', 'published','category','tag_list']

    def get_queryset(self, request):
        return super(PinModelAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Pin, PinModelAdmin)