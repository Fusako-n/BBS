from django import template
register = template.Library()


@register.simple_tag()
def url_replace(request, key, value):
    # 引数①リクエストオブジェクト②クエリストリングで書き換えたいキー③キーに対応する値
    copied = request.GET.copy()
    copied[key] = value
    return copied.urlencode()