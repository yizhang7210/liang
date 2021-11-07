# Publish to PyPI

``` shell script
pipenv install  # install packages
pipenv shell  # To get into the shell
python setup.py sdist bdist_wheel  # build packages
twine check dist/*  # to check the artifacts
twine upload --repository-url https://test.pypi.org/legacy/ dist/*  # upload to test PyPI
twine upload dist/*  # upload to actual PyPI
```
