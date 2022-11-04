from tkinter import *
from tkinter import ttk
import datetime
import pygame
import subprocess

import autostart


def ComboChange(event):
    global city
    city = regions_list.get()
    save()


def save():
    with open("settings.txt", "r", encoding="utf-8") as f:
        settings = eval(f.read())
    with open("settings.txt", "w", encoding="utf-8") as f:
        settings["city"] = city
        settings["c"] = c.get()
        settings["r"] = r.get()
        settings["q"] = q.get()
        settings["w"] = w.get()
        settings["t1"] = t1
        print(settings, file=f)


def autoStartUp():
    if w.get() == 0:
        autostart.disable()
    elif w.get() == 1:
        autostart.enable()
    save()


def AlarmNotification(event):
    global alarmNotification, SirenaPlayed, SirenaNowPlaying, MusicPlaying
    pygame.mixer.music.stop()
    SirenaPlayed = False
    SirenaNowPlaying = False
    MusicPlaying = False
    if alarmNotification == 0:
        alarmNotification = 1
        try:
            app.destroy()
        except:
            pass
        enableAlarm.config(background="lime", text="Сповіщення ввімкнені")
        timeAlarm1.config(state="disabled")
        timeAlarm2.config(state="disabled")
        regions_list.config(state="disabled")
        minuteCheckBox.config(state="disabled")
        ConfigTimeAlarm.config(state="disabled")
        autoOnCheckBox.config(state="disabled")
        autoStartUpCheckBox.config(state="disabled")

    else:
        alarmNotification = 0
        enableAlarm.config(background="pink", text="Сповіщення вимкнені")
        timeAlarm1.config(state="normal")
        timeAlarm2.config(state="normal")
        regions_list.config(state="read")
        minuteCheckBox.config(state="normal")
        ConfigTimeAlarm.config(state="normal")
        autoOnCheckBox.config(state="normal")
        autoStartUpCheckBox.config(state="normal")


def IsAlarm(City):
    cmd = "curl https://alerts.com.ua/api/states -H \"X-API-Key: 95d44c372a0ff7220475e373ece7e0ac3362bfdc\""
    returned_output = subprocess.check_output(cmd, shell=True)
    cities = returned_output.decode("utf-8")[:-1]
    cities = cities.replace("true", "True")
    cities = cities.replace("false", "False")
    cities = eval(cities)["states"]
    for i in cities:
        if i["name"] == City and i["alert"] == True:
            return True
    return False


