#!/bin/bash

# Проверяем, что переданы два аргумента
if [ "$#" -ne 2 ]; then
    echo "Использование: $0 <число1> <число2>"
    exit 1
fi

num_1=$1
num_2=$2

# Сравниваем числа
if [ "$num_1" -gt "$num_2" ]; then
    echo "$num_1 больше $num_2"
elif [ "$num_1" -lt "$num_2" ]; then
    echo "$num_1 меньше $num_2"
else
    echo "$num_1 равно $num_2"
fi
