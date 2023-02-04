import io

from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


def page_template(c):
    """Шаблон страницы листа PDF, если
    список покупок будет очень большой"""

    c.setFont('Bad_Comic', size=25)
    c.drawCentredString(297, 800, 'Список покупок!')
    c.drawCentredString(297, 20, 'Удачных покупок!')
    c.line(0, 730, 600, 730)
    c.line(0, 50, 600, 50)
    c.setFont('Bad_Comic', size=12)
    c.drawCentredString(510, 825, 'Prod by foodgram')
    c.drawString(30, 750, '№')
    c.drawString(160, 750, 'Ингредиент')
    c.drawString(350, 750, 'Количество')
    c.drawString(480, 750, 'Ед.Изм')


def universal_post(
    obj, user, model, obj_serialiezer, context, filter_field='recipe'
):
    if user == obj:
        raise ValidationError('Нельзя подписываться на себя!')
    if model.objects.filter(user=user, **{filter_field: obj}).exists():
        raise ValidationError(
            f'{user.first_name}, вы уже добавили'
            f'"{obj}" в {model._meta.verbose_name_plural}!'
        )
    serializer = obj_serialiezer(obj, context=context)
    model.objects.create(user=user, **{filter_field: obj})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def universal_delete(obj, user, model, filter_field='recipe'):
    queryset = model.objects.filter(user=user, **{filter_field: obj})
    if not queryset.exists():
        raise ValidationError(
            f'{user.first_name}, вы не добавляли'
            f'"{obj}" в {model._meta.verbose_name_plural}!'
        )
    queryset.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
