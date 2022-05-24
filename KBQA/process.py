# %%
import json
import numpy as np
from collections import Counter
import re
import shlex
import copy

kb_json = '../dataset/kb.json'

train_json = '../dataset/train.json'
val_json = '../dataset/val.json'
test_json = '../dataset/test.json'

from sparql_converter import sparql_to_graph
from data_converter import get_all_clean_fullname_combine

# %%


# %%