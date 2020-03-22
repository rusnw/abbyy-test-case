'''
Created on 22 мар. 2020 г.

@author: ikostionov
'''

import requests
import csv
import json
import logging
import yaml
import glob, os
import re
from pathlib import Path
from zipfile import ZipFile
from datetime import date

# Инициализация конфигурационного yaml файла

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Путь до лог-файла
 
fh = logging.FileHandler("abbyycase-" +  date.today().strftime("%Y%m%d") + ".log")

# Создание экземпляра логгера для настройки сообщений в журнал

logger = logging.getLogger("AbbyyCase")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


'''
Фильтр по полю License Risk.
Возвращает True если значение поля License Risk в переданной строке равно одному из значений в переменной license_risk_filter конфигурационного файла.

Возвращает True если license_risk_filter имеет пустое значение и если оно не указано в конфигурации.
'''
def filter_lic_risk(row):
    try:
        if cfg["license_risk_filter"]:
            return row["License Risk"] in cfg["license_risk_filter"]
        else:
            return True
    except KeyError:
        return True

'''
Создание компонента/

'''
def create_component(csv):
        data = {'title': csv["Component name"],
                'version': csv["Component version name"],
                'license': csv["License names"].strip("()").split(" AND ")[0],
                'usage': csv["Usage"]  }
        requests.post(cfg["URL"], json.dumps(data), headers=cfg["headers"])
'''


'''
    
def campare(response, csv):
    for key,value in cfg["campare_field"].items():
        if response[key] != csv[value]:
            logger.error("Component with OSS Registy ID = " + csv["OSS Registry ID"] + " has error! Field \"" + key + "\" has value from API = [" + response[key] + "], value from file = [" + csv[value] +"]")
    
    csv_licenses = csv["License names"].strip("()").split(" AND ")
    if response["license"] not in csv_licenses:
        logger.error("Component with OSS Registy ID = " + csv["OSS Registry ID"] + " has error! Field \"License\" has value from API = [" + response["license"] + "], value from file = [" + csv["License names"].strip("()") + "]")
    
    if response["usage"] != csv["Usage"]:
        logger.error("Component with OSS Registy ID = " + csv["OSS Registry ID"] + " has error! Field \"Usage\" has value from API = [" + response["usage"] + "], value from file = [" + csv["Usage"] + "]. Will be updated!")
        data = {'id': response["id"], 
                'title': response["title"],
                'version': response["version"],
                'license': response["license"],
                'usage': csv["Usage"]  }
        requests.put(cfg["URL"], json.dumps(data), headers=cfg["headers"])
'''
Основной процессинг с csv-файлом.

'''
def csvfile_processing(file):
    with open(file) as csvfile:
        logger.info("Start processing " + file) 
        csvrows = csv.DictReader(csvfile)
        for row in filter(filter_lic_risk, csvrows):        
            if row["OSS Registry ID"]:
                r = requests.get(url = cfg["URL"] + "/" + row["OSS Registry ID"])
                data = r.json()
                if data:
                    campare(data, row)
                else:
                    logger.error("Component with OSS Registy ID = " + row["OSS Registry ID"] + " not found!")
            else:
                create_component(row)
    os.replace(file, cfg["csv_out"] + "/" + os.path.basename(file))
    os.rmdir(Path(file).parent.absolute())

'''
main функция

'''

def main():
    # В каталоге zip_in ищем zip-файлы по маске и сортируем их до дате модификации от старых к новым
    os.chdir(cfg["zip_in"])
    files = glob.glob(cfg["zipfile_wildcard"])
    files.sort(key=os.path.getmtime)
    # Вытаскиваем из каждого архива csv файл, имя которого соотвествует шаблону csvfile_regexp, в каталог csv_inи отправляем на обработку
    for file in files:
        with ZipFile(file, 'r') as zipObj:
            listOfFileNames = zipObj.namelist()
            for fileName in listOfFileNames:
                if re.match(cfg["csvfile_regexp"], fileName):
                    zipObj.extract(fileName, cfg["csv_in"])
                    csvfile_processing(cfg["csv_in"] + "/" + fileName)
        # В случае успешной обработки отправляем архив в архивный каталог
        os.replace(cfg["zip_in"] + "/" + file, cfg["zip_out"] + "/" + file)

if __name__ == '__main__':
    main()
