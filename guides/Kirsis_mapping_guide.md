# KIRSI'S MAPPING GUIDE

*(Open this in a Markdown editor!)*

## Introduction

This guide is meant to be a tutorial for mappers to explain how to make maps with the same visual style as mine. It's not intended to show you how to make a new map from scratch. I'm mainly just going to show you how I compile the source imagery and what my workflow looks like to get results like this:

![alt text](https://i.imgur.com/Y50ul58.jpg)

![alt text](https://i.imgur.com/n7qxUGU.jpg)

![alt text](https://i.imgur.com/e0NWOc5.jpg)

----------

### What this will cover

- Getting and setting up the source images for my maps
- How my PSD files are organized
- Techniques for painting the various TGAs
- Workflow
- How to use IWTE to render your map (customizing textures, task file setup)
- Documentation of various crash causing error messages from the message_log

### What this will not cover

- How to set up your own template map - (there are various tutorials out there already)
- What the correct size ratio & max sizes are for all the TGAs - (again, there are tutorials already)
- How to make 'land bridges' - (there's a tutorial)
- How to set up each text file associated with the campaign map (descr_regions, descr_strat, etc)
- How to install IWTE correctly

### Tools I Use

- Wacom cintiq tablet - infinitely better than using a mouse, unless you hate yourself
- Photoshop - all of the image/brush settings I list here are for pshop; if you're using gimp, sorry but you're on your own!
- Illustrator - this is just for making an outline map
- G.Projector - for map projection https://www.giss.nasa.gov/tools/gprojector/
- Typora (or any other markdown editor) - easy way to keep notes & incorporate tables for region/faction planning. It's what I'm writing this whole guide on.
- IWTE - http://www.twcenter.net/forums/downloads.php?do=file&id=2741
  - Refer to https://wiki.twcenter.net/index.php?title=IWTE_-_Rome_Remastered_Functions
  - Keep in mind, IWTE renders the map mesh as multiple square sections, with a max of 22 squares on any one axis. As such you will want your map ratio to be 22 by X. 22x22 supposedly causes stability issues. My map is 22x19 and works fine.
- IWTE texture pack V2 - https://drive.google.com/file/d/1TnICOKHdNzf0n5vmKbyvZjAGX8MnDVQI/view?usp=sharing
  - You don't need to download this if you're going to use my texture set.

- **My current entire texture set** - https://drive.google.com/drive/folders/1OscwU1sPDAxdmFz_gGpDHYE-PH449L9Y?usp=sharing
  - This folder will be the most up to date place for my textures as I make edits to them in the future.
  - (This one includes the IWTE textures that I still use)
  - Make sure to view the readme for how to set it up and use it.


### Optional Tools

- ArcMap - more versatile for compiling the raw GIS data & doing map projections, but the UI is absolute garbage and unless you've taken a class for it, you'll likely be lost. I don't recommend this unless you're like a GIS engineer, most of its functionalities are completely uneeded here anyway.

----------

## Chapter I - Compiling Source Images

- **RAW image files**, these are in <u>Equirectangular</u> projection: https://drive.google.com/file/d/133dG-n9UmZmUyRYDtCbEJtnOauKpZrhN/view?usp=sharing

  - If you're going to use these, you'll need to project & then resize, crop & draw the coastlines yourself.

- **Template TGAs** for my Europe map extended to include India, <u>Lambert Conformal Conic</u> projection: https://drive.google.com/drive/folders/19pow0iFd67KSeqOGSMPr7yhBZ7d-oWEg?usp=sharing

  - These are all ready to use in game, and can save you a lot of time if you aren't looking to make a different-scaled map from what I've provided.

  - Specifically, map_climates & the coastlines are all completed and don't require you to draw stuff in by hand. The map_heights & map_ground_types are unaltered/blank.

    ![](https://i.imgur.com/o2KzPxq.png)

--------------

*(You can skip this and go straight to the G.Projector section if you use my provided PSD file instead. You'll still need to get your own historical source maps though.)*

### NASA Blue Marble Imagery (equirectangular projection)

- https://visibleearth.nasa.gov/collection/1484/blue-marble
- You'll want the grayscale Topography, and 2 Blue Marble images - one for summer & one for winter. You can find Blue Marble images for each month, you'll have to Search for 'Blue Marble [month]' because NASA's Blue Marble collection page doesn't actually display all of the Blue Marble...collection.
- Make sure to get the 21600x10800 sized ones.
- Alternate download: https://drive.google.com/drive/folders/1qQReoTs68DHA8sB7boDLFAvh9jDlWceb?usp=sharing

#### Alternate Heightmap Source

- https://tangrams.github.io/heightmapper
- This site uses the same base data as the NASA grayscale map, but allows you to zoom in much more.
- I'm pretty sure it's using a Mercator projection.
- The obvious issue with using this source for the heightmap instead, would be needing to adjust all your other sources by hand to line up with this one.

### Climate Map (equirectangular projection)

- https://en.wikipedia.org/wiki/K%C3%B6ppen_climate_classification
- Download the largest version of the climate map, 43200x21600.
- You'll be resizing this (nearest neighbor) to fit the NASA imagery, 21600x10800.

### Land Cover (equirectangular projection)

- https://neo.gsfc.nasa.gov/view.php?datasetId=MCD12C1_T1
- You can download a 3600x1800 land cover map here from NASA, you can use this to supplement the climate map when making map_climates & map_ground_types.
- For instance, you can see 'cultivated' areas on the land cover map that are located in 'desert' on the climate map (such as the Nile Delta). And likewise 'savannah' & 'shrubland' as well; you can mark these areas out as farmland in map_ground_types, or something like semiarid in map_climates.

### DEMIS Topographic Info (equirectangular projection)

- http://www2.demis.nl/worldmap/mapper.asp
- This one is tedious and time consuming to do, but once you have it it makes things much much simpler. Play around with the layer options and grab all the ones you want.
- I used this for river/lake info, you'll have to zoom in a bit until you get the level of detail you want for your map. Then open the image in a new tab and save as png (you'll need a save as png addon for your browser). 
- **Make sure to keep the same zoom level as you pan around to get images for the whole extent of your map!**
- Now you get the fun of stitching together all the images in pshop, then resize them to fit over your NASA imagery.

### Historical Maps

- Build up a folder for whatever good reference maps you can find. You'll be resizing/warp them to overlay on your map_regions to trace over or use as reference.
  - https://www.deviantart.com/cyowari has a good catalogue of maps
- Since your other source images are all equirectangular projections, I highly recommend you try and find as many maps that are the same projection to use as your sources here wherever possible. This way you can just overlay them on one of the 21600x10800 images, put them through G.Projector with your other images and them perfectly aligned for use on map_regions later. Is this time consuming to do one by one? Yes, but it'll let you draw more accurate borders and is less frustrating than the alternative.
  - Thomas Lessman has a large library of historical world maps in equirectangular projection. Keep in mind, many of the borders on the maps aren't exactly the most accurate, but it's a good start.
    - https://www.worldhistorymaps.info/ancient/


-------------

## Chapter II - Preparing the Source Images

### Rome Remastered, Changes To Map Size Limits

So since Feral didn't announce removing map size limits along with all the other limits that were lifted, most people have assumed that the limits remain the same. Well some ongoing testing shows otherwise. RR no longer limits the map size to 510 tiles on either axis, what the new limits are exactly, I don't think anyone knows definitively.

```
EdwinSmith_Feral — 06/14/2022
Not exactly, we fixed a number of memory issues that likely caused some of the OG map limitations as part of the RR work so a larger map might be possible but once you go over 510x510 you could start to hit issues as it wasn’t increased by design just due to unrelated items so it’s a side effect not a feature.
```

From what I understand @jorellaf has done some testing internally with the RIS team.

```
jorellaf — 06/14/2022
1020x350 worked. 1020x510 didnt
And 1030x350 didnt work
```

From my own testing, 720 x 440 seems to work without issue.

![](https://i.imgur.com/F7e8gjq.png)

----------

### Map Projections

#### Apps

- G.Projector - free, simple, decent results (works well for basically everything except Van der Grinten projection, more on that later)
  - https://www.giss.nasa.gov/tools/gprojector/
  - You'll also need to install some version of Java, you can find it on google if you don't have it.

- ArcMap - expensive, laggy, horrible UI, better & more customizable results

--------

Open G.Projector, choose one of the source image (one of the 21600x10800 ones) and make sure to select Equirectangular for input projection.

​	![alt text](https://i.imgur.com/u13Wvw7.png)

- Now you have to choose your projection. Whatever you choose, make sure you write down all the settings, since you'll be repeating this process for all of your source images!

- Make sure to turn graticules off.

- When you export, you'll want to save the image to max 20000, or some other large size, since you'll be using these for everything to come. Just be aware, if you're resizing to a size that is larger than the projected image G.Projector is giving you, the image is resized with Nearest Neighbor resampling.

- I think a lot of maps use Lambert Conformal Conic or Albers Equal Area Conic. I'd also recommend considering Van der Grinten II centered on the middle of your map. The only issue is exporting VdG projections with G.Projector creats a 2 pixel wide seam down the middle of the image, like so. You'll have to clean that up by hand if you want to use this projection. I'd assume ArcMap wouldn't have this issue, but haven't tried it.

  ![alt text](https://i.imgur.com/1mhGQOq.png)

  - Why Van der Grinten II? Personal preference, but you can refer to the wiki.
    - https://en.wikipedia.org/wiki/Van_der_Grinten_projection

- For my Europe map, I used the following projection

  ```
  Lambert Conformal Conic
  Center 31E, 38N
  Parallels = 10N & 10N
  Height = 55 degrees
  Save Size 11000 x 5500 px
  Import to pshop & rotate -6 degrees
  ```

- If you don't want to use a projection tool at all, you can just go into pshop and resize the 21600x10800 source images to 21600x13317. This gets you as close as you can get to a VdG projection without actually reprojecting it, as far as mid-latitudes are concerned. This method takes the least effort, but a projected map would look better in the end.

-----------

## Chapter III - Making the TGAs

This section explains the workflow I use. Keep in mind, this is for after you have your base map working in game. I recommend doing map heights & map ground types in chunks rather than trying to do the whole map in one go.

---------

### Make the Radar Maps

- The original Blue Marble imagery will be too dark to see details in game with faction colors overlaid on it. Recommended adjustment:

```
Color Balance			shadow		+50	+50	+50
  						midtones	+20	+20	+20
```


- *(The blue marble maps in my included PSD file have already been color balanced.)*

- radar_map1 & radar_map2 are not used by the game.
- feral_radar_map & feral_radar_map_winter are used instead, this is for the minimap. Dimensions are 4x map_regions.
- feral_map & feral_map_winter are used for the strategy overlay map. Dimensions are 16x map_regions.
- You can actually use different dimensions for all the radar maps, the game may have an upper limit, but not that I know of.

------

### Finalize the Coastline

- The easiest way is to use the climate map + blue marble imagery as reference and trace out your coastline. 
- Keep the sea as a separate overlay from your map heights, it makes things easier in the future.
- I also recommend keeping something like google maps open to reference areas of complex coastline.

---------

### Map Climates

- If you're following my mapping method, you should have the Koppen climate map as one of your source layers, make sure to resize it with nearest neighbor resampling to your TGA requirement. Now you can just select and paint over the climate zones one by one to fit Rome's climate colors to your liking and you're basically done. You'll probably want to come back to this after finishing map_ground_types and touch up some areas - namely mountains along where the snow boundaries are. You can see my examples.

#### Koppen Climates![](https://i.imgur.com/4pmxMYK.png)

#### Edited for map_climates.tga

- Typically you can keep the same divisions for temperate climates, but you'll want to place extra care and hand edit the areas that will be the boundaries between desert & other climates, since the Koppen desert climates represent much more varied environments than the in-game texture sets. You may want to represent some of the 'desert' areas with steppe or semi arid climate color.![](https://i.imgur.com/QON3mrH.png)

#### Set up a separate file for IWTE, we'll name it map_climates_for_mesh.tga

- If you're using the texture set I provided, you'll need to follow this convention.
- Notice how I don't have swam climate (yellow) anywhere on my climate map, that's because I've repurposed it to serve as a second sandy desert texture set. This helps areas like Arabia & the Sahara seem more varried and pleasing to the eye.
- Likewise, I've repurposed IWTE's 'default' climate folder as an arid steppe texture set which I use for a transitional area between green grass steppe & desert (basically used for Central Asia).
- This means, all the other climate folders have to have their full set of textures in them, so IWTE doesn't pull from the Default folder. Now, in your map_climates, you just use any non-RR climate color and IWTE will take that and apply Default textures to anything that's not a 'correct' climate color. So like, white.![](https://i.imgur.com/HHwK2Fk.png)

#### That's how I get results like this![](https://i.imgur.com/SXmD9q7.jpg)

-----

### Map Snow

- "My farmland is covered by snow when it shouldn't be / My farmland isn't covered by snow when it should be."

  - This is because Rome Remastered has a new TGA that's needed, map_snow.tga. I googled it, but couldn't find it mentioned anywhere in the TW Wiki, so here's my explanation. RR uses map_climates to determine snow for all the map textures *except cultivated farmland*. **map_snow controls snow on farmland!**

- It should be the same size as map_heights, but can be different dimensions - the game is just going to resize it to fit.

- It's fairly simple, you just want a grayscale image, black (0 0 0) means no snow, white (255 255 255) means snow. Presumably values in between would apply the snow texture w/ a transparancy value. I would just use the map_climates to make this.

- "But why does my map load even without map_snow?"

  - That's because the game is just reading the vanilla file in the base game install, and as I mentioned, resizing it to fit your map instead of crashing.

  ![alt text](https://i.imgur.com/whUWNS4.png)
  
  - I use the wand tool set to 5x5 avg with auto-alias ticked to select all the snowy climates from the climate map, then just paint bucket white over a black layer.

-----

### Draw in the Rivers

- Assuming you took the time to compile and stitch all the DEMIS imagery together, this is where that work pays off. Now you can basically just trace over all the rivers you want in one go. You'll have to keep in mind, portions of some rivers might be shown under the 'waterbodies' layer - such as the Nile. Usually this corresponds to sections that have been dammed and turned into reservoirs. 

- Don't need to bother adding in river crossings yet, that can come later.

- Rule of thumb, the river should extend 1 pixel past the coastline on map_features to avoid visible mesh clipping. After reviewing it in game, you can make further adjustment (shorter/longer) as needed. Again, *make sure you review and adjust after finishing the final map_heights!*

- The game has a limit of only being able to read 1 river_mesh file (if you have too many rivers, IWTE generates a 2nd river_mesh with the overflow). 

  ```
  river mesh contains positions = 65273  triangles = 55088
  ```
  
  - *IWTE limit for the river mesh is set at 65500 (against a max of 65535) positions **or** triangles.* 
  - *It may also be helpful to refer to the river_mesh.cas file size to judge how close to the limit you are, 2374 KB is about the limit.*
  
  ![alt text](https://i.imgur.com/zleNQPT.png)
  
  - The newer versions of IWTE have introduced changes for river mesh generation, allowing any river bits that are at the level of the Sea mesh to just use the water from the Sea mesh instead, thus reducing the amount of rivers rendered in the river_mesh.cas.
  
    - This feature can be further controlled in your task file by automatically applying additional height decrease along rivers.
  
      ```
      # river height parameter value is equivalent to applying a greyscale reduction. 
      # if you use extreme values you will get extreme results and I would advise amending your TGA heights.
      <river_drop_height>                     5.0
      ```
  
  -----
  
  ### River Loops
  
  IWTE supports rendering river loops, but you need to know how to set up the map_features for the loops to work.
  
  - Basically, you will have to add 1 white source pixel on the loop at a spot that is valid. A valid spot corresponds to dividing the loop in such a way that it functions as two separate rivers that just happen to touch at that source pixel. See example below for visual aid.
  
  - For each river loop section that IWTE detects, you should see ```typeidx retuned = 4   nameidx returned = 4```
  
  - If your map_features loop setup is invalid, IWTE will throw an error message after ```river chain count```
  
    ![](https://i.imgur.com/fTrDC1J.png)
  
    ![](https://i.imgur.com/Ky7mNxl.jpg)

---------

### Add the Cities

- This is where I use illustrator, I make an obscenely large (same size as your feral_map) overlay map with the DEMIS + blue marble images, then reference city locations in satellite view on google maps. It's fairly easy to pinpoint and mark all the cities this way. Now you have a nice looking outline that you can also resize down to place cities very accurately for map_regions.

- Alternately, if you have ArcMap or other GIS software, you can just make a dataset w/ the cities + lat/long (can usually be found on wiki).

- Obviously if you don't care that much about getting the city locations exact, then you can just skip this whole thing and eyeball it directly on map_regions.

- Note: sometimes you can place cities closer than you'd expect. This example works in game - even though the Taras region color is touching Brundisium diagonally. And, sometimes this type of thing causes the game to crash, it's just trial and error.

  ![alt text](https://i.imgur.com/kKp5pRy.png)
  
- Error - City is showing up in the bottom left corner of the campaign map instead of where it should be, no error message or log:

  - This is due to an 'invalid' location of the settlement pixel in map_regions.tga, similar to the issue discussed above. 

    ![alt text](https://i.imgur.com/nEmrcwl.png)

    In this case, moving the city 1 pixel to the right fixed the issue.


---------

### Draw the Region Borders

- This is where your historical reference maps come in, given the amount of effort that'll be going into making the map mesh look good, it doesn't make any sense to drop the ball here (as so many mods have imho). So put effort into drawing detailed borders instead of just having a bunch of boxy, straight lines.

  This:

  ![alt text](https://i.imgur.com/VgoPpHW.png)

  Not this:

  ![alt text](https://i.imgur.com/fnu3jUD.png)

  --------

  #### The Landmass Limit

  - The 'landmass' limit is still in the game; it's 22 landmasses. Where landmass = land that's fully separated by ocean & doesn't have regions that overlap onto other landmasses. Landmasses that are connected by land bridges count as just 1 landmass. And same goes for if you have say an island but put 1 pixel of it's region color anywhere on the mainland. *(That's the way you get around the landmass limit!)*

  - Basically, the easiest solution to add more island regions if you've hit the limit, is just add 1 pixel of the island region color in one of the far corners of your map (just cover it with impassable terrain).

  - If your map crashes on campaign start with no map.rwm generated and this error message, it's probably the Landmass Limit.
  
    ```
    n < N Failed
    checked array access out of range
    ```

--------

### Plan the Roads

- Make a new layer to overlay on map heights/ground types and mark out where your cities & roads need to be pixel for pixel. When we paint in the mountains for map heights, this will be serve as a stencil. We'll also resize the map features and keep an overlay of the rivers for this purpose.

  Like so: ![alt text](https://i.imgur.com/KIgdJGI.png)

- At this point, you can also resize the roads outline down, overlay it on the map_features, and see all the spots you need river crossings.

-------

### Map Heights

- Set up the image so 5 5 5 is the darkest RGB value - this is important for smoothing the coastlines later.

- Keep the original topo grayscale for reference, duplicate it and now we need to lower the brightness since we'll be painting our mountains over it rather than just fiddling with the raw image as the actual map_heights. This is the part I usually see neglected by people making maps with topo data. The reason we're going this route is we want something that actually *looks good in game*. It shouldn't come as a surprise, but generally not straying to far from the mountain shape/style of vanilla tends to give better results (and sure, it's personal preference to a degree).

```
Levels			channel: 		Gray
  				input levels:	0	2.5	255
  				output levels:	0	40
```

  This will give us something that we can paint over and only need to do minor touch ups to afterwards. You can experiment w/ brighter/darker values till you find something to your liking, as how much you need to adjust the image really comes down to the overall light/dark balance of the map area you're using.

  Original:

  ![alt text](https://i.imgur.com/d1aOtpR.png)

  Adjusted:

  ![alt text](https://i.imgur.com/vadLvM3.png)

- Brushes for mountains: It's very very simple

```	
Standard Brush		mode:		normal
  					opacity:	50%
  					flow:		50%
  					smoothing:	0%
  					size:		4px & 5px
```

  - For basically all of the mountains just use the 4 pixel brush. For large, high mountain lines, use the 5 pixel - I try to use it sparingly, only for the most prominent mountain lines that I want to pop and stand out on the campaign map.

- Keep in mind, this is all said with use of a pressure sensitive stylus in mind! It gives you extreme control on how thick/bright your lines are or aren't, which translates into size & height in game. Controlling the pressure you paint with gives you everything from small foothills to giant peaks in-game. Once you get the hang of it, it's completely straightforward

- Since different parts of our 'base map' will have different base height levels in terms of RGB, you need to take that into account when painting the mountains. With a 4 pixel brush, mostly keeping the peaks around 70~90 RGB higher than the base of the mountain gives good results for standard mountains. Make it too high and the slope of the mountains looks bad in game; too low, and trees being taller than the mountain doesn't look pleasing. And obviously you'll vary mountain height according to terrain.

- **Raising & lowering terrain**: You can use Dodge & Burn tools (exposure 50%, shadow/midtone/highlight depending what you want) to lighten & darken parts of the map while preserving grayscale. Don't use the Smudge tool - it wont preserve grayscale. This is handy if you finish a region and find that mountains for the whole thing are too low or too high. As you get more experienced, you should be needing this less and less.

- After you've drawn in the mountains, you'll also want to make sure to smooth out the valleys in between the mountains, you can use the same brush and just pick an RGB that's at the height you want the valleys to be at for any given area. This is important in order to keep terrain more flat in battle maps and also to keep cities from clipping through the mesh in an ugly way on the campaign map.

--------

### High altitude lakes with IWTE

- Once map heights is finalized, you can add 'high altitude' lakes in via IWTE. This way you can have inland lakes without having to lower the map_heights down to sea level. Add this line to your IWTE task file (you can name the lake TGA whatever you want):

```
<map_heights_lakes_tga>              "C:\Users\KirsiKura\AppData\Local\Feral Interactive\Total War ROME REMASTERED\Mods\Local Mods\East Asia Map\data\world\maps\base\map_lakes.tga" 
```

- The lake map needs to have a RGB 255 255 255 background, with lake pixels colored in w/ grayscale at the height level you want the water to be; so basically choose something 1~3 pixels lower than the edges of the lake.

- The lakes still need to be defined as sea in map_heights, map_ground_types, map_regions like normal sea areas.

- Be aware, IWTE makes these lakes by adding water on the river_mesh, so it shares the limit w/ your map_features rivers.

Like so:

![alt text](https://i.imgur.com/3DT9XiE.png)

![alt text](https://i.imgur.com/OqInOTd.png)

---------

### Sculpting Coastlines with IWTE

If you modded original Rome, you might remember that you could smooth out coastlines to get rid of jaggedness and clipping by using darker sea colors (RGB 0 0 X) diagonally touching coastline pixels in map_heights. IWTE rendering works basically the same. 

- You'll usually get better results if your coastal tiles are RGB 2 2 2 or 3 3 3 instead of 1 1 1 on low elevation areas. But it mostly seems like trial and error pixel by pixel between that and the sea color until you get a result that looks good in game.

#### This is what doing it by hand looks like

![alt text](https://i.imgur.com/4jp1M4C.png)

![alt text](https://i.imgur.com/DBDLZOi.jpg)

___________

### AUTOMATIC   COASTLINE   SMOOTHING!

- I highly, highly recommend you follow G|I|Sandy's guide and set up a copy of the map heights layer accordingly.

- Explanation - https://www.twcenter.net/forums/showthread.php?669184
  - Alternate link to the .psd with the layer style - https://drive.google.com/file/d/16ghLv2kl6NtBGRLOtOY_hDhwY9i6whiD/view?usp=sharing
- Keep in mind, you'll need to rasterize the layer after applying the layer style to it, since we'll be editing & touching up a bunch of parts of it - and that's why it's important you kept a copy of the original!
  - First, the layer style results in a 2 pixel 'bleed' all along the edges of the map (not just the coast pixels) that darkens the RGB values, we'll need to isolate all those pixels and delete/replace them w/ the original map_heights.
  - Similarly, if you're using the map_lakes.tga feature of IWTE to have high altitude lakes, you'll want to clear those areas up & keep your original map_heights pixels.
- After doing that, the last time consuming part is open it up in game, look it over and start touching up sea pixels by hand.
  - Basically, anything that is 1 pixel of sea w/ land on both sides will need to be 'widened' since this technique will generate it @ 0 0 255. Use a color like 0 0 253, or 0 0 252 or 0 0 251. And usually something like 0 0 246ish for diagonally touching pixels if you want.
  - Then just go over and touch up any remaining jaggedness.

#### Results

![alt text](https://i.imgur.com/QM1rgrM.jpg)

-------

### Map Ground Types

It's pretty straight forward, my process goes like this:

1) Draw in mountain
   - For high mountain, you can just eyeball it in, or you can use the selection tool and go by height so you just fill in the highest peaks, you can just do whatever, it's pretty forgiving since IWTE tends to make it look good either way.
2) Add dense forest where you want it - the Blue Marble satellite imagery helps a lot here; obviously you'll have to make allowances/guesses for what ancient forest cover would have been though.
3) Add hills & light forest. Generally, just add hills around your mountains, or if you're adding a bunch of hill that isn't adjacent any mountain, don't make it a big solid patch, make it more of a splattered pattern, as I've done for the Thad desert. And as you can see, I have almost all mountain pixels surrounded by at least 1 pixel of hill or forest, I just think it tends to look better in game this way.
4) Add coast & swamp to your liking
5) Add farmland to your liking
6) Everything else is wilderness
7) For sea, again, you can use the Blue Marble image since it has bathymetry shading. Just play around w/ the selection tool till you get divisions you like for shallow/deep/ocean, smooth the selections to your liking and your basically done. You'll probably want to do some hand editing too to smooth down sharp corners. I'd also recommend at least making sure you have a 3~5 pixel band of shallow sea along all your continental coastlines. This is all done to get a good looking result in IWTE.
8) You can use small lines/blobs of shallow sea surrounded by deep sea / ocean to display bathymetric features on the campaign map.

![alt text](https://i.imgur.com/CJX1AR0.png)

----

### Generating Heightmap Bins

- My descr_map_tiles for reference: https://drive.google.com/file/d/1KVG18iWITCcPvhN5TikD-V-Dlw6bkPXc/view?usp=sharing

- Make sure your mod is set up in
  ```
  ...\Feral Interactive\Total War ROME REMASTERED\Mods\Local Mods\
  ```

- The simplest way to generate updated bins is to just find/replace all for ```_lod0.bin``` portion of the bin file names in descr_map_files. Just change it so the bin name is different from default and load up the map, RR will generate new bins when it can't find your file names. Afterwards, just undo the change so you have the correct bin names.
  - *IMPORTANT: After hearing feedback, it seems certain filename changes wont work for getting RR to generate new heightmaps. I've always renamed the bins to* ```_lodk.bin``` *and never had any issue, whereas ahowl tried* ```_lod00.bin```*, which didn't work.*
  
- Keep in mind, RR wont generate new bins if your map is installed directly into the steam install, you need to have it in your local mods folder.

- Also, the bins will only generate for you if you have no other mods enabled besides the one you're working on! Otherwise, the game generates a temporary set of bins that lasts until you exit out of the game and doesn't get saved anywhere.

--------

## Chapter III - More IWTE Stuff

- Setting up the task files: I'm not going to go in depth for this step, there's info on the wiki. In total, you should have 5 task files.
  - Summer mesh rendering
  - Winter mesh rendering
  - Convert normals
  - Summer albedo
  - Winter albedo
- Here's my own task files for reference: https://drive.google.com/file/d/1h4wUAuDiI4mAtA55DSdUOnqKeeTJfXK7/view?usp=sharing
  - They have some important setting changes that'll save you time if you were just going off of the IWTE provided sample task.
  - They're numbered 1-5, run them in that order.
  - You only need to run the winter ones if you want to see the winter mesh.

----

#### Settings That I Changed

```
<map_pieces_longest_dimension>        22
```

- Default was 13, this controls how many square sections the map mesh is generated in, 22 is the max number for the longest axis. The default 13 was for the vanilla Rome sized map. Since you presumably want a large map size, make sure to set this to 22.
  

```
<mesh_detail_level>                high
```

- Default was medium, setting it to high helps with shadows on mountain peaks, and some other stuff? I'll let Wilddog explain:

  > Basically there is a parameter in the task process which can have different settings and the mesh density ie number of triangles/vertex that will be created are amended. Its set relatively low as people were causing too many crashes by copying parameters set for a small map whilst trying to create maximum size maps. 
  
  

```
<map_heights_lakes_tga>              "C:\Users\KirsiKura\AppData\Local\Feral Interactive\Total War ROME REMASTERED\Mods\Local Mods\East Asia Map\data\world\maps\base\map_lakes.tga" 
```

- You need to add that line w/ your file path in order for IWTE to render highland lakes.
  

```
<mtn_ht_factor>                  0.8
<mtnhigh_ht>                     75.0 
<ridge_ht_factor>                1.0 
```

- The above lines are for overall mountain shape & defining what height IWTE switches between mountains_low & mtnhigh textures. I use these settings for my Europe map, but keep the default ones for the Asia map.

```
<beach_factor>                    0.90 
```

- The newest version of IWTE include an additional coastline texture overlay to give an appearance closer to the vanilla map. I changed the beach factor to 0.9 to make the color more prominent.

```
Sea textures
<default_ocean>     "X:\Rome Remastered Modding\Tools\ITWE\IWTE_v22_02_B\MapMesh\base-textures\default_climate\sea_shallow.tga"
<default_sea_deep>     "X:\Rome Remastered Modding\Tools\ITWE\IWTE_v22_02_B\MapMesh\base-textures\default_climate\sea_shallow.tga"
<default_sea_shallow>     "X:\Rome Remastered Modding\Tools\ITWE\IWTE_v22_02_B\MapMesh\base-textures\default_climate\sea_shallow.tga"
```

- The sample task file lists sea texture as 'sea.tga', if you're using the newer (version 2) IWTE textures from the wiki, there's multiple sea textures provided. Just use sea_shallow.tga for all 3. Trying to use all 3 of the textures provided for shallow/deep/ocean respectively results in bad texture transition between sea types, like this:	

  ![alt text](https://i.imgur.com/A4OAGMP.jpg)
  

```
Sea settings
<sea_drop_list>     7 5 4	# sea drop for seas shallow, deep, ocean (value  of 5 is similar to TGA pixel difference of 5 in heights_tga)
<drop_loop_factor>     320		# used to calculate itterations in sea drop. Higher value makes sea deeper.
```

- Instead, you'll add these lines and let IWTE take care of the transitions: ![alt text](https://i.imgur.com/6wyGw1K.jpg)

______

### Making New Map Textures for IWTE

It's very tricky to get the look of a map texture just right so it fits smoothly and blends in with the other map textures in-game, generally it takes multiple iterations going through slight variations of color & light/dark balance. This is my basic workflow.

1) **Look for suitable textures on google, or pan around on google earth to find something usable. I'll be using this for sandy desert hills.**![](https://i.imgur.com/WQb45qb.jpg)
2) **Use https://www.imgonline.com.ua/eng/make-seamless-texture.php to convert it to seamless.**![](https://i.imgur.com/WZej1Bv.png)
3) **Determine what existing texture(s) you want it to match/blend with, here I want it to match with my sandy desert waste & rocky desert hills.**![](https://i.imgur.com/56SI8Gn.png)
4) **In Photoshop, use Image Adjustments > Match Color to edit the new texture to fit with the one you want.**![](https://i.imgur.com/iny8sle.png)
5) **Touch up the result however you want, here I added a sharpness filter to give an added impression of ridgelines.**

------

## Best Practices

- Never try adding new regions at the same time you're making major changes to map heights/ground types & re-rendering the mesh. This is a recipe for disaster as it's easy to make errors adding regions, and now it'll be harder to track down why your map is crashing.
- Every time you solve a crash, make sure to document the error you were getting in the message_log - especially for the nonsensical error messages, which is most of them for mapping.
- Keep multiple back ups of all your files - I have mine on 2 local drives + google drive.
- Always keep a quick back up of the specific map TGAs that are currently working when you're making changes to them.

-------

## Message_Log Error Documentation

This is just a list of random error messages I've encountered while modding:



```Landmass Limit
n < N Failed
checked array access out of range
```

- Landmass Limit, explained in earlier section



```
Generating default settlement in region  (189)
```

- Crash caused by placeholder region #189 being too large (we're talking couple hundred pixels) & having too many 1 pixel islands, solved by splitting it into 2 placeholder regions.



```
edge_count <= 3 Failed
edge_count <= 3 Failed
WORLD_MAP river crossroads are forbidden (too many nasty permutations)
```

- Crash caused by bad map_features. Accidentally had 4 pixels of river in a square.



```
verts
verts_used < MAX_REGION_BORDER_VERTICES Failed
too many verts!!!
```

- Crashed after loading bar filled when launching campaign. Map.rwm generated
- map_regions had a region with 'too many vertices', redrawing the border a bit fixed it, still not able to pin down what it was.



```
script error "trying to place [settlement] in this region (region name), but it already has a settlement [settlement]"
script error "trying to place [settlement] in this region (region name), but it already has a settlement [settlement]"
```

- Problem probably caused by 'something' happening that makes the mentioned region 'too big', solved by reducing the region size. Though, this region worked fine as one of the 10 base regions when map was empty.



```
generating trade routes
```

- Crash on start new campaign, after "generating trade routes", no map.rwm, no pop up error log. This is crashing right before "Generating regions" should occur.
- Problem with map_features, 4x4 pixel bit of river (blue), same problem as the previous 4x4 pixel error, but resulted in a different message - in this case, no message.



```
"unable to get name for region '' from stringtable"
```

- descr_regions cannot have blank lines at the start of the file before region name



```
Crash on scrolling over on campaign map
```

- Faction name for culture in descr_region is not listed in descr_strat under playable or non playable, resulting in no factions of that culture present.



```
Generating default settlement in region  (189)
Generating default settlement in region  (189)
type < MAX_FACTIONS Failed
you are trying to retrieve an invalid faction
index < m_num_records Failed
DATABASE_TABLE error found : index out of range.
```

- Caused by a city with duplicate region color in descr_regions & missing the actual region color for that city.



```
BATTLE_ALLIANCE_STATS::clear() setting battle result to none
```

- Kick back to menu when trying to load campaign, happen after editing coordinates in descr_strat, no useful error message.
- Caused by faction's character being assigned to a settlement that is not listed in descr_strat as belonging to that faction. Sometimes doing so causes no error, sometimes this happens.



```
attaching region
attaching region Bactria(1) to faction(slave), giving them 486 triumph points
Created a port attached to settlement 'Patala', faction 'slave'
Generating default settlement in region  (10)
type < MAX_FACTIONS Failed
you are trying to retrieve an invalid faction
type < MAX_FACTIONS Failed
you are trying to retrieve an invalid faction
```

- Crash on start campaign, does generate map.rwm
- Caused by repeat region color in descr_regions. The region after the one listed last in the log is *supposed to be* the one where the 1st instance of the duplicate color in descr_regions, but it can also just be listing a completely unrelated region!



```
Error loading region: Region label 'Luoyang_R' not found
```

- Changed internal region name, all appropriate files updated. Problem persisted until deleting map.rwm, even though that shouldn't be required.



```
Generic Error:
SettlementBuildingExists needs a settlement. ([text])
```

- Persisted until deleting map.rwm



```
Script Error in Q:\Feral\Users\Default\AppData\Local\Mods\Local Mods\Local Mod/data/world/maps/campaign/imperial_campaign/descr_strat.txt, at line 13314, column 83. duplicated character name in this faction
```

- Duplicate 'named character' name in Slave faction. 'General' cannot share a name with 'Named_Character'.



```
descr_strat.txt, at line 6104, column 12. could not create settlement at script line 6104.
```

- Settlement defined in descr_regions / descr_strat, but region is not drawn on map_regions.tga



```
descr_strat.txt, at line 1424, column 5. Settlement specifies port, but this region is not allowed a port - can be ignored,but port building will not be created for settlement!
```

- Region is coastal, with port pixel at valid location on map_regions.tga, so it's unclear what the issue is.
- Caused by map_heights.tga pixel being RGB 0 0 0



```
descr_strat.txt, at line 2377, column 55. you have chosen an invalid tile(219, 204) for Alexios (parthia)
```

- (219, 204) is a valid tile in map_regions.tga
- Caused by map_heights.tga pixel being RGB 0 0 0



```
descr_strat.txt, at line 13063, column 12. You are trying to place Pskov in this region(WILDERNESS_R), but it already has a settlement(Pskov)
```

- Region color is present in map_regions, but missing black pixel for the city (Pskov)



```
descr_strat.txt, at line 4232, column 12. could not create settlement at script line 4232.
```

- descr_strat, descr_regions, region_and_settlement_names, and map_regions.tga are all correct
- Map loads if descr_strat entry is removed, but results in the problem city becoming the city/region of another region.
- Unable to fix, problem region/settlement name was Zaranj_R / Zaranj, only way to work around was using a different internal name for region + settlement and just setting display name for Zaranj.



```
Error loading region: Region label 'testR' not found
```

- Attempting to change internal region name with game open @ main menu.



```
unexpected section after region Antiochia
```

- Happens when trying to add fort/watchtower in descr_strat
- Caused by not using the correct internal region name.



```
Instant CTD after campaign load
```

- Caused by doing an incomplete job of changing settlement internal name, changed descr_regions, names_lookup, win_conditions. The game loads, but crashes when a script referencing the old name activates.



```
CTD when pre-battle screen is supposed to show up when player attempts to attack [faction_name]
```

- Caused by error in expanded_bi
- {EMT_YOUR_FORCES_ATTACK_ARMY_*[FACTION_NAME]*} , faction name did not match internal faction name.



```
CTD after clicking campaign load, no message, error log shows region name list cuts off early. No map.rwm
```

- The next region entry in order in descr_regions has an error: duplicated other region name instead of typing the correct one.



```
descr_strat.txt, at line 15844, column 1. You have chosen an invalid tile(488, 355) for the settlement of Toqsoba Camp
```

- Caused by settlement has no entry in descr_strat, but trying to place a non slave faction character inside settlement.



```
descr_strat.txt, at line 7480, column 12. could not create settlement at script line 7480.
```

- Region name listed in descr_strat does not exist.



```
Failed to create staging buffer result was 0x80070057 (E_INVALIDARG), bufferDesc: {0, 3, 0, 65536, 0, 0}
```

- Crash on campaign load when trying to change strat map model for village
- Checked cas file, all textures referenced are present in textures folder
- All other city levels can be replaced fine, but the villages crash no matter what, so removed



```
we have either got a region too big or we have 2 similar coloured regions. Max Width(100), Max Height(100)
couldn't find rebel type() in rebel database
couldn't find rebel type() in rebel database
```

- Crash on campaign start before transition to loading screen, no map.rwm generated
- Caused by bad map_regions.tga, the message log is unrelated, it's just getting cut off when it gets to the problem 'region' and crashes.
- Need to go back to previous working version of map_regions & start making incremental changes to see what was causing the crash.
- Caused by stray brush stroke on the map_regions layer, identify it by comparing working tga w/ bugged on https://www.diffchecker.com/image-diff/
- Can also be caused by bad map_ground_types, in this instance, forgot to toggle black layer, so map heights was showing on ground types TGA.
- Duplicate region entry in descr_strat + incorrect palace for town level + region color on map_regions & defined in descr_regions, but without a city pixel + trying to place a settlement in faction when there is a slave army still in settlement in descr_strat.
- Having a region drawn into map_regions, but forgot settlement entry in descr_regions



```
loading world map file 'Q:\Feral\Users\Default\AppData\Local\Mods\Local Mods\RTRPE/data/world/maps/base/map.rwm'...
finished
```

- Game freezes after clicking start campaign, map.rwm does generate, never progresses to load screen, does not actually CTD.
- Game does not progress beyond parsing the region list & generating map.rwm
- Next step should be loading map_features, then resources.
- Problem caused by porting OG Rome descr_strat without redoing the resource section to include # for each resource.



```
Couldn't find required geometry 'pole' in the campaign map standard model.
```

- CTD with geometry pole as last entry
- Next line should be about character portrait generation
- Caused by problem involving merchants



```
Q:/Feral/Users/Default/AppData/Local/Mods/Local Mods/Kirsi Map Submod/data/world/maps/campaign/kirsi_map_1072_test/feral_map.tga		WARNING: STANDARD_TEXTUREs do not support mip-mapping
Q:/Feral/Users/Default/AppData/Local/Mods/Local Mods/Kirsi Map Submod/data/world/maps/campaign/kirsi_map_1072_test/feral_map_winter.tga		WARNING: STANDARD_TEXTUREs do not support mip-mapping
Failed to initialise the campaign radar texture.
```

- CTD on campaign load
- Not sure what the problem was.



```
AERIAL_MAP_TILE_MANAGER could not find overlay base model river_straight1b
```

- CTD on campaign load
- Caused by trying to use river_a.cas provided by IWTE on Imperator Map
- This is due to not having the descr_arial_map_tiles.txt provided by IWTE, need to copy that intp \data as well.



```
*** Event handler open complete, available texture mem is 4138729472. ***
```

- Random CTD when campaign loading should transition to the campaign map.
- Relaunching game a second time worked, w/o problem.
- Probably something relating to user CPU/GPU memory allocation @ time of launch.



```
Traceback (most recent call last):
  File "IWTE_v22_07_C.py", line 55303, in run
  File "IWTE_v22_07_C.py", line 16019, in execute_create_piece_tga_textures
  File "WDstratmapping.py", line 9083, in create_piece_tga_textures
  File "WDstratmapping.py", line 6513, in create_tga_textures
  File "WDstratmapping.py", line 13503, in create_heightmaps
  File "scipy\interpolate\ndgriddata.py", line 264, in griddata
  File "interpnd.pyx", line 908, in scipy.interpolate.interpnd.CloughTocher2DInterpolator.__init__
  File "qhull.pyx", line 1841, in scipy.spatial.qhull.Delaunay.__init__
  File "qhull.pyx", line 280, in scipy.spatial.qhull._Qhull.__init__
ValueError: No points given
```

- IWTE error, caused by <map_pieces_longest_dimension> value being set too high. Lower the value and test again.



```
You have chosen an invalid tile(0, 0) for the settlement of Alexandria.
It will mean not being able to reach this settlement and is a bug.
For now we'll ignore it.
```

- Kick back to menu on campaign start
- The tile on map_regions somehow became 'invalid', even though it worked in that exact position before, and nothing changed, editing coast line elsewhere in the nile delta. This is confirmed by testing just moving Alexandria, has nothing to do w/ port placement.
- Problem has nothing to do w/ map heights, it is 100% caused by map_regions.tga
- Solution, an offshore 2 pixel island needed to have 1 pixel colored for Alexandria, makes no sense



```
The card cycle button has been set to cycle through an unknown tab type
```

- CTD on campaign map when screen shows city of a specific faction or click on city.
  - Only happening when attempting to implement ```latin``` faction for Chivalry by swapping parthia to latin in desc_strat.
- Ruled out invalid character names in descr_strat, ruled out missing faction entry in descr_sm_factions, ruled out missing faction creator not listed under factions in descr_strat

```
invalid tile for Argos, means can't reach settlment, for now we will ignore it
```

- Kick back to menu on campaign faction select, error message pops up in log when there is another issue in descr_strat, completely unrelated.
- Argos pops up due to pixel diagonally touching city pixel in map regions, removing the other region diagonal color gets the map to load, and after that, we see descr_strat has some invalid character coordinates that overlap with other armies.
- Fixing the character coordinates allows us to revert Argos map regions to prior configuration w/ no problem.



```
You have chosen an invalid tile(30, 171) for the settlement of Lixus
```

- Kick back to menu on faction select.
- Caused by other region color touching city pixel on diagonal.



```
"Unable to get region name for Saldae from string table" - in dialogue box
"we have either got a region too big or we have 2 similar coloured regions. Max Width(100), Max Height(100)" - in message log
```

- CTD, no map.rwm generated, happened when trying to add region, all region name entries exist and are correct/unique

- Caused by format error in region_and_settlement_names.txt

  ```
  {Hippo)			Hippo
  ```

  Used a parenthesis instead of } to close the entry on the line above Saldae



```
map.rwm generates but kick back to menu on faction select
```

- having region entry in descr_strat for region that doesn't exist

