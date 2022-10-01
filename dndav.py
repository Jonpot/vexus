from random import randrange


def setdir():
    import os
    if os.getcwd() != 'G:\Shared drives\Vexus\_attachments\scripts':
        os.chdir('G:\Shared drives\Vexus\_attachments\scripts')
        print("Changed current directory to:\n", os.getcwd(),"\n")


def createfile():
    from time import time, ctime
    setdir()
    m = open("lightMultithreading.md","w")
    m.write("File created at "+ctime(time())+"\nIdle"+"\nRunning")
    m.close

def runEffect():
    from time import time, ctime
    setdir()
    unpauseEffect()
    m = open("lightMultithreading.md","r")
    m.readline()
    line = m.readline()
    if line == "Idle\n":
        w = open("lightMultithreading.md","w")
        w.write("File edited at "+ctime(time())+"\nRunning\nRunning")

def pauseEffect():
    from time import time, ctime, sleep
    setdir()
    m = open("lightMultithreading.md","r")
    m.readline()
    line = m.readline()
    line = m.readline()
    if line == "Running":
        w = open("lightMultithreading.md","w")
        w.write("File edited at "+ctime(time())+"\nRunning\nPaused")
        w.close()
    m.close

def unpauseEffect():
    from time import time, ctime
    setdir()
    m = open("lightMultithreading.md","r")
    m.readline()
    line = m.readline()
    line = m.readline()
    if line != "Running":
        w = open("lightMultithreading.md","w")
        w.write("File edited at "+ctime(time())+"\nRunning\nRunning")
        w.close()
    m.close


def stopAllEffects():
    from time import time, ctime
    setdir()
    m = open("lightMultithreading.md","w")
    m.write("File edited at "+ctime(time())+"\nIdle\nRunning")

def checkRunning():
    setdir()
    m = open("lightMultithreading.md","r")
    m.readline()
    line = m.readline()
    if line == "Idle\n":
        return(False)
    else:
        return(True)

def checkPause():
    setdir()
    m = open("lightMultithreading.md","r")
    m.readline()
    m.readline()
    line = m.readline()
    if line == "Paused":
        return(True)
    else:
        return(False)

def setup():
    # Imports
    global Bridge, random, time, playsound, requests, json, b, huelights, lights, groups, namedLights, namedScenes, namedGroups, namedLights, dicecloudChars, token
    from qhue import Bridge
    import random
    import time
    import playsound
    import requests
    import json

    # Connect to the bridge with a particular username
    b = Bridge("10.0.0.134", "lGXw2X9bf6o-kyEVGmVQLoiUhztSD2Kx8ivIW54l")
    print(b.url)
    huelights = b.lights   # Creates a new Resource with its own URL
    print(huelights.url)    # Should have '/lights' on the end

    # Construct a dictionary of the lights.
    namedLights = {}
    for k in b.lights():
        namedLights[b.lights[k]()['name']] = k

    # Construct a dictiony of the scenes
    namedScenes = {}
    for k in b.scenes():
        namedScenes[b.scenes[k]()['name']] = k

    # Construct a dictiony of the groups
    namedGroups = {}
    for k in b.groups():
        namedGroups[b.groups[k]()['name']] = k

    # Define some nice to use classes
    class lights():
        moon = namedLights['The Moon']
        sky1 = namedLights['Sky 1']
        sky2 = namedLights['Sky 2']
        jon = namedLights['Jon 2']
        strip = namedLights['Strip']
        zeke = namedLights['Zeke Spotlight']

    class groups():
        livingRoom = namedGroups['Living Room']

    # Create a dictionary of dicecloud character keys:
    #dicecloudChars = {"Rhogar":"mxiGk7BjCtjoB4AAx", "Rexxar":"sYFpp3zrLsBhnFgbL", "Akanta":"T97kkFwogty98Hddn", "Erelis":"d3HM3tByrcqtP2CrC", "Eren":"ntXBhshvSsK3Woaq8", "Steyl":"spGdCAKCAyTJwyTxS", "Bahlegdu":"DBms8fpAgiWnX68A8"}
    dicecloudChars = {"Rhogar":"mxiGk7BjCtjoB4AAx", "Akanta":"T97kkFwogty98Hddn", "Erelis":"d3HM3tByrcqtP2CrC", "Eren":"ntXBhshvSsK3Woaq8", "Iyrn":"TCbsFhRFQWgjnLZLQ", "Bahlegdu":"DBms8fpAgiWnX68A8", "Arianna":"xGugeD7bM3Diuzcak"}
    token = "Bearer 3ZHwL3ubDyTSWHHcC8v-49s_5-1RYefTJgtV5fuIvSZ"

    #unpauseEffect()


