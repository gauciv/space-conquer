# Space Conquer - Enemy Types Analysis

## Overview of Enemy Types

The game features several distinct enemy types, each with unique movement patterns, attack behaviors, and visual characteristics. This document provides a detailed analysis of each enemy type.

## 1. Low-Type Enemy (Drifter)

### Characteristics
- **Health**: 1 hit point
- **Speed**: Base speed of 2 (slower than other enemies)
- **Points**: 30 points when destroyed
- **Visual**: Basic enemy with a flickering light
- **Hitbox**: 80% of sprite size

### Movement Pattern: "drifter"
- Moves horizontally from right to left at a moderate pace
- Features a "stutter" behavior where it occasionally slows down to 50% speed
- Can perform random vertical "dashes" in either up or down direction
- Dash chance: 0.5% per frame
- Dash duration: 0.3-0.6 seconds
- Dash cooldown: 2-4 seconds

### Attack Pattern
- Can only shoot once during its lifetime
- Prepares to shoot when within range (15 pixels from right edge)
- Has a visual telegraph (flashing) for 0.8 seconds before shooting
- Fires a single horizontal shot to the left
- Will only shoot if the player is on the same horizontal line
- Stops moving horizontally during shot preparation

### Visual Effects
- Features a flickering light that brightens during shot preparation
- Engine glow on the left side (since it moves right to left)
- Visual flash effect when preparing to shoot

## 2. Elite-Type Enemy (Zigzag)

### Characteristics
- **Health**: 1 hit point
- **Speed**: Base speed of 8 (much faster than other enemies)
- **Points**: 45 points when destroyed
- **Visual**: Triangular/fast enemy with trail effects
- **Hitbox**: 70% of sprite size (smaller, harder to hit)

### Movement Pattern: "zigzag"
- Moves horizontally from right to left at high speed
- Features a "burst" capability that doubles its speed temporarily
- Burst speed: 12 (extremely fast)
- Burst duration: 0.6 seconds
- Has player targeting capability
- Can detect player within 250 pixels ahead
- Will attempt to align with player vertically before bursting

### Attack Pattern
- Does not have a direct attack pattern in the code
- Relies on collision damage from its high-speed movement

### Visual Effects
- Trail effect behind the enemy emphasizing its speed
- Enhanced trail during burst mode
- Orange/yellow engine glow that intensifies during burst
- Visual telegraph (flashing) before burst
- Energy particles during burst mode

## 3. Super-Type Enemy (Juggernaut)

### Characteristics
- **Health**: 4 hit points (highest of regular enemies)
- **Speed**: Base speed of 1.5 (slowest of all enemies)
- **Points**: 100 points when destroyed
- **Visual**: Larger, tank-like enemy
- **Hitbox**: 90% of sprite size (larger target)

### Movement Pattern: "juggernaut"
- Slow, deliberate tank-like movement
- Moves horizontally with slight vertical bobbing
- Can track the player vertically at a slow pace
- Features a charge attack that increases speed temporarily
- Charge speed: 2.5 (faster than base speed)
- Charge duration: 0.8-1.2 seconds
- Charge cooldown: 6-9 seconds
- Will retreat after charging

### Attack Pattern
- Has multiple attack types based on its current phase:
  1. **Phase 1** (3-4 health): Shield pulse or single shot
  2. **Phase 2** (2 health): Twin shots
  3. **Phase 3** (1 health): Missile barrage
- Attack cooldown varies by phase (3-4s in Phase 1, 2.5-3.5s in Phase 2, 2-3s in Phase 3)
- All attacks have a 0.8 second telegraph warning
- Shield pulse: Creates an expanding shield that can knock back the player
- Single shot: Fires a large purple energy bolt
- Twin shot: Fires two purple energy bolts at different angles
- Missile barrage: Fires five homing missiles in a spread pattern

### Shield System
- Has a one-hit shield that absorbs damage
- Shield regenerates after a cooldown (6 seconds) if in Phase 1
- Can perform a shield pulse attack if shield is active

### Visual Effects
- Shield visualization with gradient effect
- Shield pulse expanding effect
- Engine flare during charge
- Damage flash effect when hit
- Sparks appear when in critical condition (Phase 3)
- Visual warnings before attacks
- Health bar indicator

## 4. Mini-Boss (Vanguard)

### Characteristics
- **Health**: 50 hit points
- **Speed**: 2
- **Points**: 750 points when destroyed
- **Visual**: 1.5x scaled boss sprite
- **Hitbox**: 85% of sprite size

### Movement Pattern: "sine"
- Enters from the right side of the screen
- Positions itself 15 pixels from the right edge
- Moves in a sine wave pattern vertically
- Amplitude: 100 pixels (how far up/down it moves)

### Attack Pattern
- Shoots every 1000 milliseconds (1 second)
- Fires 2 bullets simultaneously
- Bullets move horizontally to the left at speed 8
- Each bullet deals 1 damage

### Visual Effects
- Health bar at the top of the screen
- Death animation with explosion particles
- Fading effect during destruction

## 5. Main Boss (Dreadnought)

### Characteristics
- **Health**: 100 hit points
- **Speed**: 1.5
- **Points**: 1500 points when destroyed
- **Visual**: 0.975x scaled boss sprite
- **Hitbox**: 85% of sprite size

### Movement Pattern: "complex"
- Enters from the right side of the screen
- Positions itself 15 pixels from the right edge
- Changes vertical direction randomly every 60-180 frames
- Stays within screen boundaries

### Attack Pattern
- Shoots every 800 milliseconds (0.8 seconds)
- Fires 3 bullets in a spread pattern:
  - One straight bullet
  - One angled upward (with vertical velocity)
  - One angled downward (with vertical velocity)
- Bullets move horizontally to the left at speed 10
- Each bullet deals 2 damage

### Visual Effects
- Health bar at the top of the screen
- Death animation with explosion particles
- Fading effect during destruction

## Enemy Bullet Types

### Standard Bullets
- Simple projectiles moving in a straight line
- Different colors based on enemy type
- Typically deal 1 damage

### Juggernaut Projectiles
- Larger, more visible projectiles
- Can be aimed at the player
- Purple energy bolts for standard attacks

### Homing Missiles
- Used by Super-type enemy in Phase 3
- Track the player's position
- Have a limited lifetime (5 seconds)
- Feature a visual trail effect
- Orange color to distinguish from other projectiles

### Boss Bullets
- Larger than standard enemy bullets
- Can have vertical velocity components for angled shots
- Mini-boss bullets deal 1 damage
- Main boss bullets deal 2 damage

## Difficulty Progression

The enemy behavior system incorporates several mechanisms for increasing difficulty over time:

1. **Speed Multiplier**: All enemies have a speed multiplier property that can be increased as the game progresses
2. **Phase System**: Super-type enemies become more aggressive as they take damage
3. **Berserk Mode**: Super-type enemies enter a berserk mode at critical health, increasing speed by 20%
4. **Boss Progression**: The game features a mini-boss at the 1:30 mark and a final boss at the 3:00 mark

## Visual Feedback

The game provides rich visual feedback for enemy behaviors:

1. **Telegraph Effects**: Enemies flash or change appearance before attacks
2. **Damage Indicators**: Enemies flash when taking damage
3. **Health Bars**: Displayed for enemies with multiple hit points
4. **Engine Effects**: Glow effects indicate movement direction and intensity
5. **Trail Effects**: Visual trails emphasize speed and movement
6. **Shield Visualization**: Super-type enemies display shield status
7. **Attack Warnings**: Visual indicators before attacks
8. **Death Animations**: Especially elaborate for bosses
