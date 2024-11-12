#!/bin/bash

# Параметры
REMOTE_USER="root"        # Пользователь на удалённом сервере
REMOTE_HOST="localhost"        # Хост удалённого сервера
REMOTE_PORT=2222
EMAIL="$1"              # Email для уведомлений

# Проверка на наличие необходимых параметров
if [ $# -ne 1 ]; then
    echo "Использование: $0 <email>"
    exit 1
fi

# Подключение к удалённому серверу и выполнение обновлений
ssh "${REMOTE_USER}@${REMOTE_HOST}" -p "$REMOTE_PORT" << EOF

# Проверка наличия обновлений
UPDATES=$(apt-get update && apt-get upgrade -s | grep -E '^[[:digit:]]+' | wc -l)

if [ "$UPDATES" -gt 0 ]; then
    echo "Обновления найдены. Устанавливаем..."
    apt-get upgrade -y

    # Проверка необходимости перезагрузки
    if [ -f /var/run/reboot-required ]; then
        echo "Сервер требует перезагрузки."
        reboot
        REBOOT_REQUIRED=true
    else
        echo "Обновления установлены без необходимости перезагрузки."
    fi
else
    echo "Обновлений не найдено."
fi

EOF

# Отправка уведомления по электронной почте, если сервер был перезагружен
if [ "$REBOOT_REQUIRED" = true ]; then
    echo "Сервер ${REMOTE_HOST} был перезагружен после установки обновлений." | mail -s 
"Уведомление о перезагрузке сервера" "$EMAIL"
fi

echo "Скрипт завершён."
