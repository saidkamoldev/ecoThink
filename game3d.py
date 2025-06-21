from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from resources import Resurslar
from buildings3d import qurilmalar
from ui import UI

def start_game():
    TRANSPARENT = color.rgba(0, 0.8, 0, 0.5)
    global resurslar, obyektlar, building_mode, preview_building, selected_building, player, ui
    resurslar = Resurslar()
    obyektlar = []
    building_mode = False
    preview_building = None
    selected_building = None

    def sign(x):
        return -1 if x < 0 else (1 if x > 0 else 0)

    # O'yin maydonini yaratish
    ground = Entity(
        model='plane',
        scale=(100, 1, 100),
        color=color.rgba(0.7, 0.7, 0.4, 1),
        texture='white_cube',
        texture_scale=(100, 100),
        collider='box'
    )
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

    def qurish(qurilma):
        global building_mode, preview_building, selected_building
        if resurslar.pul >= qurilma['narx']:
            building_mode = True
            selected_building = qurilma
            if preview_building:
                destroy(preview_building)
            preview_building = qurilma['model_func']()
            preview_building.color = TRANSPARENT
            mouse.locked = False
            mouse.visible = True
            print(f"[LOG] {qurilma['nom']} tanlandi! Joylashtirish uchun O'NG tugmani, bekor qilish uchun CHAP tugmani bosing.")
        else:
            print("[LOG] Yetarli pul yo'q!")
            ui.show_message("Yetarli mablag' mavjud emas!", color.red)

    def qurish_mumkinmi(position):
        if abs(position.x) > 48 or abs(position.z) > 48:
            print("[LOG] Chegara tashqarisiga qurib bo'lmaydi!")
            return False
        for obj in obyektlar:
            if hasattr(obj, 'position'):
                distance = (position - obj.position).length()
                if distance < 5:
                    print("[LOG] Bu yerda boshqa bino bor!")
                    return False
        return True

    def update():
        global building_mode, preview_building
        ui.update_ui()

        if building_mode and preview_building:
            hit_info = mouse.hovered_entity
            if hit_info and hit_info.name == 'ground':
                pos = mouse.world_point
                preview_building.position = Vec3(round(pos.x), 0, round(pos.z))
                if qurish_mumkinmi(preview_building.position):
                    preview_building.color = TRANSPARENT
                else:
                    preview_building.color = color.rgba(1, 0, 0, 0.5)

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
            if preview_building and qurish_mumkinmi(preview_building.position):
                try:
                    new_building = selected_building['model_func']()
                    new_building.position = preview_building.position
                    obyektlar.append(new_building)
                    print(f"[LOG] Yangi {selected_building['nom']} qurildi: {new_building.position}")
                    resurslar.pul -= selected_building['narx']
                    resurslar.energiya += selected_building['energiya']
                    resurslar.suv += selected_building['suv']
                    resurslar.daraxtlar += selected_building['daraxtlar']
                    resurslar.ifloslanish += selected_building['ifloslanish']
                    
                    # Qurilish tugagandan so'ng kursorni yashirish va boshqaruvni tiklash
                    mouse.locked = True
                    mouse.visible = False
                    building_mode = False
                    if preview_building:
                        destroy(preview_building)
                    preview_building = None
                    selected_building = None
                    
                    # Agar pul qolmasa, qurilish rejimini to'xtatish
                    if resurslar.pul < selected_building['narx']:
                        bekor_qilish()

                except Exception as e:
                    print(f"[ERROR] Qurilishda xatolik: {e}")
        
        # Chap tugma bilan bekor qilish
        if building_mode and key == 'left mouse down':
            bekor_qilish()

    player = FirstPersonController(
        position=(0, 2, -20),
        speed=8,
        jump_height=2,
        gravity=0.8,
        mouse_sensitivity=Vec2(40, 40)
    )
    player.collider = 'box'
    ground.name = 'ground'

    pivot = Entity()
    DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 0))
    AmbientLight(color=color.rgba(100, 100, 100, 0.1))
    Sky()

    global ui
    ui = UI(resurslar=resurslar, qurilmalar=qurilmalar, qurish_func=qurish)

    # O'yinni kursor bilan boshlash
    mouse.locked = False
    mouse.visible = True

    application.update = update
    application.input = input_func