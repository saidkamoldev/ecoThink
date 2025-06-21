from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina import held_keys
from resources import Resurslar
from buildings3d import qurilmalar
from ui import UI
import random

def start_game():
    TRANSPARENT = color.rgba(0, 0.8, 0, 0.5)
    global resurslar, obyektlar, building_mode, preview_building, selected_building, player, ui, ishlatilgan_joylar
    resurslar = Resurslar()
    obyektlar = []
    ishlatilgan_joylar = set()
    building_mode = False
    preview_building = None
    selected_building = None

    # O'yin maydonini yaratish - kichiklashtirilgan
    ground = Entity(
        model='plane',
        scale=(100, 1, 100),  # 200 → 100 (2 barobar kichik)
        color=color.rgba(0.7, 0.7, 0.4, 1),
        texture='white_cube',
        texture_scale=(100, 100),  # Texture ni ham kichiklashtirdik
        collider='box'
    )
    
    # Devorlar - kichiklashtirilgan
    for x in [-50, 50]:  # -100, 100 → -50, 50
        wall = Entity(
            model='cube',
            color=color.rgba(1,1,1,0.2),
            scale=(1,15,100),  # Balandlikni o'rtacha qildik
            position=(x,7.5,0),  # Balandlikni o'rtacha qildik
            collider='box'
        )
    for z in [-50, 50]:  # -100, 100 → -50, 50
        wall = Entity(
            model='cube',
            color=color.rgba(1,1,1,0.2),
            scale=(100,15,1),  # Balandlikni o'rtacha qildik
            position=(0,7.5,z),  # Balandlikni o'rtacha qildik
            collider='box'
        )
    
    floor = Entity(
        model='plane',
        scale=(200,1,200),  # 400 → 200
        y=-0.5,
        collider='box',
        visible=False
    )

    def random_joylashuv_topish():
        """Random joylashuv topish algoritmi - kichiklashtirilgan maydon uchun"""
        max_urunishlar = 500  # Urunishlar sonini kamaytirdik
        urunish = 0
        
        while urunish < max_urunishlar:
            # Random joylashuv - kichiklashtirilgan maydon
            x = random.uniform(-45, 45)  # -90, 90 → -45, 45
            z = random.uniform(-45, 45)  # -90, 90 → -45, 45
            
            # Grid ga moslashtirish (3 birlik masofada)
            x = round(x / 3) * 3
            z = round(z / 3) * 3
            joylashuv = (x, z)
            
            # Agar bu joy ishlatilmagan bo'lsa
            if joylashuv not in ishlatilgan_joylar:
                return Vec3(x, 0, z)
            
            urunish += 1
        
        # Agar random joy topilmasa, grid bo'ylab qidirish - kichiklashtirilgan
        for x in range(-45, 46, 3):  # -90, 91 → -45, 46
            for z in range(-45, 46, 3):  # -90, 91 → -45, 46
                joylashuv = (x, z)
                if joylashuv not in ishlatilgan_joylar:
                    return Vec3(x, 0, z)
        
        return None

    def qurish(qurilma):
        global building_mode, preview_building, selected_building
        if resurslar.pul >= qurilma['narx']:
            # Random joylashuv topish
            joylashuv = random_joylashuv_topish()
            if joylashuv:
                try:
                    # Yangi obyekt yaratish
                    new_building = qurilma['model_func']()
                    new_building.position = joylashuv
                    
                    # Ishlatilgan joyni saqlash
                    joylashuv_tuple = (joylashuv.x, joylashuv.z)
                    ishlatilgan_joylar.add(joylashuv_tuple)
                    obyektlar.append(new_building)
                    
                    print(f"[LOG] Yangi {qurilma['nom']} random joylashuvda qurildi: {new_building.position}")
                    print(f"[DEBUG] Grid joylashuv: ({joylashuv.x}, {joylashuv.z})")
                    print(f"[DEBUG] Ishlatilgan joylar soni: {len(ishlatilgan_joylar)}")
                    
                    # Resurslarni yangilash - yangi tizim
                    resurslar.resurs_qoshish(qurilma)
                    
                    # UI yangilashini majburiy qilish
                    ui.update_ui()
                    
                    # Debug uchun UI qiymatlarini ko'rsatish
                    print(f"[DEBUG] UIdagi pul: {ui.resurslar.pul}, energiya: {ui.resurslar.energiya}, suv: {ui.resurslar.suv}")
                    
                    ui.show_message(f"{qurilma['nom']} random joylashuvda qurildi!", color.green)
                except Exception as e:
                    print(f"[ERROR] Qurishda xatolik: {e}")
            else:
                print("[LOG] Bo'sh joy topilmadi!")
                ui.show_message("Bo'sh joy topilmadi!", color.red)
        else:
            print("[LOG] Yetarli pul yo'q!")
            ui.show_message("Yetarli mablag' mavjud emas!", color.red)

    def qurish_mumkinmi(position):
        """Qurish mumkinligini tekshirish - kichiklashtirilgan maydon uchun"""
        # Grid ga moslashtirish (3 birlik masofada)
        x = round(position.x / 3) * 3
        z = round(position.z / 3) * 3
        
        # Chegaradan tashqarida tekshirish - kichiklashtirilgan
        if abs(x) > 48 or abs(z) > 48:  # 98 → 48
            return False
        
        # Ishlatilgan joylarni tekshirish
        joylashuv_tuple = (x, z)
        if joylashuv_tuple in ishlatilgan_joylar:
            return False
        
        return True

    def kamera_yordamchisi():
        # Q va E tugmalari bilan aylanish - kuchaytirilgan
        if held_keys.get('q', False):
            player.camera_pivot.rotate_y(-3)  # 2 → 3 (tezroq aylanish)
        if held_keys.get('e', False):
            player.camera_pivot.rotate_y(3)   # 2 → 3 (tezroq aylanish)
        
        # R tugmasi bilan kamera pozitsiyasini tiklash
        if held_keys.get('r', False):
            player.camera_pivot.rotation = (0, 0, 0)
            player.position = (0, 2, -20)
        
        # F tugmasi bilan yuqoridan ko'rish - kuchaytirilgan
        if held_keys.get('f', False):
            player.camera_pivot.rotation = (90, player.camera_pivot.rotation_y, 0)
            player.y = 120  # 80 → 120 (kengroq ko'rish)
        
        # G tugmasi bilan juda yuqoridan ko'rish - kuchaytirilgan
        if held_keys.get('g', False):
            player.camera_pivot.rotation = (90, player.camera_pivot.rotation_y, 0)
            player.y = 200  # 150 → 200 (kengroq ko'rish)
        
        # T tugmasi bilan kamera balandligini oshirish
        if held_keys.get('t', False):
            player.y += 1
        # Y tugmasi bilan kamera balandligini kamaytirish
        if held_keys.get('y', False):
            player.y -= 1

    def update():
        global building_mode, preview_building
        ui.update_ui()
        
        # Kamera yordamchisi
        kamera_yordamchisi()

        if hasattr(player, 'position'):
            # O'yinchi yer ostiga tushib qolsa
            if player.y < -10:
                player.position = (0, 5, 0)
            # O'yinchi chegaradan tashqariga chiqib ketsa - kichiklashtirilgan
            if abs(player.x) > 49 or abs(player.z) > 49:  # 99 → 49
                player.x = clamp(player.x, -49, 49)
                player.z = clamp(player.z, -49, 49)

    def bekor_qilish():
        global building_mode, preview_building, selected_building
        building_mode = False
        if preview_building:
            destroy(preview_building)
        preview_building = None
        selected_building = None
        mouse.locked = True
        mouse.visible = False
        print('[LOG] Qurilish rejimidan chiqildi')

    def input_func(key):
        global building_mode, preview_building, selected_building
        
        if key == 'escape':
            mouse.locked = not mouse.locked
            mouse.visible = not mouse.visible

    # O'yinchi yaratish - yaxshilangan kamera boshqaruvi
    player = FirstPersonController(
        position=(0, 2, -20),
        speed=15,  # Tezlikni oshirdik
        jump_height=4,  # Sakrash balandligini oshirdik
        gravity=0.8,
        mouse_sensitivity=Vec2(100, 100),  # Mouse sezgirligini kuchaytirdik
        rotation_speed=300,  # Aylanish tezligini oshirdik
        max_zoom=60,  # Zoom chegarasini oshirdik
        min_zoom=1,  # Minimal zoom ni kamaytirdik
        zoom_speed=4,  # Zoom tezligini oshirdik
        field_of_view=130  # Ko'rish maydonini kengaytirdik
    )
    player.collider = 'box'
    
    # Kamera cheklovlarini olib tashlash - to'liq 360 gradus
    player.camera_pivot.rotation_speed = 400
    player.camera_pivot.max_rotation_x = 180  # Yuqori cheklovni oshirdik
    player.camera_pivot.min_rotation_x = -180  # Pastki cheklovni oshirdik
    
    ground.name = 'ground'

    # Yorug'lik va osmon - kichiklashtirilgan
    pivot = Entity()
    DirectionalLight(parent=pivot, y=3, z=3, shadows=True, rotation=(45, -45, 0))  # Yorug'likni kamaytirdik
    AmbientLight(color=color.rgba(120, 120, 120, 0.15))  # Ambient yorug'likni kamaytirdik
    Sky()

    # UI yaratish
    global ui
    ui = UI(resurslar=resurslar, qurilmalar=qurilmalar, qurish_func=qurish)

    # O'yinni kursor bilan boshlash
    mouse.locked = False
    mouse.visible = True

    # Update va input funksiyalarini bog'lash
    application.update = update
    application.input = input_func