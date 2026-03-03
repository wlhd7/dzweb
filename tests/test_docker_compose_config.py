import os
import yaml

def test_docker_compose_exists():
    assert os.path.exists('docker-compose.yml')

def test_docker_compose_content():
    with open('docker-compose.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    assert 'services' in config
    assert 'web' in config['services']
    web = config['services']['web']
    assert 'build' in web
    assert 'volumes' in web
    assert 'environment' in web
    envs = [e.split('=')[0] for e in web['environment']]
    assert 'FLASK_DEBUG' in envs
