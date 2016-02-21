# Intro

A mini fighting (Python) game to be run locally on the Python console, inspired by [this Udacity Object Oriented Programming Code](https://www.udacity.com/wiki/wiki-game). Use this to practice OOP.

# Usage

Note, these instructions are not elegant. I'm yet to learn / master / write clean Python OOP codes.

Navigate to the projecOpen up a python console:

```
$ python3
Python 3.4.4 (v3.4.4:737efcadf5a6, Dec 19 2015, 20:38:52)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from game_v1 import *
```

Then try out all sort of OOP commands:

e.g.

```.py
>>> alice = Character(10,10,100)
>>> bob = Character(11,10,100)
>>> bob.gain_protection()
>>> alice.attack(bob)
>>> bob.attack(alice)
>>> bob.__dict__
{'items': [], 'hp': 100, 'x': 11, 'y': 10, 'protection': 0}
>>> alice.__dict__
{'items': [], 'hp': 90, 'x': 10, 'y': 10, 'protection': 0}
>>> bob.gain_protection()
>>> bob.__dict__
{'items': [], 'hp': 100, 'x': 11, 'y': 10, 'protection': 4}
>>> bob.gain_protection()
>>> bob.__dict__
{'items': [], 'hp': 100, 'x': 11, 'y': 10, 'protection': 8}
>>> alice.__dict__
{'items': [], 'hp': 90, 'x': 10, 'y': 10, 'protection': 0}
```

# Future Enhancement

It is hope that over time my OOP skill will improve and be able to improve this fighting game further / make code base cleaner.