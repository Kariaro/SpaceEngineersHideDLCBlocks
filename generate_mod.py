import os
from lxml import etree

# Author : HardCoded
# GitHub : https://github.com/Kariaro
# Created: 2023-06-17
#
# Description:
description="""
--- INFO ---

  This file was created to fix the overly cluttered GUI in SpaceEngineers
  You will be promped for where on your computer SpaceEngineers is located

  It will usually be found in '<Drive>/Steam/steamapps/common/SpaceEngineers'

  After that this script will automatically generate a mod in
  '%s'
  
  If there is a mod already named this you will be prompted if you want to
  replace it.
  
--- INFO ---
"""

def get_files_from_path(path, extension = ''):
    result = []
    for file in os.listdir(path):
        if not file.endswith(extension):
            continue
        result.append(os.path.join(path, file))
    return result


def normalze_xml(xml):
    text = etree.tostring(xml).decode('utf-8')
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.fromstring(text, parser=parser)


def generate_dlc_hiding(se_path, filter):
    se_path = os.path.join(se_path, 'Content', 'Data', 'CubeBlocks')
    files = get_files_from_path(se_path, '.sbc')

    hidden_items = []
    
    print('\nProcessing CubeBlocks')
    print('  - Path \'%s\'' % se_path)
    
    # Make printing a bit prettier
    name_length = 1
    for file in files:
        name_length = max(name_length, len(os.path.basename(file)))
    
    for file in files:
        dlc_items = []
        for item in etree.parse(os.path.join(se_path, file)).xpath('//Definition'): 
            # Get DLC tag
            dlc_tag = item.find('DLC')
            
            # Check if the item is from a DLC
            if dlc_tag is not None:
                # If the DLC is inside the filter we keep it
                if dlc_tag.text in filter:
                    continue
                
                # Update the public tag to 'False'. (Effectively hiding it from the GUI)
                public_tag = item.find('Public')
                if public_tag is None:
                    public_tag = etree.SubElement(item, 'Public')
                public_tag.text = 'false'
                
                # Add item to DLC hide list
                dlc_items.append(item)
        
        # Print how many items were hidden
        print(('  - %-' + str(name_length) + 's - %3d hidden') % (os.path.basename(file), len(dlc_items)))
        hidden_items += dlc_items
    print('\nTotal: %d hidden item(s)\n' % len(hidden_items))
    
    # Create new sbc file with hidden definitions
    dlc_hide_xml = etree.Element('Definitions', nsmap={
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsd': 'http://www.w3.org/2001/XMLSchema'
    })
    dlc_hide_items = etree.SubElement(dlc_hide_xml, 'CubeBlocks')
    for item in hidden_items:
        dlc_hide_items.append(item)
    
    # Fix tab issues and return the element tree
    return etree.ElementTree(normalze_xml(dlc_hide_xml))


def generate_local_mod(mod_path, mod_name, xml):
    # Print the mod location
    print('Local mod will be generated here')
    print('  - Path \'%s\'' % mod_path)
    
    # Check if mod already exists
    if os.path.exists(mod_path):
        result = input('\nA mod named \'%s\' already exsists do you wish to replace it (y/n)' % mod_name)
        if result.lower() != 'y':
            print('Will not overwrite file. Stopping')
            return
    
    # Generate folders
    os.makedirs(os.path.join(mod_path, 'Data'), exist_ok=True)
    
    # Write data
    data_path = os.path.join(mod_path, 'Data', 'CubeBlocks_Hidden.sbc')
    with open(data_path, 'wb') as f:
        f.write(etree.tostring(xml, pretty_print=True, xml_declaration=True))
    
    # Print success
    print('\nDone! Mod has been successfully generated')


if __name__ == '__main__':
    mod_name = 'HideAllDLCBlocks'
    mod_path = os.path.join(os.path.expandvars(r'%APPDATA%\SpaceEngineers\Mods'), mod_name)

    print((description % mod_path).strip() + '\n')

    # Prompt the user for the SpaceEngineers folder
    while True:
        se_path = input('Please write your SpaceEngineers folder path: (Press Ctrl+C to exit)\n> ')
        if not os.path.exists(se_path):
            print('Could not find the path \'%s\' please try again\n\n' % se_path)
            continue
        break
    
    # Generate the xml file with hidden DLCs
    dlc_hide_xml = generate_dlc_hiding(se_path, [])
    
    # Generate the local mod from the hidden DLCs
    generate_local_mod(mod_path, mod_name, dlc_hide_xml)
    