def hex2rgb(hex_value):
    h = hex_value.strip("#") 
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def rgb2hsv(rgb):
    # Normalize R, G, B values
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0

    # h, s, v = hue, saturation, value
    max_rgb = max(r, g, b)    
    min_rgb = min(r, g, b)   
    difference = max_rgb-min_rgb 
 
    # if max_rgb and max_rgb are equal then h = 0
    if max_rgb == min_rgb:
        h=0
    # if max_rgb==r then h is computed as follows
    elif max_rgb == r:
        h = (60 * ((g - b) / difference) + 360) % 360
 
    # if max_rgb==g then compute h as follows
    elif max_rgb == g:
        h = (60 * ((b - r) / difference) + 120) % 360
 
    # if max_rgb=b then compute h
    elif max_rgb == b:
        h = (60 * ((r - g) / difference) + 240) % 360

    # if max_rgb==zero then s=0
    if max_rgb == 0:
        s = 0
    else:
        s = (difference / max_rgb) * 100
 
    # compute v
    v = max_rgb * 254
    # return rounded values of H, S and V
    return list(map(round, (h, s, v)))

def fixhsv(hsv):
    hsv[0] = 65535*hsv[0]/360
    return hsv

def setcolor(light,on=-1,hex=-1,rgb=-1,xy=-1,manualhsv=-1,hsv=-1):
    if on == False:
        b.lights[light].state(on=False)
        return
    else:
        b.lights[light].state(on=True)
    if hex != -1:
        hsv = fixhsv(rgb2hsv(hex2rgb(hex)))
    elif rgb != -1:
        hsv = fixhsv(rgb2hsv(rgb))
    elif manualhsv != -1:
        hsv = fixhsv(manualhsv)

    if hsv != -1:
        b.lights[light].state(on=True,hue=int(hsv[0]),sat=int(hsv[1]),bri=int(hsv[2]))
    elif xy != -1:
        b.lights[light].state(on=True,xy=xy)
    else:
        print("Something went wrong! Couldn't identify a complete color scheme!\n")

def setbri(light,bri):
    b.lights[light].state(on=True,bri=bri)

def setscene(group='Living Room', scene='Energize'):
    setup()
    #for light in b.groups[namedGroups[group]]()["lights"]:
        #print("Before:",b.lights[light]()['name'],b.lights[light]()['state']['hue'],"\n")
    time.sleep(0.5)
    b.groups[namedGroups[group]].action(scene=namedScenes[scene])

def torchlight():
    setup()
    jonBase = (lights.jon,b.lights[lights.jon]()['state']['bri'])
    zekeBase = (lights.zeke,b.lights[lights.zeke]()['state']['bri'])
    runEffect()
    while checkRunning() == True:
        for baseBri in [jonBase,zekeBase]:
            newBri = random.randrange(max(baseBri[1]-75,50),min(baseBri[1]+10,255),1)
            setbri(baseBri[0],newBri)
        time.sleep(0.75)

def sparkle():
    setup()
    sparklePalette = []
    for baseLight in b.groups[groups.livingRoom]()['lights']:
        sparklePalette.append([b.lights[baseLight]()['state']])
        #print(b.lights[baseLight]()['name'],b.lights[baseLight]()['state']['hue'],"\n")
    runEffect()
    while checkRunning() == True:
        light2change = b.groups[groups.livingRoom]()['lights'][random.randrange(0,len(b.groups[groups.livingRoom]()['lights']),1)]
        randIndex=int(random.randrange(0,len(sparklePalette),1))
        for bulb in sparklePalette[randIndex]:
            setcolor(light2change,on=bulb['on'],hsv=[bulb['hue'],bulb['sat'],bulb['bri']])
        time.sleep(0.5)

