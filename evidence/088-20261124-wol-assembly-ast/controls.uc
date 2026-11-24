import { popen } from 'fs';

function shellquote(s) { return s; }
function other(s) { return s; }

const methods = {
  positive: {
    args: { name: 'string', args: [] },
    call: function(request) {
      if (request.args.name == '/usr/bin/etherwake') {
        let parts = map(request.args.args, shellquote);
        const fd = popen(request.args.name + ' ' + join(' ', parts));
        return fd;
      }
    }
  },
  fixed_args: {
    args: { name: 'string', args: [] },
    call: function(request) {
      let parts = map(['fixed'], shellquote);
      return popen(request.args.name + ' ' + join(' ', parts));
    }
  },
  other_callback: {
    args: { name: 'string', args: [] },
    call: function(request) {
      let parts = map(request.args.args, other);
      return popen(request.args.name + ' ' + join(' ', parts));
    }
  },
  no_join: {
    args: { name: 'string', args: [] },
    call: function(request) {
      let parts = map(request.args.args, shellquote);
      return popen(request.args.name + ' ' + parts);
    }
  }
};

return { probe: methods };
