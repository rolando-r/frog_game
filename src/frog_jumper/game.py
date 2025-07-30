import pygame, random
from .menu import Menu
from .utils import load_image, load_sound
from .entities.frog import Frog
from .entities.leaf import Leaf
from .entities.bird import Bird
from .entities.snake import Snake
from .entities.enemy import Enemy

class Game:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Frog Jumper')
        self.clock = pygame.time.Clock()
        self.assets = self._load_assets()
        self.menu = Menu(self.screen, self.assets)
        self._reset()
        self.scroll_speed = 2
        self.scroll_speed = min(6, self.scroll_speed + 0.001)
        self.score = 0
        self.last_score_update = pygame.time.get_ticks()
        self.countdown_active = False
        self.countdown_start_time = 0
        self.countdown_number = 3

    def _load_assets(self) -> dict:
        return {
            'frog': pygame.transform.scale(load_image('../assets/images/frog.png'), (50, 50)),
            'leaf': pygame.transform.scale(load_image('../assets/images/leaf.png'), (80, 30)),
            'bird': pygame.transform.scale(load_image('../assets/images/bird.png'), (60, 40)),
            'snake': pygame.transform.scale(load_image('../assets/images/snake.png'), (100, 40)),
            'jump': load_sound('../assets/sounds/jump.wav'),
            'lose': load_sound('../assets/sounds/lose.wav'),
        }

    def _reset(self) -> None:
        # Crear la rana
        self.frog = Frog(self.assets['frog'], (400, 550), self.assets['jump'])
        
        # Crear hojas iniciales - asegurar que la rana comience en una hoja
        self.leaves = []
        # Crear hoja inicial donde comenzará la rana
        initial_leaf = Leaf(self.assets['leaf'], (375, 570))  # Posicionada debajo de la rana
        self.leaves.append(initial_leaf)
        
        # Asegurar que la rana comience en la hoja
        self.frog.on_leaf = True
        self.frog.current_leaf = initial_leaf
        
        # Crear otras hojas iniciales
        for i in range(1, 6):
            x = random.randint(50, self.SCREEN_WIDTH - 100)
            y = 500 - i * 80
            if random.random() < 0.05:  # Reducir probabilidad de serpientes iniciales
                self.leaves.append(Snake(self.assets['snake'], (x, y)))
            else:
                self.leaves.append(Leaf(self.assets['leaf'], (x, y)))
        
        self.enemies = pygame.sprite.Group()
        self.state = 'MENU'
        self.game_over_time = None
        self.score = 0
        self.death_reason = ""
        
        # Reset countdown
        self.countdown_active = False
        self.countdown_start_time = 0
        self.countdown_number = 3

    def _start_countdown(self):
        """Inicia la cuenta regresiva antes del juego"""
        self.countdown_active = True
        self.countdown_start_time = pygame.time.get_ticks()
        self.countdown_number = 3

    def _spawn_enemies(self) -> None:
        screen_width = pygame.display.get_surface().get_width()

        # Probabilidad de aparecer un enemigo estático (hoja o serpiente)
        if random.random() < 0.01:
            enemy_type = "snake"
            image = self.assets[enemy_type]
            enemy_rect = image.get_rect()
            enemy_x = random.randint(0, screen_width - enemy_rect.width)
            enemy_y = random.randint(-enemy_rect.height - 100, -enemy_rect.height)
            enemy_rect.topleft = (enemy_x, enemy_y)

            # Verificar si se superpone con otros enemigos
            overlap = any(enemy.rect.colliderect(enemy_rect) for enemy in self.enemies)

            if not overlap:
                self.enemies.add(Enemy(image, (enemy_x, enemy_y)))

        # Probabilidad de aparecer un pájaro (enemigo móvil)
        if random.random() < 0.01:
            bird_image = self.assets["bird"]
            spawn_left = random.choice([True, False])
            y_position = random.randint(50, 150)

            if spawn_left:
                image = pygame.transform.flip(bird_image, True, False)
                bird = Bird(image, (-image.get_width(), y_position), speed=5)
            else:
                image = bird_image
                bird = Bird(image, (screen_width, y_position), speed=-5)

            self.enemies.add(bird)



    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = 'QUIT'
            if self.state == 'PLAY' and not self.countdown_active:
                self.frog.handle_event(event)
            elif self.state == 'MENU':
                selection = self.menu.handle_event(event)
                if selection == 'PLAY':
                    self.state = 'PLAY'
                    self._start_countdown()  # Iniciar cuenta regresiva
                elif selection == 'QUIT':
                    self.state = 'QUIT'
    
    def _update_countdown(self):
        """Actualiza la cuenta regresiva"""
        if not self.countdown_active:
            return True  # El juego puede continuar
        
        elapsed = pygame.time.get_ticks() - self.countdown_start_time
    
        if elapsed >= 3000:  # 3 segundos total
            self.countdown_active = False
            return True  # Terminar cuenta regresiva
        elif elapsed >= 2000:  # 2 segundos
            self.countdown_number = 1
        elif elapsed >= 1000:  # 1 segundo
            self.countdown_number = 2
        else:
            self.countdown_number = 3
        
        return False  # Cuenta regresiva aún activa

    def _check_collisions(self) -> None:
        # Verificar colisiones con enemigos voladores
        for enemy in self.enemies:
            if self.frog.rect.colliderect(enemy.rect):
                self.assets['lose'].play()
                self.state = 'GAME_OVER'
                self.game_over_time = pygame.time.get_ticks()

                if isinstance(enemy, Bird):
                    self.death_reason = "Fuiste golpeado por un pájaro"
                else:
                    self.death_reason = "Colisionaste con un enemigo"
                return

        # Verificar si la rana pisó una serpiente (verificar TODAS las hojas/serpientes)
        for leaf in self.leaves:
            if self.frog.rect.colliderect(leaf.rect):
                # Si es una serpiente, verificar si la tocó de cualquier manera
                if hasattr(leaf, '__class__') and 'Snake' in str(leaf.__class__):
                    self.assets['lose'].play()
                    self.state = 'GAME_OVER'
                    self.game_over_time = pygame.time.get_ticks()
                    self.death_reason = "Pisaste una serpiente"
                    return

        # Verificar si la rana está en el suelo sin hoja
        if self.frog.is_on_ground_without_leaf(self.SCREEN_HEIGHT):
            self.assets['lose'].play()
            self.state = 'GAME_OVER'
            self.game_over_time = pygame.time.get_ticks()
            self.death_reason = "Tocaste el suelo sin estar en una hoja"
            return

        # Verificar si la rana se cayó de la pantalla sin hojas
        if self.frog.is_falling_to_death(self.SCREEN_HEIGHT):
            self.assets['lose'].play()
            self.state = 'GAME_OVER'
            self.game_over_time = pygame.time.get_ticks()
            self.death_reason = "Te caíste al vacío"

    def _update(self):
        if self.state == 'PLAY':
            # Actualizar cuenta regresiva
            game_can_continue = self._update_countdown()
            
            # Actualizar la rana pasándole las hojas y el estado del juego
            self.frog.update(self.leaves, game_can_continue)
            
            # Solo actualizar el resto del juego si no hay cuenta regresiva
            if game_can_continue:
                self._spawn_enemies()

                # Scroll automático
                self.frog.rect.y += self.scroll_speed
                for leaf in self.leaves:
                    leaf.rect.y += self.scroll_speed
                for enemy in self.enemies:
                    enemy.rect.y += self.scroll_speed

                # Eliminar hojas fuera de la pantalla
                self.leaves = [leaf for leaf in self.leaves if leaf.rect.top < self.SCREEN_HEIGHT + 50]

                # Generar nuevas hojas arriba
                if len(self.leaves) < 8:  # Aumentar número de hojas
                    x = random.randint(50, self.SCREEN_WIDTH - 100)
                    y = random.randint(-120, -60)
                    if random.random() < 0.05:
                        self.leaves.append(Snake(self.assets['snake'], (x, y)))
                    else:
                        self.leaves.append(Leaf(self.assets['leaf'], (x, y)))

                # Aumentar puntaje
                now = pygame.time.get_ticks()
                if now - self.last_score_update > 500:
                    self._update_score()
                    self.last_score_update = now

                # Actualizar enemigos
                for enemy in list(self.enemies):
                    enemy.update()
                    if (enemy.rect.right < 0 or enemy.rect.left > self.SCREEN_WIDTH or 
                        enemy.rect.top > self.SCREEN_HEIGHT):
                        self.enemies.remove(enemy)

                self._check_collisions()

        elif self.state == 'GAME_OVER':
            if pygame.time.get_ticks() - self.game_over_time >= 2000:
                self._reset()

    def _draw(self) -> None:
        self.screen.fill((135, 206, 235))  # cielo
        if self.state == 'MENU':
            self.menu.draw()
        elif self.state == 'PLAY':
            # Dibujar elementos del juego
            for leaf in self.leaves:
                leaf.draw(self.screen)
            self.frog.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            # Dibujar puntaje
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))
            
            # Dibujar cuenta regresiva si está activa
            if self.countdown_active:
                countdown_font = pygame.font.SysFont(None, 120)
                countdown_text = countdown_font.render(str(self.countdown_number), True, (255, 0, 0))
                countdown_rect = countdown_text.get_rect(center=self.screen.get_rect().center)
                
                # Fondo semi-transparente
                overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))
                
                # Número de cuenta regresiva
                self.screen.blit(countdown_text, countdown_rect)
                
        elif self.state == 'GAME_OVER':
            # Mensaje principal
            font = pygame.font.SysFont(None, 72)
            text = font.render('GAME OVER', True, (255, 0, 0))
            self.screen.blit(text, text.get_rect(center=self.screen.get_rect().center))

            # Motivo del game over
            small_font = pygame.font.SysFont(None, 36)
            reason_text = small_font.render(self.death_reason, True, (0, 0, 0))
            text_rect = text.get_rect(center=self.screen.get_rect().center)
            reason_rect = reason_text.get_rect(midtop=(text_rect.centerx, text_rect.bottom + 10))
            self.screen.blit(reason_text, reason_rect)

            # Puntaje obtenido
            score_text = small_font.render(f'Score: {self.score}', True, (0, 0, 0))
            score_rect = score_text.get_rect(midtop=(reason_rect.centerx, reason_rect.bottom + 10))
            self.screen.blit(score_text, score_rect)
        pygame.display.flip()

    def run(self) -> None:
        while self.state != 'QUIT':
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(self.FPS)
        pygame.quit()

    def _update_score(self):
        self.score += 1