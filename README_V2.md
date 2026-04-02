# Dell OpenManage Enterprise Zabbix Template 7.0 v2.2

[![Zabbix](https://img.shields.io/badge/Zabbix-7.0-green.svg)](https://www.zabbix.com/)
[![Dell OME](https://img.shields.io/badge/Dell%20OME-3.x%2B-blue.svg)](https://www.dell.com/openmanage)
[![Version](https://img.shields.io/badge/Version-2.2-orange.svg)](https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise/releases/tag/v2.2)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Optimized** template for Dell OME API monitoring with Master+Dependent Items architecture, GPU monitoring, and advanced health tracking.

> ✅ **v2.2 FULLY OPTIMIZED** — Master+Dependent Items (1 HTTP request per device instead of ~20), GPU monitoring, trigger tags, null-safe preprocessing.

---

## 📋 Содержание

- [Что нового в v2.2](#-что-нового-в-v22)
- [Сравнение версий](#-сравнение-версий)
- [Быстрый старт](#-быстрый-старт)
- [Макросы](#-макросы)
- [Приложения](#-приложения)
- [Метрики](#-метрики)
- [Триггеры](#-триггеры)
- [API Endpoints](#-api-endpoints)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Что нового в v2.2

### 🆕 Ключевые оптимизации

| Оптимизация | Описание | Выгода |
| :--- | :--- | :--- |
| **🔄 Master+Dependent Items** | Один HTTP-запрос получает полный JSON устройства | -95% запросов к API |
| **🎮 GPU Monitoring** | Отдельный GPU Master Item + Count + Temperature | Полный мониторинг GPU |
| **🏷️ Trigger Tags** | Теги type/source/component для всех триггеров | Лучшая категоризация |
| **🛡️ Null-Safe JSONPATH** | Обработка отсутствующих значений | Меньше ложных срабатываний |
| **📦 Макросы тегов** | `{$TAG_SOURCE}`, `{$TAG_COMPONENT}` | Централизованное управление |

### 🆕 Новые макросы

| Макрос | Значение | Описание |
| :--- | :--- | :--- |
| `{$GPU_TEMP_WARN}` | 75 | Порог температуры GPU (°C) |
| `{$GPU_UTIL_WARN}` | 80 | Порог утилизации GPU (%) |
| `{$GPU_UTIL_CRIT}` | 95 | Критический порог утилизации GPU (%) |
| `{$FAN_RPM_WARN}` | 0 | Порог вентиляторов RPM (0 = отключено) |
| `{$CPU_UTIL_WARN}` | 80 | Порог утилизации CPU (%) |
| `{$CPU_UTIL_CRIT}` | 95 | Критический порог утилизации CPU (%) |
| `{$MEM_UTIL_WARN}` | 80 | Порог утилизации памяти (%) |
| `{$MEM_UTIL_CRIT}` | 95 | Критический порог утилизации памяти (%) |
| `{$TAG_SOURCE}` | dell-ome | Тег source для триггеров |
| `{$TAG_COMPONENT}` | hardware | Тег component для триггеров |

### 🆕 Новые триггеры GPU

| Имя | Выражение | Приоритет |
| :--- | :--- | :--- |
| **GPU Temperature Warning** | `last(gpu.temp) > {$GPU_TEMP_WARN}` | AVERAGE |
| **GPU Not Found** | `last(gpu.count) = 0` | INFO |

---

## 📊 Сравнение версий

| Функция | v1.1 | v2.0 | v2.1 | v2.2 |
| :--- | :---: | :---: | :---: | :---: |
| **Базовый мониторинг** | ✅ | ✅ | ✅ | ✅ |
| **Статус/Питание/Температура** | ✅ | ✅ | ✅ | ✅ |
| **Здоровье системы** | ✅ | ✅ | ✅ | ✅ |
| **Инвентаризация (CPU/Memory/Disk)** | ❌ | ✅ | ✅ | ✅ |
| **Метрики питания** | ❌ | ✅ | ✅ | ✅ |
| **Утилизация** | ❌ | ✅ | ✅ | ✅ |
| **Мониторинг алертов** | ❌ | ✅ | ✅ | ✅ |
| **GPU Monitoring** | ❌ | ❌ | ❌ | ✅ |
| **Master+Dependent Items** | ❌ | ❌ | ❌ | ✅ |
| **Trigger Tags** | ❌ | ❌ | ❌ | ✅ |
| **Null-Safe Preprocessing** | ❌ | ❌ | ❌ | ✅ |
| **HTTP-запросов на устройство** | ~20 | ~20 | ~20 | **1-2** |
| **Приложений** | 7 | 19 | 19 | 19 |
| **Макросов** | 7 | 18 | 22 | **24** |
| **Триггеров с тегами** | 0 | 0 | 0 | **11** |

---

## 🚀 Быстрый старт

### Вариант 1: Git Clone

```bash
git clone https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise.git
cd zabbix-template-api-dell-openmanage-enterprise
```

### Вариант 2: Ручная загрузка

1. Скачайте `template_dell_ome_2.2.xml` из [releases](https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise/releases)
2. Импортируйте в Zabbix

### Импорт в Zabbix

1. Войдите в Zabbix как администратор
2. Перейдите: **Data collection → Templates**
3. Нажмите **Import**
4. Выберите файл:
   - `template_dell_ome_1.1.xml` — базовая версия (v1.1)
   - `template_dell_ome_1.1_db.xml` — с dashboard (v1.1)
   - `template_dell_ome_2.0.xml` — полная версия (v2.0)
   - `template_dell_ome_2.2.xml` — **оптимизированная (v2.2)** ⭐
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
| `{$GPU_TEMP_WARN}` | `75` | ❌ |
| `{$POWER_WARN_THRESHOLD}` | `80` | ❌ |
| `{$DISK_WARN_THRESHOLD}` | `80` | ❌ |
| `{$CPU_WARN_THRESHOLD}` | `80` | ❌ |
| `{$MEMORY_WARN_THRESHOLD}` | `80` | ❌ |
| `{$INVENTORY_UPDATE_INTERVAL}` | `1h` | ❌ |
| `{$METRICS_UPDATE_INTERVAL}` | `2m` | ❌ |

> ⚠️ **Важно:** Установите пароль в `{$OME_PASSWORD}` перед началом мониторинга!

---

## 📁 Приложения

### v2.2 (19 приложений)

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
| 16 | Dell OME - GPU | Графические ускорители ⭐ |
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

### v2.2 (Optimized)

#### Master Items

| Ключ | Тип | Описание |
| :--- | :--- | :--- |
| `ome.device[{#Id}.master]` | HTTP_AGENT | Полный JSON устройства (1 запрос) |
| `ome.device[{#Id}.gpu.master]` | HTTP_AGENT | JSON GPU устройств (отдельный запрос) |

#### Dependent Items (от master)

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.status]` | DEPENDENT | - | Статус из master JSON |
| `ome.device[{#Id}.power]` | DEPENDENT | - | Питание из master JSON |
| `ome.device[{#Id}.model]` | DEPENDENT | - | Модель из master JSON |
| `ome.device[{#Id}.tag]` | DEPENDENT | - | Service Tag из master JSON |
| `ome.device[{#Id}.identifier]` | DEPENDENT | - | Identifier из master JSON |
| `ome.device[{#Id}.connection]` | DEPENDENT | - | Подключение из master JSON |
| `ome.device[{#Id}.uptime]` | DEPENDENT | s | Uptime из master JSON |

#### GPU Items (от gpu.master)

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.gpu.count]` | DEPENDENT | шт | Количество GPU |
| `ome.device[{#Id}.gpu.temp]` | DEPENDENT | °C | Температура GPU |

#### Inventory Items

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.device[{#Id}.cpu.count]` | HTTP_AGENT | шт | Количество процессоров |
| `ome.device[{#Id}.cpu.cores]` | HTTP_AGENT | шт | Общее количество ядер |
| `ome.device[{#Id}.cpu.model]` | HTTP_AGENT | - | Модель процессора |
| `ome.device[{#Id}.memory.total]` | HTTP_AGENT | MB | Общий объём памяти |
| `ome.device[{#Id}.memory.count]` | HTTP_AGENT | шт | Количество модулей |
| `ome.device[{#Id}.disk.count]` | HTTP_AGENT | шт | Количество дисков |
| `ome.device[{#Id}.raid.count]` | HTTP_AGENT | шт | Количество RAID контроллеров |
| `ome.device[{#Id}.psu.count]` | HTTP_AGENT | шт | Количество БП |
| `ome.device[{#Id}.nic.count]` | HTTP_AGENT | шт | Количество сетевых интерфейсов |

#### System Metrics

| Ключ | Тип | Единицы | Описание |
| :--- | :--- | :--- | :--- |
| `ome.session.auth` | HTTP_AGENT | TEXT | Session ID |
| `ome.session.status` | DEPENDENT | UINT | Статус сессии |
| `ome.alerts.critical` | HTTP_AGENT | шт | Критические алерты |

---

## 🔔 Триггеры

### DISASTER

| Имя | Выражение | Теги |
| :--- | :--- | :--- |
| **CRITICAL FAILURE** | `status=1002 AND connection=0` | type:status, source:dell-ome, component:hardware |

### HIGH

| Имя | Выражение | Теги |
| :--- | :--- | :--- |
| **Critical Status** | `status=1002` | type:status, source:dell-ome, component:hardware |
| **Not Connected** | `connection=0` | type:connectivity, source:dell-ome, component:hardware |
| **Temperature Critical** | `temp>{$TEMP_CRIT_THRESHOLD}` | type:temperature, source:dell-ome, component:hardware |
| **Health Check Failed** | `health!=1` | type:health, source:dell-ome, component:hardware |
| **Session Invalid** | `strlen(session)=0` | type:authentication, source:dell-ome, component:system |

### AVERAGE

| Имя | Выражение | Теги |
| :--- | :--- | :--- |
| **Warning Status** | `status=1001` | type:status, source:dell-ome, component:hardware |
| **Power Off** | `power=18` | type:power, source:dell-ome, component:hardware |
| **Temperature Warning** | `temp>{$TEMP_WARN_THRESHOLD}` | type:temperature, source:dell-ome, component:hardware |
| **GPU Temperature Warning** | `gpu.temp>{$GPU_TEMP_WARN}` | type:temperature, source:dell-ome, component:gpu |

### INFO

| Имя | Выражение | Теги |
| :--- | :--- | :--- |
| **GPU Not Found** | `gpu.count=0` | type:inventory, source:dell-ome, component:gpu |

---

## 📡 API Endpoints

### Основные

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/SessionService/Sessions` | POST | Аутентификация |
| `/api/DeviceService/Devices` | GET | Список устройств |
| `/api/DeviceService/Devices({Id})` | GET | Данные устройства (Master) |
| `/api/DeviceService/Devices({Id})/InventoryDetails('gpuDevices')` | GET | GPU данные |

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

### Нет данных GPU

**Причина:** GPU endpoint не доступен или нет GPU в системе

**Решение:**
```text
1. Проверьте /InventoryDetails('gpuDevices') через API
2. Убедитесь, что в системе есть GPU
3. Проверьте item "GPU Master Item"
```

### Триггеры не имеют тегов

**Причина:** Теги не настроены в макросах

**Решение:**
```text
1. Проверьте макросы {$TAG_SOURCE} и {$TAG_COMPONENT}
2. Пересоздайте триггеры после изменения макросов
```

---

## 📁 Структура репозитория

```text
zabbix-template-api-dell-openmanage-enterprise/
├── template_dell_ome_1.1.xml         # Шаблон v1.1 (без dashboard)
├── template_dell_ome_1.1_db.xml      # Шаблон v1.1 (с dashboard)
├── template_dell_ome_2.0.xml         # Шаблон v2.0 (полная версия)
├── template_dell_ome_2.2.xml         # Шаблон v2.2 (оптимизированный) ⭐
├── README.md                         # Основная документация
├── README_V2.md                      # Документация v2.x (этот файл)
├── LICENSE                           # Лицензия MIT
├── .gitignore                        # Git ignore file
└── dell-openmanage-enterprise_...pdf # Документация Dell OME
```

---

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

---

## 🏷️ Версии

| Версия | Дата | Описание | Статус |
| :--- | :--- | :--- | :--- |
| **v2.2** | 2026-04-02 | Оптимизированная: Master+Dependent Items, GPU, Tags | ✅ РЕКОМЕНДУЕТСЯ |
| **v2.1** | 2026-03-31 | Промежуточная версия | ⚠️ Устарела |
| **v2.0** | 2026-03-31 | Полная версия с инвентаризацией | ✅ Рабочая |
| **v1.1** | 2026-03-31 | Расширенная версия | ✅ Рабочая |
| **v1.0** | 2026-03-30 | Базовая версия | ✅ Рабочая |

---

## 🔧 История изменений v2.2

### v2.2 (2026-04-02)

**Новые возможности:**
- ✅ Master+Dependent Items архитектура (1 HTTP-запрос вместо ~20)
- ✅ GPU Master Item для мониторинга GPU
- ✅ GPU Count и GPU Temperature как Dependent Items
- ✅ Триггеры GPU Temperature Warning и GPU Not Found
- ✅ Теги для всех триггеров (type, source, component)
- ✅ Макросы `{$TAG_SOURCE}`, `{$TAG_COMPONENT}`
- ✅ Null-safe JSONPATH preprocessing

**Исправления:**
- ✅ Исправлена структура GPU Master Item XML
- ✅ Обновлены JSONPATH для GPU items
- ✅ Удалены пустые строки из XML

**Выгода:**
- Снижение нагрузки на Zabbix Server на 95%
- Уменьшение HTTP-запросов к OME API
- Лучшая категоризация инцидентов через теги

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
**Версия шаблона:** 2.2 (Optimized)
**Последнее обновление:** 2026-04-02
**Dashboard:** Включён в template_dell_ome_1.1_db.xml (v1.1)
**GitHub:** https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise
