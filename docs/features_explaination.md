# Features guide
This is a guide that aims to explain the features more in-depth

## 1. Home tab

### Starting and stopping the macro
You can start/stop the macro by pressing the start/stop button. Alternatively, you can also use hotkeys to do so. f1 to start, f3 to stop. On some macs, you'll need to press fn alongside the f1/f3 key as those keys could be binded to the brightness settings by default

### Update
The update button deletes the current macro version and downloads the latest version. It does not delete the settings folder, so any profiles, patterns or paths remain unchanged

### Tasks
The task list is a easy way for you to see what tasks you have enabled. It also represents the general order that the tasks are done in. (The higher up the task, the earlier it will be done). Certain tasks (mondo chick and stinger hunt) are high priority, meaning that they do not follow the order dictated by the task list. These tasks are done right after each task.

## 2. Gather
The gather tab allows you to enable up to 3 fields for the macro to gather in. The gather settings are the same as natro macro, so the settings should work the same

### Use shift lock
Use shift lock when gathering. The macro will toggle it on before gathering, then toggle it off afterwards.

### Field Drift Compensation
The macro searches for the supreme saturator after each pattern and moves towards it. It does that by looking for the brightly-colored blue pixels that indicate the location of the saturator.

### Shape (aka pattern)
This determines the pattern that the macro walks in when gathering. You can also import new patterns by adding the pattern's .py file in settings -> patterns

### Size
This determines the size of the pattern. Size affects each pattern differently, its entirely up to the pattern's creator to decide how size works for that pattern

### Width
Similar to size, width also determiens the size of the pattern. It also affects each pattern differently

### Invert Left/Right
Invert the left and right keys of the pattern. Instead of going left, the macro will go right and vice versa

### Invert Forward/Back
Invert forward and backward keys of the pattern. Instead of going forwards, the macro will go backwards and vice versa

### Direction
The direction to turn the camera in before gathering. The initial direction the macro faces varies from field to field. Below is a table of fields and their initial direction. It is the same as Natro Macro

*Note: North is the direction in which the player faces away from the hive*
| Field | Initial Direction |
| --- | --- |
| Sunflower | West |
| Dandelion | East |
| Mushroom | North |
| Blue Flower| East |
| Clover | South |
| Strawberry | West |
| Spider | North |
| Bamboo | East |
| Pineapple | North |
| Stump | East |
| Cactus | South |
| Pumpkin | North |
| Pine Tree | North |
| Rose | West |
| Mountain Top | South |
| Pepper | West |
| Coconut | South |

### Turn X times
The number of times to turn in the specified direction

### Mins
The maximum number of the minutes the macro will gather for. Decimals are accepted. Note that the macro will also stop gathering if it reaches the specified backpack%

### Backpack%
The minimum backpack capacity (in percent) that the macro will gather for. Note that the macro will also stop gathering if it reaches the specified mins

### Return to hive
The method used to return to hive.

- **Reset** -> The macro resets. This is the fastest and most reliable way to return to hive, but causes the player to lose all stored pollen in the backpack. As such, its preferred for blue hives, where most of their pollen is stored in balloons instead

- **Walk** -> The macro walks from the field to the hive. Generally the best return to hive method. While this is the least reliable walk to hive method, its reliability tends to vary based on the field. Some fields tend have more consistent walk paths than others

- **Rejoin** -> The macro rejoins the game, then claims a hive. A good alternative if walk is too unreliable to be used. Blue hives should use reset instead

- **Whirligig** -> The macro uses a whirligig to get to hive. A reliable option, but has a limited number of uses, making it unsuitable for long periods of macroing. Note that if the player runs out of whirligigs, the macro will be able to detect that and walk back to hive instead.

### Start Location
Which section of the field the macro should farm in. The direction of the sections are determined by the initial direction the macro faces when it lands in the field (see: Direction). It is the same as Natro Macro

### Distance
The distance the macro should travel from the center of the field to the specified start location. This setting does nothing if the start location is set to center. It is the same as Natro's Macro

## 3. Collect
This tab is primarily focused on collecting dispensers, which the exception of those that gives the player buffs (such as the field boosters)

### Regular
Collect dispensers

### Sticker Printer
The macro collects a sticker from the sticker printer. The macro is able to detect if the player runs out of the required eggs, in which case it will not attempt to print the sticker

### Beesmas
Collect dispensers related to the beesmas event

### Memory Match
The macro completes the memory match. Note that there is no item prioritisation, so the macro will aim to get as many matches as possible

### Blender
The macro can craft and collect up to 3 items in the blender. Note that if there is already an item crafting, the macro will detect it's completion time and wait for the crafting process to be completed before starting on the blender cycle.

- **Quantity** -> The number of items to craft at one time. Enabling the max setting makes it craft the maximum number of items possible

- **Repeat** -> The number of times the macro can craft the item. Enabling the inf setting makes it crafts the item indefinitely.

## 4. Kill
This tab is focused on killing mobs and bosses

### Settings
This is where you can enter any respawn modifiers that you may have. The macro will account for them when calculating respawn times


