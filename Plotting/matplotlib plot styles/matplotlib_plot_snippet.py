with plt.style.context(('CRAWLAB.mplstyle')):
    fig = plt.figure()

    # Remove the top and right splines. As of 01/11/15, we can't do this in the style file
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Define the X and Y axis labels
    plt.xlabel('X label (units)', labelpad=5)
    plt.ylabel('Y label (units)', labelpad=10)

    # Plot the data and set the labels to be used in the legend
    plt.plot(x1, y1, linestyle="-", label=r'Data 1')
    plt.plot(x2, y2, linestyle="--", label=r'Data 2')
    plt.plot(x3, y3, linestyle="-.", label=r'Data 3')
    plt.plot(x4, y4, linestyle=":", label=r'Data 4')

    # Uncomment below and set limits if needed
    # plt.xlim(0,5)
    # plt.ylim(0,10)

    # Create the legend
    leg = plt.legend(loc='upper right', ncol = 1)

    # OPTIONAL : Adjust the page layout filling the page using the new tight_layout command
    # plt.tight_layout(pad=0.5)

    # Uncomment below save the figure as a high-res pdf in the current folder
    # It's saved at the original 6x4 size
    # plt.savefig('plot_from_Notebook.pdf')

    # If using in the IPython Notebook, uncomment the line below
    # fig.set_size_inches(9,6) # resize the figure for better display in the notebook