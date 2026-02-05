# Existance Macro

![Discord](https://img.shields.io/discord/1065032948119769118?label=Discord&color=7289da&logo=discord&logoColor=white&link=https://discord.gg/WdbWgFewqx)
![GitHub Repo stars](https://img.shields.io/github/stars/LaganYT/Existance-Macro?style=flat&label=Stars&color=fff240&logo=github&logocolor=white&link=https://github.com/LaganYT/Existance-Macro/stargazers)
![Repo Size](https://img.shields.io/github/repo-size/LaganYT/Existance-Macro?label=Repo%20Size&logo=github&logoColor=white)

Roblox Bee Swarm Simulator macro for macOS. Free, open source, and actively maintained.

- Docs: https://existance-macro.gitbook.io/existance-macro-docs/
- Discord: https://discord.gg/3qf8bgqCVu (Original Macro)
- Original Macro: https://github.com/existancepy/bss-macro-py

![GUI](https://github.com/LaganYT/Existance-Macro/blob/06dd4987b68053c9bdfa842a17e51db3b7c83d30/src/gui.png)

## Features

- **Home / Control**

  - Start/stop via UI, hotkeys (F1 start, F3 stop; may require Fn), or Discord commands
  - One-click updater preserves `settings/` (profiles, patterns, paths)
  - Task list shows enabled tasks and execution order
  - Field-only mode for gathering-only operation
  - Planter timer management with visual countdowns
  - Real-time log monitoring with detailed/simple views

- **Gather**

  - Farm up to 5 fields with Natro-compatible settings
  - Patterns (shapes), size/width, invert axes, direction and turns
  - Shift-lock handling and field drift compensation (Saturator tracking)
  - Time- or backpack%-based stop conditions
  - Return-to-hive methods: Reset, Walk, Rejoin, Whirligig
  - Select start location and distance per field

- **Collect**

  - Regular dispensers (e.g., Wealth Clock, Glue, boosters, etc.)
  - Sticker Printer with egg availability detection
  - Beesmas dispensers (seasonal)
  - Memory Match (regular/mega/extreme/winter) completion
  - Blender craft/collect up to 3 items with quantity and repeat/inf modes
  - Remote enable/disable via Discord commands
  - Comprehensive collectible management system

- **Kill**

  - Regular mob runs (ladybug, rhino, werewolf, etc.) with respawn modifiers
  - Bosses: Vicious Bee (Stinger Hunt), Stump Snail, Coconut Crab
  - Night detection logic for Stinger Hunt field route
  - Optional Ant Challenge
  - Remote mob configuration via Discord
  - Vicious Bee detection with Discord notifications

- **Boost**

  - Hotbar scheduling: when and how often to trigger slots
  - Buffs: Field Boosters with spacing and gather-in-boosted-field priority
  - Sticker Stack activation (stickers or tickets) and optional Hive Skins

- **Planters**

  - Tracks placed planters and growth timing across cycles
  - Harvest by interval or when full; clear timers when needed
  - Up to 3 planters per cycle, loops cycles automatically
  - Gather in planter field and optional Glitter usage
  - Visual timer management in web interface
  - Auto-planter ranking system with optimal placement
  - Manual and automatic planter modes

- **Quests**

  - Quest-oriented gathering logic and settings (WIP; see docs)

- **Discord Bot**

  - Remote control via Discord commands (start, stop, pause, resume, skip)
  - Field management (enable/disable fields, swap fields, field-only mode)
  - Quest and collectible management
  - Mob run configuration
  - Real-time status updates and screenshots
  - Automatic stream URL pinning when streaming is enabled

- **Live Streaming**

  - Real-time screen streaming through web interface
  - Cloudflared tunnel integration for public access
  - Adaptive quality and FPS optimization
  - Mobile-friendly responsive design
  - Automatic reconnection and error handling

- **Hourly Reports & Analytics**

  - Detailed performance tracking with honey/minute statistics
  - Buff detection and uptime monitoring
  - Planter data integration
  - Historical data with trend analysis
  - Visual reports with charts and statistics
  - Automatic Discord webhook delivery

- **Web Interface**

  - Modern, responsive web-based GUI
  - Real-time log monitoring with detailed/simple views
  - Planter timer management
  - Field-only mode toggle
  - Task list visualization
  - Cross-platform accessibility

- **Notifications & Webhooks**
  - Discord webhook integration for events
  - Configurable ping notifications for:
    - Critical errors and disconnects
    - Character deaths and Vicious Bee spawns
    - Mondo Chick buffs and Ant Challenges
    - Sticker events and mob spawns
    - Conversion events and hourly reports
  - Screenshot capture and delivery
  - Stream URL sharing with auto-pinning

## Getting Started

For requirements, installation, recommended system/Roblox settings, and usage guides, see the docs:

https://existance-macro.gitbook.io/existance-macro-docs/

## Notes

- Designed for macOS.
- This project and documentation are a work in progress but actively supported.
