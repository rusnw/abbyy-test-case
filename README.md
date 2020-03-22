# Summary
Проект состоит из скрипта ([main.py](https://github.com/rusnw/abbyy-test-case/blob/master/main.py)) на языке Python (v3.8) и конфигурационного файла ([config.yml](https://github.com/rusnw/abbyy-test-case/blob/master/config.yml)).
В процессе работы скрипт формирует лог-файл формата abbyycase-YYYYMMDD.log в директории запуска.

# Clone
```
git clone https://github.com/rusnw/abbyy-test-case.git
```
Все необходимые каталоги in/out необходимо предварительно создать.
Пример конфигурационного файла:
```
# Каталог из которого скрипт будет забирать ZIP файл 
zip_in: "C:/reports/zip_in"

# Архивный каталог в который скрипт будет выкладывать обработанные ZIP файлы для анализа возможных проблем
zip_out: "C:/reports/zip_out"

# Каталог в который помещается csv файл для обработки
csv_in: "C:/reports/csv_in"

# Архивный каталог в который скрипт будет выкладывать обработанные csv файлы для анализа возможных проблем
csv_out: "C:/reports/csv_out"

# Маска для выбоки zip файлов
zipfile_wildcard: "Image-1.0.0.1_*.zip"

# Маска csv файла, который будет извлечен из ZIP файла и обработан
csvfile_regexp: "(.*)/bom_component_custom_fields(.*).csv"

# URL сервиса 2
URL: "http://localhost:3001/component"

# Заголовки с которыми будут производиться PUT/POST запросы
headers:
  Content-Type: "application/json"

# Список полей для "простого" сравнения между ответом от REST и полем в файле.
# key - поле в API
# value - поле в файле
campare_field:
  title: "Component name"
  version: "Component version name"

# Настройка, которая позволяет обработать не все записи из csv, а только те, у которых License Risk соответсвует значениям в массиве license_risk_filter.
# Если настройка не задана или имеет в значении пустоту – то обрабатываем всё. 
license_risk_filter:
  - HIGH
  - MEDIUM
```
