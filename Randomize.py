import os
import yaml
import random

currentDir = os.path.realpath(__file__).replace(os.path.basename(__file__),'')

f = open(currentDir+'objtemplate.yml')
f = yaml.safe_load(f)
g = {}

#UCM for each of Sora's worlds
ZZ = [  84,  85,  86,2397,  87,  88,  89]
NM = [ 693, 998, 999,2398,1000,1001,1002]
TR = [1622,1641,1643,2400,1645,1647,1649]
WI = [1623,1642,1644,2401,1646,1648,1650]
XM = [2389,2390,2391,2399,2392,2393,2394]

#Do randomization
base = random.choice([0,2,3,6]) #No Dual-Wield
randomresult = [0,1,2,3,4,5,6]
random.shuffle(randomresult)
while randomresult[0] != base:
    random.shuffle(randomresult)

#Make the new dictionary
for world in [ZZ,NM,TR,WI,XM]:
    for i in range(7):
        j = randomresult[i]
        #Form[i] is turned into form[j]
        g[world[i]] = f[world[j]]
        if i == 3: #Replaces Limit Form
            mset = ['','_BTLF','_MAGF','_KH1F','_TRIF','_ULTF','_HTLF']
            mset = 'P_EX100'+mset[j]+'_LIMIT.mset'
            g[world[i]]['AnimationName'] = mset

#Final fixes
for i in g:
    g[i]['ObjectId'] = i
    if i in [84,693,1622,1623,2389]:
        g[i]['ObjectForm'] = 'SoraRoxasDefault'

h = open(currentDir+'obj.yml','w')
yaml.dump(g,h)
h.close()
