from ursina import *
from textwrap import dedent

# Shrift sifatini global darajada oshirish, aniqlik uchun
Text.default_resolution = Text.default_resolution * 2

class UI(Entity):
    def __init__(self, resurslar, qurilmalar, qurish_func):
        super().__init__(parent=camera.ui)

        self.resurslar = resurslar
        self.qurilmalar = qurilmalar
        self.qurish_func = qurish_func

        # 1. YUQORI PANEL (Pul va Ekologiya)
        # Aniq va oddiy, faqat matn va fon bilan
        self.pul_text = Text(
            parent=camera.ui,
            text=f"PUL: {self.resurslar.pul:,}$",
            position=window.top_left + Vec2(0.04, -0.04),
            origin=(-0.5, 0.5),
            scale=2,
            font='VeraMono.ttf',
            background=True
        )

        # Ekologiya paneli yuqori o'ngda
        self.ekologiya_panel = Entity(parent=camera.ui, position=window.top_right + Vec2(-0.04, -0.04), origin=(0.5, 0.5))
        Text(parent=self.ekologiya_panel, text="EKOLOGIYA", origin=(0, 0.5), scale=2, font='VeraMono.ttf')
        self.ekologiya_bar = Entity(
            parent=self.ekologiya_panel,
            model='quad',
            scale=(0.3, 0.04),
            position=(0, -0.05, 0),
            color=color.green,
            origin=(0, 0.5)
        )
        self.ekologiya_foiz = Text(
            parent=self.ekologiya_bar,
            text="100%",
            scale=1.5,
            origin=(0,0),
            color=color.black
        )

        # 2. PASTKI PANEL (Qurilish menyusi)
        # Barcha tugmalar pastda, markazda joylashadi
        bottom_panel = Entity(parent=camera.ui, model='quad', scale=(0.9, 0.14), position=(0, -0.42), color=color.black66)
        
        # Tugmalarni gorizontal joylashtirish
        button_width = 1 / (len(self.qurilmalar) + 1)
        for i, qurilma in enumerate(self.qurilmalar):
            b = Button(
                parent=bottom_panel,
                text=f"{qurilma['nom']}\n({qurilma['narx']:,}$)",
                position=((-0.5 + (i + 1) * button_width) * bottom_panel.scale_x, 0),
                scale=(button_width * 0.9, 0.8),
                on_click=Func(self.qurish_func, qurilma)
            )
            if b.text_entity:
                b.text_entity.line_height = 0.8
                b.text_entity.font = 'VeraMono.ttf'
                b.text_entity.scale *= 0.6


        # 3. CHAP PANEL (Resurslar ro'yxati)
        self.resurslar_text = Text(
            parent=camera.ui,
            text=self.resurslar.update_text(),
            position=window.left + Vec2(0.01, 0.3),
            origin=(-0.5, 0.5),
            scale=1.5,
            font='VeraMono.ttf',
            background=True
        )

        # Yordam oynasi o'z joyida qoladi
        self.yordam_button = Button(
            parent=self, 
            text='?', 
            position=window.bottom_right - Vec2(0.05, -0.05), 
            scale=0.05, 
            text_origin=(0,0)
        )
        self.yordam_button.color = color.orange
        self.yordam_oynasi = Entity(parent=camera.ui, model='quad', color=color.black90, scale=(0.7, 0.6), enabled=False)
        Text(
            parent=self.yordam_oynasi,
            text=dedent('''
                <yellow>O'YIN BOSHQARUVI</yellow>
                WASD - Harakatlanish, SPACE - Sakrash
                <yellow>KAMERA BOSHQARUVI</yellow>
                Mouse - Kamera aylanishi, Q/E - Burilish
                R - Tiklash, F/G - Yuqoridan ko'rish
                T/Y - Balandlikni o'zgartirish
             ''').strip(),
            origin=(0,0),
            scale=1.2,
            font='VeraMono.ttf'
        )
        self.yordam_button.on_click = self.toggle_yordam

    def update_ui(self):
        self.pul_text.text = f"PUL: {self.resurslar.pul:,}$"
        self.resurslar_text.text = self.resurslar.update_text()

        ekologiya_foiz = max(0, 100 - self.resurslar.ifloslanish * 5 + self.resurslar.daraxtlar * 2)
        self.ekologiya_foiz.text = f"{ekologiya_foiz:.0f}%"
        self.ekologiya_bar.scale_x = ekologiya_foiz / 100 * 0.3 # Parent scale'ga moslash
        
        if ekologiya_foiz > 70: self.ekologiya_bar.color = color.green
        elif ekologiya_foiz > 30: self.ekologiya_bar.color = color.yellow
        else: self.ekologiya_bar.color = color.red
        
    def toggle_yordam(self):
        self.yordam_oynasi.enabled = not self.yordam_oynasi.enabled

    def show_message(self, text, text_color=color.white, duration=3):
        message = Text(text=text, parent=camera.ui, origin=(0,0), y=0, scale=2, color=text_color, background=True, font='VeraMono.ttf')
        message.fade_out(duration=0.5, delay=duration-0.5)
        destroy(message, delay=duration)
