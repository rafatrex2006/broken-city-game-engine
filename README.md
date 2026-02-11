# Broken City — Custom 2D Game Engine in Python (Pygame)

This project is a fully custom 2D game engine written from scratch in Python using Pygame.

What started as a single-file prototype later grew into a modular, multi-file architecture to resemble how real game engines and software projects are structured.

The goal of this project was not just to make a game, but to implement the core systems behind a game, including animation handling, level management, cutscenes, UI systems, and a custom level editor, all organized into a clean multi-module architecture.

## Features

- Custom animation system for player, enemies, and bosses
- Enemy AI and boss fight mechanics
- Tile-based level system with auto-tiling
- Integrated level editor for building terrain
- Cutscene engine
- Scene and level selector UI
- Particle system
- Structured asset loading and shared state management
- Modular project architecture (engine, entities, systems, levels, editor)

## Project Structure
engine/ → game loop, state management, asset loading, pygame setup
entities/ → player, enemies, boss, particles, weapons
systems/ → UI, cutscenes
levels/ → map and tile logic
editor/ → standalone level editor
assets/ → pixel art, sounds, level data

## How to Run

Install dependencies:
pip install -r requirements.txt

Run the game:
python main.py

## About

All pixel art, animations, and systems were created from scratch as part of this project.

