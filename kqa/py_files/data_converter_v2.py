import json
import numpy as np
from collections import Counter

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

def get_qualifier_relational_clean_fullname(kb_json, output=False, file_name='kb_q_r_clean_fullname.txt'):
    qualifier = set()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        fullname = kb['entities'][i]['name']
        for rel_dict in kb['entities'][i]['relations']:
            # First: add fact key, also called triple pairs
            statement = list()
            if rel_dict['direction'] == 'forward':
                statement += [string_clean(fullname), string_clean(rel_dict['predicate']), string_clean(find_name(kb, rel_dict['object']))]
            elif  rel_dict['direction'] == 'backward':
                statement += [string_clean(find_name(kb, rel_dict['object'])), string_clean(rel_dict['predicate']), string_clean(fullname)]

            for qk, qvs in rel_dict['qualifiers'].items():                
                # Second add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                new_qvs = []
                for qv in qvs:
                    if qv['type'] == 'string':
                        new_qvs.append(string_clean(qv['value']))
                        
                if len(new_qvs) != 0:
                    for qv in new_qvs:
                        statement += [string_clean(qk), qv]
        
            # Third: Make sure the statement is qualifier 
            if len(statement) > 3:
                qualifier.add(tuple(statement))

    # qualifier = sorted(qualifier)

    if output:
        str_q = [",".join(q)+'\n' for q in qualifier]
        with open(file_name, 'w') as f:
            f.writelines(str_q)

    return qualifier

def get_relational_clean_fullname(kb_json, output=False, file_name='kb_r_clean_fullname.txt'):
    qualifier = set()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        fullname = kb['entities'][i]['name']
        
        # For instance of
        for concept_id in kb['entities'][i]['instanceOf']:
            statement = [string_clean(fullname), 'instance of', string_clean(find_name(kb, concept_id))]
            qualifier.add(tuple(statement))

        # For relation
        for rel_dict in kb['entities'][i]['relations']:
            # First: add fact key, also called triple pairs
            statement = list()
            if rel_dict['direction'] == 'forward':
                statement += [string_clean(fullname), string_clean(rel_dict['predicate']), string_clean(find_name(kb, rel_dict['object']))]
            elif  rel_dict['direction'] == 'backward':
                statement += [string_clean(find_name(kb, rel_dict['object'])), string_clean(rel_dict['predicate']), string_clean(fullname)]

            for qk, qvs in rel_dict['qualifiers'].items():                
                # Second add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                new_qvs = []
                for qv in qvs:
                    if qv['type'] == 'string':
                        new_qvs.append(string_clean(qv['value']))
                        
                if len(new_qvs) != 0:
                    for qv in new_qvs:
                        statement += [string_clean(qk), qv]

            # Third: add statement
            qualifier.add(tuple(statement))

    # qualifier = sorted(qualifier)

    if output:
        str_q = [",".join(q)+'\n' for q in qualifier]
        with open(file_name, 'w') as f:
            f.writelines(str_q)
    
    return qualifier

def get_qualifier_attributes_clean_fullname(kb_json, output=False, file_name='kb_q_a_clean_fullname.txt'):
    qualifier = set()
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
                statement = list()
                statement += [string_clean(fullname), string_clean(att_dict['key']), string_clean(att_dict['value']['value'])]

                for qk, qvs in att_dict['qualifiers'].items():                
                    # Third: add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                    new_qvs = []
                    for qv in qvs:
                        if qv['type'] == 'string':
                            new_qvs.append(string_clean(qv['value']))
                            
                    if len(new_qvs) != 0:
                        for qv in new_qvs:
                            statement += [string_clean(qk), qv]
            
                # Fourth: Make sure the statement is qualifier 
                if len(statement) > 3:
                    qualifier.add(tuple(statement))

    # qualifier = sorted(qualifier)

    if output:
        str_q = [",".join(q)+'\n' for q in qualifier]
        with open(file_name, 'w') as f:
            f.writelines(str_q)
    
    return qualifier

