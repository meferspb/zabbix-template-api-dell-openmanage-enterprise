# 📦 Dell OME Zabbix Template v2.0 - Release Notes

**Дата релиза:** 31 марта 2026 г.  
**Версия:** 2.0 (FIXED)  
**Статус:** ✅ Готов к продакшену

---

## 🎯 Обзор релиза

Шаблон **Dell OpenManage Enterprise by HTTP agent v2.0** обеспечивает комплексный мониторинг устройств Dell через REST API OME в Zabbix 7.0.

### Поддерживаемые устройства

- ✅ Серверы **Dell PowerEdge** (все модели)
- ✅ Шасси **Dell Chassis** (MX7000, FX2, VRTX)
- ✅ Сетевые устройства **Dell Networking**
- ✅ Системы хранения **Dell Storage**

---

## ✨ Новые возможности v2.0

### 🆕 Мониторинг инвентаризации

| Компонент | Метрики |
| :--- | :--- |
| **CPU** | Count, Total Cores, Model, Max Speed |
| **Memory** | Total Size, Modules Count |
| **Storage** | Physical Disk Count, Total Size |
| **RAID** | Controller Count, Model |
| **PSU** | Count, Total Wattage |
| **Network** | NIC Count |
| **System** | Up Time |

### 📊 Новые макросы

| Макрос | Значение | Описание |
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

## 🔧 Исправления v2.0 FIXED

### Критические исправления

| Проблема | Статус |
| :--- | :--- |
| Неверный тип preprocessing `'°C'` в temperature | ✅ Исправлено |
| Неверный тип preprocessing `'MHz'` в cpu.maxspeed | ✅ Исправлено |
| Неверный тип preprocessing `'s'` в uptime | ✅ Исправлено |
| Item `ome.metrics.grouped` использует `{#Id}` вне LLD | ✅ Удалено |
| regex preprocessing без параметров | ✅ Исправлено |

### Изменения в структуре

- ✅ Удалён нерабочий `template_dell_ome_2.0.xml` (с ошибками)
- ✅ Переименован `template_dell_ome_2.0_fixed.xml` → `template_dell_ome_2.0.xml`
- ✅ Удалены вспомогательные скрипты генерации
- ✅ Обновлена документация

---

## 📊 Статистика шаблона

| Компонент | Количество |
| :--- | :--- |
| **Макросы** | 18 |
| **Приложения** | 19 |
| **Items** | 3 (глобальные) |
| **Discovery Rules** | 1 |
| **Item Prototypes** | 22 |
| **Trigger Prototypes** | 9 |
| **Graph Prototypes** | 3 |
| **Value Maps** | 10 |

---

## 📁 Файлы релиза

| Файл | Размер | Описание |
| :--- | :--- | :--- |
| `template_dell_ome_2.0.xml` | 42,5 KB | **Основной файл шаблона** ⭐ |
| `template_dell_ome_1.1.xml` | 19,8 KB | Базовая версия v1.1 |
| `template_dell_ome_1.1_db.xml` | 24,8 KB | Версия v1.1 с dashboard |
| `README_V2.md` | 19,0 KB | Документация v2.0 |
| `TEMPLATE_ANALYSIS_REPORT.md` | 3,0 KB | Отчёт по анализу |

---

## 🚀 Быстрый старт

### 1. Импорт в Zabbix

1. Войдите в Zabbix как администратор
2. Перейдите: **Data collection → Templates**
3. Нажмите **Import**
4. Выберите файл: `template_dell_ome_2.0.xml`
5. Нажмите **Import**

### 2. Настройка хоста

1. Перейдите: **Data collection → Hosts**
2. Нажмите **Create host**
3. Заполните:
   - **Host name**: Dell OME Server
   - **Visible name**: Dell OpenManage Enterprise
   - **Groups**: Servers / Monitoring
4. Вкладка **Templates**: добавьте `Dell OpenManage Enterprise by HTTP agent`
5. Вкладка **Macros**: настройте макросы

### 3. Настройка макросов

| Макрос | Значение | Обязательно |
| :--- | :--- | :--- |
| `{$OME_HOST}` | `https://192.168.1.100` | ✅ |
| `{$OME_USER}` | `admin` | ✅ |
| `{$OME_PASSWORD}` | *(ваш пароль)* | ✅ |
| `{$OME_UPDATE_INTERVAL}` | `5m` | ❌ |
| `{$OME_TIMEOUT}` | `30s` | ❌ |

> ⚠️ **Важно:** Установите пароль в `{$OME_PASSWORD}` перед началом мониторинга!

---

## 📈 Приложения шаблона

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

## 🔔 Триггеры

### DISASTER (1)

| Имя | Выражение | Описание |
| :--- | :--- | :--- |
| **CRITICAL FAILURE** | `status=1002 AND connection=0` | Устройство в критическом состоянии и потеряно соединение |

### HIGH (5)

| Имя | Выражение | Описание |
| :--- | :--- | :--- |
| **Critical Status** | `status=1002` | Критический статус устройства |
| **Not Connected** | `connection=0` | Устройство не подключено |
| **Temperature Critical** | `temp>{$TEMP_CRIT_THRESHOLD}` | Температура > 80°C |
| **Health Check Failed** | `health!=1` | Здоровье не Normal |
| **Session Invalid** | `strlen(session)=0` | Сессия API истекла |

### AVERAGE (3)

| Имя | Выражение | Описание |
| :--- | :--- | :--- |
| **Warning Status** | `status=1001` | Предупреждение устройства |
| **Power Off** | `power=18` | Устройство выключено |
| **Temperature Warning** | `temp>{$TEMP_WARN_THRESHOLD}` | Температура > 65°C |

---

## 🔍 API Endpoints

### Основные

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/SessionService/Sessions` | POST | Аутентификация |
| `/api/DeviceService/Devices` | GET | Список устройств |
| `/api/DeviceService/Devices({Id})` | GET | Данные устройства |

### Инвентаризация

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
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

---

## 📋 Требования

| Компонент | Версия |
| :--- | :--- |
| **Zabbix** | 7.0 или новее |
| **Dell OME** | 3.x или новее |

---

## 🐛 Известные проблемы

Отсутствуют. Все критические проблемы исправлены в версии v2.0 FIXED.

---

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи Zabbix Server
2. Проверьте item `OME: Session Authentication`
3. Убедитесь, что Dell OME API доступен через браузер
4. Проверьте макросы `{$OME_USER}` и `{$OME_PASSWORD}`
5. Откройте issue на GitHub

---

## 📄 Лицензия

MIT License

---

## 🔗 Ссылки

- **GitHub:** https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise
- **Документация:** README_V2.md
- **Отчёт по анализу:** TEMPLATE_ANALYSIS_REPORT.md

---

**Совместимость:** Zabbix 7.0+  
**Версия шаблона:** 2.0 FIXED  
**Дата релиза:** 31 марта 2026 г.  
**Статус:** ✅ Готов к продакшену
