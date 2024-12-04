import copy
import opsc
import oobb
import oobb_base
import yaml
import os

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    # save_type variables
    if True:
        filter = ""
        #filter = "test"

        kwargs["save_type"] = "none"
        #kwargs["save_type"] = "all"
        
        navigation = False
        #navigation = True    

        kwargs["overwrite"] = True
        
        #kwargs["modes"] = ["3dpr", "laser", "true"]
        kwargs["modes"] = ["3dpr"]
        #kwargs["modes"] = ["laser"]

    # default variables
    if True:
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        part_default = {} 
        part_default["project_name"] = "test" ####### neeeds setting
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 4
        p3["height"] = 5
        p3["thickness"] = 3
        p3["extra"] = "electronic_breakout_board_mcu_esp32_30_pin_espressif_esp32"
        part["kwargs"] = p3
        part["name"] = "base"
        parts.append(part)

        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 4
        p3["height"] = 4
        p3["thickness"] = 3
        p3["extra"] = "electronic_breakout_board_mcu_esp32_30_pin_espressif_esp32"
        part["kwargs"] = p3
        part["name"] = "base"
        parts.append(part)

    #make the parts
    if True:
        for part in parts:
            name = part.get("name", "default")            
            extra = part["kwargs"].get("extra", "")
            if filter in name or filter in extra:
                print(f"making {part['name']}")
                make_scad_generic(part)            
                print(f"done {part['name']}")
            else:
                print(f"skipping {part['name']}")


    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        generate_navigation(sort = sort)

def get_base(thing, **kwargs):
    extra = kwargs.get("extra", "")
    if "electronic_breakout_board_mcu_esp32_30_pin_espressif_esp32" in extra:
        get_base_electronic_breakout_board_mcu_esp32_30_pin_espressif_esp32(thing, **kwargs)

def get_base_electronic_breakout_board_mcu_esp32_30_pin_espressif_esp32(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    if height == 4:
        p3["holes"] = ["top", "bottom"]
    else:
        p3["holes"] = ["top", "bottom","left"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    depth_lift = 3
    depth_total = depth + depth_lift
    
    #add screw_countersunk_holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["depth"] = depth_total
    p3["radius_name"] = "m3"
    
    
    shift_board_x = 0
    shift_board_y = 0
    if height == 5:
        shift_board_x = 0
        shift_board_y = 5

    pos1 = copy.deepcopy(pos)
    pos1[2] += 0
    shift_x = 0.9*25.4/2
    shift_y = 1.85*25.4/2
    pos11 = copy.deepcopy(pos1)
    pos11[0] += shift_x + shift_board_x
    pos11[1] += shift_y + shift_board_y
    pos12 = copy.deepcopy(pos1)
    pos12[0] += -shift_x + shift_board_x
    pos12[1] += shift_y + shift_board_y
    pos13 = copy.deepcopy(pos1)
    pos13[0] += -shift_x + shift_board_x
    pos13[1] += -shift_y + shift_board_y
    pos14 = copy.deepcopy(pos1)
    pos14[0] += shift_x + shift_board_x
    pos14[1] += -shift_y + shift_board_y
    poss = []
    poss.append(pos11)
    poss.append(pos12)
    poss.append(pos13)
    poss.append(pos14)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)
    rot1[0] = 180
    p3["rot"] = rot1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)

    #lift cubes

    min = 0.5
    size_lift_cube_top = [5.25-min, 6.85-min, depth_lift]

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_cube"
    p3["size"] = size_lift_cube_top    
    pos1 = copy.deepcopy(pos)
    pos1[0] += shift_board_x
    pos1[1] += shift_board_y
    pos1[2] += depth
    pos11 = copy.deepcopy(pos1)
    shift_x = 11.625
    shift_y = 22.475
    pos11[0] += shift_x
    pos11[1] += shift_y
    pos12 = copy.deepcopy(pos1)
    pos12[0] += -shift_x
    pos12[1] += shift_y
    pos13 = copy.deepcopy(pos1)
    pos13[0] += -shift_x
    pos13[1] += -shift_y
    pos14 = copy.deepcopy(pos1)
    pos14[0] += shift_x
    pos14[1] += -shift_y

    poss = []
    poss.append(pos11)
    poss.append(pos12)
    poss.append(pos13)
    poss.append(pos14)
    p3["pos"] = poss    
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)


    #pin under cutouts
    ex = 1
    size_pin_cutout_cube = [2.54 + ex, (2.54*15)+ex, depth_total]
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    p3["size"] = size_pin_cutout_cube
    pos1 = copy.deepcopy(pos)
    pos1[0] += shift_board_x
    pos1[1] += shift_board_y
    pos1[2] += 0
    pos11 = copy.deepcopy(pos1)
    shift_x = 1*25.4/2
    shift_y = 0
    pos11[0] += shift_x
    pos11[1] += shift_y
    pos12 = copy.deepcopy(pos1)
    pos12[0] += -shift_x
    pos12[1] += shift_y
    poss = []
    poss.append(pos11)
    poss.append(pos12)
    p3["pos"] = poss
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)

    #reset button cutout
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    w = 18.5
    h = 8
    d = depth_total
    p3["size"] = [w, h, d]
    pos1 = copy.deepcopy(pos)
    pos1[0] += shift_board_x
    pos1[1] += 26.9 + shift_board_y- h/2
    pos1[2] += 0
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)

    #usb cutout
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    w = 12
    h = 14
    d = depth_total
    p3["size"] = [w, h, d]
    pos1 = copy.deepcopy(pos)
    pos1[0] += shift_board_x
    pos1[1] += 31.9 + shift_board_y
    pos1[2] += 0
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
###### utilities



