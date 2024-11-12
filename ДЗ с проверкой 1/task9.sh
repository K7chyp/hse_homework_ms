#!/bin/bash

check_memory_usage() {
    MEMORY_USAGE=$(free | awk '/Mem/{printf("%.0f"), $3/$2*100}')
    
    if [ "$MEMORY_USAGE" -gt 80 ]; then
        echo "Внимание: Использование памяти составляет ${MEMORY_USAGE}%!"
        echo "Процессы, потребляющие наибольшее количество ресурсов:"
        ps aux --sort=-%mem | awk 'NR<=10{print $0}'
    else
        echo "Использование памяти в норме: ${MEMORY_USAGE}%"
    fi
}

check_cpu_load() {
    CPU_LOAD=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *([0-9.]*)%* id.*/1/" | awk '{print 100 - $1}')
    echo "Загрузка процессора: ${CPU_LOAD}%"
}

check_disk_usage() {
    DISK_USAGE=$(df -h | grep '^/dev/' | awk '{ print $5 }' | sed 's/%//')
    echo "Использование дискового пространства:"
    df -h | grep '^/dev/'
    
    for usage in $DISK_USAGE; do
        if [ "$usage" -gt 90 ]; then
            echo "Внимание: Использование дискового пространства превышает 90%!"
        fi
    done
}

check_memory_usage
check_cpu_load
check_disk_usage
