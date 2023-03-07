# Flask RestAPI PostgreSQL

Sample Project of building RESTFul API's using **Python**.
**PostgreSQL** has been used as Database.
Whole Code can be deployed in **Heroku**.

Code has the following things:
1. _**Data Models**_
2. _**Resources**_
3. _**SQL Queries of Table Creation**_
4. _**All Resources needed for Heroku Deployment.**_
5. **_Requirements_**

EndPoints are of following Categories:
1. _**Users**_
2. _**Genre**_
3. _**Artists**_
4. _**Albums**_
5. _**Tracks**_
6. _**Media Types**_
7. _**Playlist**_

## Instructions:

### Create and Run Database:
It is postgreSQL Database, so local database can be set up, by using [following link.](https://www.prisma.io/dataguide/postgresql/setting-up-a-local-postgresql-database)

Once database is set up, you need to run queries from ```SQLQueries``` folder.
Order of queries should be like this:
1. ```users.sql```
2. ```user_session.sql```
3. ```revoked_tokens.sql```
4. ```artists.sql```
5. ```album.sql```
6. ```genre.sql```
7. ```media_types.sql```
8. ```tracks.sql```

## Install Python Virtual Environment:
Once you are done with Database setup, now we have to deal with python setup,


### Install Virtual Environment
```bash
pip install virtualenv
```

### Clone the Project

```bash
git clone https://github.com/taimoorpashanbs17/flask-jwt-postgres.git
```

### Navigate to Your Project

```bash
cd flask-jwt-postgres
```

### Create Virtual Environment within project

```bash
virtualenv myenv
```

#### For Windows

```bash
myenv\Scripts\activate
```

#### For Mac and Linux

```bash
source myenv/bin/activate`
```

### Install dependencies

```bash
pip install -r requirements.txt
```

#### Note: 
1. Don't upgrade or Downgrade the dependencies, use it, as they are mentioned.
2. Enter Password on ```config.ini``` file at ```password``` key.
3. If port is already use, then change the port with any four digit.
#### Start using this Project.

```bash
python3 app.py
```

Learn to use these end points, with [following article](https://medium.com/@taimoorpasha2009/restful-apis-testing-project-using-access-tokens-along-with-database-verification-891f87224f6f) 

## 🔗 Get In Touch with me
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/taimoor-pasha-a2294878/)