import json
from collections import Counter
from utils.misc import init_vocab
from datetime import date
from queue import Queue
from utils.value_class import ValueClass

kb_json = './dataset/kb.json'

train_json = './dataset/train.json'
val_json = './dataset/val.json'
test_json = './dataset/test.json'

'''
##################################################################################################################################
NOTE:

Deprecated functions
##################################################################################################################################
'''


def get_number_entity(kb_json):
    counter = Counter()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        for attr_dict in kb['entities'][i]['attributes']:
            # print(attr_dict['key'])
            counter.update(['literal'])
            for qk, qvs in attr_dict['qualifiers'].items():
                # print(qk, ":", qvs)
                # counter.update(['qualifier'])
                for qv in qvs:
                    counter.update(['qualifier'])

        for rel_dict in kb['entities'][i]['relations']:
            # print(attr_dict['key'])
            counter.update(['relation'])
            for qk, qvs in rel_dict['qualifiers'].items():
                # print(qk, ":", qvs)
                for qv in qvs:
                    counter.update(['qualifier'])

    return kb, counter


# def get_qualifier_all_undirect(kb_json):
#     qualifier = set()
#     counter = Counter()
#     number_counter = Counter()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:
#         for attr_dict in kb['entities'][i]['attributes']:
#             counter.update(['literal'])
#             for qk, qvs in attr_dict['qualifiers'].items():
#                 counter.update(['literal qualifier'])
#                 # FIXME: what if no qualifier?
#                 qualifier.add((i, attr_dict['key'], str(attr_dict['value']['value']), qk, *[str(qv['value']) for qv in qvs]))
#                 number_counter.update([len(qvs)])

#         for rel_dict in kb['entities'][i]['relations']:
#             counter.update(['relation'])
#             for qk, qvs in rel_dict['qualifiers'].items():
#                 counter.update(['relational qualifier'])
#                 # FIXME: what if no qualifier?
#                 qualifier.add((i, rel_dict['predicate'], rel_dict['object'], qk, *[str(qv['value']) for qv in qvs]))
#                 number_counter.update([len(qvs)])

#     return kb, counter, number_counter, qualifier


# def get_qualifier_all_triple_undirect(kb_json):
#     qualifier = set()
#     counter = Counter()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:
#         for attr_dict in kb['entities'][i]['attributes']:
#             # print(attr_dict['key'])
#             counter.update(['literal'])
#             for qk, qvs in attr_dict['qualifiers'].items():
#                 # print(qk, ":", qvs)
#                 # counter.update(['qualifier'])
#                 for qv in qvs:
#                     counter.update(['literal qualifier'])
#                     # print(f"Qualifier: [({kb['entities'][i]['name']}, {attr_dict['key']}, {attr_dict['value']}), {qk}, {qv}]")
#                     qualifier.add(((kb['entities'][i]['name'], attr_dict['key'], attr_dict['value']['value']), qk, qv['value']))

#         for rel_dict in kb['entities'][i]['relations']:
#             # print(attr_dict['key'])
#             counter.update(['relation'])
#             for qk, qvs in rel_dict['qualifiers'].items():
#                 # print(qk, ":", qvs)
#                 for qv in qvs:
#                     counter.update(['relational qualifier'])
#                     # FIXME This is wrong: 1. left name right id. 2. no direction
#                     qualifier.add(((kb['entities'][i]['name'], rel_dict['predict'], rel_dict['object']), qk, qv['value']))

#     return kb, counter, qualifier


# def statistic(number_counter):
#     total = 0
#     total_value = 0
#     max_length = 0
#     min_length = 999
#     single = 0
#     hyper = 0
#     for key, value in number_counter.items():
#         total += value
#         total_value += key * value
#         max_length = max(max_length, key)
#         min_length = min(min_length, key)
#         if key == 1: single += value
#         else: hyper += value
#     mean_length = total_value / total
#     return mean_length, max_length, min_length, single, hyper


'''
##################################################################################################################################
NOTE:

Auxiliary function
##################################################################################################################################
'''

def string_clean(s: str) -> str:
    s = s.replace(',', ' ')
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
##################################################################################################################################
NOTE:

