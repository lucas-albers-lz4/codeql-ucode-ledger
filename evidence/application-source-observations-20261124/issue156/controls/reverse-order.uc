import { cursor } from 'uci';
const methods = {
  observe: {
    call: function(request) {
      let uci_ctx = cursor();
      switch (request) {
        case 'left': {
          system('/etc/init.d/fixture-service restart >/dev/null 2>&1');
          uci_ctx.commit('fixture-config'); }
        case 'right': { }
      }
    }
  }
};
return { 'luci.review.adjacency': methods };
