#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Использование: $0 <директория_для_резервного_копирования> <директория_для_резервных_копий>"
    exit 1
fi

SOURCE_DIR="$1"
BACKUP_DIR="$2"
LOG_FILE="backup_log.txt"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Ошибка: Исходная директория '$SOURCE_DIR' не существует."
    exit 1
fi

mkdir -p "$BACKUP_DIR"

CURRENT_DATE=$(date +%Y-%m-%d)

FILE_COUNT=0

for FILE in "$SOURCE_DIR"/*; do
    if [ -f "$FILE" ]; then
        FILENAME=$(basename "$FILE")
        BACKUP_FILE="$BACKUP_DIR/${FILENAME}_$CURRENT_DATE"
      	
	cp "$FILE" "$BACKUP_FILE"
        
        ((FILE_COUNT++))
      
        echo "Скопирован файл: $FILE -> $BACKUP_FILE" >> "$LOG_FILE"
    fi
done

if [ "$FILE_COUNT" -gt 0 ]; then
    echo "Резервное копирование завершено. Скопировано файлов: $FILE_COUNT."
else
    echo "Нет файлов для резервного копирования в '$SOURCE_DIR'."
fi
