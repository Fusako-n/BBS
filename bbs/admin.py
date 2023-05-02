from django.contrib import admin
from .models import Topic, Category, Contacts
from .forms import TopicAdminForm
from django_summernote.admin import SummernoteModelAdmin


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'name', 'created_at']
    list_filter = ['name']
    form = TopicAdminForm


admin.site.register(Topic, TopicAdmin)
admin.site.register(Category)
admin.site.register(Contacts)