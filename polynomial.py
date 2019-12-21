import math

# Используем для сравнения:
EPSILON = 1.E-20

class Polynomial:
    '''
    Класс для работы с многочленами.
    '''

    def __init__(self, *coefficients):
        '''
        Позволяет построить многочлен по списку коэффициентов
        или на основе другого экземпляра того же самого класса.
        '''

        # В качестве внутреннего представления многочлена мы будем использовать
        # список значений коэффициентов от нулевой до максимальной степени,
        # при этом возможны нулевые значения:
        self.coefs = []

        # Если передан словарь, то извлекаем из нее значения
        # в список, выставляя нулевые значения для пропущенных степеней:
        if isinstance(coefficients[0], (dict,)):
            # Определяем максимальную степень многочлена:
            d = max(coefficients[0].keys())

            # В цикле обходим все возможные коэффициенты многочлена:
            for k in range(d + 1):
                # Если коэффициент данной степени отсутствует в словаре, то
                # указываем ноль, иначе извлекаем соответствующее значение:
                if not k in coefficients[0]:
                    self.coefs.append(0)
                else:
                    self.coefs.append(coefficients[0][k])

        # Если передан список, то просто извлекаем значения:
        elif isinstance(coefficients[0], (list,)):
            self.coefs = [c for c in coefficients[0]]

        # Если передан другой экземпляр класса, то копируем:
        elif isinstance(coefficients[0], (Polynomial,)):
            self.coefs = [c for c in coefficients[0].coefs]

        # Если переданы аргументы, то сохраняем их аналогично списку:
        else:
            self.coefs = [c for c in coefficients]

        # Удаляем ведущие нули при наличии
        while len(self.coefs) > 0 and abs(self.coefs[-1]) < EPSILON:
            self.coefs.pop()

        # Для возможности хранения тождественно равных нулю многочленов:
        if len(self.coefs) == 0:
            self.coefs = [0]

    @property
    def d(self):
        '''
        Свойство - степень многочлена.
        '''

        return len(self.coefs) - 1

    def __repr__(self):
        '''
        Возвращает компактное представление многочлена.
        '''

        s = ', '.join([str(c) for c in self.coefs])
        s = 'Polynomial ' + '[%s]'%s
        return s

    def __str__(self):
        '''
        Возвращает строковое представление многочлена.
        '''

        s = ''

        # В цикле обходим все коэффициенты многочлена в обратном порядке:
        for i, c in enumerate(self.coefs[::-1]):

            # Текущий показатель степени:
            k = self.d - i

            # Если коэффициент данной степени нулевой, то
            # обрываем итерацию цикла:
            if c == 0:
                continue

            # Для отрицательных коэффициентов всегда приписываем знак '-':
            if c < 0:
                # Если это знак в начале записи, то пробел не делаем:
                if len(s) > 0:
                    s+= ' - '
                else:
                    s+= '-'

            # Для положительных коэффициентов приписываем знак '+',
            # если это не самый первый коэффициент в записи:
            elif len(s) > 0:
                s+= ' + '

            # Приписываем абсолютное значение коэффициента,
            # если степень нулевая, или он не равен единице
            if abs(c) != 1 or k == 0:
                s+= '%d'%abs(c)

            # Приписываем x, если показатель больше нуля:
            if k > 0:
                s+= 'x'

            # Припысываем степень x, если показатель больше единицы:
            if k > 1:
                s+= '^%d'%k

        return s

    def __eq__(self, other):
        '''
        Проверка на равенство.
        '''

        # Если сравнивается не с полиномом, то всегда не равны:
        if not isinstance(other, Polynomial):
            return False

        # Если степени не совпадают, то возвращаем False
        if self.d != other.d:
            return False

        # Сравниваем попарно коэффициенты:
        for c1, c2 in zip(self.coefs, other.coefs):
            if abs(c1 - c2) > EPSILON:
                return False

        return True

    def __add__(self, other):
        '''
        Вычисляем сумму данного многочлена с другим.
        '''

        # Если передано число:
        if isinstance(other, (int, float)):
            coefs = [c for c in self.coefs]
            coefs[0]+= other
            return Polynomial(coefs)

        coefs = []
        for i in range(max(len(self.coefs), len(other.coefs))):
            c1 = 0 if i >= len(self.coefs) else self.coefs[i]
            c2 = 0 if i >= len(other.coefs) else other.coefs[i]
            coefs.append(c1 + c2)

        return Polynomial(coefs)

    def __radd__(self, other):
        '''
        Сложение симметрично, поэтому просто возвращаем __add__.
        '''

        return self.__add__(other)

    def __neg__(self):
        '''
        Обратный к данному.
        '''

        return (-1) * self

    def __sub__(self, other):
        '''
        Вычитание из данного полинома.
        Домножаем other на (-1) и складываем.
        '''

        return self + (-1) * other

    def __rsub__(self, other):
        '''
        Вычитание данного полинома.
        Домножаем себя на (-1) и складываем.
        '''

        return other + (-1) * self

    def __call__(self, x):
        '''
        Возвращает значение многочлена в заданной точке x.
        '''

        p = 0.

        # Обходим в цикле все степени многочлена:
        for i, c in enumerate(self.coefs):
            p+= c * x**i

        return p

    def degree(self):
        '''
        Степень многочлена.
        '''

        return self.d

    def der(self, d=1):
        '''
        Вычисляет n-ую производную многочлена.
        '''

        if d == 0:
            return Polynomial(self)

        if len(self.coefs) == 1:
            return Polynomial(0)

        coefs = [0 for i in range(len(self.coefs)-1)]
        for i, c in enumerate(self.coefs):
            if i > 0:
                coefs[i-1] = c * i

        # Создаем новый полином и вычисляем оставшиеся производные
        return Polynomial(coefs).der(d-1)

    def __mul__(self, other):
        '''
        Произведение полиномов.
        '''

        # Если передано число:
        if isinstance(other, (int, float)):
            coefs = [c * other for c in self.coefs]
            return Polynomial(coefs)

        n1 = len(self.coefs)
        n2 = len(other.coefs)

        coefs = []
        for i in range(n1 * n2):
            coefs.append(0)

        for i in range(n1):
            for j in range(n2):
                coefs[i+j]+= self.coefs[i] * other.coefs[j]

        return Polynomial(coefs)

    def __rmul__(self, other):
        '''
        Произведение симметрично, поэтому просто возвращаем __mul__.
        '''

        return self.__mul__(other)

    def __mod__(self, other):
        '''
        Вычисление остатка от деления на other.
        '''

        # Если передано число:
        if isinstance(other, (int, float)):
            coefs = [c%other for c in self.coefs]
            return Polynomial(coefs)

        coefs = [0.]*(self.d - other.d)

        mod = Polynomial(self.coefs)
        while mod.d >= other.d:
            k = mod.d - other.d
            a = mod.coefs[-1] / other.coefs[-1]
            coefs[-k] = a

            for i in range(other.d, -1, -1):
                mod.coefs[i+k]-= a * other.coefs[i]

            # Делаем для удаления ведущих нулей:
            mod = Polynomial(mod)

        return mod

    def __rmod__(self, other):
        '''
        Данная операция не имеет смысла.
        '''

        return None

    def gcd(self, other):
        '''
        Вычисление наименьшего общего кратного.
        '''

        def gcd(f, g, p=0, verbose=False):
            if (len(f)<len(g)):
                return gcd(g,f,p, verbose)

            r = [0]*len(f)
            r_mult = reciprocal(g[0], p)*f[0]

            for i in range(len(f)):
                if (i < len(g)):
                    r[i] = f[i] - g[i]*r_mult
                else:
                    r[i] = f[i]
                if (p != 0):
                    r[i] %= p

            while (abs(r[0])<EPSILON):
                r.pop(0)
                if (len(r) == 0):
                    return g

            return gcd(r, g, p, verbose)

        def reciprocal(n, p=0):
            if (p == 0):
                return 1/n
            for i in range(p):
                if (n*i)%p == 1:
                    return i
            return None

        # Копируем:
        x1 = Polynomial(self).coefs[::-1]
        x2 = Polynomial(other).coefs[::-1]

        res = gcd(x1, x2)

        return Polynomial(res)

    def __iter__(self):
        '''
        Итерации по многочлену.
        '''

        for i, c in enumerate(self.coefs):
            yield (i, c)

    def __next__(self):
        '''
        Итерации по многочлену.
        '''

        try:
            return next(self.__iter__()).key
        except AttributeError:
            raise StopIteration


