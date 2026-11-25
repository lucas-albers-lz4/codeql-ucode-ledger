function pick(s) { return s; }
function probe() {
  {
    function pick(s) { return 'inner'; }
    print(pick);
  }
  {
    print(pick);
  }
}
