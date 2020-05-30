import requests
from urllib.parse import urlencode
from .log import logger


class RestAPI:

    def __init__(self, endpoint, api_token, user_agent, timeout=60):
        self.endpoint = endpoint
        self.timeout = timeout
        self.headers = {
            'Authorization': 'Bearer {}'.format(api_token),
            'Content-type': 'application/json',
            'User-Agent': user_agent,
        }

    def _return_result(self, r):
        logger.info(f"HTTP status code {r.status_code}")
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

        logger.info(f"HTTP payload: {data}")
        return data

    def get_resources(self, resource, payload=None, resource_id=None):
        query_url = self.endpoint + '/' + resource
        if resource_id:
            query_url = query_url + '/' + resource_id

        if payload:
            for k, v in payload.items():
                if v is not None:
                    data = urlencode({k: v})
                else:
                    data = k
                break

            query_url = query_url + '?' + data

        logger.info(f"HTTP GET to {query_url}")

        r = requests.get(query_url, headers=self.headers, timeout=self.timeout)
        return self._return_result(r)

    def post_patch_resource(self, resource, payload=None, resource_id=None, action=None):
        data = self._handle_payload(payload)
        query_url = self.endpoint + '/' + resource

        if not resource_id:
            logger.info(f"HTTP POST to {query_url}")
            r = requests.post(query_url, json=data, headers=self.headers, timeout=self.timeout)
            return self._return_result(r)

        query_url += '/' + resource_id
        if action:
            query_url += '/' + action
            logger.info(f"HTTP POST to {query_url}")
            r = requests.post(query_url, json=data, headers=self.headers, timeout=self.timeout)
            return self._return_result(r)
        else:
            logger.info(f"HTTP PATCH to {query_url}")
            r = requests.patch(query_url, json=data, headers=self.headers, timeout=self.timeout)
            return self._return_result(r)

    def delete_resource(self, resource, resource_id):
        query_url = self.endpoint + '/' + resource + '/' + resource_id
        logger.info(f"HTTP DELETE to {query_url}")
        r = requests.delete(query_url, headers=self.headers, timeout=self.timeout)
        return self._return_result(r)
