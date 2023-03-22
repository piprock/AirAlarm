import datetime
import json
import logging.handlers
import sys
from pathlib import Path
from tkinter import *
from tkinter import ttk
from urllib.request import Request, urlopen

import pygame

import autostart
import regions
from storage import State

LOG_FILENAME = "airalarm.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    RUNNING_FILE = sys.executable
else:
    # Running in a normal Python process
    RUNNING_FILE = __file__
BASE_PATH = Path(RUNNING_FILE).parent / "data"
SETTINGS_PATH = BASE_PATH / "settings.txt"
ICONS_PATH = BASE_PATH / "icons"


def ComboChange(event):
    STATE.region_name = regionsCombobox.get()
    save()


def save():
    with SETTINGS_PATH.open("r", encoding="utf-8") as f:
        settings = eval(f.read())
    with SETTINGS_PATH.open("w", encoding="utf-8") as f:
        settings["city"] = regions.IDS[STATE.region_name]
        settings["c"] = is_minute_enabled.get()
        settings["r"] = mode.get()
        settings["q"] = autoenable_notifications.get()
        settings["w"] = w.get()
        settings["t1"] = t1
        print(settings, file=f)


def autoStartUp():
    if w.get() == 0:
        autostart.disable()
    elif w.get() == 1:
        autostart.enable()
    save()


def switch_notification(event):
    pygame.mixer.music.stop()
    STATE.SirenaPlayed = False
    STATE.SirenaNowPlaying = False
    STATE.MusicPlaying = False
    button = event.widget
    if STATE.alarmNotification == 0:
        STATE.alarmNotification = 1
        STATE.reset_test_alarm()
        try:
            # It is used to destroy window with time adjustment when this window is open and clicked button to enable
            # alarm
            app.destroy()
        except:
            pass
        button.config(background="lime", text="Сповіщення ввімкнені")
        timeAlarm1.config(state="disabled")
        timeAlarm2.config(state="disabled")
        regionsCombobox.config(state="disabled")
        minuteCheckBox.config(state="disabled")
        ConfigTimeAlarm.config(state="disabled")
        autoOnCheckBox.config(state="disabled")
        autoStartUpCheckBox.config(state="disabled")

    else:
        STATE.alarmNotification = 0
        button.config(background="pink", text="Сповіщення вимкнені")
        timeAlarm1.config(state="normal")
        timeAlarm2.config(state="normal")
        regionsCombobox.config(state="read")
        minuteCheckBox.config(state="normal")
        ConfigTimeAlarm.config(state="normal")
        autoOnCheckBox.config(state="normal")
        autoStartUpCheckBox.config(state="normal")


def IsAlarm(City):
    if City == regions.TEST_NAME:
        return STATE.is_test_alarm()
    request = Request(
        "https://alerts.com.ua/api/states",
        headers={"X-API-Key": "95d44c372a0ff7220475e373ece7e0ac3362bfdc"},
    )
    with urlopen(request) as response:
        data = json.load(response)
    states = data["states"]
    for state in states:
        if state["name"] == City and state["alert"]:
            return True
    return False


