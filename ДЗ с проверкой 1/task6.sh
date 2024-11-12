#!/bin/bash

if [[ ! -f input.txt ]]; then
    echo "Файл input.txt не найден."
    exit 1
fi

wc -l < input.txt > output.txt

ls nonexistent_file.txt 2> error.log

echo "Подсчет строк завершен. Результат записан в output.txt."
echo "Ошибки выполнения команды ls записаны в error.log."
