# Activate the virtual environment
.\venv\Scripts\activate

# install packages
pip install -r requirements.txt

# update requirement.txt
pip freeze > requirements.txt

# leave virtual environment
deactivate