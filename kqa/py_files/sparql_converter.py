import re
import shlex

def sparql_to_graph(sparql):
    PRED_INSTANCE = 'pred:instance_of'
    PRED_NAME = 'pred:name'

    PRED_VALUE = 'pred:value'       # link packed value node to its literal value
    PRED_UNIT = 'pred:unit'         # link packed value node to its unit

    PRED_YEAR = 'pred:year'         # link packed value node to its year value, which is an integer
    PRED_DATE = 'pred:date'         # link packed value node to its date value, which is a date

    PRED_FACT_H = 'pred:fact_h'     # link qualifier node to its head
    PRED_FACT_R = 'pred:fact_r'
    PRED_FACT_T = 'pred:fact_t'

    SPECIAL_PREDICATES = (PRED_INSTANCE, PRED_NAME, PRED_VALUE, PRED_UNIT, PRED_YEAR, PRED_DATE, PRED_FACT_H, PRED_FACT_R, PRED_FACT_T)

    target = None

    """
    Some sparql have UNION inside. Ingore them at this stage.
    """

    if sparql.startswith('SELECT DISTINCT ?e') or sparql.startswith('SELECT ?e'):
        parse_type = 'name'
        target = '?e'
    elif sparql.startswith('SELECT (COUNT(DISTINCT ?e)'):
        parse_type = 'count'
        target = 'count ?e'
    elif sparql.startswith('SELECT DISTINCT ?p '):
        parse_type = 'pred'
        target = '?p'
    elif sparql.startswith('ASK'):
        parse_type = 'bool'
        target = 'bool'
    else:
        parse_type = 'attr'
        tokens = sparql.split()
        target = tokens[2]
        
        """
        Should consider attributes selection here, but it is complex at first glance. Ignore it first and 
        I will implemented it later
        """
        pass

    case = 0
    triples = None
    '''
    0 - Normal case
    1 - UNION exist
    2 - "\'" exist
    3 -  BOTH 1 and 2 happens
    4 - 2 happens and "\'" in pred and will cause the shlex throw error
    '''
    if 'UNION' in sparql:
        case = 1
        triples = sparql.split('{', maxsplit=1)[1].rsplit('}', maxsplit=1)[0]
        match = re.fullmatch(r'''(.*?){(.*?)} UNION {(.*?)}(.*)''', triples)
        four_triples = match.groups()
        '''
        Now the four_triples contain four triples and [2:3] are union based
        '''
        triples = []
        for idx, group in enumerate(four_triples):
            _gs = re.split(r'''\.(?=(?:[^"]|"[^"]*")*$)''', group)
            _gs = [_g.strip() for _g in _gs]
            if idx == 0:
                _gs.append('SEPARATER{')
            elif idx == 1:
                _gs.append('}SEPARATER{')
            elif idx == 2:
                _gs.append('}SEPARATER')
            triples += _gs

    if '\'' in sparql:
        case = 2 if case == 0 else 3
        if case == 2:
            triples = sparql.split('{')[1].split('}')[0]
            triples = re.split(r'''\.(?=(?:[^"]|"[^"]*")*$)''', triples)
            triples = [triple.strip() for triple in triples]
        else:
            pass

    if case == 0: # Normal case
        triples = sparql.split('{')[1].split('}')[0]
        triples = re.split(r'''\.(?=(?:[^"]|"[^"]*")*$)''', triples)
        triples = [triple.strip() for triple in triples]
    
    '''
    Match the space: if there are even number of " or ' after the space, use it as the delimilator
    The re is hard to match escape quote
    '''
    seperated_triples = []

    if case == 2 or case == 3:
        '''
        There is a case that r\' in pred and make the whole string quote in double quotes and cannot be recognized by shlex
        A question that index is 3060~3070 in train is a case
        '''
        for triple in triples:
            try:
                new_triple = shlex.split(triple)
            except:
                case = 4
                return case, target, None
            if not (len(new_triple) == 0 or new_triple == ''):
                seperated_triples.append(new_triple)
    if case == 0 or case == 1:
        for triple in triples:
            new_triple = shlex.split(triple)
            if not (len(new_triple) == 0 or new_triple == ''):
                seperated_triples.append(new_triple)
    
    '''
    Now make all seperated triple to the format we want
    '''
    disposed_triples = []
    for triple in seperated_triples:
        if len(triple) == 3:
            r = triple[1]
            if r.startswith('<'): # and not r.startswith('<pred:'):
                # A normal predicate/relation 
                relation = r[1:-1].replace('_', ' ')
                new_triple = (triple[0], relation, triple[2])
                disposed_triples.append(new_triple)
            elif r == PRED_INSTANCE:
                pass
                # relation = r[6:-1].replace('_', ' ')
                # new_triple = (triple[0], relation, triple[2])
                # disposed_triples.append(new_triple)
            elif r == PRED_NAME:
                pass
            elif r == PRED_VALUE:
                pass
            elif r == PRED_UNIT:
                pass
            elif r == PRED_YEAR:
                pass
            elif r == PRED_DATE:
                pass
            else:
                new_triple = (triple[0], triple[1], triple[2])
                disposed_triples.append(new_triple)

        elif len(triple) != 3:
            if triple[0] == '[':
                pred = triple[10]
                if pred.startswith('<'):
                    pred = pred[1:-1].replace('_', ' ')
                attr = triple[11]
                fact_h = triple[2]
                fact_r = triple[5]
                if fact_r.startswith('<'):
                    fact_r = fact_r[1:-1].replace('_', ' ')
                fact_t = triple[8]
                qualifier_nodes = [fact_h, fact_r, fact_t]
                new_triple = (*qualifier_nodes, pred, attr)
                disposed_triples.append(new_triple)
            elif triple[0] == 'FILTER':
                new_triple = " ".join(triple)
                disposed_triples.append(tuple([new_triple]))
            elif 'SEPARATER' in triple[0]:
                disposed_triples.append(tuple(triple))

    '''
    Post process
    '''
    if parse_type == 'name':
        pass
    elif parse_type == 'count':
        pass
    elif parse_type == 'bool':
        pass
    elif parse_type == 'pred':
        pass
    elif parse_type == 'attr': 
        pass

    return case, target, disposed_triples

