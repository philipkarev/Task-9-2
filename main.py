from tkinter import *

max_X = 1200  # ширина окна (количество точек по горизонтали)
max_Y = 800  # высота окна
e_x = 6.0  # количество единичных отрезков по полож. части оси х в преобразованной системе координат
e_y = e_x * max_Y / max_X  # кол-во единичных отр. по полож. части оси у из условия их рав-вва по длине


def define_array(SInputFile):  # заполнение массива точками из файла

    a1 = []  # сюда считаем числа из файла
    a2 = []  # двумерный массив точек
    ise = 0  # флаг

    try:
        with open(SInputFile) as f:
            while True:
                s = f.readline()

                if not s:  # выходим, если конец
                    break

                s = s.split()

                for i in range(len(s)):
                    a1.append(int(s[i]))
                    ise += 1

    except ValueError:
        print("Error: bad value.")
        f.close()
        return -1

    except FileNotFoundError:
        print("Error: file not found.")
        return -1

    if ise == 0:  # проверка на пустой файл
        print("Error: file is empty.")
        return -1

    if ise % 2 != 0:  # проверка на нечётное кол-во чисел в файле
        print("Error: the number of numbers in the file is odd.")
        return -1

    if ise == 2 or ise == 4:  # вершин д.б. больше 2
        print("Error: it's not a polygon.")

    for i in range(0, len(a1) - 1, 2):
        a2.append([a1[i], a1[i + 1]])

    for i in range(len(a2)):  # проверка на самопересечение точек
        for j in range(i + 1, len(a2)):
            if a2[i] == a2[j]:
                print("a2[i] =", a2[i], " == a2[j] =", a2[j])
                print("Error: detected intersection of points.")
                return -1
     
    return a1, a2

def isConvex(array):  # проверка на выпуклость

    isc = 1

    # if (len(array)) == 3:
    #     return 1  # triangle always is convex

    for i in range(len(array) - 1):  # ур-ие прямой через данные две точки
        a = array[i + 1][1] - array[i][1]
        b = array[i][0] - array[i + 1][0]
        c = array[i][0] * (array[i][1] - array[i + 1][1]) + \
            array[i][1] * (array[i + 1][0] - array[i][0])
        #ур-ие ищу в виде: a * x + b * y + c = 0

        # print("\n i =", i)
        # print("\nLine:", a, "* x +", b, "* y +", c, "= 0")

        for j in range(len(array) - 1):
            if j != i and j + 1 != i and j != i + 1:  # точки, по к-рым составл.ур-ие
                if sign(a * array[j][0] + b * array[j][1] + c) != \
                        sign(a * array[j + 1][0] + b * array[j + 1][1] + c):
                    # print("@@ j =", j)
                    # print("points for line: i =", i, "i + 1 =", i + 1)
                    # print("a * array[j][0] + b * array[j][1] + c =",
                    #       a * array[j][0] + b * array[j][1] + c)
                    # print("a * array[j + 1][0] + b * array[j + 1][1] + c =",
                    #       a * array[j + 1][0] + b * array[j + 1][1] + c)

                    isc = 0  # it's not a convex polygon

    a = array[len(array) - 1][1] - array[0][1]  # построим прямую по 1-ой и посл. точкам
    b = array[0][0] - array[len(array) - 1][0]
    c = array[0][0] * (array[0][1] - array[len(array) - 1][1]) + \
        array[0][1] * (array[len(array) - 1][0] - array[0][0])

    for j in range(len(array) - 1):
        if j != 0 and j != len(array) - 1 and j + 1 != len(array) - 1:  # точки, по к-рым составл.ур-ие
            if sign(a * array[j][0] + b * array[j][1] + c) != \
                    sign(a * array[j + 1][0] + b * array[j + 1][1] + c):
                # print("@@ j =", j)
                # print("points for line: i =", i, "i + 1 =", i + 1)
                # print("a * array[j][0] + b * array[j][1] + c =",
                #       a * array[j][0] + b * array[j][1] + c)
                # print("a * array[j + 1][0] + b * array[j + 1][1] + c =",
                #       a * array[j + 1][0] + b * array[j + 1][1] + c)

                isc = 0  # it's not a convex polygon

    if isc == 0:
        return 0
    elif isc == 1:
        return 1  # it's convex polygon


