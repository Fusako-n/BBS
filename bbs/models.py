from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリ名', max_length=20)
    
    def __str__(self):
        return self.name
        
    # idを文字列型に変えるモデルメソッド
    def str_id(self):
        return str(self.id)
    
    # トピック数を数えるモデルメソッド
    def topic_amount(self):
        return Topic.objects.filter(category=self.id).count()
    
    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(verbose_name='タグ名', max_length=20)
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.CASCADE, null=True, blank=True)
    # 投稿時にタグを指定しなくてもOKならblank=True、指定が必須ならFalse
    # forms.pyのTopicAdminFormのfieldsにもtagを追加する
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    comment = models.TextField(verbose_name='コメント')
    name = models.CharField(verbose_name="名前", max_length=20, default="匿名")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # リプライ数を数えるモデルメソッド
    def reply_amount(self):
        return Reply.objects.filter(target=self.id).count()
    
    def __str__(self):
        return self.comment


class Reply(models.Model):
    target = models.ForeignKey(Topic, verbose_name='リプライ対象のトピック', on_delete=models.CASCADE)
    comment = models.CharField(verbose_name='コメント', max_length=200)
    
    def __str__(self):
        return self.comment
    
    class Meta:
        verbose_name_plural = 'Replies'


class Contacts(models.Model):
    name = models.CharField(verbose_name='お名前', max_length=20)
    email = models.EmailField(verbose_name='メールアドレス', max_length=50)
    content = models.TextField(verbose_name='お問い合わせ内容')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Contacts'