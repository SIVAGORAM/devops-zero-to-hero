import requests

def health_check(url, timeout=10):
    try:
        res = requests.get(url, timeout=timeout)
        return {'status_code': res.status_code, 'healthy': res.ok}
    except requests.RequestException as e:
        return {'status_code': None, 'healthy': False, 'error': str(e)}