def NowInSec():
    return int((datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds())


def save_time(entr1):
    global t1
    try:
        t1 = int(float(entr1.get())) if int(float(entr1.get())) == float(entr1.get()) else float(entr1.get())
        save()
        timeAlarm1.config(text=f"Оголошення - {t1} хвилин")
        app.destroy()
    except:
        but.config(text="Помилка")
        root.after(400, lambda: but.config(text="Зберегти"))


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
    frame.grid(pady=10, padx=10)
    lb1 = Label(frame, text="Оголошення: ", font="Arial 12")
    lb1.grid(row=0, column=0)
    but = Button(frame, text="Зберегти", font="Arial 12", command=lambda: save_time(entr1))
    but.grid()

    entr1 = Entry(frame, width=8)
    entr1.grid(row=0, column=1)

    app.mainloop()


root = Tk()
root.title("Повітряна тривога")
root.resizable(width=False, height=False)
root.wm_iconphoto(True, *(PhotoImage(file=path) for path in ICONS_PATH.iterdir()))
pygame.init()

with SETTINGS_PATH.open("r", encoding="utf-8") as f:
    settings = eval(f.read())

mode = IntVar()
mode.set(settings["r"])
is_minute_enabled = IntVar()
is_minute_enabled.set(settings["c"])
autoenable_notifications = IntVar()
autoenable_notifications.set(settings["q"])
w = IntVar()
w.set(settings["w"])
STATE = State(regions.NAMES[settings["city"]])
t1 = settings["t1"]
lengthVdbj = int(pygame.mixer.Sound(BASE_PATH / "Sound/vdbj.mp3").get_length())


def SirenaPlay(link, sec=1, count=-1):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(link)
    pygame.mixer.music.play(count)
    STATE.SirenaNowPlaying = True
    STATE.end = NowInSec() + sec


def MusicOff():
    STATE.MusicPlaying = False


def Refresh():
    try:
        if STATE.alarmNotification:
            Is_Alarm = IsAlarm(STATE.region_name)
            logger.debug("Are authorities signalling about air alarm now: %s", Is_Alarm)
            logger.debug("Playing siren in the beginning and in the end mode is enabled: %s", mode.get() == 1)
            logger.debug("Has siren played already: %s", STATE.SirenaPlayed)
            logger.debug("Is siren playing now: %s", STATE.SirenaNowPlaying)
            if Is_Alarm and mode.get() == 1 and not STATE.SirenaPlayed and not STATE.SirenaNowPlaying:  # Тривога
                SirenaPlay(BASE_PATH / "Sound/sirena.mp3", int(t1 * 60))
            elif not Is_Alarm and mode.get() == 1 and STATE.SirenaPlayed and not STATE.SirenaNowPlaying:  # Відбій
                SirenaPlay(BASE_PATH / "Sound/vdbj.mp3", lengthVdbj, 1)
            elif Is_Alarm and not STATE.SirenaNowPlaying and mode.get() == 2:  # Сирена
                SirenaPlay(BASE_PATH / "Sound/sirena.mp3")
            elif not Is_Alarm and STATE.SirenaNowPlaying and mode.get() == 2:
                pygame.mixer.music.stop()
                STATE.SirenaNowPlaying = False
                STATE.SirenaPlayed = False
    except Exception as err:
        logger.exception(err)
    if STATE.SirenaNowPlaying and mode.get() == 1 and NowInSec() > STATE.end:
        pygame.mixer.music.stop()
        STATE.SirenaNowPlaying = False
        STATE.SirenaPlayed = not STATE.SirenaPlayed
    if (
            datetime.datetime.now().hour == 9
            and datetime.datetime.now().minute == 0
            and not STATE.MusicPlaying
            and not STATE.SirenaNowPlaying
            and is_minute_enabled.get() == 1
    ):
        STATE.MusicPlaying = True
        pygame.mixer.music.stop()
        pygame.mixer.music.load(BASE_PATH / "Sound/hvilina.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.queue(BASE_PATH / "Sound/gimn.mp3")
        root.after(61000, MusicOff)

    root.after(2000, Refresh)


locFrame = Frame(root)
alarmFrame = Frame(root)
locFrame.grid(row=0, column=0, padx=10, pady=10, sticky="W")
alarmFrame.grid(row=1, column=0, padx=10, pady=10, sticky="W")

lb_region = Label(locFrame, text="Область", font="Impact 14")
lb_timeAlarm = Label(alarmFrame, text="Довжина сирени", font="Impact 16")
lb_additionalFunc = Label(alarmFrame, text="Додаткові функції", font="Impact 16")
lb_copyright = Label(root, text="© 2023, Кір'янчук Юрій")
lb_region.grid(row=0, column=0, sticky="W", padx=5)
lb_timeAlarm.grid(row=2, column=0, sticky="W", padx=5, pady=(30, 0))
lb_additionalFunc.grid(row=6, column=0, sticky="W", padx=5, pady=(30, 0))
lb_copyright.grid(row=2, column=0, padx=10, pady=(50, 10), sticky="W")

regionsCombobox = ttk.Combobox(
    locFrame,
    state="readonly",
    width=len(max(regions.LIST, key=len)),
    font="Arial 14",
    values=regions.LIST,
)
regionsCombobox.grid(row=0, column=1, sticky="W", padx=5)
regionsCombobox.current(regions.LIST.index(STATE.region_name))

alarmSwitchButton = Button(alarmFrame, background="pink", text="Сповіщення вимкнені", font="Arial 14")
ConfigTimeAlarm = Button(alarmFrame, text="Змінити час тривоги", font="Arial 10", command=ChangeTimeAlarm)
ConfigTimeAlarm.grid(row=3, column=1, sticky="W", padx=5)
alarmSwitchButton.grid(row=0, column=0, sticky="W", padx=5)

timeAlarm1 = Radiobutton(
    alarmFrame,
    variable=mode,
    value=1,
    text=f"Оголошення - {t1} хвилин", font="Arial 14",
    command=save,
)
timeAlarm2 = Radiobutton(alarmFrame, variable=mode, value=2, text="Від початку до кінця", font="Arial 14", command=save)
minuteCheckBox = Checkbutton(
    alarmFrame,
    variable=is_minute_enabled,
    text="Хвилина мовчання і гімн України",
    font="Arial 14",
    command=save,
)
autoOnCheckBox = Checkbutton(
    alarmFrame,
    variable=autoenable_notifications,
    text="Ввімкнення сповіщень при запуску програми",
    font="Arial 14",
    command=save,
)
autoStartUpCheckBox = Checkbutton(alarmFrame, variable=w, text="Автозапуск", font="Arial 14", command=autoStartUp)
timeAlarm1.grid(row=3, column=0, sticky="W", padx=5)
timeAlarm2.grid(row=4, column=0, sticky="W", padx=5)
minuteCheckBox.grid(row=7, column=0, sticky="W", padx=5)
autoOnCheckBox.grid(row=8, column=0, sticky="W", padx=5)
autoStartUpCheckBox.grid(row=9, column=0, sticky="W", padx=5)

regionsCombobox.bind("<<ComboboxSelected>>", ComboChange)
alarmSwitchButton.bind("<Button-1>", switch_notification)

if autoenable_notifications.get() == 1:
    event = Event()
    event.widget = alarmSwitchButton
    switch_notification(event)

Refresh()
root.mainloop()
