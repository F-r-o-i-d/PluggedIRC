import socket
import sys
import os
import Message

class ModuleHandler:
    def __init__(self) -> None:
        self.modules = {}
    
    def LoadAllModules(self):
        for file in os.listdir("Modules"):
            if file.endswith(".py"):
                self.LoadModule(file)
    
    def LoadModule(self, module):
        if module in self.modules:
            return
        
        sys.path.append("Modules")
        module = module.replace(".py", "")
        self.modules[module] = __import__(module)

    def UnloadModule(self, module):
        if module not in self.modules:
            return
        del self.modules[module]

    def InitModules(self):
        for module in self.modules:
            self.modules[module].init()

    def GetNumModules(self):
        return len(self.modules)

    def messageEvent(self, message):
        for module in self.modules:
            self.modules[module].messageEvent(message)

    