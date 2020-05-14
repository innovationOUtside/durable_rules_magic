from IPython.core.magic import magics_class, line_cell_magic, Magics
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

import uuid
from durable.lang import assert_fact, delete_state, m, c
from durable.engine import MessageObservedException
import warnings


def new_ruleset(name=None):
    """Optionally create, then set, new ruleset name."""
    #TO DO - add in rules to check a name is well-formed
    if name and isinstance(name, str):
        return name
    return f'rs_{uuid.uuid4()}'

def subject_(pred, obj):
    """Clause where subject is assumed and predicate and object tested."""
    return (m.predicate == pred) & (m.object == obj)

def predicate_(subj, obj):
    """Clause where predicate is assumed and subject and object tested."""
    return  (m.subject == subj) & (m.object == obj)

def object_(subj, pred):
    """Clause where object is assumed and subject and predicate tested."""
    return  (m.subject == subj) & (m.predicate == pred)

def _delete_state(rs):
    """Clear the state associated with a ruleset."""
    try:
        delete_state(rs, None)
    except:
        pass

def spo(subj, pred, obj):
    """Return subject-predicate-object dict."""
    if not isinstance(subj, str):
        subj = subj.m.subject
    if not isinstance(obj, str):
        obj = subj.m.object
    if not isinstance(pred, str):
        pred = subj.m.predicate

    return { 'subject': subj, 'predicate': pred, 'object': obj }

def quick_assert_fact(r, f):
    """
    Assert a fact from a colon separated triple string.
    Triple strings of the form: "a subject: predicate : and object"
    """
    _statement = [t.strip() for t in f.split(':')]
    
    if len(_statement) != 3:
        return

    subj = _statement[0]
    pred = _statement[1]
    obj = _statement[2]
    #print('..', r, spo(subj, pred, obj ),'..' )
    try:
        assert_fact(r, spo(subj, pred, obj ) )
    except MessageObservedException:
        warnings.warn(f"Assertion error: is {_statement} already asserted?")