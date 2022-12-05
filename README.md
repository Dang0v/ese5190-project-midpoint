# ese5190-project-midpoint

## Code

Currently we have done the 'flappy bird' demo on an OLED screen with driven by QTPY and circuit python. Basically using `displayio` function to draw the image, according to the [tutorial for OLED](https://learn.adafruit.com/adafruit-1-5-color-oled-breakout-board/python-usage).

## Media

### Materials

**OLED Breakout Board - 16-bit Color 1.27" w/microSD holder**

<img src="https://cdn-shop.adafruit.com/970x728/1673-09.jpg" alt="16-bit Color 1.27&quot; Color OLED with color bars test pattern" style="zoom:50%;" />

**Adafruit QT Py RP2040**

<img src="https://cdn-shop.adafruit.com/970x728/4900-12.jpg" alt="Angled shot of QT Py PCB." style="zoom:50%;" />



### Design

<img src="https://cdn-learn.adafruit.com/assets/assets/000/084/680/medium800/arduino_compatibles_1.5_OLED_bb.jpg?1574277589" alt="arduino_compatibles_1.5_OLED_bb.jpg" style="zoom:50%;" />

<img src="README.assets/IMG_0241.jpg" alt="IMG_0241" style="zoom: 25%;" />

### Troubleshooting

Basically we are using REPL for troubleshooting. Since we are using the screen, watching the movement of pixel is also a method for troubleshooting.

For example, we want to monitor the input of button, we just print the state to serial console.

```python
control = digitalio.DigitalInOut(board.BUTTON)
control.direction = digitalio.Direction.INPUT


print(control.value)
```

![image-20221204214204645](README.assets/image-20221204214204645.png)

### demo

![IMG_0240](README.assets/IMG_0240.gif)



## Diagram and works to do

For the next step, we will going through a really cool idea. Including augmented reality in our simple game. This can be simply realized by [pico4ML](https://www.arducam.com/pico4ml-an-rp2040-based-platform-for-tiny-machine-learning/). And also, the user input will be changing from the simple button input to [gyro IMU sensor](https://www.adafruit.com/product/4480), we are planning to use PIO module to drive the sensor for more frequent input.

