import ast
with open("fieldsettings.txt","r") as f:
    fields = ast.literal_eval(f.read())
f.close()

for field in fields:
    fields[field]['shift_lock'] = 0
with open("fieldsettings.txt","w") as f:
    f.write(str(fields))
f.close()
