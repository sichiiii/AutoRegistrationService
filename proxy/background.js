function startProxy() {
        var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: 	"<host>",		// Proxy IP or URL: type -> string
                port: 	<port>		// Proxy port : type -> int
            },
            bypassList: ["localhost"]
            }
        };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        }
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "<username>",
                    password: "<password>"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        startProxy();
                