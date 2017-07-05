# Connect Four
<img src="resources/images/icon_github.png" align="right" />

The [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) game, implemented in Python.

## Features

  - All the Connect Four rules
  - State of the art graphics
  - Chips that made the player win are highlighted
  - Sound effects!
  - Musics!
  - Two players, either:
    - On the same computer
    - (WIP) LAN game
    - (WIP) Online game

## Executables download

Go [here](https://github.com/EpocDotFr/connectfour/releases) to find the latest ones.

The following executables are currently available:

  - Windows (64 bits). Tested on Windows 7 / 10
  - Mac OS (64 bits). Tested on Mac OS Sierra

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
python run.py [--muted] [--dev]
```

## Controls

  - <kbd>ESC</kbd> quits to the menu or close the game when already on the menu
  - <kbd>←</kbd> and <kbd>→</kbd> moves the chip respectively to the left and to the right
  - <kbd>↓</kbd> drops the chip in the selected column
  - <kbd>↵</kbd> starts a new game when one is finished

## How it works

This game is built on top of [PyGame](http://www.pygame.org/hifi.html). I obviously can't explain how it
works here, so you'll have to jump yourself in the source code. Start with the entry point, `run.py`.

Beside the game itself, I use [PyInstaller](http://www.pyinstaller.org/) to generate the executables. It packs up all the
game and its assets in a single executable file so players just have to run it with nothing to install. This task is
performed by the `build_*` scripts to be ran in the corresponding OS.

Network gaming is done by [WebSockets](https://en.wikipedia.org/wiki/WebSocket) using [Autobahn](http://autobahn.ws/python/).
A [master server](https://github.com/EpocDotFr/connectfour-master-server) (with the help of a [REST](https://en.wikipedia.org/wiki/Representational_state_transfer)
API) is used to centralize all Connect Four games.

## Credits

  - Board graphics by [François Haffner](https://commons.wikimedia.org/wiki/File:Puissance4_01.svg) (public domain)
  - Sound effects by [Freesfx.co.uk](http://www.freesfx.co.uk/) (© Freesfx.co.uk)
  - Musics by [SoundImage.org](http://soundimage.org/) (Royalty-Free)
  - Font by [Tobias Benjamin Köhler](http://www.dafont.com/monofur.font) (freeware)
  - Thanks to the [Swervin Mervin](https://github.com/buntine/SwervinMervin) game's source code who helped me a lot to properly design the architecture of my game and understand the PyGame mechanics
  - Connect Four™ is a trademark of Milton Bradley / Hasbro. This project isn't supported nor endorsed by Milton Bradley / Hasbro

## Gotcha

This is my very first game I ever crafted, and my very first projet using PyGame, so please be indulgent.

## End words

If you have questions or problems, you can [submit an issue](https://github.com/EpocDotFr/connectfour/issues).

You can also submit pull requests. It's open-source man!