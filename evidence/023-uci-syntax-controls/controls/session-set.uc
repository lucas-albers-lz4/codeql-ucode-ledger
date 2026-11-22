function probe(ubus) {
	return ubus.call('session', 'set', {});
}
