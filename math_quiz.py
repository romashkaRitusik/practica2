from tkinter import *
from tkinter.messagebox import showinfo

FILENAME = 'voprosy_testa.txt'

root = Tk()
root.title('Тест по математике')

v = IntVar(value=0)
res = 0
num = 0
k = 0

quest = Text(root, width=40, height=4, bg='white', wrap=WORD,
             font=('Comic Sans MS', 14), padx=15)
quest.grid(row=0, column=0, columnspan=2, padx=8, pady=(8, 0))

rb = []
for i in range(4):
    r = Radiobutton(root, variable=v, value=i + 1, padx=10, anchor='w', width=40,
                    font=('Arial', 12))
    r.grid(row=i + 1, column=0, sticky='w', padx=12)
    rb.append(r)

button = Button(root, width=20, text='Следующий вопрос', bg='white')
button.grid(row=5, column=0, pady=10)


def reaction(event=None):
    button.config(state='normal')


for r in rb:
    r.bind('<Button-1>', reaction)

f = None


def parse_answer_line(line):
    """Поддержка '2' и '+2'."""
    s = line.strip()
    if s.startswith('+'):
        s = s[1:]
    return int(s)


def newQuestion():
    global k, f, num, res

    button.config(state='disabled')
    v.set(0)

    s = f.readline()
    if not s:
        s = '#\n'
    if s[0] == '#':
        showinfo('Результат', f'Правильных ответов: {res} из {num}')
        try:
            f.close()
        except Exception:
            pass
        root.destroy()
        return

    num += 1
    root.title('Вопрос ' + s.rstrip())

    vopros = f.readline().rstrip()

    quest.config(state='normal')
    quest.delete('1.0', END)
    quest.insert('1.0', vopros)
    quest.config(state='disabled')

    k = parse_answer_line(f.readline())

    for i in range(4):
        txt = f.readline().rstrip()
        rb[i].config(text=txt)


def check():
    global num, res, k
    if v.get() == 0:
        return
    if v.get() == k:
        res += 1
    newQuestion()


button.config(command=check)

f = open(FILENAME, encoding='utf-8')
newQuestion()

root.mainloop()
