from setuptools import setup

setup(
      name = 'testing',
      version = '1.1',
      include_package_data = True,
      author = "Isaac Naylor",
      include_dirs = ["src"],
      packages = [
            "Testing"
      ],
      package_data = {
            'Testing': ['py.typed']
      }
)