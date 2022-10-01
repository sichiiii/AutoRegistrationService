class ProxyManager:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.proxy_index = 0
        self.proxy = self.proxy_list[self.proxy_index]

    def get_proxy(self):
        return self.proxy

    def next_proxy(self):
        self.proxy_index += 1
        if self.proxy_index >= len(self.proxy_list):
            self.proxy_index = 0
        self.proxy = self.proxy_list[self.proxy_index]

    def reset_proxy(self):
        self.proxy_index = 0
        self.proxy = self.proxy_list[self.proxy_index]