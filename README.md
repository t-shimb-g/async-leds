# Internet Of Things Final Project
## Tyler Guldberg

# Steps
- Setup the following circuit:
![](Pictures/CircuitPicture.jpg)
There are five major sections of this circuit
- RGB LED
- 3 Individual LEDs
- Rotary Encoder
- OLED Display
- Photoresistor

These components on their own would make a neat product, however this class is called **Internet** of Things, so an
internet component will only heighten this products use!

Through the power of Websockets, we can have a webpage display _and control_ the data and states of the breadboard.

![](Pictures/PageScreenshot.png)

A really simple webpage like above can control the lights in their entirety. Not only that, but the webpage works
seamlessly with the breadboard components in tandem! Control from both the webpage or the breadboard to your hearts
content.

- The bulk of this work is through websockets: 
  - [Backend Websocket Setup](main.py)
  - [Frontend Websocket Setup](script.js)
    - This contains all the logic that transmits data to and from the board. 

Websockets allow two way communication between the board and the webpage. This enables both 'clients' to work in tandem.



The bulk of this product is having two way
communication using Websockets and demonstrating different applications of this concept (in this case with individual LEDs, a
RGB LED that is synchronized, and full control of them all from two locations at once!).
![](Pictures/CircuitPicture2.jpg)

And this shows the synchronization of the board and webpage.

[FinalProject.zip](FinalProject.zip)

All of the necessary files are in this zip file. Simply download it, upload it all to ESP32, and hit run!

Do you need to have control over your lights all of the time? Of course you do, and with this neat little product, you
can have all the control one could ask for!

_(In all seriousness, I do wish I had the time to refactor a great deal of this code. Namely, making a menu class to
handle callback functions and menu navigation with the rotary encoder which would clean up `main.py` a ton. Also
breaking up each device 'section' into different Websockets to greatly simplify the data that gets sent to and from.)_
