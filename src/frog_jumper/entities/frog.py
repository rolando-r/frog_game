import pygame
from pygame.sprite import Sprite
from ..utils import scale_image

class Frog:
    JUMP_VELOCITY = -15
    GRAVITY = 0.8
    EXTRA_JUMP_BOOST = -0.8
    MAX_JUMP_TIME = 300
    TERMINAL_VELOCITY = 10  # velocidad máxima de caída

    def __init__(self, image: pygame.Surface, position: tuple[int, int], jump_sound: pygame.mixer.Sound) -> None:
        self.image = scale_image(image, 0.5)
        self.rect = self.image.get_rect(midbottom=position)
        self.velocity_y = 0
        self.jump_sound = jump_sound
        self.jumping = False
        self.jump_time = 0
        self.move_speed = 5
        self.on_leaf = False  # Nueva variable para saber si está en una hoja
        self.current_leaf = None  # Referencia a la hoja actual

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def check_leaf_collision(self, leaves):
        """Verifica colisiones con hojas y maneja el aterrizaje"""
        self.on_leaf = False
        self.current_leaf = None
        
        # Solo verificar colisiones si está cayendo
        if self.velocity_y > 0:
            for leaf in leaves:
                # Verificar si la rana está sobre la hoja
                if (self.rect.colliderect(leaf.rect) and 
                    self.rect.bottom <= leaf.rect.top + 15):  # Margen de tolerancia
                    
                    # Verificar si es una serpiente ANTES de aterrizar
                    if hasattr(leaf, '__class__') and 'Snake' in str(leaf.__class__):
                        # No aterrizar en serpientes, dejar que el juego detecte la colisión
                        continue
                    
                    # Aterrizar en la hoja (solo si NO es serpiente)
                    self.rect.bottom = leaf.rect.top
                    self.velocity_y = 0
                    self.on_leaf = True
                    self.current_leaf = leaf
                    self.jumping = False
                    break

    def update(self, leaves=None, game_active=True) -> None:
        if not game_active:
            return  # No hacer nada durante la cuenta regresiva
            
        keys = pygame.key.get_pressed()
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        # Movimiento lateral (con límites de pantalla)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.move_speed

        # Limitar movimiento lateral dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

        # Salto - SOLO puede saltar si está en una hoja
        if keys[pygame.K_SPACE]:
            if not self.jumping and self.on_leaf:
                self.jumping = True
                self.jump_time = pygame.time.get_ticks()
                self.velocity_y = self.JUMP_VELOCITY
                self.jump_sound.play()
                self.on_leaf = False  # Ya no está en la hoja
                self.current_leaf = None
            elif self.jumping:
                elapsed = pygame.time.get_ticks() - self.jump_time
                if elapsed < self.MAX_JUMP_TIME:
                    self.velocity_y += self.EXTRA_JUMP_BOOST
        else:
            self.jumping = False

        # Aplicar gravedad solo si no está en una hoja
        if not self.on_leaf:
            self.velocity_y += self.GRAVITY
            # Limitar velocidad de caída
            if self.velocity_y > self.TERMINAL_VELOCITY:
                self.velocity_y = self.TERMINAL_VELOCITY

        # Actualizar posición vertical
        self.rect.y += self.velocity_y

        # Verificar colisiones con hojas si se proporcionaron
        if leaves:
            self.check_leaf_collision(leaves)

        # Solo tocar el suelo si no hay hojas disponibles o como respaldo
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.velocity_y = 0
            self.on_leaf = False
            self.current_leaf = None

    def is_on_ground_without_leaf(self, screen_height):
        """Verifica si la rana está en el suelo sin estar en una hoja"""
        return (self.rect.bottom >= screen_height and not self.on_leaf)
    
    def is_falling_to_death(self, screen_height):
        """Verifica si la rana está cayendo sin hojas cerca"""
        return (not self.on_leaf and 
                self.velocity_y > 0 and 
                self.rect.top > screen_height)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)