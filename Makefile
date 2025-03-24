# Setup the project by installing packages, and
install:
	@pip install -r requirements.txt
train_and_save_model:
	python setup.py
# Run locally the front-end and the API
develop:
	make -j 2 run_api run_frontend

run_api:
	fastapi run api/main.py
run_frontend:
	streamlit run interface/frontend.py