def birds():
    setup()
    runEffect()
    while checkRunning() == True:
        coinflip=1
        while coinflip == 1:
            light2toggle = b.groups[groups.livingRoom]()['lights'][random.randrange(0,len(b.groups[groups.livingRoom]()['lights']),1)]
            b.lights[light2toggle].state(on=False)
            time.sleep(1)
            coinflip = randrange(0,2,1)
        for bulb in b.groups[groups.livingRoom]()['lights']:
            b.lights[bulb].state(on=True)
        time.sleep(random.randrange(1,15,1))

def getHealth():
    import requests, json
    setup()
    maxHealth = 0
    currentHealth = 0
    for characterID in dicecloudChars:
        try:
            r = requests.get("https://beta.dicecloud.com/api/creature/"+dicecloudChars[characterID],headers={"Authorization":token})
            characterData = json.loads(r.text)
            currentCharHealth = next(x for x in characterData["creatureProperties"] if x.get("variableName") == "hitPoints")['value']
            maxCharHealth = next(x for x in characterData["creatureProperties"] if x.get("variableName") == "hitPoints")['total']
        except:
            currentCharHealth = 0
            maxCharHealth = 0
        print(characterID,"is currently at",currentCharHealth,"/",maxCharHealth,"hit points.\n")
        maxHealth += maxCharHealth
        currentHealth += currentCharHealth
    print("The party is currently at",currentHealth,"/",maxHealth," hit points.\n")

def getProperties(variableName="athletics"):
    import requests, json
    setup()
    totalMod = "Put the following equation into anydice: output "
    for characterID in dicecloudChars:
        disadvantageCheck = 0
        try:
            r = requests.get("https://beta.dicecloud.com/api/creature/"+dicecloudChars[characterID],headers={"Authorization":token})
            characterData = json.loads(r.text)
            variableMod = next(x for x in characterData["creatureProperties"] if x.get("variableName") == variableName)['value']
            try:
                effects = next(x for x in characterData["creatureProperties"] if x.get("variableName") == variableName)['effects']
                for effect in effects:
                    try:
                        if effect["operation"] == "disadvantage":
                            disadvantageCheck = 1
                    except:
                        pass
            except:
                disadvantageCheck == 0
                
        except:
            variableMod = 0
            disadvantageCheck = 0
        if disadvantageCheck == 1:
            returnstat = "does"
            modDisMod = "([lowest 1 of 2d20]+"
        else:
            returnstat = "does not"
            modDisMod = "(1d20+"
        print(characterID,"has a",variableName,"modifier of",variableMod,"and",returnstat,"have disadvantage.\n")
        
        totalMod += modDisMod
        totalMod += str(variableMod)
        totalMod += ") +"

    print(totalMod[:-1])

def updateHealth(startHSV=[0,0,0],endHSV=[533,243,99],lights=[]):
    setup()
    maxHealth = 0
    currentHealth = 0
    runEffect()
    while checkRunning() == True:
        while checkPause() == True:
            time.sleep(2)
        for characterID in dicecloudChars:
            try:
                r = requests.get("https://beta.dicecloud.com/api/creature/"+dicecloudChars[characterID],headers={"Authorization":token})
                characterData = json.loads(r.text)
                currentCharHealth = next(x for x in characterData["creatureProperties"] if x.get("variableName") == "hitPoints")['value']
                maxCharHealth = next(x for x in characterData["creatureProperties"] if x.get("variableName") == "hitPoints")['total']
            except:
                currentCharHealth = 0
                maxCharHealth = 0
            
            maxHealth += maxCharHealth
            currentHealth += currentCharHealth

        newHue= []
        for i in range(len(startHSV)):
            newHue.append((((startHSV[i]-endHSV[i])/maxHealth)*(currentHealth))+endHSV[i])
        for bulb in lights:
            setcolor(namedLights[bulb],hsv=newHue)
        time.sleep(15)

