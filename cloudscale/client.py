import requests
from urllib.parse import urlencode

class RestAPI:

    def __init__(self, endpoint, api_token):
        self.endpoint = endpoint
        self.headers = {
            'Authorization': 'Bearer %s' % api_token,
            'Content-type': 'application/json',
        }

    def _return_result(self, r):
        result = {
            'status_code': r.status_code,
        }

        try:
            result['data'] = r.json()
        except ValueError:
            result['data'] = None
        return result

    def _handle_payload(self, payload):
        if not payload:
            return

        data = dict()
        for k, v in payload.items():
            if v is not None:
                data[k] = v
        return data

    def get_resources(self, resource, payload, resource_id=None):
        if not resource:
            return {}

        query_url = self.endpoint + '/' + resource
        if resource_id:
            query_url = query_url + '/' + resource_id

        # TODO: make this less ugly
        if payload:
            for k, v in payload.items():
                if v is not None:
                    data = "%s=%s" % (k, urlencode(v))
                else:
                    data = k
                break

            query_url = query_url + '?' + data

        r = requests.get(query_url, headers=self.headers)
        return self._return_result(r)

    def post_patch_resource(self, resource, payload=None, resource_id=None, action=None):
        data = self._handle_payload(payload)
        query_url = self.endpoint + '/' + resource

        # TODO: undecided yet, whether this is the best way we should distinquish between post or patch method or not.
        if resource_id:
            query_url += '/' + resource_id
            if action:
                query_url += '/' + action
                r = requests.post(query_url, json=data, headers=self.headers)
                return self._return_result(r)

            r = requests.post(query_url, json=data, headers=self.headers)
            return self._return_result(r)
        else:
            r = requests.post(query_url, json=data, headers=self.headers)
            return self._return_result(r)

    def delete_resource(self, resource, resource_id):
        query_url = self.endpoint + '/' + resource + '/' + resource_id
        r = requests.delete(query_url, headers=self.headers)
        return self._return_result(r)
