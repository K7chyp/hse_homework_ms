read -p "Введите файл: " file

if [ -f "$file" ]; then
    line_count=$(wc -l < "$file")
    chrs_count=$(wc -c < "$file")
    echo "Количество строк в файле '$file': $line_count"
    echo "Количество букв в файле '$file': $chrs_count"
else
    echo "Файл '$file' не найден."
    exit 1
fi
