# from NFSPathParser_sm import NFSParser

# class FSMWrapper:
#     def __init__(self):
#         self.buf = ""
#         self.server = None
#         self.accepted = False

#         self.fsm = NFSParser(self)
#         self.fsm.enterStartState()

#     def input(self, ch):
#         method = getattr(self.fsm, f"{ch}" if ch.isalpha() else {
#             ':': 'Colon', '/': 'Slash', '\0': 'EOS'
#         }.get(ch, 'Default'), None)

#         if method:
#             method()
#         else:
#             self.Default()

#     # FSM callbacks
#     def addtobuf(self, x): self.buf += x
#     def clearbuf(self): self.buf = ""
#     def recordServer(self): self.server = self.buf
#     def clearallbuf(self): self.buf = ""
#     def nil(self): self.accepted = True


def method_smc(line: str):
    # fsm = FSMWrapper()
    # try:
    #     path = line.strip()
    #     if not path.startswith("nfs://"):
    #         return False, None

    #     for ch in path:
    #         fsm.input(ch)
    #     fsm.input('\0')  # конец строки

    # except Exception:
    #     return False, None

    return print("smc!")
# fsm.accepted and fsm.server is not None, fsm.server
