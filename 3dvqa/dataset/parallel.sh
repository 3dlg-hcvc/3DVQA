#!/bin/bash
if [ $# -eq 0 ]; then 
    echo "You need to specify number of cores to use and path to scannet annotations!"  
fi 

all_scenes=$(ls $2)
sub_arr_len=${#all_scenes[@]}

for i in $(eval echo {0..$(($1-1))}); do  
    python src/qa_all.py "--files" ${all_scenes[@]:$((i*sub_arr_len)):$(($((i+1))*sub_arr_len))} "--filename" $i &
done
