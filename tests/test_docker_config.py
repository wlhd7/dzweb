import os
import re

def test_dockerfile_exists():
    assert os.path.exists('Dockerfile')

def test_dockerfile_content():
    with open('Dockerfile', 'r') as f:
        content = f.read()
    assert 'FROM python:3.12-slim' in content
    assert 'WORKDIR /app' in content
    assert 'COPY requirements.txt .' in content
    assert 'pip install' in content
