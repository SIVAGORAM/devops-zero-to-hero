from devops.system import get_system_info

def test_system_info():
    result = get_system_info()
    assert isinstance(result, dict)
    assert 'OS' in result
