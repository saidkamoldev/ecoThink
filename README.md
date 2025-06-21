# ecoThink - 3D Ekologik Shahar Qurish O'yini

Bu 3D o'yin Ursina engine yordamida yaratilgan bo'lib, o'yinchilar ekologik shahar qurish orqali resurslarni boshqarish va atrof-muhitni himoya qilishni o'rganadi.

## O'rnatish

1. Python 3.8+ o'rnatilgan bo'lishi kerak
2. Kerakli kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

## O'yinni ishga tushirish

```bash
python main3d.py
```

## O'yin boshqaruvi

- **WASD** - Harakatlanish
- **SPACE** - Sakrash
- **ESC** - Kursor/Menyu
- **O'ng tugma** - Bino qurish
- **Chap tugma** - Qurilishni bekor qilish
- **?** - Yordam oynasi

## O'yin elementlari

### Qurilmalar:
1. **Uy** (1200$) - Aholi uchun
2. **Zavod** (3500$) - Ishlab chiqarish
3. **Daraxt** (200$) - Ekologiya
4. **Quyosh Paneli** (1800$) - Energiya
5. **Suv Minorasi** (1500$) - Suv ta'minoti

### Resurslar:
- **Pul** - Qurilish uchun
- **Energiya** - Shahar uchun
- **Suv** - Aholi uchun
- **Daraxtlar** - Ekologiya uchun
- **Ifloslanish** - Atrof-muhit holati

## Xususiyatlar

- ✅ 3D muhit
- ✅ Real vaqtda resurs boshqaruvi
- ✅ Ekologiya indikatori
- ✅ 3D modellar (.obj formatida)
- ✅ Random joylashuv algoritmi
- ✅ O'zaro to'qnashuvlarni oldini olish
- ✅ Optimallashtirilgan ishlash

## Fayl tuzilishi

```
ecoThink/
├── main3d.py          # Asosiy dastur
├── game3d.py          # O'yin logikasi
├── buildings3d.py     # Bino modellari
├── ui.py              # Foydalanuvchi interfeysi
├── resources.py       # Resurs boshqaruvi
├── models/            # 3D modellar
│   ├── Bambo_House.obj
│   ├── zavod.obj
│   ├── solar_panels.obj
│   └── daraxt.obj
└── requirements.txt   # Kerakli kutubxonalar
```

## Muammolarni hal qilish

Agar o'yin ishlamasa:
1. Python versiyasini tekshiring (3.8+)
2. Kerakli kutubxonalarni o'rnatganingizni tekshiring
3. `models` papkasida .obj fayllar borligini tekshiring

## Rivojlantirish

O'yinni rivojlantirish uchun:
1. Yangi bino turlarini `buildings3d.py` ga qo'shing
2. Yangi 3D modellarni `models/` papkasiga qo'shing
3. UI elementlarini `ui.py` da o'zgartiring

## Litsenziya

Bu loyiha ochiq manbaa hisoblanadi. 