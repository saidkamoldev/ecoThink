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
    house = Entity(model='models/Bambo_House.obj', scale=(0.3, 0.3, 0.3), color=BROWN, shader=lit_with_shadows_shader, collider='box')
    return house

def create_factory():
    factory = Entity(model='models/zavod.obj', scale=(0.4, 0.4, 0.4), color=GRAY, shader=lit_with_shadows_shader, collider='box')
    return factory

def create_tree():
    trunk = Entity(parent=None, model='models/daraxt.obj', scale=(0.5, 0.5, 0.5), color=BROWN, shader=lit_with_shadows_shader, collider='box')
    return trunk

def create_solar_panel():
    panel_frame = Entity(model='models/solar_panels.obj', scale=(0.2, 0.2, 0.2), color=DARK_GRAY, shader=lit_with_shadows_shader, collider='box')
    return panel_frame

def create_water_tower():
    tank = Entity(model='cylinder', color=LIGHT_GRAY, scale=(0.9, 0.8, 0.9), y=0.8, shader=lit_with_shadows_shader)
    
    # Tayanch ustunlari
    for x in [-0.1, 0.1]:
        for z in [-0.1, 0.1]:
            Entity(parent=tank, model='cylinder', color=GRAY, scale=(0.08, 0.8, 0.08), position=(x, -0.4, z))
            
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