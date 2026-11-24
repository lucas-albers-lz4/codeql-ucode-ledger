/**
 * @name WOL assembly AST entities
 * @description Testing-only syntactic witness for map, join and imported popen.
 * @kind table
 * @id ucode/testing/wol-assembly-ast
 */

import codeql.ucode.m3.Models

from RequestArgsAccess src, NamedCall mapCall, UCODE::VariableDeclarator partsDecl,
     UCODE::Identifier callback, UCODE::Identifier partsUse, NamedCall joinCall,
     UCODE::BinaryExpression assembly, NamedFsPopenCall sink,
     UCODE::FunctionDeclaration callbackDecl
where
  src.getProperty().getValue() = "args" and
  mapCall.getName() = "map" and
  mapCall.getArgument(0) = src and
  callback = mapCall.getArgument(1) and callback.getValue() = "shellquote" and
  partsDecl.getName().getValue() = "parts" and partsDecl.getValue() = mapCall and
  joinCall.getName() = "join" and
  partsUse = joinCall.getArgument(1) and partsUse.getValue() = "parts" and
  assembly.getOperator() = "+" and assembly.getRight() = joinCall and
  assembly = sink.getArgument(0) and
  callbackDecl.getName().getValue() = "shellquote" and
  callbackDecl.getLocation().getFile() = src.getLocation().getFile() and
  sameRpcMethod(src, sink) and sameRpcMethod(mapCall, joinCall) and
  src.getLocation().getFile().getRelativePath() in
    ["usr/share/rpcd/ucode/luci.wol", "usr/share/rpcd/ucode/controls.uc"]
select src, callbackDecl, callback, mapCall, partsDecl, partsUse, joinCall,
  assembly, sink,
  src.getLocation().getFile().getRelativePath(),
  src.getLocation().getStartLine(), sink.getLocation().getStartLine()
