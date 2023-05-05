from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from .utils import MyMixin
from news.models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginFrom, ContactForm


# Функция отсылает нас на шаблон register.html
def register(request):
    # Проверяем пришли ли данные постом
    if request.method == "POST":
        # Создадим экземпляр класса UserRegisterForm, который мы настроили в forms.py и передадим ему запрос POST
        form = UserRegisterForm(request.POST)
        # Проводим валидацию формы и сохраняем её
        if form.is_valid():
            user = form.save()
            # Авторизуем нашего пользователя
            login(request, user)
            # Обозначим сообщение для успешной регистрации
            messages.success(request, 'Вы успешно зарегистрировались')
            # Перенаправим пользователя на путь 'home'
            return redirect('home')
        else:
            # Обозначим сообщение для провальной регистрации
            messages.error(request, 'Ошибка регистрации')
    # В противном случае создаём несвязанную с данными форму
    else:
        form = UserRegisterForm()
    # Передаём одну из двух форму в контекст
    return render(request, 'news/register.html', {'form': form})


# Функция отсылает нас на шаблон login.html
def user_login(request):
    # Проверяем пришли ли данные постом
    if request.method == 'POST':
        # Создаём экземпляр класса UserLoginForm и связываем его с данными
        # Необходимо передавать именованный аргумент
        form = UserLoginFrom(data=request.POST)
        # Проводим валидацию формы и сохраняем её
        if form.is_valid():
            # Пользователя необходимо получить методом get_user из класса UserLoginFrom
            user = form.get_user()
            # Авторизуем пользователя методом login
            login(request, user)
            # Перенаправляем пользователя на путь 'home'
            return redirect('home')
    else:
        # Создаём несвязанный с данными экземпляр класса UserLoginForm
        form = UserLoginFrom()
    return render(request, 'news/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    # Проверяем пришли ли данные постом
    if request.method == "POST":
        # Создадим экземпляр класса ContactForm
        form = ContactForm(request.POST)
        # Проводим валидацию формы и сохраняем её
        if form.is_valid():
            # Отправим письмо методом send_mail, результат функции 0 или 1
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'tarb4@yandex.ru',
                             ['tarb3@yandex.ru'], fail_silently=True)
            if mail:
                # Обозначим сообщение для успешной отправки
                messages.success(request, 'Письмо отправлено')
                # Перенаправим пользователя на путь 'test'
                return redirect('contact')
            else:
                # Обозначим сообщение для провальной отправки
                messages.error(request, 'Ошибка отправки')
        else:
            # Обозначим сообщение для провальной отправки
            messages.error(request, 'Ошибка валидации')
    else:
        # В противном случае создаём несвязанную с данными форму
        form = ContactForm()
    # Передаём одну из двух форму в контекст
    return render(request, 'news/test.html', {'form': form})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'Hello, Misha!'
    # в paginate_by указываем количество страниц
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    # в paginate_by указываем количество страниц
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True, category_id=self.kwargs['category_id']).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'
    # success_url = reverse_lazy('home')

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})
#
#
# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
#     Проверяем пришли ли данные постом
#     if request.method == 'POST':
#         Заполняем форму
#         form = NewsForm(request.POST)
#         Проверяем прошла ли форма валидацию и сохраняем её
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         Создаём несвязанную с данными форму
#         form = NewsForm()
#     Передаём одну из двух форму в контекст
#     return render(request, 'news/add_news.html', {'form': form})
