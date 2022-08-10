#!/usr/bin/env sh
PATH_IN="../../../data/combined/" #..\data_files\data "
PATH_OUT="../data_files/data_output"

date_out="200103"  #add to config
variable="t2m" #add to config

new_path=$PATH_IN$date_out

mv $new_path* $PATH_OUT