def pingHealth(startHSV=[0,0,0],endHSV=[533,243,99],lights=[]):
    setup()
    maxHealth = 0
    currentHealth = 0
    for characterID in dicecloudChars:
        try:
            r = requests.get("https://beta.dicecloud.com/api/creature/"+dicecloudChars[characterID],headers={"Authorization":token})
            characterData = json.loads(r.text)
            currentCharHealth = next(x for x in characterData["creatureProperties"] if x.get("variableName") == "hitPoints")['value']
            maxCharHealth = next(x for x in characterData["creatureProperties"] if x.get("variableName") == "hitPoints")['total']
        except:
            currentCharHealth = 0
            maxCharHealth = 0
        
        maxHealth += maxCharHealth
        currentHealth += currentCharHealth

    newHue= []
    for i in range(len(startHSV)):
        newHue.append((((startHSV[i]-endHSV[i])/maxHealth)*(currentHealth))+endHSV[i])
    for bulb in lights:
        setcolor(namedLights[bulb],hsv=newHue)

def forgeSurge():
    setup()
    setscene(scene="ForgeFirey")
    pingHealth(startHSV=[0,0,30],lights=["Sky 1", "Sky 2"])
    runEffect()
    newBri=254
    while checkRunning() == True:
        while checkPause() == True:
            time.sleep(2)
        lights2change = [lights.jon,lights.zeke,lights.strip]
        delBri = randrange(-60,61,1)
        newBri = min(255,max(20,(newBri+delBri))) 
        for bulb in lights2change:
            b.lights[bulb].state(bri=newBri)
        time.sleep(0.1)

def kondensiteStrike(scene="ForgeDefault"):
    setup()
    pauseEffect()
    
    setcolor(lights.strip,hsv=[42805,216,254])
    time.sleep(0.5)
    setcolor(lights.jon,hsv=[42805,216,254])
    setcolor(lights.zeke,hsv=[42805,216,254])
    time.sleep(0.5)
    setcolor(lights.moon,hsv=[42805,216,254])
    time.sleep(0.5)
    setcolor(lights.sky1,hsv=[42805,216,254])
    setcolor(lights.sky2,hsv=[42805,216,254])
    time.sleep(0.5)
    for bulb in b.groups[groups.livingRoom]()['lights']:
            setcolor(bulb,hsv=[41590,75,254])
    time.sleep(1)
    for bulb in b.groups[groups.livingRoom]()['lights']:
            setcolor(bulb,hsv=[41590,75,1])
    time.sleep(1)
    setscene(scene=scene)
    unpauseEffect()
    pingHealth(startHSV=[0,0,30],lights=["Sky 1", "Sky 2"])

