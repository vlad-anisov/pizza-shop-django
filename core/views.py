from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.http import QueryDict
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from allauth.account.views import PasswordChangeView
from .serializers import ItemPolymorphicSerializer
from .models import Item, Pizza, Drink, Order, OrderItem, Address, Restaurant
from .form import AddressForm, UserEditForm


class IndexView(ListView):
    queryset = Pizza.objects.filter(size='25')
    template_name = 'core/index.html'


class DrinksView(ListView):
    model = Drink
    template_name = 'core/drinks.html'


class PizzaView(ListAPIView):
    serializer_class = ItemPolymorphicSerializer

    def get_queryset(self):
        if self.kwargs['slug']:
            return Pizza.objects.filter(slug=self.kwargs['slug'])
        else:
            return Pizza.objects.all()


class ProfileView(View):

    def get(self, request):
        context = {
            'form': UserEditForm(instance=request.user),
            'orders': Order.objects.filter(user=request.user)
        }
        return render(request, 'core/profile.html', context)

    def post(self, request):
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль был обнавлён')
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка обновления аккунта')
            return redirect('profile')


class CartView(APIView):

    def get(self, request):  
        request.session['order_items'] = request.session.get('order_items', [])
        request.session.modified = True
        return Response(request.session['order_items'])

    def post(self, request, pk):
        item = ItemPolymorphicSerializer(Item.objects.get(pk=pk))
        order_item = {
            'item': item.data,
            'quantity': 1
        }
        request.session['order_items'].append(order_item)
        request.session.modified = True
        return Response(order_item)

    def put(self, request, pk):
        for index, order_item in enumerate(request.session['order_items']):
            if order_item['item']['id'] == pk:
                request.session['order_items'][index] = request.data
                request.session.modified = True
                return Response('OK')

    def delete(self, request, pk):
        for order_item in request.session['order_items']:
            if order_item['item']['id'] == pk:
                request.session['order_items'].remove(order_item)
                request.session.modified = True
                return Response('OK')


class OrderView(APIView):

    def send_message(self, user):
        message = f'Заказ принят. Статус заказа можно посмотреть в своём профиле'\
            f'Логин: {user.username}'\
            f'Пароль: {user.password}'
        send_mail('Pizza', message, settings.EMAIL_HOST_USER,
                  [user.email], fail_silently=False)

    def create_user(self, email):
        password = User.objects.make_random_password()
        user = User.objects.create_user(
            username=email, email=email, password=password)
        user.save()
        return user

    def order_items(self):
        order_items = []
        for order_item in self.request.session['order_items']:
            item = Item.objects.get(pk=order_item['item']['id'])
            quantity = order_item['quantity']
            order_item = OrderItem(item=item, quantity=quantity)
            order_item.save()
            order_items.append(order_item)
        return order_items

    def order(self, user, address):
        order = Order(
            user=user,
            address=address,
            order_time=self.request.data['order_time'],
        )
        order.save()
        order.order_items.add(*self.order_items())
        order.save()
        return order

    def address(self):
        query_dict = QueryDict('', mutable=True)
        query_dict.update({
            'street': self.request.data['street'],
            'house': self.request.data['house'],
            'apartment': self.request.data['apartment'],
        })
        address = AddressForm(query_dict)
        if address.is_valid():
            return address.save()
        else:
            return False

    def get(self, request):
        context = {
            'form': AddressForm(),
            'restaurants': Restaurant.objects.all()
        }
        return render(request, 'core/order.html', context)

    def post(self, request):
        if not request.session['order_items']:
            return Response('Корзина пуста. Пожалуйста добавьте товар в корзину')

        address = self.address()
        if not address:
            return Response('Не правильно введены данные')

        if request.user.is_authenticated:
            order = self.order(request.user, address)
            return Response('Заказ принят. Статус заказа можно посмотреть в своём профиле')

        if User.objects.filter(email=request.data['email']):
            return Response('Пользователь с таким email уже существует. Пожалуйста войдите в свой аккаунт или измените email')

        user = self.create_user(email=request.data['email'])
        self.order(user, address)
        self.send_message(user)
        return Response('Заказ принят. Статус заказа можно посмотреть в своём профиле. Данные для входа в аккаунт мы отпраивли вам на email')


class CustomPasswordChangeView(PasswordChangeView):
    success_url = '/profile'
