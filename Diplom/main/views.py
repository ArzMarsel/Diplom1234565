from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import Error
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_recaptcha.fields import ReCaptchaField
from .forms import UserCreation, LoginForm, PaymentForm, ConnectForm
from .models import Dish, Connect, DishImage
from .bot import send_telegram_message
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Connect
import json
@csrf_exempt
@require_http_methods(["POST"])
def update_connect_status(request, connect_id):
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        connect = Connect.objects.get(id=connect_id)
        connect.status = new_status
        connect.save()
        return JsonResponse({'message': 'Статус успешно обновлён!'}, status=200)
    except Connect.DoesNotExist:
        return JsonResponse({'error': 'Connect не найден.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def accepted_connects_view(request):
    accepted_connects = Connect.objects.filter(status='accepted').values('id', 'user__username', 'dish__name', 'quantity')
    connect_list = list(accepted_connects)
    return JsonResponse(connect_list, safe=False)

def cooking_connects_view(request):
    accepted_connects = Connect.objects.filter(status='cooking').values('id', 'user__username', 'dish__name', 'quantity')
    connect_list = list(accepted_connects)
    return JsonResponse(connect_list, safe=False)



@receiver(post_save, sender=Connect)
def send_notification(sender, instance, **kwargs):
    if instance.status == 'accepted':
        message = f"Заказ {instance.dish.name} принят!"
        async_to_sync(send_telegram_message)(chat_id='5139247587', text=message)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password1'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Ошибка в имени или пароле')
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {'form': form})


def user_login_l(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password1'])
            if user is not None:
                login(request, user)
                return redirect('dishes-l')
            else:
                form.add_error(None, 'Ошибка в имени или пароле')
    else:
        form = LoginForm()
    return render(request, 'register/login-l.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreation()
    return render(request, 'register/registrate.html', {'form': form})


def register_l(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login-l')
    else:
        form = UserCreation()
    return render(request, 'register/registrate-l.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def logout_view_l(request):
    logout(request)
    return redirect('dishes-l')


def ListOfDishes(request):
    dishes = Dish.objects.all().prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesLight(request):
    dishes = Dish.objects.all().prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesSoda(request):
    dishes = Dish.objects.filter(kind='soda').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesSalat(request):
    dishes = Dish.objects.filter(kind='salat').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesTuck(request):
    dishes = Dish.objects.filter(kind='tuck').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesFast(request):
    dishes = Dish.objects.filter(kind='fast').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesSec(request):
    dishes = Dish.objects.filter(kind='sec').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})



def ListOfDishesDesert(request):
    dishes = Dish.objects.filter(kind='desert').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesAlco(request):
    dishes = Dish.objects.filter(kind='alco').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesFirst(request):
    dishes = Dish.objects.filter(kind='first').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesSoda_l(request):
    dishes = Dish.objects.filter(kind='soda').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesSalat_l(request):
    dishes = Dish.objects.filter(kind='salat').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesTuck_l(request):
    dishes = Dish.objects.filter(kind='tuck').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesFast_l(request):
    dishes = Dish.objects.filter(kind='fast').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesSec_l(request):
    dishes = Dish.objects.filter(kind='sec').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})



def ListOfDishesDesert_l(request):
    dishes = Dish.objects.filter(kind='desert').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesAlco_l(request):
    dishes = Dish.objects.filter(kind='alco').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})


def ListOfDishesFirst_l(request):
    dishes = Dish.objects.filter(kind='first').prefetch_related('dishimage_set')
    dishes_with_images = [
        (dish, dish.dishimage_set.first().image.url if dish.dishimage_set.exists() else None)
        for dish in dishes
    ]
    return render(request, 'restaurant/main-light.html', {'dishes_with_images': dishes_with_images})


@login_required(login_url='login')
def DetailDish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    model = DishImage.objects.filter(dishes=dish)
    return render(request, 'restaurant/more_dish.html', context={'dish': dish, 'images': model})