def get_attributes_clean_fullname(kb_json, output=False, file_name='kb_a_clean_fullname.txt'):
    qualifier = set()
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
                statement = list()
                statement += [string_clean(fullname), string_clean(att_dict['key']), string_clean(att_dict['value']['value'])]

                for qk, qvs in att_dict['qualifiers'].items():                
                    # Third: add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                    new_qvs = []
                    for qv in qvs:
                        if qv['type'] == 'string':
                            new_qvs.append(string_clean(qv['value']))
                            
                    if len(new_qvs) != 0:
                        for qv in new_qvs:
                            statement += [string_clean(qk), qv]
            
                # Fourth: Add statement
                qualifier.add(tuple(statement))

    # qualifier = sorted(qualifier)

    if output:
        str_q = [",".join(q)+'\n' for q in qualifier]
        with open(file_name, 'w') as f:
            f.writelines(str_q)
    
    return qualifier

def get_all_clean_fullname(kb_json, output=False, file_name='kb_all_clean_fullname.txt'):
    qualifier = set()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        fullname = kb['entities'][i]['name']

        # For instance of
        for concept_id in kb['entities'][i]['instanceOf']:
            statement = [string_clean(fullname), 'instance of', string_clean(find_name(kb, concept_id))]
            qualifier.add(tuple(statement))

        # For attribute
        for att_dict in kb['entities'][i]['attributes']:
            # First: if it is literal, ignore it
            if att_dict['value']['type'] != 'string':
                continue
            else:
                # Second: add attributes
                statement = list()
                statement += [string_clean(fullname), string_clean(att_dict['key']), string_clean(att_dict['value']['value'])]

                for qk, qvs in att_dict['qualifiers'].items():                
                    # Third: add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                    new_qvs = []
                    for qv in qvs:
                        if qv['type'] == 'string':
                            new_qvs.append(string_clean(qv['value']))
                            
                    if len(new_qvs) != 0:
                        for qv in new_qvs:
                            statement += [string_clean(qk), qv]
            
                # Fourth: Add statement
                qualifier.add(tuple(statement))

        # For relation
        for rel_dict in kb['entities'][i]['relations']:
            # First: add fact key, also called triple pairs
            statement = list()
            if rel_dict['direction'] == 'forward':
                statement += [string_clean(fullname), string_clean(rel_dict['predicate']), string_clean(find_name(kb, rel_dict['object']))]
            elif  rel_dict['direction'] == 'backward':
                statement += [string_clean(find_name(kb, rel_dict['object'])), string_clean(rel_dict['predicate']), string_clean(fullname)]

            for qk, qvs in rel_dict['qualifiers'].items():                
                # Second add qk - qv pairs, for qv that have more than one instance, seperate to single qk - qv pairs
                new_qvs = []
                for qv in qvs:
                    if qv['type'] == 'string':
                        new_qvs.append(string_clean(qv['value']))
                        
                if len(new_qvs) != 0:
                    for qv in new_qvs:
                        statement += [string_clean(qk), qv]
        
            # Third: Add statement 
            qualifier.add(tuple(statement))

    # qualifier = sorted(qualifier)

    if output:
        str_q = [",".join(q)+'\n' for q in qualifier]
        with open(file_name, 'w') as f:
            f.writelines(str_q)
    
    return qualifier

'''
###########################
###########################
###########################
'''

def random_sampling(s: set, split: list=[0.85, 0.15]):
    str_l = [",".join(q)+'\n' for q in s]
    str_l = np.array(str_l)
    length = len(str_l)
    permutation = np.random.permutation(length).reshape(-1)
    trn_length = np.round(length * split[0]).astype(int)
    # vld_length = np.round(length * split[1])
    tst_length = np.round(length * split[1]).astype(int)
    # assert (trn_length + vld_length + tst_length) == length
    assert (trn_length + tst_length) == length
    trn = str_l[permutation[0:trn_length]]
    # vld = str_l[permutation[trn_length:trn_length+vld_length]]
    # tst = str_l[permutation[trn_length+vld_length:length]]
    tst = str_l[permutation[trn_length:length]]

    with open("train.txt", 'w')as f:
        f.writelines(trn)
    with open("test.txt", 'w')  as f:
        f.writelines(tst)

'''
###########################
###########################
###########################
'''

