#!/bin/bash

# Проверяем, передан ли аргумент
if [ $# -eq 0 ]; then
    echo "Пожалуйста, укажите путь к директории."
    exit 1
fi

# Получаем путь к директории из аргумента
directory="$1"

# Проверяем, является ли указанный путь директорией
if [ ! -d "$directory" ]; then
    echo "Указанный путь '$directory' не является директорией."
    exit 1
fi

# Проходим по всем файлам в директории
for file in "$directory"/backup_*; do
    # Проверяем, что файл существует
    if [ -f "$file" ]; then
        # Получаем имя файла без пути и префикса
        filename=$(basename "$file")
        new_filename="${filename#backup_}"
        # Переименовываем файл, убирая префикс
        mv "$file" "$directory/$new_filename"
        echo "Префикс 'backup_' убран у файла '$filename'."
    fi
done

echo "Все файлы в директории '$directory' были переименованы."
