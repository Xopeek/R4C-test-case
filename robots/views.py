import datetime

from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from openpyxl import Workbook

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

        # if Robot.objects.filter(version=version).exists():
        #     return JsonResponse(
        #         {'message': 'Данная модель и версия роботы уже существует.'},
        #         status=400
        #     )

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


class ExcelReportView(View):
    def get(self, request, *args, **kwargs):
        end_date = timezone.now()
        start_date = end_date - datetime.timedelta(days=7)

        robots = Robot.objects.filter(
            created__range=[start_date, end_date]
        ).values('model', 'version').annotate(count=Count('id'))

        wb = Workbook()

        current_model = None

        for robot in robots:
            model = robot['model']
            version = robot['version']
            count = robot['count']

            if model != current_model:
                ws = wb.create_sheet(title=model)
                ws.append(["Модель", "Версия", "Количество за неделю"])
                current_model = model
            else:
                ws = wb[model]

            ws.append([model, version, count])

        default_sheet = wb['Sheet']
        wb.remove(default_sheet)

        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = f'attachment; filename="robot_production_report.xlsx"'
        wb.save(response)

        return response
