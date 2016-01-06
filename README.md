
     ,-----.,--.                  ,--. ,---.   ,--.,------.  ,------.
    '  .--./|  | ,---. ,--.,--. ,-|  || o   \  |  ||  .-.  \ |  .---'
    |  |    |  || .-. ||  ||  |' .-. |`..'  |  |  ||  |  \  :|  `--, 
    '  '--'\|  |' '-' ''  ''  '\ `-' | .'  /   |  ||  '--'  /|  `---.
     `-----'`--' `---'  `----'  `---'  `--'    `--'`-------' `------'
    ----------------------------------------------------------------- 
              ___  ____  _____  _____   _       ______              
             |_  ||_  _||_   _||_   _| / \    .' ____ \             
               | |_/ /    | |    | |  / _ \   | (___ \_|            
               |  __'.    | '    ' | / ___ \   _.____`.             
              _| |  \ \_   \ \__/ /_/ /   \ \_| \____) |            
             |____||____|   `.__.'|____| |____|\______.'            
                                                                    
             _________    ___   ________  _____   ______            
            |  _   _  | .'   `.|_   __  ||_   _|.' ___  |           
            |_/ | | \_|/  .-.  \ | |_ \_|  | | / .'   \_|           
                | |    | |   | | |  _| _   | | | |                  
               _| |_   \  `-'  /_| |__/ | _| |_\ `.___.'\           
              |_____|   `.___.'|________||_____|`.____ .'           
                        .oOOo. .oOOo. .oOOo.                        
                        O    o O    o O    o                        
                        o    O o    O o    O                        
                        `OooOo `OooOo o    o                        
                             O      O O    O                        
                             o      o o    O                        
                        `OooO' `OooO' `OooO'                        
                                                             by TCC 
Welcome!!
Install Step:
1.Install Flask and Selenium

    sudo pip3 install flask selenium

2.Install Google Chrome

    sudo apt-get install libxss1 libappindicator1 libindicator7
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome*.deb
    sudo apt-get install -f

3.Install Xvfb

    sudo apt-get install xvfb

4.Install ChromeDriver

    sudo apt-get install unzip
    wget -N http://chromedriver.storage.googleapis.com/2.20/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
    sudo mv -f chromedriver /usr/local/share/chromedriver
    sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
    sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

5.Install 中文字型(文鼎PL新宋,UMing,UKai,cwTex)

    sudo apt-get install ttf-wqy-zenhei xfonts-wqy ttf-arphic-ukai ttf-arphic-uming ttf-arphic-newsung
    sudo apt-get install fonts-cwtex-*
    sudo fc-cache -v

Start Step:

    ./start