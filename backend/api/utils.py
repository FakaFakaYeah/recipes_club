import io

from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


def shopping_cart_style(ingredients):
    buffer = io.BytesIO()
    c = Canvas(buffer)
    pdfmetrics.registerFont(
        TTFont('Bad_Comic', 'Bad_Comic.ttf', 'UTF-8'))
    c.setFont('Bad_Comic', size=25)
    c.drawCentredString(297, 800, 'Список покупок!')
    for ingredient in ingredients:
        c.drawString(50, 500, f"{ingredient['ingredient__name']}")
        c.drawString(50, 500, f"{ingredient['amount']}")
        c.drawString(50, 500, f"{ingredient['ingredient__measurement_unit']}")
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='Список покупок.pdf')


def universal_post(
    obj, user, model, obj_serialiezer, context, filter_field='recipe'
):
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
