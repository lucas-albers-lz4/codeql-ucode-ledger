import { cursor } from 'uci';
const methods = {
  observe: {
    call: function(request) {
      let uci_ctx = cursor();
      uci_ctx = { commit: function(package_name) { return null; } };
      switch (request) {
        case 'left': {
          uci_ctx.commit('fixture-config');
          system('/etc/init.d/fixture-service restart >/dev/null 2>&1'); }
        case 'right': { }
      }
    }
  }
};
return { 'luci.review.adjacency': methods };
