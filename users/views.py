from django.shortcuts import render,reverse,HttpResponseRedirect ,HttpResponseRedirect
from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from products.models import Basket
from django.views.generic.edit import  CreateView, UpdateView
from common.views import TitleMixin
from django.views.generic.base import TemplateView


# Create your views here.


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    # передаем всего лишь ссылку а сам класс вызовится под капотам
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    # куда перенаправляем
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляем! Вы успешно зарегестрировались'
    title = 'Store - Регистрация '


# наглядный  пример сто лучше использовать класссы
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация '

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - личный кабинет'

    # чтобы изменить пользователя нам нужен его айдишник
    # он же и используется когда перенаправляем пользователя
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.request.user)
    #     return context


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store  - подтверждение электронной почты'
    template_name = 'users/email_verification.html '

    # в шаблоне срабатывает  get_запрос и вызывается метод
    # метод get мз TemplateView  мы его переоределим
    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        # если список не пуст и срок не истек
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email=True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index', ))


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             # сохраняем объект в базе данных
#             form.save()
#             # messages будет достпунов login, пердовать его не надо
#             messages.success(request, 'Поздравляем! Вы успешно зарегестрировались')
#             # reverse  перенаправлять с помощью  параметров  name
#             # HttpResponseRedirect служит для перенаправления url адреса
#             # можно прописывать адрес через /(не работает), мы пишем через :  потому что используем namе наверное(проверить)
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


# def login(request):
#     # в данном конролере выполнятся сразу два запроса POST и Get
#     # Get  выдает пользователю страницу(форму для заполнения)
#     # post клиент отправляет данные на сервер, а сервер их проверяет
#     # контроль Audit
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             # антификация -  проверка подлиности Autenication
#             user = auth.authenticate(username=username, password=password)
#             # если такой пользователь существует
#             if user:
#                 # авторизация -разрешение на выполнение чего либо Authonrisation
#                 auth.login(request, user)
#                 return HttpResponseRedirect('/')
#     else:
#         form = UserLoginForm
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         # не совсем понятно, такое чувтство что мы создали нового пользователмя а не изменили текущего
#         # почему- то эту проблему решил instance=request.user
#         # files=request.FILES для добовления файла в шаблоне profile,
#         # почему-то не работает может быть изображение не подходит по размерам, проверить позже
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         # что бы имеющиеся данные о пользователи отброжались на полях используем параметр instance
#         form = UserProfileForm(instance=request.user)
#     baskets = Basket.objects.filter(user=request.user)
#
#     context = {
#         'title': 'Store-профиль',
#         'form': form,
#         'baskets': baskets,
#     }
#     return render(request, 'users/profile.html', context)
