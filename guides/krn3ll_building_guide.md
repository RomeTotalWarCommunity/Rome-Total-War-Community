![Workshop_header_template](/Workshop_header_template.png)
# Krn3ll Guide to add brand new buildings to RTW

## Creator: ![alt text](seth_k3rnll.png "Seth Krn3ll") *Seth Krn3ll*
---

#### Modding area: 
* Buildings (strategic - battle map)
#### Required software: 
* Notepad (or other text editor)
* 3dsMax (or Blender)
* Graphic editor like Photoshop or GIMP
#### Summary: This tutorial explains how to add totally new buildings to the gameplay, both in strategic and battle map modes.

## PREMISE:
Just to be clear: I will NOT explain HOW to model buildings here, just how to add them to the gameplay. Specifically, I will explain step to step how to:
Add new buildings in the building tree of the game
Add their 3d models to the building DB so that they will appear in game

Before starting, keep in mind there are different type of buildings you can add to the game.

**Ambient Buildings** are the simpler ones. They need much less steps then the others. They can’t have recruiting capabilities, they can’t have bonus capabilities, they do not affect campaign game and in battles they are merely obstacles for troops or scenario decorations and they are discussed in this tutorial.

**Game Buildings** are the ones buildable by the players during the game in the settlements. They affect both campaign and battle game, and they are discussed in this tutorial.

**Special buildings** are walls and towers and they are somehow more complicated to manage due to their multiple features. They will not be discussed here, you can check my Wall Modding tutorial there:
--> [Krn3ll's RTW wall modding guide](http://www.twcenter.net/forums/showthread.php?t=439235) 

## ADDING AMBIENT BUILDINGS TO RTW
***

## ADDING GAME BUILDINGS TO RTW
***

Now, there are about 1 million chances you’ll get errors. Trying to write a troubleshooting on this process is simply ridiculous, but let me share a few recurring problems:

a) Game just does not load, no error messages – something is wrong in descr_settlement_plan.txt usually a not closed bracket or something similar.
Game loads, you enter the campaign, no traces of your buildings in game – something wrong written in descr_items.txt or in descr_building_battle.txt
Check if the game created the monolith1 and 2 items in data\items\ folder.
b) Game loads, but when you go in tactical view, loading freezes – you missed adding the textures.
c) All works, but your buildings are missing sides or show weird colors – 50% chances that the exporting procedure did not worked very well. It happens, export them again – no need to rebuild the db. The other 50% chances are – let me be rude – that you are a poor modeler.


Have fun.
Seth Krn3ll

***
*[Original post](http://www.twcenter.net/forums/showthread.php?437930-Krn3ll-Guide-to-add-brand-new-buildings-to-RTW-1-5)*
added by: **Dagovax**

