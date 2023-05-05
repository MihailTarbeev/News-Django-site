from django import template

from news.models import Category
from django.db.models import Count, F
from django.core.cache import cache


register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello', arg2='world'):
    # Попробуем достать из кэша категории
    # categories = cache.get('categories')
    # Проверяем, достали ли мы из кэша категории
    # if not categories:
    #     # С помощью filter=F('news__is_published') выберем те записи, у которых is_published=True
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    #     # При запросе категорий сохраняем их в кэш на 30 секунд
    #     cache.set('categories', categories, 30)
    return {'categories': categories, 'arg1': arg1, 'arg2': arg2}

