from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

class LogoutView(BaseLogoutView):
    pass

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    # FCV for email verification
    def form_valid(self, form):
        self.object = form.save()
        send_mail(
            subject='Верификация по почте',
            message=f'Это подтверждение регистрации пользователя {self.object.email}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def reset(request):
    found = False  # flag to check existing user
    email = None
    user_to_save = None
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.all()
        for user in users:
            if email == user.email:
                found = True
                user_to_save = user
                user
        # Generate new password
        if not found:
            print('No email found')
            render(request, 'users/reset.html')
        else:
            new_password = User.objects.make_random_password(length=12)
            # new_password = '123admin123'
            send_mail(
                subject='Восстановление пароля',
                message=(f'Пользователь - {email}\n'
                         f'Ваш новый пароль: {new_password}'),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            user_to_save.set_password(new_password)
            user_to_save.save()
            return redirect(reverse('users:login'))

    return render(request, 'users/reset.html')






