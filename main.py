import tkinter
from tkinter.filedialog import *
import pygame
import threading
from tkinter import messagebox as msg

win = tkinter.Tk()
win.title('MP3 PLAYER')
win.geometry('645x365')
win.resizable(0,0)

#전역변수
li_music = []
ls_music = []
index = 0
lb_string = StringVar()
v_size = 0.30
win.pauseFlag = False
win.songgedFlag = False

def music_list():   #get folder with mp3 files
    global index
    dir = askdirectory()
    os.chdir(dir)

    for files in os.listdir(dir):
        li_music.append(files)
        ls_music.append(files)

    ls_music.reverse()

    pygame.mixer.init()
    pygame.mixer.music.load(li_music[index])

    win.songgedFlag = True


    def list_select(event):
        lb_string.set("")
        index = int(lb.curselection()[0])
        pygame.mixer.music.load(li_music[index])
        pygame.mixer.music.play()
        lb_string.set(li_music[index])

    def list_insert():
        i = 0

        for song in li_music:
            lb.insert(i, song)
            i += 1


    # win_menu = Toplevel(win)
    # win_menu.title("menu")
    # scrollbar = tkinter.Scrollbar(win_menu)
    # scrollbar.pack(side=RIGHT, fill=Y)
    # lb = Listbox(win_menu, width=50, yscrollcommand=scrollbar.set)
    # lb.pack(side=LEFT)
    # scrollbar.config(command=lb.yview)
    # song_lb = Label(textvariable = lb_string)
    # song_lb.pack()
    # list_insert()

    frame_menu = tkinter.Frame(win)
    frame_menu.place(x=10, y=50)
    scrollbar = tkinter.Scrollbar(frame_menu)
    scrollbar.pack(side=RIGHT, fill=Y)
    lb = Listbox(frame_menu, width=30, yscrollcommand=scrollbar.set)
    lb.pack(side=LEFT)
    scrollbar.config(command=lb.yview)
    song_lb = Label(win, textvariable = lb_string)
    song_lb.place(x=10, y=10)
    list_insert()

    lb.bind("<<ListboxSelect>>", list_select)

def music_AutoPlay():
    t = threading.Thread(target=music_autoplay)
    t.daemon = True
    t.start()

def music_autoplay():

    if win.songgedFlag == True:
        pygame.mixer.init()
        pygame.display.init()

        pygame.mixer.music.load(ls_music.pop())
        pygame.mixer.music.queue(ls_music.pop())
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.play()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if len(ls_music) > 0:
                        pygame.mixer.music.queue(ls_music.pop())
    else:
        msg.showinfo(title='Alarm', message='select your song first.')


def play_song(event):

    if win.songgedFlag == True:
        if (win.pauseFlag == True):
            pygame.mixer.music.unpause()
            win.pauseFlag = False
        else:
            pygame.mixer.music.play()
            lb_update()
    else:
        msg.showinfo(title='Alarm', message='select your song first.')

def stop_song(event):

    if win.songgedFlag == True:
        pygame.mixer.music.pause()
        win.pauseFlag = True
    else:
        msg.showinfo(title='Alarm', message='select your song first.')

def lb_update():
    global index
    lb_string.set(li_music[index])

def pre_song(event):

    if win.songgedFlag == True:
        global index
        if index == 0:
            return
        index -= 1
        pygame.mixer.music.load(li_music[index])
        pygame.mixer.music.play()
        lb_update()
    else:
        msg.showinfo(title='Alarm', message='select your song first.')

def next_song(event):

    if win.songgedFlag == True:
        global index
        if index == len(li_music[index]) -1:
            return
        index += 1
        pygame.mixer.music.load(li_music[index])
        pygame.mixer.music.play()
        lb_update()
    else:
        msg.showinfo(title='Alarm', message='select your song first.')

def v_up(event):
    if win.songgedFlag == True:
        global v_size
        pygame.mixer.music.set_volume(v_size)
        v_size += 0.10

    else:
        msg.showinfo(title='Alarm', message='select your song first.')

def v_down(event):
    if win.songgedFlag == True:
        global v_size
        pygame.mixer.music.set_volume(v_size)
        v_size -= 0.10
    else:
        msg.showinfo(title='Alarm', message='select your song first.')

def quit_music():
    pygame.mixer.music.stop()
    win.destroy()


img_main = tkinter.PhotoImage(file='image\\main.png')
main = tkinter.Label(image=img_main)
main.place(x=0, y=0)

img_forward = tkinter.PhotoImage(file='image\\fast-forward-1.png')
forward = tkinter.Button(image=img_forward)
forward.place(x=412, y=270)

img_rewind = tkinter.PhotoImage(file='image\\rewind-1.png')
rewind = tkinter.Button(image=img_rewind)
rewind.place(x=172, y=270)

img_play = tkinter.PhotoImage(file='image\\play-button-1.png')
play = tkinter.Button(image=img_play)
play.place(x=252, y=270)

img_pause = tkinter.PhotoImage(file='image\\pause-1.png')
pause = tkinter.Button(image=img_pause)
pause.place(x=332, y=270)

img_plus = tkinter.PhotoImage(file='image\\plus.png')
plus = tkinter.Button(image=img_plus)
plus.place(x=560, y=105)

img_minus = tkinter.PhotoImage(file='image\\minus.png')
minus = tkinter.Button(image=img_minus)
minus.place(x=560, y=195)

img_folder = tkinter.PhotoImage(file='image/folder-15.png')
folder = tkinter.Button(image=img_folder, command=music_list)
folder.place(x=560, y=15)

img_disc = tkinter.PhotoImage(file='image/compact-disc-1.png')
autoPlay = tkinter.Button(image=img_disc,command=music_AutoPlay)
autoPlay.place(x=560,y=285)





forward.bind("<Button-1>", next_song)
rewind.bind("<Button-1>", pre_song)
play.bind("<Button-1>", play_song)
pause.bind("<Button-1>", stop_song)
plus.bind("<Button-1>", v_up)
minus.bind("<Button-1>", v_down)




win.protocol('WM_DELETE_WINDOW', quit_music)

win.mainloop()



