#!/usr/bin/env python3
"""
Dell OME Template v2.0 - Comprehensive Error Analysis
Проверка шаблона Zabbix на ошибки и потенциальные проблемы
"""

import xml.etree.ElementTree as ET
import re
import sys
from collections import defaultdict

class TemplateAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = None
        self.root = None
        self.errors = {'critical': [], 'warning': [], 'info': []}
        self.stats = defaultdict(int)
        
    def load_template(self):
        """Загрузка и парсинг XML"""
        try:
            self.tree = ET.parse(self.filepath)
            self.root = self.tree.getroot()
            print(f"✅ Файл загружен: {self.filepath}")
            return True
        except ET.ParseError as e:
            print(f"❌ XML Parse Error: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ Файл не найден: {self.filepath}")
            return False
    
    def check_xml_structure(self):
        """Проверка структуры XML"""
        print("\n" + "="*80)
        print("1️⃣ ПРОВЕРКА XML СТРУКТУРЫ")
        print("="*80)
        
        # Проверка корневого элемента
        if self.root.tag != 'zabbix_export':
            self.errors['critical'].append(f"Неверный корневой элемент: {self.root.tag}")
        else:
            print("✅ Корневой элемент: zabbix_export")
        
        # Проверка версии
        version = self.root.find('version')
        if version is None:
            self.errors['critical'].append("Отсутствует элемент <version>")
        elif version.text != '7.0':
            self.errors['warning'].append(f"Версия Zabbix: {version.text} (ожидалась 7.0)")
        else:
            print(f"✅ Версия Zabbix: {version.text}")
        
        # Проверка обязательных секций
        required_sections = ['templates', 'value_maps']
        for section in required_sections:
            if self.root.find(section) is None:
                self.errors['critical'].append(f"Отсутствует обязательная секция: {section}")
            else:
                print(f"✅ Секция {section}: найдена")
    
    def check_template_basic(self):
        """Проверка базовой информации шаблона"""
        print("\n" + "="*80)
        print("2️⃣ ПРОВЕРКА БАЗОВОЙ ИНФОРМАЦИИ")
        print("="*80)
        
        template = self.root.find('.//template')
        if template is None:
            self.errors['critical'].append("Шаблон не найден")
            return
        
        # Название шаблона
        name = template.find('name')
        if name is not None:
            print(f"✅ Название: {name.text}")
            self.stats['template_name'] = name.text
        
        # Описание
        desc = template.find('description')
        if desc is not None:
            print(f"✅ Описание: {desc.text[:100]}...")
        
        # Группы
        groups = template.findall('.//groups/group/name')
        if groups:
            print(f"✅ Группы: {[g.text for g in groups]}")
        else:
            self.errors['warning'].append("Шаблон не имеет групп")
    
    def check_macros(self):
        """Проверка макросов"""
        print("\n" + "="*80)
        print("3️⃣ ПРОВЕРКА МАКРОСОВ")
        print("="*80)
        
        macros = self.root.findall('.//macros/macro')
        self.stats['macros'] = len(macros)
        print(f"📊 Всего макросов: {len(macros)}")
        
        required_macros = ['{$OME_HOST}', '{$OME_USER}', '{$OME_PASSWORD}', '{$OME_TIMEOUT}']
        found_macros = set()
        
        for macro in macros:
            name = macro.find('macro').text
            value_elem = macro.find('value')
            value = value_elem.text if value_elem is not None else ''
            desc = macro.find('description')
            
            found_macros.add(name)
            
            # Проверка на пустые значения
            if name == '{$OME_PASSWORD}' and value:
                self.errors['warning'].append(f"Макрос ${{OME_PASSWORD}} имеет значение по умолчанию!")
            
            # Проверка формата макроса
            if not re.match(r'{\$[A-Z0-9_.]+}', name):
                self.errors['warning'].append(f"Неверный формат макроса: {name}")
            
            print(f"  {name} = {value if value else '(пусто)'}")
        
        # Проверка обязательных макросов
        for req in required_macros:
            if req not in found_macros:
                self.errors['critical'].append(f"Отсутствует обязательный макрос: {req}")
            else:
                print(f"✅ Обязательный макрос {req}: найден")
    
    def check_applications(self):
        """Проверка приложений"""
        print("\n" + "="*80)
        print("4️⃣ ПРОВЕРКА ПРИЛОЖЕНИЙ")
        print("="*80)
        
        apps = self.root.findall('.//applications/application')
        self.stats['applications'] = len(apps)
        print(f"📊 Всего приложений: {len(apps)}")
        
        app_names = set()
        for app in apps:
            name = app.find('name').text
            if name in app_names:
                self.errors['warning'].append(f"Дублирующееся приложение: {name}")
            app_names.add(name)
            print(f"  ✓ {name}")
    
    def check_items(self):
        """Проверка items"""
        print("\n" + "="*80)
        print("5️⃣ ПРОВЕРКА ITEMS")
        print("="*80)
        
        items = self.root.findall('.//items/item')
        self.stats['items'] = len(items)
        print(f"📊 Всего items: {len(items)}")
        
        valid_types = ['0', '1', '2', '3', '4', '5', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
        type_names = {
            '0': 'NUMERIC_FLOAT', '1': 'CHAR', '2': 'LOG', '3': 'NUMERIC_UNSIGNED',
            '4': 'TEXT', '5': 'NUMERIC_TEXT', '7': 'IPMI_AGENT', '8': 'DEPENDENT',
            '9': 'HTTP_AGENT', '10': 'SNMP_AGENT', '11': 'JMX', '12': 'ODBC',
            '13': 'SSH_AGENT', '14': 'TELNET', '15': 'CALCULATED', '16': 'SCRIPT',
            '17': 'HTTPSTEP', '18': 'TRAP'
        }
        
        for item in items:
            name = item.find('name').text
            key = item.find('key').text
            type_elem = item.find('type')
            item_type = type_elem.text if type_elem is not None else 'UNKNOWN'
            delay = item.find('delay').text if item.find('delay') is not None else 'N/A'
            
            # Проверка типа
            if item_type not in valid_types:
                self.errors['warning'].append(f"Item {key}: Неизвестный тип '{item_type}'")
            
            # Проверка ключа на уникальность
            print(f"  [{type_names.get(item_type, item_type)}] {key} (delay: {delay})")
            
            # Проверка preprocessing
            self._check_preprocessing(item, key)
    
    def _check_preprocessing(self, item_or_proto, key):
        """Проверка preprocessing шагов"""
        preprocessing = item_or_proto.findall('.//preprocessing/step')
        
        valid_pp_types = [
            'JSONPATH', 'REGEX', 'XPATH', 'XMLVALUE', 'CHANGE_PER_SECOND',
            'DELTA', 'MULTIPLIER', 'OFFSET', 'DECIMAL', 'HEX_DEC', 'OCT_DEC',
            'BOOL_DEC', 'BOOL_OCT', 'DISCARD_UNCHANGED', 'THROTTLE', 'RTRIM',
            'LTRIM', 'TRIM', 'UPPERCASE', 'LOWERCASE', 'CRC32', 'CHECKSUM',
            'JQ', 'MATCH', 'PROMETHEUS_PATTERN', 'PROMETHEUS_TO_JSON',
            'CSV_PATTERN', 'STR_REPLACE', 'COPY', 'QUERY_FIELD', 'PROMOTE',
            'STRLEN', 'GET_GROUP', 'GET_MACRO', 'GET_SENSITIVE', 'GET_URL'
        ]
        
        # Недопустимые типы (единицы измерения)
        invalid_as_type = ['°C', 'MHz', 'GB', 'W', 's', 'ms', 'B', 'KB', 'MB']
        
        for i, step in enumerate(preprocessing):
            step_type = step.find('type')
            if step_type is not None:
                st = step_type.text
                
                # Проверка на недопустимые типы
                if st in invalid_as_type:
                    self.errors['critical'].append(
                        f"{key}: Тип preprocessing '{st}' НЕВАЛИДЕН! "
                        f"Это единицы измерения, должны быть в <units>, не в <type>"
                    )
                
                # Проверка на допустимые типы
                elif st not in valid_pp_types:
                    self.errors['warning'].append(f"{key}: Нестандартный тип preprocessing '{st}'")
                
                # Проверка параметров для regex
                if st == 'REGEX':
                    params = step.findall('.//parameters/parameter')
                    if len(params) == 0:
                        self.errors['warning'].append(f"{key}: REGEX preprocessing без параметров")
    
    def check_discovery_rules(self):
        """Проверка discovery rules"""
        print("\n" + "="*80)
        print("6️⃣ ПРОВЕРКА DISCOVERY RULES")
        print("="*80)
        
        drs = self.root.findall('.//discovery_rules/discovery_rule')
        self.stats['discovery_rules'] = len(drs)
        
        for dr in drs:
            name = dr.find('name').text
            key = dr.find('key').text
            delay = dr.find('delay').text
            lifetime = dr.find('lifetime').text
            
            print(f"\n📁 {name}")
            print(f"   Key: {key}, Delay: {delay}, Lifetime: {lifetime}")
            
            # Проверка LLD макросов
            lld_macros = dr.findall('.//lld_macro_paths/lld_macro_path')
            print(f"   LLD Macros: {len(lld_macros)}")
            
            has_id = False
            for lld in lld_macros:
                path = lld.find('path').text
                lld_name = lld.find('name').text
                print(f"     {lld_name} ← {path}")
                if lld_name == '{#Id}':
                    has_id = True
            
            if not has_id:
                self.errors['critical'].append(f"DR {key}: Отсутствует макрос {{#Id}}")
            
            # Проверка item prototypes
            item_protos = dr.findall('.//item_prototypes/item_prototype')
            print(f"   Item Prototypes: {len(item_protos)}")
            self.stats['item_prototypes'] = len(item_protos)
            
            for proto in item_protos:
                proto_name = proto.find('name').text
                proto_key = proto.find('key').text
                proto_type = proto.find('type').text if proto.find('type') is not None else 'UNKNOWN'
                proto_delay = proto.find('delay').text
                proto_value_type = proto.find('value_type').text
                
                # Проверка value_type
                if proto_value_type not in ['0', '1', '3', '4']:
                    self.errors['warning'].append(f"{proto_key}: value_type='{proto_value_type}' (ожидалось 0/1/3/4)")
                
                # Проверка URL
                url_elem = proto.find('url')
                if url_elem is not None:
                    url = url_elem.text
                    if proto_type == 'HTTP_AGENT' and '{#Id}' not in url and 'discovery' not in proto_key.lower():
                        # Это может быть нормально для некоторых случаев
                        pass
                
                # Проверка preprocessing
                self._check_preprocessing(proto, proto_key)
                
                print(f"     [{proto_type}] {proto_key} (delay: {proto_delay}, vt: {proto_value_type})")
            
            # Проверка trigger prototypes
            trigger_protos = dr.findall('.//trigger_prototypes/trigger_prototype')
            print(f"   Trigger Prototypes: {len(trigger_protos)}")
            self.stats['trigger_prototypes'] = len(trigger_protos)
            
            for trig in trigger_protos:
                trig_name = trig.find('name').text
                trig_priority = trig.find('priority').text
                trig_expr = trig.find('expression').text
                
                # Проверка priority
                valid_priorities = ['DISASTER', 'HIGH', 'AVERAGE', 'WARNING', 'INFO', 'NOT CLASSIFIED']
                if trig_priority not in valid_priorities:
                    self.errors['warning'].append(f"Trigger {trig_name}: Неверный priority '{trig_priority}'")
                
                print(f"     [{trig_priority}] {trig_name}")
            
            # Проверка graph prototypes
            graph_protos = dr.findall('.//graph_prototypes/graph_prototype')
            print(f"   Graph Prototypes: {len(graph_protos)}")
            self.stats['graph_prototypes'] = len(graph_protos)
    
    def check_value_maps(self):
        """Проверка value maps"""
        print("\n" + "="*80)
        print("7️⃣ ПРОВЕРКА VALUE MAPS")
        print("="*80)
        
        vms = self.root.findall('.//value_maps/value_map')
        self.stats['value_maps'] = len(vms)
        print(f"📊 Всего value maps: {len(vms)}")
        
        vm_names = set()
        for vm in vms:
            vm_name = vm.find('name').text
            mappings = vm.findall('mapping')
            
            if vm_name in vm_names:
                self.errors['warning'].append(f"Дублирующийся value map: {vm_name}")
            vm_names.add(vm_name)
            
            print(f"  {vm_name}: {len(mappings)} mappings")
            
            # Проверка на дубликаты значений
            values = set()
            for mapping in mappings:
                value = mapping.find('value').text
                if value in values:
                    self.errors['warning'].append(f"Value map {vm_name}: Дубликат значения '{value}'")
                values.add(value)
    
    def check_for_specific_issues(self):
        """Специальные проверки"""
        print("\n" + "="*80)
        print("8️⃣ СПЕЦИАЛЬНЫЕ ПРОВЕРКИ")
        print("="*80)
        
        # Проверка на наличие ome.metrics.grouped с {#Id}
        grouped_item = self.root.find(".//item[key='ome.metrics.grouped']")
        if grouped_item is not None:
            post_data = grouped_item.find('post_data')
            if post_data is not None and '{#Id}' in post_data.text:
                self.errors['critical'].append(
                    "Item ome.metrics.grouped: Использует {#Id} в post_data вне discovery context!"
                )
                print("  ✗ ome.metrics.grouped: Проблема с {#Id}")
            else:
                print("  ✓ ome.metrics.grouped: OK")
        else:
            print("  ✓ ome.metrics.grouped: Не найден (удалён)")
        
        # Проверка session auth
        auth_item = self.root.find(".//item[key='ome.session.auth']")
        if auth_item is not None:
            promote_step = auth_item.find(".//preprocessing/step[type='PROMOTE']")
            if promote_step is not None:
                param = promote_step.find('.//parameters/parameter')
                if param is not None and '--macro={$OME_SESSION_ID}' in param.text:
                    print("  ✓ Session authentication: PROMOTE настроен корректно")
                else:
                    self.errors['warning'].append("Session auth: PROMOTE макрос может быть настроен неправильно")
            else:
                self.errors['warning'].append("Session auth: Отсутствует PROMOTE шаг")
        else:
            self.errors['warning'].append("Session auth: Item не найден")
        
        # Проверка на дубликаты ключей
        all_keys = []
        for item in self.root.findall('.//item/key'):
            if item.text:
                all_keys.append(item.text)
        for proto in self.root.findall('.//item_prototype/key'):
            if proto.text:
                all_keys.append(proto.text)
        
        duplicates = set([k for k in all_keys if all_keys.count(k) > 1])
        if duplicates:
            self.errors['critical'].append(f"Дублирующиеся ключи: {duplicates}")
            print(f"  ✗ Дубликаты ключей: {duplicates}")
        else:
            print("  ✓ Дубликаты ключей: Не найдены")
    
    def print_summary(self):
        """Вывод сводки"""
        print("\n" + "="*80)
        print("📊 СВОДНАЯ СТАТИСТИКА")
        print("="*80)
        print(f"  Макросы:            {self.stats['macros']}")
        print(f"  Приложения:         {self.stats['applications']}")
        print(f"  Items:              {self.stats['items']}")
        print(f"  Discovery Rules:    {self.stats['discovery_rules']}")
        print(f"  Item Prototypes:    {self.stats['item_prototypes']}")
        print(f"  Trigger Prototypes: {self.stats['trigger_prototypes']}")
        print(f"  Graph Prototypes:   {self.stats['graph_prototypes']}")
        print(f"  Value Maps:         {self.stats['value_maps']}")
        
        print("\n" + "="*80)
        print("🚨 НАЙДЕННЫЕ ПРОБЛЕМЫ")
        print("="*80)
        
        if self.errors['critical']:
            print(f"\n🔴 КРИТИЧЕСКИЕ ({len(self.errors['critical'])}):")
            for err in self.errors['critical']:
                print(f"  • {err}")
        
        if self.errors['warning']:
            print(f"\n🟡 ПРЕДУПРЕЖДЕНИЯ ({len(self.errors['warning'])}):")
            for err in self.errors['warning']:
                print(f"  • {err}")
        
        if self.errors['info']:
            print(f"\nℹ️ ИНФОРМАЦИЯ ({len(self.errors['info'])}):")
            for err in self.errors['info']:
                print(f"  • {err}")
        
        if not any(self.errors.values()):
            print("\n  ✅ Проблем не найдено!")
        
        print("\n" + "="*80)
        
        # Итоговый вердикт
        if self.errors['critical']:
            print(f"\n❌ НАЙДЕНО {len(self.errors['critical'])} критических проблем!")
            print("   Шаблон НЕ ГОТОВ к использованию!")
            return False
        elif self.errors['warning']:
            print(f"\n⚠️ НАЙДЕНО {len(self.errors['warning'])} предупреждений")
            print("   Шаблон готов к использованию, но рекомендуется исправить предупреждения")
            return True
        else:
            print("\n✅ Шаблон готов к использованию!")
            return True
    
    def analyze(self):
        """Запуск полного анализа"""
        print("="*80)
        print("🔍 DELL OME TEMPLATE v2.0 - COMPREHENSIVE ERROR ANALYSIS")
        print("="*80)
        print(f"Файл: {self.filepath}")
        print(f"Дата: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.load_template():
            return False
        
        self.check_xml_structure()
        self.check_template_basic()
        self.check_macros()
        self.check_applications()
        self.check_items()
        self.check_discovery_rules()
        self.check_value_maps()
        self.check_for_specific_issues()
        
        return self.print_summary()


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'template_dell_ome_2.0.xml'
    analyzer = TemplateAnalyzer(filepath)
    success = analyzer.analyze()
    sys.exit(0 if success else 1)
