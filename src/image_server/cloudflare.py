import json
import requests
from urlparse import urljoin


class CloudFlareBase(object):
    endpoint = 'https://api.cloudflare.com/client/v4/'

    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key

    def get_header(self, headers):
        """

        Args:
            headers(dict):

        Returns:
            dict

        """
        header = {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        if isinstance(headers, dict):
            header.update(headers)
        return header


class CloudFlare(CloudFlareBase):
    def user_detail(self, header=None):
        url = urljoin(self.endpoint, 'user')
        headers = self.get_header(header)
        return requests.get(url, headers=headers)

    def zone_list(self, header=None):
        url = urljoin(self.endpoint, 'zones')
        headers = self.get_header(header)
        return requests.get(url, headers=headers)

    def get_zone_id(self, zone_name):
        content = json.loads(self.zone_list().content)
        zone = list(filter(
            lambda _zone: _zone['name'] == zone_name,
            content['result'])
        )[0]
        return zone['id']

    def zone_detail(self, zone_name, header=None):
        zone_id = self.get_zone_id(zone_name)
        url = urljoin(self.endpoint, 'zones/{}'.format(zone_id))
        headers = self.get_header(header)
        return requests.get(url, headers=headers)

    def purge_individual_files(self, zone_name, files, header=None):
        zone_id = self.get_zone_id(zone_name)
        url = urljoin(self.endpoint, 'zones/{}/purge_cache'.format(zone_id))
        headers = self.get_header(header)
        data = {'files': files}
        return requests.delete(url, json=data, headers=headers)


if __name__ == '__main__':
    from pprint import pprint

    print("*" * 20, 'start', '*' * 20)
    AUTH_EMAIL = 'chenzhigao@mingdabeta.com'
    AUTH_KEY = '5429536daa4802c477d8affe1b6ff0a8d7e1a'
    cf = CloudFlare(AUTH_EMAIL, AUTH_KEY)
    print("-" * 20, "user detail", "-" * 20)
    r = cf.user_detail()
    pprint(json.loads(r.content))
    # print("-"*20, "zone list", "-"*20)
    # r = cf.zone_list()
    # pprint(json.loads(r.content))
    # print("-"*20, "zone detail", "-"*20)
    # r = cf.zone_detail(zone_name='avarsha.com')
    # pprint(json.loads(r.content))
    print("-" * 20, "zone id", "-" * 20)
    r = cf.get_zone_id(zone_name='avarsha.com')
    print(r)
    print("-" * 20, "zone id", "-" * 20)
    r = cf.purge_individual_files(zone_name='avarsha.com',
                                  files=['http://www.avarshacdn.com/s5Rqd'
                                         'oPxIymf7h-bsz_UGJEdM9k=/0x100/l'
                                         'ogos/vistaprint.png', ])
    pprint(json.loads(r.content))
    print("*" * 20, 'end', "*" * 20)
