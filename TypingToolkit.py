class TypingBase:
    def TypeIF(self, target) -> bool:
        pass
    def TypeCheck(self, Target: object, Type: object, SubClass: bool = False) -> bool:
        if SubClass:
            return isinstance(Target, Type)
        return Target.__class__ == Type
    def ClassCheck(self, Type: object) -> bool:
        if isinstance(Type, type):
            return True
        else:
            return False

class _Any(TypingBase):
    def TypeIF(self, target) -> bool:
        return True

Any = _Any()

class Union(TypingBase):
    def __init__(self, *Types: object):
        self.Types = set(Types)
        
    def TypeIF(self, target) -> bool:
        for Type in self.Types:
            if self.TypeCheck(Type, TypingBase, True):
                if Type.TypeIF(target):
                    return True
            elif self.TypeCheck(target, Type):
                return True
        return False

class Optional(TypingBase):
    def __init__(self, Type):
        self.Type = Type
        
    def TypeIF(self, target) -> bool:
        if target is None:
            return True
        elif self.TypeCheck(self.Type, TypingBase, True):
            return self.Type.TypeIF(target)
        else:
            return self.TypeCheck(target, self.Type)

class Literal(TypingBase):
    def __init__(self, *Literals):
        self.Literals = set(Literals)
        
    def TypeIF(self, target) -> bool:
        return target in self.Literals

class List(TypingBase):
    def __init__(self, Type):
        self.Type = Type
        
    def TypeIF(self, target) -> bool:
        if not self.TypeCheck(target, list):
            return False
        for item in target:
            if self.TypeCheck(self.Type, TypingBase, True):
                if not self.Type.TypeIF(item):
                    return False
            elif not self.TypeCheck(item, self.Type):
                return False
        return True

class Dict(TypingBase):
    def __init__(self, KeyType, ValueType):
        self.KeyType = KeyType
        self.ValueType = ValueType
        
    def TypeIF(self, target) -> bool:
        if not self.TypeCheck(target, dict):
            return False
        for key, value in target.items():
            if self.TypeCheck(self.KeyType, TypingBase, True):
                if not self.KeyType.TypeIF(key):
                    return False
            elif not self.TypeCheck(key, self.KeyType):
                return False
            if self.TypeCheck(self.ValueType, TypingBase, True):
                if not self.ValueType.TypeIF(value):
                    return False
            elif not self.TypeCheck(value, self.ValueType):
                return False
        return True

class Tuple(TypingBase):
    def __init__(self, Type):
        self.Type = Type
        
    def TypeIF(self, target) -> bool:
        if not self.TypeCheck(target, tuple):
            return False
        for item in target:
            if self.TypeCheck(self.Type, TypingBase, True):
                if not self.Type.TypeIF(item):
                    return False
            elif not self.TypeCheck(item, self.Type):
                return False
        return True

class Set(TypingBase):
    def __init__(self, Type):
        self.Type = Type
        
    def TypeIF(self, target) -> bool:
        if not self.TypeCheck(target, set):
            return False
        for item in target:
            if self.TypeCheck(self.Type, TypingBase, True):
                if not self.Type.TypeIF(item):
                    return False
            elif not self.TypeCheck(item, self.Type):
                return False
        return True

class Type(TypingBase):
    def __init__(self, Class):
        if self.ClassCheck(Class):
            self.Class = Class
        else:
            raise ValueError("'Class' argument must be a class, not an instance.")
        
    def TypeIF(self, target: object) -> bool:
        return (self.Class == target) and self.ClassCheck(target)
