# Making your own custom content (paths, patterns)

Disclaimer: Python knowledge is required

## Patterns
Patterns are stored as python files in settings -> patterns

To make your own pattern, create a new .py file (name is up to you) in the patterns folder and start coding!

You can reference other patterns in the folder to see how its done

### How patterns are run
Patterns are ran using [exec](https://www.geeksforgeeks.org/exec-in-python/) within a class function

Below is a simplified version:
```python
def gather(self):
    while True:
        exec(open(f"../settings/patterns/pattern.py").read())
```

### Size and Width
The variables `size`, `sizeword` and `width` can be used for the pattern's size and width. 


They are already defined in the gather function, so there is no need to define them in your own pattern.

- `width` refers to the setting's width
- `sizeword` refers to the setting's size (eg, xs, s, etc)
- `size` is a float that represents the size (`sizeword`) converted to a number

This is the default mapping of sizeword to size.
```python
sizeData = {
    "xs": 0.25,
    "s": 0.5,
    "m": 1,
    "l": 1.5,
    "xl": 2
}
size = sizeData[sizeword]
```
You can create your own custom mapping for the size in the pattern's code by overriding the `size` variable

Here is an example of a custom size (cornerxe_lol.py)

```python
if sizeword.lower() == "xs":
    size = 0.5
elif sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "l":
    size = 2
elif sizeword.lower() == "xl":
    size = 2.5
else:
    size = 1.5
```

### Movement

Movement is done through the keyboard module (src -> modules -> controls -> keyboard.py)

#### self.keyboard.keyDown(key, pause = True)
**Description:**  

Presses the specified key down

**Parameters:**  

- key: key to press
- pause: if the program should wait 0.1s after pressing the key

**Example:**

```python
  self.keyboard.keyDown("a") #press down the a key
```

#### self.keyboard.keyUp(key, pause = True)
**Description:**  

Releases the specified key

**Parameters:**  

- key: key to release
- pause: if the program should wait 0.1s after releasing the key

**Example:**

```python
  self.keyboard.keyUp("a") #release the a key
```

#### self.keyboard.press(key, delay = 0.02)
**Description:**  

Presses a key for a specified duration 

**Parameters:**  

- key: key to press
- delay: how long to press the key for (in secs)

**Example:**

```python
  self.keyboard.press("a", 1) #press down the a key for 1s, then release it
```

#### self.keyboard.walk(k, t, applyHaste = True)
**Description:**  

Presses a key for a specified duration, but accounts for the player's walkspeed and compensates the duration accordingly 

The formula for calculating the duration: newT = t*28/player_movespeed

**Parameters:**  

- k: key to press
- t: how long to press the key for at 28 movespeed (in secs)
- applyHaste: include haste compensation when calculating the duration. If disabled, it will use the player's base walkspeed instead

**Example:**

```python
  self.keyboard.walk("a", 1) #press down the a key for 1s, then release it
```

#### self.keyboard.multiWalk(keys, t)
**Description:**  

Presses multiple keys for a specified duration, accounts for the player's walkspeed and compensates the timing accordingly 

The formula for calculating the duration is the same as keyboard.walk

Note: this function does not have a applyHaste parameter, it will always compensation for haste

**Parameters:**  

- keys: a list of keys to press
- t: how long to press the key for at 28 movespeed (in secs)

**Example:**

```python
  self.keyboard.multiWalk(["a", "d"], time) #press down the a and d keys for 1s, then release them
```

#### self.keyboard.tileWalk(key, tiles)
**Description:**  

Presses a key for a specified number of in-game tiles, accounts for the player's walkspeed and compensates the timing accordingly. A tile is a grass tile

Note: this function does not have a applyHaste parameter, it will always compensation for haste

This function converts the tiles into seconds, then presses the key for that duration.
The formula is: secs = tiles/8.3

**Parameters:**  

- keys: a list of keys to press
- tiles: how many tiles the program should walk for. Accepts float values

**Example:**

```python
  self.keyboard.tileWalk("a", 7) #press down the a key for 7 tiles
```


