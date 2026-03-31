# QWEN CONTEXT - Dell OME Zabbix Template

**Проект:** Zabbix Template для Dell OpenManage Enterprise  
**Версия:** 2.0 FIXED  
**Дата:** 31 марта 2026 г.  
**Zabbix:** 7.0+  
**Dell OME:** 3.x+

---

## 📁 СТРУКТУРА ПРОЕКТА

```
zabbix-template-api-dell-openmanage-enterprise/
├── template_dell_ome_1.1.xml         # Базовая версия v1.1 (19.8 KB)
├── template_dell_ome_1.1_db.xml      # v1.1 с dashboard (24.8 KB)
├── template_dell_ome_2.0.xml         # Полная версия v2.0 FIXED (42.5 KB) ⭐
├── README.md                         # Основная документация
├── README_V2.md                      # Документация v2.0
├── RELEASE_NOTES_V2.md               # Release notes для GitHub
├── LICENSE                           # MIT License
└── .gitignore
```

---

## 🎯 ОСНОВНЫЕ ФАЙЛЫ

### Шаблоны Zabbix

| Файл | Версия | Описание | Статус |
| :--- | :--- | :--- | :--- |
| `template_dell_ome_2.0.xml` | 2.0 FIXED | Полная версия со всеми метриками | ✅ Основной |
| `template_dell_ome_1.1.xml` | 1.1 | Базовая версия | ✅ Рабочий |
| `template_dell_ome_1.1_db.xml` | 1.1 | Версия с dashboard | ✅ Рабочий |

### Документация

| Файл | Описание |
| :--- | :--- |
| `README_V2.md` | Основная документация v2.0 |
| `README.md` | Базовая документация |
| `RELEASE_NOTES_V2.md` | Release notes для GitHub |
| `LICENSE` | MIT License |

---

## 📊 СТАТИСТИКА ШАБЛОНА v2.0

```
Макросы:            18
Приложения:         19
Items:              3 (глобальные)
Discovery Rules:    1
Item Prototypes:    22
Trigger Prototypes: 9
Graph Prototypes:   3
Value Maps:         10
```

---

## 🔧 МАКРОСЫ

### Обязательные

| Макрос | Значение по умолчанию | Описание |
| :--- | :--- | :--- |
| `{$OME_HOST}` | `https://192.168.1.100` | URL Dell OME API |
| `{$OME_USER}` | `admin` | Имя пользователя |
| `{$OME_PASSWORD}` | *(пусто)* | Пароль (настроить!) |

### Опциональные

| Макрос | Значение | Описание |
| :--- | :--- | :--- |
| `{$OME_UPDATE_INTERVAL}` | `5m` | Интервал обнаружения |
| `{$OME_TIMEOUT}` | `30s` | Таймаут запроса |
| `{$TEMP_WARN_THRESHOLD}` | `65` | Температура Warning (°C) |
| `{$TEMP_CRIT_THRESHOLD}` | `80` | Температура Critical (°C) |
| `{$POWER_WARN_THRESHOLD}` | `80` | Питание Warning (%) |
| `{$POWER_CRIT_THRESHOLD}` | `95` | Питание Critical (%) |
| `{$DISK_WARN_THRESHOLD}` | `80` | Диск Warning (%) |
| `{$DISK_CRIT_THRESHOLD}` | `90` | Диск Critical (%) |
| `{$CPU_WARN_THRESHOLD}` | `80` | CPU Warning (%) |
| `{$CPU_CRIT_THRESHOLD}` | `95` | CPU Critical (%) |
| `{$MEMORY_WARN_THRESHOLD}` | `80` | Память Warning (%) |
| `{$MEMORY_CRIT_THRESHOLD}` | `95` | Память Critical (%) |
| `{$INVENTORY_UPDATE_INTERVAL}` | `1h` | Интервал инвентаризации |
| `{$METRICS_UPDATE_INTERVAL}` | `2m` | Интервал метрик |
| `{$ALERTS_UPDATE_INTERVAL}` | `1m` | Интервал алертов |

---

## 📡 API ENDPOINTS

### Основные

```
POST /api/SessionService/Sessions          # Аутентификация
GET  /api/DeviceService/Devices            # Список устройств
GET  /api/DeviceService/Devices({Id})      # Данные устройства
```

### Инвентаризация

```
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverProcessors')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverMemoryDevices')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverArrayDisks')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverRaidControllers')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverPowerSupplies')
GET /api/DeviceService/Devices({Id})/InventoryDetails('serverNetworkInterfaces')
```

### Метрики и мониторинг

```
GET  /api/DeviceService/Devices({Id})/Temperature
GET  /api/DeviceService/Devices({Id})/SubSystemHealth
GET  /api/AlertService/Alerts
```

