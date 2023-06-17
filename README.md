# Hide DLC Blocks

This file will generate a local `SpaceEngineers` mod and hide all the dlc items.

I made this script after comming back to `SpaceEngineers` and having problems navigating the Creative menu with so much clutter in it.


## Download from Steam Workshop
This mod has been uploaded to Steam Workshop and can be downloaded here

https://steamcommunity.com/sharedfiles/filedetails/?id=2990811919

## Usage

If you are getting errors that `lxml` is not found run the following command
```
python -m pip install lxml
```

Usage
1. Open up `cmd.exe` and run `python generate_mod.py`
2. You will be prompted to write the `SpaceEngineers` path on your computer
3. If a mod with this name already exists it will ask you if you want to overwrite it (Y)es or (N)o
4. The local mod should have been successfully generated and can be accessed in your `Mods` tab


## Info
```
This file was created to fix the overly cluttered GUI in SpaceEngineers
You will be promped for where on your computer SpaceEngineers is located

It will usually be found in '<Drive>/Steam/steamapps/common/SpaceEngineers'

After that this script will automatically generate a mod in your local mods folder.

If there is a mod already named this you will be prompted if you want to
replace it.
```
