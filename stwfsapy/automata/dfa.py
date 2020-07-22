# Copyright 2020 Leibniz Information Centre for Economics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import List, Dict, Iterable, Tuple, Any, Callable, Optional

_KEY_STATE_SYMBOL_TRANSITIONS = 'symbol_transitions'
_KEY_STATE_NON_WORD_CHAR_TRANSITION = 'non_word_char_transitions'
_KEY_STATE_ACCEPTS = 'accepts'
_KEY_DFA_STATES = 'states'


class State:

    def __init__(
            self,
            symbol_transitions=None,
            non_word_char_transition=None,
            accepts=None):
        self.symbol_transitions: Dict[str, int] = symbol_transitions or dict()
        """Transitions consuming a symbol."""
        self.non_word_char_transition: Optional[int] = non_word_char_transition
        """Transition consuming a non word character symbol."""
        self.accepts: List[Any] = accepts or []
        """What is accepted by this state."""

    def set_symbol_transition(self, symbol: str, idx: int):
        self.symbol_transitions[symbol] = idx

    def set_non_word_char_transition(self, idx: int):
        self.non_word_char_transition = idx

    def add_acceptances(self, accepts: Iterable):
        self.accepts.extend(accepts)

    def to_dict(
            self,
            acceptance_handler: Callable) -> Dict[str, Any]:
        return {
            _KEY_STATE_SYMBOL_TRANSITIONS: self.symbol_transitions,
            _KEY_STATE_NON_WORD_CHAR_TRANSITION: self.non_word_char_transition,
            _KEY_STATE_ACCEPTS: [acceptance_handler(a) for a in self.accepts],
        }

    def __eq__(self, other):
        return isinstance(other, State) and self.accepts == other.accepts and (
            self.symbol_transitions == other.symbol_transitions) and (
                self.non_word_char_transition == other.non_word_char_transition
            )

    @staticmethod
    def from_dict(
            conf: Dict[str, Any],
            acceptance_handler: Callable):
        return State(
            symbol_transitions=conf[_KEY_STATE_SYMBOL_TRANSITIONS],
            non_word_char_transition=conf.get(
                _KEY_STATE_NON_WORD_CHAR_TRANSITION),
            accepts=[
                acceptance_handler(accept)
                for accept
                in conf[_KEY_STATE_ACCEPTS]
            ]
        )


class Dfa:
    """Represents a deterministic finite automaton.
    This class is not intended to be used directly.
    Instead create a stwfsapy.automata.nfa.Nfa and convert it.
    Example:
        from stwfsapy.automata import nfa
        from stwfsapy.automata import conversion

        nfautomaton = nfa.Nfa()

        # Construct automaton,
        # e.g., using stwfsapy.automata.construction
        # ...

        nfa.remove_empty_transitions()

        dfa = conversion.NfaToDfaConverter(nfautomaton).start_conversion()"""

    def __init__(self, states=None):
        self.states: List[State] = states or []
        """All the states of this Automaton."""

    def add_state(self) -> int:
        """Creates a new state and returns its index."""
        idx = len(self.states)
        state = State()
        self.states.append(state)
        return idx

    def add_acceptances(self, idx: int, accepts: Iterable):
        """Adds new acceptances to a state.
        The state is given by its index."""
        self.states[idx].add_acceptances(accepts)

    def set_symbol_transition(self, start_idx: int, end_idx: int, symbol: str):
        """Add a new symbol consuming transition between to states.
        The states are given by their index."""
        self.states[start_idx].set_symbol_transition(symbol, end_idx)

    def set_non_word_char_transition(self, start_idx: int, end_idx: int):
        """Add a new non word char consuming transition between two states.
        The states are given by their index."""
        self.states[start_idx].set_non_word_char_transition(end_idx)

    def search(self, text: str) -> Iterable[Tuple[Any, str, int, int]]:
        """ Process a string, yielding acceptances of all substrings.
        The method assumes a DFA which has been constructed by the application
        of stwfsapy.automata.construction.ConstructionState and
        stwfsapy.automata.conversion.NfaToDfaConverter."""
        # At construction time we add non word char transitions at
        # the beginning and end of a label. Therefore add them for search.
        search_text = f'.{text}.'
        last_end_position = 0
        for start in range(len(search_text)):
            if start < last_end_position:
                continue
            stack = [(0, start)]
            while len(stack) > 0:
                state_idx, position = stack.pop()
                state = self.states[state_idx]
                non_empty_accepts = False
                for accept in state.accepts:
                    last_end_position = position
                    # subtract one from position,
                    # as the match is without consuming the next symbol
                    # subtract another one for the '.' introduced at the start
                    original_end = position - 2
                    yield (
                        accept,
                        text[start:original_end],
                        start,
                        original_end)
                    non_empty_accepts = True
                if non_empty_accepts:
                    break
                try:
                    symbol = search_text[position]
                except IndexError:
                    continue
                # First append non word_char.
                # As stack is LIFO,
                # explicit symbol transitions will be preferred.
                if not symbol.isalnum() and state.non_word_char_transition:
                    stack.append(
                        (state.non_word_char_transition, position+1))
                try:
                    transition = state.symbol_transitions[symbol]
                    stack.append((transition, position+1))
                except KeyError:
                    pass

    def to_dict(
            self,
            acceptance_handler: Callable) -> Dict[str, Any]:
        return {
            _KEY_DFA_STATES: [
                state.to_dict(acceptance_handler)
                for state
                in self.states
            ]
        }

    @staticmethod
    def from_dict(
            conf: Dict[str, Any],
            acceptance_handler: Callable):
        return Dfa([
            State.from_dict(state_conf, acceptance_handler)
            for state_conf
            in conf[_KEY_DFA_STATES]
        ])

    def __eq__(self, other):
        return isinstance(other, Dfa) and self.states == other.states
