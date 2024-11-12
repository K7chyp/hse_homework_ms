#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Использование: $0 <имя_файла>"
    exit 1
fi

target_file=$1

echo "Список файлов и каталогов в текущей директории:"
for item in *; do
    if [ -d "$item" ]; then
        echo "$item - Каталог"
    elif [ -f "$item" ]; then
        echo "$item - Файл"
    else
        echo "$item - Другой тип"
    fi
done

if [ -e "$target_file" ]; then
    echo "Файл '$target_file' существует."
else
    echo "Файл '$target_file' не найден."
fi

echo "Информация о файлах в текущей директории:"
for file in *; do
    if [ -e "$file" ]; then
        permissions=$(ls -l "$file" | awk '{print $1}')
        echo "$file - Права доступа: $permissions"
    fi
done
