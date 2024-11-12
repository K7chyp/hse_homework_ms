#!/bin/bash

# Параметры
SOURCE_DIR="$1"              # Директория для резервного копирования
REMOTE_USER="root"             # Пользователь на удалённом сервере
REMOTE_HOST="localhost"             # Хост удалённого сервера
REMOTE_DIR="$2"              # Директория на удалённом сервере для хранения архивов
MAX_ARCHIVES=3               # Максимальное количество архивов на удалённом сервере

# Проверка на наличие необходимых параметров
if [ $# -ne 2 ]; then
    echo "Использование: $0 <источник> <директория>"
    exit 1
fi

# Создание имени архива с текущей датой и временем
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="backup_${TIMESTAMP}.tar.gz"

# Архивирование директории
tar -czf "$ARCHIVE_NAME" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

# Копирование архива на удалённый сервер
scp -r -i "$ARCHIVE_NAME" -P 2222 "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"

# Удаление локального архива после копирования
rm "$ARCHIVE_NAME"

# Удаление старых архивов на удалённом сервере
ssh "${REMOTE_USER}@${REMOTE_HOST}" <<EOF
cd "$REMOTE_DIR"
ls -t | grep 'backup_' | awk "NR > $MAX_ARCHIVES" | xargs -r rm --
EOF

echo "Резервное копирование завершено."
