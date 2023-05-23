from django.contrib import admin
from .models import Topic, Category, Contacts, Tag
from .forms import TopicAdminForm
from django.utils.html import format_html


class TopicAdmin(admin.ModelAdmin):
    # タグは複数あるのでlist_displayにM2Mのfieldは指定できない→下記のdef関数で対応
    list_display = ['id', 'comment', 'name', 'created_at', 'format_tag']
    list_filter = ['name']
    form = TopicAdminForm
    
    def format_tag(self, obj):  # objはTopicのオブジェクト（1obj=トピック1件）
        tag_str = ''
        if obj.tag:
            for tag in obj.tag.all():
                tag_str += tag.name + ','  # tag1,tag2,tag3のようになる
            return format_html('<div>{}</div>', tag_str)


admin.site.register(Topic, TopicAdmin)
admin.site.register(Category)
admin.site.register(Contacts)
admin.site.register(Tag)