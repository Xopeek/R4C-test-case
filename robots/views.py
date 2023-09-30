from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

import json

from robots.models import Robot


@method_decorator(csrf_exempt, name='dispatch')
class RobotCreationView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serial = data['serial']
        model = data['model']
        version = data['version']
        created = data['created']

        if Robot.objects.filter(model=model, version=version).exists():
            return JsonResponse(
                {'message': 'Данная модель и версия роботы уже существует.'},
                status=400
            )

        if serial and model and version and created:
            Robot.objects.create(
                serial=serial,
                model=model,
                version=version,
                created=created
            )
            return JsonResponse(
                {'message': 'Robot created successfully.'}
            )
        return JsonResponse(
            {'message': 'Invalid data provided.'},
            status=400
        )
