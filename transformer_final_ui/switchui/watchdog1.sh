#!/bin/bash

if [[ ! $(pgrep -f main1.py) ]]; then
        env DISPLAY=:0.0 python /home/pi/transform_final_ui_confirm/transformer_final_ui/switchui/main1.py
fi