The following fuctions have not consider the direction in the relation, nor consider invalid format in string (like ',')
##################################################################################################################################
'''


# def get_qualifier_undirect(kb_json, output=False, file_name='kb_q_ud.txt'):
#     qualifier = set()
#     counter = Counter()
#     number_counter = Counter()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:
#         for attr_dict in kb['entities'][i]['attributes']:
#             counter.update(['literal'])
#             for qk, qvs in attr_dict['qualifiers'].items():
#                 counter.update(['literal qualifier'])
#                 # FIXME: what if no qualifier?
#                 qualifier.add((i, attr_dict['key'], str(attr_dict['value']['value']), qk, *[str(qv['value']) for qv in qvs]))
#                 number_counter.update([len(qvs)])

#         for rel_dict in kb['entities'][i]['relations']:
#             counter.update(['relation'])
#             for qk, qvs in rel_dict['qualifiers'].items():
#                 counter.update(['relational qualifier'])
#                 # FIXME: what if no qualifier?
#                 qualifier.add((i, rel_dict['predicate'], rel_dict['object'], qk, *[str(qv['value']) for qv in qvs]))
#                 number_counter.update([len(qvs)])

#     if output:
#         str_q = [",".join(q)+'\n' for q in qualifier]
#         with open(file_name, 'w') as f:
#             f.writelines(str_q)

#     return qualifier


# def get_qualifier_relation_undirect(kb_json, output=False, file_name='kb_q_r_ud.txt'):
#     qualifier = set()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:

#         for rel_dict in kb['entities'][i]['relations']:
#             for qk, qvs in rel_dict['qualifiers'].items():
#                 qualifier.add((i, rel_dict['predicate'], rel_dict['object'], qk, *[str(qv['value']) for qv in qvs]))

#     if output:
#         str_q = [",".join(q)+'\n' for q in qualifier]
#         with open(file_name, 'w') as f:
#             f.writelines(str_q)

#     return qualifier


# def get_relation_undirect(kb_json, output=False, file_name='kb_r_ud.txt'):
#     qualifier = set()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:

#         for rel_dict in kb['entities'][i]['relations']:
#             if len(rel_dict['qualifiers']) == 0:
#                 qualifier.add((i, rel_dict['predicate'], rel_dict['object']))
#             else:
#                 for qk, qvs in rel_dict['qualifiers'].items():
#                     qualifier.add((i, rel_dict['predicate'], rel_dict['object'], qk, *[str(qv['value']) for qv in qvs]))

#     if output:
#         str_q = [",".join(q)+'\n' for q in qualifier]
#         with open(file_name, 'w') as f:
#             f.writelines(str_q)

#     return qualifier


# def get_qualifier_relation_clean_undirect(kb_json, output=False, file_name='kb_q_r_clean_ud.txt'):
#     qualifier = set()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:
#         for rel_dict in kb['entities'][i]['relations']:
#             for qk, qvs in rel_dict['qualifiers'].items():
#                 new_qvs = []
#                 for qv in qvs:
#                     if qv['type'] != 'string':
#                         continue
#                     new_qvs.append(qv['value'])
#                 if len(new_qvs) != 0:
#                     qualifier.add((i, rel_dict['predicate'], rel_dict['object'], qk, *new_qvs))

#     if output:
#         str_q = [",".join(q)+'\n' for q in qualifier]
#         with open(file_name, 'w') as f:
#             f.writelines(str_q)

#     return qualifier


# def get_relation_clean_undirect(kb_json, output=False, file_name='kb_r_clean_ud.txt'):
#     qualifier = set()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:
#         for rel_dict in kb['entities'][i]['relations']:
#             if len(rel_dict['qualifiers']) == 0:
#                 qualifier.add((i, rel_dict['predicate'], rel_dict['object']))
#             else:
#                 for qk, qvs in rel_dict['qualifiers'].items():
#                     new_qvs = []
#                     for qv in qvs:
#                         if qv['type'] != 'string':
#                             continue
#                         new_qvs.append(qv['value'])
#                     if len(new_qvs) != 0:
#                         qualifier.add((i, rel_dict['predicate'], rel_dict['object'], qk, *new_qvs))
#                     else:
#                         qualifier.add((i, rel_dict['predicate'], rel_dict['object']))

#     if output:
#         str_q = [",".join(q)+'\n' for q in qualifier]
#         with open(file_name, 'w') as f:
#             f.writelines(str_q)

#     return qualifier

'''
##################################################################################################################################
NOTE:

The following fuctions have directions and should be use, but does not consider invalid format in string

