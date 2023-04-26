from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib import messages
# from django.urls import reverse_lazy

from .models import Topic, Category, Reply
from .forms import TopicForm, ContactsForm, ReplyForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        topics = Topic.objects.order_by('-created_at')
        categories = Category.objects.all()
        context = {'topics': topics, 'categories': categories}
        return render(request, 'bbs/index.html', context)
    
    def post(self, request, *args, **kwargs):
        form = TopicForm(request.POST)
        if not form.is_valid():
            values = form.errors.get_json_data().values()
            for value in values:
                for v in value:
                    messages.error(request, v['message'])
            return redirect('bbs:index')
        form.save()
        messages.info(request, '投稿内容を保存しました！')
        return redirect('bbs:index')

index = IndexView.as_view()


class ContactsView(View):
    def get(self, request, *args, **kwargs):
        form = ContactsForm
        return render(request, 'bbs/contacts.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ContactsForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('バリデーションNG')
        return redirect('bbs:contacts')

contacts = ContactsView.as_view()


class ReplyView(View):
    def get(self, request, pk, *args, **kwargs):
        topic = Topic.objects.filter(id=pk).first()
        replies = Reply.objects.filter(target=pk)
        context = {'topic': topic, 'replies': replies}
        return render(request, 'bbs/reply.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        copied = request.POST.copy()
        copied['target'] = pk
        form = ReplyForm(copied)
        if form.is_valid():
            form.save()
        else:
            print('バリデーションNG')
        return redirect('bbs:reply', pk)

reply = ReplyView.as_view()


class TopicDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        topic = Topic.objects.filter(id=pk).first()
        if topic:
            topic.delete()
        else:
            print('対象のデータは見つかりませんでした')
        return redirect('bbs:index')

topic_delete = TopicDeleteView.as_view()


class TopicEditView(View):
    def get(self, request, pk, *args, **kwargs):
        topic = Topic.objects.filter(id=pk).first()
        categories = Category.objects.all()
        context = {'topic': topic, 'categories': categories}
        return render(request, 'bbs/topic_edit.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        topic = Topic.objects.filter(id=pk).first()
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.info(request, '投稿内容を変更しました！')
        else:
            messages.info(request, 'バリデーションNG')
        return redirect('bbs:index')

topic_edit = TopicEditView.as_view()