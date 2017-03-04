# Connect Four

The [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) game, implemented in Python.

> TODO: screenshot

## Features

  - All the Connect Four rules
  - State of the art graphics
  - Two players (of course) on the same computer
  - Sound effects

## Downloads

Go [here](https://github.com/EpocDotFr/connectfour/releases).

There's currently Windows and Mac OS executables available.

## Prerequisites

**If you are a player**:

  - Nothing.

**If you are a developer:**

  - Python 3.5

## Installation

**If you are a player**:

  - Nothing to install.

**If you are a developer:**

Clone this repo, and then the usual `pip install -r requirements.txt`.

## Usage

**If you are a player**:

Just run the executable.

**If you are a developer:**

```
python run.py
```

## Controls

  - <kbd>ESC</kbd> quits the game
  - <kbd>←</kbd> and <kbd>→</kbd> moves the chip respectively to the left and to the right
  - <kbd>↓</kbd> drops the chip in the selected column

## How it works

This game is built on top of [PyGame](http://www.pygame.org/hifi.html). I obviously can't explain how it
works here, so you'll have to jump yourself in the source code. Start with the entry point, `run.py`.

Beside the game itself, I use [PyInstaller](http://www.pyinstaller.org/) to generate the executables. It packs up all the
game and its assets in a single executable file so players just have to run it with nothing to install. This task is
performed by the `build_*` scripts to be ran in the corresponding OS.

## Credits

  - [Board graphics](https://commons.wikimedia.org/wiki/File:Puissance4_01.svg) by François Haffner (public domain)
  - Sound effects are from GoldenEye 007 (Copyright © 1997 Rareware)
  - [Font](http://www.dafont.com/monofur.font) by Tobias Benjamin Köhler (freeware)

## Gotcha

This is my very first game I ever crafted, and my very first projet using PyGame, so please be indulgent.

## End words

If you have questions or problems, you can [submit an issue](https://github.com/EpocDotFr/connectfour/issues).

You can also submit pull requests. It's open-source man!