from django.contrib import admin

# Register your models here.
from .models import Document,Subject,Section
admin.site.register(Document)
admin.site.register(Subject)
admin.site.register(Section)