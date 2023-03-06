from django.shortcuts import render, HttpResponseRedirect
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from products.models import Basket
from django.views.generic.edit import CreateView, UpdateView


# Create your views here.


class UserRegistrationView(CreateView):
    model = User
    # передаем всего лишь ссылку а сам класс вызовится под капотам
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    # куда перенаправляем
    success_url = reverse_lazy('users:login')


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # сохраняем объект в базе данных
            form.save()
            # messages будет достпунов login, пердовать его не надо
            messages.success(request, 'Поздравляем! Вы успешно зарегестрировались')
            # reverse  перенаправлять с помощью  параметров  name
            # HttpResponseRedirect служит для перенаправления url адреса
            # можно прописывать адрес через /(не работает), мы пишем через :  потому что используем namе наверное(проверить)
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/registration.html', context)



def login(request):
    # в данном конролере выполнятся сразу два запроса POST и Get
    # Get  выдает пользователю страницу(форму для заполнения)
    # post клиент отправляет данные на сервер, а сервер их проверяет
    # контроль Audit
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # антификация -  проверка подлиности Autenication
            user = auth.authenticate(username=username, password=password)
            # если такой пользователь существует
            if user:
                # авторизация -разрешение на выполнение чего либо Authonrisation
                auth.login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = UserLoginForm
    context = {'form': form}
    return render(request, 'users/login.html', context)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    #чтобы изменить пользователя нам нужен его айдишник
    # он же и используется когда перенаправляем пользователя
    def get_success_url(self):
        return reverse_lazy('users:profile',args=( self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - личный кабинет'
        context['baskets']= Basket.objects.filter(user=self.object)
        return context


@login_required
def profile(request):
    if request.method == 'POST':
        # не совсем понятно, такое чувтство что мы создали нового пользователмя а не изменили текущего
        # почему- то эту проблему решил instance=request.user
        # files=request.FILES для добовления файла в шаблоне profile,
        # почему-то не работает может быть изображение не подходит по размерам, проверить позже
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        # что бы имеющиеся данные о пользователи отброжались на полях используем параметр instance
        form = UserProfileForm(instance=request.user)
    baskets = Basket.objects.filter(user=request.user)

    context = {
        'title': 'Store-профиль',
        'form': form,
        'baskets': baskets,
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
