# Dell OpenManage Enterprise Zabbix Template 7.0 v2.0

[![Zabbix](https://img.shields.io/badge/Zabbix-7.0-green.svg)](https://www.zabbix.com/)
[![Dell OME](https://img.shields.io/badge/Dell%20OME-3.x%2B-blue.svg)](https://www.dell.com/openmanage)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)](https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise/releases/tag/v2.0)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Comprehensive** template for Dell OME API monitoring with inventory, power metrics, utilization, and hardware health tracking.

---

## 📋 Содержание

- [Что нового в v2.0](#-что-нового-в-v20)
- [Сравнение версий](#-сравнение-версий)
- [Быстрый старт](#-быстрый-старт)
- [Макросы](#-макросы)
- [Приложения](#-приложения)
- [Метрики](#-метрики)
- [Триггеры](#-триггеры)
- [API Endpoints](#-api-endpoints)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Что нового в v2.0

### 🆕 Новые возможности

| Категория | Метрики | Описание |
| :--- | :--- | :--- |
| **🖥️ Инвентаризация** | CPU/Memory/Disk/RAID/PSU/NIC | Автоматическое обнаружение компонентов |
| **⚡ Энергопотребление** | Instant/Avg/Max/Min Power | Мониторинг потребления энергии |
| **📊 Утилизация** | CPU/Memory/IO | Загрузка ресурсов |
| **🔔 Алерты** | Critical Alerts Count | Подсчёт критических событий |
| **🌡️ Температура** | Enhanced | Расширенный мониторинг температуры |
| **💚 Здоровье** | SubSystem Health | Мониторинг здоровья систем |

### 📈 Новые макросы

| Макрос | Значение по умолчанию | Описание |
| :--- | :--- | :--- |
| `{$POWER_WARN_THRESHOLD}` | 80 | Порог предупреждения по питанию (%) |
| `{$POWER_CRIT_THRESHOLD}` | 95 | Порог критического по питанию (%) |
| `{$DISK_WARN_THRESHOLD}` | 80 | Порог предупреждения по диску (%) |
| `{$DISK_CRIT_THRESHOLD}` | 90 | Порог критического по диску (%) |
| `{$CPU_WARN_THRESHOLD}` | 80 | Порог предупреждения по CPU (%) |
| `{$CPU_CRIT_THRESHOLD}` | 95 | Порог критического по CPU (%) |
| `{$MEMORY_WARN_THRESHOLD}` | 80 | Порог предупреждения по памяти (%) |
| `{$MEMORY_CRIT_THRESHOLD}` | 95 | Порог критического по памяти (%) |
| `{$INVENTORY_UPDATE_INTERVAL}` | 1h | Интервал обновления инвентаризации |
| `{$METRICS_UPDATE_INTERVAL}` | 2m | Интервал обновления метрик |
| `{$ALERTS_UPDATE_INTERVAL}` | 1m | Интервал обновления алертов |

### 🗺️ Новые Value Maps

- Dell OME - PSU Status
- Dell OME - Fan Status
- Dell OME - Disk Status
- Dell OME - RAID Status
- Dell OME - Alert Severity

---

## 📊 Сравнение версий

| Функция | v1.1 | v2.0 |
| :--- | :---: | :---: |
| **Базовый мониторинг** | ✅ | ✅ |
| **Статус/Питание/Температура** | ✅ | ✅ |
| **Здоровье системы** | ✅ | ✅ |
| **Инвентаризация (CPU)** | ❌ | ✅ |
| **Инвентаризация (Memory)** | ❌ | ✅ |
| **Инвентаризация (Disk/RAID)** | ❌ | ✅ |
| **Инвентаризация (PSU)** | ❌ | ✅ |
| **Инвентаризация (NIC)** | ❌ | ✅ |
| **Метрики питания** | ❌ | ✅ |
| **Утилизация (CPU/Memory/IO)** | ❌ | ✅ |
| **Мониторинг алертов** | ❌ | ✅ |
| **Групповые запросы** | ❌ | ✅ |
| **Приложений** | 7 | 19 |
| **Item Prototypes** | 8 | 26 |
| **Trigger Prototypes** | 8 | 9 |
| **Value Maps** | 5 | 10 |
| **Макросов** | 7 | 18 |

---

## 🚀 Быстрый старт

### Вариант 1: Git Clone

```bash
git clone https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise.git
cd zabbix-template-api-dell-openmanage-enterprise
```

### Вариант 2: Ручная загрузка

1. Скачайте `template_dell_ome_2.0.xml` из [releases v2.0](https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise/releases/tag/v2.0)
2. Импортируйте в Zabbix

### Импорт в Zabbix

1. Войдите в Zabbix как администратор
2. Перейдите: **Data collection → Templates**
3. Нажмите **Import**
4. Выберите файл:
   - `template_dell_ome_1.1.xml` — базовая версия (v1.1)
   - `template_dell_ome_1.1_db.xml` — с dashboard (v1.1)
   - `template_dell_ome_2.0.xml` — **полная версия (v2.0)** ⭐
5. Нажмите **Import**

### Настройка хоста

1. Перейдите: **Data collection → Hosts**
2. Нажмите **Create host**
3. Заполните:
   - **Host name**: Dell OME Server
   - **Visible name**: Dell OpenManage Enterprise
   - **Groups**: Servers / Monitoring
4. Вкладка **Templates**: добавьте `Dell OpenManage Enterprise by HTTP agent`
5. Вкладка **Macros**: настройте макросы

### Настройка макросов

| Макрос | Значение | Обязательно |
| :--- | :--- | :--- |
| `{$OME_HOST}` | `https://192.168.1.100` | ✅ |
| `{$OME_USER}` | `admin` | ✅ |
| `{$OME_PASSWORD}` | *(ваш пароль)* | ✅ |
| `{$OME_UPDATE_INTERVAL}` | `5m` | ❌ |
| `{$OME_TIMEOUT}` | `30s` | ❌ |
| `{$TEMP_WARN_THRESHOLD}` | `65` | ❌ |
| `{$TEMP_CRIT_THRESHOLD}` | `80` | ❌ |
| `{$POWER_WARN_THRESHOLD}` | `80` | ❌ |
| `{$DISK_WARN_THRESHOLD}` | `80` | ❌ |
| `{$CPU_WARN_THRESHOLD}` | `80` | ❌ |
| `{$MEMORY_WARN_THRESHOLD}` | `80` | ❌ |
| `{$INVENTORY_UPDATE_INTERVAL}` | `1h` | ❌ |
| `{$METRICS_UPDATE_INTERVAL}` | `2m` | ❌ |

> ⚠️ **Важно:** Установите пароль в `{$OME_PASSWORD}` перед началом мониторинга!

---

## 📁 Приложения

### v2.0 (19 приложений)

| № | Приложение | Описание |
| :--- | :--- | :--- |
| 1 | Dell OME - Authentication | Аутентификация API |
| 2 | Dell OME - Discovery | Обнаружение устройств |
| 3 | Dell OME - Status | Статус устройств |
| 4 | Dell OME - Power | Состояние питания |
| 5 | Dell OME - Temperature | Температура |
| 6 | Dell OME - Health | Здоровье компонентов |
| 7 | Dell OME - Alerts | Алерты и уведомления |
| 8 | Dell OME - Inventory | Инвентаризация |
| 9 | Dell OME - CPU | Процессоры |
| 10 | Dell OME - Memory | Память |
| 11 | Dell OME - Storage | Диски и хранилище |
| 12 | Dell OME - RAID | RAID контроллеры |
| 13 | Dell OME - Power Supplies | Блоки питания |
| 14 | Dell OME - Fans | Вентиляторы |
| 15 | Dell OME - Network | Сетевые интерфейсы |
| 16 | Dell OME - GPU | Графические ускорители |
| 17 | Dell OME - Utilization | Утилизация ресурсов |
| 18 | Dell OME - Chassis | Шасси |
| 19 | Dell OME - System | Системная информация |

---

## 📊 Метрики

### Базовые (v1.1)

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.status]` | UINT | - | Статус (1000/1001/1002) |
| `ome.device[{#Id}.power]` | UINT | - | Питание (17/18/19) |
| `ome.device[{#Id}.model]` | TEXT | - | Модель устройства |
| `ome.device[{#Id}.tag]` | TEXT | - | Service Tag |
| `ome.device[{#Id}.identifier]` | TEXT | - | Identifier |
| `ome.device[{#Id}.connection]` | UINT | - | Подключение (0/1) |
| `ome.device[{#Id}.temperature]` | UINT | °C | Температура |
| `ome.device[{#Id}.health]` | UINT | - | Здоровье (0-3) |

### Новые (v2.0)

#### CPU

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.cpu.count]` | UINT | шт | Количество процессоров |
| `ome.device[{#Id}.cpu.cores]` | UINT | шт | Общее количество ядер |
| `ome.device[{#Id}.cpu.model]` | TEXT | - | Модель процессора |
| `ome.device[{#Id}.cpu.maxspeed]` | UINT | MHz | Максимальная частота |

#### Memory

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.memory.total]` | UINT | MB | Общий объём памяти |
| `ome.device[{#Id}.memory.count]` | UINT | шт | Количество модулей |

#### Storage

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.disk.count]` | UINT | шт | Количество дисков |
| `ome.device[{#Id}.disk.totalsize]` | UINT | GB | Общий объём дисков |

#### RAID

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.raid.count]` | UINT | шт | Количество RAID контроллеров |
| `ome.device[{#Id}.raid.model]` | TEXT | - | Модель RAID контроллера |

#### Power Supplies

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.psu.count]` | UINT | шт | Количество БП |
| `ome.device[{#Id}.psu.wattage]` | UINT | W | Общая мощность БП |

#### Network

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.nic.count]` | UINT | шт | Количество сетевых интерфейсов |

#### System

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.uptime]` | UINT | s | Время работы системы |
| `ome.metrics.grouped` | TEXT | - | Групповые метрики (Power/Utilization) |
| `ome.alerts.critical` | UINT | шт | Количество критических алертов |

---

## 🔔 Триггеры

### DISASTER

| Имя | Выражение | Описание |
| :--- | :--- | :--- |
| **CRITICAL FAILURE** | `status=1002 AND connection=0` | Устройство в критическом состоянии и потеряно соединение |

### HIGH

| Имя | Выражение | Описание |
| :--- | :--- | :--- |
| **Critical Status** | `status=1002` | Критический статус устройства |
| **Not Connected** | `connection=0` | Устройство не подключено |
| **Temperature Critical** | `temp>{$TEMP_CRIT_THRESHOLD}` | Температура > 80°C |
| **Health Check Failed** | `health!=1` | Здоровье не Normal |
| **Session Invalid** | `strlen(session)=0` | Сессия API истекла |

### AVERAGE

| Имя | Выражение | Описание |
| :--- | :--- | :--- |
| **Warning Status** | `status=1001` | Предупреждение устройства |
| **Power Off** | `power=18` | Устройство выключено |
| **Temperature Warning** | `temp>{$TEMP_WARN_THRESHOLD}` | Температура > 65°C |

---

## 📡 API Endpoints

### Основные

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/SessionService/Sessions` | POST | Аутентификация |
| `/api/DeviceService/Devices` | GET | Список устройств |
| `/api/DeviceService/Devices({Id})` | GET | Данные устройства |

### Инвентаризация

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/DeviceService/Devices({Id})/InventoryDetails` | GET | Все детали |
| `/api/DeviceService/Devices({Id})/InventoryDetails('serverProcessors')` | GET | Процессоры |
| `/api/DeviceService/Devices({Id})/InventoryDetails('serverMemoryDevices')` | GET | Память |
| `/api/DeviceService/Devices({Id})/InventoryDetails('serverArrayDisks')` | GET | Диски |
| `/api/DeviceService/Devices({Id})/InventoryDetails('serverRaidControllers')` | GET | RAID |
| `/api/DeviceService/Devices({Id})/InventoryDetails('serverPowerSupplies')` | GET | Блоки питания |
| `/api/DeviceService/Devices({Id})/InventoryDetails('serverNetworkInterfaces')` | GET | Сеть |

### Метрики

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/MetricService/Metrics` | POST | Групповые метрики |
| `/api/MetricService/MetricTypes` | GET | Типы метрик |
| `/api/MetricService/EnergyConsumption` | POST | Энергопотребление |

### Температура и здоровье

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/DeviceService/Devices({Id})/Temperature` | GET | Температура |
| `/api/DeviceService/Devices({Id})/SubSystemHealth` | GET | Здоровье |

### Алерты

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/AlertService/Alerts` | GET | Все алерты |
| `/api/AlertService/Alerts?$filter=SeverityType eq 'Critical'` | GET | Критические |

---

## 🔧 Troubleshooting

### Нет данных с устройств

**Причина:** Не настроена аутентификация

**Решение:**
```text
1. Проверьте макросы {$OME_USER} и {$OME_PASSWORD}
2. Проверьте item "OME: Session Authentication"
3. Убедитесь, что SessionId сохраняется
```

### Ошибка таймаута

**Причина:** Долгий ответ от OME API

**Решение:**
```text
1. Увеличьте {$OME_TIMEOUT} до 60s
2. Проверьте сетевое подключение
3. Увеличьте {$INVENTORY_UPDATE_INTERVAL} до 2h
```

### Устройства не обнаруживаются

**Причина:** Неправильный URL или нет прав

**Решение:**
```text
1. Проверьте {$OME_HOST} (должен быть https://)
2. Убедитесь в правах учетной записи
3. Проверьте API через браузер
```

### Частые разрывы сессии

**Решение:**
```text
1. Уменьшите {$OME_UPDATE_INTERVAL} до 2m
2. Session обновляется каждые 1 минуту автоматически
```

### Нет данных инвентаризации

**Причина:** Неправильный InventoryType

**Решение:**
```text
1. Проверьте URL InventoryDetails
2. Убедитесь, что тип инвентаризации поддерживается
3. Проверьте логи Zabbix
```

---

## 📁 Структура репозитория

```text
zabbix-template-api-dell-openmanage-enterprise/
├── template_dell_ome_1.1.xml         # Шаблон v1.1 (без dashboard)
├── template_dell_ome_1.1_db.xml      # Шаблон v1.1 (с dashboard)
├── template_dell_ome_2.0.xml         # Шаблон v2.0 (полная версия) ⭐
├── generate_template_v2_full.py      # Генератор шаблона v2.0
├── README.md                         # Основная документация
├── README_V2.md                      # Документация v2.0 (этот файл)
├── DASHBOARDS.md                     # Отдельные dashboards
├── TEMPLATE_DASHBOARDS.md            # Включение dashboard в шаблон
├── ANALYSIS_REPORT.md                # Отчёт по анализу v1.1
├── ANALYSIS_REPORT_V2.md             # Отчёт по анализу v2.0
├── LICENSE                           # Лицензия MIT
├── .gitignore                        # Git ignore file
└── dell-openmanage-enterprise_...pdf # Документация Dell OME
```

---

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

---

## 🏷️ Версии

| Версия | Дата | Описание |
| :--- | :--- | :--- |
| **v2.0** | 2026-03-31 | Полная версия с инвентаризацией, метриками питания, утилизацией |
| **v1.1** | 2026-03-31 | Расширенная версия с температурой, здоровьем, сессией |
| **v1.0** | 2026-03-30 | Базовая версия |

---

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи Zabbix Server
2. Проверьте item `OME: Session Authentication`
3. Убедитесь, что Dell OME API доступен через браузер
4. Проверьте макросы `{$OME_USER}` и `{$OME_PASSWORD}`
5. Откройте issue на GitHub

---

**Совместимость:** Zabbix 7.0+  
**Версия шаблона:** 2.0 (Full)  
**Последнее обновление:** 2026-03-31  
**Dashboard:** Включён в template_dell_ome_1.1_db.xml (v1.1)  
**GitHub:** https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise
