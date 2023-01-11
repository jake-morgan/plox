lint:
	$(info Formatting with Black)
	python -m black --target-version py311 ./plox/
	@echo ""

	$(info Sorting imports with isort)
	python -m isort --profile black ./plox/
	@echo ""

	$(info Linting with pylint)
	python -m pylint --exit-zero ./plox/
	@echo ""

	$(info Security scanning with Bandit)
	python -m bandit ./plox/
	@echo ""
