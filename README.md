# SimpleLEDSimulator

This library exposes a API identical to that of SimpleLED, except instead of drawing on a physical LED matrix, we draw on an emulated LED matrix built on Tkinter.

## How-To

In one terminal, run 
```
python board.py
```

This will construct the simulated LED board - this replaces the physical board, and will wait until a client using the display library makes a connection.

In another terminal, we can run a script meant for SimpleLED, but importing the above display.py instead of the one supplied by SimpleLED. This should now connect to the board in the other terminal, and begin drawing to it. 

## Issues

It's really slow. Nothing is optimized, and it updates "pixel" by "pixel" in the Tkinter window. 
