from ursina import load_model, load_texture, Cube, Cylinder
from ursina.shaders import lit_with_shadows_shader

class Models:
    def __init__(self):
        try:
            self.house = load_model('assets/models/house.obj', use_deepcopy=True)
            self.house.shader = lit_with_shadows_shader
            self.house.texture = load_texture('assets/textures/house.png')
        except:
            print("[LOG] Uy modeli yuklanmadi, standart model ishlatiladi")
            self.house = Cube()
        try:
            self.factory = load_model('assets/models/factory.obj', use_deepcopy=True)
            self.factory.shader = lit_with_shadows_shader
            self.factory.texture = load_texture('assets/textures/factory.png')
        except:
            print("[LOG] Zavod modeli yuklanmadi, standart model ishlatiladi")
            self.factory = Cube()
        try:
            self.tree = load_model('assets/models/tree.obj', use_deepcopy=True)
            self.tree.shader = lit_with_shadows_shader
            self.tree.texture = load_texture('assets/textures/tree.png')
        except:
            print("[LOG] Daraxt modeli yuklanmadi, standart model ishlatiladi")
            self.tree = Cylinder()
        try:
            self.garden = load_model('assets/models/garden.obj', use_deepcopy=True)
            self.garden.shader = lit_with_shadows_shader
            self.garden.texture = load_texture('assets/textures/garden.png')
        except:
            print("[LOG] Bog' modeli yuklanmadi, standart model ishlatiladi")
            self.garden = Cube()
        try:
            self.solar = load_model('assets/models/solar_panel.obj', use_deepcopy=True)
            self.solar.shader = lit_with_shadows_shader
            self.solar.texture = load_texture('assets/textures/solar_panel.png')
        except:
            print("[LOG] Quyosh paneli modeli yuklanmadi, standart model ishlatiladi")
            self.solar = Cube()
        try:
            self.water_tower = load_model('assets/models/water_tower.obj', use_deepcopy=True)
            self.water_tower.shader = lit_with_shadows_shader
            self.water_tower.texture = load_texture('assets/textures/water_tower.png')
        except:
            print("[LOG] Suv minorasi modeli yuklanmadi, standart model ishlatiladi")
            self.water_tower = Cylinder() 