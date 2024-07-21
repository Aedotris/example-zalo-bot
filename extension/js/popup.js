chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.action === 'IMEIValue') {
		document.getElementById('imei-div').classList.remove('is-disabled');
		document.getElementById('imei-input').value = request.imei;
	
	} else if (request.action === 'CookiesValue') {
		document.getElementById('cookies-div').classList.remove('is-disabled');
		document.getElementById('cookies-input').value = request.cookies;
	
	}
});