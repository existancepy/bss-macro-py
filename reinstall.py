import update, updateexperiment

inp = ""
while True:
    inp = input("Do you want to reinstall files for experimental macro or main macro? (e for experimental, m for main)")
    if inp.lower() == "e" or inp.lower() == "m":
        break
    else:
        print("Invalid input")

if inp.lower() == "e":
    updateexperiment.update()
else:
    update.update()
