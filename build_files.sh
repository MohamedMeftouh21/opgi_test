# build_files.sh
pip install -r requirements.txt
python3.10.4 manage.py collectstatic
