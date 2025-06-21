from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
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

    # O'yin maydonini yaratish
    ground = Entity(
        model='plane',
        scale=(100, 1, 100),
        color=color.rgba(0.7, 0.7, 0.4, 1),
        texture='white_cube',
        texture_scale=(100, 100),
        collider='box'
    )
    
    # Devorlar
    for x in [-50, 50]:
        wall = Entity(
            model='cube',
            color=color.rgba(1,1,1,0.2),
            scale=(1,10,100),
            position=(x,5,0),
            collider='box'
        )
    for z in [-50, 50]:
        wall = Entity(
            model='cube',
            color=color.rgba(1,1,1,0.2),
            scale=(100,10,1),
            position=(0,5,z),
            collider='box'
        )
    
    floor = Entity(
        model='plane',
        scale=(200,1,200),
        y=-0.5,
        collider='box',
        visible=False
    )

    def random_joylashuv_topish():
        """Random joylashuv topish algoritmi"""
        max_urunishlar = 500
        urunish = 0
        
        while urunish < max_urunishlar:
            # Random joylashuv
            x = random.uniform(-45, 45)
            z = random.uniform(-45, 45)
            
            # Grid ga moslashtirish (3 birlik masofada)
            x = round(x / 3) * 3
            z = round(z / 3) * 3
            joylashuv = (x, z)
            
            # Agar bu joy ishlatilmagan bo'lsa
            if joylashuv not in ishlatilgan_joylar:
                return Vec3(x, 0, z)
            
            urunish += 1
        
        # Agar random joy topilmasa, grid bo'ylab qidirish
        for x in range(-45, 46, 3):
            for z in range(-45, 46, 3):
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
                    # selected_building atributlarini olish
                    model_func = qurilma['model_func']
                    nom = qurilma['nom']
                    narx = qurilma['narx']
                    energiya = qurilma['energiya']
                    suv = qurilma['suv']
                    daraxtlar = qurilma['daraxtlar']
                    ifloslanish = qurilma['ifloslanish']
                    
                    # Yangi obyekt yaratish
                    new_building = model_func()
                    new_building.position = joylashuv
                    
                    # Ishlatilgan joyni saqlash
                    joylashuv_tuple = (joylashuv.x, joylashuv.z)
                    ishlatilgan_joylar.add(joylashuv_tuple)
                    obyektlar.append(new_building)
                    
                    print(f"[LOG] Yangi {nom} random joylashuvda qurildi: {new_building.position}")
                    print(f"[DEBUG] Grid joylashuv: ({joylashuv.x}, {joylashuv.z})")
                    print(f"[DEBUG] Ishlatilgan joylar soni: {len(ishlatilgan_joylar)}")
                    
                    # Resurslarni yangilash
                    resurslar.pul -= narx
                    resurslar.energiya += energiya
                    resurslar.suv += suv
                    resurslar.daraxtlar += daraxtlar
                    resurslar.ifloslanish += ifloslanish
                    
                    ui.show_message(f"{nom} random joylashuvda qurildi!", color.green)
                except Exception as e:
                    print(f"[ERROR] Qurishda xatolik: {e}")
            else:
                print("[LOG] Bo'sh joy topilmadi!")
                ui.show_message("Bo'sh joy topilmadi!", color.red)
        else:
            print("[LOG] Yetarli pul yo'q!")
            ui.show_message("Yetarli mablag' mavjud emas!", color.red)

    def qurish_mumkinmi(position):
        """Qurish mumkinligini tekshirish"""
        # Grid ga moslashtirish (3 birlik masofada)
        x = round(position.x / 3) * 3
        z = round(position.z / 3) * 3
        
        # Chegaradan tashqarida tekshirish
        if abs(x) > 48 or abs(z) > 48:
            return False
        
        # Ishlatilgan joylarni tekshirish
        joylashuv_tuple = (x, z)
        if joylashuv_tuple in ishlatilgan_joylar:
            return False
        
        return True

    def update():
        global building_mode, preview_building
        ui.update_ui()

        if building_mode and preview_building:
            hit_info = mouse.hovered_entity
            if hit_info and hit_info.name == 'ground':
                pos = mouse.world_point
                # Grid ga moslashtirish (3 birlik masofada)
                x = round(pos.x / 3) * 3
                z = round(pos.z / 3) * 3
                preview_building.position = Vec3(x, 0, z)
                preview_building.visible = True
                
                if qurish_mumkinmi(preview_building.position):
                    preview_building.color = TRANSPARENT
                else:
                    preview_building.color = color.rgba(1, 0, 0, 0.5)
            else:
                # Agar kursor ground ustida bo'lmasa, preview_building ni ko'rsatmaslik
                preview_building.visible = False

        if hasattr(player, 'position'):
            # O'yinchi yer ostiga tushib qolsa
            if player.y < -10:
                player.position = (0, 5, 0)
            # O'yinchi chegaradan tashqariga chiqib ketsa
            if abs(player.x) > 49 or abs(player.z) > 49:
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
            if building_mode:
                bekor_qilish()
            else:
                mouse.locked = not mouse.locked
                mouse.visible = not mouse.visible

        # O'ng tugma bilan qurish
        if building_mode and key == 'right mouse down':
            if preview_building and preview_building.visible and qurish_mumkinmi(preview_building.position) and selected_building:
                try:
                    joylashuv = preview_building.position
                    # Grid ga moslashtirish (3 birlik masofada)
                    x = round(joylashuv.x / 3) * 3
                    z = round(joylashuv.z / 3) * 3
                    joylashuv_tuple = (x, z)
                    
                    # Agar bu joy ishlatilmagan bo'lsa
                    if joylashuv_tuple not in ishlatilgan_joylar:
                        # selected_building atributlarini olish
                        model_func = selected_building['model_func']
                        nom = selected_building['nom']
                        narx = selected_building['narx']
                        energiya = selected_building['energiya']
                        suv = selected_building['suv']
                        daraxtlar = selected_building['daraxtlar']
                        ifloslanish = selected_building['ifloslanish']
                        
                        # Yangi obyekt yaratish
                        new_building = model_func()
                        new_building.position = Vec3(x, 0, z)
                        
                        # Ishlatilgan joyni saqlash
                        ishlatilgan_joylar.add(joylashuv_tuple)
                        obyektlar.append(new_building)
                        
                        print(f"[LOG] Yangi {nom} qurildi: {new_building.position}")
                        print(f"[DEBUG] Grid joylashuv: ({x}, {z})")
                        print(f"[DEBUG] Ishlatilgan joylar soni: {len(ishlatilgan_joylar)}")
                        
                        # Resurslarni yangilash
                        resurslar.pul -= narx
                        resurslar.energiya += energiya
                        resurslar.suv += suv
                        resurslar.daraxtlar += daraxtlar
                        resurslar.ifloslanish += ifloslanish
                        
                        # Qurilishdan keyin preview ni yo'q qilish va rejimdan chiqish
                        bekor_qilish()
                    else:
                        print("[LOG] Bu joyda allaqachon obyekt bor!")
                        ui.show_message("Bu joyda allaqachon obyekt bor!", color.red)
                except Exception as e:
                    print(f"[ERROR] Qurilishda xatolik: {e}")
            else:
                # Agar qurish mumkin bo'lmasa, xabar berish
                if preview_building and not qurish_mumkinmi(preview_building.position):
                    ui.show_message("Bu joyga qurib bo'lmaydi!", color.red)
        
        # Chap tugma bilan bekor qilish
        if building_mode and key == 'left mouse down':
            bekor_qilish()

    # O'yinchi yaratish
    player = FirstPersonController(
        position=(0, 2, -20),
        speed=8,
        jump_height=2,
        gravity=0.8,
        mouse_sensitivity=Vec2(40, 40)
    )
    player.collider = 'box'
    ground.name = 'ground'

    # Yorug'lik va osmon
    pivot = Entity()
    DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 0))
    AmbientLight(color=color.rgba(100, 100, 100, 0.1))
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