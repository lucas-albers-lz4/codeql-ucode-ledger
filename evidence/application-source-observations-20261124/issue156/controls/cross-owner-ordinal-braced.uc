import { cursor } from 'uci';
const methods = {
  observe: {
    call: function(request) {
      let uci_ctx = cursor();
      switch (request) {
        case 'outer': {
          {
            uci_ctx.commit('fixture-config'); }
          system('/etc/init.d/fixture-service restart >/dev/null 2>&1'); }
        case 'other': { }
      }
    }
  }
};
return { 'luci.review.adjacency': methods };
