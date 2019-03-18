# hw3pr1.py 
#  lab problem - matplotlib tutorial (and a bit of numpy besides...)
#
# this asks you to work through the first part of the tutorial at   
#     www.labri.fr/perso/nrougier/teaching/matplotlib/
#   + then try the scatter plot, bar plot, and one other kind of "Other plot" 
#     from that tutorial -- and create a distinctive variation of each
#
# include screenshots or saved graphics of your variations of those plots with the names
#   + plot_scatter.png, plot_bar.png, and plot_choice.png
# Remember to run  %matplotlib  at your ipython prompt!
# in-class examples...
#
import math 

def inclass1():
    """
    Simple demo of a scatter plot.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    plt.figure(num=6)
    N = 4242
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
    plt.scatter(x, y, s=area, c=colors, alpha=0.5, cmap='jet')
    plt.show()

# First example from the tutorial/walkthrough
# Feel free to replace this code as you go -- or to comment/uncomment portions of it...
def example1():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    #plt.figure(num=1)
    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C,S = np.cos(X), np.sin(X)

    plt.plot(X,C)
    plt.plot(X,S)
    plt.show()

# Here is a larger example with many parameters made explicit
def example2():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    plt.figure(num=2)
    # Create a new figure of size 8x6 points, using 100 dots per inch
    #plt.figure(figsize=(8,6), dpi=80)
    # Create a new subplot from a grid of 1x1
    plt.subplot(111)
    X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
    C,S = np.cos(X), np.sin(X)
    # Plot cosine using blue color with a continuous line of width 1 (pixels)
    plt.plot(X, C, color="blue", linewidth=1.0, linestyle="-")
    # Plot sine using green color with a continuous line of width 1 (pixels)
    plt.plot(X, S, color="green", linewidth=1.0, linestyle="-")
    # Set x limits
    plt.xlim(-4.0,4.0)
    # Set x ticks
    plt.xticks(np.linspace(-4,4,9,endpoint=True))
    # Set y limits
    plt.ylim(-1.0,1.0)
    # Set y ticks
    plt.yticks(np.linspace(-1,1,5,endpoint=True))
    # Save figure using 72 dots per inch
    # savefig("../figures/exercice_2.png",dpi=72)
    # Show result on screen
    plt.show()

def example3():
    """
    # -----------------------------------------------------------------------------
    # Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
    # Distributed under the (new) BSD License. See LICENSE.txt for more info.
    # -----------------------------------------------------------------------------
    """
    import numpy as np
    import matplotlib.pyplot as plt 
    plt.figure(num=3,figsize=(8,5), dpi=80)
    ax = plt.subplot(111)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))

    X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
    C,S = np.cos(X), np.sin(X)

    plt.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine")
    plt.plot(X, S, color="red", linewidth=2.5, linestyle="-",  label="sine")
    plt.xlim(X.min()*1.1, X.max()*1.1)
    plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
            [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
    plt.ylim(C.min()*1.1,C.max()*1.1)
    plt.yticks([-1, +1],
            [r'$-1$', r'$+1$'])
    plt.legend(loc='upper left', frameon=False)
    t = 2*np.pi/3
    plt.plot([t,t],[0,np.cos(t)],
            color ='blue',  linewidth=1.5, linestyle="--")
    plt.scatter([t,],[np.cos(t),], 50, color ='blue')
    plt.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
                xy=(t, np.sin(t)),  xycoords='data',
                xytext=(+10, +30), textcoords='offset points', fontsize=16,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    plt.plot([t,t],[0,np.sin(t)],
            color ='red',  linewidth=1.5, linestyle="--")
    plt.scatter([t,],[np.sin(t),], 50, color ='red')
    plt.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$',
                xy=(t, np.cos(t)),  xycoords='data',
                xytext=(-90, -50), textcoords='offset points', fontsize=16,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(16)
        label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.25 ))

    plt.savefig("./example3.png",dpi=72)
    plt.show()


def example4():
    """
    ===========================
    FiveThirtyEight style sheet
    ===========================

    This shows an example of the "fivethirtyeight" styling, which
    tries to replicate the styles from FiveThirtyEight.com.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    plt.style.use('fivethirtyeight')
    #plt.figure(4)
    x = np.linspace(0, 10)
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    fig, ax = plt.subplots(num=4)
    
    #plt.figure(4)
    ax.plot(x, np.sin(x) + x + np.random.randn(50))
    ax.plot(x, np.sin(x) + 0.5 * x + np.random.randn(50))
    ax.plot(x, np.sin(x) + 2 * x + np.random.randn(50))
    ax.plot(x, np.sin(x) - 0.5 * x + np.random.randn(50))
    ax.plot(x, np.sin(x) - 2 * x + np.random.randn(50))
    ax.plot(x, np.sin(x) + np.random.randn(50))
    ax.set_title("'fivethirtyeight' style sheet")

    plt.show()

