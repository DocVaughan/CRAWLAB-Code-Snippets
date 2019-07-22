#!/bin/bash

# WARNING... exisiting configurations for .inputrc and .tmux.conf will be
#            overwritten when this script is run
#
# Run this from the home directory of a newly setup machine to automatically
# configure tmux and inputrc for easier use. 
#
# To do so, copy this script to the home directory for the desired user. You 
# can generally do:
# 
#    cd ~
# 
# to do that. You may have to change the permissions to make the script
# executable. Do to that, use the chmod command
#
#    chmod +x dotfile_setup.sh
#
# Then, run the file from the terminal by:
#
#    ./dotfile_setup.sh


# This section will create a tmux configuration file. 
TMUX_FILE=".tmux.conf"

/bin/cat <<EOM >$TMUX_FILE
# Make mouse useful
set -g mouse on

# Only resize to the smallest client if they are looking at it
setw -g aggressive-resize on
EOM

# This section will create a inputrc configuration file. 
INPUTRC_FILE=".inputrc"

/bin/cat <<EOM >$INPUTRC_FILE
"\e[A": history-search-backward
"\e[B": history-search-forward
set show-all-if-ambiguous on
set completion-ignore-case on
EOM