#!/usr/bin/env python3
"""
Dell OME Zabbix Template Generator v2.0
Generates comprehensive Zabbix 7.0 template for Dell OpenManage Enterprise API
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_template():
    """Create the main template structure"""
    zabbix_export = ET.Element('zabbix_export')
    ET.SubElement(zabbix_export, 'version').text = '7.0'
    ET.SubElement(zabbix_export, 'date').text = '2026-03-31T14:00:00Z'
    
    # Groups
    groups = ET.SubElement(zabbix_export, 'groups')
    group = ET.SubElement(groups, 'group')
    ET.SubElement(group, 'name').text = 'Templates/Server hardware'
    
    # Template
    templates = ET.SubElement(zabbix_export, 'templates')
    template = ET.SubElement(templates, 'template')
    
    # Basic info
    ET.SubElement(template, 'template').text = 'Dell OpenManage Enterprise by HTTP agent'
    ET.SubElement(template, 'name').text = 'Dell OpenManage Enterprise by HTTP agent'
    ET.SubElement(template, 'description').text = 'Dell OME API monitoring template v2.0. Features: Auto-discovery, Status/Power/Temperature/Health monitoring, Inventory (CPU/Memory/Disk/RAID/PSU/Fans/Network), Power Metrics, GPU, Chassis, Alerts, Session control.'
    
    # Template groups
    tmpl_groups = ET.SubElement(template, 'groups')
    ET.SubElement(ET.SubElement(tmpl_groups, 'group'), 'name').text = 'Templates/Server hardware'
    
    # Macros
    macros = ET.SubElement(template, 'macros')
    macro_definitions = [
        ('{$OME_HOST}', 'https://192.168.1.100', 'Dell OME API base URL'),
        ('{$OME_USER}', 'admin', 'Username for OME API'),
        ('{$OME_PASSWORD}', '', 'Password for OME API (set manually!)'),
        ('{$OME_UPDATE_INTERVAL}', '5m', 'Discovery interval'),
        ('{$OME_TIMEOUT}', '30s', 'HTTP timeout'),
        ('{$TEMP_WARN_THRESHOLD}', '65', 'Temperature warning threshold (Celsius)'),
        ('{$TEMP_CRIT_THRESHOLD}', '80', 'Temperature critical threshold (Celsius)'),
        ('{$POWER_WARN_THRESHOLD}', '80', 'Power consumption warning threshold (%)'),
        ('{$POWER_CRIT_THRESHOLD}', '95', 'Power consumption critical threshold (%)'),
        ('{$DISK_WARN_THRESHOLD}', '80', 'Disk usage warning threshold (%)'),
        ('{$DISK_CRIT_THRESHOLD}', '90', 'Disk usage critical threshold (%)'),
        ('{$CPU_WARN_THRESHOLD}', '80', 'CPU utilization warning threshold (%)'),
        ('{$CPU_CRIT_THRESHOLD}', '95', 'CPU utilization critical threshold (%)'),
        ('{$MEMORY_WARN_THRESHOLD}', '80', 'Memory utilization warning threshold (%)'),
        ('{$MEMORY_CRIT_THRESHOLD}', '95', 'Memory utilization critical threshold (%)'),
        ('{$INVENTORY_UPDATE_INTERVAL}', '1h', 'Inventory update interval'),
        ('{$METRICS_UPDATE_INTERVAL}', '2m', 'Metrics update interval'),
        ('{$ALERTS_UPDATE_INTERVAL}', '1m', 'Alerts update interval'),
    ]
    
    for macro_name, value, desc in macro_definitions:
        macro = ET.SubElement(macros, 'macro')
        ET.SubElement(macro, 'macro').text = macro_name
        ET.SubElement(macro, 'value').text = value
        ET.SubElement(macro, 'description').text = desc
    
    # Applications
    applications = ET.SubElement(template, 'applications')
    app_names = [
        'Dell OME - Authentication', 'Dell OME - Discovery', 'Dell OME - Status',
        'Dell OME - Power', 'Dell OME - Temperature', 'Dell OME - Health',
        'Dell OME - Alerts', 'Dell OME - Inventory', 'Dell OME - CPU',
        'Dell OME - Memory', 'Dell OME - Storage', 'Dell OME - RAID',
        'Dell OME - Power Supplies', 'Dell OME - Fans', 'Dell OME - Network',
        'Dell OME - GPU', 'Dell OME - Utilization', 'Dell OME - Chassis',
        'Dell OME - System'
    ]
    for app_name in app_names:
        ET.SubElement(ET.SubElement(applications, 'application'), 'name').text = app_name
    
    # Items (Session auth and status)
    items = ET.SubElement(template, 'items')
    
    # Session Auth Item
    item = ET.SubElement(items, 'item')
    ET.SubElement(item, 'name').text = 'OME: Session Authentication'
    ET.SubElement(item, 'type').text = 'HTTP_AGENT'
    ET.SubElement(item, 'key').text = 'ome.session.auth'
    ET.SubElement(item, 'delay').text = '1m'
    ET.SubElement(item, 'history').text = '1h'
    ET.SubElement(item, 'trends').text = '0'
    ET.SubElement(item, 'value_type').text = '4'
    ET.SubElement(item, 'applications').text = 'Dell OME - Authentication'
    ET.SubElement(item, 'url').text = '{$OME_HOST}/api/SessionService/Sessions'
    ET.SubElement(item, 'timeout').text = '{$OME_TIMEOUT}'
    headers = ET.SubElement(item, 'headers')
    header = ET.SubElement(headers, 'header')
    ET.SubElement(header, 'name').text = 'Content-Type'
    ET.SubElement(header, 'value').text = 'application/json'
    ET.SubElement(item, 'post_data').text = '{"UserName": "{$OME_USER}", "Password": "{$OME_PASSWORD}"}'
    ET.SubElement(item, 'retrieve_mode').text = 'HEADERS_AND_BODY'
    preprocessing = ET.SubElement(item, 'preprocessing')
    step1 = ET.SubElement(preprocessing, 'step')
    ET.SubElement(step1, 'type').text = 'JSONPATH'
    params = ET.SubElement(step1, 'parameters')
    ET.SubElement(params, 'parameter').text = '$.SessionId'
    step2 = ET.SubElement(preprocessing, 'step')
    ET.SubElement(step2, 'type').text = 'PROMOTE'
    params2 = ET.SubElement(step2, 'parameters')
    ET.SubElement(params2, 'parameter').text = '--macro={$OME_SESSION_ID}'
    
    # Session Status Item
    item = ET.SubElement(items, 'item')
    ET.SubElement(item, 'name').text = 'OME: Session Status'
    ET.SubElement(item, 'type').text = 'DEPENDENT'
    ET.SubElement(item, 'key').text = 'ome.session.status'
    ET.SubElement(item, 'delay').text = '0'
    ET.SubElement(item, 'history').text = '1h'
    ET.SubElement(item, 'value_type').text = '3'
    ET.SubElement(item, 'applications').text = 'Dell OME - Authentication'
    ET.SubElement(item, 'master_item').text = 'ome.session.auth'
    preprocessing = ET.SubElement(item, 'preprocessing')
    step = ET.SubElement(preprocessing, 'step')
    ET.SubElement(step, 'type').text = 'STRLEN'
    params = ET.SubElement(step, 'parameters')
    ET.SubElement(params, 'parameter').text = ''
    
    # Discovery Rules
    discovery_rules = ET.SubElement(template, 'discovery_rules')
    
    # Device Discovery Rule
    dr = ET.SubElement(discovery_rules, 'discovery_rule')
    ET.SubElement(dr, 'name').text = 'Device Discovery'
    ET.SubElement(dr, 'type').text = 'HTTP_AGENT'
    ET.SubElement(dr, 'key').text = 'ome.device.discovery'
    ET.SubElement(dr, 'delay').text = '{$OME_UPDATE_INTERVAL}'
    ET.SubElement(dr, 'lifetime').text = '7d'
    ET.SubElement(dr, 'url').text = '{$OME_HOST}/api/DeviceService/Devices'
    ET.SubElement(dr, 'timeout').text = '{$OME_TIMEOUT}'
    headers = ET.SubElement(dr, 'headers')
    header = ET.SubElement(headers, 'header')
    ET.SubElement(header, 'name').text = 'X-Auth-Token'
    ET.SubElement(header, 'value').text = '{$OME_SESSION_ID}'
    preprocessing = ET.SubElement(dr, 'preprocessing')
    step = ET.SubElement(preprocessing, 'step')
    ET.SubElement(step, 'type').text = 'JSONPATH'
    params = ET.SubElement(step, 'parameters')
    ET.SubElement(params, 'parameter').text = '$.value[*]'
    
    # LLD Macro Paths
    lld_macros = ET.SubElement(dr, 'lld_macro_paths')
    lld_paths = [
        ('$..Id', '{#Id}'),
        ('$..DeviceName', '{#DeviceName}'),
        ('$..Model', '{#Model}'),
        ('$..Status', '{#Status}'),
        ('$..PowerState', '{#PowerState}'),
        ('$..DeviceServiceTag', '{#ServiceTag}'),
    ]
    for path, name in lld_paths:
        lmp = ET.SubElement(lld_macros, 'lld_macro_path')
        ET.SubElement(lmp, 'path').text = path
        ET.SubElement(lmp, 'name').text = name
    
    # Item Prototypes
    item_prototypes = ET.SubElement(dr, 'item_prototypes')
    
    # Define all item prototypes
    prototypes = [
        # Basic Status & Power (existing v1.1)
        ('{#DeviceName}: Status', 'ome.device[{#Id}.status]', '1m', '3', 'Dell OME - Status', '$.Status'),
        ('{#DeviceName}: Power State', 'ome.device[{#Id}.power]', '1m', '3', 'Dell OME - Power', '$.PowerState'),
        ('{#DeviceName}: Model', 'ome.device[{#Id}.model]', '1m', '4', 'Dell OME - Discovery', '$.Model'),
        ('{#DeviceName}: Service Tag', 'ome.device[{#Id}.tag]', '1m', '4', 'Dell OME - Discovery', '$.DeviceServiceTag'),
        ('{#DeviceName}: Identifier', 'ome.device[{#Id}.identifier]', '1m', '4', 'Dell OME - Discovery', '$.Identifier'),
        ('{#DeviceName}: Connection State', 'ome.device[{#Id}.connection]', '1m', '3', 'Dell OME - Status', '$.ConnectionState'),
        ('{#DeviceName}: Temperature', 'ome.device[{#Id}.temperature]', '2m', '3', 'Dell OME - Temperature', '$.Temperature[0].Reading', '°C'),
        ('{#DeviceName}: Health Status', 'ome.device[{#Id}.health]', '2m', '3', 'Dell OME - Health', '$.HealthState'),
        
        # Inventory - CPU
        ('{#DeviceName}: CPU Count', 'ome.device[{#Id}.cpu.count]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - CPU', '$.serverProcessors..Id', '', 'length'),
        ('{#DeviceName}: CPU Total Cores', 'ome.device[{#Id}.cpu.cores]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - CPU', '$.serverProcessors..NumberOfCores', '', 'sum'),
        ('{#DeviceName}: CPU Model', 'ome.device[{#Id}.cpu.model]', '{$INVENTORY_UPDATE_INTERVAL}', '4', 'Dell OME - CPU', '$.serverProcessors[0].BrandName'),
        
        # Inventory - Memory
        ('{#DeviceName}: Memory Total Size', 'ome.device[{#Id}.memory.total]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - Memory', '$.serverMemoryDevices..Size', '', 'sum'),
        ('{#DeviceName}: Memory Modules Count', 'ome.device[{#Id}.memory.count]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - Memory', '$.serverMemoryDevices..Id', '', 'length'),
        
        # Inventory - Storage
        ('{#DeviceName}: Disk Count', 'ome.device[{#Id}.disk.count]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - Storage', '$.serverArrayDisks..Id', '', 'length'),
        ('{#DeviceName}: RAID Controller Count', 'ome.device[{#Id}.raid.count]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - RAID', '$.serverRaidControllers..Id', '', 'length'),
        
        # Inventory - PSU
        ('{#DeviceName}: PSU Count', 'ome.device[{#Id}.psu.count]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - Power Supplies', '$.serverPowerSupplies..Id', '', 'length'),
        ('{#DeviceName}: PSU Total Wattage', 'ome.device[{#Id}.psu.wattage]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - Power Supplies', '$.serverPowerSupplies..Wattage', '', 'sum'),
        
        # Inventory - Network
        ('{#DeviceName}: NIC Count', 'ome.device[{#Id}.nic.count]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - Network', '$.serverNetworkInterfaces..Id', '', 'length'),
        
        # Inventory - Fans
        ('{#DeviceName}: Fan Count', 'ome.device[{#Id}.fan.count]', '{$INVENTORY_UPDATE_INTERVAL}', '3', 'Dell OME - Fans', '$.serverDeviceCards..Id', '', 'length'),
        
        # System
        ('{#DeviceName}: System Up Time', 'ome.device[{#Id}.uptime]', '5m', '3', 'Dell OME - System', '$.SystemUpTime'),
    ]
    
    for proto in prototypes:
        item_proto = ET.SubElement(item_prototypes, 'item_prototype')
        ET.SubElement(item_proto, 'name').text = proto[0]
        ET.SubElement(item_proto, 'type').text = 'HTTP_AGENT'
        ET.SubElement(item_proto, 'key').text = proto[1]
        ET.SubElement(item_proto, 'delay').text = proto[2]
        ET.SubElement(item_proto, 'history').text = '7d'
        ET.SubElement(item_proto, 'value_type').text = proto[3]
        ET.SubElement(item_proto, 'applications').text = proto[4]
        ET.SubElement(item_proto, 'url').text = '{$OME_HOST}/api/DeviceService/Devices({#Id})/InventoryDetails' if 'cpu' in proto[1] or 'memory' in proto[1] or 'disk' in proto[1] or 'raid' in proto[1] or 'psu' in proto[1] or 'nic' in proto[1] or 'fan' in proto[1] else '{$OME_HOST}/api/DeviceService/Devices({#Id})' if 'uptime' in proto[1] else '{$OME_HOST}/api/DeviceService/Devices({#Id})/Temperature' if 'temperature' in proto[1] else '{$OME_HOST}/api/DeviceService/Devices({#Id})/SubSystemHealth' if 'health' in proto[1] else '{$OME_HOST}/api/DeviceService/Devices({#Id})'
        ET.SubElement(item_proto, 'timeout').text = '{$OME_TIMEOUT}'
        headers = ET.SubElement(item_proto, 'headers')
        header = ET.SubElement(headers, 'header')
        ET.SubElement(header, 'name').text = 'X-Auth-Token'
        ET.SubElement(header, 'value').text = '{$OME_SESSION_ID}'
        
        if len(proto) > 5 and proto[5]:
            preprocessing = ET.SubElement(item_proto, 'preprocessing')
            step = ET.SubElement(preprocessing, 'step')
            ET.SubElement(step, 'type').text = 'JSONPATH'
            params = ET.SubElement(step, 'parameters')
            ET.SubElement(params, 'parameter').text = proto[5]
            
            if len(proto) > 7 and proto[7]:
                step2 = ET.SubElement(preprocessing, 'step')
                ET.SubElement(step2, 'type').text = proto[7]
        
        if len(proto) > 6 and proto[6]:
            ET.SubElement(item_proto, 'units').text = proto[6]
    
    # Trigger Prototypes
    trigger_prototypes = ET.SubElement(dr, 'trigger_prototypes')
    
    triggers = [
        ('last(ome.device[{#Id}.status])=1002', 'Critical Status: {#DeviceName}', 'HIGH'),
        ('last(ome.device[{#Id}.status])=1001', 'Warning Status: {#DeviceName}', 'AVERAGE'),
        ('last(ome.device[{#Id}.power])=18', 'Power Off: {#DeviceName}', 'AVERAGE'),
        ('last(ome.device[{#Id}.connection])=0', 'Not Connected: {#DeviceName}', 'HIGH'),
        ('last(ome.device[{#Id}.temperature])>{$TEMP_CRIT_THRESHOLD}', 'Temperature Critical: {#DeviceName}', 'HIGH', 'Temperature exceeded critical threshold ({$TEMP_CRIT_THRESHOLD}°C)'),
        ('last(ome.device[{#Id}.temperature])>{$TEMP_WARN_THRESHOLD}', 'Temperature Warning: {#DeviceName}', 'AVERAGE', 'Temperature exceeded warning threshold ({$TEMP_WARN_THRESHOLD}°C)'),
        ('last(ome.device[{#Id}.health])!=1', 'Health Check Failed: {#DeviceName}', 'HIGH', 'Device health status is not Normal'),
        ('last(ome.device[{#Id}.status])=1002 and last(ome.device[{#Id}.connection])=0', 'CRITICAL FAILURE: {#DeviceName}', 'DISASTER', 'Device is in CRITICAL status AND not connected - possible hardware failure'),
    ]
    
    for trig in triggers:
        trigger_proto = ET.SubElement(trigger_prototypes, 'trigger_prototype')
        ET.SubElement(trigger_proto, 'expression').text = trig[0]
        ET.SubElement(trigger_proto, 'name').text = trig[1]
        ET.SubElement(trigger_proto, 'priority').text = trig[2]
        if len(trig) > 3:
            ET.SubElement(trigger_proto, 'description').text = trig[3]
    
    # Graph Prototypes
    graph_prototypes = ET.SubElement(dr, 'graph_prototypes')
    graphs = [
        ('{#DeviceName}: Status History', 'ome.device[{#Id}.status]', '199C0D'),
        ('{#DeviceName}: Power State History', 'ome.device[{#Id}.power]', 'F63100'),
        ('{#DeviceName}: Temperature', 'ome.device[{#Id}.temperature]', 'FF0000'),
    ]
    
    for graph in graphs:
        graph_proto = ET.SubElement(graph_prototypes, 'graph_prototype')
        ET.SubElement(graph_proto, 'name').text = graph[0]
        ET.SubElement(graph_proto, 'width').text = '900'
        ET.SubElement(graph_proto, 'height').text = '200'
        graph_items = ET.SubElement(graph_proto, 'graph_items')
        gi = ET.SubElement(graph_items, 'graph_item')
        ET.SubElement(gi, 'color').text = graph[2]
        ET.SubElement(gi, 'item').text = graph[1]
    
    # Value Maps
    value_maps = ET.SubElement(zabbix_export, 'value_maps')
    
    value_map_defs = [
        ('Dell OME - Device Status', [('1000', 'Normal'), ('1001', 'Warning'), ('1002', 'Critical')]),
        ('Dell OME - Power State', [('17', 'Power On'), ('18', 'Power Off'), ('19', 'Unknown')]),
        ('Dell OME - Health Status', [('0', 'Unknown'), ('1', 'Normal'), ('2', 'Warning'), ('3', 'Critical')]),
        ('Dell OME - Connection State', [('0', 'Disconnected'), ('1', 'Connected')]),
        ('Dell OME - Session Status', [('0', 'Invalid/Expired'), ('1', 'Valid')]),
        ('Dell OME - PSU Status', [('0', 'Unknown'), ('1', 'Normal'), ('2', 'Warning'), ('3', 'Critical'), ('2000', 'OK')]),
        ('Dell OME - Fan Status', [('0', 'Unknown'), ('1', 'Normal'), ('2', 'Warning'), ('3', 'Critical'), ('2000', 'OK')]),
        ('Dell OME - Disk Status', [('0', 'Unknown'), ('1', 'Normal'), ('2', 'Warning'), ('3', 'Critical'), ('2000', 'OK')]),
        ('Dell OME - RAID Status', [('0', 'Unknown'), ('1', 'Normal'), ('2', 'Warning'), ('3', 'Critical'), ('2000', 'OK')]),
        ('Dell OME - Alert Severity', [('0', 'Unknown'), ('1', 'Critical'), ('2', 'Warning'), ('3', 'Informational')]),
    ]
    
    for vm_name, mappings in value_map_defs:
        vm = ET.SubElement(value_maps, 'value_map')
        ET.SubElement(vm, 'name').text = vm_name
        for value, label in mappings:
            mapping = ET.SubElement(vm, 'mapping')
            ET.SubElement(mapping, 'value').text = value
            ET.SubElement(mapping, 'label').text = label
    
    return zabbix_export

def prettify_xml(elem):
    """Return a pretty-printed XML string"""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

if __name__ == '__main__':
    template = create_template()
    xml_string = prettify_xml(template)
    
    # Remove extra blank lines
    lines = [line for line in xml_string.split('\n') if line.strip()]
    xml_string = '\n'.join(lines)
    
    with open('template_dell_ome_2.0.xml', 'w', encoding='utf-8') as f:
        f.write(xml_string)
    
    print("Template v2.0 generated successfully!")
    print(f"File: template_dell_ome_2.0.xml")
