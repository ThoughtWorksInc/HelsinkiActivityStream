pip install -q -r requirements.txt
pip install -q -r requirements_for_tests.txt
./venv/bin/nosetests && ./venv/bin/pep8 --exclude=tests/data openahjo_activity_streams tests
