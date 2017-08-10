#!/bin/bash

echo '####################################'
echo '#                                  #'
echo '# Logdatei wird abgespielt         #'
echo '#                                  #' 
echo '# canplayer -l i -I vcan0.log      #'
echo '#                                  #'
echo '# in eine weiteren Termial einfach #'
echo '#                                  #'
echo '# candump vcan0  eingeben          #'
echo '#                                  #'
echo '# Abbruch mit strg-C               #' 
echo '####################################'

canplayer -l i -I vcan0.log
