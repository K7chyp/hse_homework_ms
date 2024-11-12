#!/bin/bash

read -p "Введите число: " number

if (( $(echo "$number > 0" | bc -l) )); then
    echo "Число положительное."
    
    # Используем цикл while для подсчета от 1 до введенного числа
    count=1
    while (( count <= number )); do
        echo $count
        ((count++))
    done

elif (( $(echo "$number < 0" | bc -l) )); then
    echo "Число отрицательное."
else
    echo "Число равно нулю."
fi
