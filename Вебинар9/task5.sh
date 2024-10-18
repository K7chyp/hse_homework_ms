#!/bin/bash

# Перебираем все файлы в текущей директории
for file in *; do
    # Проверяем, что это файл (не директория)
    if [ -f "$file" ]; then
        # Получаем имя файла в строчных буквах
        lower_file=$(echo "$file" | tr '[:upper:]' '[:lower:]')
        
        # Переименовываем файл, если имена различаются
        if [ "$file" != "$lower_file" ]; then
            mv "$file" "$lower_file"
            echo "Переименован: '$file' -> '$lower_file'"
        fi
    fi
done
