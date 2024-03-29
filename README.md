# Повітряна тривога
Програма для увімкнення повітряної тривоги.

## Встановлення
1. Завантажити python 3.8 (вищі версії не підтримуються Windows 7) з сайту [python](https://www.python.org/downloads/release/python-3810/) і встановити
2. Установити залежності (для цього потрібно відкрити термінал і ввести `pip install -r requirements.txt`)

## Запуск
Для роботи програми необхідно:
1. Підключити до комп'ютера гучномовець чи інший пристрій для програвання аудіо
2. Забезпечити комп'ютер доступом до мережі Інтернет.
3. Щоб запустити програму виконайте команду `python src/airalarm.py`

## Збірка
Щоб створити збірку для Windows з директорії репозиторія виконайте команду
```build.bat 0.0.0```
де `0.0.0` - це бажана версія збірки.
Щоб створити збірку для linux з директорії репозиторія виконайте команду
```build.sh 0.0.0```

## Передісторія
По всій Україні лунають повітряні тривоги і в нашій школі в тому числі. Але так як її запускає людина, вона тратить свій час. Тому ми вирішили автоматизувати цей процес, створивши цю програму.

## Функції
### Основні функції
* При повітряній тривозі сирена лунає 10 хвилин за замовчуванням (можна змінити, щоб лунала до кінця повітряної тривоги)
* При закінченні повітряної тривоги лунає голосове сповіщення про її закінчення

### Додаткові функції
* О 9:00 лунає хвилина мовчання
* О 9:01 лунає лімн України
* Автоввімкнення сповіщень про повітряню тривогу
* Автозапуск програми при старті Операційної Системи

## Про роботу програми
Інформація про сигнал повітряної тривоги даною програмою береться із api який надав сайт [https://alerts.com.ua/](https://alerts.com.ua/)
