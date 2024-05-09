
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="/GitAssets/Layer_1.png">
 <source media="(prefers-color-scheme: light)" srcset="/GitAssets/Layer_1.png">
 <img src="/GitAssets/Layer_1.png">
</picture>

# **An extractor for Roblox's Temp Assets**
## Getting started

Make sure to have python installed. Once you downloaded the source, you will need to install the requirements. To do so, open a cmd inside of the folder and type:

```
pip install -r requirements.txt
```
## Usage

Once you got everything installed, run main.py inside of the cmd:

```
python main.py
```
## Extract Functions

+ **Images:** Extracts Images to /Meshes as PNG
+ **Sounds:** Extracts Sounds to /Sounds as OGG
+ **Meshes:** Extracts Meshes to /Meshes as OBJ
+ **Animations:** Extracts Animations to /Animations as rbxm

