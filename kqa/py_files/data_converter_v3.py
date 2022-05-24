import json
import numpy as np
from collections import Counter

kb_json = '../dataset/kb.json'

train_json = '../dataset/train.json'
val_json = '../dataset/val.json'
test_json = '../dataset/test.json'

def string_clean(s: str) -> str:
    s = s.replace(',', ' and ')
    s = ' '.join(s.split())
    return s

def find_name(kb, id):
    try:
        return kb['entities'][id]['name']
    except:
        try:
            return kb['concepts'][id]['name']
        except:
            raise


'''
###########################
###########################
qualifer: contain only qualifier
relational: only consider relational
attributes: only consider attributes
clean: no literal
fullname: no ID
###########################
'''

# Version that will have same sort
def get_qualifier_relational_clean_fullname_combine(kb_json, output=False, file_name='kb_q_r_clean_fullname_combine.txt'):
    qualifier = dict()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        fullname = kb['entities'][i]['name']
        for rel_dict in kb['entities'][i]['relations']:
            # First: add fact key, also called triple pairs
            statement = None
            if rel_dict['direction'] == 'forward':
                statement = (string_clean(fullname), string_clean(rel_dict['predicate']), string_clean(find_name(kb, rel_dict['object'])))
            elif  rel_dict['direction'] == 'backward':
                statement = (string_clean(find_name(kb, rel_dict['object'])), string_clean(rel_dict['predicate']), string_clean(fullname))
            
            if not statement in qualifier: 
                qualifier[statement] = dict()

            for qk, qvs in rel_dict['qualifiers'].items():                
                # Second add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                new_qvs = []
                for qv in qvs:
                    if qv['type'] == 'string':
                        new_qvs.append(string_clean(qv['value']))
                        
                if len(new_qvs) != 0:
                    for qv in new_qvs:
                        if string_clean(qk) not in qualifier[statement]:
                            qualifier[statement][string_clean(qk)] = [qv]
                        else:
                            if qv not in qualifier[statement][string_clean(qk)]:
                                qualifier[statement][string_clean(qk)] += [qv]
        
    # Third: Make sure the statement is qualifier 
    output_qualifier = set()
    for statement, qkv_pairs in qualifier.items():    
        if len(qkv_pairs) > 0:
            new_qkv_list = []
            for qk in qkv_pairs:
                for qv in qkv_pairs[qk]:
                    new_qkv_list += [qk, qv]
            output_qualifier.add(tuple(list(statement) + new_qkv_list))

    # output_qualifier = sorted(output_qualifier)

    if output:
        str_q = [",".join(q)+'\n' for q in output_qualifier]
        with open(file_name, 'w', encoding='utf-8') as f:
            f.writelines(str_q)

    return output_qualifier

def get_relational_clean_fullname_combine(kb_json, output=False, file_name='kb_r_clean_fullname_combine.txt'):
    qualifier = dict()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        fullname = kb['entities'][i]['name']
        
        # For instance of
        for concept_id in kb['entities'][i]['instanceOf']:
            statement = (string_clean(fullname), 'instance of', string_clean(find_name(kb, concept_id)))
            if not statement in qualifier: 
                qualifier[statement] = dict()

        for rel_dict in kb['entities'][i]['relations']:
            # First: add fact key, also called triple pairs
            statement = None
            if rel_dict['direction'] == 'forward':
                statement = (string_clean(fullname), string_clean(rel_dict['predicate']), string_clean(find_name(kb, rel_dict['object'])))
            elif  rel_dict['direction'] == 'backward':
                statement = (string_clean(find_name(kb, rel_dict['object'])), string_clean(rel_dict['predicate']), string_clean(fullname))
            
            if not statement in qualifier: 
                qualifier[statement] = dict()

            for qk, qvs in rel_dict['qualifiers'].items():                
                # Second add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                new_qvs = []
                for qv in qvs:
                    if qv['type'] == 'string':
                        new_qvs.append(string_clean(qv['value']))
                        
                if len(new_qvs) != 0:
                    for qv in new_qvs:
                        if string_clean(qk) not in qualifier[statement]:
                            qualifier[statement][string_clean(qk)] = [qv]
                        else:
                            if qv not in qualifier[statement][string_clean(qk)]:
                                qualifier[statement][string_clean(qk)] += [qv]

    # Third: Add statement
    output_qualifier = set()
    for statement, qkv_pairs in qualifier.items():    
        new_qkv_list = []
        for qk in qkv_pairs:
            for qv in qkv_pairs[qk]:
                new_qkv_list += [qk, qv]
        output_qualifier.add(tuple(list(statement) + new_qkv_list))
    
    # output_qualifier = sorted(output_qualifier)
    
    if output:
        str_q = [",".join(q)+'\n' for q in output_qualifier]
        with open(file_name, 'w', encoding='utf-8') as f:
            f.writelines(str_q)
    
    return output_qualifier

