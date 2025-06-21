from ursina import *
from textwrap import dedent

class UI(Entity):
    def __init__(self, resurslar, qurilmalar, qurish_func):
        super().__init__(parent=camera.ui)

        self.resurslar = resurslar
        self.qurilmalar = qurilmalar
        self.qurish_func = qurish_func

        # Zamonaviy pul mablag'i paneli
        self.pul_panel = Entity(
            parent=self, 
            model='quad', 
            scale=(0.3, 0.1), 
            position=window.top_left + Vec2(0.02, -0.02), 
            color=color.rgba(0, 0.8, 0, 0.9),
            texture='white_cube'
        )
        # Pul paneli uchun gradient effekt
        self.pul_gradient = Entity(
            parent=self.pul_panel,
            model='quad',
            scale=(1, 1),
            color=color.rgba(0, 1, 0, 0.3),
            position=(0, 0, -0.01)
        )
        self.pul_text = Text(
            parent=self.pul_panel, 
            text=f"💰 {self.resurslar.pul:,}$", 
            origin=(0, 0), 
            position=(0, 0), 
            scale=1.5, 
            color=color.white,
            font='VeraMono.ttf'
        )

        # Zamonaviy ekologik balans paneli
        self.ekologiya_panel = Entity(
            parent=self, 
            model='quad', 
            scale=(0.5, 0.12), 
            position=(0, 0.4), 
            color=color.rgba(0, 0, 0, 0.8),
            texture='white_cube'
        )
        # Ekologiya paneli uchun gradient
        self.ekologiya_gradient = Entity(
            parent=self.ekologiya_panel,
            model='quad',
            scale=(1, 1),
            color=color.rgba(0, 0.5, 0, 0.4),
            position=(0, 0, -0.01)
        )
        self.ekologiya_text = Text(
            parent=self.ekologiya_panel, 
            text="🌱 Ekologiya: 100%", 
            origin=(0, 0.3), 
            scale=1.3,
            color=color.white,
            font='VeraMono.ttf'
        )
        self.ekologiya_bar_bg = Entity(
            parent=self.ekologiya_panel, 
            model='quad', 
            scale=(0.9, 0.25), 
            position=(0, -0.2), 
            color=color.rgba(0.2, 0.2, 0.2, 0.8)
        )
        self.ekologiya_bar = Entity(
            parent=self.ekologiya_bar_bg, 
            model='quad', 
            scale=(1, 1), 
            color=color.green, 
            origin=(-.5, 0)
        )

        # Zamonaviy resurslar paneli
        self.resurslar_panel = Entity(
            parent=self, 
            model='quad', 
            scale=(0.45, 0.35), 
            position=window.top_left + Vec2(0.02, -0.15), 
            color=color.rgba(0, 0, 0, 0.85),
            texture='white_cube'
        )
        # Resurslar paneli uchun gradient
        self.resurslar_gradient = Entity(
            parent=self.resurslar_panel,
            model='quad',
            scale=(1, 1),
            color=color.rgba(0.1, 0.1, 0.1, 0.5),
            position=(0, 0, -0.01)
        )
        self.resurslar_text = Text(
            parent=self.resurslar_panel, 
            text=self.resurslar.update_text(), 
            origin=(-0.5, 0.5), 
            position=(-0.4, 0.4), 
            scale=1.2,
            color=color.white,
            font='VeraMono.ttf'
        )

        # Zamonaviy qurilish menyusi
        self.qurilish_menyusi = Entity(parent=self, position=window.top_right + Vec2(-0.05, -0.05))
        for i, qurilma in enumerate(self.qurilmalar):
            # Zamonaviy qurilish tugmasi
            b = Button(
                parent=self.qurilish_menyusi,
                text=f"🏗️ {qurilma['nom']}\n💰 {qurilma['narx']:,}$",
                color=color.rgba(0.2, 0.2, 0.2, 0.9),
                highlight_color=color.rgba(0.3, 0.6, 1, 0.9),
                position=(0, -i * 0.08),
                scale=(0.28, 0.07),
                on_click=Func(self.qurish_func, qurilma)
            )
            b.text_entity.font = 'VeraMono.ttf'
            b.text_entity.scale = 0.9

        # Zamonaviy yordam tugmasi
        self.yordam_button = Button(
            parent=self, 
            text='❓', 
            position=window.bottom_right - Vec2(0.06, -0.06), 
            scale=0.06, 
            color=color.rgba(1, 0.6, 0, 0.9),
            text_origin=(0,0)
        )
        self.yordam_oynasi = Entity(
            parent=camera.ui, 
            model='quad', 
            color=color.rgba(0, 0, 0, 0.9), 
            scale=(0.8, 0.7), 
            enabled=False
        )
        Text(
            parent=self.yordam_oynasi,
            text=dedent('''
                <orange>🎮 O'YIN BOSHQARUVI</orange>
                
                <white>WASD</white> - Harakatlanish
                <white>SPACE</white> - Sakrash
                <white>ESC</white> - Kursor/Menyu
                <white>🏗️ Bino tugmasi</white> - Avtomatik qurish
                
                <orange>📷 KAMERA BOSHQARUVI</orange>
                <white>Mouse</white> - Kamera aylanishi (360°)
                <white>Q/E</white> - Chap/O'ng aylanish
                <white>R</white> - Kamera pozitsiyasini tiklash
                <white>F</white> - Yuqoridan ko'rish (120m)
                <white>G</white> - Juda yuqoridan ko'rish (200m)
                <white>T/Y</white> - Balandlikni oshirish/kamaytirish
                
                <orange>🌍 MAYDON HAQIDA</orange>
                <white>Maydon o'lchami: 100x100 birlik</white>
                <white>Ko'rish maydoni: 110 gradus</white>
                <white>To'liq 360° aylanish</white>
             ''').strip(),
            origin=(0,0),
            scale=1.1,
            font='VeraMono.ttf'
        )
        self.yordam_button.on_click = self.toggle_yordam

    def update_ui(self):
        # Pul mablag'ini yangilash
        self.pul_text.text = f"💰 {self.resurslar.pul:,}$"
        
        # Resurslarni yangilash
        self.resurslar_text.text = self.resurslar.update_text()
        
        # Ekologiya holatini hisoblash va yangilash
        ekologiya_foiz = max(0, 100 - self.resurslar.ifloslanish * 5 + self.resurslar.daraxtlar * 2)
        self.ekologiya_text.text = f"🌱 Ekologiya: {ekologiya_foiz:.0f}%"
        
        # Ekologiya rangini yangilash
        if ekologiya_foiz > 70:
            self.ekologiya_bar.color = color.green
            self.ekologiya_gradient.color = color.rgba(0, 0.8, 0, 0.3)
        elif ekologiya_foiz > 30:
            self.ekologiya_bar.color = color.yellow
            self.ekologiya_gradient.color = color.rgba(1, 1, 0, 0.3)
        else:
            self.ekologiya_bar.color = color.red
            self.ekologiya_gradient.color = color.rgba(1, 0, 0, 0.3)
        
        self.ekologiya_bar.scale_x = ekologiya_foiz / 100

    def toggle_yordam(self):
        self.yordam_oynasi.enabled = not self.yordam_oynasi.enabled

    def show_message(self, text, color=color.white, duration=3):
        message = Text(
            text=text, 
            parent=camera.ui, 
            origin=(0,0), 
            y=-0.4, 
            scale=1.5, 
            color=color,
            font='VeraMono.ttf'
        )
        message.fade_out(duration=1, delay=duration-1)