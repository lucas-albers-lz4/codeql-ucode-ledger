import MarkupCreationTestUtils
from MarkupCreationCFG::Node a, MarkupCreationCFG::Node b
where MarkupCreationCFG::edge(a, b) and file(a) = ["siblings.ut", "siblings-all-covered.ut"]
select file(a), scope(a), identity(a), file(b), scope(b), identity(b),
  count(MarkupCreationCFG::Node x, MarkupCreationCFG::Node y |
    MarkupCreationCFG::edge(x, y) and file(x) = file(a) and scope(x) = scope(a) and identity(x) = identity(a) and
    file(y) = file(b) and scope(y) = scope(b) and identity(y) = identity(b) | x, y)
