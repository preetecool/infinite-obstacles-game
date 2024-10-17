# Infinite Obstacles Game

A real-time, browser-based arcade game built using **Python**, **Flask**, **Socket.IO**, **HTML5 Canvas**, and **JavaScript**. The player navigates through an infinite series of obstacles, with dynamic difficulty scaling over time. Players can shoot projectiles to clear obstacles while managing their ammo and score.

## Features

- **Real-time gameplay** using WebSockets (Socket.IO) for seamless player movement and shooting.
- **Dynamic obstacles** that increase in speed over time to challenge the player.
- **Collision detection** for player, obstacles, and projectiles.
- **Responsive UI** with real-time score and ammo tracking.
- Built with **Python** and **Flask** for the backend, and **HTML5 Canvas** for rendering.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO

### Installation

1. Clone the repository:

 ```bash
   git clone https://github.com/yourusername/infinite-obstacles-game.git
   cd infinite-obstacles-game
   ``` 

2. Install the required dependencies:
 ```bash
   pip install Flask Flask-SocketIO
```
3. Run the Flask app:

 ```bash
 python app.py
```

4. Open your browser and navigate to http://127.0.0.1:5000 to play the game.

### Controls

Arrow Keys / WASD: Move the player
Space Bar: Shoot projectiles
