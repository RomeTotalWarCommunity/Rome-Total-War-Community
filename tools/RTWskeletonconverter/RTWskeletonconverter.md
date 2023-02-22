![Workshop_header_template](/Workshop_header_template.png)
# RTWskeletonconverter.py - Convert skeleton files from binary to text and back

## Table Of Contents

* [WARNING](#warning)
* [About the tool](#about-the-tool)
* [How it works](#how-it-works)
* [How to use](#how-to-use)
* [Additional info](#additional-info)

## WARNING

You need to unpack the skeletons first using Vercingetorix's XIDX. Skeleton files of Rome - Total War are two files: **skeletons.idx** (index file) and **skeletons.dat** (actual skeletons), located in the data/animations folder of the game.

Rome Remastered skeletons CAN NOT be unpacked with XIDX because of the format differences. See details in the article for Feral's [Skeletonconverter](https://github.com/FeralInteractive/romeremastered/blob/main/tools/SkeletonConverter/SkeletonConverter.md). You can only unpack and repack skeleton files of original RTW and mods.

**Windows users:** in order to run this python script, you need to have python installed globally. You can download python here: https://www.python.org/downloads/

## About the tool

This is RTW Skeleton converter script created originally by **KnightErrant** and updated by **Suppanut**. It requires Python 3+ to work.
The script allows you to convert unpacked skeletons from binary to editable form (text file) and convert back from text file to binary which game could use.

## How to use

To use, first you need to unpack **skeleton.idx** and **.dat** files using the tool ([Vercingetorix's xidx packer](https://github.com/AKAfreaky/XIDX)). 

The best strategy would be to do it in a separate folder because the tool outputs all the skeletons as loose files in the same directory as **skeletons.idx** and **skeletons.dat**. After using the tool, skeletons will appear as a bunch of binary files like *fs_dagger*, *fs_horse* et cetera.

You can now simply run the [RTWskeletonconverter.py](/tools/RTWskeletonconverter/RTWskeletonconverter.py). There will be two options available: **Skeleton to Text Converter** and **Text to Skeleton Converter**. First one will create a .txt version of the selected skeleton, and the other option will convert it back to binary, adding "_modified" at the end of new file name just in case to not overwrite the original skeleton. You can now repack the skeletons back using XIDX and use them in game.

Skeleton files contain links to the **.CAS** animations used, keyframe numbers, and other information. More information see in [TWC thread](https://www.twcenter.net/forums/showthread.php?318920-RTW-skeletons-CRACKED) and in **Lom1138**'s definitive guide to skeleton editing.

## Additional info

To use the modded skeletons for Rome Remastered, you need to run Feral's [Skeletonconverter](https://github.com/FeralInteractive/romeremastered/blob/main/tools/SkeletonConverter/SkeletonConverter.md) tool to convert old **skeletons.idx** and **skeletons.dat** to new RR compatible format.