def lavashockRidge():
    setup()

    # Create a list of the working scene
    thunderScene = [lights.sky1,lights.sky2,lights.moon]

    # Establish Palettes for the Lights
    whitePalette = [0.33,0.33]

    # Setup Sounds
    sounds = {0:'C:/Users/jonat/Downloads/QHueExperiments/sounds/thunder1.mp3',1:'C:/Users/jonat/Downloads/QHueExperiments/sounds/thunder2.mp3',2:'C:/Users/jonat/Downloads/QHueExperiments/sounds/thunder3.mp3'}
    # Set the scene
    b.groups[groups.livingRoom].action(scene=namedScenes['Lavashock Ridge'])

    # Thunder Script
    runEffect()
    while checkRunning() == True:
        thunderChoice = random.randrange(0,5,1)
        if thunderChoice == 0 or thunderChoice == 1:
            # Small Thunder 1 or 2
            b.lights[[lights.sky1,lights.sky2][thunderChoice]].state(on=True,bri=254,xy=whitePalette)
            time.sleep(0.25)
            b.groups[groups.livingRoom].action(scene=namedScenes['Lavashock Ridge'])
            time.sleep(random.randrange(5,10,1))
            playsound.playsound(sounds[random.randrange(0,len(sounds),1)])
        elif thunderChoice == 2 or thunderChoice == 3:
            # Rolling Thunder 1 or 2
            b.lights[[lights.sky1,lights.sky2][thunderChoice-2]].state(on=True,bri=254,xy=whitePalette)
            time.sleep(0.25)
            b.lights[[lights.sky1,lights.sky2][thunderChoice-2]].state(bri=100)
            time.sleep(0.25)
            b.lights[[lights.sky1,lights.sky2][thunderChoice-2]].state(bri=254)
            time.sleep(0.25)
            b.groups[groups.livingRoom].action(scene=namedScenes['Lavashock Ridge'])
            time.sleep(random.randrange(5,10,1))
            playsound.playsound(sounds[random.randrange(0,len(sounds),1)])
        else:
            # Biggest Thunder
            for n in thunderScene:
                    b.lights[n].state(on=True,bri=254,xy=whitePalette)
            time.sleep(0.25)
            b.lights[thunderScene[random.randrange(0,len(thunderScene))]].state(bri=160)
            time.sleep(0.25)
            b.lights[thunderScene[random.randrange(0,len(thunderScene))]].state(bri=160)
            for n in thunderScene:
                    b.lights[n].state(bri=254)
            time.sleep(0.25)
            for n in thunderScene:
                    b.lights[n].state(on=False)
            time.sleep(0.25)
            b.lights[thunderScene[random.randrange(0,len(thunderScene))]].state(on=True,bri=160)
            time.sleep(0.25)
            b.lights[thunderScene[random.randrange(0,len(thunderScene))]].state(on=True,bri=160)
            for n in thunderScene:
                    b.lights[n].state(on=True,bri=254)
            b.groups[groups.livingRoom].action(scene=namedScenes['Lavashock Ridge'])
            playsound.playsound(sounds[random.randrange(0,len(sounds),1)])
        
        time.sleep(random.randrange(1,2*60,1))
        if random.randrange(1,20,1) >= 19:
            sounds2 = {0:'C:/Users/jonat/Downloads/QHueExperiments/sounds/volcano1.mp3'}
            playsound.playsound(sounds2[random.randrange(0,len(sounds2),1)])
        time.sleep(random.randrange(30,1*60,1))

def storm(sceneIn = "Promethean Storm"):
    setup()

    # Create a list of the working scene
    thunderScene = [lights.sky1,lights.sky2,lights.moon]

    # Establish Palettes for the Lights
    whitePalette = [0.33,0.33]

    # Setup Sounds
    sounds = {0:'C:/Users/jonat/Downloads/QHueExperiments/sounds/thunder1.mp3',1:'C:/Users/jonat/Downloads/QHueExperiments/sounds/thunder2.mp3',2:'C:/Users/jonat/Downloads/QHueExperiments/sounds/thunder3.mp3'}
    # Set the scene
    b.groups[groups.livingRoom].action(scene=namedScenes[sceneIn])

    # Thunder Script
    runEffect()
    while checkRunning() == True:
        thunderChoice = random.randrange(0,5,1)
        if thunderChoice == 0 or thunderChoice == 1:
            # Small Thunder 1 or 2
            b.lights[[lights.sky1,lights.sky2][thunderChoice]].state(on=True,bri=254,xy=whitePalette)
            time.sleep(0.25)
            b.groups[groups.livingRoom].action(scene=namedScenes[sceneIn])
            time.sleep(random.randrange(5,10,1))
            playsound.playsound(sounds[random.randrange(0,len(sounds),1)])
        elif thunderChoice == 2 or thunderChoice == 3:
            # Rolling Thunder 1 or 2
            b.lights[[lights.sky1,lights.sky2][thunderChoice-2]].state(on=True,bri=254,xy=whitePalette)
            time.sleep(0.25)
            b.lights[[lights.sky1,lights.sky2][thunderChoice-2]].state(bri=100)
            time.sleep(0.25)
            b.lights[[lights.sky1,lights.sky2][thunderChoice-2]].state(bri=254)
            time.sleep(0.25)
            b.groups[groups.livingRoom].action(scene=namedScenes[sceneIn])
            time.sleep(random.randrange(5,10,1))
            playsound.playsound(sounds[random.randrange(0,len(sounds),1)])
        else:
            # Biggest Thunder
            for n in thunderScene:
                    b.lights[n].state(on=True,bri=254,xy=whitePalette)
            time.sleep(0.25)
            b.lights[thunderScene[random.randrange(0,len(thunderScene))]].state(bri=160)
            time.sleep(0.25)
            b.lights[thunderScene[random.randrange(0,len(thunderScene))]].state(bri=160)
            for n in thunderScene:
                    b.lights[n].state(bri=254)
            time.sleep(0.25)
            for n in thunderScene:
                    b.lights[n].state(on=False)
            time.sleep(0.25)
            b.lights[thunderScene[random.randrange(0,len(thunderScene))]].state(on=True,bri=160)
            time.sleep(0.25)
            b.lights[thunderScene[random.randrange(0,len(thunderScene))]].state(on=True,bri=160)
            for n in thunderScene:
                    b.lights[n].state(on=True,bri=254)
            b.groups[groups.livingRoom].action(scene=namedScenes[sceneIn])
            playsound.playsound(sounds[random.randrange(0,len(sounds),1)])
        
        time.sleep(random.randrange(1,2*60,1))

