from ursina import Entity, color
from ursina.shaders import lit_with_shadows_shader

BROWN = color.rgba(0.6, 0.4, 0.2, 1)
DARK_RED = color.rgba(0.5, 0.1, 0.1, 1)
GRAY = color.rgba(0.5, 0.5, 0.5, 1)
DARK_GRAY = color.rgba(0.3, 0.3, 0.3, 1)
GREEN = color.rgba(0.2, 0.8, 0.2, 1)

# Modellarni yaratish
def create_house():
    house = Entity(
        model='cube',
        scale=(2, 2, 2),
        color=BROWN,
        shader=lit_with_shadows_shader
    )
    roof = Entity(
        model='cube',
        scale=(2, 1, 2),
        y=1.5,
        rotation_z=45,
        color=DARK_RED,
        shader=lit_with_shadows_shader,
        parent=house
    )
    return house

def create_factory():
    factory = Entity(
        model='cube',
        scale=(3, 2.5, 4),
        color=GRAY,
        shader=lit_with_shadows_shader
    )
    chimney = Entity(
        model='cube',
        scale=(0.5, 2, 0.5),
        position=(0.5, 1.5, 0),
        color=DARK_GRAY,
        shader=lit_with_shadows_shader,
        parent=factory
    )
    return factory

def create_tree():
    trunk = Entity(
        model='cube',
        scale=(0.3, 2, 0.3),
        color=BROWN,
        shader=lit_with_shadows_shader
    )
    leaves = Entity(
        model='cube',
        scale=(1.5, 2, 1.5),
        y=1.5,
        color=GREEN,
        shader=lit_with_shadows_shader,
        parent=trunk
    )
    return trunk

qurilmalar = [
    {
        'nom': 'Uy',
        'model_func': create_house,
        'narx': 1000,
        'energiya': -5,
        'suv': -3,
        'daraxtlar': -1,
        'ifloslanish': 2
    },
    {
        'nom': 'Zavod',
        'model_func': create_factory,
        'narx': 2000,
        'energiya': -20,
        'suv': -10,
        'daraxtlar': -3,
        'ifloslanish': 10
    },
    {
        'nom': 'Daraxt',
        'model_func': create_tree,
        'narx': 100,
        'energiya': 1,
        'suv': -1,
        'daraxtlar': 1,
        'ifloslanish': -1
    }
] 