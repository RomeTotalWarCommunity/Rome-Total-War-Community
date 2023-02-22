![Workshop_header_template](/Workshop_header_template.png)

---

# Solved Problems

This file is a storage for known problems and issues which we modders encountered in our experience and managed to resolve in some way or another. Please keep the cases as short and informative as possible, in the format Problem -> Solution.

## Table Of Contents
* [Generic](#generic)
* [Campaign Map](#campaign-map)
* [Modeling and Text Editing](#modeling-and-text-editing)
	* [Modeling](#modeling)
	* [Text Editing](#text-editing)
* [Music](#music)
* [Settlement Modding](#settlement-modding)
* [Scripting](#scripting)

## Generic

**Problem** *found by* **EdwinSmith_Feral**<br/>
Random Errors or limits that people might hit:

**Solution**<br/>
I have (slowly) been adding bits of info we have looked up to help modders to this page so if you have an issue it's worth having a quick check here: https://github.com/FeralInteractive/romeremastered/blob/main/documentation/feature_guides/MiscellaneousTips.md

***

**Problem** *found by* **Lanjane**<br/>
When the game launches, you get an empty warning / error message, but the game seems to be running just fine.

**Solution**<br/>
The error appears due to combined length of the paths and folders in the modfolder being too long. The easiest fix is to make the name of the mod folder shorter, but you can also get rid of any spare 'blah_blah_copy (01)_copy' type files and folders in there, and don't do anything like unpacking the animations in the mod folder which gets you recursive paths of data/animations/data/animations/blah_blah etc..

Update: to get rid of the error, your total path to a file including the modfolder name should be shorter than 100 symbols
example of path (89 symbols)
```
Downfall\data\characters\textures\BI_unit_steppe_horde_chosen_warriors_ostrogoths.tga.dds
```

***

**Problem** *found by* **Lanjane**<br/>
Crash when you try to move a unit out of the army or out of city in campaign (when a new lesser general should be created). Also custom battles are crashing.

**Solution**<br/>
1) Wrong default ethnicity set for a faction in `descr_sm_factions.txt`
2) This type of CTD also happen because of names. If you for example include "egypt_men", "egypt_women", and don't include "egypt_surnames" etc. (Thanks Crazyroman for info) 

***

**Problem** *found by* **Eduardo Sousa**<br/>
Captain cards not showing up in game despite being correctly named. 

**Solution**<br/>
the folder is incorrectly named. The captain banners folder is the only one in the ui folder that does not have an underscore instead of space.

Simple one but hard to spot.

***

**Problem** *found by* **Lanjane**<br/>
Game doesn't accept "extras" animations even if correctly referenced in descr_skeleton_feral_overrides.txt

**Solution**<br/>
The modfoldered skeletons.dat need to contain the skeletons related to those animations, plus pack.dat needs to have "default" versions of those animations


## Campaign Map

**Problem** *found by* **Arcyllis†**<br/>
Some of the faction_relations entries were not working properly (when listing multiple factions in the same entry, only the first one would get read on certain entries).

**Solution**<br/>
Separate each faction onto it's own separate entry, doing them one at a time instead of as a group. It may make your code a bit messier, but it seems to fix the problem.

***

**Problem** *found by* **Lanjane**<br/>
Campaign loads, but any battle crashes and settlement view also crashes. When you try to quit to the main menu, the game also crashes with no information in logs. Custom battles work.

**Solution**<br/>
Check carefully your descr_character.txt and descr_model_strat.txt files. In my case, it was additional strat character type which wasn't even used by any faction, which missed RR-specific lines as "male", "Tired Very Tired" etc. Double check if new references keep the same syntax as the existing ones.

***

**Problem** *found by* **Lanjane**<br/>
when you add new ancillaries, game starts to complain about descriptions for RR merchant ancillaries (like Caravan Leader etc.) and refuses to load. When you delete all RR-specific ancillaries from the file, the game loads with vanilla ancillaries plus the modded ones added.

**Solution**<br/>
??? (TBD, still yet to figure out)

***

**Problem** *found by* **Lanjane**<br/>
Campaign does not start when you add a new faction to the game, but didn't add the faction to campaign.

**Solution**<br/>
Even if the faction is not needed for this specific campaign, you still need to add it to victory conditions file and descr_strat.txt file (as dead_until_resurrected)

***

**Problem** *found by* **pyruvic_acid**<br/>
When adding regions to the map the game crashes right after starting a campaign without seeing a loading bar.

**Solution**<br/>
The problem is likely due to a typo or placing things in the wrong section. An example: putting armies that belong to a faction in the slave section. In the slave faction section generals require a subfaction to be assigned which generals belonging to a regular faction ofcourse do not have.

***

**Problem** *found by* **Dagovax**<br/>
CTD with a scripted campaign for Mac users only, where some UI stuff is scripted to be executed once campaign loaded.

**Solution**<br/>
This can be caused due to `disable_cursor` and `enable_cursor`. Not tested with other UI stuff. I removed them and the crash was gone.

***

**Problem** *found by* **Eduardo Sousa**<br/>
Porting an OG descr_strat file and the game crashes.

**Solution**<br/>
(A lot more issues are possible, but this one is hard to see) : Spy ancillary Catamite in OG has been changed to Networker in RR. Beware of that.

***

**Problem** *found by* **Lanjane**<br/>
Campaign crash with no error, `map.rwm` is generated.

**Solution**<br/>
(one of the many) unknown character to kill for the kill_character command at turn 0 script.

***

**Problem** *found by* **Dagovax**<br/>
Land mass crash. Thinking having a big map with a lot of land and internal seas is a great idea: OG doesn't like it (It does for RR, but who wants to create a map in RR to test the heights/groundtypes etc). Adding a lot of 'placeholder' regions and assigning armies to them don't work.

**Solution**<br/>
Make your map smaller. I decreased it to 70% and no CTD (not even with only 2 huge regions and 2 armies).

***

**Problem** *found by* **Lanjane**<br/>
Campaign doesn't start after you placed watchtower or fort in descr_strat (kick to menu)

**Solution**<br/>
The tile you placed the fort or watchtower, belongs to a different province. Coordinates should point to the tile belonging to the exact province mentioned in the end of descr_strat. 
Although the error message you get doesn't tell anything about watchtower, the line number it refers does.

Example:
>```
>region Phoenicia
>road_level 0
>farming_level 0
>famine_threat 0
>watchtower     217 45
>```

***

**Problem** *found by* **Shoebopp the Fluffy**<br/>
Crashes during a campaign mode battle seconds after any of these events occur:
1. Engaging a certain enemy unit
2. Engaging any enemy unit during a defensive siege sally battle

**Solution**<br/>
Disable daylight-saving mode on your laptop/computer

***

**Problem** *found by* **Dagovax**<br/>
You  notice that AI is passive against AI super faction factions (most noticable if you have multiple super factions setup).

**Solution**<br/>
Apparently there is an hardcoded factor in OG and RR, making it impossible for AI factions with less than 7 regions to attack another AI inside a superfactions. For example, carthage in base game (6 starting regions) is not allowed to attack roman factions (Scipii) from the start. Gauls on the other hand have 7 starting regions and therefore can attack the Julii.

So either wait for faction to reach 7 regions or give them 7 from the start.

***

**Problem** *found by* **Lanjane**<br/>
CTD when a faction within a superfaction attacks a neutral or allied faction.

**Solution**<br/>
Every single faction existing in the descr_sm_factions.txt file should also be listed in the descr_strat.txt file of your campaign  (found by Dagovax)

***

**Problem** *found by* **Dagovax**<br/>
AI is very passive and is not attacking other AI's settlements.

**Solution**<br/>
Be sure to have the `AI Improvement` toggle set to REMASTERED.

![AI Improvement Toggle](/images/documentation/ai_improvement_toggle.png)

As modder you can override this toggle state and lock it, so that players can't switch to CLASSIC.<br/>
`toggles\toggle button states.txt`

![AI Improvement File](/images/documentation/ai_improvement_file.png)

***

**Problem** *found by* **Lanjane**<br/>
You are getting KTM when trying to launch campaign after you've added new factions to the game, and the error logs contain something like this:
>```
>Faction baktria listed as present in header, but not supplied.
>Script Error in Q:\Feral\Users\Default\AppData\Local\Mods\My 
>Mods\Barbarian_Empires/data/world/maps/campaign/imperial_campaign/descr_strat.txt, at line 29928, column 1. Faction baktria listed as present in header, but not supplied.
>```
**Solution**<br/>
Missing empty line at the end of descr_standards.txt file. To be on safe side, make sure to have an empty line at the end of each file in RR! Engine ignores the last line for some files, so it might ignore your data if you don't provide the empty line.

***

**Problem** *found by* **Kirsi**<br/>
>```
>Landmass Limit
>n < N Failed
>checked array access out of range
>```
**Solution**<br/>
The 'landmass' limit is still in the game; it's 22 landmasses. Where landmass = land that's fully separated by ocean & doesn't have regions that overlap onto other landmasses. Landmasses that are connected by land bridges count as just 1 landmass. And same goes for if you have say an island but put 1 pixel of it's region color anywhere on the mainland. *(That's the way you get around the landmass limit!)*

***

**Problem** *found by* **Kirsi**<br/>
>```
>Generating default settlement in region  (189)
>```
**Solution**<br/>
Crash caused by placeholder region #189 being too large (we're talking couple hundred pixels) & having too many 1 pixel islands, solved by splitting it into 2 placeholder regions.

***

**Problem** *found by* **Kirsi**<br/>
>```
>edge_count <= 3 Failed
>edge_count <= 3 Failed
>WORLD_MAP river crossroads are forbidden (too many nasty permutations)
>```
**Solution**<br/>
Crash caused by bad map_features. Accidentally had 4 pixels of river in a square.

***

**Problem** *found by* **Kirsi**<br/>
Crash after loading bar filled when launching campaign. Map.rwm generated
>```
>verts_used < MAX_REGION_BORDER_VERTICES Failed
>too many verts!!!
>```
**Solution**<br/>
map_regions had a region with 'too many vertices', redrawing the border fixes it.

***

**Problem** *found by* **Kirsi**<br/>
>```
>script error "trying to place [settlement] in this region (region name), but it already has a >settlement [settlement]"
>script error "trying to place [settlement] in this region (region name), but it already has a >settlement [settlement]"
>```
**Solution**<br/>
Problem probably caused by 'something' happening that makes the mentioned region 'too big', solved by reducing the region size. Though, this region worked fine as one of the 10 base regions when map was empty.

***

**Problem** *found by* **Kirsi**<br/>
Crash on start new campaign, after "generating trade routes", no map.rwm, no pop up error log. This is crashing right before "Generating regions" should occur.
>```
>generating trade routes
>```
**Solution**<br/>
Problem with map_features again, 4x4 pixel bit of river (blue), same problem as the previous one, but resulted in a different message - in this case, no message.

***

**Problem** *found by* **Kirsi**<br/>
>```
>"unable to get name for region '' from stringtable"
>```
**Solution**<br/>
descr_regions cannot have blank lines at the start of the file before region name

***

**Problem** *found by* **Kirsi**<br/>
>```
>Crash on scrolling over on campaign map
>```
**Solution**<br/>
Faction name for culture in descr_region is not listed in descr_strat under playable or non playable, resulting in no factions of that culture present.

***

**Problem** *found by* **Kirsi**<br/>
>```
>Generating default settlement in region  (189)
>Generating default settlement in region  (189)
>type < MAX_FACTIONS Failed
>you are trying to retrieve an invalid faction
>index < m_num_records Failed
>DATABASE_TABLE error found : index out of range.
>```
**Solution**<br/>
Caused by a city with duplicate region color in descr_regions & missing the actual region color for that city.

***

**Problem** *found by* **Kirsi**<br/>
Kick back to menu when trying to load campaign, happen after editing coordinates in descr_strat, no useful error message.
>```
>BATTLE_ALLIANCE_STATS::clear() setting battle result to none
>```
**Solution**<br/>
Caused by faction's character being assigned to a settlement that is not listed in descr_strat as belonging to that faction. Sometimes doing so causes no error, sometimes this happens.

***

**Problem** *found by* **Kirsi**<br/>
Crash on start campaign, does generate map.rwm
>```
>attaching region
>attaching region Bactria(1) to faction(slave), giving them 486 triumph points
>Created a port attached to settlement 'Patala', faction 'slave'
>Generating default settlement in region  (10)
>type < MAX_FACTIONS Failed
>you are trying to retrieve an invalid faction
>type < MAX_FACTIONS Failed
>you are trying to retrieve an invalid faction
>```
**Solution**<br/>
Caused by repeat region color in descr_regions. The region after the one listed last in the log is *supposed to be* the one where the 1st instance of the duplicate color in descr_regions, but it can also just be listing a completely unrelated region!

***

**Problem** *found by* **Kirsi**<br/>
>```
>Error loading region: Region label 'Luoyang_R' not found
>```
**Solution**<br/>
Changed internal region name, all appropriate files updated. Problem persisted until deleting map.rwm, even though that shouldn't be required.

***

**Problem** *found by* **Kirsi**<br/>
>```
>Generic Error:
>SettlementBuildingExists needs a settlement. ([text])
>```
**Solution**<br/>
Delete map.rwm

***

**Problem** *found by* **Kirsi**<br/>
>```
>Script Error in Q:\Feral\Users\Default\AppData\Local\Mods\Local Mods\Local Mod/data/world/maps/campaign/imperial_campaign/descr_strat.txt, at line 13314, column 83. duplicated character name in this faction
>```
**Solution**<br/>
Duplicate 'named character' name in Slave faction. 'General' cannot share a name with 'Named_Character'.

***

**Problem** *found by* **Kirsi**<br/>
>```
>descr_strat.txt, at line 6104, column 12. could not create settlement at script line 6104.
>```
**Solution**<br/>
Settlement defined in descr_regions / descr_strat, but region is not drawn on map_regions.tga

## Modeling and Text Editing

### Modeling

**Problem** *found by* **Eduardo Sousa**<br/>
RR shows white lines around models (especially noticeable in RR modified ones).

**Solution**<br/>
This happens when the texture non-opaque pixels (=/= transparent pixels). Transparent pixeld (= deleted) do not show in any way, however, for non-opaque pixels, the game apparently fills them in with white pixels, causing the white lines. This issue is easily encounterable when reskinning or texturing your new models with existing parts.

If anyone knows of an easy way to make all non-opaque pixels in a texture opaque with their color that could be a good addition here.<br/>
Edit: apparently this can also be cause due to compression methods when exporting the textures. See [#remaster_modding_info](https://discord.com/channels/558359897394118687/837357688932532224) for a pinned message with a link on this

***

**Problem** *found by* **Eduardo Sousa**<br/>
Remastered cavalry units have the sheath clipping into their leg.

**Solution** (Potentional)<br/>
Rig the sheath to their thigh bone. Haven't tried this in game yet with in game animations, but in blender it seems to work fine. (also might depend on the size and shape of the sheath)

***

**Problem** *found by* **Lanjane**<br/>
You are getting instant crash when trying to launch a battle with some unit (usually ported from original RTW). In the logs, there's a message like "min <= max Failed you are trying to get invalid faction"

**Solution**<br/>
(One of the possible solutions): Check how many LODs the unit has assigned. If there's more than 4 LODs set up in descr_model_battle.txt, the game will crash. NB: ping Vartan to update OG2RR converter some day

***

**Problem** *found by* **Lanjane**<br/>
Flickering shields/wrong looking shields for ported units (like the bottom of the shield rendered on top and vise versa).<br/>
Also may be too dark/wrong looking hairs/plumes/cloaks/cheekguards etc.

**Solution**<br/>
You need to edit the 3D model of the unit. RR engine renders textures on both sides of any surface unlike original game engine, and super flat objects like the original oval shields for example have problems, because the engine gets counfused (it's called Z-fighting in 3D modelling terminology).
For the shields: you need to open the model in Blender and move the bottom of the shield little bit away from the top of the shield, or replace the shield object completely with a new 3D shield object
For hairs/plumes/cloaks/cheekguards, usually just deleting the secondary surface responsible for the "backside" of the object is enough

### Text Editing

**Problem** *found by* **Dagovax**<br/>
You are a bad modder and did everything mount-related wrong in multiple mods without knowing it was broken (mounts don't have correct hitbox).

**Solution**<br/>
`radius` should always be a bigger number than `x_radius`.

***

**Problem** *found by* **Dagovax**<br/>
You are looking for the correct `radius` and `x_radius` of a mount, but never knew how to correctly calculate it.

**Solution**<br/>
The collision of a mount is in the form of an ellipse, and the radius parameters are in meters. So in 3ds max (I guess too in blender), you can draw an ellipse around your mount and set the position to `0,0,0`:

![Mount Collision](/images/documentation/mount_collision.png)

The `radius` is here the length, so it is 9,75.
The `x_radius` of the mount is the width, so 4,049 
Then you need to divide these numbers by two and you get the correct collision boundaries:

![Maus Mount](/images/documentation/maus_mount.png)

You can clearly see that in game as result:

![Maus In-game](/images/documentation/maus_ingame.png)

***

**Problem** *found by* **Galvanized Iron Raptor**<br/>
The game mechanics by default make chariots massacre cavalry, but you want them to just be strong VS infantry.

**Solution**<br/>
Add a negative mount effect VS horse to the chariots. Screenshots attached are of two battles between Scythed Chariots and Praetorian Cavalry. First two show the typical outcome of unmodified chariots. Last two show the outcome when the only modification made to the Scythed Chariots is giving them "mount_effect            horse -50" in the EDU.

This was tested on RR. I am not sure whether "mount_effect" is equally moddable on OG Rome.

![Chariot & Mount Effect](/images/documentation/chariot_mount_effect.png)

## Music

**Problem** *found by* **Lanjane**<br/>
Battle crash after you edited music.

**Solution**<br/>
Either a music track you refer to is missing, or it contains a bad symbol in the name (There can be only latin letters, numbers or "-" and "_").

***

**Problem** *found by* **__tartaros__**<br/>
I can not hear my new sounds

**Solution**<br/>
Also, if you mod the descr_sounds.txt and/or vanilla's (or edited) sounds folder in your mod. Run the game with 1 time with the command **snd_save_events**. This will create music states. Otherwise you'll crash on custom battle.

## Settlement Modding

**Problem** *found by* **Lanjane**<br/>
Game crashes with no message in logs when you try to view your settlement on the battle map in campaign (LBC view).

**Solution**<br/>
Missing or corrupted model referenced in `descr_lbc_db.txt` (Note that if there's no reference at all, the game will not crash but the city will just appear empty with no citizens walking on the streets).

## Scripting

**Problem** *found by* **Dagovax**<br/>
Campaign crashes without anything useful in message_log, but it is gamebreaking. You have a background script with monitors that give trait points:
```
console_command give_trait_points Gandalf-g FellowshipContent 1
```
Looking at the scripting_log with verbose_script_logging on will tell you the game crashed executing this command.

**Solution**<br/>
This specific character is not alive (anymore), and can't be found by this script section.
To solve it, you need to wrap the command around a checker if he is alive. You can either do that by checking certain ancillaries, or doing this:
>```
>; check if Gandalf is alive first to prevent CTD
>if I_CharacterNameNearTile gondor Gandalf-g, 1000 1,1
>	console_command give_trait_points Gandalf-g FellowshipContent 1
>end_if
>```