def make_scad_generic(part):
    
    # fetching variables
    name = part.get("name", "default")
    project_name = part.get("project_name", "default")
    
    kwargs = part.get("kwargs", {})    
    
    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{name}"

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")

    #get the part from the function get_{name}"
    func = globals()[f"get_{name}"]    
    # test if func exists
    if callable(func):            
        func(thing, **kwargs)        
    else:            
        get_base(thing, **kwargs)   
    
    folder = f"scad_output/{thing['id']}"

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        

        opsc.opsc_make_object(f'{folder}/{mode}.scad', thing["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)  

    yaml_file = f"{folder}/working.yaml"
    with open(yaml_file, 'w') as file:
        part_new = copy.deepcopy(part)
        kwargs_new = part_new.get("kwargs", {})
        kwargs_new.pop("save_type","")
        part_new["kwargs"] = kwargs_new
        import os
        cwd = os.getcwd()
        part_new["project_name"] = cwd
        part_new["id"] = thing["id"]
        part_new["thing"] = thing
        yaml.dump(part_new, file)

def generate_navigation(folder="scad_output", sort=["width", "height", "thickness"]):
    #crawl though all directories in scad_output and load all the working.yaml files
    parts = {}
    for root, dirs, files in os.walk(folder):
        if 'working.yaml' in files:
            yaml_file = os.path.join(root, 'working.yaml')
            #if working.yaml isn't in the root directory, then do it
            if root != folder:
                with open(yaml_file, 'r') as file:
                    part = yaml.safe_load(file)
                    # Process the loaded YAML content as needed
                    part["folder"] = root
                    part_name = root.replace(f"{folder}","")
                    
                    #remove all slashes
                    part_name = part_name.replace("/","").replace("\\","")
                    parts[part_name] = part

                    print(f"Loaded {yaml_file}: {part}")

    pass
    for part_id in parts:
        part = parts[part_id]
        kwarg_copy = copy.deepcopy(part["kwargs"])
        folder_navigation = "navigation_oobb"
        folder_source = part["folder"]
        folder_extra = ""
        for s in sort:
            if s == "name":
                ex = part.get("name", "default")
            else:
                ex = kwarg_copy.get(s, "default")
            folder_extra += f"{s}_{ex}/"

        #replace "." with d
        folder_extra = folder_extra.replace(".","d")            
        folder_destination = f"{folder_navigation}/{folder_extra}"
        if not os.path.exists(folder_destination):
            os.makedirs(folder_destination)
        if os.name == 'nt':
            #copy a full directory auto overwrite
            command = f'xcopy "{folder_source}" "{folder_destination}" /E /I /Y'
            print(command)
            os.system(command)
        else:
            os.system(f"cp {folder_source} {folder_destination}")

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)