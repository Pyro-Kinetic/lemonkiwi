from random import randint

import pygame
from game_data import levels
from particles import ParticleEffect
from player import Player
from settings import tile_size
from support import import_csv_layout, import_cut_graphics, image_loader, sound_loader
from tiles import StaticTileSets, Fruits, Skull
from traps import Fire, Trampoline, AnimateFireTraps, AnimateTrampoline


def place_holder_tile(data, tile_type):
    if tile_type in data:
        return tile_type
    else:
        return "empty"


class Level:
    def __init__(self, surface, level_number, load_over_world):
        # general setup
        self.display_surface = surface
        self.screen_shake_duration = 0
        self.screen_shake = 0
        self.game_over = False
        self.load_over_world = load_over_world

        # audio
        self.button_click_sound = sound_loader("../audio/button_click.mp3")
        self.button_click_sound.set_volume(0.5)
        self.tramp_hit_sound = sound_loader("../audio/tramp_bounce.mp3")
        self.jump_sound1 = sound_loader("../audio/jump.mp3")
        self.jump_sound2 = sound_loader("../audio/double_jump.mp3")
        self.pop_sound = sound_loader("../audio/pop.mp3")
        self.pop_sound.set_volume(0.5)
        self.death_by_fire_sound = sound_loader("../audio/death_by_fire.mp3")
        self.death_by_spikes_sound = sound_loader("../audio/death_by_spikes.mp3")

        # level switcher
        self.level_number = level_number
        level_data = levels[self.level_number]

        # placeholder tiles
        platform_tile_place_holder = place_holder_tile(level_data, "platform")
        fire_pot_place_holder = place_holder_tile(level_data, "fire_pot")
        trampoline_place_holder = place_holder_tile(level_data, "trampoline")
        spikes_place_holder = place_holder_tile(level_data, "spikes")

        # levels
        level_layout = import_csv_layout(level_data["level"])
        self.level_sprites = self.create_tile_group(level_layout, "level")

        # skull
        self.render_skull = False
        checkpoint_layout = import_csv_layout(level_data["checkpoint"])
        self.checkpoint_sprites = self.create_tile_group(checkpoint_layout, "checkpoint")

        # fruits
        fruits_layout = import_csv_layout(level_data["fruits"])
        self.fruit_sprites = self.create_tile_group(fruits_layout, "fruits")
        self.collected_fruits = 0
        self.total_fruits = len(pygame.sprite.Group.sprites(self.fruit_sprites))

        # platform
        platform_layout = import_csv_layout(level_data[platform_tile_place_holder])
        self.platform_sprites = self.create_tile_group(platform_layout, platform_tile_place_holder)

        # player
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # menu_buttons
        menu_layout = import_csv_layout(level_data["menu_buttons"])
        self.menu_sprites = self.create_tile_group(menu_layout, "menu_buttons")

        # dust particles
        self.particle_sprites = pygame.sprite.GroupSingle()

        # collected fruit particles
        self.collected_fruit_sprites = pygame.sprite.GroupSingle()

        # TRAPS

        # spikes
        self.spike_layout = import_csv_layout(level_data[spikes_place_holder])
        self.spike_sprites = self.create_tile_group(self.spike_layout, spikes_place_holder)

        # fire pot
        self.fire_layout = import_csv_layout(level_data[fire_pot_place_holder])
        self.fire_sprites = self.create_tile_group(self.fire_layout, fire_pot_place_holder)

        # fire pot animation sprite
        self.fire_animation_sprites = pygame.sprite.Group()

        # collision timer variables
        self.fire_collision = False
        self.fire_collision_duration = 105
        self.fire_collision_time = 0

        # trampoline
        self.trampoline_layout = import_csv_layout(level_data[trampoline_place_holder])
        self.trampoline_sprites = pygame.sprite.Group()
        self.trampoline_setup(self.trampoline_layout)

        # trampoline animation sprite
        self.animated_trampoline_sprites = pygame.sprite.Group()

    def create_tile_group(self, layout, tile_type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if tile_type == "fruits":
                        if val == "3":
                            sprite = Fruits(tile_size, x, y, "../graphics/items/fruits/strawberry.png",
                                            self.display_surface)
                        if val == "4":
                            sprite = Fruits(tile_size, x, y, "../graphics/items/fruits/bananas.png",
                                            self.display_surface)
                        if val == "5":
                            sprite = Fruits(tile_size, x, y, "../graphics/items/fruits/apple.png",
                                            self.display_surface)
                        if val == "6":
                            sprite = Fruits(tile_size, x, y, "../graphics/items/fruits/cherries.png",
                                            self.display_surface)
                        if val == "8":
                            sprite = Fruits(tile_size, x, y, "../graphics/items/fruits/kiwi.png",
                                            self.display_surface)
                        if val == "9":
                            sprite = Fruits(tile_size, x, y, "../graphics/items/fruits/melon.png",
                                            self.display_surface)
                        if val == "10":
                            sprite = Fruits(tile_size, x, y, "../graphics/items/fruits/orange.png",
                                            self.display_surface)
                        if val == "11":
                            sprite = Fruits(tile_size, x, y, "../graphics/items/fruits/pineapple.png",
                                            self.display_surface)

                    if tile_type == "checkpoint":
                        sprite = Skull(tile_size, x, y, "../graphics/items/idle_skull.png")

                    if tile_type == "menu_buttons":
                        if val == "0":
                            previous_button_image = image_loader("../graphics/menu/buttons/previous.png")
                            sprite = StaticTileSets(tile_size, x, y, previous_button_image)
                        if val == "1":
                            restart_button_image = image_loader("../graphics/menu/buttons/restart.png")
                            sprite = StaticTileSets(tile_size, x, y, restart_button_image)
                        if val == "2":
                            next_button_image = image_loader("../graphics/menu/buttons/next.png")
                            sprite = StaticTileSets(tile_size, x, y, next_button_image)
                        if val == "4":
                            over_world_button = image_loader("../graphics/menu/buttons/levels.png")
                            sprite = StaticTileSets(tile_size, x, y, over_world_button)

                    if tile_type == "level":
                        if val == "7":
                            level_0_image = image_loader("../graphics/menu/levels/00.png")
                            sprite = StaticTileSets(tile_size, x, y, level_0_image)
                        if val == "8":
                            level_1_image = image_loader("../graphics/menu/levels/01.png")
                            sprite = StaticTileSets(tile_size, x, y, level_1_image)
                        if val == "9":
                            level_2_image = image_loader("../graphics/menu/levels/02.png")
                            sprite = StaticTileSets(tile_size, x, y, level_2_image)
                        if val == "10":
                            level_3_image = image_loader("../graphics/menu/levels/03.png")
                            sprite = StaticTileSets(tile_size, x, y, level_3_image)
                        if val == "11":
                            level_4_image = image_loader("../graphics/menu/levels/04.png")
                            sprite = StaticTileSets(tile_size, x, y, level_4_image)
                        if val == "12":
                            level_5_image = image_loader("../graphics/menu/levels/05.png")
                            sprite = StaticTileSets(tile_size, x, y, level_5_image)

                    if tile_type == "terrain":
                        terrain_tile_list = import_cut_graphics(path="../graphics/terrain/terrain.png",
                                                                tile_size=tile_size, is_tile_on_y_axis=True,
                                                                offset_y=tile_size, destination=(0, 0))
                        terrain_tiles = terrain_tile_list[int(val)]
                        sprite = StaticTileSets(tile_size, x, y, terrain_tiles)

                    if tile_type == "platform":
                        platform_tile_list = import_cut_graphics(path="../graphics/terrain/terrain.png",
                                                                 tile_size=tile_size, is_tile_on_y_axis=True,
                                                                 offset_y=tile_size, destination=(0, 0))
                        platform_tiles = platform_tile_list[int(val)]
                        sprite = StaticTileSets(tile_size, x, y, platform_tiles)

                    if tile_type == "empty":
                        empty_image = image_loader("../graphics/traps/saw/chain.png")
                        sprite = StaticTileSets(tile_size, x, y, empty_image)

                    # traps
                    if tile_type == "fire_pot":
                        fire_image = image_loader("../graphics/traps/fire/off.png")
                        sprite = Fire(tile_size, x, y, fire_image, 64, self.display_surface)

                    if tile_type == "spikes":
                        if val == "0":
                            spike_image = image_loader("../graphics/traps/spikes/idle.png")
                            sprite = StaticTileSets(tile_size, x, y, spike_image)
                        if val == "1":
                            spike_image = image_loader("../graphics/traps/spikes/idle_down.png")
                            sprite = StaticTileSets(tile_size, x, y, spike_image)
                        if val == "2":
                            spike_image = image_loader("../graphics/traps/spikes/idle_right.png")
                            sprite = StaticTileSets(tile_size, x, y, spike_image)
                        if val == "3":
                            spike_image = image_loader("../graphics/traps/spikes/idle_left.png")
                            sprite = StaticTileSets(tile_size, x, y, spike_image)

                    sprite_group.add(sprite)

        return sprite_group

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self.button_click_sound.play()
            self.load_over_world()

    def world_shift(self):
        if self.screen_shake_duration > 0:
            self.screen_shake = randint(0, 8) - 4
            self.screen_shake_duration -= 1

        else:
            self.screen_shake = 0
        # print(self.screen_shake)

    def create_jump_particles(self, pos):
        pos -= pygame.math.Vector2(0, 12)
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.particle_sprites.add(jump_particle_sprite)

    def get_player_landing(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground:
            offset = pygame.math.Vector2(0, 20)
            fall_dust_particle = ParticleEffect(self.player.sprite.collision_rect.midbottom - offset, "land")
            self.particle_sprites.add(fall_dust_particle)

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0":
                    sprite = Player(tile_size, x, y, self.display_surface)
                    self.player.add(sprite)

    def trampoline_setup(self, layout):
        trampoline_image = image_loader("../graphics/traps/trampoline/idle.png")

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "5":
                    sprite = Trampoline(tile_size, x, y, trampoline_image, 8, 20, self.display_surface)
                    self.trampoline_sprites.add(sprite)

    # Terrain Collision
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites:
            if not self.game_over:
                if sprite.rect.colliderect(player.collision_rect):
                    if player.direction.x < 0:
                        player.collision_rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.collision_rect.right = sprite.rect.left

        self.horizontal_fire_trap_collision()

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites:
            if not self.game_over:
                if sprite.rect.colliderect(player.collision_rect):
                    if player.direction.y > 0:
                        player.collision_rect.bottom = sprite.rect.top
                        player.jump_counter = 0
                        player.direction.y = 0
                        player.on_ground = True
                        player.on_left_wall = False
                        player.on_right_wall = False

                    elif player.direction.y < 0:
                        player.collision_rect.top = sprite.rect.bottom
                        player.direction.y = 0

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        self.activate_fire_on_vertical_collision()

    # Platforms and Fruits Collision
    def check_platform_collision(self):
        player = self.player.sprite

        for sprite in self.platform_sprites:
            if not self.game_over:
                if sprite.rect.colliderect(player.collision_rect):
                    platform_top = sprite.rect.top
                    platform_center = sprite.rect.centery
                    player_bottom = player.collision_rect.bottom
                    if platform_top < player_bottom < platform_center and player.direction.y > 0:
                        player.collision_rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                        player.on_left_wall = False
                        player.on_right_wall = False
                        player.jump_counter = 0

    def check_fruit_collision(self):
        # until next time on dragon ball z
        if pygame.sprite.spritecollide(self.player.sprite, self.fruit_sprites, False, pygame.sprite.collide_rect):
            collected_fruits = pygame.sprite.spritecollide(self.player.sprite, self.fruit_sprites, True,
                                                           pygame.sprite.collide_mask)
            if collected_fruits:
                if not self.game_over:
                    for fruit in collected_fruits:
                        collected_fruit_particle = ParticleEffect(pos=fruit.rect.center, animation_type="collected")
                        self.collected_fruit_sprites.add(collected_fruit_particle)
                        if self.collected_fruits < self.total_fruits:
                            self.collected_fruits += 1
                            self.pop_sound.play()

    # Fire Trap Collision
    def horizontal_fire_trap_collision(self):
        player = self.player.sprite

        for sprite in self.fire_sprites:
            if not self.game_over:
                if sprite.collision_rect.colliderect(player.collision_rect):
                    if player.direction.x < 0:
                        player.collision_rect.left = sprite.collision_rect.right
                    elif player.direction.x > 0:
                        player.collision_rect.right = sprite.collision_rect.left

    def activate_fire_on_vertical_collision(self):
        player = self.player.sprite

        for sprite in self.fire_sprites:
            if not self.game_over:
                if sprite.collision_rect.colliderect(player.collision_rect):
                    if player.direction.y > 0:
                        player.collision_rect.bottom = sprite.collision_rect.top
                        player.jump_counter = 0
                        player.direction.y = 0
                        player.on_ground = True
                        player.on_left_wall = False
                        player.on_right_wall = False

                    elif player.direction.y < 0:
                        player.collision_rect.top = sprite.collision_rect.bottom
                        player.direction.y = 0

                    fire_pot_animation = AnimateFireTraps(pos=sprite.rect.center, animation_type="fire_hit")
                    if not self.fire_collision:
                        self.fire_animation_sprites.add(fire_pot_animation)
                        self.fire_collision = True
                        self.fire_collision_time = pygame.time.get_ticks()

    # Trampoline Collision
    def trampoline_bounce(self):
        player = self.player.sprite

        if not self.game_over:
            if pygame.sprite.spritecollide(player, self.trampoline_sprites, False, pygame.sprite.collide_rect):
                collided = pygame.sprite.spritecollide(player, self.trampoline_sprites, False,
                                                       pygame.sprite.collide_mask)
                if collided:
                    for sprite in collided:
                        trampoline_bounce_animation = AnimateTrampoline(pos=sprite.rect.center, animation_type="bounce")
                        self.animated_trampoline_sprites.add(trampoline_bounce_animation)

                        self.screen_shake_duration = 10
                        player.direction.y = -30
                        player.jump_counter = 1
                        self.tramp_hit_sound.play()

    def collision_timer(self):
        if self.fire_collision:
            current_time = pygame.time.get_ticks()
            if current_time - self.fire_collision_time >= self.fire_collision_duration:
                self.fire_collision = False

    # Player Mechanics
    def wall_slide(self):
        player = self.player.sprite
        wall_slide_speed = 2

        for sprite in self.terrain_sprites:
            if not self.game_over:
                if sprite.rect.colliderect(player.wall_slide_rect):
                    if player.direction.y > 0:
                        player.direction.y = wall_slide_speed
                        player.jump_counter = 1

    def check_wall_bounce(self):
        player = self.player.sprite

        if player.on_wall and player.direction.y == 2 and not player.facing_right:
            player.on_left_wall = True
        else:
            player.on_left_wall = False
        if player.on_wall and player.direction.y == 2 and player.facing_right:
            player.on_right_wall = True
        else:
            player.on_right_wall = False

    def player_double_jump_mechanic(self, pygame_event):
        player = self.player.sprite

        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_UP and player.jump_counter < 2:
                player.jump()
                self.create_jump_particles(player.collision_rect.midbottom)
                player.on_ground = False
                player.wall_slide = False
                if player.jump_counter == 1:
                    self.jump_sound1.play()
                else:
                    self.jump_sound2.play()

    def death_state(self):
        self.player.sprite.direction.y = -31
        self.screen_shake_duration = 50
        self.game_over = True

    def death_by_spikes(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.spike_sprites, False, pygame.sprite.collide_rect):
            collided = pygame.sprite.spritecollide(self.player.sprite, self.spike_sprites, False,
                                                   pygame.sprite.collide_mask)
            if collided:
                if not self.game_over:
                    self.death_by_spikes_sound.play()
                    self.death_state()

    def death_by_fire(self):
        player = self.player.sprite
        for sprite in self.fire_animation_sprites:
            if sprite.rect.colliderect(player.collision_rect) and sprite.is_flame_on:
                self.death_by_fire_sound.play()
                self.death_state()

    def end_game(self):
        self.death_by_spikes()
        self.death_by_fire()

    def run(self):
        self.input()
        self.world_shift()

        # levels
        self.level_sprites.update()
        self.level_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update()
        self.terrain_sprites.draw(self.display_surface)

        # platform
        self.platform_sprites.update()
        self.platform_sprites.draw(self.display_surface)

        # spikes
        self.spike_sprites.update()
        self.spike_sprites.draw(self.display_surface)

        # fire
        self.fire_sprites.update()
        self.fire_sprites.draw(self.display_surface)

        # fire animation
        self.fire_animation_sprites.update()
        self.fire_animation_sprites.draw(self.display_surface)

        # trampoline
        self.trampoline_sprites.update(self.screen_shake)
        self.trampoline_sprites.draw(self.display_surface)
        self.animated_trampoline_sprites.update()
        self.animated_trampoline_sprites.draw(self.display_surface)

        # fruits
        self.fruit_sprites.update(self.screen_shake)
        self.fruit_sprites.draw(self.display_surface)

        # skull
        if self.render_skull:
            self.checkpoint_sprites.update()
            self.checkpoint_sprites.draw(self.display_surface)

        # fruit particle
        self.collected_fruit_sprites.update()
        self.collected_fruit_sprites.draw(self.display_surface)

        # player
        self.player.update()
        self.trampoline_bounce()
        self.horizontal_movement_collision()
        self.get_player_landing()
        self.vertical_movement_collision()
        self.check_platform_collision()
        self.check_fruit_collision()
        self.collision_timer()
        self.wall_slide()
        self.check_wall_bounce()
        self.create_landing_particles()
        self.player.draw(self.display_surface)

        # dust particles
        self.particle_sprites.update()
        self.particle_sprites.draw(self.display_surface)

        # menu buttons
        self.menu_sprites.update()
        self.menu_sprites.draw(self.display_surface)

        self.display_surface.scroll(self.screen_shake, self.screen_shake)

        self.end_game()
