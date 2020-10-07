# contract.py
# Framework for enforcing assertions

_contracts = {}
bob = 22

class Contract:

  @classmethod
  def __init_subclass__(cls):
    _contracts[cls.__name__] = cls
  
  # own the "dot" (Descriptor protocol)
  def __set__(self, instance, value):
    self.check(value)
    instance.__dict__[self.name] = value

  # python 3.6+ feature
  def __set_name__(self, cls, name):
    self.name = name

  @classmethod
  def check(cls, value):
    pass


class Typed(Contract):
  type = None
  @classmethod
  def check(cls, value):
    assert isinstance(value, cls.type), f'Expected {cls.type}'
    super().check(value)



class Integer(Typed):
  type = int

class String(Typed):
  type = str

class Float(Typed):
  type = float

class Negitive(Contract):

  @classmethod
  def check(cls, value):
    assert value < 0, 'Must be < 0'
    super().check(value)

class Positive(Contract):
  @classmethod
  def check(cls, value):
    assert (value > 0), 'Must be > 0'
    super().check(value)

class Nonempty(Contract):
  @classmethod
  def check(cls, value):
    assert len(value) > 0, 'Must be nonempty'
    super().check(value)

# Call it "Composition"
class PositiveInteger(Positive, Integer):
  pass

class NonemptyString(Nonempty, String):
  pass

from functools import wraps
from inspect import signature

def checked(func):
  sig = signature(func)

  ann = ChainMap(
    func.__annotations__,
    func.__globals__.get('__annotations__', {})
  )

  @wraps(func)
  def wrapper(*args, **kwargs):
    bound = sig.bind(*args, **kwargs)
    for name, value in bound.arguments.items():
      if name in ann:
        ann[name].check(value)
    return func(*args, **kwargs)
  return wrapper

from collections import ChainMap

class BaseMeta(type):
  @classmethod
  def __prepare__(cls, *args):
    return ChainMap({ }, _contracts)
  
  def __new__(meta, name, bases, methods):
    methods = methods.maps[0]
    return super().__new__(meta, name, bases, methods)

class Base(metaclass=BaseMeta):
  # 3.6+
  @classmethod
  def __init_subclass__(cls):
    # Apply checked decorator
    for name, val in cls.__dict__.items():
      if callable(val):
        setattr(cls,name,checked(val))
    
    # Instantiate the contracts
    for name, val in cls.__annotations__.items():
      contract = val() # Integer()
      contract.__set_name__(cls, name)
      setattr(cls, name,contract)
   
  def __init__(self, *args):
    ann = self.__annotations__
    assert len(args) == len(ann), f'Expected {len(ann)} arguments'
    for name, val in zip(ann, args):
      satattr(self, name, val)
  
  def __repr__(self):
    args = ','.join([repr(getattr(self, name)) for name in self.__annotations__])
    return f'{type(self).__name__}({args})'
