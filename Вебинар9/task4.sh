# Проверяем, что передан один аргумент (адрес сервера)
if [ "$#" -ne 1 ]; then
    echo "Использование: $0 <адрес_сервера>"
    exit 1
fi

SERVER=$1

# Пингуем сервер
if ping -c 1 "$SERVER" &> /Users/nvoronov/Desktop/hse/mentor/Вебинар9/res.txt; then
    echo "Сервер $SERVER доступен."
else
    echo "Сервер $SERVER недоступен."
fi
