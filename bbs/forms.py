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
        fields = ['name', 'comment', 'category', 'tag']
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


class TopicTagForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['tag']


class TopicAdminForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'comment', 'category', 'tag']
    # comment = forms.CharField(widget=forms.Textarea(attrs={'maxlength':str(Topic.comment.field.max_length),}), label=Topic.comment.field.verbose_name)
    comment = HTMLField()  # admin画面でsummernoteを表示させる方法


class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['name', 'email', 'content']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['target', 'comment']