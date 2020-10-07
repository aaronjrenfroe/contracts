contracts framework based on David Beazley's 2017 PyCon Isreal talk

https://www.youtube.com/watch?v=js_0wjzuMfc

Modified to accept python's builtin class types

```python

from contract import Base, PositiveInteger

# global annotations
dx: PositiveInteger # Only need to import annotation if used outside of class inheriting from base class

class Player(Base):
  name: NonemptyString
  x: int
  y: int
  
  def __init__(self, name, x, y): # <- Method annotations work here too!
    self.name = name
    self.x = x
    self.y = y
   
  def right(self, dx):
    self.x += dx
  
  def left(self, dx):
    self.x -= dx
    
  # method annotations
  def up(self, dy: PositiveInteger): 
    self.y += dy

  def down(self, dy: NegitiveInteger):
    self.y += dy

```

```
>>> p = Player('', 0, 0)
...
AssertionError: Must be nonempty

>>> p = Player('Guido', 0.0, 0)
...
AssertionError: Expected <class 'int'>

>>> p = Player('Guido', 0, -1)
>>> p.left(-1)
...
AssertionError: Must be > 0

>>> p.right(1.0)
...
AssertionError: Expected <class 'int'>

>>> p.left(-0.5)
...
AssertionError: Expected <class 'int'>
```
