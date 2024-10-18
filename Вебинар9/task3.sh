#!/bin/bash

# Проверяем, что передан один аргумент (длина пароля)
if [ "$#" -ne 1 ]; then
    echo "Использование: $0 <длина_пароля>"
    exit 1
fi

len=$1

pass=$(openssl rand -base64 "$len")
pass2=$(tr -d -c 'A-Za-z0-9!?%=' < /Users/nvoronov/Desktop/hse/mentor/Вебинар9/res.txt | head -c "$len")
echo "$pass"
echo "$pass2"
