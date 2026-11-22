function probe(api) {
	const saved = api.ubus_call;
	return saved;
}
