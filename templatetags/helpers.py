from django import template

register = template.Library()

@register.filter
def batch(sequence, count):
    """Разбивает последовательность на равные части заданной длины"""
    result = []
    for i in range(0, len(sequence), count):
        result.append(sequence[i:i+count])
    return result