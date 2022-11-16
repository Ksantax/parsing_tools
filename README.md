# parsing_tools

requires docker

Run in terminal:
    
    git clone https://github.com/Ksantax/parsing_tools.git
    cd parsing_tools
    docker build -t pt_image .
    docker run -d -p 8000:8000 --name parsing_tools pt_image

Now, the application is avalable on adress `localhost:8000`

Example:

    localhost:8000\posts\?city=alzamay&car_type=auto
