#!/bin/bash

EVENTS=$(python gui.py)
sudo cat gui.html | sed -e "s|REPLACEMEREPLACEME12345|$EVENTS|" > /var/www/html/gui.html
