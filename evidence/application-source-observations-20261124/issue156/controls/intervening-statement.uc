import { cursor } from 'uci';
const methods = {
  observe: {
    call: function(request) {
      let uci_ctx = cursor();
      switch (request) {
        case 'left': {
          uci_ctx.commit('fixture-config');
          let marker = 0;
          system('/etc/init.d/fixture-service restart >/dev/null 2>&1'); }
        case 'right': { }
      }
    }
  }
};
return { 'luci.review.adjacency': methods };
