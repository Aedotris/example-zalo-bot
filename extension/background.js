// background script
function captureRequests() {
	chrome.webRequest.onBeforeRequest.addListener(
	function(details) {
		var url = details.url;
		var imeiFound = false;
		var imeiValue = 'Not Found';
		
		// check if IMEI param is present in the URL
		if (url.includes('/api/login/getServerInfo') && url.indexOf('imei=') > -1) {
			params = new URLSearchParams(new URL(url).search);
			imeiFound = true;
			imeiValue = params.get('imei'); //url.split('imei=')[1].split('&')[0];
			chrome.runtime.sendMessage({ action: 'IMEIValue', imei: imeiValue });
			let options = {
				type: 'basic',
				title: 'IMEI Found',
				message: 'Successfully get IMEI',
				iconUrl: '/images/success.png'
			};
			
			chrome.notifications.create(options);
		}
		
		// if IMEI is found and URL is chat.zalo.me, get cookies
		if (imeiFound && url.includes('chat.zalo.me')) {
			chrome.cookies.getAll({ url: url }, function(cookies) {
				// var cookieString = '';
				var cookiesDict = {};
				
				for (var i = 0; i < cookies.length; i++) {
					cookiesDict[cookies[i].name] = cookies[i].value;
					// cookieString += cookies[i].name + '=' + cookies[i].value + '; ';
				}
				chrome.runtime.sendMessage({ action: 'CookiesValue', cookies: JSON.stringify(cookiesDict) });
				let options = {
					type: 'basic',
					title: 'Cookies Found',
					message: 'Successfully get Cookies',
					iconUrl: '/images/success.png'
				};
				
				chrome.notifications.create(options);
			});
		}
	},
	{ urls: ["<all_urls>"] },
	["requestBody"]
	);
}

captureRequests();