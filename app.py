import random
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 'blue')
        self.speed = 10
        self.ammo = 5

    def move(self, direction):
        if direction == 'up' and self.y > 0:
            self.y -= self.speed
        elif direction == 'down' and self.y < 550:
            self.y += self.speed
        elif direction == 'left' and self.x > 0:
            self.x -= self.speed
        elif direction == 'right' and self.x < 750:
            self.x += self.speed

class Obstacle(GameObject):
    def __init__(self, color, speed):
        super().__init__(random.randint(0, 750), -50, 50, 50, color)
        self.speed = speed

    def move(self):
        self.y += self.speed

class Projectile(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 20, 'black')
        self.speed = 15

    def move(self):
        self.y -= self.speed

class Game:
    def __init__(self):
        self.player = Player(375, 550)
        self.obstacles = []
        self.projectiles = []
        self.score = 0
        self.game_over = False
        self.start_time = time.time()

    def update(self):
        if self.game_over:
            return False

        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # Increase obstacle speed over time
        base_speed = 2
        speed_increase = min(3, elapsed_time / 30)  # Cap at 5 after 90 seconds
        
        # Move obstacles and handle collisions
        new_obstacles = []
        for obs in self.obstacles:
            obs.move()
            if obs.y < 600:
                new_obstacles.append(obs)
            elif obs.color == 'red':
                self.score += 1
            
            if self.check_collision(self.player, obs):
                if obs.color == 'red':
                    self.game_over = True
                    return False
                elif obs.color == 'green':
                    self.score += 10
                elif obs.color == 'black':
                    self.player.ammo = min(self.player.ammo + 5, 100)  # Cap ammo at 100

        self.obstacles = new_obstacles

        # Move projectiles and handle collisions
        new_projectiles = []
        for proj in self.projectiles:
            proj.move()
            if proj.y > 0:
                new_projectiles.append(proj)
                for obs in self.obstacles:
                    if self.check_collision(proj, obs):
                        if obs.color == 'green':
                            self.score += 10
                        elif obs.color == 'black':
                            self.player.ammo = min(self.player.ammo + 5, 100)  # Cap ammo at 100
                        self.obstacles.remove(obs)
                        new_projectiles.remove(proj)
                        break
        self.projectiles = new_projectiles

        # Add new obstacles
        if random.random() < 0.02:
            color = random.choices(['red', 'green', 'black'], weights=[0.7, 0.25, 0.05])[0]
            speed = base_speed + speed_increase if color == 'red' else base_speed
            self.obstacles.append(Obstacle(color, speed))

        # Add ammo every 50 points
        if self.score > 0 and self.score % 50 == 0 and self.score // 50 > (self.score - 1) // 50:
            self.player.ammo = min(self.player.ammo + 5, 100)  # Cap ammo at 100

        return True

    def shoot(self):
        if self.player.ammo > 0:
            self.projectiles.append(Projectile(self.player.x + 20, self.player.y))
            self.player.ammo -= 1

    def check_collision(self, obj1, obj2):
        return (obj1.x < obj2.x + obj2.width and
                obj1.x + obj1.width > obj2.x and
                obj1.y < obj2.y + obj2.height and
                obj1.y + obj1.height > obj2.y)

    def reset(self):
        self.__init__()

game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('move')
def handle_move(direction):
    if not game.game_over:
        game.player.move(direction)
        emit('update', get_game_state())

@socketio.on('shoot')
def handle_shoot():
    if not game.game_over:
        game.shoot()
        emit('update', get_game_state())

@socketio.on('update')
def handle_update():
    if game.update():
        emit('update', get_game_state())
    elif game.game_over:
        emit('game_over', {'score': game.score})

@socketio.on('reset')
def handle_reset():
    game.reset()
    emit('update', get_game_state())

def get_game_state():
    return {
        'player': {'x': game.player.x, 'y': game.player.y, 'ammo': game.player.ammo},
        'obstacles': [{'x': obs.x, 'y': obs.y, 'color': obs.color} for obs in game.obstacles],
        'projectiles': [{'x': proj.x, 'y': proj.y, 'color': proj.color} for proj in game.projectiles],
        'score': game.score
    }

if __name__ == '__main__':
    socketio.run(app, debug=True)