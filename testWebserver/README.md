
## Using Docker

A number of docker-compose configuration are available in the [src/main/docker](src/main/docker) folder to launch required third party services.


You can also fully dockerize your application and all the services that it depends on.
To achieve this, first build a docker image of your app by running:

    ./mvnw package -Pprod jib:dockerBuild
    

Then run:

    docker-compose -f src/main/docker/app.yml up -d
