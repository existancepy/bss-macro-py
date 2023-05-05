
import ast
import os
with open("fieldsettings.txt","r") as f:
    fields = ast.literal_eval(f.read())
f.close()
totalFields = gather_fields = [x.split("_")[1][:-3] for x in os.listdir("./") if x.startswith("field_")]
for i in fields:
    if i not in totalFields:
        print(i)
while True:
    field = input("field: ")
    if field == "quit": break
    gp = input("gather pattern: ")
    gs = "s"
    gw = 2
    gt = 8
    pack = 100
    bgt = input("before gather turn: ")
    tt = input("turn times: ")
    rth = "walk"
    ws = 1
    sl = input("start location: ")
    dfc = input("distance from center: ")
    fdc = 0
    fields[field] = {
        "gather_pattern": gp,
        "gather_width": gw,
        "gather_time": gt,
        "pack": pack,
        "before_gather_turn": bgt,
        "turn_times": tt,
        "return_to_hive": rth,
        "whirligig_slot": ws,
        "start_location": sl,
        "distance_from_center": dfc,
        "field_drift_compensation": fdc
        

        }
    with open("fieldsettings.txt","w") as f:
        f.write(str(fields))
    f.close()
print(fields)
