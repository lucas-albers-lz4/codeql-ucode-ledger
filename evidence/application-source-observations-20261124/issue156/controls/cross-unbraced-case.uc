import { cursor } from 'uci';
const methods = {
  observe: {
    call: function(request) {
      let uci_ctx = cursor();
      switch (request) {
        case 'left':
          uci_ctx.commit('fixture-config'); case 'right':
          system('/etc/init.d/fixture-service restart >/dev/null 2>&1');
          return null;
      }
    }
  }
};
return { 'luci.review.adjacency': methods };
