![Workshop_header_template](/Workshop_header_template.png)

![Seth Kr3ll](/images/contributors/seth_k3rnll.png)
## Creator: **Seth Krn3ll**
---

# Krn3ll Guide to add brand new buildings to RTW

#### Modding area: 
* Buildings (strategic - battle map)
#### Required software: 
* Notepad (or other text editor)
* 3dsMax (or Blender)
* Graphic editor like Photoshop or GIMP
#### Summary: This tutorial explains how to add totally new buildings to the gameplay, both in strategic and battle map modes.

# Table Of Contents
* [Premise](#premise)
* [Adding Ambient Building to RTW](#ADDING-AMBIENT-BUILDINGS-TO-RTW)
* [Adding Game Buildings To RTW](#ADDING-GAME-BUILDINGS-TO-RTW)
	* [Preparation](#Adding-Game-Buildings-Preperation)
	* [Adding a new Game Building](#Adding-a-new-Game-Building)
	* [Adding the 3D Model of the new Building](#ADDING-THE-3D-MODEL-OF-THE-NEW-BUILDING)
		* [Using existing models](#Using-existing-models)
		* [Using brand new models](#Using-brand-new-models)
* [When you have errors](#When-you-have-errors)
## PREMISE:
Just to be clear: I will NOT explain HOW to model buildings here, just how to add them to the gameplay. Specifically, I will explain step to step how to:
Add new buildings in the building tree of the game
Add their 3d models to the building DB so that they will appear in game

Before starting, keep in mind there are different type of buildings you can add to the game.

**Ambient Buildings** are the simpler ones. They need much less steps then the others. They can’t have recruiting capabilities, they can’t have bonus capabilities, they do not affect campaign game and in battles they are merely obstacles for troops or scenario decorations and they are discussed in this tutorial.

**Game Buildings** are the ones buildable by the players during the game in the settlements. They affect both campaign and battle game, and they are discussed in this tutorial.

**Special buildings** are walls and towers and they are somehow more complicated to manage due to their multiple features. They will not be discussed here, you can check my Wall Modding tutorial there:
--> [Krn3ll's RTW wall modding guide](http://www.twcenter.net/forums/showthread.php?t=439235) 

## 1. ADDING AMBIENT BUILDINGS TO RTW
***
RTW host some buildings which are there just for decoration purposes. They shall indeed be improved to make them fully interactive with the game, host units or force passages in a city map, but those features will not be discussed here. Here I will only explain how to add or modify those models.

Files involved:
* **data\descr_items.db**
* **data\descr_items.txt**
* **data\descr_items\di_*.txt**
* **data\descr_building_battle.txt**
* **data\descr_building_battle\dbb_*_buildings.txt**
* **data\settlement_plans\CITYNAME_plan.txt**

As always, remember to backup those files before changing them, so if things go wrong you can always restore original situation.

We assume you already have the new model you want to add to the game.
Ambient buildings do not need specific text string nor they need to be added to any game related tree.
To have them in the game all you need is to have the models, register them in the game db and place them in the settlement plan where you want them to show up.

Lets say you want your new “MYHOUSE.cas” model in the game.

Put your "MYHOUSE.cas" model in ***data\models_building*** and if it uses new textures put them in ***data\models_building\textures***.

#### 1. Open ***data\descr_items.txt***
Add a line like “include di_MYOWN_buildings.txt”<br />
Save and close<br />

#### 2. Create a file named “di_MYOWN_buildings.txt”
* Type in it:
> ```
> type		MYHOUSE 
> lod
> max_distance	4000.0
> model_rigid	MYHOUSE.cas
> ```
* Save it in data\descr_items\ folder and close

#### 3. Open **data\descr_building_battle.txt**
Add a line like “include dbb_MYOWN_buildings.txt”<br />
Save and close

#### 4. Create a file named “dbb_MYOWN_buildings.txt”
Type in it:

> ```
>	MYHOUSE
>    {
>        stat_cat large_stone
>        localised_name ambient
>        level
>        {
>            min_health 1
>            battle_stats
>            item MYHOUSE
>            physical_info info_roman_small_temple.cas
>        }
>        transition default_large_stone
>        level
>        {
>            min_health 0
>            battle_stats
>            item roman_rubble_112x64
>            physical_info info_roman_rubble_112x64.cas
>        }
>    }
> ```

Three notes here:
1. The string “physical_info” tells the game which INFO file to be used to define some features of the building. In the example I put the “info_roman_small_temple.cas” but you’ll need to put there one compatible cas model with your own building.
If you are not able to create your own INFO files you’ll have to add here an existing INFO file, so chose one of an item which have similar dimension of your model, or you’ll have weird results in game.
I will discuss how to create the INFO files for your buildings in another tutorial, I’ll post here a link when its ready.

2. The “stat_cat” string tells the game the stats of resistance to damage of your building.
The stats I knew of are:
* small_wooden
* medium_wooden
* small_stone
* medium_stone
* large_stone

3. The “transition” paragraph tells the game what happens if your building is damaged/destroyed during battle. If you want it to be damageable/destroyable you’ll need either to create another model of your building remains when destroyed or to use in such paragraph the model of an existing building remains. If it’s the latter, pick the remains of a model with compatible dimensions. The “level” string is the level of damage of the building. You can add there more then one level of damage along with more then one model of your partially damaged building.
if you don’t want your new building to be damageable/destroyable, use such code:

> ```
> MYHOUSE
>     {
>         stat_cat indestructable
>         localised_name ambient
>         level
>         {
>             min_health 1
>             battle_stats
>             item MYHOUSE.cas
>             physical_info info_roman_small_temple.cas
>         }
>     }
> 	
> ```

Save your “dbb_MYOWN_buildings.txt” into ***data\descr_building_battle\*** folder and close it.

#### 5. Now you have to put your new building in some settlement plan where you’ll see it in game.
Go to **data\settlement_plans\** folder and open the settlement plan of the type where you want your building to show up.

In the *_plan.txt file are defined all the features related to that specific settlement plan type. Look for the “;AMBIENT” comment line, usually there are already some ambient buildings set there. If there’s no one, just add it at the end of the file, BUT be sure to add it INSIDE the last “}” which closes the file.
Add a line like this:
“MYHOUSE, 140, 150, 180.0, 0.0”
This string tells the game to put the model item “MYHOUSE” in that settlement map, at cords x 140 y 150, to rotate it of 180 degrees on his z axis and to have it at 0 meters altitude. You shall have a view of the settlement before deciding those parameters, otherwise your model shall be placed under a hill or collide with other buildings already present in that settlement at such position, or be put on a road and stop the passage of troops.

If you are just replacing some existing models with your one, then simply replace their names with your model’s name and use their original coordinates as they are in the settlement_plan.


Once all those tasks are done, save all, backup your descr_items.db file, rename or delete it and start the game. Game will freeze at starting screen or show errors, just ctrl-alt-canc, kill it, restart it. If you did everything correctly, You should have your buildings in the game.


## 2. ADDING GAME BUILDINGS TO RTW
***

### Adding Game Buildings - Preperation

First thing, BACKUP all the files involved. I suggest to backup a copy of the folders, so to be sure you can get back to start if things goes wrong.

Here is the list of files involved in the process:

**data\export_descr_buildings.txt**<br/>
This file lists all the buildings that can be built during the game, specifying which cultures can build them, the costs and times, features, bonuses and recruitments capabilities.

**data\text\export_buildings.txt**<br/>
Hhere all buildings are given a text description which will appears in game.

**data\text\building_battle.txt**<br/>
Here all buildings are given a text description which will NOT appears in game. Its needed to the game.

**data\settlement_plans\descr_settlement_plan.txt**<br/>
Here are listed the primary buildings, and you’ll have to add your new ones there. Are also set the city plans, and all the slots that can be called from the single settlement plan files.

**data\settlement_plans\[culturetype_settlementtype].txt**<br/>
Where " settlementtype " stands for each type of settlement in the game, forts and camps included. There you define all building models to be shown in each kind of settlement. You can specify coords and type for all kinda objects, including walls. It can list only models already listed in descr_settlement_plan, so if you want to customize settlements a lot you will have to work on descr_settlement_plan too.

**data\descr_items.txt**<br/>
This file enlist all buildings the game will manage. You need to add here all the new buildings you want to appear in the game. You can also include subfiles there, to keep them separated for culture, for example.

**data\descr_items.db**<br/>
This file is generated by the game when you start it. If there is already a descr_items.db the game will not generate a new one.

**data\descr_settlement_plan**<br/>
This one defines the single elements to be used in every city shown ingame. There are set association with every culture settlement single plans, groups of various building models to be shown in settlements and culture variations.

**data\descr_building_battle\dbb._*_.txt**<br/>
Those files enlist all 3d building models to the game. Here are specified the health stats, the different cas models to refer to and some other things.

### Adding a new Game Building

Lets say you want to add a new building named “MONOLITH”, buildable by Romans and Britons, with two levels named monolith1 and monolith2, which gives a some happiness to settlement population.

**1.** Open **data/export_descr_buildings.txt**, scroll to the end of it and add the new building tree. It will look like that:

>```
> building monolith
> {
>     levels monolith1 monolith2
>     {
>         monolith1 requires factions { romans, britons } 
>         {
>             capability
>             {
>                 happiness_bonus bonus 1
>             }
>             construction 1 
>             cost 400 
>             settlement_min town
>             upgrades
>             {
>                 monolith2
>             }
>         }
>         monolith2 requires factions { romans, britons } 
>         {
>             capability
>             {
>                 happiness_bonus bonus 2
>             }
>             construction 3
>             cost 800
>             settlement_min large_town
>             upgrades
>             {
>             }
>         }
>     }
>     plugins 
>     {
>     }
> }
>```

**2.** Open **data/text/export_buildings.txt** and add the description lines for the levels of your new building:
>```
>{monolith1} The wonderful lunar Monolith!
>{monolith1_desc} The lunar Monolith helps people read at night, so they love it. People is very happy to have it in the settlement.
>{monolith1 _desc_short} The lunar Monolith makes people happy.
>{monolith2} The Unbearable solar Monolith!
>{monolith2_desc} The solar Monolith gives all people a nice tan and makes all them say “Wohooo!”. People is very happy to have it in the settlement and they will love you for building it.
>{monolith2 _desc_short} The solar Monolith makes people happy.
>```

Add also a line to the name string at the end of the file:

>```
>{monolith_name} Wonderful Big Stones – Makes people happy
>```

**3.** Add some nice pictures to be seen in your building queue ingame.<br/><br/>
To do so you need to be able to use a graphic editor, like GIMP or Photoshop or something else. Find a nice picture you like and save it as your Building Card Picture with the name<br/>
**#roman_monolith1_constructed.tga**
in<br/>
data\ui\roman\buildings<br/>
Then resize to 78x62 pixels. If you are good with graphics add the alpha channel, if you dunno what is it, just forget it. Save that picture as<br/>
**#roman_monolith1.tga**
in<br/>
data\ui\roman\buildings<br/>
Then make a copy, resize it to 64x51 pixels and save it with the same name in data\ui\roman\buildings\construction

Do the same in barbarian building folders (as Britons are barbarian) and of course, name them
**#barbarian_etc** etc

At this point you can start the game and if you play as romans or as Britons you’ll find your new building available to be built in your settlements. You can play and benefit all the features of the monolith, but if you enter the settlement in tactical view, you will not see anything like a monolith. To have the monolith around in your battles, you’ll need to create and then add the 3d model to the models db, and that’s what I’m gonna explain now.

### ADDING THE 3D MODEL OF THE NEW BUILDING
If adding a new building to the game was pretty easy, adding a 3d model is all BUT easy. There are two ways I know to go for it, one is complicated, the other is utterly complicated.

#### Using existing models
The complicated way is to use an existing building of the game, which means you will somehow rename an existing building. To do so first thing you have to pick the existing building you want to be your monolith. Lets say you chose the barbarian bardic circle.

**1.** Open descr_settlement_plan.txt and first of all add monolith1 and monolith2 to the primary building list.<br/>
Then chose a slot to settle your new building. Slots are prefixed areas in the settlement plans where specific buildings may be built. Given you want the monolith to be buildable in roman and (barbarian) britons settlements, you must pick a slot that is present in both those culture settlements files. You also have to pick slots with adequate dimensions, which means you have to open in 3dmax the bardic_circle and see the dimensions it occupies, or at least check it in descr_settlement_plan.txt. Remember that if you use a slot for that building, you will not be able to build another building in that slot – so if you decide to use lets say the slot_160x128_missiles slot, then you will not be able to build the missile building if you build your monolith.

Best way is to create a brand new slot for your new building, something like a slot_monolith with the right dimensions. But you’ll have then to find the correct coordinates in romans and barbarian settlements to set your new slot. If you put it on a road, soldiers will run against it and get stuck there.
So if you go to create your own slot, then you’ll have to add it to all the settlement files you want the monolith to be buildable in.

**2.** Once found the right slot for your monolith, add a variant line to it. It will look like that:<br/>

>```
>variant
>{
>	cultures
>	{
>		roman
>        barbarian
>	}
>	buildings
>	{
>	    Monolith monolith1
>    }
>    bardic_circle_barbarian, 		0, 	0, 	0, 	0		
>}
>variant
>{
>	cultures
>	{
>		roman
>        barbarian
>	}
>	buildings
>	{
>	    monolith monolith2
>	}
>    bardic_circle_barbarian, 		0, 	0, 	0, 	0		
>}
>```

Consider that this way the 3d models shown ingame will be the bardic circle for both levels of your monolith, and for both romans and Britons. Of course you can use different models for cultures and levels if you want, but pay attention to dimensions of the models: if you use a model bigger then the slot you put it in, it may collide with other buildings or block roads.

In **descr_settlement_plan.txt** file you can also set the models for the building time of your monolith, or what to show if its not at all built. Here I try to stay at the basics.


**3.** Once you added your monolith to a slot and the slot is available in the settlement plans, you have to declare it in **data/text/building_battle.txt**<br/>
Easy step here: just add a line like:
>```
>{monolith1} My Monolith
>{monolith2} Again my Monolith
>```
Those lines never appears in game, ir at least I never saw them. But they are needed to have the building working.

**4.** Now you have to include your new building to the models db of the game. To do so, first thing open<br/>
**descr_building_battle.txt**
and add the monolith entry like that:

>```
>monolith1
>{
>    stat_cat large_stone
>    localised_name monolith1
>    level
>    {
>        min_health 1
>        battle_stats
>        item bardic_circle_barbarian
>        physical_info	bardic_circle_barbarian_info.CAS
>    }
>    transition default_large_stone
>    level
>    {
>        min_health 0
>        battle_stats
>        item		roman_rubble_112x64
>        physical_info	info_roman_rubble_112x64.cas
>    }
>}
>
>monolith2
>{
>    stat_cat large_stone
>    localised_name monolith2
>    level
>    {
>        min_health 1
>        battle_stats
>        item bardic_circle_barbarian
>        physical_info	bardic_circle_barbarian_info.CAS
>    }
>    transition default_large_stone
>    level
>    {
>        min_health 0
>        battle_stats
>        item		roman_rubble_112x64
>        physical_info	info_roman_rubble_112x64.cas
>    }
>}
>```

At this point, given you used an existing model, there is nothing else you have to do with files. But you have to delete the existing **descr_items.db** (which you have already backupped, haven’t you?) and then run the game.
You’ll have some errors, just ctrl-atl-canc and stop the program. If you have made no mistakes, the program creates the new **descr_items.db** including your monolith.
Restart the game, and this time there should be no errors. If you play as romans or Britons you’ll be able not just to build the monolith but also to go and see it in your cities in tactical view. O well, you’ll see the bardic_circle, of course, but the cursor will say “Monolith” and you will be happy like the people in your settlement are.

Ok this was the complicated way, which is not that much because, as I just outlined, you’ll see the same old models in your game. So lets go to see how to add a completely new model to your new building. And, well, it will be not that easy.<br/>
Did I already say that?

#### Using brand new models

**1.** To add a brand new model for your monolith, first thing you have to do is to create that model. <br/>You can do so by importing an original item form the game that have similar dimensions to the one you want to create and this also keep its own collision INFO file – or go on and create your new model with its own INFO file.

If you keep and existent INFO file as reference for your new building, just import in 3dsMax the vanilla model and then start to create your own building keeping it within the dimensions of the original item. Once you created your new model, remove the original item and all its textures, add your own textures and finally export it as
monolith1_high.cas<br/>
Put it in<br/>
**data\models_building**<br/>
And put your textures in<br/>
**data\models_building\textures**

If you want to make a new building with its own INFO file, after you create the .cas for your new building you have to create the INFO file for it.
To know how to do so, lets first explain what are INFO files and how they work. INFO files tell the game some functionalities of the model they refer to. Including their walkable/non walkable areas, if and where the camera will go around them or get through them, and some more complicated features like tunnels, platforms, siege points and the like.
Here I will explain just the two basic ones needed to create functional INFO files for simple buildings, which are “collision” and “collision_3d” issues.

* Collisions are simple squares, made on ONE SINGLE element (even better one single polygon) with no holes inside. They define the areas where troops or peasants will NOT be able to walk. If the building is just a cube, the basic collision file is a square a little bigger then the cube base. The units will walk into it and stop. If you don’t put working collision files in the INFO file, units will walk up on your buildings. If you need to add more then one collision area, you have to name them “collision_01”, “collision_02”, etc.
* collision_3d is the general shape of your building in 3d. It mainly have two functions: telling the game that the camera will have to go around the building and not through it and blocking projectiles. Given so, it may be used to create fake roofs to some areas where the camera will be able to pass into, or invisible fences to protect troops from arrow attacks. Staying at the basics, the collision_3d is just a shape of the same size of your building, and that’s all. A good modeler will usually simplify it a lot, to make easier the job of the game engine.<br/>
If you’re lazy, you can do it in the easy way by just keeping the model as it is, collapsing all its part in one object and naming it “collision_3d” then exporting it as *monolith1_INFO.cas* and *monolith2_INFO.cas*. Put it in
**data\models_building\info**<br/>
Given the game engine will have to deal with all the polys of all the objects around, its strongly advised you simplify the object in the INFO file.

**2.** Follow the point **1.** of the complicated way about descr_settlement_plan.txt
I strongly suggest you to create your own slot for your own building.

**3.** Add your monolith to your slot, this time with no references to bardic_circle.

**4.** Once found the right slot for your monolith, add a variant line to it. It will look like that:
>```
>variant
>{
>     cultures
>	{
>	    roman
>         barbarian
>     }
>	buildings
>	{
>	    monolith monolith1
>     }
>     monolith1, 		0, 	0, 	0, 	0		
>}
>variant
>{
>    cultures
>     {
>	    roman
>         barbarian
>	}
>	buildings
>	{
>	    monolith monolith2
>     }
>     monolith2, 		0, 	0, 	0, 	0		
>}
>```

**5.** Follow step **3.** of complicated way:
**data/text/building_battle.txt**
>```
>{monolith1} My Monolith
>{monolith2} Again my Monolith
>```

**6.** Just like complicated way, add your entry to **descr_building_battle.txt** but no need to use the item “bardic_circle_barbarian” because you’re gonna use your brand new item “monolith1” and “monolith2”.<br/>
Here it is:
>```
>monolith1
>{
>    stat_cat large_stone
>    localised_name monolith1
>    level
>        {
>        min_health 1
>        battle_stats
>        item monolith1
>        physical_info	monolith1_INFO.cas
>        }
>    transition default_large_stone
>    level
>    {
>        min_health 0
>        battle_stats
>        item		roman_rubble_112x64
>        physical_info	info_roman_rubble_112x64.cas
>    }
>}
>
>monolith2
>{
>    stat_cat large_stone
>    localised_name monolith2
>    level
>    {
>        min_health 1
>        battle_stats
>        item monolith2
>        physical_info	monolith2_INFO.cas
>    }
>    transition default_large_stone
>    level
>    {
>        min_health 0
>        battle_stats
>        item		roman_rubble_112x64
>        physical_info	info_roman_rubble_112x64.cas
>    }
>}
>```

Note that you keep using roman_rubble_112x64 as default transition item. If you are good, you’ll probably create some more ambient objects to fit the building stage / destroyed stage of your own building. Either, try to use some default item which have similar dimensions.

**7.** Now you need to have the game creating the monolith items. To do so, you’ll need one more step then the complicated way. Open **data\descr_items.txt** and add your monolith entry as:
>```
>type		monolith1
>lod
>max_distance	4000.0
>model_rigid	monolith1_high.cas 
>
>type		monolith2
>lod
>max_distance	4000.0
>model_rigid	monolith2_high.cas
>```

This is the simplified version. You should actually have two or three cas files, high, med and low, to be used at different distances. That means you have to create three or more .cas files for each new building you create.
But well, for now lets work with just the high one.

**8.** Now again you have to get rid of the **descr_items.db** (backup, backup!) and start the game. Game shows errors, ctrl-alt-canc, kill it, restart it. You should have your buildings in the game.

#### When you have errors

Now, there are about 1 million chances you’ll get errors. Trying to write a troubleshooting on this process is simply ridiculous, but let me share a few recurring problems:

a) Game just does not load, no error messages – something is wrong in descr_settlement_plan.txt usually a not closed bracket or something similar.
Game loads, you enter the campaign, no traces of your buildings in game – something wrong written in descr_items.txt or in descr_building_battle.txt
Check if the game created the monolith1 and 2 items in data\items\ folder.
b) Game loads, but when you go in tactical view, loading freezes – you missed adding the textures.
c) All works, but your buildings are missing sides or show weird colors – 50% chances that the exporting procedure did not worked very well. It happens, export them again – no need to rebuild the db. The other 50% chances are – let me be rude – that you are a poor modeler.


Have fun.<br />
Seth Krn3ll

***
added by: **Dagovax**

*[Original post](http://www.twcenter.net/forums/showthread.php?437930-Krn3ll-Guide-to-add-brand-new-buildings-to-RTW-1-5)*<br />


