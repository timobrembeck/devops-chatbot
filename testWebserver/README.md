

## Building for production

The following command will package an executable war file.

    mvn -Pprod package
    
You can run it using
    
    java -jar xyz.war
    
Make sure a Mysql database with the respective table is running. Use Docker to simplify it.



## Using Docker

A number of docker-compose configuration are available in the [src/main/docker](src/main/docker) folder to launch required third party services.

For example, to start a  database in a docker container, run:

    docker-compose -f src/main/docker/.yml up -d

To stop it and remove the container, run:

    docker-compose -f src/main/docker/.yml down

You can also fully dockerize your application and all the services that it depends on.
To achieve this, first build a docker image of your app by running:

    ./mvnw package -Pprod jib:dockerBuild
    

Then run:

    docker-compose -f src/main/docker/app.yml up -d
