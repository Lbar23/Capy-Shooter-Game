# Capy's Christmas Nightmare

## Game Description
**Capy's Christmas Nightmare** is a top-down shooter where players control Capy, a capybara trapped in a nightmare. In a frozen wasteland, terrifying enemies chase Capy, and she must defend herself with her makeshift wooden gun, which fires her favorite food—watermelon. The goal is to survive as long as possible while eliminating enemies.

## Game Information
- **Genre:** Top-down shooter
- **Skill Rating:** 10+
- **Target Audience:** Males and females aged 10 and older

## Game Objectives
- Survive against waves of nightmare creatures
- Use Capy's watermelon gun to defeat enemies
- Navigate a frozen landscape filled with obstacles

## Game Mechanics
### **Enemy Spawning**
- Enemies spawn randomly across the map, both on-screen and off-screen.
- They track the player’s location and move toward Capy.

### **Shooting the Gun**
- The gun follows the mouse cursor in 360-degree motion.
- Left-clicking fires a watermelon projectile.
- Hitting an enemy with a watermelon kills it and increases the score.

### **Health & Score**
- The player has a limited health bar that decreases upon enemy contact.
- No immunity frames, so damage continues as long as Capy is in contact with an enemy.
- The score increases with every enemy defeated.
- The score is displayed in real-time and on the game-over screen.

## Entities
### **Player Character**
- Capy is controlled using **WASD** or **arrow keys**.
- A capybara sprite sheet is used for animations.

### **Enemies**
- Enemies glide across the screen towards Capy.
- Sprites are adapted from Terraria.
- Colliding with Capy deals damage.
- A hit from a watermelon projectile eliminates an enemy and increases the score.

## Background & Environment
- The game world is a **Frozen Wasteland** created with **pytmx**.
- The tilemap includes obstacles such as trees and rocks that Capy must navigate around.


## Setup
Run the game:
   ```sh
   python main.py
   ```

## How to Play
- Use **WASD** or **arrow keys** to move Capy.
- Aim using the **mouse cursor**.
- **Left-click** to shoot watermelon projectiles.
- Avoid enemy contact to preserve health.
- Survive as long as possible while increasing your score!

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contributors
- **Luis Barrera**

## Acknowledgments
- All sprites are not made by me
- Developed as part of **CPSC 4160/6160** coursework

