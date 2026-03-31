# Dashboards для Dell OME Zabbix Template

## Варианты добавления dashboards (без изменения template_dell_ome_7.0.xml)

---

## 📋 Вариант 1: Отдельный XML файл dashboard

### Создание через UI Zabbix

1. **Dashboard → Create dashboard**
2. Добавьте виджеты для Dell OME
3. **Dashboard → Export** → XML
4. Сохраните как `dashboard_dell_ome.xml`

### Пример структуры файла

```xml
<?xml version="1.0" encoding="UTF-8"?>
<zabbix_export>
    <version>7.0</version>
    <date>2026-03-31T12:00:00Z</date>
    <dashboards>
        <dashboard>
            <name>Dell OME Monitoring</name>
            <private>0</private>
            <pages>
                <page>
                    <name>Overview</name>
                    <widgets>
                        <widget>
                            <type>PROBLEMS</type>
                            <name>Problems</name>
                            <x>0</x>
                            <y>0</y>
                            <width>12</width>
                            <height>7</height>
                            <fields>
                                <field>
                                    <name>problemTags</name>
                                    <value>Dell</value>
                                </field>
                                <field>
                                    <name>showSeverity</name>
                                    <value>1</value>
                                </field>
                            </fields>
                        </widget>
                        <widget>
                            <type>SYSTEM</type>
                            <name>System status</name>
                            <x>12</x>
                            <y>0</y>
                            <width>12</width>
                            <height>7</height>
                        </widget>
                    </widgets>
                </page>
                <page>
                    <name>Devices</name>
                    <widgets>
                        <widget>
                            <type>GRAPH_PROTOTYPE</type>
                            <name>Status</name>
                            <x>0</x>
                            <y>0</y>
                            <width>12</width>
                            <height>7</height>
                            <fields>
                                <field>
                                    <name>graph</name>
                                    <value>
                                        <host>Dell OpenManage Enterprise by HTTP agent</host>
                                        <name>{#DeviceName}: Status History</name>
                                    </value>
                                </field>
                            </fields>
                        </widget>
                        <widget>
                            <type>GRAPH_PROTOTYPE</type>
                            <name>Temperature</name>
                            <x>12</x>
                            <y>0</y>
                            <width>12</width>
                            <height>7</height>
                            <fields>
                                <field>
                                    <name>graph</name>
                                    <value>
                                        <host>Dell OpenManage Enterprise by HTTP agent</host>
                                        <name>{#DeviceName}: Temperature</name>
                                    </value>
                                </field>
                            </fields>
                        </widget>
                    </widgets>
                </page>
            </pages>
        </dashboard>
    </dashboards>
</zabbix_export>
```

### Импорт dashboard

1. **Dashboard → Import**
2. Выберите `dashboard_dell_ome.xml`
3. **Import**

### Преимущества

| ✅ | ❌ |
| :--- | :--- |
| Не изменяет шаблон | Нужно импортировать отдельно |
| Простое создание через UI | Не привязан к версии шаблона |
| Можно обновлять шаблон независимо | |

---

## 📋 Вариант 2: Python скрипт (Zabbix API)

