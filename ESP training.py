from tkinter import *
from PIL import ImageTk, Image
# from tkinter import ttk
import datetime
import random
import time
import glob, os
from threading import Event, Thread
import playsound

show_picture = True
show_picked_color = False
show_picture = False   # Do you want to see picture from Pics folder on correct guess?
# show_picked_color = True   # For testing only. It prints chosen color.

vysledky = ''
guess = ''
r1 = '#f00'
r2 = '#600000'
g1 = '#0f0'
g2 = '#006000'
b1 = '#00f'
b2 = '#000060'
y1 = '#ff0'
y2 = '#606000'
r_btn = ''
y_btn = ''
b_btn = ''
g_btn = ''
text_note = ''
sg = ''
which_good = '  '
clr_d = {1: 'red', 2: 'yellow', 3: 'blue', 4: 'green'}
picked_color = ''
good = 0
bad = 0
col_dic = {'red': [r_btn, r1, r2], 'blue': [b_btn, b1, b2], 'green': [g_btn, g1, g2], 'yellow': [y_btn, y1, y2]}


def chime():
    playsound.playsound('chime.mp3')


def my_choice(clr):
    global sg
    global picked_color
    global good
    global bad
    global threads
    global text_note
    global vysledky
    global which_good
    global guess

    selection = ''
    try:
        selection = str(sg.get())
        sg.set('')
    except:
        pass

    if clr == '':
        pass
    elif clr == 'skip':
        # print('skip', picked_color)
        # btn_change_clr(picked_color)
        threads = [(Thread(target=btn_change_clr, args=(picked_color, False)))]
        threads[-1].start()
        vysledky += picked_color[:1] + ' '
        guess += 's '
    elif clr == picked_color:
        # print('match', picked_color)
        # btn_change_clr(picked_color)
        threads = [(Thread(target=chime))]
        threads[-1].start()
        threads = [(Thread(target=btn_change_clr, args=(picked_color, True,)))]
        threads[-1].start()
        good += 1
        vysledky += picked_color[:1] + ' '
        which_good += ' ' + str(good + bad)
        if selection and selection != picked_color:
            guess += clr[:1] + selection[:1]
        else:
            guess += clr[:1] + ' '
    elif clr != picked_color:
        # print('nomatch', picked_color)
        # btn_change_clr(picked_color)
        if picked_color == selection:
            bad += 0.5
            good += 0.5
            guess += clr[:1] + selection[:1]
        elif picked_color != selection and selection and selection != clr:
            guess += clr[:1] + selection[:1]
            bad += 1
        else:
            bad += 1
            guess += clr[:1] + ' '
        vysledky += picked_color[:1] + ' '
        threads = [(Thread(target=btn_change_clr, args=(picked_color, False,)))]
        threads[-1].start()

    picked_color = clr_d[random.randint(1, 4)]
    if show_picked_color:
        print(picked_color)
    if good + bad == 24:
        now = str(datetime.datetime.now())
        now = now[:-7] + '   '
        # text_note.delete(0.0, END)
        note = 'Done. Good: ' + str(good) + '   Bad: ' + str(bad) + '\n' + str(vysledky) + '\n' + str(guess)
        text_note.insert(END, note)
        f = open('ESP results.txt', 'a', encoding='utf8')
        f.write(now + str(vysledky) + '   ' + str(good) + which_good + '\n' + 22*' ' + guess + '\n')
        f.close()
    # print(vysledky)
    # print(guess)
    # print(good, bad, good+bad)


