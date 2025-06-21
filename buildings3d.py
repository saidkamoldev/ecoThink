from ursina import Entity, color, Vec3, time
from ursina.shaders import lit_with_shadows_shader

# Ranglar
BROWN = color.rgb(139, 69, 19)
DARK_BROWN = color.rgb(87, 43, 11)
ROOF_RED = color.rgb(178, 34, 34)
GRAY = color.gray
DARK_GRAY = color.dark_gray
GREEN = color.green.tint(-.2)
WINDOW_BLUE = color.rgb(135, 206, 250)
LIGHT_GRAY = color.light_gray

def create_house():
    house = Entity(model='cube', scale=(3, 2, 4), color=BROWN, shader=lit_with_shadows_shader, collider='box')
    
    # Tom
    roof = Entity(parent=house, model='pyramid', scale=(1.1, 1, 1.05), y=0.75, color=ROOF_RED)
    
    # Eshik
    Entity(parent=house, model='quad', color=DARK_BROWN, scale=(0.4, 0.6), position=(0, -0.2, -0.505))
    
    # Derazalar
    Entity(parent=house, model='quad', color=WINDOW_BLUE, scale=(0.5, 0.5), position=(0.3, 0.1, -0.505))
    Entity(parent=house, model='quad', color=WINDOW_BLUE, scale=(0.5, 0.5), position=(-0.3, 0.1, -0.505))
    Entity(parent=house, model='quad', color=WINDOW_BLUE, scale=(0.5, 0.5), position=(0.505, 0.1, 0))
    
    return house

def create_factory():
    factory = Entity(model='cube', color=GRAY, scale=(5, 3, 6), shader=lit_with_shadows_shader, collider='box')
    
    # Mo'ri
    chimney = Entity(parent=factory, model='cylinder', color=DARK_GRAY, scale=(0.5, 3, 0.5), position=(0.4, 0.8, 0.3))
    # Tutun effekti
    smoke = Entity(parent=chimney, model='sphere', color=color.smoke, scale=0.01, y=0.6)
    def update_smoke():
        smoke.y += time.dt * 0.2
        smoke.scale += time.dt * 0.3
        if smoke.y > 1.5:
            smoke.y = 0.6
            smoke.scale = 0.01
    smoke.update = update_smoke

    # Kichik bino
    Entity(parent=factory, model='cube', color=GRAY.tint(-.2), scale=(0.4, 0.5, 0.3), position=(-0.3, -0.25, 0.5))
    
    return factory

def create_tree():
    trunk = Entity(parent=None, model='cylinder', color=BROWN, scale=(0.4, 3, 0.4), shader=lit_with_shadows_shader, collider='box')
    
    # Barglar (bir nechta sfera bilan)
    Entity(parent=trunk, model='sphere', color=GREEN, scale=2.5, y=1)
    Entity(parent=trunk, model='sphere', color=GREEN.tint(.1), scale=2, y=1.5, x=0.5)
    Entity(parent=trunk, model='sphere', color=GREEN.tint(-.1), scale=1.8, y=1.2, z=-0.4)
    
    return trunk

def create_solar_panel():
    panel_frame = Entity(model='cube', scale=(4, 0.2, 2.5), color=DARK_GRAY, shader=lit_with_shadows_shader, collider='box')
    
    # Panel yuzasi
    Entity(parent=panel_frame, model='quad', color=color.blue.tint(-0.5), scale=0.9)
    
    # Tayanch
    Entity(parent=panel_frame, model='cube', scale=(0.1, 1, 0.1), position=(0.3, -0.5, 0.2), color=LIGHT_GRAY)
    Entity(parent=panel_frame, model='cube', scale=(0.1, 1, 0.1), position=(-0.3, -0.5, 0.2), color=LIGHT_GRAY)
    
    panel_frame.rotation_x = 25
    return panel_frame

def create_water_tower():
    tank = Entity(model='cylinder', color=LIGHT_GRAY, scale=(2.5, 2, 2.5), y=2, shader=lit_with_shadows_shader)
    
    # Tayanch ustunlari
    for x in [-0.3, 0.3]:
        for z in [-0.3, 0.3]:
            Entity(parent=tank, model='cylinder', color=GRAY, scale=(0.2, 2, 0.2), position=(x, -1, z))
            
    tank.collider = 'box'
    return tank

qurilmalar = [
    {
        'nom': 'Uy',
        'model_func': create_house,
        'narx': 1200,
        'energiya': -5,
        'suv': -3,
        'daraxtlar': 0,
        'ifloslanish': 2
    },
    {
        'nom': 'Zavod',
        'model_func': create_factory,
        'narx': 3500,
        'energiya': -20,
        'suv': -10,
        'daraxtlar': 0,
        'ifloslanish': 15
    },
    {
        'nom': 'Daraxt',
        'model_func': create_tree,
        'narx': 200,
        'energiya': 0,
        'suv': -1,
        'daraxtlar': 1,
        'ifloslanish': -2
    },
    {
        'nom': 'Quyosh Paneli',
        'model_func': create_solar_panel,
        'narx': 1800,
        'energiya': 15,
        'suv': 0,
        'daraxtlar': 0,
        'ifloslanish': -1
    },
    {
        'nom': 'Suv Minorasi',
        'model_func': create_water_tower,
        'narx': 1500,
        'energiya': -2,
        'suv': 25,
        'daraxtlar': 0,
        'ifloslanish': 0
    }
]