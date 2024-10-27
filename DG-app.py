import random
import math
import json
import httpx
import urllib
import webbrowser
from appJar import gui
from PIL import Image

def setcolor():
    app.setButton("Background color: #ffffff",f"Current color: {app.colourBox(colour="#ff0000")}")

def next(): #Settings for conversion
    inFile = app.getEntry("Select PNG/GIF: ")
    fileExt = inFile.split(".")[len(inFile.split("."))-1]
    if fileExt == "png" or fileExt == "gif":
        if fileExt == "png":
            target = Image.open(inFile)
            maxScale = math.sqrt(9216/(target.width*target.height))
            defaultWidth = math.floor(maxScale*target.width)
            defaultHeight = math.floor(maxScale*target.height)
            app.addImage("display", inFile)
            app.zoomImage("display",-1*round(target.height/100))
        else:
            defaultWidth = 4*16
            defaultHeight = 4*9
            app.addLabel("name",inFile.split("/")[len(inFile.split("/"))-1])
            app.setLabelFont("name",{'weight':'bold'})
        app.hideLabel("error1")
        app.hideButton("Next")
        app.hideEntry("Select PNG/GIF: ")
        app.addLabelNumericEntry("Width: ")
        app.setEntry("Width: ", defaultWidth)
        app.addLabelNumericEntry("Height: ")
        app.setEntry("Height: ", defaultHeight)
        if fileExt == "gif":
            app.addLabelNumericEntry("Frame step: ")
            app.setEntryDefault("Frame step: ",1)
            app.addLabelNumericEntry("Max Frames: ")
        app.addLabel("Graph Site:")
        app.addButton("Background color: #ffffff", setcolor)
        app.addLabelEntry("Hash: ")
        app.setEntryDefault("Hash: ","10 characters, or leave blank for random!")
        app.addLabelEntry("Title: ")
        app.addButton("Convert!", convert)
        app.addLabel("error2","Error posting graph - too much data or invalid hash!")
        app.hideLabel("error2")
        app.addWebLink("Desmos Graph", "https://www.desmos.com/calculator/")
        app.hideLink("Desmos Graph")
        app.setSize(500,400)
    else:
        app.showLabel("error1")

def convert():
    #Generate color values
    res = (int(app.getEntry("Width: ")),int(app.getEntry("Height: ")))
    inFile = app.getEntry("Select PNG/GIF: ")
    target = Image.open(inFile)
    fileExt = inFile.split(".")[len(inFile.split("."))-1]
    if fileExt == "png":
        pixelated = target.convert('RGB').resize(res)
        pixels = pixelated.load()
        RGBList = []
        for y in range(res[1]):
            for x in range(res[0]):
                RGBList.append(pixels[x,res[1]-1-y])
        frames = [RGBList]
    else:
        if(app.getEntry("Frame step: ")):
            frameskip = int(app.getEntry("Frame step: "))
        else:
            frameskip = 1
        if(app.getEntry("Max Frames: ")):
            maxFrames = int(app.getEntry("Max Frames: "))
        else:
            maxFrames = 10000
        
        frames = []
        try:
            for i in range(maxFrames):
                target.seek(i*frameskip)
                pixels = target.convert('RGB').resize(res).load()
                RGBList = []
                for y in range(res[1]):
                    for x in range(res[0]):
                        RGBList.append(pixels[x,res[1]-1-y])
                frames.append(RGBList)
                
        except EOFError:
            pass
    
    #Load request dictionaries
    #RequestBody = open("TemplateRequests/RequestBody.json","r")
    RequestBody = {
        "thumb_data": "data:image/png;base64,b",
        "graph_hash": "",
        "my_graphs": "false",
        "is_update": "false",
        "title": "Screen",
        "calc_state": "",
        "lang": "en",
        "product": "graphing"
    }
    #CalcState = open("TemplateRequests/CalcState.json","r")
    CalcState = {
        "version": 11,
        "randomSeed": "a8f578afe43f4593ea7a24b9769aab01",
        "graph": {
            "viewport": {
                "xmin": 0,
                "ymin": 0,
                "xmax": 1,
                "ymax": 1
            },
            "showGrid": False,
            "showXAxis": False,
            "showYAxis": False,
            "xAxisNumbers": False,
            "yAxisNumbers": False,
            "polarNumbers": False,
            "userLockedViewport": True,
            "squareAxes": False
        },
        "expressions": {
            "list": [
                {
                    "type": "folder",
                    "id": "19",
                    "title": "Back / Dimensions",
                    "collapsed": True
                },
                {
                    "type": "expression",
                    "id": "18",
                    "folderId": "19",
                    "color": "#000000",
                    "latex": "B_{ackground}=\\operatorname{polygon}\\left(\\left(0,0\\right),\\left(0,1\\right),\\left(1,1\\right),\\left(1,0\\right)\\right)",
                    "fillOpacity": "1"
                },
                {
                    "type": "expression",
                    "id:": "32",
                    "folderId": "19",
                    "color": "#000000",
                    "latex": "w_{idth}=16"
                },
                {
                    "type": "expression",
                    "id:": "34",
                    "folderId": "19",
                    "color": "#000000",
                    "latex": "h_{eight}=9"
                },
                {
                    "type": "expression",
                    "id": "10",
                    "folderId": "19",
                    "color": "#000000",
                    "latex": "B_{ack}=\\operatorname{polygon}\\left(\\left(L,B\\right),\\left(L,T\\right),\\left(R,T\\right),\\left(R,B\\right)\\right)",
                    "fillOpacity": "1"
                },
                {
                    "type": "expression",
                    "id": "14",
                    "folderId": "19",
                    "color": "#6042a6",
                    "latex": "L=\\left\\{\\frac{\\operatorname{width}}{w_{idth}}<\\frac{\\operatorname{height}}{h_{eight}}:0,0.5-\\frac{\\operatorname{height}w_{idth}}{2\\operatorname{width}h_{eight}}\\right\\}",
                    "hidden": True,
                    "slider": {
                        "hardMin": True,
                        "hardMax": True,
                        "min": "0",
                        "max": "0.5"
                    }
                },
                {
                    "type": "expression",
                    "id": "15",
                    "folderId": "19",
                    "color": "#000000",
                    "latex": "B=\\left\\{\\frac{\\operatorname{width}}{w_{idth}}<\\frac{\\operatorname{height}}{h_{eight}}:0.5-\\frac{\\operatorname{width}h_{eight}}{2\\operatorname{height}w_{idth}},0\\right\\}",
                    "hidden": True,
                    "slider": {
                        "hardMin": True,
                        "hardMax": True,
                        "min": "0",
                        "max": "0.5"
                    }
                },
                {
                    "type": "expression",
                    "id": "16",
                    "folderId": "19",
                    "color": "#c74440",
                    "latex": "T=1-B",
                    "hidden": True
                },
                {
                    "type": "expression",
                    "id": "17",
                    "folderId": "19",
                    "color": "#2d70b3",
                    "latex": "R=1-L",
                    "hidden": True
                },
                {
                    "type": "folder",
                    "id": "24",
                    "title": "Pixels",
                    "collapsed": True
                },
                {
                    "type": "expression",
                    "id": "1",
                    "folderId": "24",
                    "color": "#000000",
                    "latex": "P_{ixels}=\\left(i,j\\right)\\operatorname{for}i=\\left[L,L+\\frac{R-L}{w_{idth}-1}...R\\right],j=\\left[B,B+\\frac{T-B}{h_{eight}-1}...T\\right]",
                    "points": True,
                    "lines": False,
                    "dragMode": "NONE",
                    "colorLatex": "C_{olortemp}",
                    "pointSize": "p_{size}",
                    "movablePointSize": "p_{size}"
                },
                {
                    "type": "expression",
                    "id": "21",
                    "folderId": "24",
                    "color": "#000000",
                    "latex": "p_{size}=\\frac{1.15\\left(R-L\\right)\\operatorname{width}}{w_{idth}}",
                    "hidden": True
                },
                {
                    "type": "expression",
                    "id": "5",
                    "folderId": "24",
                    "color": "#000000",
                    "latex": "C_{olortemp}=C\\left(f_{rame},i\\right)\\operatorname{for}i=\\left[1...{w_{idth}h_{eight}}\\right]"
                },
                {
                    "type": "expression",
                    "id": "30",
                    "color": "#388c46",
                    "latex": "f_{rame}=1",
                    "hidden": True,
                    "slider": {
                        "hardMin": True,
                        "min": "1",
                        "hardMax": True,
                        "max": "",
                        "loopMode": "LOOP_FORWARD",
                        "step": "1"
                    }
                },
                {
                    "type": "folder",
                    "id": "35",
                    "title": "Video Data (CAREFUL LARGE FOLDER)",
                    "collapsed": True
                },
                {
                    "type": "expression",
                    "id": "33",
                    "folderId": "35",
                    "color": "#c74440"
                },
                {
                    "type": "expression",
                    "id": "31",
                    "folderId": "35",
                    "color": "#6042a6",
                    "latex": "F_{1}=\\left[\\right]"
                }
            ]
        },
        "includeFunctionParametersInRandomSeed": True
    }

    #Generate 2D formula
    CalcState["expressions"]["list"][1]["color"] = "#"+app.getButton("Background color: #ffffff").split("#")[1]
    CalcState["expressions"]["list"][2]["latex"] = f"w_{{idth}}={res[0]}"
    CalcState["expressions"]["list"][3]["latex"] = f"h_{{eight}}={res[1]}"
    CalcState["expressions"]["list"][13]["slider"]["max"] = str(len(frames))
    formula = []
    for i in range(len(frames)):
        formula.append(f"F_{{{i+1}}}\\left[P\\right]")
    formula = ','.join(formula)
    CalcState["expressions"]["list"][15]["latex"] = f"C\\left(t,P\\right)=\\left[{formula}\\right]\\left[t\\right]"

    #Paste Color Values
    exampleList = CalcState["expressions"]["list"][16]
    expList = CalcState["expressions"]["list"][0:16]
    for f in range(len(frames)):
        frameList = json.loads(json.dumps(exampleList))
        frameList["id"] = str(36 + f)
        pixelRGB = []
        for p in range(res[0]*res[1]):
            pixelRGB.append(f"\\operatorname{{rgb}}\\left({frames[f][p][0]},{frames[f][p][1]},{frames[f][p][2]}\\right)")
        pixelRGB = ",".join(pixelRGB)
        frameList["latex"] = f"F_{{{f+1}}}=\\left[{pixelRGB}\\right]"
        expList.append(frameList)
    CalcState["expressions"]["list"] = expList

    #Build Request Body
    hashInput = app.getEntry("Hash: ")
    if hashInput:
        hashN = str(hashInput)
    else:
        hashN = bytes(int(10000000000 * random.random()))
        hashN = str(abs(hash(hashN)))[0:10]
    RequestBody["graph_hash"] = hashN
    RequestBody["calc_state"] = CalcState
    title = app.getEntry("Title: ")
    if title:
        RequestBody["title"] = title
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.desmos.com',
        'Priority': 'u=0',
        'Referer': 'https://desmos.com/calculator/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    response = httpx.post("https://www.desmos.com/api/v1/calculator/save", headers=headers,data=urllib.parse.urlencode(RequestBody).replace("+","").replace("%27","%22").replace("False","false").replace("True","true"))
    if response.status_code == 200:
        app.removeLink("Desmos Graph")
        app.addWebLink("Desmos Graph", f"https://www.desmos.com/calculator/{hashN}")
        app.hideLabel("error2")
    else:
        app.hideLink("Desmos Graph")
        app.showLabel("error2")

def menuItem(item):
    if item == "GitHub":
        webbrowser.open_new_tab("https://github.com/Dan1elTheMan1el/Desmos-Graphics")
    elif item == "DanielTheManiel":
        webbrowser.open_new_tab("https://linktr.ee/DanielTheManiel")

#Initialize GUI
with gui("Desmos Graphics","500x200",bg = '#3fba6e', font={'size':18,'family':'futura'}) as app:
    app.setResizable(canResize=False)
    app.label("Desmos Graphics",font={'size':24,'weight':'bold','family':'futura'})
    app.label("DanielTheManiel",font={'size':12,'slant':'italic','family':'futura'})
    app.addHorizontalSeparator()
    app.addLabelFileEntry("Select PNG/GIF: ")
    app.addLabel("error1","Please select a PNG or GIF!")
    app.setLabelFg("error1",'red')
    app.hideLabel("error1")
    app.addButton("Next", next)
    app.createMenu("Desmos Graphics")
    app.addMenuList("Desmos Graphics",["Desmos Graphics","-","GitHub","DanielTheManiel"],menuItem)
    app.disableMenuItem("Desmos Graphics","Desmos Graphics")