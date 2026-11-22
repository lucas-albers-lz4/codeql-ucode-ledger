function ubus_call(object, method, args) {
	return logger(object, method, args);
}

function probe() {
	return ubus_call('uci', 'commit', {});
}