---

## 🔑 КОДЫ СТАТУСОВ

### Device Status

| Код | Значение |
| :--- | :--- |
| 1000 | Normal |
| 1001 | Warning |
| 1002 | Critical |

### Power State

| Код | Значение |
| :--- | :--- |
| 17 | Power On |
| 18 | Power Off |
| 19 | Unknown |

### Health Status

| Код | Значение |
| :--- | :--- |
| 0 | Unknown |
| 1 | Normal |
| 2 | Warning |
| 3 | Critical |

---

## 🚀 БЫСТРЫЙ СТАРТ

### 1. Импорт в Zabbix

```
Data collection → Templates → Import → template_dell_ome_2.0.xml
```

### 2. Настройка хоста

```
1. Data collection → Hosts → Create host
2. Host name: Dell OME Server
3. Templates: Dell OpenManage Enterprise by HTTP agent
4. Macros: настроить {$OME_HOST}, {$OME_USER}, {$OME_PASSWORD}
```

### 3. Проверка

```
1. Проверить item "OME: Session Authentication"
2. Дождаться Discovery (5m)
3. Проверить появление устройств
```

---

## 📂 ПРИЛОЖЕНИЯ ШАБЛОНА

```
1.  Dell OME - Authentication      # Аутентификация API
2.  Dell OME - Discovery           # Обнаружение устройств
3.  Dell OME - Status              # Статус устройств
4.  Dell OME - Power               # Состояние питания
5.  Dell OME - Temperature         # Температура
6.  Dell OME - Health              # Здоровье компонентов
7.  Dell OME - Alerts              # Алерты
8.  Dell OME - Inventory           # Инвентаризация
9.  Dell OME - CPU                 # Процессоры
10. Dell OME - Memory              # Память
11. Dell OME - Storage             # Диски
12. Dell OME - RAID                # RAID контроллеры
13. Dell OME - Power Supplies      # Блоки питания
14. Dell OME - Fans                # Вентиляторы
15. Dell OME - Network             # Сеть
16. Dell OME - GPU                 # Графические ускорители
17. Dell OME - Utilization         # Утилизация
18. Dell OME - Chassis             # Шасси
19. Dell OME - System              # Система
```

---

## 🔔 ТРИГГЕРЫ

### DISASTER (1)

- **CRITICAL FAILURE** — `status=1002 AND connection=0`

### HIGH (5)

- **Critical Status** — `status=1002`
- **Not Connected** — `connection=0`
- **Temperature Critical** — `temp>{$TEMP_CRIT_THRESHOLD}`
- **Health Check Failed** — `health!=1`
- **Session Invalid** — `strlen(session)=0`

### AVERAGE (3)

- **Warning Status** — `status=1001`
- **Power Off** — `power=18`
- **Temperature Warning** — `temp>{$TEMP_WARN_THRESHOLD}`

---

## 🏷️ GIT TAGS

```
v1.1    — Версия 1.1 (базовая)
v2.0    — Версия 2.0 FIXED ⭐
```

---

## 📝 ИСТОРИЯ ВЕРСИЙ

### v2.0 FIXED (текущая)

**Исправления:**
- ✅ Неверный тип preprocessing `'°C'` → перемещено в `<units>`
- ✅ Неверный тип preprocessing `'MHz'` → перемещено в `<units>`
- ✅ Неверный тип preprocessing `'s'` → перемещено в `<units>`
- ✅ Item `ome.metrics.grouped` (использовал `{#Id}` вне LLD) → удалён
- ✅ regex preprocessing без параметров → исправлено

**Новые возможности:**
- Мониторинг инвентаризации (CPU, Memory, Disk, RAID, PSU, NIC)
- 11 новых макросов для пороговых значений
- 5 новых value maps
- Расширенный мониторинг алертов

### v1.1

- Мониторинг температуры
- Мониторинг здоровья (SubSystem Health)
- Session authentication
- DISASTER триггер (Critical + Not Connected)

---

## 🐛 TROUBLESHOOTING

### Нет данных с устройств

```
1. Проверить макросы {$OME_USER} и {$OME_PASSWORD}
2. Проверить item "OME: Session Authentication"
3. Убедиться, что SessionId сохраняется
```

### Ошибка таймаута

```
1. Увеличить {$OME_TIMEOUT} до 60s
2. Проверить сетевое подключение
```

### Устройства не обнаруживаются

```
1. Проверить {$OME_HOST} (должен быть https://)
2. Убедиться в правах учетной записи
3. Проверить API через браузер
```

---

## 📞 ПОДДЕРЖКА

**GitHub:** https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise  
**Лицензия:** MIT

---

**Последнее обновление:** 31 марта 2026 г.  
**Статус:** ✅ Готов к продакшену
