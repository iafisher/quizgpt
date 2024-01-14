To run the backend server:

```shell
$ cd backend
$ source .venv/bin/activate
$ uvicorn main:app --reload --port 5757
```

To serve the frontend:

```shell
$ cd frontend
$ npm run dev
```

To install the project:

```shell
$ cd backend
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cd ../frontend
$ npm install
```

The project is developed with Python 3.11 and Node 20.8. Older versions not guaranteed to work.
