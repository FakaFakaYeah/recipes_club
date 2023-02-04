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
