from django import template

register = template.Library()

CENSOR_SYMBOLS = {
    'редиска': '******',
    'сосиска': '******',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    if not (isinstance(value, str)):
        return f"{value} is not str"

    words = ''
    for word in value.split():
        slovo = word.lower() if word.lower()[-1].isalpha() else word.lower()[:-1]
        if slovo in CENSOR_SYMBOLS:
            znak = '' if word.lower()[-1].isalpha() else word[-1]
            words += word[:1] + CENSOR_SYMBOLS[slovo] + znak + ' '
        else:
            words += word + ' '

    return words[:-1]
