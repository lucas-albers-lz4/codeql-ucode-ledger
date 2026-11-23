import MarkupCreationTestUtils
from MarkupCreationCFG::Node a, MarkupCreationCFG::Node b
where MarkupCreationCFG::edge(a, b) and file(a) = ["siblings.ut", "siblings-all-covered.ut", "siblings-computed-callee.ut"]
select file(a), scope(a), identity(a), file(b), scope(b), identity(b), 1
