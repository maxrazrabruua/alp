import os
import time

class Block:
    def __init__(self, code: 'Program', l: int):
        self.start = code.t + 1
        self.code = code
        self.code.ins(f"SET INT nib = {code.t + 2 + l}")
        self.code.ins("JUMP nib")
    
    def __call__(self):
        self.code.ram['callblock' + str(self.code.ram['stackNum'])] = self
        self.code.ram['stackNum'] += 1
        self.callback = self.code.t + 1
        self.code.ins(f"SET INT nib = {self.start}")
        self.code.ins("JUMP nib")
    
    def end(self):
        print('log:', self.callback)
        self.code.ram['stackNum'] -= 1
        self.code.ins(f"SET INT nib = {self.callback}")
        self.code.ins("JUMP nib")

class Program:
    def __init__(self):
        self.ram = {'end': '\n', 'stackNum': 0}
        self.code = ""
        self.t = 0
        self.i = False
        self.sinc = False
        self.timesleep = 0
        self.view = False
    
    def intpTypes(self, instruct: str):
        if len(instruct) == 0:
            return ''
        else:
            if instruct[0] == 's':
                return instruct[1:]
            elif instruct[0] == 'i':
                try:
                    return int(instruct[1:])
                except:
                    return 0
            elif instruct[0] == 'f':
                try:
                    return float(instruct[1:])
                except:
                    return float(int(instruct[1:]))
            elif instruct[0] == 'b':
                if instruct[1:] not in ['TRUE', 'FALSE']:
                    return False
                return True if instruct[1:] == 'TRUE' else False
            else:
                try:
                    return self.ram[instruct[1:]]
                except:
                    return ''
                
    
    def ins(self, string: str):
        if self.timesleep > time.time():
            self.t -= 1
            return
        
        if self.view:
            print('[LOGCODE]:', string)

        if len(string) == 0:
            return
        else:
            c = string.split(" ")
            if c[0] == "SET":
                if len(c) >= 5:
                    if c[3] == "=":
                        if c[1] == "STR":
                            name = c[2]
                            data = ' '.join(c[4:])
                            data = data.replace('\\n', '\n').replace('\\r', '\r')
                            self.ram[name] = data
                        elif c[1] == "INT":
                            if len(c) == 5:
                                try:
                                    name = c[2]
                                    data = int(c[4])
                                    self.ram[name] = data
                                except:
                                    print("[WARN]: Value is not number")
                        elif c[1] == "FLOAT":
                            if len(c) == 5:
                                try:
                                    name = c[2]
                                    try:
                                        data = float(c[4])
                                    except:
                                        data = float(int(c[4]))
                                    self.ram[name] = data
                                except:
                                    print("[WARN]: Value is not float number")
                        elif c[1] == "BOOL":
                            if len(c) == 5:
                                try:
                                    name = c[2]
                                    if c[4] not in ['TRUE', 'FALSE']:
                                        raise Exception('Не булевое значение')
                                    data = True if c[4] == 'TRUE' else False
                                    self.ram[name] = data
                                except:
                                    print("[WARN]: Value is not bool")
                        elif c[1] == "LIST":
                            if len(c) >= 5:
                                try:
                                    name = c[2]
                                    data = [self.intpTypes(i) for i in ' '.join(c[4:]).split('\\, ')]
                                    self.ram[name] = data
                                except:
                                    print("[WARN]: Value is not list")
                        elif c[1] == "VAR":
                            if len(c) == 5:
                                try:
                                    name = c[2]
                                    self.ram[name] = self.ram[c[4]]
                                except:
                                    print("[WARN]: Var not exist")
                                    
            elif c[0] == "PRINT":
                if len(c) == 2:
                    try:
                        print(self.ram[c[1]], end=self.ram['end'])
                    except:
                        print(f'[WARN]: var {c[1]} not exist')
                        
            elif c[0] == "JUMP":
                if len(c) == 2:
                    try:
                        self.t = self.ram[c[1]] - 1
                    except:
                        print(f'[WARN]: var {c[1]} not exist or not int')
            
            elif c[0] == "EXIT":
                if len(c) == 1:
                    self.i = True
            
            elif c[0] == "IF":
                if len(c) == 4:
                    try:
                        b = self.ram[c[1]]
                        m1 = self.ram[c[2]]
                        m2 = self.ram[c[3]]
                        if b:
                            self.t = m1 - 1
                        else:
                            self.t = m2 - 1
                    except Exception as e:
                        print("[WARN]: Error in If ... ... ...")
                        print(f"{e.__class__.__name__}: {str(e)}")
            
            elif c[0] == "CMP":
                if len(c) == 6:
                    if c[1] == "MATH":
                        if c[4] == "==":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[5]]
                                
                                self.ram[out] = var1 == var2
                            except:
                                print("[WARN]: Error in CMP MATH ... ... == ...")
                        elif c[4] == "!=":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[5]]
                                
                                self.ram[out] = var1 != var2
                            except:
                                print("[WARN]: Error in CMP MATH ... ... != ...")
                        elif c[4] == ">":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[5]]
                                
                                self.ram[out] = var1 > var2
                            except:
                                print("[WARN]: Error in CMP MATH ... ... > ...")
                        elif c[4] == ">=":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[5]]
                                
                                self.ram[out] = var1 >= var2
                            except:
                                print("[WARN]: Error in CMP MATH ... ... >= ...")
                        elif c[4] == "<=":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[5]]
                                
                                self.ram[out] = var1 <= var2
                            except:
                                print("[WARN]: Error in CMP MATH ... ... <= ...")
                        elif c[4] == "<":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[5]]
                                
                                self.ram[out] = var1 < var2
                            except:
                                print("[WARN]: Error in CMP MATH ... ... < ...")
                        elif c[4] == "is":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[5]]
                                
                                self.ram[out] = var1 is var2
                            except:
                                print("[WARN]: Error in CMP MATH ... ... is ...")
            
            elif c[0] == "MATH":
                if len(c) == 5:
                    if c[3] == "+":
                        try:
                            out = c[1]
                            var1 = self.ram[c[2]]
                            var2 = self.ram[c[4]]
                            
                            self.ram[out] = var1 + var2
                        except:
                            print("[WARN]: Error in MATH ... ... + ...")
                    elif c[3] == "-":
                        try:
                            out = c[1]
                            var1 = self.ram[c[2]]
                            var2 = self.ram[c[4]]
                            
                            self.ram[out] = var1 - var2
                        except:
                            print("[WARN]: Error in MATH ... ... - ...")
                    elif c[3] == "*":
                        try:
                            out = c[1]
                            var1 = self.ram[c[2]]
                            var2 = self.ram[c[4]]
                            
                            self.ram[out] = var1 * var2
                        except:
                            print("[WARN]: Error in MATH ... ... * ...")
                    elif c[3] == "/":
                        try:
                            out = c[1]
                            var1 = self.ram[c[2]]
                            var2 = self.ram[c[4]]
                            
                            self.ram[out] = var1 / var2
                        except:
                            print("[WARN]: Error in MATH ... ... / ...")
                    elif c[3] == "^":
                        try:
                            out = c[1]
                            var1 = self.ram[c[2]]
                            var2 = self.ram[c[4]]
                            
                            self.ram[out] = var1 ** var2
                        except:
                            print("[WARN]: Error in MATH ... ... ^ ...")
                    elif c[3] == "//":
                        try:
                            out = c[1]
                            var1 = self.ram[c[2]]
                            var2 = self.ram[c[4]]
                            
                            self.ram[out] = var1 // var2
                        except:
                            print("[WARN]: Error in MATH ... ... // ...")
                    else:
                        if c[1] == "GET":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[4]]
                                
                                self.ram[out] = var1[var2]
                            except:
                                print("[WARN]: Error in MATH GET ... ... ...")
                        elif c[1] == "EDIT":
                            try:
                                var1 = self.ram[c[2]]
                                var2 = self.ram[c[3]]
                                var3 = self.ram[c[4]]
                                
                                var1[var2] = var3
                            except:
                                print("[WARN]: Error in MATH EDIT ... ... ...")
                        elif c[1] == "SLICELEFT":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[4]]
                                
                                self.ram[out] = var1[var2:]
                            except:
                                print("[WARN]: Error in MATH SLICELEFT ... ... ...")
                        elif c[1] == "SLICERIGHT":
                            try:
                                out = c[2]
                                var1 = self.ram[c[3]]
                                var2 = self.ram[c[4]]
                                
                                self.ram[out] = var1[:var2]
                            except:
                                print("[WARN]: Error in MATH SLICERIGHT ... ... ...")

                elif len(c) == 4:
                    if c[1] == "LEN":
                        try:
                            out = c[2]
                            var1 = self.ram[c[3]]
                            
                            self.ram[out] = len(var1)
                        except Exception as e:
                            print("[WARN]: Error in MATH LEN ... ...")
                            # print(f"{e.__class__.__name__}: {str(e)}")
                    elif c[1] == "APPEND":
                        try:
                            out = c[1]
                            var1 = self.ram[c[2]]
                            var2 = self.ram[c[3]]
                            
                            var1.append(var2)
                        except:
                            print("[WARN]: Error in MATH APPEND ... ...")
                    elif c[1] == "REMOVE":
                        try:
                            out = c[1]
                            var1 = self.ram[c[2]]
                            var2 = self.ram[c[3]]
                            
                            var1.remove(var2)
                        except:
                            print("[WARN]: Error in MATH REMOVE ... ...")

            elif c[0] == "TYPE":
                if len(c) == 5:
                    if c[1] == "NEW":
                        try:
                            tab = {
                                'INT': int,
                                'FLOAT': float,
                                'STR': str,
                                'BOOL': bool
                            }

                            typestr = tab[c[2]]
                            var1 = self.ram[c[3]]
                            self.ram[c[4]] = typestr(var1)
                        except:
                            print("[WARN]: Error in TYPE NEW ... ... ...")
                    elif c[1] == "IS":
                        try:
                            tab = {
                                'INT': int,
                                'FLOAT': float,
                                'STR': str,
                                'BOOL': bool
                            }

                            typestr = tab[c[2]]
                            var1 = self.ram[c[3]]
                            self.ram[c[4]] = isinstance(var1, typestr)
                        except:
                            print("[WARN]: Error in TYPE IS ... ... ...")
            elif c[0] == "CLS":
                os.system("cls")
            elif c[0] == ";":
                pass
            elif c[0] == "PAUSE":
                if len(c) == 2:
                    try:
                        interval = self.ram[c[1]]
                        start = time.time()
                        while start + interval > time.time():
                            pass
                    except:
                        print("[WARN]: PAUSE ...")
            elif c[0] == "ASP":
                if len(c) == 2:
                    try:
                        interval = self.ram[c[1]]
                        start = time.time()
                        self.timesleep = start + interval
                    except:
                        print("[WARN]: ASP ...")
            elif c[0] == "BLOCK":
                if len(c) == 3:
                    try:
                        l = int(c[2])
                        name = c[1]
                        self.ram[name] = Block(self, l)
                    except:
                        print("[WARN]: BLOCK ... INT")
            elif c[0] == "GOTO":
                if len(c) == 2:
                    try:
                        name = c[1]
                        self.ram[name]()
                    except:
                        print("[WARN]: GOTO ...")
            elif c[0] == "END":
                if len(c) == 1:
                    try:
                        self.ram['callblock' + str(self.ram['stackNum'] - 1)].end()
                    except:
                        print("[WARN]: Block not declared")
    
    def run(self):
        self.i = False
        self.sinc = True
        while not self.i:
            self.go()
        self.sinc = False
        if self.view:
            print('ram:', self.ram)
    
    def go(self):
        a = self.code.split("\n")
        if len(a) == 0:
            return
        
        if len(a) == self.t:
            self.t = 0
            self.i = True
            if self.sinc:
                return
        
        self.ins(a[self.t])
        self.t += 1
        
program = Program()

with open('mycode.alp', 'r', encoding='utf-8') as f:
    program.code = f.read()

program.view = True
program.run()

while True: pass
