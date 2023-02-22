![Workshop_header_template](/Workshop_header_template.png)

![Dagovax](/images/contributors/dagovax.png)
## Creator: **Dagovax**
---

# Adding a completely new faction to Rome: Total War REMASTERED

#### Summary: In this guide, I will explain the neccesary steps in adding a completely new faction into your Rome: Total War REMATERED mod.

## Table Of Contents
* [Preperation](#preperation)
* [Adding the initial faction](#ADDING-THE-INITIAL-FACTION)
* [Changing characters and banners](#CHANGING-CHARACTERS-AND-BANNERS)
* [Adding the faction descriptions](#ADDING-THE-FACTION-DESCRIPTIONS)
* [Adding the menu icons](#ADDING-THE-MENU-ICONS)
* [Adding the new faction to your campaign](#ADDING-THE-NEW-FACTION-TO-YOUR-CAMPAIGN)
* [(Optional) Adding the captain banners](#OPTIONAL-ADDING-THE-CAPTAIN-BANNERS)

## Preperation

We need to edit the following files, so copy them from the base game into your mod folder:

* descr_banners.txt
* descr_character.txt
* descr_standards.txt
* descr_sm_faction_logos.txt
* descr_sm_factions.txt
* descr_sm_factions_difficulty.json
* text/expanded_bi.txt
* export_descr_unit.txt

I will divide this guide into seperate chapters.

## 1. ADDING THE INITIAL FACTION

*Files involved:*
* descr_sm_factions.txt
* descr_sm_factions_difficulty.json
* descr_sm_faction_logos.txt
* descr_standards.txt
* export_descr_unit.txt

### descr_sm_factions.txt

The first thing we need to do, is adding your new faction to the game. To do this, we need to add it to **descr_sm_factions.txt**. Open the file in your text editor and scroll all the way to the bottom.
This file format looks a lot like json, and the comma's are very sensitive!
So copy a whole block (like the one below), and paste it before last line, which is the **]**, tag.
>```
>"newfaction":
>     {
>        ;;name and description
>        "string":      "NEWFACTION",
>        "description": "NEWFACTION_DESCR",
>
>
>        ;;culture and (default?) character ethnicity
>        "culture":   "barbarian",
>        "ethnicity": "mediterranean",
>
>
>        ;;tags for faction groups
>        "tags": [ ],
>
>
>        ;;namelists
>        "namelists":
>        {
>            "men":      "pontus_men",
>            "women":    "pontus_women",
>            "surnames": "pontus_surnames",
>        },
>
>
>        "logos":
>        {
>            ;;logo to use in the loading screens (seperate as sprite sheets aren't loaded at that point)
>            "loading screen icon": "data/ui/faction_icons/new_faction.tga",
>
>
>            ;;standard index as declared in descr_standards (4 per page)
>            "standard index":       9,
>            "rebel standard index": 25,
>
>
>            ;;logo index as declared in descr_sm_faction_logos (1 per page)
>            "logo index":       25,
>            "rebel logo index": 25,
>
>
>            ;;flag models to be used on the strat map when a settlement is unoccupied
>            "strat symbol model":       "data/models_strat/symbol_pontus.CAS",
>            "strat rebel symbol model": "data/models_strat/symbol_eastern_rebel.CAS",
>        },
>
>
>        ;;faction colours (some base game factions may have hardcoded overrides)
>        "colours":
>        {
>            "primary":   [  255,  0, 255, ],
>            "secondary": [ 0, 255,  255,  ],
>
>
>            "family tree":
>            {
>                "background":      [  255,  0,  255, ],
>                "font":            [  0, 0, 0, ],
>
>
>                "selected line":   [  255, 255, 255, ],
>                "unselected line": [  200, 187, 187, ],
>            },
>        },
>
>
>        "movies":
>        {
>            ;;movie to play when starting a campaign
>            "intro": "data/fmv/intros/eastern_intro_1080p.wmv",
>
>
>            ;;movie to play when this faction wins or is defeated, respectively
>            "victory": "data/fmv/victory/eastern_outro.wmv",
>            "defeat": "data/fmv/lose/pontus_eliminated.wmv",
>        },
>
>
>        "available in custom battles": true,
>        "prefer naval invasions": false,
>        "default battle ai personality": "default_personality",
>    
>        ;;allow this faction to have a functioning family tree
>        "allow reproduction": true,
>    },
>```

As you can see, Feral already added information so you know what each line means.<br/>
I will get back to this file when we need to change some lines, but you need to change the <span style="color:red">**newfaction**</span> to the name of your wanted faction. This will be the internal name that your faction will use for i.e. EDU, EDB and DMB entries.<br/>
As for <span style="color:green">**namelists**</span>, you can add new sections in ***descr_namelists.txt*** and add them to this file. Your faction will then use your new names. In this example, we will just keep the pontus ones.

You can change the culture (**descr_cultures.txt**) and default *ethnicity* (**descr_unit_variation.txt**). The default ethnicity is used for units and generals/officers for your faction when no variation is set in their EDU entries.

## 2. CHANGING CHARACTERS AND BANNERS

## 3. ADDING THE FACTION DESCRIPTIONS

## 4. ADDING THE MENU ICONS

## 5. ADDING THE NEW FACTION TO YOUR CAMPAIGN

## 6. (OPTIONAL) ADDING THE CAPTAIN BANNERS



