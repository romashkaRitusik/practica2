from random import shuffle, randint
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Таблица чисел')

nums = []
btns = []
row = 3
col = 5
count = 0
err = 0

v = IntVar(value=0)


def hide(x):
    global nums, btns, count, err, row, col
    if not nums:
        return
    w = min(nums) if v.get() == 0 else max(nums)
    if btns[x]['text'] == str(w):
        btns[x]['text'] = ''
        btns[x]['state'] = 'disable'
        btns[x]['bg'] = 'lightgreen'
        nums.remove(w)
        count += 1
        if count == row * col:
            yes = messagebox.askyesno(
                'Игра окончена',
                f'Сделано {err} ошибки(ок,а). Начать новую?'
            )
            if yes:
                newgame(row, col)
            else:
                root.destroy()
    else:
        btns[x]['bg'] = 'pink'
        err += 1


def newgame(n, m):
    global nums, btns, count, err, row, col
    row, col = n, m
    count, err = 0, 0

    nums = []
    w = 0
    for _ in range(row * col):
        w = w + randint(2, 7)
        nums.append(w)
    shuffle(nums)

    if btns:
        for b in btns:
            b.destroy()

    btns.clear()
    for i in range(row * col):
        b = Button(
            root, width=3, height=1,
            text=str(nums[i]),
            font=('Georgia', 16, 'bold'),
            command=lambda x=i: hide(x)
        )
        btns.append(b)
        b.grid(row=i // col, column=i % col, padx=4, pady=4)


menubar = Menu(root)
root.config(menu=menubar)

submenu = Menu(menubar, tearoff=0)
submenu.add_command(label='3 строки, 4 столбца', command=lambda: newgame(3, 4))
submenu.add_command(label='3 строки, 5 столбцов', command=lambda: newgame(3, 5))
submenu.add_command(label='4 строки, 6 столбцов', command=lambda: newgame(4, 6))
menubar.add_cascade(label='Параметры', menu=submenu)

dopmenu = Menu(menubar, tearoff=0)
dopmenu.add_radiobutton(label='по возрастанию', variable=v, value=0)
dopmenu.add_radiobutton(label='по убыванию', variable=v, value=1)
menubar.add_cascade(label='Порядок выбора', menu=dopmenu)

newgame(3, 5)
root.mainloop()
