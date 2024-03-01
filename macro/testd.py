import loadsettings
from webhook import webhook
from html2image import Html2Image
from datetime import datetime
import time
import os
import math
from logpy import log
hti = Html2Image()

def millify(n):
    if not n: return 0
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def hourlyReport(hourly=1):
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']

    honeyHist = [4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 4364004, 39173643, 86004872, 139513109, 167073388, 167758541, 270029533, 350596059, 352108125, 370451087, 412702458, 466005506, 484401176, 485526699, 486651152, 564702674, 650993525, 651106186, 652498193, 671562881, 717465980, 777301296, 805108806, 846230541, 944391486, 946808309, 956503756, 967199662, 1008628061, 1030134647, 1077987203, 1107212527, 1146354879, 1155831017, 1185502882, 1273851786, 1366878952, 1440151425, 1444121086, 1472893105, 1523448424, 1554142534, 1555045584, 1556389236, 1602470642, 1686344716]
    setdat = loadsettings.load()
    log(honeyHist)
    #remove values less than 1000
    for i, e in enumerate(honeyHist[:]):
        if len(str(e)) <= 4:
            honeyHist.pop(i)
    #remove values less than the previous one
    honeyHist = honeyHist[1:]
    counter = 1
    while counter < len(honeyHist):
        if honeyHist[counter] < honeyHist[counter-1]:
            honeyHist.pop(counter)
        else:
            counter += 1
    if hourly == 0:
        setdat['prev_honey'] = honeyHist[-1]
    log('prev honey: {}'.format(setdat['prev_honey']))
    log(honeyHist)
    currHoney = honeyHist[-1]
    session_honey = currHoney - setdat['start_honey']
    hourly_honey = currHoney - setdat['prev_honey']
    if hourly:
        loadsettings.save('prev_honey',currHoney)
        timehour = int(datetime.now().hour) - 1
    else:
        timehour = int(datetime.now().hour)
        
    stime = time.time() - setdat['start_time']
    day = stime // (24 * 3600)
    stime = stime % (24 * 3600)
    hour = stime // 3600
    stime %= 3600
    minutes = stime // 60
    stime %= 60
    seconds = round(stime)
    session_time = "{}d {}h {}m".format(round(day),round(hour),round(minutes))
    yvals = []
    for i in range(len(honeyHist)):
        if i != 0:
            hf, hb = honeyHist[i], honeyHist[i-1]
            yvals.append(int(hf) - int(hb))
    #yvals = [1,2,3,4,5,6,7,8]
    xvals = [x+1 for x in range(len(yvals))]
    rootDir = os.path.dirname(os.path.abspath(__file__)) + "/hourlyReport"
    with open("./hourlyReport/index.html", "r") as f:
        data = f.read().split("\n")
        data.insert(0,"")
    f.close()
    print(data)
    data[13] = f"url({rootDir}/assets/background.png);"
    data[32] = f"Session Time:\t{session_time}"
    data[35] = f"Current Honey:\t{millify(currHoney)}"
    data[38] = f"Session Honey:\t{millify(session_honey)}"
    data[41] = f"Honey This Hour:\t{millify(hourly_honey)}"
    data[60] = f"const xValues = {xvals}"
    data[61] = f"const yValues = {yvals}"
    print(data)
    with open("./hourlyReport/index.html","w") as f:
        f.write('\n'.join(data))
    f.close()
    '''
    fig = plt.figure(figsize=(12,12), dpi=300,constrained_layout=True)
    gs = fig.add_gridspec(12,12)
    fig.patch.set_facecolor('#121212')

    axText = fig.add_subplot(gs[0:12, 8:12])
    axText.get_xaxis().set_visible(False)
    axText.get_yaxis().set_visible(False)
    axText.patch.set_facecolor('#121212')
    axText.spines['bottom'].set_color('#121212')
    axText.spines['top'].set_color('#121212')
    axText.spines['left'].set_color('#121212')
    axText.spines['right'].set_color('#121212')

    plt.text(0.3,1,"Report", fontsize=20,color="white")
    plt.text(0,0.95,"Session Time: {}".format(session_time), fontsize=15,color="white")
    plt.text(0,0.9,"Current Honey: {}".format(millify(currHoney)), fontsize=15,color="white")
    plt.text(0,0.85,"Session Honey: {}".format(millify(session_honey)), fontsize=15,color="white")
    plt.text(0,0.8,"Honey/Hr: {}".format(millify(hourly_honey)), fontsize=15,color="white")

    ax1 = fig.add_subplot(gs[0:3, 0:7])
    if not yvals:
        yvals = honeyHist.copy()
    if max(yvals) == 0:
        yticks = [0]
    else:
        yticks = np.arange(0, max(yvals)+1, max(yvals)/4)
    yticksDisplay = [millify(x) if x else x for x in yticks]

    xticks = np.arange(0,max(xvals)+1, 10)
    xticksDisplay = ["{}:{}".format(timehour,x) if x else "{}:00".format(timehour) for x in xticks]

    ax1.set_yticks(yticks,yticksDisplay,fontsize=16)
    ax1.set_xticks(xticks,xticksDisplay,fontsize=16)
    ax1.set_title('Honey/min',color='white',fontsize=19)
    ax1.patch.set_facecolor('#121212')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['top'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.spines['right'].set_color('white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.plot(xvals, yvals,color="#BB86FC")
    '''
    
    '''
    buffim = plt.imread('buffs.png')
    ax2 = fig.add_subplot(gs[4:6, 0:7])
    ax2.set_title('Buffs',color='white',fontsize=19)
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    ax2.patch.set_facecolor('#121212')
    ax2.imshow(buffim)
    
    plt.grid(alpha=0.08)
    plt.savefig("hourlyReport-resized.png", bbox_inches='tight')
    '''
    hti.screenshot(html_file='./hourlyReport/index.html', save_as='hourlyReport-resized.png')
    webhook("**Hourly Report**","","light blue",0,1)
hourlyReport()
