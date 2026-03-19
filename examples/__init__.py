from typing import List, Set, Tuple

from utils import normalize_type

foo = List[int]

t = normalize_type(foo)

print(f'было: {foo}')
print(f'стало: {t}')
