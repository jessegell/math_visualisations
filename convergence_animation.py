"""
This is part of a project to create visualizations of sequence convergence.

Input a sequence seq of points in the plain, a tuple of epsilons, and an accuracy parameter acc.  

If the sequence converges to zero fast enough, the functions conv_animation will output an animation that plots the sequence, zooms in on each epsilon ball, and shows the first point in the sequence after which all other points are expected to lie in the ball.

To produce an example, input

seq = lambda n: ((4/(n+1))**3 + 2/(n+1)**2, 2/(n+1)**2)

epsilons = (1/4, 1/50, 1/400,1/10000)

acc = 200
"""


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import functools


def conv_animation(seq, epsilons, acc):
    """Create an animation which zooms in successively on balls of radii in the tuple epsilons."""

    # Need epsilons to be a tuple
    if type(epsilons) != tuple:
        return print("Error: epsilons must by a tuple.  If you want to enter a single epsilon it must be in the form (num,)")
        
    
    # Need epsilons to be descending, if not return an error message
    if not all(epsilons[i] > epsilons[i + 1] for i in range(len(epsilons) - 1)):
        return print("Error: The list of epsilons must be decreasing.")
    
    def dist(u, v):
        """Compute planar distance."""
        return np.sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2)

    dist_lim = functools.partial(dist, v=(0, 0))

    def find_N(sequ, eps, acc):
        """Return the N such that for a given epsilon, N and the subsequence acc - 1 points are distance less then epsilon from the origin."""
        j, k = 1, 1
        while j <  acc:
            if dist_lim(sequ(k)) < eps:
                j += 1
            else:
                j = 0
            k += 1
            if k > 2**16:
                return False
        return k - acc

    # create figure and axes
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot([0,0,1,1])  # [left, bottom, width, height]

    # Axes spine parameters.  
    ax.spines.left.set_position(('zero'))  # float gives x offset
    ax.spines.right.set_color('none')
    ax.spines.bottom.set_position(('zero'))  # float gives y offset
    ax.spines.top.set_color('none')
    '''
    If you want to add, ticks you need the following two lines:
    ax.xaxis.set_ticks_position('bottom') # needed because the center spine is the bottom spine moved to center
    ax.yaxis.set_ticks_position('left') # same
    '''
    # remove axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Make an epsilon ball as a fill_between object.  alpha is the opacity.
    def make_ball(eps, alpha):

        nd = np.linspace(-eps,eps, num=100)  # iterator for circle points
        du, dd = np.sqrt(eps**2 - nd**2), - np.sqrt(eps**2 - nd**2)  # top and bottom of circle
        return plt.fill_between(nd,du,dd, facecolor = 'orange',alpha=alpha)  
    # tuple of N corresponding to each epsilon
    Ns = ()
    for i in range(len(epsilons)):
        Ns += (find_N(seq, epsilons[i], acc),)

    # it is possible some Ns were False, in which case error message:
    if False in Ns:
        return print("Error: You may have entered a value of epsilon that is too small, or the sequence might diverge or converge too slowly for this program to detect.")
        
    # full range of indices that will appear
    n = (np.arange(1, Ns[-1] + acc,1))

    # Make tuple of axis sizes at each step.  Want x/y-lims after zoom to be so that ball takes up no more than 1/2 the screen.
    radii = ((1.1)*np.ceil(max(dist_lim(seq(n)))),)  
    for i in range(len(epsilons)):
        factor = int(np.floor(radii[i]/epsilons[i]))
        radii += (2*(radii[i]/factor),)

    # Initiate x and y lims
    ax.set_xlim([-radii[0],radii[0]]) 
    ax.set_ylim([-radii[0],radii[0]]) 

    # Number of frams in each zoom / freeze component of the animation
    frame_unit = 500
    freeze_unit = 400

    # These are the axis limits for each step. On the i^th step it is a np.linspace list going between the two prechosen axis limits from the list radii.  The step number is frame_unit, and that is the number of frames in the zoom in the animate function.
    ax_lims = ()
    for i in range(len(epsilons)):
        ax_lims += (np.linspace(radii[i], radii[i + 1],frame_unit),)

    eps_text = plt.text(0,0,'')  # Text will display radii in animation

    num_points = len(n)
    scat = ax.scatter(seq(n)[0],seq(n)[1],c='blue',s=[0]*num_points)  # size set to zero.

    # rate is the frames per appearance of scatter point, and points to show is the number of points you want to animate.  If you animate the appearance of all points it will take too long.
    rate, points_to_show = 60, 20
    scatter_frames = rate * points_to_show

    wait_to_plot = 50 # How many frames to wait before animation after the scatter plot is made.

    # Make the balls
    balls = ()
    for i in range(len(epsilons)):
        balls += (make_ball(epsilons[i],(i + 1)/10),)

    # Make the arrows.  They begin as not visible and then are made visible in the animation.
    arrows = ()
    for i in range(len(epsilons)):
        arrows += (plt.annotate(f'{Ns[i]}-th point',xy= seq(Ns[i]),xytext=(-(1.25)*epsilons[i], (1.25)*epsilons[i]),arrowprops = dict(facecolor='black', shrink=0.02, width = 1), visible=False),)

    wiggle = 1.1 # Gives some wiggle room for nice looking text in animation

    def animate(i):
        """Gives the animated scatter plot effect, for the first (points_to_show) points"""
        if i < scatter_frames and i % rate == 0:
            if i % rate == 0:
                Sizes = scat.get_sizes()
                Sizes[i//rate] = 20 / ((i // rate) + 1)
                scat.set_sizes(Sizes)

        # graph the remaining points.
        if i == scatter_frames:
            scat.set_sizes(20/n)

        if i >= scatter_frames + wait_to_plot:
            # zoom comes from this block.  k is the "step", i.e. which epsilon you are on, and j is the index within that step.
            k, j = (i - (scatter_frames + wait_to_plot)) // (frame_unit + freeze_unit), (i - (scatter_frames + wait_to_plot)) % (frame_unit + freeze_unit)

            if j in range(1,frame_unit):
                ax.set_xlim([-(ax_lims[k][j]), ax_lims[k][j]]) # sets x limits to max needed
                ax.set_ylim([-(ax_lims[k][j]), ax_lims[k][j]]) # sets y limits to max needed

            # text comes and goes from these block
            if j == frame_unit:
                eps_text.set_position((wiggle*epsilons[k]/np.sqrt(2), -wiggle*epsilons[k]/np.sqrt(2)))
                eps_text.set_text(f'$\epsilon =$ {epsilons[k]}')
                arrows[k].set_visible(True)

            if j == frame_unit+freeze_unit-1:
                eps_text.set_text('')
                arrows[k].set_visible(False)

        return (ax, scat, eps_text) + arrows + balls

    # the number of frames is the sum of: scatter_frames (animates the scatter plot), wait_to_plot (pauses before animation begins, frame_unit (frames in the zoom), freeze_unit (still part with epsilon and arrow displayed), the latter two happen len(epsilons) times.

    anim = animation.FuncAnimation(fig, animate, frames=range(0, scatter_frames + wait_to_plot + len(epsilons)*(frame_unit+freeze_unit)), interval=0.4,blit=True)
    plt.show()
