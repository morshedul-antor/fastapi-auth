### create database name 'auth'
### create '.env' file

******** run command *********
# python3 -m venv env
# source env/bin/activate
# pip3 install -r requirements.txt
# cd src
# alembic upgrade head
# python3 main.py 

*********** add the following lines into .env ************
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/auth
URL_ONE=http://localhost:3000
URL_TWO=https://localhost:3000


******** run command for SECRET_KEY *********
# openssl rand -hex 32
# paste the key to SECRET_KEY

SECRET_KEY=d0edcf1fe0b762a3a3eaf06d49a396f175b29ce3ecd680c61e3a0f94292e206c
ALGORITHM=HS256

DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/auth
URL_ONE=http://localhost:3000
URL_TWO=https://localhost:3000