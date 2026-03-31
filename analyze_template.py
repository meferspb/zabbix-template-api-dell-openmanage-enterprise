#!/usr/bin/env python3
"""
Dell OME Template v2.0 - Deep Analysis Script
Analyzes Zabbix template for errors, issues, and improvement opportunities
"""

import xml.etree.ElementTree as ET
import re
from collections import defaultdict

def analyze_template(filepath):
    """Analyze Zabbix template for issues"""
    
    print("=" * 80)
    print("DEEP ANALYSIS: Dell OME Template v2.0")
    print("=" * 80)
    print()
    
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    issues = {
        'critical': [],
        'warning': [],
        'suggestion': []
    }
    
    stats = {
        'macros': 0,
        'applications': 0,
        'items': 0,
        'discovery_rules': 0,
        'item_prototypes': 0,
        'trigger_prototypes': 0,
        'graph_prototypes': 0,
        'value_maps': 0
    }
    
    template = root.find('.//template')
    
    # 1. Analyze Macros
    print("📊 АНАЛИЗ МАКРОСОВ")
    print("-" * 40)
    macros = template.findall('.//macros/macro')
    stats['macros'] = len(macros)
    
    macro_names = set()
    for macro in macros:
        name = macro.find('macro').text
        value_elem = macro.find('value')
        value = value_elem.text if value_elem is not None and value_elem.text else ''
        desc = macro.find('description').text if macro.find('description') is not None else ''
        
        macro_names.add(name)
        print(f"  {name} = {value[:50] if value else '(пусто)'}{'...' if value and len(value) > 50 else ''}")
    
    # Check required macros
    required_macros = ['{$OME_HOST}', '{$OME_USER}', '{$OME_PASSWORD}', '{$OME_TIMEOUT}']
    for req in required_macros:
        if req not in macro_names:
            issues['critical'].append(f"Отсутствует обязательный макрос: {req}")
    
    # Check password macro
    password_macro = template.find(".//macro[macro='{$OME_PASSWORD}']")
    if password_macro is not None:
        value_elem = password_macro.find('value')
        if value_elem is not None and value_elem.text:
            issues['warning'].append("Макрос {$OME_PASSWORD} имеет значение по умолчанию - это небезопасно!")
    
    print(f"\n  Всего макросов: {stats['macros']}")
    print()
    
    # 2. Analyze Applications
    print("📁 АНАЛИЗ ПРИЛОЖЕНИЙ")
    print("-" * 40)
    apps = template.findall('.//applications/application')
    stats['applications'] = len(apps)
    
    app_names = []
    for app in apps:
        name = app.find('name').text
        app_names.append(name)
        print(f"  ✓ {name}")
    
    # Check for unused applications
    print(f"\n  Всего приложений: {stats['applications']}")
    print()
    
    # 3. Analyze Items
    print("🔧 АНАЛИЗ ITEMS")
    print("-" * 40)
    items = template.findall('.//items/item')
    stats['items'] = len(items)
    
    item_keys = set()
    for item in items:
        name = item.find('name').text
        key = item.find('key').text
        type_elem = item.find('type')
        item_type = type_elem.text if type_elem is not None else 'UNKNOWN'
        delay = item.find('delay').text if item.find('delay') is not None else 'N/A'
        
        item_keys.add(key)
        
        # Check for issues
        if item_type == 'HTTP_AGENT':
            url = item.find('url')
            if url is not None and '{$OME_SESSION_ID}' in url.text and key != 'ome.session.auth':
                # This is OK - session is used after auth
                pass
        
        # Check for unused preprocessing steps
        preprocessing = item.findall('.//preprocessing/step')
        for step in preprocessing:
            step_type = step.find('type')
            if step_type is not None:
                # Check for invalid preprocessing types
                valid_types = ['JSONPATH', 'REGEX', 'PROMOTE', 'STRLEN', 'XPATH', 'XMLVALUE', 
                              'CHANGE_PER_SECOND', 'DELTA', 'MULTIPLIER', 'OFFSET', 
                              'DECIMAL', 'HEX_DEC', 'OCT_DEC', 'BOOL_DEC', 'BOOL_OCT',
                              'DISCARD_UNCHANGED', 'THROTTLE', 'RTRIM', 'LTRIM', 'TRIM',
                              'UPPERCASE', 'LOWERCASE', 'CRC32', 'CHECKSUM', 'JQ', 'MATCH',
                              'PROMETHEUS_PATTERN', 'PROMETHEUS_TO_JSON', 'CSV_PATTERN',
                              'STR_REPLACE', 'COPY', 'XPATH', 'QUERY_FIELD']
                if step_type.text not in valid_types and step_type.text not in ['°C', 'MHz', 'GB', 'W', 's', 'length', 'sum', 'regex']:
                    issues['warning'].append(f"Item {key}: Нестандартный тип preprocessing '{step_type.text}'")
        
        print(f"  {item_type}: {key} (delay: {delay})")
    
    print(f"\n  Всего items: {stats['items']}")
    print()
    
    # 4. Analyze Discovery Rules
    print("🔍 АНАЛИЗ DISCOVERY RULES")
    print("-" * 40)
    discovery_rules = template.findall('.//discovery_rules/discovery_rule')
    stats['discovery_rules'] = len(discovery_rules)
    
    for dr in discovery_rules:
        name = dr.find('name').text
        key = dr.find('key').text
        delay = dr.find('delay').text
        lifetime = dr.find('lifetime').text
        
        print(f"  {name}")
        print(f"    Key: {key}, Delay: {delay}, Lifetime: {lifetime}")
        
        # Check LLD macros
        lld_macros = dr.findall('.//lld_macro_paths/lld_macro_path')
        print(f"    LLD Macros: {len(lld_macros)}")
        for lld in lld_macros:
            path = lld.find('path').text
            lld_name = lld.find('name').text
            print(f"      {lld_name} ← {path}")
        
        # Check for {#Id} usage
        id_macro = dr.find(".//lld_macro_path[name='{#Id}']")
        if id_macro is None:
            issues['critical'].append(f"Discovery rule {key}: Отсутствует макрос {{#Id}} - критично для работы шаблона!")
        
        # Check item prototypes
        item_protos = dr.findall('.//item_prototypes/item_prototype')
        print(f"    Item Prototypes: {len(item_protos)}")
        
        # Analyze each prototype
        for proto in item_protos:
            proto_name = proto.find('name').text
            proto_key = proto.find('key').text
            proto_type = proto.find('type').text if proto.find('type') is not None else 'UNKNOWN'
            proto_delay = proto.find('delay').text
            proto_value_type = proto.find('value_type').text
            
            item_keys.add(proto_key)
            stats['item_prototypes'] += 1
            
            # Check URL for {#Id} usage
            url_elem = proto.find('url')
            if url_elem is not None and '{#Id}' not in url_elem.text and proto_type == 'HTTP_AGENT':
                issues['warning'].append(f"Item prototype {proto_key}: URL не использует {{#Id}}")
            
            # Check for invalid value_type
            if proto_value_type not in ['0', '1', '3', '4']:
                issues['warning'].append(f"Item prototype {proto_key}: Неправильный value_type '{proto_value_type}'")
            
            # Check preprocessing steps
            preprocessing = proto.findall('.//preprocessing/step')
            for step in preprocessing:
                step_type = step.find('type')
                if step_type is not None:
                    # Check for invalid preprocessing types used as units
                    if step_type.text in ['°C', 'MHz', 'GB', 'W', 's']:
                        issues['critical'].append(f"Item prototype {proto_key}: Тип preprocessing '{step_type.text}' НЕВАЛИДЕН! Должен быть в элементе <units>, не в <type>")
                    if step_type.text == 'regex' and len(step.findall('parameters/parameter')) == 0:
                        issues['warning'].append(f"Item prototype {proto_key}: regex preprocessing без параметров")
            
            print(f"      {proto_type}: {proto_key} (delay: {proto_delay}, type: {proto_value_type})")
        
        # Check trigger prototypes
        trigger_protos = dr.findall('.//trigger_prototypes/trigger_prototype')
        print(f"    Trigger Prototypes: {len(trigger_protos)}")
        
        for trig in trigger_protos:
            trig_name = trig.find('name').text
            trig_expr = trig.find('expression').text
            trig_priority = trig.find('priority').text
            
            stats['trigger_prototypes'] += 1
            
            # Check for valid priority
            valid_priorities = ['DISASTER', 'HIGH', 'AVERAGE', 'WARNING', 'INFO', 'NOT CLASSIFIED']
            if trig_priority not in valid_priorities:
                issues['warning'].append(f"Trigger prototype {trig_name}: Неправильный priority '{trig_priority}'")
            
            # Check expression for proper item key usage
            for key in item_keys:
                if key in trig_expr:
                    break
            
            print(f"      [{trig_priority}] {trig_name}")
        
        # Check graph prototypes
        graph_protos = dr.findall('.//graph_prototypes/graph_prototype')
        print(f"    Graph Prototypes: {len(graph_protos)}")
        stats['graph_prototypes'] += len(graph_protos)
        
        for graph in graph_protos:
            graph_name = graph.find('name').text
            graph_items = graph.findall('.//graph_items/graph_item')
            print(f"      {graph_name} ({len(graph_items)} items)")
            
            for gi in graph_items:
                item_ref = gi.find('item').text
                # Check if referenced item exists
                if item_ref not in item_keys:
                    issues['warning'].append(f"Graph {graph_name}: Ссылка на несуществующий item '{item_ref}'")
    
    print(f"\n  Всего discovery rules: {stats['discovery_rules']}")
    print()
    
    # 5. Analyze Value Maps
    print("🗺️ АНАЛИЗ VALUE MAPS")
    print("-" * 40)
    value_maps = root.findall('.//value_maps/value_map')
    stats['value_maps'] = len(value_maps)
    
    for vm in value_maps:
        vm_name = vm.find('name').text
        mappings = vm.findall('mapping')
        print(f"  {vm_name}: {len(mappings)} mappings")
    
    print(f"\n  Всего value maps: {stats['value_maps']}")
    print()
    
    # 6. Check for specific issues
    print("🔎 СПЕЦИАЛЬНЫЕ ПРОВЕРКИ")
    print("-" * 40)
    
    # Check ome.metrics.grouped item
    grouped_item = template.find(".//item[key='ome.metrics.grouped']")
    if grouped_item is not None:
        post_data = grouped_item.find('post_data')
        if post_data is not None and '{#Id}' in post_data.text:
            issues['critical'].append(f"Item ome.metrics.grouped: Использует {{#Id}} в post_data, но это НЕ item prototype - макрос не будет работать!")
        print(f"  ✗ ome.metrics.grouped: Проблема - использует {{#Id}} вне discovery context")
    else:
        print(f"  ✓ ome.metrics.grouped: Не найден")
    
    # Check session auth item
    auth_item = template.find(".//item[key='ome.session.auth']")
    if auth_item is not None:
        promote_step = auth_item.find(".//preprocessing/step[type='PROMOTE']")
        if promote_step is not None:
            param = promote_step.find('.//parameters/parameter')
            if param is not None and '--macro={$OME_SESSION_ID}' in param.text:
                print(f"  ✓ Session authentication: PROMOTE макрос настроен корректно")
            else:
                issues['warning'].append("Session authentication: PROMOTE макрос может быть настроен неправильно")
    
    # Check for duplicate keys
    all_keys = list(item_keys)
    duplicates = [k for k in all_keys if all_keys.count(k) > 1]
    if duplicates:
        issues['critical'].append(f"Дублирующиеся ключи: {set(duplicates)}")
        print(f"  ✗ Найдены дубликаты: {set(duplicates)}")
    else:
        print(f"  ✓ Дубликаты ключей: Не найдены")
    
    # Check URL encoding
    for item in template.findall('.//item') + template.findall('.//item_prototype'):
        url_elem = item.find('url')
        if url_elem is not None:
            url = url_elem.text
            if "'" in url and "InventoryDetails" in url:
                # URL with single quotes may need encoding
                print(f"  ⚠ URL содержит кавычки: {url}")
    
    print()
    
    # 7. Summary
    print("=" * 80)
    print("📊 СВОДНАЯ СТАТИСТИКА")
    print("=" * 80)
    print(f"  Макросы:           {stats['macros']}")
    print(f"  Приложения:        {stats['applications']}")
    print(f"  Items:             {stats['items']}")
    print(f"  Discovery Rules:   {stats['discovery_rules']}")
    print(f"  Item Prototypes:   {stats['item_prototypes']}")
    print(f"  Trigger Prototypes:{stats['trigger_prototypes']}")
    print(f"  Graph Prototypes:  {stats['graph_prototypes']}")
    print(f"  Value Maps:        {stats['value_maps']}")
    print()
    
    print("=" * 80)
    print("🚨 НАЙДЕННЫЕ ПРОБЛЕМЫ")
    print("=" * 80)
    
    if issues['critical']:
        print("\n🔴 КРИТИЧЕСКИЕ (обязательно к исправлению):")
        for issue in issues['critical']:
            print(f"  • {issue}")
    
    if issues['warning']:
        print("\n🟡 ПРЕДУПРЕЖДЕНИЯ (рекомендуется исправить):")
        for issue in issues['warning']:
            print(f"  • {issue}")
    
    if not issues['critical'] and not issues['warning']:
        print("\n  ✓ Проблем не найдено!")
    
    print()
    print("=" * 80)
    
    return issues, stats


if __name__ == '__main__':
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else 'template_dell_ome_2.0.xml'
    issues, stats = analyze_template(filename)
    
    # Exit with error code if critical issues found
    if issues['critical']:
        print(f"\n❌ НАЙДЕНО {len(issues['critical'])} критических проблем!")
        exit(1)
    else:
        print(f"\n✅ Критических проблем не найдено")
        exit(0)
