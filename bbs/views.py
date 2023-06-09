from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Topic, Category, Reply, Tag
from .forms import TopicForm, TopicCategoryForm, TopicTagForm, ContactsForm, ReplyForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        
        query = Q()
        # name='search'に記録されたデータを取り出す
        if 'search' in request.GET:
            # スペース区切りのキーワード検索に対応させる
            words = request.GET['search'].replace(' ', '　').replace('、', '　').replace(',', '　').split('　')
            for word in words:
                # 空文字の場合は条件に加えない
                if word == '':
                    continue
                query &= Q(comment__icontains=word)
        
        # カテゴリ検索：指定されたカテゴリが存在するか調べる
        form = TopicCategoryForm(request.GET)
        if form.is_valid():
            cleaned = form.clean()  # fieldsで指定したフィールドを全て型変換{'category': Categoryのオブジェクト}
            if cleaned['category']:  # if文がないとカテゴリ未指定のデータだけ出てくる
                query &= Q(category=cleaned['category'])
        
        # order_by()で並び替えをしないと、pagenatorでWARNINGが出る
        topics = Topic.objects.filter(query).order_by('-created_at')
        
        # タグ検索
        form = TopicTagForm(request.GET)
        if form.is_valid():
            cleaned = form.clean()
            # Tagのオブジェクトのリスト
            selected_tags = cleaned['tag']
            for tag in selected_tags:
                # 指定したタグがトピックに含まれているかチェックし、含まれていれば追加
                # topics = [topic for topic in topics if tag in topic.tag.all()]
                # ↑と↓は同じこと
                new_topics = []
                for topic in topics:
                    if tag in topic.tag.all():
                        new_topics.append(topic)
                topics = new_topics
        
        paginator = Paginator(topics, 2)
        if 'page' in request.GET:
            topics = paginator.get_page(request.GET['page'])
        else:
            topics = paginator.get_page(1)
        
        categories = Category.objects.all()
        tags = Tag.objects.all()
        form = TopicForm
        context = {'topics': topics, 'categories': categories, 'tags': tags, 'form': form}
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
        tags = Tag.objects.all()
        form = TopicForm(instance=topic)
        context = {'topic': topic, 'categories': categories, 'tags':tags, 'form': form}
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