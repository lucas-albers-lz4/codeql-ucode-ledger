import { popen } from 'fs';

function shellquote(value) {
	return value;
}

const methods = {
	raw: {
		args: { switch: 'switch0' },
		call: function(request) {
			const fd = popen(`swconfig dev ${request.args.switch} help 2>/dev/null`);
			return { value: fd?.read?.('all') };
		}
	},
	quoted_other: {
		args: { other: 'switch0' },
		call: function(request) {
			const fd = popen(`swconfig dev ${shellquote(request.args.other)} help 2>/dev/null`);
			return { value: fd?.read?.('all') };
		}
	}
};

return { probe: methods };
