
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
+ **Meshes:** Extracts Meshes to /Meshes as OBJ using the RBXMesh library by [PrintedScript](https://github.com/PrintedScript/RBXMesh)
+ **Animations:** Extracts Animations to /Animations as rbxm

![image](https://github.com/zxnearby/Temp-Extractor/assets/71570183/e6fb707e-d954-4e2b-9981-aa11f7a24dd7)


## Mesh Viewer

A mesh viewer is included, you can find the source here: [OBJ Viewer](https://github.com/Zehina/3D-.obj-File-Viewer)
Just drag and drop a mesh from the Meshes folder to the viewer

![image](https://github.com/zxnearby/Temp-Extractor/assets/71570183/365828d9-ba31-41c6-96f3-8a9d72d2d201)


