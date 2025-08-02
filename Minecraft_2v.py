from ursina import*
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
app=Ursina()
grass_texture=load_texture("Grass_Block.png")
stone_texture=load_texture("Stone_Block.png")
brick_texture=load_texture("Brick_Block.png")
dirt_texture=load_texture("Dirt_Block.png")
wood_texture=load_texture("Wood_Block.png")
bedrock_texture=load_texture("bedrock.png")
music_texture=load_texture("music.png")
sky_texture=load_texture("Skybox.png")
arm_texture=load_texture("Arm_Texture.png")
punch_sound=Audio("Punch_Sound.wav",loop=False,autoplay=False)
block_sound=Audio("sweden-m.mp3",loop=False,autoplay=False,volume=2)
window.exit_button.visible=True
block_pick=1
noise = PerlinNoise(octaves=1, seed=random.randint(0, 10000))
blocks_dict = {}
generated_chunks = set()
GENERATE_RADIUS = 1
chunks_to_generate = []
CHUNK_SIZE = 5
def get_chunks_around(player_chunk,radius):
    current_x,current_z = player_chunk
    chunks=[]
    for x in range(current_x - radius,current_x+radius+1):
        for z in range(current_z - radius,current_z+radius+1):
            chunks.append((x,z))
    return chunks




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
    if held_keys['6']: block_pick=6
    if held_keys['7']: block_pick=7
    if player.y <= -12:
        player.position = Vec3(0, 0, 0)
    if held_keys['escape']:
        app.userExit()

    current_chunk = (int(player.x // CHUNK_SIZE), int(player.z // CHUNK_SIZE))
    forward = Vec3(camera.forward.x, 0, camera.forward.z).normalized()
    next_chunk_pos = Vec3(player.x, 0, player.z) + forward * CHUNK_SIZE
    target_chunk = (int(next_chunk_pos.x // CHUNK_SIZE), int(next_chunk_pos.z // CHUNK_SIZE))
    unload_far_chunks(current_chunk, radius=2)

    for chunk in [current_chunk, target_chunk]:
        if chunk not in generated_chunks and chunk not in chunks_to_generate:
            chunks_to_generate.append(chunk)

    if chunks_to_generate:
        next_chunk = chunks_to_generate.pop(0)
        generator_blocks(next_chunk)
        generated_chunks.add(next_chunk)



    
    
        
    
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
                if block_pick==1:
                    main=Main(position=self.position+mouse.normal,texture=grass_texture)
                if block_pick==2:
                    main=Main(position=self.position+mouse.normal,texture=stone_texture)
                if block_pick==3:
                    main=Main(position=self.position+mouse.normal,texture=brick_texture)
                if block_pick==4:
                    main=Main(position=self.position+mouse.normal,texture=dirt_texture)
                if block_pick==5: 
                    main=Main(position=self.position+mouse.normal,texture=wood_texture)
                if block_pick==6: 
                    main=Main(position=self.position+mouse.normal,texture=bedrock_texture)
                if block_pick==7:
                    main=Main(position=self.position+mouse.normal,texture=music_texture)
            if key=="right mouse down" and not self.texture==bedrock_texture:
                punch_sound.play()
                destroy(self)
            if key.lower() == 'q' and self.texture==music_texture:
                music_go()
            if key.lower() == 'e' and self.texture==music_texture:
                music_stop()
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='Sphere',
            texture=sky_texture,
            scale=1500,
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
min_height=-5
before_min_height = -4
for z in range(10):
    for x in range(10):
        height = round(noise([x/10, z/10]) * 10)
        for y in range(height, min_height - 1, -1):
            pos = (x, y + min_height, z)
            if y == min_height:
                block = Main(position=pos, texture=bedrock_texture)
            elif height - y > 2:
                block = Main(position=pos, texture=stone_texture)
            elif y == height:
                block = Main(position=pos, texture=grass_texture)
            else:
                block = Main(position=pos, texture=dirt_texture)
            blocks_dict[pos] = block
def generator_blocks(chunk):
    chunk_x, chunk_z = chunk
    for z in range(chunk_z * 5, chunk_z * 5 + 5):
        for x in range(chunk_x * 5, chunk_x * 5 + 5):
            height = round(noise([x/10, z/10]) * 10)
            for y in range(height, min_height - 1, -1):
                pos = (x, y + min_height, z)
                if y == min_height:
                    block = Main(position=pos, texture=bedrock_texture)
                elif height - y > 2:
                    block = Main(position=pos, texture=stone_texture)
                elif y == height:
                    block = Main(position=pos, texture=grass_texture)
                else:
                    block = Main(position=pos, texture=dirt_texture)
               
                blocks_dict[pos] = block
                
                
def unload_far_chunks(player_chunk, radius=2):
    chunks_to_keep = set(get_chunks_around(player_chunk, radius))
    chunks_to_delete = generated_chunks - chunks_to_keep

    for chunk in chunks_to_delete:
        chunk_x, chunk_z = chunk
        for z in range(chunk_z * CHUNK_SIZE, chunk_z * CHUNK_SIZE + CHUNK_SIZE):
            for x in range(chunk_x * CHUNK_SIZE, chunk_x * CHUNK_SIZE + CHUNK_SIZE):
                height = round(noise([x / 10, z / 10]) * 10)  
                for y in range(height, min_height - 1, -1):
                    pos = (x, y + min_height, z)
                    if pos in blocks_dict:
                        destroy(blocks_dict[pos])
                        del blocks_dict[pos]
        generated_chunks.remove(chunk)
def music_go():
    print('1')
    block_sound.play()
def music_stop():
    print('2')
    block_sound.stop()
            
player=FirstPersonController()
sky=Sky()
hand=Hand()
app.run()
            
