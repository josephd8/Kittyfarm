.PHONY: test app venv clean clean-pyc clean-env clean-tests trained-model features


pennylane-env/bin/activate: requirements.txt
	test -d pennylane-env || virtualenv pennylane-env
	. pennylane-env/bin/activate; pip install -r requirements.txt
	touch pennylane-env/bin/activate

venv: pennylane-env/bin/activate

data/features/example-features.csv: data/sample/music_data_combined.csv src/generate_features.py
	python run.py generate_features --config=config/test_model_config.yml --input=data/sample/music_data_combined.csv --output=data/features/example-features.csv

features: data/features/example-features.csv

models/example-model.pkl: data/features/example-features.csv src/train_model.py
	python run.py train_model --config=config/test_model_config.yml --input=data/features/example-features.csv --output=models/example-model.pkl

trained-model: models/example-model.pkl

app:
	python run.py app

swagger: app/app.py
	python run.py swagger

test:
	python run.py test

	py.test

clean-tests:
	rm -rf .pytest_cache
	rm -r test/model/test/
	mkdir test/model/test
	touch test/model/test/.gitkeep

clean-env:
	rm -r pennylane-env

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf .pytest_cache

clean: clean-tests clean-env clean-pyc