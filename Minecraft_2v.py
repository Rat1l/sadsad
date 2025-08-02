from ursina import*
from ursina.prefabs.first_person_controller import FirstPersonController
app=Ursina()
grass_texture=load_texture("Grass_Block.png")
stone_texture=load_texture("Stone_Block.png")
brick_texture=load_texture("Brick_Block.png")
dirt_texture=load_texture("Dirt_Block.png")
wood_texture=load_texture("Wood_Block.png")
sky_texture=load_texture("Skybox.png")
arm_texture=load_texture("Arm_Texture.png")
punch_sound=Audio("Punch_Sound.wav",loop=False,autoplay=False)
window.exit_button.visible=True
block_pick=1
def update():
    global block_pick
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()
    if held_keys['1']: block_pick=1
    if held_keys['2']: block_pick=2
    if held_keys['3']: block_pick=3
    if held_keys['4']: block_pick=4
    if held_keys['5']: block_pick=5
    if held_keys['escape']: app.userExit()
class Main(Button):
    def __init__(self, position=(0,0,0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model="Block",
            origin_y=0.5,
            texture=texture,
            color=color.color(0,0,random.uniform(0.9,1)),
            highlight_color=color.light_gray,
            scale=0.5) 
    def input(self,key):
        if self.hovered:
            if key=="left mouse down":
                punch_sound.play()
                if block_pick==1: main=Main(position=self.position+mouse.normal,texture=grass_texture)
                if block_pick==2: main=Main(position=self.position+mouse.normal,texture=stone_texture)
                if block_pick==3: main=Main(position=self.position+mouse.normal,texture=brick_texture)
                if block_pick==4: main=Main(position=self.position+mouse.normal,texture=dirt_texture)
                if block_pick==5: main=Main(position=self.position+mouse.normal,texture=wood_texture)
            if key=="right mouse down":
                punch_sound.play()
                destroy(self)
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='Sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True)
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model="Arm",
            scale=0.2,
            texture=arm_texture,
            rotation=Vec3(150,-10,0),
            position=Vec2(0.4,-0.6))
    def active(self):
        self.position=Vec2(0.3,-0.5)
    def passive(self):
        self.position=Vec2(0.4,-0.6)
for z in range(30):
    for x in range(30):
        main=Main(position=(x,0,z))
player=FirstPersonController()
sky=Sky()
hand=Hand()
app.run()
            
