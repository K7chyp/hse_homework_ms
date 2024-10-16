#!/bin/bash

# Получаем путь к директории из аргумента
read -p "Введите директорию" directory

# Проверяем, является ли указанный путь директорией
if [ ! -d "$directory" ]; then
    echo "Указанный путь '$directory' не является директорией."
    exit 1
fi

# Проходим по всем файлам в директории
for file in "$directory"/*; do
    # Проверяем, что это файл, а не директория
    if [ -f "$file" ]; then
        # Получаем имя файла без пути
        filename=$(basename "$file")
        # Переименовываем файл, добавляя префикс
        mv "$file" "$directory/backup_$filename"
        echo "Префикс 'backup_' добавлен к файлу '$filename'."
    fi
done

echo "Все файлы в директории '$directory' были переименованы."
