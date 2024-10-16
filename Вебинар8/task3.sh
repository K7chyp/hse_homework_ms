read -p "Введите путь к директории для архивации: " dirpath

if [ -d "$dirpath" ]; then
    current_date=$(date +%Y-%m-%d)
    archive_name="$(basename "$dirpath")_$current_date.tar.gz"
    tar -czf "$archive_name" -C "$(dirname "$dirpath")" "$(basename "$dirpath")"
    echo "Архив '$archive_name' успешно создан."
else
    echo "Директория не найдена."
fi