'''
###########################
###########################
###########################
'''

def statement_simplification(case, target, statement):
    if case == 4:
        return None

    statement_refine = []
    for triple in statement:
        if len(triple) == 3:
            if triple[1].startswith('pred:') and triple[1] != 'pred:instance of' and triple[1] != 'pred:name':
                pass
            elif triple[1] == 'pred:instance of':
                statement_refine.append((triple[0], 'instance of', triple[2]))
            elif triple[1] == 'pred:name':
                statement_refine.append((triple[0], 'NAME'))
            else:
                if triple[1] != '?p':
                    if 'e' in triple[2]:
                        statement_refine.append((triple[0], 'relational', triple[2]))
                    else:
                        statement_refine.append((triple[0], 'literal', triple[2]))
                else:
                    statement_refine.append(triple)
        elif len(triple) != 3:
            if 'FILTER' in triple[0]:
                statement_refine.append(tuple(['OPERATION']))
            elif 'SEPARATER' in triple[0]:
                if triple[0] == 'SEPARATER{':
                    statement_refine.append(tuple(['[']))
                elif triple[0] == '}SEPARATER{':
                    statement_refine.append(tuple(['UNION']))
                else:
                    statement_refine.append(tuple([']']))
            elif len(triple) == 5: # Must be qualifier
                if 'e' in triple[2]:
                    statement_refine.append((triple[0], 'relational', triple[2], 'qualifier', triple[4]))
                else:
                    statement_refine.append((triple[0], 'literal', triple[2], 'qualifier', triple[4]))
    return statement_refine

'''
###########################
###########################
###########################
'''

def graph_simplifier_rough_no_literal(case, parse_type, target, query_graph):

    PRED_VALUE = 'pred:value'       # link packed value node to its literal value
    PRED_UNIT = 'pred:unit'         # link packed value node to its unit

    PRED_YEAR = 'pred:year'         # link packed value node to its year value, which is an integer
    PRED_DATE = 'pred:date'  

    if (case == 1) or (case == 3) or (case == 4):
        return
    for statement in query_graph:
        if (PRED_VALUE in statement[1]) or (PRED_UNIT in statement[1]) or (PRED_YEAR in statement[1]) or (PRED_DATE in statement[1]):
            return

    substitution_dict = dict()
    for statement in query_graph:
        if len(statement) == 3: # Normal case, no qualifier, no filter
            if statement[1] == 'pred:name':
                substitution_dict[statement[0]] = statement[2]

    output_graph = []
    keys = list(substitution_dict.keys())
    for statement in query_graph:
        if len(statement) == 3 or len(statement) == 5: # Normal case, no qualifier, no filter
            if statement[1] == 'pred:name':
                pass
            else:
                ### Refine the statement
                new_statement_0 = statement[0]
                new_statement_2 = statement[2]
                if statement[0] in keys:
                    new_statement_0 = substitution_dict[statement[0]]
                if statement[2] in keys:
                    new_statement_2 = substitution_dict[statement[2]]

                if len(statement) == 3:
                    output_graph.append((new_statement_0, statement[1], new_statement_2))
                elif len(statement) == 5:
                    output_graph.append((new_statement_0, statement[1], new_statement_2, statement[3], statement[4]))
        else:
            print("Special graph")
            output_graph.append(statement)
    
    # Check redundant qualifier and triple
    statement_need_remove = []
    for statement in output_graph:
        if len(statement) == 5:
            for st in output_graph:
                if len(st) == 3 and (st[0] == statement[0]) and (st[1] == statement[1]) and (st[0] == statement[0]):
                    statement_need_remove.append(st)
    for st in statement_need_remove:
        output_graph.remove(st)

    return output_graph