def btn_change_clr(clr, spravny):
    def pick_img():
        s = []
        for filename in glob.glob(os.path.join("Pics/", '*.jpg')):
            s.append(filename)
        for filename in glob.glob(os.path.join("Pics/", '*.png')):
            s.append(filename)
        i = random.randint(0, len(s)-1)
        s = s[i]
        return s

    if spravny and show_picture:
        img = Image.open(pick_img())
        img = img.resize((175, 220), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        # photo = PhotoImage(file="img.png")  # , height=130, width=130
        # photo.config(height=155, width=175)
        col_dic[clr][0].config(image=photo, height=175, width=220)  #
        time.sleep(4)
        col_dic[clr][0].config(image='', height=10, width=25)  #
    else:
        col_dic[clr][0].config(background=col_dic[clr][1])
        time.sleep(4)
        col_dic[clr][0].config(background=col_dic[clr][2])


my_choice('')


def ml():
    # Main Loop - Code for Window design
    global r_btn
    global y_btn
    global b_btn
    global g_btn
    global col_dic
    global text_note
    global sg
    clr_bgr = '#2b2b2b'  # Form background
    clr_fgr = '#a9b7c6'  # '#bbbbbb' #a9b7c6 '#cfcfcf'
    clr_frm_header = '#ccff00'
    # clr_d_bgr = '#3b3b3b'
    # clr_d_fgr = '#cfcfcf'  # '#818181'
    clr_btn_bgr = '#365880'  # 'gray'
    clr_btn_fgr = 'white'

    window = Tk()
    window.title("ESP Trainer")
    # window.geometry('350x200')
    # window.configure(background='#2b2b2b')
    # window.geometry('620x620')
    window.tk_setPalette(background=clr_bgr, foreground=clr_fgr, activeBackground=clr_bgr, activeForeground=clr_fgr)

    spec_frame = Frame(window, bd=2, relief=GROOVE)  # text="Options: ", padding="9 9 12 12"
    spec_frame.grid(row=0, column=0, sticky=(N, W, E, S))

    n_row = 0
    Label(spec_frame, text="I picked color. Which one is it?", foreground=clr_frm_header).grid(row=n_row, column=0,
                                                                                               sticky=W)
    n_row += 1
    r_btn = Button(spec_frame, text='', width=25, height=10, bg=r2, fg=clr_btn_fgr, command=lambda: my_choice('red'))
    r_btn.grid(row=n_row, column=0, sticky=N)
    col_dic['red'][0] = r_btn
    y_btn = Button(spec_frame, text='', width=25, height=10, bg=y2, fg=clr_btn_fgr, command=lambda: my_choice('yellow'))
    y_btn.grid(row=n_row, column=1, sticky=N)
    col_dic['yellow'][0] = y_btn

    n_row += 1
    b_btn = Button(spec_frame, text='', width=25, height=10, bg=b2, fg=clr_btn_fgr, command=lambda: my_choice('blue'))
    b_btn.grid(row=n_row, column=0, sticky=N)
    col_dic['blue'][0] = b_btn
    g_btn = Button(spec_frame, text='', width=25, height=10, bg=g2, fg=clr_btn_fgr, command=lambda: my_choice('green'))
    g_btn.grid(row=n_row, column=1, sticky=N)
    col_dic['green'][0] = g_btn

    n_row += 1
    Button(spec_frame, text='Skip', width=51, height=1, bg=clr_btn_bgr, fg=clr_btn_fgr,
           command=lambda: my_choice('skip')) \
        .grid(row=n_row, column=0, columnspan=2, sticky=N)

    n_row = 0
    sg = StringVar()
    sg_frame = Frame(window, bd=2, relief=GROOVE)  # text="Options: ", padding="9 9 12 12"
    sg_frame.grid(row=1, column=0, sticky=(N, W, E, S))
    Label(sg_frame, text="Second guess:", foreground=clr_frm_header).grid(row=n_row, column=0, sticky=W)
    R1 = Radiobutton(sg_frame, text="Red", selectcolor='black', variable=sg, value='red')\
        .grid(row=n_row, column=1, sticky=W)
    R2 = Radiobutton(sg_frame, text="Yellow", selectcolor='black', variable=sg, value='yellow')\
        .grid(row=n_row, column=2, sticky=W)
    R3 = Radiobutton(sg_frame, text="Blue", selectcolor='black', variable=sg, value='blue')\
        .grid(row=n_row, column=3, sticky=W)
    R4 = Radiobutton(sg_frame, text="Green", selectcolor='black', variable=sg, value='green')\
        .grid(row=n_row, column=4, sticky=W)

    notes_frame = Frame(window, bd=2, relief=GROOVE)  # text="Options: ", padding="9 9 12 12"
    notes_frame.grid(row=2, column=0, sticky=(N, W, E, S))
    n_row = 0
    # Label(notes_frame, text=note, foreground=clr_frm_header).grid(row=n_row, column=0, sticky=(W, N))
    text_note = Text(notes_frame, height=12, width=52, wrap="word", font=("Courier New", 9))
    text_note.grid(row=n_row, column=0, columnspan=2, sticky=(W, E))

    window.mainloop()


threads = [(Thread(target=ml))]
threads[-1].start()


