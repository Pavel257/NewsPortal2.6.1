from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    censor_list = ['дебил',
                   'дурак',
                   'придурок']

    value1 = (str(value)).split()
    for i in censor_list:
        for j in value1:
            if j == i:
                value1.remove(i)
    value = ' '.join(value1)
    return str(value)

    # else:
    #     return f'Нелья писать следующие слова:{censor_list}'

    # if isinstance(value, str) and isinstance(arg, int):
    #     return str(value) * arg  # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
    # else:
    #     raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')  #  в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку

#
@register.filter(name='update_page')
def update_page(full_path: str, page: int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param in params_list])
        params.update({'page': page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"



# список слов, которые будем цензурировать
# STRONG_WORDS = ["php", "редиска"]
#
#
# @register.filter()
# def censor(value):
#    if not isinstance(value, str):
#        raise ValueError('Нельзя цензурировать не строку')
#
#    for word in STRONG_WORDS:
#        value = value.replace(word[1:], '*' * (len(word)-1))
#
#    return value

# '''фильтр, который заменяет все буквы кроме первой и последней на «*» у слов из списка «нежелательных».'''
# '''Можно считать, что запрещенные слова находятся в списке forbidden_words.'''
# @register.filter
# def hide_forbidden(value):
#     forbidden_words = ['дебил',
#                    'дурак',
#                    'придурок',
#
#     ]
#     words = value.split() #Предполагается, что в качестве аргумента гарантированно передается текст, и слова разделены пробелами
#     result = []
#     for word in words:
#         if word in forbidden_words:
#             result.append(word[0] + "*"*(len(word)-2) + word[-1])
#         else:
#             result.append(word)
#     return " ".join(result)