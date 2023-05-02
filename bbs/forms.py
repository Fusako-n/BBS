from django import forms
from django_summernote.widgets import SummernoteWidget
from django.conf import settings
import bleach
from .models import Topic, Reply, Contacts


class HTMLField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(HTMLField, self).__init__(*args, **kwargs)
        self.widget = SummernoteWidget()

    def to_python(self, value):
        value       = super(HTMLField, self).to_python(value)
        return bleach.clean(value, tags=settings.ALLOWED_TAGS, attributes=settings.ATTRIBUTES)


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'comment', 'category']
        error_messages = {
            'name': {
                'max_length': 'お名前は20文字以内で入力して下さい',
                'required': 'お名前を入力して下さい',
            },
            'comment': {
                'required': 'コメントを入力して下さい',
            },
        }
    comment = HTMLField()


class TopicCategoryForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['category']


class TopicAdminForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'comment', 'category']
    comment = forms.CharField(widget=forms.Textarea(attrs={'maxlength':str(Topic.comment.field.max_length),}), label=Topic.comment.field.verbose_name)


class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['name', 'email', 'content']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['target', 'comment']