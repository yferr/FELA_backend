# Docker Django API template

It is a Docker template to start Django + DRF + GeoDjango APIs.
It cams with a working example in the buildings app.

# Help

- Clone the repo:

```ruby
    git clone https://github.com/joamona/django-api-template.git
```

- Change to the project folder:
```ruby
    cd django-api-template
```
- Create the pgadmin folders:
```ruby
    Windows: pgadmin_create_folders_windows.bat
    Linux: ./pgadmin_create_folders_linux.sh
```
- Create the containers and start the services:
```ruby
    docker compose up
```
- Check the services:

    - pgadmin: http://localhost:8051
    - geoserver: http://localhost:7002
    - Django API: http://localhost:8888/FELA

# Start developping
To avoid to install Pyhton and its dependencies in your computer, you can 
use the interpreter in the container. You can achieve this with Visual Studio Code (VS).

- Start the services: docker compose up.
- Open VS.
- Press Ctrl + Shift + p.
- Paste the following: Dev Containers: Attach to Running Container.
- Select the container *-djangoapi-1.
- A new VS code window is started.
- In the terminal, change to the folder /home/$username, where the source code is.
- Select the interpreter: Ctrl + Shift + p, and type python select interpreter, and select the interpreter in the container. There are two interpreters. Select the one in 
/usr/local/bib/python. This one is the one that has all the pythin mackages installed: Django, GeoDjango, etc. In this way VS will help you to code.


# Debugging

RemoteDebug has been configured in the VS project and in settings.py. To stop the execution in a line:

- If you change the username in the file .env, you musy change the file .vscode/launch.json:

      "remoteRoot": "/home/joamona"   <-- Change joamona to your username

- Put a breackpoint.
- Set, in djangoapi/settings.py, the REMOTE_DEBUG to true.
- Open the Debug window of VS and click Play over the DjangoAPI configuration.
- Ready to debug.

# Installed apps

The project cams with three app:

- core: It has the myLib package, who contains the geoModelSerializer. It is a base class to manage models with geometries. Ii uses geodjango.
- FELA: It contains a model, serializer, and modelViewSet 



