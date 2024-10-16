# Science Olympiad Testing Environment

This project aims to create a web-based coding platform specifically tailored for Science Olympiad programming events.

For more information visit our [COMP523 E-Team Website here](https://tarheels.live/eteam/).

## Get Programming

### Running the DevContainer

1. Install Docker Desktop and the DevContainers extension in VSCode
2. Clone the repo into VSCode and open it
3. Press `Ctrl+Shift+P` on windows (`Cmd+Shift+P`?? on mac) to open the command pallet and run `Dev Containers: Build and Reopen in Container` (In the future to open you can just use `Dev Containers: Reopen in Container`)
4. Grab some water while the container builds

### Installing Dependencies

Run the following commands:

1. `cd frontend`
2. `npm install` to install React dependencies
3. `cd ../backend`
4. `python3 -m pip install -r requirements.txt` to install FastAPI & SQLModel dependencies (This must be run every time the container is rebuilt)
5. `python3 -m backend.script.reset_database` to create the database and load in fake data. This can be run as many times as possible to reset the databse.

### Running the Development Server

1. Run `honcho start`
2. Open `http://localhost:4400` to view the application

## Development Concerns

### Frontend

#### React Router

If you would like to create a new page and add it to the app itself. You would need to create the file, and if you have intellisense for react snippets, you can run "tsrafce" to spin up a component/page.

Now move to App.tsx. Import the page from the component you had just created. and add the following underneath the Routes tag:

```jsx
<Route path="[PATH THAT SHOWS IN THE URL]" element ={<[YOUR PAGE] />} />
```

Then you're all set to continue development!

### Backend

To help with backend implementation, you can reference the `count` demo feature.

#### FastAPI

When creating FastAPI routes, make sure to define the routes in a feature file named corresponding to the feature inside of the `api` directory.
This file should look similar to the example one in `api/count.py`. You will need to import the file in `main.py` and
add it to the `feature_apis` list as well as the tags in the `openapi_tags` list in the `FastAPI()` constructor.

#### SQLModel

Define all SQLModels in the `models` folder in a file named according to the feature. Make sure to add this file to the `__all__` list inside
of the `__init__.py` file in the `models` folder. This will allow it to be imported by default inside of the `create_database` script.

In the future we will support adding fake data inside of the `create_database` script.
