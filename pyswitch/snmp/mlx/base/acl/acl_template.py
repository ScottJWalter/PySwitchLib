"""
Copyright 2017 Brocade Communications Systems, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

create_acl_template = '''
    mac access-list {{ acl_name_str }}
    '''

delete_acl_template = '''
    no mac access-list {{ acl_name_str }}
    '''

show_ip_access_list = '''
    show access-list name {{ acl_name_str }}
    '''

show_l2_access_list = '''
    show access-list l2 {{ acl_name_str }}
    '''

add_l2_acl_rule_template = '''
    {% if seq_id_str is not none %} sequence {{ seq_id_str }} {% endif %}
    {% if action_str is not none %} {{ action_str }} {% endif %}
    {% if source_str is not none %} {{ source_str }} {% endif %}
    {% if dst_str is not none %} {{ dst_str }} {% endif %}
    {% if vlan_str is not none %} {{ vlan_str }} {% endif %}
    {% if ethertype_str is not none %} {{ ethertype_str }} {% endif %}
    {% if drop_precedence_force_str is not none %}
    {{ drop_precedence_force_str }} {% endif %}
    {% if mirror_str is not none %} {{ mirror_str }} {% endif %}
    {% if drop_precedence_str is not none %}
    {{ drop_precedence_str }} {% endif %}
    {% if priority_str is not none %} {{ priority_str }} {% endif %}
    {% if priority_force_str is not none %}
    {{ priority_force_str }} {% endif %}
    {% if priority_mapping_str is not none %}
    {{ priority_mapping_str }} {% endif %}
    {% if log_str is not none %} {{ log_str }} {% endif %}
    {% if arp_guard_str is not none %} {{ arp_guard_str }} {% endif %}
    '''

delete_rule_by_seq_id = '''
    no sequence {{ seq_id_str }}
    '''