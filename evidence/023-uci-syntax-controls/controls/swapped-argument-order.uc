function probe(ubus_call) {
	return ubus_call('commit', 'uci', {});
}
