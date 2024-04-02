import subprocess
def lowBattery():
    ps = subprocess.Popen(
        'pmset -g batt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0].decode("utf-8").split(";")
    charging = not "discharging" in output[1].lower()
    batt = int(output[0].split("\t")[1].split("%")[0])
    return batt < 10 and not charging
print(lowBattery())
