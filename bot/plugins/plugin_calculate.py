# coding:utf8


import math


class Plugin(object):
    __doc__ = '''Плагин редназначен для вычисления результатов метематического выражения.
    Для использования необходимо иметь уровень доступа {protection} или выше
    Ключевые слова: [{keywords}]
    Использование: {keyword} <выражение>
    Пример: {keyword} (3/4) * PI * 7^3'''

    name = 'calculate'
    keywords = (name, u'посчитай', '=')
    protection = 0
    argument_required = True

    def respond(self, msg, rsp, *args, **kwargs):
        expression = ''.join(msg.args[1:]).lower()

        if re.match(u'^([\d+\-*/%:().,^√πe]|(sqrt)|(pi))+$', expression):
            expression = re.sub(u'(sqrt)|√', 'math.sqrt', expression)
            expression = re.sub(u'(pi)|π',   'math.pi',   expression)
            expression = re.sub(u':|÷',      '/',         expression)
            expression = re.sub('e',         'math.e',    expression)
            expression = re.sub('\^',        '**',        expression)
            expression = re.sub(',',         '.',         expression)

            expression = re.sub('(?P<int>(?<![\d.])\d+(?![\d.]))',
                                '\g<int>.', expression)

            try:
                result = eval(expression)
            except SyntaxError:
                result = u'Ошибка [0]\n' + expression
            except NameError:
                result = u'Ошибка [1]\n' + expression
            except AttributeError:
                result = u'Ошибка [2]\n' + expression
            except TypeError:
                result = u'Ошибка [3]\n' + expression
            except ZeroDivisionError:
                result = u'Деление на 0'
            except OverflowError:
                result = 'Infinite'
            else:
                if type(result) not in (int, long, float):
                    result = u'Не математическая операция'
                else:
                    result = str(result)
        else:
            result = u'Не математическая операция'

        rsp.text = result

        return rsp
