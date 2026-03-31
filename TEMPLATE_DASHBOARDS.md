# Включение Dashboards в шаблон Zabbix 7.0

## Варианты добавления dashboards в template_dell_ome_1.1.xml

**Готовый файл с dashboard:** `template_dell_ome_1.1_db.xml`

---

## 📋 Вариант 1: Dashboard внутри шаблона (Zabbix 7.0+)

### Рекомендуемый способ для Zabbix 7.0+

### Структура XML

Dashboard добавляется **внутри** элемента `<template>`, после `<discovery_rules>` и перед закрывающим `</template>`:

```xml
<templates>
    <template>
        <template>Dell OpenManage Enterprise by HTTP agent</template>
        <name>Dell OpenManage Enterprise by HTTP agent</name>
        ...
        
        <!-- Discovery rules -->
        <discovery_rules>
            ...
        </discovery_rules>
        
        <!-- Dashboard (добавляется здесь) -->
        <dashboards>
            <dashboard>
                <name>Dell OME Monitoring Dashboard</name>
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
                                </fields>
                            </widget>
                        </widgets>
                    </page>
                </pages>
            </dashboard>
        </dashboards>
        
    </template>
</templates>
```

### Полная структура template

```text
<template>
    ├── <template>          # Имя шаблона
    ├── <name>              # Видимое имя
    ├── <description>       # Описание
    ├── <groups>            # Группы
    ├── <macros>            # Макросы
    ├── <applications>      # Приложения
    ├── <items>             # Items
    ├── <discovery_rules>   # Discovery rules
    ├── <dashboards>        # ← Dashboard (добавляется здесь)
    └── </template>
</template>
```

---

## 📋 Вариант 2: Генерация через Python скрипт

