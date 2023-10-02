from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

import json

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


@method_decorator(csrf_exempt, name='dispatch')
class OrderCreationView(View):
    """Создание заказов на роботов."""
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        customer_email = data['customer']
        robot_serial = data['robot_serial']
        customer, created = Customer.objects.get_or_create(
            email=customer_email
        )

        try:
            with transaction.atomic():
                order, created = Order.objects.get_or_create(
                    customer=customer,
                    robot_serial=robot_serial
                )
                if created:
                    response_data = {
                        'message': 'Заказ создан'
                    }
                else:
                    response_data = {
                        'message': 'Заказ уже существует'
                    }
        except IntegrityError:
            response_data = {
                'message': 'Ошибка создания заказа'
            }
            return JsonResponse(response_data, status=400)
        try:
            robot = Robot.objects.get(serial=robot_serial)
            if robot:
                response_data = {
                    'message': 'Заказ успешно выполнен'
                }
        except Exception:
            response_data = {
                'message': 'Такого робота нет,'
                           ' но мы Вам напишем как только он появится'
            }
        return JsonResponse(response_data)

