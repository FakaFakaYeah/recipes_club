import io

from django.conf import settings
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


def shopping_cart_page_create(ingredients):
    """Функция создания списка покупок в PDF"""
    buffer = io.BytesIO()
    c = Canvas(buffer)
    pdfmetrics.registerFont(
        TTFont('Bad_Comic', 'Bad_Comic.ttf', 'UTF-8'))
    page_template(c)
    y = 700
    ingredient_number = 1
    for ingredient in ingredients:
        c.drawCentredString(35, y, str(ingredient_number))
        c.drawCentredString(200, y, f"{ingredient['ingredient__name']}")
        c.drawCentredString(380, y, f"{ingredient['amount']}")
        c.drawCentredString(
            500, y, f"{ingredient['ingredient__measurement_unit']}"
        )
        y -= 25
        if ingredient_number % settings.ING_IN_PAGE == settings.ING_INDEX:
            c.showPage()
            page_template(c)
            y = 700
        ingredient_number += 1
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='Список покупок.pdf')


def page_template(c):
    """Шаблон страницы листа PDF"""
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


def universal_post(filter_options, model, obj, obj_serializer, context):
    """Универсальный метод по добавлению подписок,
    избранного и в список покупок"""
    if context['request'].user == obj:
        raise ValidationError('Нельзя подписываться на себя!')
    if model.objects.filter(**filter_options).exists():
        raise ValidationError(
            f'{filter_options["user"]}, вы уже добавили'
            f'"{obj}" в {model._meta.verbose_name_plural}!'
        )
    serializer = obj_serializer(obj, context=context)
    model.objects.create(**filter_options)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def universal_delete(filter_options, model, obj):
    """Универсальный метод по удалению из подписок,
        избранного и списка покупок"""
    queryset = model.objects.filter(**filter_options)
    if not queryset.exists():
        raise ValidationError(
            f'{filter_options["user"]}, вы не добавляли'
            f'"{obj}" в {model._meta.verbose_name_plural}!'
        )
    queryset.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
