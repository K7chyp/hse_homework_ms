#!/bin/bash

set -m 

sleep 10 &
pid1=$!
echo "Запущен процесс sleep 10 с PID: $pid1"

sleep 15 &
pid2=$!
echo "Запущен процесс sleep 15 с PID: $pid2"

sleep 20 &
pid3=$!
echo "Запущен процесс sleep 20 с PID: $pid3"

echo -e "Список фоновых задач:"
jobs

read -p "Нажмите Enter, чтобы продолжить и вернуть одну из задач на передний план..."

fg %1

echo -e "Список фоновых задач после fg:"
jobs

read -p "Нажмите Enter, чтобы перевести вторую задачу (sleep 15) в фон..."

bg %2

echo -e "Список фоновых задач после bg:"
jobs

echo "Скрипт завершен."
