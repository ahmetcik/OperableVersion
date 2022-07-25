# OperableVersion
Class to make a variables of type version (e.g. '1.2.1') comparable with each other (e.g. using '>=') as well as allow arithmetic operations (e.g. '+') on them. For example, we want that '1.4.' < '2.1.2.7' = True, and '1.4 + '2.1.2.7' = '3.5.2.7', where '+' was applied elementwise.


```py
from version_operable import VersionOperable

x = VersionOperable('7.2')
y = '4.1.2.4'

print(x + y)
# 11.3.2.4

print(x >= y)
# True
```