def flamesquall():
    setup()
    livingRoomScene = [lights.moon,lights.sky1,lights.sky2,lights.jon,lights.zeke,lights.strip]
    crystalScene = [lights.zeke,lights.jon,lights.sky1,lights.sky2,lights.moon]

    # Establish Palettes for the Lights
    crystalPalette = [0.07,0.31]
    floorPalette = [0.62,0.44]
    whitePalette = [0.33,0.33]

    # Set the scene
    b.groups[groups.livingRoom].action(scene=namedScenes['Flamesquall'])

    # Crystal Script
    runEffect()
    while checkRunning() == True:
        startNode = random.randrange(0,5,1)
        b.lights[crystalScene[startNode]].state(on=True,bri=254,xy=crystalPalette)
        for i in range(1,5,1):
            try:
                b.lights[crystalScene[startNode+i]].state(on=True,bri=254,xy=crystalPalette)
            except:
                pass
            try:
                b.lights[crystalScene[startNode-i]].state(on=True,bri=254,xy=crystalPalette)
            except:
                pass
            time.sleep(0.5)
        #playsound('C:/Users/jonat/Downloads/QHueExperiments/sounds/crystalCharge.wav')
        for n in crystalScene:
            b.lights[n].state(xy=whitePalette)
        time.sleep(0.1)
        for n in crystalScene:
            b.lights[n].state(bri=100,xy=crystalPalette)
        b.lights[lights.strip].state(on=False)
        for i in range(0,5,1):
            try:
                b.lights[crystalScene[startNode+i]].state(on=False)
            except:
                pass
            try:
                b.lights[crystalScene[startNode-i]].state(on=False)
            except:
                pass
            time.sleep(0.5)
        b.groups[groups.livingRoom].action(scene=namedScenes['Flamesquall'])
        time.sleep(random.randrange(3,2*60,1))
        if random.randrange(1,20,1) >= 19:
            sounds = {0:'C:/Users/jonat/Downloads/QHueExperiments/sounds/volcano1.mp3'}
            playsound(sounds[random.randrange(0,len(sounds),1)])
        time.sleep(random.randrange(30,3*60,1))

def fangs():
    setup()
    purpleFire = [[0.645621,0.329347],[0.220051,0.100542],[0.221092,0.101100],[0.277731,0.131552],[0.615210,0.312997]]
    runEffect()
    while checkRunning() == True:
        for light2change in b.groups[groups.livingRoom]()['lights']:
            light2change.state(xy=purpleFire[random.randrange(0,len(purpleFire))],bri=random.randrange(50,254,1))
            time.sleep(0.2)

def rainbow():
    setup()
    maxcolor = 65535/6
    initcolors = [0,maxcolor,2*maxcolor,3*maxcolor,4*maxcolor,5*maxcolor]
    for i in range(25):
        j=0
        for light2change in b.groups[groups.livingRoom]()['lights']:
            newcolor = initcolors[j] + i*6000
            b.lights[light2change].state(on=True,hue=int(newcolor%65612),sat=254,bri=100)
            j+=1
            time.sleep(0.25)
            