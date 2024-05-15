This is a very simple Python and OpenCV project completed in about 2 weeks

This Python files takes in a series of images from a specified folder and reads them using CV2.imread().
It then attempts to find a narrow, dark, vertical gap in the image which has so far been a weld gap for insutrial purposes.
It writes the results of the center of these weld gaps as 'x' at y=70 into a CSV. It also saves some interim image results.

I could be significantly improved by being more cautious about determining the weld gap position when it is uncertain (refer to results from Set 3).

This project was a way to quickly become familar with OpenCV and image processing for industrial purposes.
