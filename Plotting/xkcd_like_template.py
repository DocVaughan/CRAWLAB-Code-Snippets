rc('text', usetex=False)
with xkcd(scale=1.25, length = 100, randomness = 2)):
    
    # Set the plot size - 3x2 aspect ratio is best
    fig = figure(figsize=(6,4))
    ax = gca()
    subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

    # Change the axis units to serif
    setp(ax.get_ymajorticklabels(), family='xkcd', fontsize=18)
    setp(ax.get_xmajorticklabels(), family='xkcd', fontsize=18)

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Turn on the plot grid and set appropriate linestyle and color
    ax.grid(True,linestyle=':', color='0.75')
    ax.set_axisbelow(True)

    # Define the X and Y axis labels
    xlabel('X label (units)', family='xkcd', fontsize=22, labelpad=5)
    ylabel('Y Lable (units)', family='xkcd', fontsize=22, labelpad=10)

    plot(t, x1, linewidth=2, linestyle='-',  label=r'x1')
    plot(t, x2, linewidth=2, linestyle='--', label=r'x2')

    # uncomment below and set limits if needed
    # xlim(0,5)
    # ylim(-1,1.25)

    # Create the legend, then fix the fontsize
    leg = legend(loc='upper right', ncol = 2, fancybox=True)
    ltext  = leg.get_texts()
    setp(ltext, family='xkcd', fontsize=16)

    # Adjust the page layout filling the page using the new tight_layout command
    tight_layout(pad=0.5)

    # save the figure as a high-res pdf in the current folder
    savefig('plot_filename_xkcd.pdf')

# return to using LaTeX
rc('text', usetex=True)