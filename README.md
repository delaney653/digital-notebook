## What is this?
Hello! Overall, the goal of this application is to make a web application where you can choose the site's background color and receive some feedback based on what colors you chose. It also stores any past colors you've chosen, but you also can completely delete your previous history if you'd like to do so.

## Project Setup

First, make sure you have Docker Desktop installed. If not, please download Docker Desktop here: https://www.docker.com/products/docker-desktop/. Make sure you have the latest MySQL, nginx, and python images downloaded.

Once you've pulled this repository, you can run this application by calling `docker-compose --profile production up --build`

You should be able to see and interact with the application by going to http://localhost:80

If you'd like to change any code and want to make sure all tests pass, you can run `docker-compose --profile testing up --build --abort-on-container-exit`. It'll run all of the tests in your terminal.

That's about it. Have fun!
