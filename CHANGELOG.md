# Changelog

All notable changes to the Space Conquer game will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-02

### Added
- Death animations for low-type enemies with particle effects, rings, and flash effects
- Custom sound effects for enemy destruction
- Shield system for super-type enemies that protects health until depleted
- Dynamic attack patterns for super-type enemies:
  - Bullets when shield is active
  - Lasers with 3-second cooldown when shield is broken
- Visual feedback for shield status and laser attacks
- Strategic gameplay: enemies stop moving when firing lasers

### Changed
- Enhanced visual effects with gradient colors and rotation for bullets
- Improved collision detection for all bullet types
- Different explosion colors based on enemy type
- Optimized codebase with removal of redundant files

### Fixed
- Fixed glitchy appearance of super-type enemy bullets
- Fixed collision detection for bullets with velocity components
- Fixed various bugs and glitches in enemy behavior
## [1.0.0] - 2025-06-24

### Added
- Initial release of Space Conquer game
- Multiple enemy types with different behaviors
- Power-up system (health, speed, rapid fire)
- Sound effects with volume control
- Background music with separate volume control
- Settings menu with volume sliders
- Increasing difficulty over time
- Score tracking system
- Modular code structure for better maintainability