def draw(p):  # рисуем точки из списка

    for u in p:
        u.draw_circle()


def paint(a):

    class Point:  # точка плоскости с целыми координатами (в исходной системе координат)
        def __init__(self, a, b):  # конструктор класса
            self.x = a
            self.y = b

        def draw_line(self, other, color='black'):  # рисование линии на холсте, цвет по умолчанию - черный
            c.create_line(self.x, self.y, other.x, other.y, width=3, fill=color)

        def draw_circle(self, radius=0.03, color='black'):  # рисование окружности на холсте
            r = RPoint(radius, radius)  # овал вписан в прямоугольник, выч. его границ
            c.create_oval((self - r).x, (self - r).y, (self + r).x, (self + r).y, fill=color)  # исп. -

    class RPoint(Point):  # дочерний класс  точка с вещест. координатами для реальной работы
        def __init__(self, a, b):
            self.x_ = a
            self.y_ = b
            self.x = max_X * (
                    a / e_x + 1.) / 2.  # пересчет координат из системы координат в центре окнав и единичными отрезками e_x, e_y в исходную (с центром влевом верхнем углу)
            self.y = max_Y * (-b / e_y + 1.) / 2.

        def __add__(self, other):  # сложение точек (векторов)
            return RPoint(self.x_ + other.x_, self.y_ + other.y_)

        def __sub__(self, other):  # разность точек(векторов)
            return RPoint(self.x_ - other.x_, self.y_ - other.y_)

        def __mul__(self, other):  # векторное произведение
            return self.x_ * other.y_ - self.y_ * other.x_

    root = Tk()
    c = Canvas(width=max_X, height=max_Y, bg='white')  # приготовление холста для рисунка
    c.focus_set()
    c.pack()

    c.create_text(300, 70, text="Нажмите на клавиатуре стрелку вправо", fill="black", font=("Helvectica", "15"))

    RPoint(-e_x, 0.).draw_line(RPoint(e_x, 0.))  # горизонтальная ось
    RPoint(0., e_y).draw_line(RPoint(0., -e_y))  # вертикальная ось

    RPoint(-0.1, 1.).draw_line(RPoint(0.1, 1.))  # горизонтальная метка -единичный отрезок
    RPoint(1., 0.1).draw_line(RPoint(1., -0.1))  # вертикальная

    polygon = []  # список точек

    for i in range(len(a) - 1):
        polygon.append((RPoint(a[i], a[i+1])))

    # print("len(polygon) =", len(polygon))

    draw(polygon)

    def draw_path(event):  # обработчик события
        b = 0
        for u in polygon:  # для каждой точки списка
            if b > 0:
                u.draw_line(v, 'red')  # соединяем красной линией 2 соседние точки
            b += 1
            v = u
        polygon[0].draw_line(polygon[-1], 'red')  # первую точку соединяем с последней

    c.bind('<Right>', draw_path)  # к клавише стрелочка направо привязываем действие

    root.mainloop()  # бесконечный цикл

def paint1(a):

    window = Tk()
    window.title('draw a polygon')

    canvas = Canvas(window, width = 1200, height = 800, bg = "gray",
                    cursor = "pencil")

    for i in range(len(a) - 1):
        canvas.create_line(a[i][0] * 50, a[i][1] * 50, a[i + 1][0] * 50,
                           a[i + 1][1] * 50, width = 3, fill = "yellow")
    canvas.create_line(a[0][0] * 50, a[0][1] * 50, a[len(a) - 1][0] * 50,
                       a[len(a) - 1][1] * 50, width = 3, fill = "yellow")

    canvas.pack()
    window.mainloop()


def sign(x):

    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0


def main():

    [ar, a] = define_array("1.txt")

    # print("a =", a)

    if not isinstance(a, int):
        if isConvex(a) == 1:
            print("It's a convex polygon.")
        elif isConvex(a) == 0:
            print("It isn't a convex polygon.")
        paint(ar)

    return 0


main()