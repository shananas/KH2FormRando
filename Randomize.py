import sys
import yaml
import random

currentDir = sys.argv[0].replace((sys.argv[0].split('\\')[-1]),'')

#Load obj.yml Template
f = open(currentDir+'objtemplate.yml')
f = yaml.safe_load(f)
g = {}

#UCM for each of Sora's worlds
forms = ['','_BTLF','_MAGF','_KH1F','_TRIF','_ULTF','_HTLF']
ZZ = [  84,  85,  86,2397,  87,  88,  89]
NM = [ 693, 998, 999,2398,1000,1001,1002]
TR = [1622,1641,1643,2400,1645,1647,1649]
WI = [1623,1642,1644,2401,1646,1648,1650]
XM = [2389,2390,2391,2399,2392,2393,2394]

#Do randomization
randomresult = [0,1,2,3,4,5,6]
random.shuffle(randomresult)
#Base can't dual-wield & Wisdom can't replace Final
#Reroll if those conditions aren't met
while not(randomresult[0] in [0,2,3,6] and randomresult[3] != 2):
    random.shuffle(randomresult)

#Make the new dictionary
for world in [ZZ,NM,TR,WI,XM]:
    for i in range(7):
        j = randomresult[i]
        g[world[i]] = f[world[j]] #Form[i] is turned into form[j]
        g[world[i]]['ObjectId'] = world[i] #Fix ObjectId
        if i == 0: #Enable Movement on whatever replaces Base Sora
            g[world[i]]['ObjectForm'] = 'SoraRoxasDefault'

#Write to obj.yml
h = open(currentDir+'obj.yml','w')
yaml.dump(g,h)
h.close()

#Write to mod.yml
def modymlcopy(old,new=False,platform=False,internal=False):
    if not '.' in old:
        old = 'obj/' + old + '.mset'
    if not new:
        new = old
    elif not '.' in new:
        new = 'obj/' + new + '.mset'

    h.write('- name: '+old+'\n')
    if platform:
        h.write('  platform: '+platform+'\n')
    h.write('  method: copy\n')
    h.write('  source:\n')
    h.write('  - name: '+new+'\n')
    if internal:
        h.write('    type: internal\n')

#Write static template
h = open(currentDir+'mod.yml','w')
h.write('title: Form Rando?\n')
h.write('original Author: Shananas\n')
h.write('assets:\n')
h.write('- name: 00objentry.bin\n') #Implement the objentry changes
h.write('  method: listpatch\n')
h.write('  type: List\n')
h.write('  source:\n')
h.write('  - name: obj.yml\n')
h.write('    type: objentry\n')
h.write('- name: 03system.bin\n')
h.write('  method: binarc\n')
h.write('  source:\n')
h.write('  - name: pref\n')
h.write('    method: copy\n')
h.write('    source:\n')
h.write('    - name: pref_0.bin\n')
h.write('    type: binary\n')
if randomresult[6] != 6:
    h.write('  - name: wmst\n')
    h.write('    method: copy\n')
    h.write('    source:\n')
    h.write('    - name: wmst_0.list\n')
    h.write('    type: list\n')
modymlcopy('magic/FIRE_1.mag') #Fix Final Form's magic
modymlcopy('magic/FIRE_2.mag')
modymlcopy('magic/FIRE_3.mag')
modymlcopy('magic/BLIZZARD_1.mag')
modymlcopy('magic/BLIZZARD_2.mag')
modymlcopy('magic/BLIZZARD_3.mag')
modymlcopy('remastered/magic/FIRE_1.mag/-0.dds',platform='pc',internal=True)
modymlcopy('remastered/magic/FIRE_3.mag/-0.dds',platform='pc',internal=True)
modymlcopy('remastered/magic/BLIZZARD_1.mag/-0.dds',platform='pc',internal=True)
modymlcopy('remastered/magic/BLIZZARD_2.mag/-0.dds',platform='pc',internal=True)
modymlcopy('remastered/magic/BLIZZARD_2.mag/-1.dds',platform='pc',internal=True)
modymlcopy('remastered/magic/BLIZZARD_3.mag/-0.dds',platform='pc',internal=True)
modymlcopy('remastered/magic/BLIZZARD_3.mag/-1.dds',platform='pc',internal=True)

#Write new form stuff
newbase  = randomresult[0] #The form that replaces Base
newlimit = randomresult[3] #The form that replaces Limit Form
for i in range(7):
    form = forms[i]
    if newbase == i and newbase in [2,3]: #Wisdom & Limit Effect Fix
        for world in ['','_NM','_TR','_WI','_XM']:
            h.write('- name: obj/P_EX100'+world+form+'.a.fm\n')
            if newbase == 2:
                h.write('  platform: ps2\n')
            h.write('  method: binarc\n')
            h.write('  source:\n')
            h.write('  - name: p_ex\n')
            h.write('    type: pax\n')
            h.write('    method: copy\n')
            h.write('    source:\n')
            h.write('    - name: obj/P_EX100'+form+'.pax\n')
            if newbase == 2: #'Base replaced by Wisdom' doesn't work on PC
                continue
            h.write('- name: obj/P_EX100'+world+form+'.a.us\n')
            h.write('  platform: pc\n')
            h.write('  method: binarc\n')
            h.write('  source:\n')
            h.write('  - name: p_ex\n')
            h.write('    type: pax\n')
            h.write('    method: copy\n')
            h.write('    source:\n')
            h.write('    - name: obj/P_EX100'+form+'.pax\n')
    if newlimit == i:
        if newlimit == 3: #Limit Form is vanilla
            modymlcopy('P_EX100_KH1F',internal=True)
            continue
        modymlcopy('P_EX100'+form,'P_EX100'+form+'_LIMIT') #Enable Limits
        
        #Ragnarok Fix
        h.write('- name: 00battle.bin\n')
        h.write('  method: binarc\n')
        h.write('  source:\n')
        h.write('  - name: ptya\n')
        h.write('    type: list\n')
        h.write('    method: copy\n')
        h.write('    source:\n')
        h.write('    - name: ptya'+form+'.list\n')
        
        #Limits' AI for New Form's MDLX
        for world in ['','_NM','_TR','_WI','_XM']:
            h.write('- name: obj/P_EX100'+world+form+'.mdlx\n')
            h.write('  method: binarc\n')
            h.write('  source:\n')
            h.write('  - name: limi\n')
            h.write('    type: bdx\n')
            h.write('    method: copy\n')
            h.write('    source:\n')
            h.write('    - name: limi_0.bdx\n')

        #Return Keyblade after Limits
        if newlimit in [1,4,5]: #Dual-wield forms
            form += '_R'
        modymlcopy('W_EX010'+form) #New Form's Weapon Moveset
    elif (i == 2 and randomresult[2] == 5) or (i == 4 and randomresult[4] == 5):
        modymlcopy('P_EX100_ULTF', 'P_EX100_ULTF_BLIZZ') #Enable movement
    else:        
        modymlcopy('P_EX100'+form) #Enable movement
        
for i in [0,2,4,5]: #Magic MSET
    if randomresult[i] == 1:
        modymlcopy('W_EX010_BTLF_R','W_EX010_BTLF_R_MAGIC')
    elif randomresult[i] == 3:
        modymlcopy('W_EX010_KH1F','W_EX010_KH1F_MAGIC')

if randomresult[6] != 6 and randomresult[3] != 6:
        modymlcopy('W_EX010_HTLF','W_EX010_HTLF_BASE')

h.close()
print(randomresult)
