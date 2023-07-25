from django.contrib import admin

# Register your models here.
from .models import SportsCard, Tag, TagCard

admin.site.register(SportsCard)
admin.site.register(Tag)
admin.site.register(TagCard)