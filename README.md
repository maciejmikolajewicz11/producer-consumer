# Overview

This application provides implementation of classic Producer - Consument problem with generating and pre-processing images using two queues. 

Idea:

- **Producer** fetches new images (size 1024x768px, 3 channels) from Source every 50ms and is putting them into queue A. 

- **Consumer** fetches the data from queue A (if available) and is preprocessing it in the following way:

    * Reduce its size twice
    * Apply median filter

    
once it is done, **Consumer** puts processed image into queue B. 
Images from queue B are saved in the folder *processed*.

## Installation

It is recommended to create new Python virtual environment for using this application. For more info you can refer to:

https://docs.python.org/3/library/venv.html


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all of the required requirements to run this project.

```bash
pip install -r requirements.txt
```

## Usage

From the root directory, please run the following command:

```bash
python run.py 
```
## Additional arguments

Application accepts following arguments that can be used along:

- rows: defines image height to generate, default=1024,
- columns: defines image width to generate, default=768,
- channels: defines image channels to generate, default=3,
- iterations: numbers of images to generate, default=100,
- output: name of the folder to store processed images, defaults to "processed"

Example usage:

```bash
python run.py --rows=1024 --columns=768
```
