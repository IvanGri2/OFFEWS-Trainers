# OFFEWS Trainers

Сайт OFFEWS: каталог трейнеров для одиночных игр. Страница публикуется через GitHub Pages прямо из корня репозитория, сами трейнеры лежат в [Releases](../../releases).

## Обновление

Данные трейнеров (версии, ссылки на скачивание, описания) задаются в `tools/build.py`, список функций в `tools/trainers-functions.json`. После правок:

```
python3 tools/build.py
```

Скрипт пересобирает `index.html`.