class RealPolynomial(Polynomial):
    '''
    Класс для работы с многочленами нечетной степени
    от вещественных коэффициентов.
    '''

    def find_root(self, x1=-10, x2=10, eps=1.E-6):
        '''
        Находит корень многочлена методом деления отрезка пополам:
        выбирается исходный отрезок x1, x2 и делится пополам до тех пор,
        пока значения многочлена на концах разного знака и точность
        не достигнута.
        '''

        p1, p2 = self(x1), self(x2)
        for i in range(1000000):
            x0 = (x2 + x1) / 2
            p0 = self(x0)

            if p1 * p0 < 0:
                x2, p2 = x0, p0
            else:
                x1, p1 = x0, p0
            if abs(p0) < eps:
                break

        return x0


class QuadraticPolynomial(Polynomial):
    '''
    Класс для работы с многочленами степени не выше 2-х.
    '''

    def solve(self):
        '''
        Находит корни многочлена (не более двух) и возвращает список.
        '''

        # Для многочлена нулевой степени a
        # возвращаем пустой список:
        if self.d == 0:
            return []

        # Для многочлена первой степени a + b x
        # возвращаем единственное решение x = - a / b
        if self.d == 1:
            return [- self.coefs[0] / self.coefs[1]]

        # Вычисляем детерминант
        D = self.coefs[1] * self.coefs[1] - 4 * self.coefs[0] * self.coefs[2]

        # Если детерминант меньше нуля, то корней нет:
        if D < 0:
            return []

        x1 = (-self.coefs[1] + math.sqrt(D)) / 2 / self.coefs[2]
        x2 = (-self.coefs[1] - math.sqrt(D)) / 2 / self.coefs[2]
        return [x1, x2]


if __name__ == '__main__':
    # Выполняется, если модуль вызывается непосредственно из консоли
    # Используем для отладки
    print('...')
