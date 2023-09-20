def pytest_configure(config):
    config.addinivalue_line(
        "markers", "import_matplotlib: For when matplotlib is involved."
    )