def get_attributes_clean_fullname_combine(kb_json, output=False, file_name='kb_a_clean_fullname_combine.txt'):
    qualifier = dict()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        fullname = kb['entities'][i]['name']

        # For attribute
        for att_dict in kb['entities'][i]['attributes']:
            # First: if it is literal, ignore it
            if att_dict['value']['type'] != 'string':
                continue
            else:
                # Second: add attributes
                statement = (string_clean(fullname), string_clean(att_dict['key']), string_clean(att_dict['value']['value']))
            
            if not statement in qualifier: 
                qualifier[statement] = dict()

            for qk, qvs in att_dict['qualifiers'].items():                
                # Second add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                new_qvs = []
                for qv in qvs:
                    if qv['type'] == 'string':
                        new_qvs.append(string_clean(qv['value']))
                        
                if len(new_qvs) != 0:
                    for qv in new_qvs:
                        if string_clean(qk) not in qualifier[statement]:
                            qualifier[statement][string_clean(qk)] = [qv]
                        else:
                            if qv not in qualifier[statement][string_clean(qk)]:
                                qualifier[statement][string_clean(qk)] += [qv]
            
    # Third: Add statement
    output_qualifier = set()
    for statement, qkv_pairs in qualifier.items():    
        new_qkv_list = []
        for qk in qkv_pairs:
            for qv in qkv_pairs[qk]:
                new_qkv_list += [qk, qv]
        output_qualifier.add(tuple(list(statement) + new_qkv_list))
    
    # output_qualifier = sorted(output_qualifier)
    
    if output:
        str_q = [",".join(q)+'\n' for q in output_qualifier]
        with open(file_name, 'w', encoding='utf-8') as f:
            f.writelines(str_q)
    
    return output_qualifier

def get_all_clean_fullname_combine(kb_json, output=False, file_name='kb_all_clean_fullname_combine.txt'):
    qualifier = dict()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        fullname = kb['entities'][i]['name']
        
        # For instance of
        for concept_id in kb['entities'][i]['instanceOf']:
            statement = (string_clean(fullname), 'instance of', string_clean(find_name(kb, concept_id)))
            if not statement in qualifier: 
                qualifier[statement] = dict()

        # For relation
        for rel_dict in kb['entities'][i]['relations']:
            # First: add fact key, also called triple pairs
            statement = None
            if rel_dict['direction'] == 'forward':
                statement = (string_clean(fullname), string_clean(rel_dict['predicate']), string_clean(find_name(kb, rel_dict['object'])))
            elif  rel_dict['direction'] == 'backward':
                statement = (string_clean(find_name(kb, rel_dict['object'])), string_clean(rel_dict['predicate']), string_clean(fullname))
            
            if not statement in qualifier: 
                qualifier[statement] = dict()

            for qk, qvs in rel_dict['qualifiers'].items():                
                # Second add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                new_qvs = []
                for qv in qvs:
                    if qv['type'] == 'string':
                        new_qvs.append(string_clean(qv['value']))
                        
                if len(new_qvs) != 0:
                    for qv in new_qvs:
                        if string_clean(qk) not in qualifier[statement]:
                            qualifier[statement][string_clean(qk)] = [qv]
                        else:
                            if qv not in qualifier[statement][string_clean(qk)]:
                                qualifier[statement][string_clean(qk)] += [qv]

        # For attribute
        for att_dict in kb['entities'][i]['attributes']:
            # First: if it is literal, ignore it
            if att_dict['value']['type'] != 'string':
                continue
            else:
                # Second: add attributes
                statement = (string_clean(fullname), string_clean(att_dict['key']), string_clean(att_dict['value']['value']))
            
            if not statement in qualifier: 
                qualifier[statement] = dict()

            for qk, qvs in att_dict['qualifiers'].items():                
                # Second add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                new_qvs = []
                for qv in qvs:
                    if qv['type'] == 'string':
                        new_qvs.append(string_clean(qv['value']))
                        
                if len(new_qvs) != 0:
                    for qv in new_qvs:
                        if string_clean(qk) not in qualifier[statement]:
                            qualifier[statement][string_clean(qk)] = [qv]
                        else:
                            if qv not in qualifier[statement][string_clean(qk)]:
                                qualifier[statement][string_clean(qk)] += [qv]

    # Third: Add statement
    output_qualifier = set()
    for statement, qkv_pairs in qualifier.items():    
        new_qkv_list = []
        for qk in qkv_pairs:
            for qv in qkv_pairs[qk]:
                new_qkv_list += [qk, qv]
        output_qualifier.add(tuple(list(statement) + new_qkv_list))
    
    output_qualifier = sorted(output_qualifier)
    
    if output:
        str_q = [",".join(q)+'\n' for q in output_qualifier]
        with open(file_name, 'w', encoding='utf-8') as f:
            f.writelines(str_q)
    
    return output_qualifier

