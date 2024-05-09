import os
import re
import requests
from pathlib import Path
import audioread
from PIL import Image
import filetype
import validators
import magic
from RBXMesh import FileMeshData, read_mesh_data
from RBXMesh import FileMeshData, get_mesh_version
from RBXMesh import FileMeshData, export_mesh_v2
from RBXMesh import FileMeshData, export_mesh_v3
from RBXMesh import FileMeshFace, read_data
import OBJView

dir = Path.home() / 'AppData/Local/Temp/Roblox/http'
sd = "./Sounds/" 
id = "./Images/" 
md = "./Meshes/" 
an = "./Animations/"

MeshExporters = {"2.0": export_mesh_v2, "3.0": export_mesh_v3}
SelectedFunc = None



def audio_duration(length): 
    hours = length // 3600
    length %= 3600
    mins = length // 60
    length %= 60
    seconds = length

    
    if hours < 10:
        hours = str(hours)
        hours = "0" + hours
    if mins < 10:
        mins = str(mins)
        mins = "0" + mins
    if seconds < 10:
        seconds = str(seconds)
        seconds = "0" + seconds
    hours = str(hours)
    mins = str(mins)
    seconds = str(seconds)
    return hours, mins, seconds


def ReadMesh(path):
    MB : bytearray = ""
    MD : FileMeshData = ""
    MV = ""
    VM = False
    with open(path, "rb") as MESH:
        MB : bytearray = MESH.read()
        try:
          MD : FileMeshData = read_mesh_data(MB)
          MV = get_mesh_version(MB)
          VM = True
        except:
          MD = None
          MV = None
          VM = False
    return {"Valid": VM, "Version": MV, "MeshData": MD}

def ExportMesh(mesh_data):
    obj_data = []
    obj_data.append(f"o Untitled")
    countertest = 0
    #print(mesh_data)
    for vertex in mesh_data.vnts:
        obj_data.append(f"v {vertex.vx} {vertex.vy} {vertex.vz}")
    for tex_coord in mesh_data.vnts:
        obj_data.append(f"vt {tex_coord.tu} {tex_coord.tv}")
    for normal in mesh_data.vnts:
        obj_data.append(f"vn {normal.nx} {normal.ny} {normal.nz}")
    for face in mesh_data.faces:
        face_data = [f"{face.a+1}//{face.a+1} {face.b+1}//{face.b+1} {face.c+1}//{face.c+1}"]
        obj_data.append(f"f {''.join(face_data)}")
    return '\n'.join(obj_data)

def beginsearch():
    print("Beginning Audio Search...")
    TotalAudios = 0
    for filename in os.listdir(dir):
        file = os.path.join(dir, filename)
        data = open(file, encoding="utf8", errors="ignore")
        datadecoder = data.read()
        if "audio/ogg" in datadecoder:
           TotalAudios += 1
           string = ""
           urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', datadecoder)
           for x in urls:
              string += "" + x
           response = requests.get(string)
           audioinfo = ""
           h,m,s = "","",""
           duration = 'Total Duration: {}:{}:{}'
           with open(sd + "/" + filename + ".ogg", "wb") as af:
               af.write(response.content)
               af.close()
               with audioread.audio_open(sd + "/" + filename + ".ogg") as audio:
                   audioinfo = audio.duration
                   h,m,s = audio_duration(int(audioinfo))
           print("Found Audio in File " + filename + ". " + duration.format(h,m,s))
    print("Finished Audio search. Total Audios found: " + str(TotalAudios))
    
    
def beginimagesearch():
    print("Beginning Image Search...")
    TotalImages = 0
    for filename in os.listdir(dir):
        string = ""
        IsImage = False
        file = os.path.join(dir, filename)
        data = open(file, encoding="utf8", errors="ignore")
        datadecoder = data.read()
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', datadecoder)
        for x in urls:
              string += "" + x
        if validators.url(string):
            response = requests.get(string)
            with open(id + "/" + filename, "wb") as IMG:
               IMG.write(response.content)
               if filetype.is_image(id + "/" + filename):
                  IsImage = True
                  IMG.close()
                  if not os.path.exists(id + "/" + filename + ".png"):
                      os.rename(id + "/" + filename, id + "/" + filename + ".png")
               else:
                   IMG.close()
                   os.remove(id + "/" + filename)
        if IsImage:
            TotalImages += 1
            print("Found image " + filename)

    print("Finished Image search. Total Images found: " + str(TotalImages))


def beginmeshsearch():
    SelectedFunc = "LoadMesh"
    print("Beginning Mesh Search...")
    TotalMeshes = 0
    for filename in os.listdir(dir):
        string = ""
        MeshVer = 0
        VRT = 0
        IsMesh = False
        file = os.path.join(dir, filename)
        data = open(file, encoding="utf8", errors="ignore")
        datadecoder = data.read()
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', datadecoder)
        for x in urls:
              string += "" + x
        if validators.url(string):
            response = requests.get(string)
            with open(md + "/" + filename, "wb") as MESH:
               MESH.write(response.content)
               RP = ReadMesh(md + "/" + filename)
               if RP["Valid"]:
                   IsMesh = True
                   MeshVer = RP["Version"]
                   VRT = len(RP["MeshData"].vnts)
                   meshcont = ExportMesh(RP["MeshData"])
                   with open(md + "/" + filename + ".obj", "w") as OBJMESH:
                          OBJMESH.write(meshcont)
                   MESH.close()
                   OBJMESH.close()
                   os.remove(md + "/" + filename)
               else:
                   MESH.close()
                   os.remove(md + "/" + filename)
                   
        if IsMesh:
            TotalMeshes += 1
            print("Found Mesh " + filename + " with version " + str(MeshVer) + " Vertices: " + str(VRT))

    print("Finished Mesh search. Total Meshes found: " + str(TotalMeshes))


def beginAnimsearch():
    print("Beginning Animation Search...")
    TotalAnimations = 0
    for filename in os.listdir(dir):
        file = os.path.join(dir, filename)
        data = open(file, encoding="utf8", errors="ignore")
        datadecoder = data.read()
        if "KeyframeSequence" in datadecoder:
           TotalAnimations += 1
           string = ""
           urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', datadecoder)
           for x in urls:
              string += "" + x
           response = requests.get(string)
           with open(an + "/" + filename + ".rbxm", "wb") as af:
               af.write(response.content)
               af.close()
           print("Found Animation in File " + filename)
    print("Finished Animation search. Total Animations found: " + str(TotalAnimations))


def LoadMesh():
    LM = input("Would you like to load a mesh? Y/N ")
    if LM == "Y":
       OBJView.main()
    else:
        return



AssetTypes = {"Images": beginimagesearch, "Sounds": beginsearch, "Meshes": beginmeshsearch, "Animations": beginAnimsearch}
PostAssetFuncs = {LoadMesh}

ck = input("Would you like to skip to post asset functions? Y/N ")
if ck == "N":
    types = ""
    for tp in AssetTypes:
       types+=f"{tp}, "
    var = input(f"Please select Asset Type ({types}) ")
    if AssetTypes[var]:
       AssetTypes[var]()
       for func in PostAssetFuncs:
           func()
    else:
        print("Not a valid asset type!")
else:
    for func in PostAssetFuncs:
           func()


        




