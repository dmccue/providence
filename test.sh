#!/bin/bash

EVENTS=$(python test.py)
sudo cat test.html | sed -e "s|REPLACEMEREPLACEME12345|$EVENTS|" > /var/www/html/test.html

