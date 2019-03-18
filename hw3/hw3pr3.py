#
# hw3pr3.py 
#
# Visualizing your own data with matplotlib...
# Here, you should include functions that produce two visualizations of data
#   of your own choice. Also, include a short description of the data and
#   the visualizations you created. Save them as screenshots or as saved-images,
#   named datavis1.png and datavis2.png in your hw3.zip folder.
# Gallery of matplotlib examples:   http://matplotlib.org/gallery.html
# List of many large-data sources:    https://docs.google.com/document/d/1dr2_Byi4I6KI7CQUTiMjX0FXRo-M9k6kB2OESd7a2ck/edit    
#     and, the birthday data in birth.csv is a reasonable fall-back option, if you'd like to use that...
#          you could create a heatmap or traditional graph of birthday frequency variations over the year...

"""
Short description of the two data visualizations...
"""

# datavis1()
#
"""
From:  http://matplotlib.org/examples/showcase/xkcd.html
"""
import csv 

def readcsv(csv_file_name):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object
        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append(row)                    # adds only the word to our list
        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists
    except FileNotFoundError as e:
        print("File not found: ", e)
        return []

def datavis1(filename="result.csv"):
    """ run this function for the first data visualization """
    import numpy as np
    import matplotlib.pyplot as plt

    data = readcsv(filename)
    N = len(data)
    ind = np.arange(N)
    width = 0.1
    data2 = [int(arr[-1]) for arr in data]
    data2.sort()
    print(data2)
    p1 = plt.bar(ind, data2, width) #, yerr=menStd)
    # p2 = plt.bar(ind, womenMeans, width, bottom=menMeans, yerr=womenStd)

    plt.ylabel('Scores')
    plt.title(filename)
    # plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    # plt.yticks(np.arange(0, 1000, step=25))
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    plt.show() 
# run it!
# datavis1("result2.csv")
# datavis1("result3.csv")
#
# datavis2()
#
"""
From:  http://matplotlib.org/xkcd/examples/pylab_examples/manual_axis.html
"""

import numpy as np
from pylab import figure, show
import matplotlib.lines as lines
import matplotlib.pyplot as plt

def make_xaxis(ax, yloc, offset=0.05, **props):
    """ custom-axis (x) example 
    """
    xmin, xmax = ax.get_xlim()
    locs = [loc for loc in ax.xaxis.get_majorticklocs()
            if loc>=xmin and loc<=xmax]
    tickline, = ax.plot(locs, [yloc]*len(locs),linestyle='',
            marker=lines.TICKDOWN, **props)
    axline, = ax.plot([xmin, xmax], [yloc, yloc], **props)
    tickline.set_clip_on(False)
    axline.set_clip_on(False)
    for loc in locs:
        ax.text(loc, yloc-offset, '%1.1f'%loc,
                horizontalalignment='center',
                verticalalignment='top')

def make_yaxis(ax, xloc=0, offset=0.05, **props):
    """ custom-axis (y) example 
    """
    ymin, ymax = ax.get_ylim()
    locs = [loc for loc in ax.yaxis.get_majorticklocs()
            if loc>=ymin and loc<=ymax]
    tickline, = ax.plot([xloc]*len(locs), locs, linestyle='',
            marker=lines.TICKLEFT, **props)
    axline, = ax.plot([xloc, xloc], [ymin, ymax], **props)
    tickline.set_clip_on(False)
    axline.set_clip_on(False)

    for loc in locs:
        ax.text(xloc-offset, loc, '%1.1f'%loc,
                verticalalignment='center',
                horizontalalignment='right')

def datavis2(filename="result.csv"):
    """ run this function for the second data visualization """
    data = readcsv(filename)
    N = len(data)
    import matplotlib.pyplot as plt
    import numpy as np

    # unit area ellipse
    rx, ry = 1., 1.
    area = rx * ry * np.pi
    theta = np.arange(0, 2 * np.pi + 0.01, 0.1)
    verts = np.column_stack([rx / area * np.cos(theta), ry / area * np.sin(theta)])
    x = [int(arr[1]) for arr in data]
    y = [int(arr[-1]) for arr in data]
    colors = np.random.rand(N)
    area = [score//50+1 for score in y ]
    # (10*np.random.rand(N))**2

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=area, c=colors, alpha=0.5, marker=verts)

    plt.show()

# run it!
print("Run datavis1() or datavis2() or widgets()")
datavis2()



# widgets

def widgets():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, Button, RadioButtons

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.25)
    t = np.arange(0.0, 1.0, 0.001)
    a0 = 5
    f0 = 3
    s = a0*np.sin(2*np.pi*f0*t)
    l, = plt.plot(t, s, lw=2, color='red')
    plt.axis([0, 1, -10, 10])

    axcolor = 'lightgoldenrodyellow'
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
    axamp = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

    sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0)
    samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)


    def update(val):
        amp = samp.val
        freq = sfreq.val
        l.set_ydata(amp*np.sin(2*np.pi*freq*t))
        fig.canvas.draw_idle()
    sfreq.on_changed(update)
    samp.on_changed(update)

    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


    def reset(event):
        sfreq.reset()
        samp.reset()
    button.on_clicked(reset)

    rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
    radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)


    def colorfunc(label):
        l.set_color(label)
        fig.canvas.draw_idle()
    radio.on_clicked(colorfunc)

    plt.show()