@login_required(login_url='login-l')
def DetailDish_l(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    model = DishImage.objects.filter(dishes=dish)
    return render(request, 'restaurant/more_dish-l.html', context={'dish': dish, 'images': model})


@login_required(login_url='login')
def connect_to_corsina(request):
    dishes = Connect.objects.filter(user=request.user, mark=True).select_related('dish').prefetch_related('dish__dishimage_set')
    dishes_with_images = [
        (i, i.dish, i.dish.dishimage_set.first().image.url if i.dish.dishimage_set.exists() else None)
        for i in dishes
    ]
    return render(request, 'restaurant/corsina.html', {'dishes_with_images': dishes_with_images})


@login_required(login_url='login-l')
def connect_to_corsina_l(request):
    dishes = Connect.objects.filter(user=request.user, mark=True).select_related('dish').prefetch_related('dish__dishimage_set')
    dishes_with_images = [
        (i, i.dish, i.dish.dishimage_set.first().image.url if i.dish.dishimage_set.exists() else None)
        for i in dishes
    ]
    return render(request, 'restaurant/corsina-l.html', {'dishes_with_images': dishes_with_images})


@login_required(login_url='login')
def connect_to_saled(request):
    dishes = Connect.objects.filter(user=request.user, mark=False).select_related('dish').prefetch_related('dish__dishimage_set')
    dishes_with_images = [
        (i, i.dish, i.dish.dishimage_set.first().image.url if i.dish.dishimage_set.exists() else None)
        for i in dishes
    ]
    return render(request, 'restaurant/saled.html', {'dishes_with_images': dishes_with_images})


@login_required(login_url='login-l')
def connect_to_saled_l(request):
    dishes = Connect.objects.filter(user=request.user, mark=False).select_related('dish').prefetch_related('dish__dishimage_set')
    dishes_with_images = [
        (i, i.dish, i.dish.dishimage_set.first().image.url if i.dish.dishimage_set.exists() else None)
        for i in dishes
    ]
    return render(request, 'restaurant/saled-l.html', {'dishes_with_images': dishes_with_images})


@login_required(login_url='login')
def pay(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    connect = get_object_or_404(Connect, user=request.user, dish=dish, mark=True)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.connect = get_object_or_404(Connect, user=request.user, dish=dish, mark=True)
            payment.price = dish.price
            payment.save()
            connect.status = 'accepted'
            connect.mark = False
            connect.save()
            return redirect('success')
    else:
        form = PaymentForm()

    return render(request, 'restaurant/payment.html', {'form': form, 'dish': dish})


@login_required(login_url='login-l')
def pay_l(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    connect = get_object_or_404(Connect, user=request.user, dish=dish, mark=True)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.connect = get_object_or_404(Connect, user=request.user, dish=dish, mark=True)
            payment.price = dish.price
            payment.save()
            connect.status = 'accepted'
            connect.mark = False
            connect.save()
            return redirect('success')
    else:
        form = PaymentForm()

    return render(request, 'restaurant/payment-l.html', {'form': form})


def success(requests):
    return render(requests, 'restaurant/success.html')


def success_l(requests):
    return render(requests, 'restaurant/success-l.html')


def about_us(request):
    return render(request, 'restaurant/about us.html')


def about_us_l(request):
    return render(request, 'restaurant/about us-l.html')


def quan(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form = ConnectForm(request.POST)
        form.dish = get_object_or_404(Dish, pk=pk)
        form.user = request.user
        form.mark = True
        form.status = 'done'
        if form.is_valid():
            if form.cleaned_data['quantity'] <= dish.quantity:
                connect = Connect.objects.filter(user=request.user, dish=dish, mark=True).first()
                if connect:
                    connect.mark = True
                    connect.status = 'done'
                    connect.quantity += form.cleaned_data['quantity']
                    connect.save()
                    return redirect('dishes')
                else:
                    connect = form.save(commit=False)
                    connect.user = request.user
                    connect.mark = True
                    connect.status = 'done'
                    connect.dish = dish
                    connect.save()
                    return redirect('dishes')
    else:
        form = ConnectForm()
    return render(request, 'restaurant/quan.html', {"form": form})


def quan_l(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form = ConnectForm(request.POST)
        form.dish = get_object_or_404(Dish, pk=pk)
        form.user = request.user
        form.mark = True
        form.status = 'done'
        if form.is_valid():
            if form.cleaned_data['quantity'] <= dish.quantity:
                connect = Connect.objects.filter(user=request.user, dish=dish, mark=True).first()
                if connect:
                    connect.mark = True
                    connect.status = 'done'
                    connect.quantity += form.cleaned_data['quantity']
                    connect.save()
                    return redirect('dishes-l')
                else:
                    connect = form.save(commit=False)
                    connect.user = request.user
                    connect.mark = True
                    connect.status = 'done'
                    connect.dish = dish
                    connect.save()
                    return redirect('dishes-l')
    else:
        form = ConnectForm()
    return render(request, 'restaurant/quan-l.html', {"form": form})


def iseighteen(request, pk):
    pk = pk
    return render(request, "restaurant/iseighteen.html", {'pk': pk})


def iseighteen_l(request, pk):
    pk = pk
    return render(request, "restaurant/iseighteen-l.html", {'pk': pk})