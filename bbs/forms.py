from django import forms
from .models import Topic, Reply


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
                'max_length': 'コメントの文字数が' + str(Topic.comment.field.max_length) + '文字を超えています。',
                'required': 'コメントを入力して下さい',
            },
        }


class TopicAdminForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'comment']
    comment = forms.CharField(widget=forms.Textarea(attrs={'maxlength':str(Topic.comment.field.max_length),}), label=Topic.comment.field.verbose_name)


class ContactsForm(forms.Form):
    name = forms.CharField(max_length=20, label='お名前')
    email = forms.EmailField(label='メールアドレス')
    content = forms.CharField(label='お問い合わせ内容', widget=forms.Textarea)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['target', 'comment']