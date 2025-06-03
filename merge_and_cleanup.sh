#!/bin/bash

set -e

echo "🔄 Переключение на ветку main..."
git checkout main
git pull origin main

echo "🌐 Получение всех удалённых веток..."
git fetch --all

echo "🔀 Слияние всех веток в main..."

for branch in $(git branch -r | grep -v '->' | grep -v 'main' | sed 's/origin\///'); do
  echo "➡️  Merging $branch..."
  git merge origin/$branch --no-edit || {
    echo "❌ Конфликт в $branch. Разреши вручную и продолжи."
    exit 1
  }
done

echo "🚀 Пуш объединённой ветки main..."
git push origin main

echo "🧹 Удаление всех локальных веток, кроме main..."
for branch in $(git branch | grep -v "main"); do
  git branch -D $branch
done

echo "🔥 Удаление всех удалённых веток, кроме main..."
for branch in $(git branch -r | grep -v '->' | grep -v 'main' | sed 's/origin\///'); do
  echo "❌ Удаление ветки $branch на GitHub..."
  git push origin --delete $branch || true
done

echo "✅ Готово. Все ветки объединены в main и удалены."
