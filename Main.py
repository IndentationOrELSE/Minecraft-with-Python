from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

world_size = 20
world_depth = 4

camera.fov = 90
# Variables
grass_texture = load_texture("Assets/Textures/Grass_Block.png")
stone_texture = load_texture("Assets/Textures/Stone_Block.png")
brick_texture = load_texture("Assets/Textures/Brick_Block.png")
dirt_texture = load_texture("Assets/Textures/Dirt_Block.png")
wood_texture = load_texture("Assets/Textures/Wood_Block.png")
iron_texture = load_texture("Assets/Textures/Iron_Ore.png")
crafting_table_texture = load_texture("Assets/Textures/Crafting_Table.png")
sky_texture = load_texture("Assets/Textures/Skybox.png")
arm_texture = load_texture("Assets/Textures/Arm_Texture.png")
punch_sound = Audio("Assets/SFX/Punch_Sound.wav", loop = False, autoplay = False)
window.exit_button.visible = False
block_pick = 1

# Updates every frame
def update():
    global block_pick
    if held_keys["escape"]: quit()
	# What happens to blocks on inputs
    if held_keys["left mouse"] or held_keys["right mouse"]:
        hand.active()
    else:
        hand.passive()

    if held_keys["1"]: block_pick = 1
    if held_keys["2"]: block_pick = 2
    if held_keys["3"]: block_pick = 3
    if held_keys["4"]: block_pick = 4
    if held_keys["5"]: block_pick = 5
    if held_keys["6"]: block_pick = 6
    if held_keys["7"]: block_pick = 7

# Voxel (block) properties
class Voxel(Button):
    def __init__(self, position = (0, 0, 0), texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = "Assets/Models/Block",
            origin_y = 0.5,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color = color.light_gray,
            scale = 0.5
        )
        self.default_color = self.color

    def on_mouse_enter(self):
        self.color = color.color(19, 0.03, 0.7)

    def on_mouse_exit(self):
        self.color = self.default_color
    # What happens to blocks on inputs
    def input(self,key):
        if self.hovered:
            if key == "right mouse down":
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
                if block_pick == 5: voxel = Voxel(position = self.position + mouse.normal, texture = wood_texture)
                if block_pick == 6: voxel = Voxel(position = self.position + mouse.normal, texture = iron_texture)
                if block_pick == 7: voxel = Voxel(position = self.position + mouse.normal, texture = crafting_table_texture)

            
            if key == "left mouse down":
                punch_sound.play()
                destroy(self)

# Skybox
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "Sphere",
            texture = sky_texture,
            scale = 150,
            double_sided = True
        )

# Arm
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = "Assets/Textures/Models/Arm",
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6)
        )
    
    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)
        
class NonInteractiveButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlight_color = self.color
        self.collision = False
        
class TableUI(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)

        cell_size = 0.08  # Size of each cell
        spacing = 0.02  # Spacing between cells
        hotbar = ["Assets/Textures/grass3d.png", "Assets/Textures/Stone3d.png", "Assets/Textures/Brick3d.png", "Assets/Textures/Dirt3d.png", "Assets/Textures/plank3d.png", "Assets/Textures/CraftingTable3d.png"]
        self.cells = []
        for i in range(9):
            if i <= len(hotbar)-1:   
                cell = NonInteractiveButton(               
                    parent=self,
                    model='quad',
                    color=color.rgba(1, 1, 1, 0.9),
                    texture=hotbar[i],
                    border=0.02,
                    scale=(cell_size, cell_size),  # Cells are square now
                    origin=(-0.5, 0),
                    position=(-0.43 + i * (cell_size + spacing), -0.42)  # Adjust positions
                )
            else:
                cell = NonInteractiveButton(    
                    parent=self,
                    model='quad',
                    border=0.02,
                    scale=(cell_size, cell_size),  # Cells are square now
                    origin=(-0.5, 0),
                    position=(-0.43 + i * (cell_size + spacing), -0.42)  # Adjust positions
                )

            # Create text entity after cell creation
            text_entity = Text(parent=cell, text=str(i + 1), position=(-0.43 + i * (cell_size + spacing), -0.382))
            self.cells.append(cell)
            
# Increase the numbers for more cubes. For exapmle: for z in range(20)
for z in range(20):
    for x in range(20):
        for y in range((0-world_depth), 0):
            if y == -4:
                voxel = Voxel(position = (x, y, z), texture = iron_texture)
            if y == -3:
                voxel = Voxel(position = (x, y, z), texture = stone_texture)
            if y == -2:
                voxel = Voxel(position = (x, y, z), texture = dirt_texture)
            if y == -1:
                voxel = Voxel(position = (x, y, z), texture = grass_texture)
            else:
                voxel = Voxel(position = (x,y,z), texture=dirt_texture)

table = TableUI()
player = FirstPersonController()
sky = Sky()
hand = Hand()


app.run()
