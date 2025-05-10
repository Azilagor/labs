from NFSPathParser_sm import NFSPathParser_sm, NFSPath

MAX_LENGTH = 63

class FSMWrapper:
    def __init__(self):
        self.buf = ""
        self.server = None
        self.accepted = False

        self.fsm = NFSPathParser_sm(self)
        self.fsm.setState(NFSPath.Start)
        self.fsm.enterStartState()

    def input(self, ch):
        if ch == 'n':
            self.fsm.n()
        elif ch == 'f':
            self.fsm.f()
        elif ch == 's':
            self.fsm.s()
        elif ch == ':':
            self.fsm.Colon()
        elif ch == '/':
            self.fsm.Slash()
        elif ch == '\0' or ch == '\n':
            self.fsm.EOS()
        elif ch.isalpha():
            self.fsm.Letter(ch)
        elif ch.isdigit():
            self.fsm.Digit(ch)
        else:
            self.fsm.Default()

    # FSM actions
    def addtobuf(self, x):
        self.buf += x

    def clearbuf(self):
        self.buf = ""

    def clearallbuf(self):
        self.buf = ""

    def recordServerName(self):
        self.server = self.buf

    def recordFirstDir(self): pass

    def recordDirPath(self): pass

    def validatePath(self):
        self.accepted = True

    def nil(self):
        self.accepted = True

    def reportError(self):
        self.accepted = False


# === Метод для интеграции ===

def method_smc(line: str):
    fsm = FSMWrapper()
    try:
        path = line.strip()
        if not path.startswith("nfs://"):
            return False, None
        stripped = path[6:]
        if len(stripped) > MAX_LENGTH:
            return False, None

        for ch in path:
            fsm.input(ch)
        fsm.input('\0')
    except Exception:
        return False, None

    return fsm.accepted and fsm.server is not None, fsm.server
