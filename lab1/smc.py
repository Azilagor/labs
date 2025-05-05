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
        # Подставляем нужное событие в зависимости от символа
        if ch.isalpha():
            self.fsm.Letter(ch)
        elif ch == ':':
            self.fsm.Colon()
        elif ch == '/':
            self.fsm.Slash()
        elif ch == '\0':
            self.fsm.EOS()
        else:
            self.fsm.Default()

    # Методы, вызываемые автоматом (действия из .sm)
    def addtobuf(self, x): self.buf += x
    def clearbuf(self): self.buf = ""
    def recordServer(self): self.server = self.buf
    def clearallbuf(self): self.buf = ""
    def Accept(self): self.accepted = True
