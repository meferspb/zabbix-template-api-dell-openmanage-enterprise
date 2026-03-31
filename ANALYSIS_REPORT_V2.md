# Отчёт по анализу API Dell OpenManage Enterprise
## Дополнительные метрики для мониторинга устройств

**Дата:** 31 марта 2026 г.  
**Версия анализа:** 2.0  
**Статус:** ✅ Готово к внедрению

---

## 📋 СОДЕРЖАНИЕ

- [Резюме](#резюме)
- [Текущее состояние шаблона](#текущее-состояние-шаблона)
- [Рекомендуемые новые метрики](#рекомендуемые-новые-метрики)
- [Детальное описание API endpoints](#детальное-описание-api-endpoints)
- [Приоритеты внедрения](#приоритеты-внедрения)
- [Примеры JSON ответов](#примеры-json-ответов)
- [Рекомендации по реализации](#рекомендации-по-реализации)

---

## РЕЗЮМЕ

Проведён полный анализ API Dell OpenManage Enterprise v3.x для выявления дополнительных метрик мониторинга.

### Поддерживаемые устройства

| Тип устройства | Модели | Статус |
| :--- | :--- | :--- |
| **Серверы** | Dell PowerEdge (все модели) | ✅ Поддерживаются |
| **Шасси** | Dell Chassis (MX7000, FX2, VRTX) | ✅ Поддерживаются |
| **Сеть** | Dell Networking (N-Series, Z-Series, S-Series) | ✅ Поддерживаются |
| **Storage** | Dell Storage (SC, PS, Compellent) | ✅ Поддерживаются |

### Итоговые цифры

| Категория | Количество |
| :--- | :--- |
| **Текущие метрики в шаблоне** | 8 |
| **Рекомендуемые новые метрики** | 47+ |
| **Новых API endpoints** | 35+ |
| **Новых приложений** | 12 |

---

## ТЕКУЩЕЕ СОСТОЯНИЕ ШАБЛОНА

### Реализованные метрики (v1.1)

| № | Метрика | Ключ | Приложение |
| :--- | :--- | :--- | :--- |
| 1 | Статус устройства | `ome.device[{#Id}.status]` | Status |
| 2 | Питание | `ome.device[{#Id}.power]` | Power |
| 3 | Модель | `ome.device[{#Id}.model]` | Discovery |
| 4 | Service Tag | `ome.device[{#Id}.tag]` | Discovery |
| 5 | Identifier | `ome.device[{#Id}.identifier]` | Discovery |
| 6 | Подключение | `ome.device[{#Id}.connection]` | Status |
| 7 | Температура | `ome.device[{#Id}.temperature]` | Temperature |
| 8 | Здоровье | `ome.device[{#Id}.health]` | Health |

---

## РЕКОМЕНДУЕМЫЕ НОВЫЕ МЕТРИКИ

### 1. 🖥️ ИНВЕНТАРИЗАЦИЯ (Inventory)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 1.1 | **CPU Count** | UINT | шт | Количество процессоров |
| 1.2 | **CPU Cores Total** | UINT | шт | Общее количество ядер |
| 1.3 | **CPU Model** | TEXT | - | Модель процессора |
| 1.4 | **CPU Max Speed** | UINT | MHz | Максимальная частота |
| 1.5 | **CPU Current Speed** | UINT | MHz | Текущая частота |
| 1.6 | **Memory Total Size** | UINT | MB | Общий объём памяти |
| 1.7 | **Memory Modules Count** | UINT | шт | Количество модулей |
| 1.8 | **Memory Manufacturer** | TEXT | - | Производитель памяти |
| 1.9 | **Disk Count** | UINT | шт | Количество дисков |
| 1.10 | **Disk Total Size** | UINT | GB | Общий объём дисков |
| 1.11 | **Disk Free Space** | UINT | GB | Свободное место |
| 1.12 | **RAID Controller Model** | TEXT | - | Модель RAID контроллера |
| 1.13 | **RAID Cache Size** | UINT | MB | Кэш RAID контроллера |
| 1.14 | **Network Interfaces Count** | UINT | шт | Количество сетевых интерфейсов |
| 1.15 | **Power Supply Count** | UINT | шт | Количество блоков питания |
| 1.16 | **Power Supply Wattage** | UINT | W | Мощность БП |
| 1.17 | **Storage Enclosure Count** | UINT | шт | Количество корпусов хранения |
| 1.18 | **Device Cards Count** | UINT | шт | Количество карт расширения |
| 1.19 | **Operating System** | TEXT | - | Операционная система |
| 1.20 | **BIOS Version** | TEXT | - | Версия BIOS |

**API Endpoints:**
```
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverProcessors')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverMemoryDevices')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverArrayDisks')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverRaidControllers')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverNetworkInterfaces')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverPowerSupplies')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverStorageEnclosures')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverDeviceCards')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverOperatingSystems')
GET /api/DeviceService/Devices({Id})/InventoryDetails('deviceSoftware')
```

---

### 2. ⚡ ЭНЕРГОПОТРЕБЛЕНИЕ (Power Metrics)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 2.1 | **Instant Power** | FLOAT | Вт | Текущее потребление |
| 2.2 | **Average Power** | FLOAT | Вт | Среднее потребление |
| 2.3 | **Maximum Power** | FLOAT | Вт | Максимальное потребление |
| 2.4 | **Minimum Power** | FLOAT | Вт | Минимальное потребление |
| 2.5 | **Energy Consumption** | FLOAT | кВт⋅ч | Потребленная энергия |
| 2.6 | **Power Supply Status** | UINT | 0/1/2/3 | Статус БП |
| 2.7 | **Power Supply Input Voltage** | FLOAT | В | Входное напряжение |
| 2.8 | **Power Supply Output Power** | FLOAT | Вт | Выходная мощность |
| 2.9 | **Power Budget** | FLOAT | Вт | Выделенный лимит |
| 2.10 | **Power Headroom** | FLOAT | Вт | Доступный резерв |

**API Endpoints:**
```
POST /api/MetricService/Metrics
POST /api/MetricService/EnergyConsumption
GET /api/DeviceService/Devices({Id})/PowerUsageByDevice
GET /redfish/v1/Chassis/Members({id})/Power
GET /redfish/v1/Chassis/Members({id})/Power/PowerSupplies({InstanceId})
```

**MetricType IDs для POST /api/MetricService/Metrics:**
```json
{
  "MetricTypes": [1, 2, 3, 4, 19],
  "DeviceIds": [10074]
}
```

---

### 3. 🌡️ ТЕМПЕРАТУРА И ОХЛАЖДЕНИЕ (Thermal)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 3.1 | **Inlet Temperature** | FLOAT | °C | Температура на входе |
| 3.2 | **Max Inlet Temperature** | FLOAT | °C | Макс. температура на входе |
| 3.3 | **Min Inlet Temperature** | FLOAT | °C | Мин. температура на входе |
| 3.4 | **Average Inlet Temperature** | FLOAT | °C | Сред. температура на входе |
| 3.5 | **CPU Temperature** | FLOAT | °C | Температура CPU |
| 3.6 | **System Temperature** | FLOAT | °C | Температура системы |
| 3.7 | **Fan Count** | UINT | шт | Количество вентиляторов |
| 3.8 | **Fan Speed [N]** | UINT | RPM | Скорость вентилятора N |
| 3.9 | **Fan Status [N]** | UINT | 0/1/2/3 | Статус вентилятора N |
| 3.10 | **System Airflow** | FLOAT | CFM | Поток воздуха |

**API Endpoints:**
```
GET /api/DeviceService/Devices({Id})/Temperature
GET /redfish/v1/Chassis/Members({id})/Thermal
GET /redfish/v1/Chassis/Members({id})/Thermal/Temperatures({InstanceId})
GET /redfish/v1/Chassis/Members({id})/Thermal/Fans({InstanceId})
POST /api/MetricService/Metrics (MetricType IDs: 5, 6, 7, 8, 18)
```

---

### 4. 💾 ХРАНИЛИЩЕ ДАННЫХ (Storage)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 4.1 | **Physical Disk Count** | UINT | шт | Количество физических дисков |
| 4.2 | **Virtual Disk Count** | UINT | шт | Количество виртуальных дисков |
| 4.3 | **Disk Status [N]** | UINT | 0-3 | Статус диска N |
| 4.4 | **Disk Size [N]** | UINT | GB | Размер диска N |
| 4.5 | **Disk Free Space [N]** | UINT | GB | Свободно на диске N |
| 4.6 | **Disk Used Space [N]** | UINT | GB | Занято на диске N |
| 4.7 | **RAID Level [N]** | TEXT | - | Уровень RAID N |
| 4.8 | **RAID Status [N]** | UINT | 0-3 | Статус RAID N |
| 4.9 | **Storage Enclosure Status** | UINT | 0-3 | Статус корпуса хранения |
| 4.10 | **Disk MediaType** | TEXT | - | Тип диска (HDD/SSD) |
| 4.11 | **Disk Remaining Endurance** | UINT | % | Остаточный ресурс SSD |
| 4.12 | **Controller Cache Size** | UINT | MB | Кэш контроллера |

**API Endpoints:**
```
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverArrayDisks')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverRaidControllers')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverStorageEnclosures')
GET /redfish/v1/Systems/Members({id})/SimpleStorage
GET /redfish/v1/Systems/Members({id})/SimpleStorage/Members({id})
```

---

### 5. 🔌 БЛОКИ ПИТАНИЯ (Power Supplies)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 5.1 | **PSU Count** | UINT | шт | Количество БП |
| 5.2 | **PSU Status [N]** | UINT | 0/1/2/3 | Статус БП N |
| 5.3 | **PSU Wattage [N]** | UINT | Вт | Мощность БП N |
| 5.4 | **PSU Input Voltage [N]** | FLOAT | В | Входное напряжение N |
| 5.5 | **PSU Output Power [N]** | FLOAT | Вт | Выходная мощность N |
| 5.6 | **PSU Model [N]** | TEXT | - | Модель БП N |
| 5.7 | **PSU Serial [N]** | TEXT | - | Серийный номер N |
| 5.8 | **PSU Redundancy** | UINT | 0/1/2 | Статус резервирования |
| 5.9 | **PSU AC Status [N]** | UINT | 0/1 | Питание переменным током N |

**API Endpoints:**
```
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverPowerSupplies')
GET /redfish/v1/Chassis/Members({id})/Power
GET /redfish/v1/Chassis/Members({id})/Power/PowerSupplies({InstanceId})
```

---

### 6. 🌀 ВЕНТИЛЯТОРЫ (Fans)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 6.1 | **Fan Count** | UINT | шт | Количество вентиляторов |
| 6.2 | **Fan Speed [N]** | UINT | RPM | Скорость вращения N |
| 6.3 | **Fan Status [N]** | UINT | 0/1/2/3 | Статус вентилятора N |
| 6.4 | **Fan Redundancy** | UINT | 0/1 | Резервирование вентиляторов |
| 6.5 | **Fan Health** | UINT | 0-3 | Здоровье вентилятора |

**API Endpoints:**
```
GET /redfish/v1/Chassis/Members({id})/Thermal
GET /redfish/v1/Chassis/Members({id})/Thermal/Fans({InstanceId})
```

---

### 7. 🖧 СЕТЕВЫЕ ИНТЕРФЕЙСЫ (Network)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 7.1 | **NIC Count** | UINT | шт | Количество интерфейсов |
| 7.2 | **NIC Link Status [N]** | UINT | 0/1 | Статус подключения N |
| 7.3 | **NIC Speed [N]** | UINT | Mbps | Скорость интерфейса N |
| 7.4 | **NIC MAC Address [N]** | TEXT | - | MAC-адрес N |
| 7.5 | **NIC Model [N]** | TEXT | - | Модель NIC N |
| 7.6 | **VLAN Count** | UINT | шт | Количество VLAN |
| 7.7 | **VLAN ID [N]** | UINT | - | ID VLAN N |

**API Endpoints:**
```
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverNetworkInterfaces')
GET /redfish/v1/Systems/Members({id})/EthernetInterfaces
GET /redfish/v1/Systems/Members({id})/EthernetInterfaces/Members({id})
```

---

### 8. 🎮 GPU (Графические ускорители)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 8.1 | **GPU Count** | UINT | шт | Количество GPU |
| 8.2 | **GPU Model [N]** | TEXT | - | Модель GPU N |
| 8.3 | **GPU Status [N]** | UINT | 0-3 | Статус GPU N |
| 8.4 | **GPU Memory Size [N]** | UINT | MB | Память GPU N |
| 8.5 | **GPU Temperature [N]** | FLOAT | °C | Температура GPU N |
| 8.6 | **GPU Utilization [N]** | FLOAT | % | Загрузка GPU N |

**API Endpoints:**
```
GET /api/DeviceService/Devices({Id})/GraphicInfo
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverDeviceCards')
```

---

### 9. 📊 УТИЛИЗАЦИЯ (Utilization)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 9.1 | **CPU Utilization (Max)** | FLOAT | % | Макс. загрузка CPU |
| 9.2 | **CPU Utilization (Min)** | FLOAT | % | Мин. загрузка CPU |
| 9.3 | **CPU Utilization (Avg)** | FLOAT | % | Сред. загрузка CPU |
| 9.4 | **Memory Utilization (Max)** | FLOAT | % | Макс. загрузка памяти |
| 9.5 | **Memory Utilization (Min)** | FLOAT | % | Мин. загрузка памяти |
| 9.6 | **Memory Utilization (Avg)** | FLOAT | % | Сред. загрузка памяти |
| 9.7 | **IO Utilization (Max)** | FLOAT | % | Макс. загрузка IO |
| 9.8 | **IO Utilization (Min)** | FLOAT | % | Мин. загрузка IO |
| 9.9 | **IO Utilization (Avg)** | FLOAT | % | Сред. загрузка IO |

**API Endpoints:**
```
POST /api/MetricService/Metrics
(MetricType IDs: 9-17)
```

---

### 10. 🔔 АЛЕРТЫ И СОБЫТИЯ (Alerts)

| № | Метрика | Тип данных | Описание |
| :--- | :--- | :--- | :--- |
| 10.1 | **Alert Count** | UINT | Количество алертов |
| 10.2 | **Critical Alert Count** | UINT | Критические алерты |
| 10.3 | **Warning Alert Count** | UINT | Предупреждения |
| 10.4 | **Last Alert Time** | TEXT | Время последнего алерта |
| 10.5 | **Last Alert Severity** | TEXT | Серьёзность последнего |
| 10.6 | **Last Alert Description** | TEXT | Описание последнего |

**API Endpoints:**
```
GET /api/AlertService/Alerts?$filter=SeverityType eq 'Critical'
GET /api/AlertService/Alerts?$filter=SeverityType eq 'Warning'
GET /api/AlertService/Alerts?$top=1&$orderby=CreatedDate desc
```

---

### 11. 🖥️ ШАССИ (Chassis)

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 11.1 | **Chassis Model** | TEXT | - | Модель шасси |
| 11.2 | **Chassis Status** | UINT | 0-3 | Статус шасси |
| 11.3 | **Chassis Power Status** | UINT | 0/1/2 | Питание шасси |
| 11.4 | **Chassis Temperature** | FLOAT | °C | Температура шасси |
| 11.5 | **Chassis Fan Count** | UINT | шт | Вентиляторы шасси |
| 11.6 | **Chassis PSU Count** | UINT | шт | Блоки питания шасси |
| 11.7 | **Chassis Server Count** | UINT | шт | Количество серверов |
| 11.8 | **Chassis Manager Status** | UINT | 0-3 | Статус менеджера |

**API Endpoints:**
```
GET /redfish/v1/Chassis
GET /redfish/v1/Chassis/Members({id})
GET /api/DeviceService/Devices({Id})/InventoryDetails
```

---

### 12. 📈 СИСТЕМНАЯ ИНФОРМАЦИЯ

| № | Метрика | Тип данных | Единицы | Описание |
| :--- | :--- | :--- | :--- | :--- |
| 12.1 | **System Up Time** | UINT | сек | Время работы |
| 12.2 | **BIOS Version** | TEXT | - | Версия BIOS |
| 12.3 | **BIOS Release Date** | TEXT | - | Дата выпуска BIOS |
| 12.4 | **iDRAC Version** | TEXT | - | Версия iDRAC |
| 12.5 | **iDRAC IP Address** | TEXT | - | IP-адрес iDRAC |
| 12.6 | **Firmware Version** | TEXT | - | Версия прошивки |
| 12.7 | **Device Capabilities** | TEXT | - | Возможности устройства |

**API Endpoints:**
```
GET /api/DeviceService/Devices({Id})/SystemUpTime
GET /api/DeviceService/Devices({Id})/InventoryDetails('deviceSoftware')
GET /api/DeviceService/Devices({Id})/InventoryDetails('deviceCapabilities')
GET /api/DeviceService/Devices({Id})/InventoryDetails('deviceManagement')
```

---

## ДЕТАЛЬНОЕ ОПИСАНИЕ API ENDPOINTS

### Базовые endpoints

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/SessionService/Sessions` | POST | Аутентификация |
| `/api/DeviceService/Devices` | GET | Список устройств |
| `/api/DeviceService/Devices({Id})` | GET | Информация об устройстве |

### Инвентаризация

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/DeviceService/Devices({Id})/InventoryDetails` | GET | Все детали инвентаризации |
| `/api/DeviceService/Devices({Id})/InventoryDetails('{Type}')` | GET | Детали по типу |
| `/api/DeviceService/Devices({Id})/InventoryTypes` | GET | Доступные типы |

**Доступные InventoryType:**
- `serverProcessors` — Процессоры
- `serverMemoryDevices` — Память
- `serverArrayDisks` — Диски
- `serverRaidControllers` — RAID контроллеры
- `serverNetworkInterfaces` — Сетевые интерфейсы
- `serverPowerSupplies` — Блоки питания
- `serverStorageEnclosures` — Корпуса хранения
- `serverDeviceCards` — Карты расширения
- `serverOperatingSystems` — ОС
- `deviceSoftware` — ПО
- `deviceCapabilities` — Возможности
- `deviceManagement` — Управление
- `deviceFru` — FRU информация
- `deviceLicense` — Лицензии
- `subsystemRollupStatus` — Статус подсистем

### Метрики

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/MetricService/Metrics` | POST | Метрики устройств |
| `/api/MetricService/MetricTypes` | GET | Типы метрик |
| `/api/MetricService/EnergyConsumption` | POST | Энергопотребление |
| `/api/MetricService/TopEnergyConsumption` | POST | Топ потребители |
| `/api/MetricService/TopOffenders` | GET | Проблемные устройства |
| `/api/MetricService/Threshold` | POST | Пороги метрик |

### Redfish endpoints

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/redfish/v1/Systems` | GET | Системы |
| `/redfish/v1/Systems/Members({id})` | GET | Система по ID |
| `/redfish/v1/Systems/Members({id})/Processors` | GET | Процессоры |
| `/redfish/v1/Systems/Members({id})/SimpleStorage` | GET | Хранилище |
| `/redfish/v1/Systems/Members({id})/EthernetInterfaces` | GET | Сетевые интерфейсы |
| `/redfish/v1/Chassis` | GET | Шасси |
| `/redfish/v1/Chassis/Members({id})` | GET | Шасси по ID |
| `/redfish/v1/Chassis/Members({id})/Thermal` | GET | Тепловая информация |
| `/redfish/v1/Chassis/Members({id})/Power` | GET | Питание |
| `/redfish/v1/Managers` | GET | Менеджеры (iDRAC) |

### Алерты

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/AlertService/Alerts` | GET | Все алерты |
| `/api/AlertService/Alerts?$filter=...` | GET | Фильтрованные алерты |
| `/api/AlertService/AlertCategories` | GET | Категории алертов |

---

## ПРИОРИТЕТЫ ВНЕДРЕНИЯ

### 🔴 Критические (Phase 1)

| Приоритет | Метрика | Обоснование |
| :--- | :--- | :--- |
| P1 | Энергопотребление | Критично для ЦОД |
| P1 | Блоки питания | Отказ = простой |
| P1 | Вентиляторы | Перегрев = отказ |
| P1 | Диски/RAID | Потеря данных |
| P1 | Алерты | Реагирование на инциденты |

### 🟡 Важные (Phase 2)

| Приоритет | Метрика | Обоснование |
| :--- | :--- | :--- |
| P2 | CPU/Memory утилизация | Производительность |
| P2 | Температура | Предотвращение проблем |
| P2 | Сетевые интерфейсы | Доступность сети |
| P2 | Инвентаризация | Учёт активов |

### 🟢 Дополнительные (Phase 3)

| Приоритет | Метрика | Обоснование |
| :--- | :--- | :--- |
| P3 | GPU | Специализированные серверы |
| P3 | Шасси | Модульные системы |
| P3 | VLAN | Детальная информация |
| P3 | System Up Time | Мониторинг доступности |

---

## ПРИМЕРЫ JSON ОТВЕТОВ

### CPU (serverProcessors)

```json
{
    "@odata.id": "/api/DeviceService/Devices(3315)/InventoryDetails('serverProcessors')",
    "InventoryType": "serverProcessors",
    "InventoryInfo": [
        {
            "Id": 28,
            "Family": "Intel(R) Xeon(TM)",
            "MaxSpeed": 4000,
            "CurrentSpeed": 1600,
            "SlotNumber": "CPU.Socket.1",
            "Status": 2000,
            "NumberOfCores": 8,
            "NumberOfEnabledCores": 8,
            "BrandName": "Intel",
            "ModelName": "Genuine Intel(R) CPU 0000%@",
            "InstanceId": "CPU.Socket.1",
            "Voltage": "1.8"
        }
    ]
}
```

### Memory (serverMemoryDevices)

```json
{
    "@odata.id": "/api/DeviceService/Devices(3315)/InventoryDetails('serverMemoryDevices')",
    "InventoryType": "serverMemoryDevices",
    "InventoryInfo": [
        {
            "Id": 19,
            "Name": "DIMM.Socket.A1",
            "BankName": "A",
            "Size": 8192,
            "Status": 2000,
            "Manufacturer": "Micron Technology",
            "PartNumber": "9ASF1G72PZ-2G6D1",
            "Speed": 2666,
            "CurrentOperatingSpeed": 2133,
            "Rank": "Single Rank",
            "InstanceId": "DIMM.Socket.A1"
        }
    ]
}
```

### Disks (serverArrayDisks)

```json
{
    "@odata.id": "/api/DeviceService/Devices(3315)/InventoryDetails('serverArrayDisks')",
    "InventoryType": "serverArrayDisks",
    "InventoryInfo": [
        {
            "Id": 10,
            "DiskNumber": "Disk 0 on Embedded AHCI Controller 2",
            "VendorName": "SEAGATE",
            "Status": 2000,
            "ModelNumber": "ST1000NX0423",
            "SerialNumber": "S47171Y1",
            "Size": "931.52 GB",
            "FreeSpace": "0 bytes",
            "BusType": "SATA",
            "MediaType": "Magnetic Drive",
            "RemainingReadWriteEndurance": "255"
        }
    ]
}
```

### RAID Controllers

```json
{
    "@odata.id": "/api/DeviceService/Devices(3315)/InventoryDetails('serverRaidControllers')",
    "InventoryType": "serverRaidControllers",
    "InventoryInfo": [
        {
            "Id": 20,
            "Name": "PERC H730P Mini",
            "Fqdd": "RAID.Slot.1-1",
            "Status": 2000,
            "RollupStatus": 2000,
            "CacheSizeInMb": 2048,
            "PciSlot": 0
        }
    ]
}
```

### Power Supplies

```json
{
    "@odata.id": "/api/DeviceService/Devices(3315)/InventoryDetails('serverPowerSupplies')",
    "InventoryType": "serverPowerSupplies",
    "InventoryInfo": [
        {
            "Id": 50,
            "Name": "PSU 1",
            "Model": "Dell 750W",
            "SerialNumber": "PH12345",
            "Status": 2000,
            "Wattage": 750,
            "InputVoltage": 220,
            "OutputPower": 150
        }
    ]
}
```

### Metrics (POST /api/MetricService/Metrics)

**Запрос:**
```json
{
    "DeviceIds": [10074],
    "MetricTypes": [1, 2, 3, 4, 9, 11, 12, 14]
}
```

**Ответ:**
```json
{
    "Metrics": [
        {
            "DeviceId": 10074,
            "MetricTypeId": 1,
            "MetricTypeName": "MAX_POWER",
            "Value": 450.5,
            "Unit": "Watts",
            "Timestamp": "2026-03-31T12:00:00Z"
        },
        {
            "DeviceId": 10074,
            "MetricTypeId": 4,
            "MetricTypeName": "INSTANT_POWER",
            "Value": 320.2,
            "Unit": "Watts",
            "Timestamp": "2026-03-31T12:00:00Z"
        },
        {
            "DeviceId": 10074,
            "MetricTypeId": 11,
            "MetricTypeName": "AVG_UTIL_CPU",
            "Value": 45.5,
            "Unit": "Percent",
            "Timestamp": "2026-03-31T12:00:00Z"
        }
    ]
}
```

### Alerts

```json
{
    "@odata.count": 5,
    "value": [
        {
            "Id": 12345,
            "DeviceName": "PowerEdge R840",
            "SeverityType": "Critical",
            "CategoryName": "System Health",
            "Description": "Power Supply 1 failed",
            "CreatedDate": "2026-03-31T10:30:00Z",
            "Status": "New"
        }
    ]
}
```

---

## РЕКОМЕНДАЦИИ ПО РЕАЛИЗАЦИИ

### 1. Структура шаблона v2.0

```text
Dell OpenManage Enterprise by HTTP agent (v2.0)
│
├── 📊 Макросы (15)
│   ├── {$OME_HOST}
│   ├── {$OME_USER}
│   ├── {$OME_PASSWORD}
│   ├── {$OME_UPDATE_INTERVAL}
│   ├── {$OME_TIMEOUT}
│   ├── {$TEMP_WARN_THRESHOLD}
│   ├── {$TEMP_CRIT_THRESHOLD}
│   ├── {$POWER_WARN_THRESHOLD}
│   ├── {$DISK_WARN_THRESHOLD}
│   ├── {$MEMORY_WARN_THRESHOLD}
│   ├── {$CPU_WARN_THRESHOLD}
│   └── ...
│
├── 📁 Приложения (19)
│   ├── Dell OME - Authentication
│   ├── Dell OME - Discovery
│   ├── Dell OME - Status
│   ├── Dell OME - Power
│   ├── Dell OME - Temperature
│   ├── Dell OME - Health
│   ├── Dell OME - Alerts
│   ├── Dell OME - Inventory (NEW)
│   ├── Dell OME - CPU (NEW)
│   ├── Dell OME - Memory (NEW)
│   ├── Dell OME - Storage (NEW)
│   ├── Dell OME - RAID (NEW)
│   ├── Dell OME - Network (NEW)
│   ├── Dell OME - Fans (NEW)
│   ├── Dell OME - Power Supplies (NEW)
│   ├── Dell OME - GPU (NEW)
│   ├── Dell OME - Utilization (NEW)
│   ├── Dell OME - Chassis (NEW)
│   └── Dell OME - System (NEW)
│
├── 🔍 Discovery Rules (3)
│   ├── Device Discovery (существующий)
│   ├── Inventory Discovery (NEW)
│   └── Metrics Discovery (NEW)
│
└── 📈 Dashboards (5)
    ├── Overview Dashboard
    ├── Power & Energy Dashboard
    ├── Temperature & Fans Dashboard
    ├── Storage & RAID Dashboard
    └── Alerts Dashboard
```

### 2. Подход к реализации

#### Вариант A: Единый шаблон
- Все метрики в одном шаблоне
- Простое развёртывание
- Может быть большим (>2000 строк)

#### Вариант B: Модульные шаблоны
- Базовый шаблон (существующие 8 метрик)
- Дополнительные шаблоны:
  - `template_dell_ome_inventory.xml`
  - `template_dell_ome_power.xml`
  - `template_dell_ome_storage.xml`
  - `template_dell_ome_network.xml`

**Рекомендация:** Вариант A с опциональными макросами для включения/выключения групп метрик.

### 3. Оптимизация производительности

| Проблема | Решение |
| :--- | :--- |
| Много HTTP запросов | Группировка через POST /api/MetricService/Metrics |
| Частые запросы инвентаризации | Увеличить интервал (1h-24h) |
| Большой размер ответов | JSONPath фильтрация |
| Таймауты | Увеличить {$OME_TIMEOUT} до 60s |

### 4. Value Maps

Добавить новые карты значений:
- Dell OME - Health Status (существует)
- Dell OME - Device Status (существует)
- Dell OME - Power State (существует)
- Dell OME - Connection State (существует)
- Dell OME - Session Status (существует)
- **Dell OME - PSU Status** (NEW)
- **Dell OME - Fan Status** (NEW)
- **Dell OME - Disk Status** (NEW)
- **Dell OME - RAID Status** (NEW)
- **Dell OME - NIC Status** (NEW)
- **Dell OME - Alert Severity** (NEW)

---

## ЗАКЛЮЧЕНИЕ

### Итоговые цифры

| Категория | Количество |
| :--- | :--- |
| **Новых метрик** | 47+ |
| **Новых приложений** | 12 |
| **Новых API endpoints** | 35+ |
| **Новых Value Maps** | 5 |
| **Новых макросов** | 8+ |

### Ожидаемые преимущества

✅ **Полный мониторинг оборудования** — все компоненты сервера  
✅ **Предсказание отказов** — раннее обнаружение проблем  
✅ **Энергоэффективность** — контроль потребления  
✅ **Планирование ресурсов** — данные для апгрейда  
✅ **Соответствие SLA** — детальный мониторинг доступности  

### Следующие шаги

1. **Приоритизация** — выбрать метрики Phase 1
2. **Прототип** — создать тестовый шаблон
3. **Тестирование** — проверить на реальной инфраструктуре
4. **Документация** — обновить README.md
5. **Релиз** — опубликовать v2.0

---

**Анализ проведён:** 31 марта 2026 г.  
**Версия отчёта:** 2.0  
**Статус:** ✅ Готово к внедрению
