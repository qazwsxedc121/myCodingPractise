'''
Created on 2012-7-2

@author: guoxc
'''
import json
import Tkinter
test_tree = json.load(open("root_frame.json"))
def tree_print(tr, intend=0):
    if not isinstance(tr, dict):
        raise Exception("tree not a dict")
    if "type" not in tr.keys() or "id" not in tr.keys():
        raise Exception("syntax Error")
    attr_list =  [(str(attr) +":"+str(tr[attr])) for attr in tr if attr not in ("menu","type","id","items")]
    print ("|   " * (intend - 1 if intend > 1 else 0) +
        "|___" * ( 1 if intend >= 1 else 0) + tr["type"] +
        ":" + tr["id"] + "  " +str(attr_list))
    if "menu" in tr.keys():
        tree_print(tr["menu"], intend +1)
    if "items" in tr.keys():
        for item in tr["items"]:
            tree_print(item, intend +1)

def get_menu(tr, parent):
    new_menu = Tkinter.Menu(parent, tearoff=0)
    if "items" in tr.keys():
        for item in tr["items"]:
            if item["type"] == "Menu":
                new_menu.add_cascade(menu=get_menu(item, new_menu),
                                     label=get_menu_text(item))
            elif item["type"] == "MenuItem":
                new_menu.add_command(label=item["text"], command=get_cmd_by_id(item["id"]))
    return new_menu

def get_button(tr, parent):
    opt = get_options(tr)
    new_button = Tkinter.Button(parent, **opt)
    return new_button

def get_entry(tr, parent):
    opt = get_options(tr)
    new_entry = Tkinter.Entry(parent, **opt)
    return new_entry

def get_label(tr, parent):
    opt = get_options(tr)
    new_label = Tkinter.Label(parent, **opt)
    return new_label


def get_options(opdict):
    opt = {}
    for key in opdict.keys():
        if key not in ["type", "id","position","items","class","sticky"]:
            opt[key] = opdict[key]
    return opt


def get_cmd_by_id(id_):
    if id_ +"_cmd" in globals():
        return globals()[id_ +"_cmd"]
    else:
        return None


def menu1_1_3_cmd():
    root.destroy()


def get_menu_text(tr):
    if not tr["text"]:
        return None
    return tr["text"]


def parse_position(text):
    rlist = text.split(" ")
    rlist = [int(item) for item in rlist]
    if len(rlist) == 2:
        return {"row": rlist[0],"column":rlist[1]}
    elif len(rlist) == 4:
        return {"row": rlist[0],"column":rlist[1],"rowspan":rlist[2],"columnspan":rlist[3]}


def tree_parse(tr):
    if tr["menu"]:
        root.config(menu=get_menu(tr["menu"], root))
    if tr["items"] and tr["layout"]:
        if tr["layout"] == "grid":
            for item in tr["items"]:
                position_dict = parse_position(item["position"])
                if "sticky" in item.keys():
                    position_dict["sticky"] = item["sticky"]
                if item["type"] == "Button":
                    get_button(item, root).grid(**position_dict)
                elif item["type"] == "Entry":
                    get_entry(item, root).grid(**position_dict)
                elif item["type"] == "Label":
                    get_label(item, root).grid(**position_dict)

root = Tkinter.Tk()
tree_print(test_tree)
tree_parse(test_tree)
root.mainloop()
