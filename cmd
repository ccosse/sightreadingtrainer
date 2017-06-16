#!/bin/bash
../jython2.2.1/jythonc -J -g:none --all -c -j MFC.jar MFC.py orch.py keyboard.py guitar.py mfcinstrument.py scroll_tab.py scroll_staff.py pyld.py music.py 
echo scp MFC.jar MFC.html root@dev:/var/www/dev/static/sightreadingtrainer/
