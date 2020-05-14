from IPython.core.magic import magics_class, line_cell_magic, Magics
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import warnings

from .rules_utils import quick_assert_fact, _delete_state

@magics_class
class DurableRulesMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(DurableRulesMagic, self).__init__(shell)
        self.graph = None
        self.RULESET = None

    @line_cell_magic
    @magic_arguments()
    @argument('--ruleset', '-r', default='', help='Ruleset name.')
    @argument('--no-reset', action='store_false', help='Disable automatic state deletion.')
    def assert_facts(self, line, cell):
        "Assert several facts."
        args = parse_argstring(self.assert_facts, line)
        if not args.ruleset and self.RULESET is None:
            warnings.warn("You must provide a ruleset reference (--ruleset/-r RULESET).")
            return
        elif args.ruleset:
            self.RULESET = self.shell.user_ns[args.ruleset]

        _ruleset = self.RULESET
        #print(_ruleset)

        if args.no_reset:
            _delete_state(_ruleset)

        for _assertion in cell.split('\n'):
            quick_assert_fact(_ruleset, _assertion)