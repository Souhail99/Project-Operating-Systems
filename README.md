# Project-Operating-Systems
# Shell

Souhail AIT LAHCEN 

Project from this [source](https://vqhuy.github.io/teaching/linux/project).

## Usage of the script

First you need to import this :

```py
import os
import sys
import subprocess
```

In this repository, you find my reports which explain the code (even if I have some block comments in my script .py) and in some examples of code necessary for the project.

## Launch :

We have two different way to lauch this script :

```bash
python3 mysh.py
```

Or :

```bash
"/home/guignole/Documents/Projet OS/mysh.py"
```
In the second case, you need to write the entire path.

For the Batch Mode, we can have this :

```bash
python3 mysh.py test.sh
```

Or :

```bash
"/home/guignole/Documents/Projet OS/mysh.py" test.sh
```

Or :

```bash
./mysh.py test.sh
```

For this three second case (without python3), I use this in my first line in script :

```py
#!/usr/bin/env python
```
To allow the user not to have to write python3 if you know the full path (like in two previous examples with a path).
