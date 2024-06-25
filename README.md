# Mandelbrot-Set-Visualiser

## :zap: About
The [Mandelbrot Set](https://en.wikipedia.org/wiki/Mandelbrot_set) is a beautiful Mathematical phenomenon. This is a little visualisation tool I made to help plot the set and see its beauty for yourself!

**NOTE:** I have tried to optimize the code a bit with `numba` and `numpy` in Python, so you should get around 24 FPS. However, it still might lag slightly, as GPU acceleration isn't enabled.

## :desktop_computer: How to run locally
Clone the repository on your machine, and run `pip install -r requirements.txt` (preferably in a virtual environment). Then, just run `main.py`!

## :grey_question: Controls
- `W`, `A`, `S`, `D` to move around the plot. 
- `Up-Arrow` or `Down-Arrow` to zoom in or out.
- `Right-Arrow` or `Left-Arrow` to increase or decrease the resolution.