Update: Find another problem. There are some qk that has many qvs, which is a problem that could not be handled by StarE. This 
need to be corrected.
##################################################################################################################################
'''

'''
V1.0: find that statement format is wrong. Deprecated.
'''

# def get_qualifier_relation_clean(kb_json, output=False, file_name='kb_q_r_clean.txt'):
#     qualifier = set()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:
#         for rel_dict in kb['entities'][i]['relations']:
#             for qk, qvs in rel_dict['qualifiers'].items():
#                 new_qvs = []
#                 for qv in qvs:
#                     if qv['type'] != 'string':
#                         continue
#                     new_qvs.append(qv['value'])
#                 if len(new_qvs) != 0:
#                     if rel_dict['direction'] == 'forward':
#                         qualifier.add((i, rel_dict['predicate'], rel_dict['object'], qk, *new_qvs))
#                     elif  rel_dict['direction'] == 'backward':
#                         qualifier.add((rel_dict['object'], rel_dict['predicate'], i, qk, *new_qvs))

#     if output:
#         str_q = [",".join(q)+'\n' for q in qualifier]
#         with open(file_name, 'w') as f:
#             f.writelines(str_q)

#     return qualifier


# def get_relation_clean(kb_json, output=False, file_name='kb_r_clean.txt'):
#     qualifier = set()
#     kb = json.load(open(kb_json))
#     for i in kb['entities']:
#         for rel_dict in kb['entities'][i]['relations']:
#             if len(rel_dict['qualifiers']) == 0:
#                 if rel_dict['direction'] == 'forward':
#                     qualifier.add((i, rel_dict['predicate'], rel_dict['object']))
#                 elif  rel_dict['direction'] == 'backward':
#                     qualifier.add((rel_dict['object'], rel_dict['predicate'], i))
                
#             else:
#                 for qk, qvs in rel_dict['qualifiers'].items():
#                     new_qvs = []
#                     for qv in qvs:
#                         if qv['type'] != 'string':
#                             continue
#                         new_qvs.append(qv['value'])
#                     if len(new_qvs) != 0:
#                         if rel_dict['direction'] == 'forward':
#                             qualifier.add((i, rel_dict['predicate'], rel_dict['object'], qk, *new_qvs))
#                         elif  rel_dict['direction'] == 'backward':
#                             qualifier.add((rel_dict['object'], rel_dict['predicate'], i, qk, *new_qvs))
#                     else:
#                         if rel_dict['direction'] == 'forward':
#                             qualifier.add((i, rel_dict['predicate'], rel_dict['object']))
#                         elif  rel_dict['direction'] == 'backward':
#                             qualifier.add((rel_dict['object'], rel_dict['predicate'], i))

#     if output:
#         str_q = [",".join(q)+'\n' for q in qualifier]
#         with open(file_name, 'w') as f:
#             f.writelines(str_q)

#     return qualifier

'''
V1.1: Find that if mix id and name, will have duplicated statements (for reference, 9 duplicated found).
      However, there must be the case that the same name will point to different entities. So this function
      is still in use. Maybe in the future we need to also treat this to the qualifier qv pairs?
'''

def get_qualifier_relational_clean(kb_json, output=False, file_name='kb_q_r_clean.txt'):
    qualifier = set()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        for rel_dict in kb['entities'][i]['relations']:
            # First: add fact key, also called triple pairs
            statement = list()
            if rel_dict['direction'] == 'forward':
                statement += [i, string_clean(rel_dict['predicate']), rel_dict['object']]
            elif  rel_dict['direction'] == 'backward':
                statement += [rel_dict['object'], string_clean(rel_dict['predicate']), i]

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

    if output:
        str_q = [",".join(q)+'\n' for q in qualifier]
        with open(file_name, 'w') as f:
            f.writelines(str_q)

    return qualifier

def get_relational_clean(kb_json, output=False, file_name='kb_r_clean.txt'):
    qualifier = set()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        for rel_dict in kb['entities'][i]['relations']:
            # First: add fact key, also called triple pairs
            statement = list()
            if rel_dict['direction'] == 'forward':
                statement += [i, string_clean(rel_dict['predicate']), rel_dict['object']]
            elif  rel_dict['direction'] == 'backward':
                statement += [rel_dict['object'], string_clean(rel_dict['predicate']), i]

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
            qualifier.add(tuple(statement))

    if output:
        str_q = [",".join(q)+'\n' for q in qualifier]
        with open(file_name, 'w') as f:
            f.writelines(str_q)

    return qualifier

def get_literal_clean(kb_json, output=False, file_name='kb_r_clean.txt'):
    qualifier = set()
    kb = json.load(open(kb_json))
    for i in kb['entities']:
        for rel_dict in kb['entities'][i]['attributes']:
            # First: add fact key, also called triple pairs
            statement = list()
            if rel_dict['direction'] == 'forward':
                statement += [i, string_clean(rel_dict['predicate']), rel_dict['object']]
            elif  rel_dict['direction'] == 'backward':
                statement += [rel_dict['object'], string_clean(rel_dict['predicate']), i]

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
            qualifier.add(tuple(statement))

    if output:
        str_q = [",".join(q)+'\n' for q in qualifier]
        with open(file_name, 'w') as f:
            f.writelines(str_q)

    return qualifier

'''
V1.2
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