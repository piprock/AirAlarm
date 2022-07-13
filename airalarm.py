import requests
import pygame
import datetime
from time import sleep

def IsAlarm(City):
    while True:
        try:
            CitiesWithAlarm = requests.get("https://alarmmap.online/assets/json/_alarms/siren.json").json()
            for i in CitiesWithAlarm:
                if i["district"] == City:
                    return True
            return False
        except:
            pass # Помилка сервера

def NowInSec():
    return int((datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds())

def PlaySirena(link, TimePlaying):
    pygame.mixer.music.stop()
    end = NowInSec() + TimePlaying
    while NowInSec() < end:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(link)
            pygame.mixer.music.play()
    pygame.mixer.music.stop()

def PlayAudio(link, loops=1):
    pygame.mixer.music.load(link)
    pygame.mixer.music.play(loops)

pygame.init()
SirenaPlayed = False
City = "Рівненська_область" # Рівненська_область

while True:
    sleep(5)
    isAlarm = IsAlarm(City)
    TimeNow = datetime.datetime.now()
    if isAlarm and not SirenaPlayed:
        SirenaPlayed = True
        PlaySirena('Sound/sirena.mp3', 2)
    elif not isAlarm and SirenaPlayed:
        SirenaPlayed = False
        PlaySirena('Sound/sirena.mp3', 10)
    elif TimeNow.hour == 9 and TimeNow.minute == 0:
        PlayAudio('Sound/hvilina.mp3')
        PlayAudio('Sound/gimn.mp3')


pygame.quit()
