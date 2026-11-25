function target(s) { return s; }
function probe() {
  function mutate() { target = function(s) { return 'fixed'; }; }
  print(target);
}
