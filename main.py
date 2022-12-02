from tkinter import *


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
     
    return a2

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


def paint(a):

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

    a = define_array("1.txt")

    # print("a =", a)

    if not isinstance(a, int):
        if isConvex(a) == 1:
            print("It's a convex polygon.")
        elif isConvex(a) == 0:
            print("It isn't a convex polygon.")
        paint(a)

    return 0


main()