def NowInSec():
    return int((datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds())


def GetTime(entr1):
    global t1
    try:
        t1 = int(float(entr1.get())) if int(float(entr1.get())) == float(entr1.get()) else float(entr1.get())
        save()
        timeAlarm1.config(text=f"Оголошення - {t1} хвилин")
        app.destroy()
    except:
        but.config(text="Помилка")
        root.after(400, lambda : but.config(text="Зберегти"))


def ChangeTimeAlarm():
    global app, but
    app = Tk()
    app.title("Змінення часу тривоги")
    app.resizable(0, 0)
    app.update()
    x = app.winfo_screenwidth() / 2 - app.winfo_reqwidth() / 2
    y = app.winfo_screenheight() / 2 - app.winfo_reqheight() / 2
    app.wm_geometry("+%d+%d" % (x, y))

    frame = Frame(app)
    frame.grid(pady=10,padx=10)
    lb1 = Label(frame, text="Оголошення: ", font="Arial 12")
    lb1.grid(row=0, column=0)
    but = Button(frame, text="Зберегти", font="Arial 12", command=lambda: GetTime(entr1))
    but.grid()

    entr1 = Entry(frame, width=8)
    entr1.grid(row=0, column=1)

    app.mainloop()


root = Tk()
root.title("Повітряна тривога")
root.resizable(width=False, height=False)
pygame.init()


with open("locations_list/regions.txt", "r", encoding="utf-8") as f:
    regions = sorted(eval(f.read()))

with open("settings.txt", "r", encoding="utf-8") as f:
    settings = eval(f.read())


r = IntVar()
r.set(settings["r"])
c = IntVar()
c.set(settings["c"])
q = IntVar()
q.set(settings["q"])
w = IntVar()
w.set(settings["w"])
alarmNotification = 0
city = settings["city"]
SirenaPlayed = False
SirenaNowPlaying = False
MusicPlaying = False
t1 = settings["t1"]
end = 0


def SirenaPlay(link, sec=1, ends=0):
    global SirenaNowPlaying, end
    pygame.mixer.music.stop()
    pygame.mixer.music.load(link)
    pygame.mixer.music.play(9**9)
    SirenaNowPlaying = True
    end = NowInSec() + sec


def MusicOff():
    global MusicPlaying
    MusicPlaying = False


def Refresh():
    global SirenaNowPlaying, SirenaPlayed, end, MusicPlaying
    try:
        if alarmNotification:
            Is_Alarm = IsAlarm(city)
            print(Is_Alarm,r.get() == 1,not SirenaPlayed,not SirenaNowPlaying)
            if Is_Alarm and r.get() == 1 and not SirenaPlayed and not SirenaNowPlaying: # Тривога
                SirenaPlay("Sound/sirena.mp3", int(t1*60))
            elif not Is_Alarm and r.get() == 1 and SirenaPlayed and not SirenaNowPlaying: # Відбій
                SirenaPlay("Sound/vdbj.mp3", 21)
            elif Is_Alarm and not SirenaNowPlaying and r.get() == 2: # Сирена
                SirenaPlay("Sound/sirena.mp3")
            elif not Is_Alarm and SirenaNowPlaying and r.get() == 2:
                pygame.mixer.music.stop()
                SirenaNowPlaying = False
                SirenaPlayed = False
    except:
        print("Помилка з'єднання!!")
    if SirenaNowPlaying and r.get() == 1 and NowInSec() > end:
        pygame.mixer.music.stop()
        SirenaNowPlaying = False
        SirenaPlayed = not SirenaPlayed
    if datetime.datetime.now().hour == 9 and datetime.datetime.now().minute == 0 and not MusicPlaying and not SirenaNowPlaying and c.get() == 1:
        MusicPlaying = True
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Sound/hvilina.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.queue("Sound/gimn.mp3")
        root.after(61000, MusicOff)

    root.after(2000, Refresh)


locFrame = Frame(root)
alarmFrame = Frame(root)
locFrame.grid(row=0, column=0, padx=10, pady=10, sticky="W")
alarmFrame.grid(row=1, column=0, padx=10, pady=10, sticky="W")

lb_region = Label(locFrame, text="Область", font="Impact 14")
lb_timeAlarm = Label(alarmFrame, text="Довжина сирени", font="Impact 16")
lb_additionalFunc = Label(alarmFrame, text="Додаткові функції", font="Impact 16")
lb_copyright = Label(root, text="© 2022, Кір'янчук Юрій")
lb_region.grid(row=0, column=0, sticky="W", padx=5)
lb_timeAlarm.grid(row=2, column=0, sticky="W", padx=5, pady=(30, 0))
lb_additionalFunc.grid(row=6, column=0, sticky="W", padx=5, pady=(30, 0))
lb_copyright.grid(row=2, column=0, padx=10, pady=(50, 10), sticky="W")

regions_list = ttk.Combobox(locFrame, state="readonly", width=len(max(regions, key=len)), font="Arial 14", values=regions)
regions_list.grid(row=0, column=1, sticky="W", padx=5)
regions_list.current(regions.index(city))

enableAlarm = Button(alarmFrame, background="pink", text="Сповіщення вимкнені", font="Arial 14")
ConfigTimeAlarm = Button(alarmFrame, text="Змінити час тривоги", font="Arial 10", command=ChangeTimeAlarm)
ConfigTimeAlarm.grid(row=3, column=1, sticky="W", padx=5)
enableAlarm.grid(row=0, column=0, sticky="W", padx=5)

timeAlarm1 = Radiobutton(alarmFrame, variable=r, value=1, text=f"Оголошення - {t1} хвилин", font="Arial 14", command=save)
timeAlarm2 = Radiobutton(alarmFrame, variable=r, value=2, text="Від початку до кінця", font="Arial 14", command=save)
minuteCheckBox = Checkbutton(alarmFrame, variable=c, text="Хвилина мовчання і гімн України", font="Arial 14", command=save)
autoOnCheckBox = Checkbutton(alarmFrame, variable=q, text="Ввімкнення сповіщень при запуску програми", font="Arial 14", command=save)
autoStartUpCheckBox = Checkbutton(alarmFrame, variable=w, text="Автозапуск", font="Arial 14", command=autoStartUp)
timeAlarm1.grid(row=3, column=0, sticky="W", padx=5)
timeAlarm2.grid(row=4, column=0, sticky="W", padx=5)
minuteCheckBox.grid(row=7, column=0, sticky="W", padx=5)
autoOnCheckBox.grid(row=8, column=0, sticky="W", padx=5)
autoStartUpCheckBox.grid(row=9, column=0, sticky="W", padx=5)


regions_list.bind("<<ComboboxSelected>>", ComboChange)
enableAlarm.bind("<Button-1>", AlarmNotification)

if q.get() == 1:
    AlarmNotification(None)

Refresh()
root.mainloop()
