# statemap.py — минимальная версия для поддержки SMC Python FSM

class FSMException(Exception):
    pass


class State:
    def __init__(self, name):
        self._name = name

    def Entry(self, fsm):
        pass

    def Exit(self, fsm):
        pass

    def __str__(self):
        return self._name


class StateMap:
    def __init__(self):
        self._states = {}

    def add_state(self, name, state):
        self._states[name] = state

    def get_state(self, name):
        return self._states.get(name)


class FSMContext:
    def __init__(self, state):
        self._state = state
        self._state_stack = []

    def getState(self):
        return self._state

    def setState(self, state):
        if self._state is not None:
            self._state.Exit(self)
        self._state = state
        if self._state is not None:
            self._state.Entry(self)

    def pushState(self, state):
        self._state_stack.append(self._state)
        self.setState(state)

    def popState(self):
        if self._state_stack:
            self.setState(self._state_stack.pop())
        else:
            raise FSMException("State stack is empty.")

    def clearStateStack(self):
        self._state_stack.clear()
