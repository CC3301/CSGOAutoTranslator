# CSGO Chat Autotranslator

BROKEN SINCE CS2 - i can't be bothered to make a new version/update this tool since cs2 sucks anyway and y'all should stop playing and touch grass.

## Motivation
Have you ever played matchmaking and ended up copy&pasting chat messages just so you can understand what your teammates or enemies are saying?
This software reads the console log output of CS:GO and trys to filter out chat-messages. It then sends those to google translate, along with a desired output language.
You are then left with a translated message, much the same as if you just copied it into google translate manually. This is just much more convienient and saves you some 
annoying clicks.

## Usage

### Prepare your CS:GO Installation
This Software connects to CS:GO's RCON-Port, which can be enabled using the launchoption `-netconport <port>`. By default the software expects CS:GO's RCON to listen on port `2121`.

## Important Notes

1. All persistant settings and last-used values are stored in `$HOME/.csgoatt.appstate` as a json string.
2. If this file does not exist, default values will be used.

## Dependencies

1. [googletrans](https://pypi.org/project/googletrans/)
2. [PyQt6](https://pypi.org/project/PyQt6/)

## Disclaimer
Although the developer of this software does not see any risk of getting VAC banned for using this software, there is no guarantee. If you get VAC banned for using this software
be aware of this disclaimer. The developer cannot be held accountable if your account gets VAC banned. Use at your own risk.
