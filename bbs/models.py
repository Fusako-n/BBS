from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリ名', max_length=20)
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(verbose_name='コメント', max_length=200)
    name = models.CharField(verbose_name="名前", max_length=20, default="匿名")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def reply_amount(self):
        return Reply.objects.filter(target=self.id).count()
    
    def __str__(self):
        return self.comment


class Reply(models.Model):
    target = models.ForeignKey(Topic, verbose_name='リプライ対象のトピック', on_delete=models.CASCADE)
    comment = models.CharField(verbose_name='コメント', max_length=200)
    
    def __str__(self):
        return self.comment
