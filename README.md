# EkoShahar Quruvchi (MVP)

Bu loyiha ekologik shahar qurilishi va boshqaruvi bo'yicha oddiy simulyatsiya dasturidir. Dastur Python tilida yozilgan va konsolda ishlaydi.

## Ishga tushirish

1. Python 3 o'rnatilganligiga ishonch hosil qiling.
2. Konsolda quyidagilarni yozing:

```
py main.py
```

## Asosiy imkoniyatlar
- Shahar resurslarini boshqarish (pul, energiya, suv, daraxtlar, ifloslanish)
- Turli obyektlarni qurish (uy, bog', zavod, quyosh paneli, suv minorasi)
- Shahar holatini ko'rish

## Foydalanish
1. Dastur ishga tushgach, menyudan kerakli amalni tanlang:
    - 1: Shahar holatini ko'rish
    - 2: Qurilma qurish
    - 3: Dasturdan chiqish
2. Qurilma qurishda ro'yxatdan birini tanlang va shahar resurslari yangilanadi.

Savollar bo'lsa, bemalol so'rang! 

from ursina import *
import random

app = Ursina()

window.title = 'EkoShahar Quruvchi 3D'
window.borderless = False

ground = Entity(model='plane', scale=(20,1,20), color=color.green, collider='box')

def build_house():
    house = Entity(model='cube', color=color.brown, position=(random.randint(-9,9),0.5,random.randint(-9,9)), scale=(1,1,1))

button = Button(text='Uy qurish', color=color.azure, position=(0.7,0.45), scale=(0.2,0.1))
button.on_click = build_house

EditorCamera()

app.run() 