### Скрипт для добавления dashboard в XML

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dashboard to Zabbix template XML
"""
import xml.etree.ElementTree as ET
from xml.dom import minidom

def add_dashboard_to_template(xml_file):
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find template element
    template = root.find('.//template')
    
    # Check if dashboards already exist
    if template.find('dashboards') is not None:
        print("Dashboard already exists in template")
        return
    
    # Create dashboard element
    dashboards = ET.SubElement(template, 'dashboards')
    dashboard = ET.SubElement(dashboards, 'dashboard')
    
    # Add dashboard name
    ET.SubElement(dashboard, 'name').text = 'Dell OME Monitoring Dashboard'
    ET.SubElement(dashboard, 'private').text = '0'
    
    # Add pages
    pages = ET.SubElement(dashboard, 'pages')
    
    # Page 1: Overview
    page1 = ET.SubElement(pages, 'page')
    ET.SubElement(page1, 'name').text = 'Overview'
    
    widgets1 = ET.SubElement(page1, 'widgets')
    
    # Widget 1: Problems
    widget1 = ET.SubElement(widgets1, 'widget')
    ET.SubElement(widget1, 'type').text = 'PROBLEMS'
    ET.SubElement(widget1, 'name').text = 'Problems'
    ET.SubElement(widget1, 'x').text = '0'
    ET.SubElement(widget1, 'y').text = '0'
    ET.SubElement(widget1, 'width').text = '12'
    ET.SubElement(widget1, 'height').text = '7'
    
    fields1 = ET.SubElement(widget1, 'fields')
    field1 = ET.SubElement(fields1, 'field')
    ET.SubElement(field1, 'name').text = 'problemTags'
    ET.SubElement(field1, 'value').text = 'Dell'
    
    # Widget 2: System
    widget2 = ET.SubElement(widgets1, 'widget')
    ET.SubElement(widget2, 'type').text = 'SYSTEM'
    ET.SubElement(widget2, 'name').text = 'System status'
    ET.SubElement(widget2, 'x').text = '12'
    ET.SubElement(widget2, 'y').text = '0'
    ET.SubElement(widget2, 'width').text = '12'
    ET.SubElement(widget2, 'height').text = '7'
    
    # Page 2: Devices
    page2 = ET.SubElement(pages, 'page')
    ET.SubElement(page2, 'name').text = 'Devices'
    
    widgets2 = ET.SubElement(page2, 'widgets')
    
    # Widget 3: Status Graph
    widget3 = ET.SubElement(widgets2, 'widget')
    ET.SubElement(widget3, 'type').text = 'GRAPH_PROTOTYPE'
    ET.SubElement(widget3, 'name').text = 'Status'
    ET.SubElement(widget3, 'x').text = '0'
    ET.SubElement(widget3, 'y').text = '0'
    ET.SubElement(widget3, 'width').text = '12'
    ET.SubElement(widget3, 'height').text = '7'
    
    fields3 = ET.SubElement(widget3, 'fields')
    field3 = ET.SubElement(fields3, 'field')
    ET.SubElement(field3, 'name').text = 'graph'
    value3 = ET.SubElement(field3, 'value')
    ET.SubElement(value3, 'host').text = 'Dell OpenManage Enterprise by HTTP agent'
    ET.SubElement(value3, 'name').text = '{#DeviceName}: Status History'
    
    # Save XML
    tree.write(xml_file, encoding='UTF-8', xml_declaration=True)
    print(f"Dashboard added to {xml_file}")

if __name__ == '__main__':
    add_dashboard_to_template('template_dell_ome_7.0.xml')
```

### Запуск

```bash
python add_dashboard.py
```

---

## 📋 Вариант 3: Ручное редактирование XML

### Шаг 1: Найдите место для вставки

Откройте `template_dell_ome_1.1.xml` и найдите закрывающий тег `</discovery_rules>`:

```xml
      </discovery_rules>
      <!-- ВСТАВИТЬ DASHBOARD ЗДЕСЬ -->
    </template>
```

### Шаг 2: Вставьте dashboard

После `</discovery_rules>` вставьте:

```xml
    <dashboards>
        <dashboard>
            <name>Dell OME Monitoring Dashboard</name>
            <private>0</private>
            <pages>
                <!-- Страницы и виджеты -->
            </pages>
        </dashboard>
    </dashboards>
```

### Шаг 3: Сохраните и проверьте

```bash
# Проверка XML
python -c "import xml.etree.ElementTree as ET; ET.parse('template_dell_ome_1.1_db.xml'); print('XML Valid')"
```

---

## 📊 Полный пример dashboard для вставки

```xml
<dashboards>
    <dashboard>
        <name>Dell OME Monitoring Dashboard</name>
        <private>0</private>
        <pages>
            <!-- Страница 1: Overview -->
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
            
            <!-- Страница 2: Devices -->
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
                        <name>Power</name>
                        <x>12</x>
                        <y>0</y>
                        <width>12</width>
                        <height>7</height>
                        <fields>
                            <field>
                                <name>graph</name>
                                <value>
                                    <host>Dell OpenManage Enterprise by HTTP agent</host>
                                    <name>{#DeviceName}: Power State History</name>
                                </value>
                            </field>
                        </fields>
                    </widget>
                    <widget>
                        <type>GRAPH_PROTOTYPE</type>
                        <name>Temperature</name>
                        <x>0</x>
                        <y>7</y>
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
                    <widget>
                        <type>GRAPH_PROTOTYPE</type>
                        <name>Health</name>
                        <x>12</x>
                        <y>7</y>
                        <width>12</width>
                        <height>7</height>
                        <fields>
                            <field>
                                <name>graph</name>
                                <value>
                                    <host>Dell OpenManage Enterprise by HTTP agent</host>
                                    <name>{#DeviceName}: Health</name>
                                </value>
                            </field>
                        </fields>
                    </widget>
                </widgets>
            </page>
            
            <!-- Страница 3: Alerts -->
            <page>
                <name>Alerts</name>
                <widgets>
                    <widget>
                        <type>PROBLEMS</type>
                        <name>Critical Alerts</name>
                        <x>0</x>
                        <y>0</y>
                        <width>24</width>
                        <height>7</height>
                        <fields>
                            <field>
                                <name>severity</name>
                                <value>4,5</value>
                            </field>
                        </fields>
                    </widget>
                    <widget>
                        <type>PROBLEMS</type>
                        <name>Warning Alerts</name>
                        <x>0</x>
                        <y>7</y>
                        <width>24</width>
                        <height>7</height>
                        <fields>
                            <field>
                                <name>severity</name>
                                <value>2,3</value>
                            </field>
                        </fields>
                    </widget>
                </widgets>
            </page>
        </pages>
    </dashboard>
</dashboards>
```

---

## 🔧 Позиции виджетов

### Сетка dashboard

```text
Y=0  +----------------+----------------+
     | Problems       | System         |
     | (0,0) 12x7     | (12,0) 12x7    |
Y=7  +----------------+----------------+
     | Status         | Power          |
     | (0,7) 12x7     | (12,7) 12x7    |
Y=14 +----------------+----------------+
```

### Правила

| Параметр | Описание |
| :--- | :--- |
| **x** | Позиция по горизонтали (0-24) |
| **y** | Позиция по вертикали (0+) |
| **width** | Ширина (1-24) |
| **height** | Высота (1+) |

---

## 📝 Сравнение вариантов

| Критерий | Вариант 1 | Вариант 2 | Вариант 3 |
| :--- | :--- | :--- | :--- |
| **Сложность** | Средняя | Низкая | Высокая |
| **Автоматизация** | ❌ | ✅ | ❌ |
| **Точность** | ✅ | ✅ | ⚠️ |
| **Рекомендация** | ✅ Ручное | ✅ Скрипт | ⚠️ Ручное |

---

## ✅ Проверка после добавления

### 1. Валидация XML

```bash
python -c "import xml.etree.ElementTree as ET; ET.parse('template_dell_ome_7.0.xml'); print('✅ XML Valid')"
```

### 2. Проверка структуры

```bash
python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('template_dell_ome_7.0.xml')
root = tree.getroot()
dashboard = root.find('.//dashboard')
if dashboard is not None:
    print('✅ Dashboard found')
    print(f\"   Name: {dashboard.find('name').text}\")
else:
    print('❌ Dashboard not found')
"
```

### 3. Импорт в Zabbix

1. **Data collection → Templates**
2. **Import**
3. Выберите `template_dell_ome_7.0.xml`
4. **Import**
5. Проверьте: **Dashboard → Dell OME Monitoring Dashboard**

---

## 🎯 Рекомендации

### Для Zabbix 7.0+

**Используйте Вариант 1** — dashboard внутри шаблона:

```xml
<templates>
    <template>
        ...
        <discovery_rules>...</discovery_rules>
        <dashboards>...</dashboards>  ← Добавьте здесь
    </template>
</templates>
```

### Преимущества

| ✅ | ❌ |
| :--- | :--- |
| Dashboard импортируется с шаблоном | Увеличивает размер XML |
| Автоматически применяется | Только Zabbix 7.0+ |
| Использует LLD макросы | Сложная структура |

---

## 📁 Структура файла после добавления

```text
template_dell_ome_7.0.xml (с dashboard)
├── <zabbix_export>
│   ├── <version>7.0</version>
│   ├── <templates>
│   │   └── <template>
│   │       ├── <template>...</template>
│   │       ├── <macros>...</macros>
│   │       ├── <items>...</items>
│   │       ├── <discovery_rules>...</discovery_rules>
│   │       ├── <dashboards>...</dashboards>  ← Добавлено
│   │       └── </template>
│   │   └── </templates>
│   └── <value_maps>...</value_maps>
└── </zabbix_export>
```

---

**Выбор зависит от вашего сценария!**
