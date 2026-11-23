"""Source-derived oracle; independent of database and query outputs."""
def expected():
 roots=[]; scopes=[]; nodes=[]; edges=[]; ast=[]
 for file,covered in [('siblings.ut',False),('siblings-all-covered.ut',True)]:
  end='68' if covered else '65'; second_end='67' if covered else '64'
  roots.append([file,'1','1','1',end,'unsupported','top-observed','1'])
  scopes.extend([[file,'1','10','1','34','covered','1'],[file,'1','43','1',second_end,'covered' if covered else 'unsupported','1']])
  top=[('object-identifier','Identifier:1:4:1:4:MemberExpression:0'),('member-reference','MemberExpression:1:4:1:6:AssignmentExpression:0'),('function-creation','FunctionExpression:1:10:1:34:AssignmentExpression:2'),('assignment-completion','AssignmentExpression:1:4:1:34:ExpressionStatement:0'),('statement-completion','ExpressionStatement:1:4:1:35:Markup:1'),('object-identifier','Identifier:1:37:1:37:MemberExpression:0'),('member-reference','MemberExpression:1:37:1:39:AssignmentExpression:0'),('function-creation',f'FunctionExpression:1:43:1:{second_end}:AssignmentExpression:2'),('assignment-completion',f'AssignmentExpression:1:37:1:{second_end}:ExpressionStatement:0'),('statement-completion',f'ExpressionStatement:1:37:1:{end}:Markup:2')]
  def sequence(scope,seq):
   nodes.extend([[file,scope,role,identity,'1'] for role,identity in seq]); edges.extend([[file,scope,a[1],file,scope,b[1],'1'] for a,b in zip(seq,seq[1:])])
  sequence('top',top)
  sequence('callable:1:10',[('entry','entry'),('initializer','Number:1:31:1:31:VariableDeclarator:2'),('declaration-completion','LexicalDeclaration:1:23:1:32:StatementBlock:1'),('exit','exit')])
  if covered: sequence('callable:1:43',[('entry','entry'),('initializer','Number:1:64:1:64:VariableDeclarator:2'),('declaration-completion','LexicalDeclaration:1:56:1:65:StatementBlock:1'),('exit','exit')])
  ast.append([file,'VariableDeclarator','1','27','1','31','LexicalDeclaration','1','1'])
  if covered: ast.append([file,'VariableDeclarator','1','60','1','64','LexicalDeclaration','1','1'])
  else: ast.extend([[file,'CallExpression','1','56','1','61','ExpressionStatement','0','1'],[file,'ExpressionStatement','1','56','1','62','StatementBlock','1','1']])
 return {'roots':roots,'scopes':scopes,'nodes':nodes,'edges':edges,'ast_selected':ast}
