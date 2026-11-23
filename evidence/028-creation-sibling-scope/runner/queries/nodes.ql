import MarkupCreationTestUtils
from MarkupCreationCFG::Node n
where file(n) = ["siblings.ut", "siblings-all-covered.ut"]
select file(n), scope(n), n.getRole(), identity(n),
 count(MarkupCreationCFG::Node x | file(x) = file(n) and scope(x) = scope(n) and x.getRole() = n.getRole() and identity(x) = identity(n) | x)
