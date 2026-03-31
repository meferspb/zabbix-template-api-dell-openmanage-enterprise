# Dell OpenManage Enterprise Zabbix Template 7.0

[![Zabbix](https://img.shields.io/badge/Zabbix-7.0-green.svg)](https://www.zabbix.com/)
[![Dell OME](https://img.shields.io/badge/Dell%20OME-3.x%2B-blue.svg)](https://www.dell.com/openmanage)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-meferspb-black?logo=github)](https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise)

Шаблон для мониторинга устройств Dell через **Dell OpenManage Enterprise (OME)** REST API в Zabbix 7.0.

---

## 📋 Содержание

- [Возможности](#-возможности)
- [Требования](#-требования)
- [Установка](#-установка)
- [Настройка](#️-настройка)
- [Компоненты](#-компоненты-шаблона)
- [Алерты](#-алерты)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Лицензия](#-лицензия)

---

## ✨ Возможности

### Мониторинг

- ✅ **Автоматическое обнаружение устройств** (LLD)
- ✅ **Статус устройств** (Normal/Warning/Critical)
- ✅ **Состояние питания** (Power On/Off/Unknown)
- ✅ **Температура компонентов** с порогами Warning/Critical
- ✅ **Здоровье системы** (SubSystem Health)
- ✅ **Состояние подключения** к OME

### Алерты

| Приоритет | Триггер | Описание |
| :--- | :--- | :--- |
| 🔴 **DISASTER** | CRITICAL FAILURE | Статус Critical + потеря связи |
| 🟥 **HIGH** | Critical Status | Статус устройства Critical |
| 🟥 **HIGH** | Not Connected | Устройство не подключено |
| 🟥 **HIGH** | Temperature Critical | Температура > 80°C |
| 🟥 **HIGH** | Health Check Failed | Здоровье не Normal |
| 🟥 **HIGH** | Session Invalid | Сессия API недействительна |
| 🟡 **AVERAGE** | Warning Status | Статус устройства Warning |
| 🟡 **AVERAGE** | Power Off | Устройство выключено |
| 🟡 **AVERAGE** | Temperature Warning | Температура > 65°C |

### Поддерживаемые устройства

- Серверы **Dell PowerEdge** (все модели)
- Шасси **Dell Chassis**
- Сетевые устройства **Dell Networking**
- Системы хранения **Dell Storage**

---

## 📋 Требования

| Компонент | Версия |
| :--- | :--- |
| **Zabbix** | 7.0 или новее |
| **Dell OME** | 3.x или новее |
| **Python** (опционально) | 3.7+ |

---

## 🚀 Установка

### Вариант 1: Git Clone (рекомендуется)

```bash
# Клонируйте репозиторий
git clone https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise.git

# Перейдите в директорию
cd zabbix-template-api-dell-openmanage-enterprise
```

### Вариант 2: Ручная загрузка

1. Скачайте `template_dell_ome_1.1.xml` (без dashboard) или `template_dell_ome_1.1_db.xml` (с dashboard)
2. Импортируйте в Zabbix

### Импорт в Zabbix

1. Войдите в Zabbix как администратор
2. Перейдите: **Data collection → Templates**
3. Нажмите **Import**
4. Выберите файл:
   - `template_dell_ome_1.1.xml` — шаблон без dashboard
   - `template_dell_ome_1.1_db.xml` — шаблон с dashboard
5. Нажмите **Import**

---

## ⚙️ Настройка

### 1. Создайте хост

1. Перейдите: **Data collection → Hosts**
2. Нажмите **Create host**
3. Заполните:
   - **Host name**: Dell OME Server
   - **Visible name**: Dell OpenManage Enterprise
   - **Groups**: Servers / Monitoring
4. Вкладка **Templates**: добавьте `Dell OpenManage Enterprise by HTTP agent`
5. Вкладка **Macros**: настройте макросы

### 2. Настройте макросы

| Макрос | Значение | Описание | Обязательно |
| :--- | :--- | :--- | :--- |
| `{$OME_HOST}` | `https://192.168.1.100` | URL Dell OME API | ✅ |
| `{$OME_USER}` | `admin` | Имя пользователя | ✅ |
| `{$OME_PASSWORD}` | *(пусто)* | Пароль | ✅ |
| `{$OME_UPDATE_INTERVAL}` | `5m` | Интервал обнаружения | ❌ |
| `{$OME_TIMEOUT}` | `30s` | Таймаут запроса | ❌ |
| `{$TEMP_WARN_THRESHOLD}` | `65` | Температура Warning (°C) | ❌ |
| `{$TEMP_CRIT_THRESHOLD}` | `80` | Температура Critical (°C) | ❌ |

> ⚠️ **Важно:** Установите пароль в `{$OME_PASSWORD}` перед началом мониторинга!

---

## 📊 Компоненты шаблона

### Приложения

| Название | Описание |
| :--- | :--- |
| Dell OME - Authentication | Аутентификация API |
| Dell OME - Discovery | Обнаружение устройств |
| Dell OME - Status | Статус устройств |
| Dell OME - Power | Состояние питания |
| Dell OME - Temperature | Температура |
| Dell OME - Health | Здоровье компонентов |
| Dell OME - Alerts | Алерты и уведомления |

---

### Элементы данных (на устройство)

| Ключ | Тип | Описание |
| :--- | :--- | :--- |
| `ome.device[{#Id}.status]` | UINT | Статус (1000/1001/1002) |
| `ome.device[{#Id}.power]` | UINT | Питание (17/18/19) |
| `ome.device[{#Id}.model]` | TEXT | Модель устройства |
| `ome.device[{#Id}.tag]` | TEXT | Service Tag |
| `ome.device[{#Id}.identifier]` | TEXT | Identifier |
| `ome.device[{#Id}.connection]` | UINT | Подключение (0/1) |
| `ome.device[{#Id}.temperature]` | UINT | Температура (°C) |
| `ome.device[{#Id}.health]` | UINT | Здоровье (0-3) |

---

## 🔔 Алерты

### DISASTER

#### CRITICAL FAILURE: {#DeviceName}

- **Выражение:** `last(status)=1002 AND last(connection)=0`
- **Описание:** Устройство в критическом состоянии и потеряно соединение

### HIGH

| Триггер | Выражение | Описание |
| :--- | :--- | :--- |
| Critical Status | `last(status)=1002` | Критический статус устройства |
| Not Connected | `last(connection)=0` | Устройство не подключено |
| Temperature Critical | `last(temp)>{$TEMP_CRIT_THRESHOLD}` | Температура > 80°C |
| Health Check Failed | `last(health)!=1` | Здоровье не Normal |
| Session Invalid | `strlen(session)=0` | Сессия API истекла |

---

### AVERAGE

| Триггер | Выражение | Описание |
| :--- | :--- | :--- |
| Warning Status | `last(status)=1001` | Предупреждение устройства |
| Power Off | `last(power)=18` | Устройство выключено |
| Temperature Warning | `last(temp)>{$TEMP_WARN_THRESHOLD}` | Температура > 65°C |

---

## 📡 API Reference

### Endpoints

| Endpoint | Метод | Описание |
| :--- | :--- | :--- |
| `/api/SessionService/Sessions` | POST | Аутентификация |
| `/api/DeviceService/Devices` | GET | Список устройств |
| `/api/DeviceService/Devices(id)` | GET | Данные устройства |
| `/api/DeviceService/Devices(id)/Temperature` | GET | Температура |
| `/api/DeviceService/Devices(id)/SubSystemHealth` | GET | Здоровье |

---

### Коды статусов

| Код | Значение |
| :--- | :--- |
| 1000 | Normal |
| 1001 | Warning |
| 1002 | Critical |

---

### Коды питания

| Код | Значение |
| :--- | :--- |
| 17 | Power On |
| 18 | Power Off |
| 19 | Unknown |

---

### Коды здоровья

| Код | Значение |
| :--- | :--- |
| 0 | Unknown |
| 1 | Normal |
| 2 | Warning |
| 3 | Critical |

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
2. Session обновляется каждые 5 минут автоматически
```

---

## 📁 Структура репозитория

```text
zabbix-template-api-dell-openmanage-enterprise/
├── template_dell_ome_1.1.xml         # Шаблон без dashboard
├── template_dell_ome_1.1_db.xml      # Шаблон с dashboard (рекомендуется)
├── README.md                         # Документация (этот файл)
├── DASHBOARDS.md                     # Отдельные dashboards
├── TEMPLATE_DASHBOARDS.md            # Включение dashboard в шаблон
├── ANALYSIS_REPORT.md                # Отчёт об анализе
├── LICENSE                           # Лицензия MIT
├── .gitignore                        # Git ignore file
└── dell-openmanage-enterprise_...pdf # Документация Dell OME
```

---

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

---

## 👥 Авторы

- **Qwen Code Assistant** - Initial work
- **GitHub**: [@meferspb](https://github.com/meferspb/zabbix-template-api-dell-openmanage-enterprise)

---

## ⭐ GitHub

Если этот шаблон был вам полезен, поставьте ⭐ **Star** на GitHub!

---

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи Zabbix Server
2. Проверьте item `OME: Session Authentication`
3. Убедитесь, что Dell OME API доступен

---

**Совместимость:** Zabbix 7.0+  
**Версия шаблона:** 1.1 (Enhanced)  
**Последнее обновление:** 2026-03-31  
**Dashboard:** Включён в template_dell_ome_1.1_db.xml
