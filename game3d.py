from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from textwrap import dedent
from models3d import Models
from resources import Resurslar
from buildings3d import qurilmalar

def start_game():
    TRANSPARENT = color.rgba(1, 1, 1, 0.5)
    WHITE = color.rgba(1, 1, 1, 1)
    global models, resurslar, obyektlar, building_mode, preview_building, selected_building, player
    models = Models()
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

    resurslar_text = Text(text=resurslar.update_text(), position=(-0.85, 0.4))

    def qurish(qurilma):
        global preview_building, selected_building
        if resurslar.pul >= qurilma['narx']:
            selected_building = qurilma
            if preview_building:
                destroy(preview_building)
            preview_building = qurilma['model_func']()
            preview_building.color = TRANSPARENT
            print(f"[LOG] {qurilma['nom']} tanlandi! O'ng tugmani bosib quring.")
        else:
            print("[LOG] Yetarli pul yo'q!")

    def qurish_mumkinmi(position):
        if abs(position.x) > 48 or abs(position.z) > 48:
            print("[LOG] Chegara tashqarisiga qurib bo'lmaydi!")
            return False
        for obj in obyektlar:
            if hasattr(obj, 'position'):
                distance = (position - obj.position).length()
                if distance < 3:
                    print("[LOG] Bu yerda boshqa bino bor!")
                    return False
        return True

    def update():
        global building_mode, preview_building, selected_building
        if building_mode and preview_building:
            hit_info = raycast(
                camera.position, 
                camera.forward, 
                distance=20, 
                ignore=[preview_building] + obyektlar
            )
            if hit_info.hit:
                preview_building.position = hit_info.world_point
                preview_building.y = 0
                if held_keys['right mouse'] and not held_keys['left mouse']:
                    if qurish_mumkinmi(preview_building.position):
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
                            if resurslar.pul < selected_building['narx']:
                                building_mode = False
                                destroy(preview_building)
                                preview_building = None
                                selected_building = None
                                mouse.locked = True
                                mouse.visible = False
                        except Exception as e:
                            print(f"[ERROR] Qurilishda xatolik: {e}")
        if hasattr(player, 'position'):
            if player.position.y < 1.8:
                player.position = Vec3(player.position.x, 1.8, player.position.z)
                player.air_time = 0
                player.jumping = False
            if abs(player.position.x) > 48:
                player.position = Vec3(48 * sign(player.position.x), player.position.y, player.position.z)
            if abs(player.position.z) > 48:
                player.position = Vec3(player.position.x, player.position.y, 48 * sign(player.position.z))
            if player.position.y > 20:
                player.position = Vec3(player.position.x, 20, player.position.z)

    def input_func(key):
        global building_mode, preview_building, selected_building
        print(f'[LOG] Tugma bosildi: {key}')
        if key == 'escape':
            if building_mode:
                building_mode = False
                if preview_building:
                    destroy(preview_building)
                preview_building = None
                selected_building = None
                mouse.locked = True
                mouse.visible = False
                print('[LOG] Qurilish rejimidan chiqildi')
            else:
                if not mouse.locked:
                    mouse.locked = True
                    mouse.visible = False
                    print('[LOG] Sichqoncha yashirildi')
                else:
                    mouse.locked = False
                    mouse.visible = True
                    print('[LOG] Sichqoncha ko\'rsatildi')
        elif key == 'right mouse down' and selected_building:
            building_mode = True
            if preview_building:
                destroy(preview_building)
            preview_building = selected_building['model_func']()
            preview_building.color = TRANSPARENT
            mouse.locked = False
            mouse.visible = True
            print(f"[LOG] Qurilish rejimi boshlandi: {selected_building['nom']}")
        elif key in ['1', '2', '3']:
            try:
                index = int(key) - 1
                if index < len(qurilmalar):
                    qurish(qurilmalar[index])
            except Exception as e:
                print(f'[ERROR] Qurilmani tanlashda xatolik: {e}')

    player = FirstPersonController(
        position=(0, 2, -20),
        speed=8,
        jump_height=2,
        jump_duration=0.35,
        gravity=1.2,
        mouse_sensitivity=Vec2(40, 40),
        jump_up_duration=0.2,
        fall_after=0.15,
        jumping=False
    )
    pivot = Entity()
    DirectionalLight(parent=pivot, y=2, z=3, shadows=True)
    AmbientLight(color=Vec4(0.6, 0.6, 0.6, 0.6))
    Sky()
    for i, qurilma in enumerate(qurilmalar):
        button = Button(
            parent=camera.ui,
            text=f"{qurilma['nom']}\n{qurilma['narx']}$",
            color=WHITE,
            position=(0.7, 0.45 - i*0.15),
            scale=(0.2, 0.12),
            on_click=lambda q=qurilma: qurish(q)
        )
    help_text = Text(
        text=dedent('''
            Boshqarish:
            WASD - harakatlanish
            SPACE - sakrash
            ESC - qurilishni bekor qilish
            O'ng tugma - qurilishni boshlash
            Chap tugma - qurilmani joylashtirish
            O'ng panel - qurilmalarni tanlash
        ''').strip(),
        position=(-0.85, -0.4)
    )
    application.update = update
    application.input = input_func 