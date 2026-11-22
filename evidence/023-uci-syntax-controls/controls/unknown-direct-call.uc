function probe(ubus) {
	return ubus.call('vendor_unknown', 'method_unknown', {});
}
