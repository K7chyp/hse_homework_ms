
read -p "Введите путь к файлу: " filepath

if [ -e "$filepath" ]; then
    echo "Файл найден!"
else
    echo "Файл не найден."
fi
