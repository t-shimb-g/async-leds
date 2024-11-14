const ip = 'ADDRESS';
        window.addEventListener("load", function () {
            let ws = new WebSocket(`ws://${ip}/slider`);
            let photoWs = new WebSocket(`ws://${ip}/ldr`)

            rooms = [document.getElementById('RedRoom'), document.getElementById('GreenRoom'), document.getElementById('BlueRoom')]
            roomColors = ['#ff0000', '#00ff00', '#0000ff']
            roomBools = [false, false, false]

            ws.onmessage = (event) => {
                data = JSON.parse(event.data); // String containing states of LEDs and RGB LED color in hex
                document.getElementById("RGBroom").style.background = 'rgb(' + String(data[0]) + ')';
                document.getElementById("colorPicker").value = 'rgb(120, 76, 200)';

                for(let i = 0; i < data.length; i++) {
                    if(i > 0) {
                        if(data[i]) {
                            rooms[i - 1].style.background = roomColors[i - 1];
                        }
                        else {
                            rooms[i - 1].style.background = '#ffffff';
                        }
                        roomBools[i] = data[i];
                        roomUpdate(rooms[i - 1], roomBools[i], roomColors[i - 1]);
                    }
                }
            }

            photoWs.onmessage = (event) => {
                data = JSON.parse(event.data);
                document.getElementById("LDRStatusLabel").innerText = data + ' / 100';
            }

            ws.onclose = (event) => {
                console.log("websocket closed");
            }
            ws.onerror = (event) => {
                console.log("websocket error: ", event);
            }

            function roomUpdate(room, roomBool, roomColor) {
                if(roomBool) {
                    room.style.background = roomColor;
                }
                else {
                    room.style.background = '#ffffff';
                }
            };
            
            rooms[0].addEventListener("click", function () {
                data = JSON.stringify({ led: 1 });
                roomBools[1] = !roomBools[1];
                roomUpdate(rooms[0], roomBools[1], roomColors[0]);
                ws.send(data); // Send back id of the LED that was clicked
                console.log("red clicked");
            });

            rooms[1].addEventListener("click", function () {
                data = JSON.stringify({ led: 2 });
                roomBools[2] = !roomBools[2];
                roomUpdate(rooms[1], roomBools[2], roomColors[1]);
                ws.send(data);
                console.log("green clicked");
            });

            blueRoom = document.getElementById("BlueRoom");
            rooms[2].addEventListener("click", function () {
                data = JSON.stringify({ led: 3 });
                roomBools[3] = !roomBools[3];
                roomUpdate(rooms[2], roomBools[3], roomColors[2]);
                ws.send(data);
                console.log("blue clicked");
            });

            colorPicker = document.getElementById("colorPicker");
            colorPicker.addEventListener("change", function () {
                document.getElementById("RGBroom").style.background = colorPicker.value;
                console.log(colorPicker.value);
                data = JSON.stringify({ rgb: colorPicker.value });
                ws.send(data);
                console.log("rgb changed");
            });
        });