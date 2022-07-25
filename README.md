# OperableVersion
A module to make variables of type version (e.g. '1.2.1') comparable with each other (e.g. using '>=') as well as allow arithmetic operations (e.g. '+') on them. For example:

```py
from version_operable import VersionOperable

x = VersionOperable('7.2')
y = '4.1.2.4'

print(x + y)
# 11.3.2.4

print(x >= y)
# True
```

The module can further be extended for individual purpose. Not that it is not optimized with respect to performance. 
