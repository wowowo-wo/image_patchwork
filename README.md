# image_patchwork

<img src="ex/ex1.png" width="1000">

<img src="ex/ex2.png" width="1000">

This is a python tool that blends images as a patchwork.
Using opencv and numpy.

## Usage

clone this repo and install the requirements:

```bash
git clone https://github.com/wowowo-wo/image_patchwork
cd image_patchwork
pip install -r requirements.txt
```
and run:
```bash
python3 --images 'PATH of image1' 'PATH of image2' --ratios 0.1 0.2 ... --block_size 1 --output 'PATH of output image'
```

or you can run this tool with a GUI using Streamlit (It is more useful):

```bash
pip install streamlit
streamlit run gui.py
```

then, open the URL shown in your brouser.


## Requirements

opencv-python
numpy