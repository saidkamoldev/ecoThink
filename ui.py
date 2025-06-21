from ursina import *
from textwrap import dedent

class UI(Entity):
    def __init__(self, resurslar, qurilmalar, qurish_func):
        super().__init__(parent=camera.ui)

        self.resurslar = resurslar
        self.qurilmalar = qurilmalar
        self.qurish_func = qurish_func

        # Resurslar paneli
        self.resurslar_panel = Entity(parent=self, model='quad', scale=(0.35, 0.25), position=window.top_left + Vec2(0.01, -0.01), color=color.rgba(0,0,0,0.7))
        self.resurslar_text = Text(parent=self.resurslar_panel, text=self.resurslar.update_text(), origin=(-0.5, 0.5), position=(-0.45, 0.45), scale=1.2)

        # Qurilish menyusi
        self.qurilish_menyusi = Entity(parent=self, position=window.top_right + Vec2(-0.05, -0.05))
        for i, qurilma in enumerate(self.qurilmalar):
            b = Button(
                parent=self.qurilish_menyusi,
                text=f"{qurilma['nom']} <scale:0.8><gold>({qurilma['narx']}$)",
                color=color.dark_gray.tint(.2),
                highlight_color=color.azure.tint(.2),
                position=(0, -i * 0.07),
                scale=(0.25, 0.06),
                on_click=Func(self.qurish_func, qurilma)
            )
            b.text_entity.font = 'VeraMono.ttf'

        # Yordam oynasi
        self.yordam_button = Button(parent=self, text='?', position=window.bottom_right - Vec2(0.05, -0.05), scale=0.05, color=color.orange, text_origin=(0,0))
        self.yordam_oynasi = Entity(parent=camera.ui, model='quad', color=color.rgba(0,0,0,0.8), scale=(0.7, 0.6), enabled=False)
        Text(parent=self.yordam_oynasi,
             text=dedent('''
                <orange>Boshqarish</orange>
                <white>WASD</white> - Harakatlanish
                <white>SPACE</white> - Sakrash
                <white>ESC</white> - Kursor/Menyu
                <white>Bino tugmasi</white> - Avtomatik qurish
             ''').strip(),
             origin=(0,0),
             scale=1.2
        )
        self.yordam_button.on_click = self.toggle_yordam

        # Ekologiya indikatori
        self.ekologiya_panel = Entity(parent=self, model='quad', scale=(0.4, 0.08), position=(0, 0.45), color=color.rgba(0,0,0,0.7))
        self.ekologiya_text = Text(parent=self.ekologiya_panel, text="Ekologiya: 100%", origin=(0,0.2), scale=1.5)
        self.ekologiya_bar_bg = Entity(parent=self.ekologiya_panel, model='quad', scale=(0.95, 0.3), position=(0, -0.15), color=color.black33)
        self.ekologiya_bar = Entity(parent=self.ekologiya_bar_bg, model='quad', scale=(1, 1), color=color.green, origin=(-.5, 0))

    def update_ui(self):
        self.resurslar_text.text = self.resurslar.update_text()
        
        # Ekologiya holatini hisoblash
        ekologiya_foiz = max(0, 100 - self.resurslar.ifloslanish * 5 + self.resurslar.daraxtlar * 2)
        self.ekologiya_text.text = f"Ekologiya: {ekologiya_foiz:.0f}%"
        
        if ekologiya_foiz > 70:
            self.ekologiya_bar.color = color.green
        elif ekologiya_foiz > 30:
            self.ekologiya_bar.color = color.yellow
        else:
            self.ekologiya_bar.color = color.red
        
        self.ekologiya_bar.scale_x = ekologiya_foiz / 100

    def toggle_yordam(self):
        self.yordam_oynasi.enabled = not self.yordam_oynasi.enabled

    def show_message(self, text, color=color.white, duration=3):
        message = Text(text=text, parent=camera.ui, origin=(0,0), y=-0.4, scale=1.5, color=color)
        message.fade_out(duration=1, delay=duration-1)