def example5():
    """
    # -----------------------------------------------------------------------------
    # Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
    # Distributed under the (new) BSD License. See LICENSE.txt for more info.
    # -----------------------------------------------------------------------------
    """
    import numpy as np
    import matplotlib.pyplot as plt
    plt.figure(num=5)
    ax = plt.axes([0.025,0.025,0.95,0.95], polar=True)
    N = 20
    theta = np.arange(0.0, 2*np.pi, 2*np.pi/N)
    radii = 10*np.random.rand(N)
    width = np.pi/4*np.random.rand(N)
    bars = plt.bar(theta, radii, width=width, bottom=0.0)

    for r,bar in zip(radii, bars):
        bar.set_facecolor( plt.cm.jet(r/10))
        bar.set_alpha(0.5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    # savefig('../figures/polar_ex.png',dpi=48)
    plt.show()

# using style sheets:
#   # be sure to               
#       import matplotlib
#   # list of all of them:     
#       matplotlib.style.available
#   # example of using one:    
#       matplotlib.style.use( 'seaborn-paper' )
#

# colormaps
# import matplotlib.cm as cm

def scatterPlot(n=1024):
    """
        creates a scatter plot & n as the # of pts. 
    """
    import numpy as np
    import matplotlib.pyplot as plt
    plt.figure("Scatter Plot")
    X = np.random.normal(0,1,n)
    Y = np.random.normal(0,1,n)
    plt.scatter(X,Y)
    plt.show()

def barGraph(n=12):
    import numpy as np
    import matplotlib.pyplot as plt
    plt.figure("bar Graph")
    X = np.arange(n)
    Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
    Y2 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)

    plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
    plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

    for x,y in zip(X,Y1):
        plt.text(x+0.4, y+0.05, '%.2f' % y, ha='center', va= 'bottom')

    plt.ylim(-1.25,+1.25)
    plt.show()

def quiverGraph(n=8):
    import numpy as np
    import matplotlib.pyplot as plt

    plt.figure("quiver graph")
    X,Y = np.mgrid[0:n,0:n]
    plt.quiver(X,Y)
    plt.show()

def graph3D(title="3D graph", func=False):
    """
        gives a title & then accepts a func that takes 2 arrays and gives 1 array 
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # plt.figure()
    fig = plt.figure(title)
    ax = Axes3D(fig)
    X = np.arange(-5, 5, .5)
    Y = np.arange(-5, 5, .5)
    X, Y = np.meshgrid(X, Y)
    if(not func): 
        R = np.sin(X*Y) 
        # R = np.log((X**2 + Y**2)**.5)
        # R = -25*X**2 - 30*Y**2 -15 
        # R = math.e**((X**2 + Y**2)**.5) 
        # R = X**2 + (Y - X**(2/3))**2 
        # R = X**(2/3) + (1- X**2)**0.5
        # R += X**(2/3) - (1- X**2)**0.5
        # R = (X**2 + Y**2 - 1)**3 - X**2 * (Y**3) 
        # R = (np.sin(Y)*(abs(np.cos(Y))**(0.5)))/(np.sin(Y) + math.pi/5) - 2*np.sin(Y) + 2
        # R = X**2 + 2*(Y) + Y**3/5 + X**4/6
        # R = np.cos(X) + Y
    else: 
        R = func(X, Y)
    Z = R

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='Blues')

    plt.show()

def main():
    """
    example1()
    example2()
    example3()
    example4()
    example5()
    inclass1()
    """
    # scatterPlot(1000)
    # barGraph(20)
    # quiverGraph(5)
    graph3D()

if __name__ == "__main__":
    main()
