class TextReader:
    def __init__(self):
        self.account_file = 'accounts.txt'
        self.proxies_file = 'proxies.txt'
        self.paid_proxies_file = 'paid_proxies.txt'

    def get_accounts(self):
        with open(self.account_file, 'r') as file:
            accounts = file.readlines()
            accounts = [i.strip().replace('/', '').split('	') for i in accounts]

            return accounts

    def get_proxies(self):
        with open(self.proxies_file, 'r') as file:
            proxies = file.readlines()
            proxies = [i.strip().split() for i in proxies]

            return proxies

    def get_paid_proxies(self):
        with open(self.paid_proxies_file, 'r') as file:
            proxies = file.readlines()
            proxies = [i.strip().split() for i in proxies]

            return proxies

