from NFSPathParser_sm import NFSPathParser_sm

class FSMWrapper:
    def __init__(self):
        self.buf = ""
        self.server = None
        self.accepted = False

        # Инициализируем автомат и стартуем
        self.fsm = NFSPathParser_sm(self)
        self.fsm.enterStartState()

    def input(self, ch):
        print(f">>> input: '{ch}' | current state: {self.fsm.getState().getName()}")  # 🔍 Debug
     # Только если в начале FSM — nfs протокол
        if self.fsm.getState().getName() == "NFSPath.Start" and ch == 'n':
            self.fsm.n()
        elif self.fsm.getState().getName() == "NFSPath.Protocol_N" and ch == 'f':
            self.fsm.f()
        elif self.fsm.getState().getName() == "NFSPath.Protocol_F" and ch == 's':
            self.fsm.s()
        elif ch.isalpha():
            self.fsm.Letter(ch)
        elif ch.isdigit():
            self.fsm.Digit(ch)
        elif ch == ':':
            self.fsm.Colon()
        elif ch == '/':
            self.fsm.Slash()
        elif ch == '\0' or ch == '\n':
            self.fsm.EOS()
        else:
            self.fsm.Default()

    # Методы, вызываемые автоматом (действия из .sm)
    def addtobuf(self, x): self.buf += x
    def clearbuf(self): self.buf = ""
    def recordServerName(self): self.server = self.buf
    def recordFirstDir(self): pass
    def recorDirPath(self): pass
    def validatePath(self): self.accepted = True
    def clearallbuf(self): self.buf = ""
    def Accept(self): self.accepted = True
