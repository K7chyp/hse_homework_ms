#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Использование: $0 <новая_директория>"
    exit 1
fi

echo "Текущее значение переменной PATH:"
echo "$PATH"

new_directory=$1

export PATH="$new_directory:$PATH"
echo "Новое значение переменной PATH:"
echo "$PATH"