### Скрипт для создания dashboard

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Dell OME Dashboard via Zabbix API
Usage: python create_dashboard.py
"""
from pyzabbix import ZabbixAPI

# Configuration
ZABBIX_URL = 'https://zabbix-server'
ZABBIX_USER = 'admin'
ZABBIX_PASSWORD = 'password'
TEMPLATE_NAME = 'Dell OpenManage Enterprise by HTTP agent'
DASHBOARD_NAME = 'Dell OME Monitoring'

def main():
    # Connect to Zabbix
    print(f"Connecting to {ZABBIX_URL}...")
    zapi = ZabbixAPI(ZABBIX_URL)
    zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)
    print("Connected!")
    
    # Get template
    print(f"Finding template: {TEMPLATE_NAME}...")
    templates = zapi.template.get({
        'output': ['templateid', 'name'],
        'filter': {'template': TEMPLATE_NAME}
    })
    
    if not templates:
        print(f"Template not found: {TEMPLATE_NAME}")
        return
    
    template = templates[0]
    print(f"Found template: {template['name']}")
    
    # Create dashboard
    print(f"Creating dashboard: {DASHBOARD_NAME}...")
    dashboard = zapi.dashboard.create({
        'name': DASHBOARD_NAME,
        'private': False,
        'pages': [
            {
                'name': 'Overview',
                'widgets': [
                    {
                        'type': 'PROBLEMS',
                        'name': 'Problems',
                        'x': 0,
                        'y': 0,
                        'width': 12,
                        'height': 7,
                        'fields': [
                            {'name': 'problemTags', 'value': 'Dell'},
                            {'name': 'showSeverity', 'value': '1'}
                        ]
                    },
                    {
                        'type': 'SYSTEM',
                        'name': 'System status',
                        'x': 12,
                        'y': 0,
                        'width': 12,
                        'height': 7
                    }
                ]
            },
            {
                'name': 'Devices',
                'widgets': [
                    {
                        'type': 'GRAPH_PROTOTYPE',
                        'name': 'Status',
                        'x': 0,
                        'y': 0,
                        'width': 12,
                        'height': 7,
                        'fields': [
                            {
                                'name': 'graph',
                                'value': {
                                    'host': TEMPLATE_NAME,
                                    'name': '{#DeviceName}: Status History'
                                }
                            }
                        ]
                    },
                    {
                        'type': 'GRAPH_PROTOTYPE',
                        'name': 'Temperature',
                        'x': 12,
                        'y': 0,
                        'width': 12,
                        'height': 7,
                        'fields': [
                            {
                                'name': 'graph',
                                'value': {
                                    'host': TEMPLATE_NAME,
                                    'name': '{#DeviceName}: Temperature'
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    })
    
    print(f"✅ Dashboard created: {dashboard['dashboardids']}")

if __name__ == '__main__':
    main()
```

### Установка зависимостей

```bash
pip install pyzabbix
```

### Запуск

```bash
python create_dashboard.py
```

### Преимущества

| ✅ | ❌ |
| :--- | :--- |
| Полная автоматизация | Требует Python + pyzabbix |
| Массовое создание | Нужны права API |
| Интеграция в CI/CD | |

---

## 📋 Вариант 3: cURL + Zabbix API

### Получение auth token

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "admin",
        "password": "password"
    },
    "id": 1
  }' \
  http://zabbix-server/api_jsonrpc.php
```

### Создание dashboard

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "dashboard.create",
    "params": {
        "name": "Dell OME Monitoring",
        "private": false,
        "pages": [
            {
                "name": "Overview",
                "widgets": [
                    {
                        "type": "PROBLEMS",
                        "x": 0,
                        "y": 0,
                        "width": 12,
                        "height": 7
                    }
                ]
            }
        ]
    },
    "auth": "AUTH_TOKEN_FROM_PREVIOUS_STEP",
    "id": 1
  }' \
  http://zabbix-server/api_jsonrpc.php
```

---

## 📊 Рекомендуемые виджеты для Dell OME

### Страница: Overview

| Виджет | Тип | Размер | Данные |
| :--- | :--- | :--- | :--- |
| Problems | PROBLEMS | 12x7 | Tag: Dell |
| System status | SYSTEM | 12x7 | Общая статистика |
| Session status | ITEM | 6x7 | ome.session.status |
| Devices discovered | ITEM | 6x7 | ome.device.discovery |

### Страница: Devices

| Виджет | Тип | Размер | Данные |
| :--- | :--- | :--- | :--- |
| Status History | GRAPH_PROTOTYPE | 12x7 | {#DeviceName}: Status |
| Power State | GRAPH_PROTOTYPE | 12x7 | {#DeviceName}: Power |
| Temperature | GRAPH_PROTOTYPE | 12x7 | {#DeviceName}: Temperature |
| Health | GRAPH_PROTOTYPE | 12x7 | {#DeviceName}: Health |

### Страница: Alerts

| Виджет | Тип | Размер | Данные |
| :--- | :--- | :--- | :--- |
| Critical | PROBLEMS | 24x7 | Severity: Disaster/High |
| Warning | PROBLEMS | 24x7 | Severity: Average |
| Timeline | ITEM | 24x7 | Status history |

---

## 📁 Структура файлов в репозитории

```
c:\Users\v.krasnikov\zabbix-template-api-dell-openmanage-enterprise\
├── template_dell_ome_7.0.xml         # Шаблон (без изменений)
├── dashboards/
│   ├── dashboard_dell_ome.xml        # Вариант 1: XML экспорт
│   └── create_dashboard.py           # Вариант 2: Python скрипт
└── DASHBOARDS.md                     # Эта документация
```

---

## 📝 Сравнение вариантов

| Критерий | Вариант 1 (XML) | Вариант 2 (Python) | Вариант 3 (cURL) |
| :--- | :--- | :--- | :--- |
| **Сложность** | Низкая | Средняя | Высокая |
| **Автоматизация** | ❌ | ✅ | ✅ |
| **Требования** | Zabbix UI | Python + pyzabbix | cURL + API |
| **Массовое создание** | ❌ | ✅ | ✅ |
| **Рекомендация** | ✅ Для 1 хоста | ✅ Для многих | ⚠️ Для скриптов |

---

## 🎯 Пошаговая инструкция (Вариант 1)

### Шаг 1: Импортируйте шаблон

1. **Data collection → Templates**
2. **Import** → выберите `template_dell_ome_7.0.xml`
3. **Import**

### Шаг 2: Создайте хост

1. **Data collection → Hosts**
2. **Create host**
3. Name: Dell OME Server
4. Templates: Dell OpenManage Enterprise by HTTP agent
5. Macros: настройте `{$OME_HOST}`, `{$OME_USER}`, `{$OME_PASSWORD}`
6. **Add**

### Шаг 3: Создайте dashboard

1. **Dashboard → Create dashboard**
2. Добавьте виджеты:
   - Problems (Problems widget)
   - System status (System widget)
   - Graph prototype (для температуры, статуса)
3. **Save**

### Шаг 4: Экспортируйте dashboard

1. **Dashboard → Export**
2. Выберите dashboard
3. **Export** → XML
4. Сохраните как `dashboards/dashboard_dell_ome.xml`

---

## 🔧 Готовые решения

### Виджет: Problems

```
Type: PROBLEMS
Name: Dell OME Problems
X: 0, Y: 0
Width: 12, Height: 7
Fields:
  - problemTags: Dell
  - showSeverity: 1
```

### Виджет: System Status

```
Type: SYSTEM
Name: System status
X: 12, Y: 0
Width: 12, Height: 7
```

### Виджет: Graph Prototype (Temperature)

```
Type: GRAPH_PROTOTYPE
Name: Temperature
X: 0, Y: 7
Width: 12, Height: 7
Fields:
  - graph:
      host: Dell OpenManage Enterprise by HTTP agent
      name: {#DeviceName}: Temperature
```

---

## ✅ Итог

**Для добавления dashboard НЕ нужно изменять `template_dell_ome_7.0.xml`!**

### Рекомендации:

| Сценарий | Вариант |
| :--- | :--- |
| **Один хост** | Вариант 1: UI → Export XML |
| **Несколько хостов** | Вариант 2: Python скрипт |
| **Автоматизация** | Вариант 2 или 3: API |
| **Документирование** | Сохраните XML в репозиторий |

---

**Дата:** 2026-03-31  
**Версия:** 1.0
