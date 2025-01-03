import os
import math
import luadata
from  pathlib import Path
n = 0
instance_id = {}

def lazyhash(name, guild, level, source):
    return str(name) + str(guild) + str(level) + str(source)

# for filename in os.listdir(os.getcwd()):
#    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
#         v = ""
#         for x in f:
#             if "\"name\"" in x:
#               v = x.split(" = ")[1].split(",")[0].split("\"")[1]
#             if "\"instance_id\"" in x:
#               iid = x.split(" = ")[1].split(",")[0]
#               print(v + " " + iid)
#               if instance_id.get(iid) == None:
#                   instance_id[iid] = []
#               instance_id[iid].append(v)
#               n += 1
# print(n)

# for k,v in instance_id.items():
#     print(k)
#     print(v)

v = {"all": {}}
complete = {}
def importFrom(fp):
    txt = Path(fp).read_text()
    if len(txt) < 1:
        return
    try:
        txt = txt.split("death_log_entries")[1].split('-- [')
        for t in txt:
            try:
                class_id = int(t.split("[\"class_id\"] = ")[1].split(",")[0].replace("\"",""))
                source_id = int(t.split("[\"source_id\"] = ")[1].split(",")[0].replace("\"",""))
                guild = t.split("[\"guild\"] = ")[1].split(",")[0].replace("\"","")
                level = int(t.split("[\"level\"] = ")[1].split(",")[0])
                name = t.split("[\"name\"] = ")[1].split(",")[0].replace("\"","")
                complete[lazyhash(name, guild, level, source_id)] = {}
                area_id = None
                if len(t.split("[\"map_id\"] = ")) > 1:
                    area_id = int(t.split("[\"map_id\"] = ")[1].split(",")[0])
                    complete[lazyhash(name, guild, level, source_id)]['map_id'] = area_id
                    map_pos_x = t.split("[\"map_pos\"] = ")[1].split(",")[0].replace("\"","")
                    map_pos_y = t.split("[\"map_pos\"] = ")[1].split(",")[1].replace("\"","")
                    complete[lazyhash(name, guild, level, source_id)]['map_pos'] = (float(map_pos_x)*1000, float(map_pos_y)*1000)
                elif len(t.split("[\"instance_id\"] = ")) > 1:
                    area_id = int(t.split("[\"instance_id\"] = ")[1].split(",")[0])
                    complete[lazyhash(name, guild, level, source_id)]['instance_id'] = area_id
                complete[lazyhash(name, guild, level, source_id)]['class_id'] = class_id
                complete[lazyhash(name, guild, level, source_id)]['area_id'] = area_id
                complete[lazyhash(name, guild, level, source_id)]['source_id'] = source_id
                complete[lazyhash(name, guild, level, source_id)]['level'] = level
            except:
                pass
    except:
        try:
            txt = txt.split("deathlog_data")[1]
            txt = txt.split("\n\t\t[")
            for t in txt:
                try:
                    class_id = int(t.split("[\"class_id\"] = ")[1].split(",")[0].replace("\"",""))
                    source_id = int(t.split("[\"source_id\"] = ")[1].split(",")[0].replace("\"",""))
                    guild = t.split("[\"guild\"] = ")[1].split(",")[0].replace("\"","")
                    level = int(t.split("[\"level\"] = ")[1].split(",")[0])
                    name = t.split("[\"name\"] = ")[1].split(",")[0].replace("\"","")
                    complete[lazyhash(name, guild, level, source_id)] = {}
                    area_id = None
                    if len(t.split("[\"map_id\"] = ")) > 1:
                        area_id = int(t.split("[\"map_id\"] = ")[1].split(",")[0])
                        complete[lazyhash(name, guild, level, source_id)]['map_id'] = area_id
                        map_pos_x = t.split("[\"map_pos\"] = ")[1].split(",")[0].replace("\"","")
                        map_pos_y = t.split("[\"map_pos\"] = ")[1].split(",")[1].replace("\"","")
                        complete[lazyhash(name, guild, level, source_id)]['map_pos'] = (float(map_pos_x)*1000, float(map_pos_y)*1000)
                    elif len(t.split("[\"instance_id\"] = ")) > 1:
                        area_id = int(t.split("[\"instance_id\"] = ")[1].split(",")[0])
                        complete[lazyhash(name, guild, level, source_id)]['instance_id'] = area_id
                    complete[lazyhash(name, guild, level, source_id)]['class_id'] = class_id
                    complete[lazyhash(name, guild, level, source_id)]['area_id'] = area_id
                    complete[lazyhash(name, guild, level, source_id)]['source_id'] = source_id
                    complete[lazyhash(name, guild, level, source_id)]['level'] = level

                except Exception as e: print(e)
        except:
            return
print(len(complete))

for filename in os.listdir(os.getcwd()):
    importFrom(os.path.join(os.getcwd(), filename))
    print(len(complete))

def updateEntry(d, e):
    d["num_entries"]+=1
    d["sum_lvl"]+=int(e['level'])

def createLeaf():
    return {"num_entries": 0, "sum_lvl": 0, "avg_lvl": 0}

stats = {"all": {"all": {"all": {"all": createLeaf()}}}}
skull_locs = {}

def updateFromEntry(entry):
    updateEntry(stats["all"]["all"]["all"]["all"], entry)

    if stats["all"].get(entry["area_id"]) == None:
        stats["all"][entry["area_id"]] = {"all": {"all": createLeaf()}}
    updateEntry(stats["all"][entry["area_id"]]["all"]["all"], entry)

    if stats["all"]["all"].get(entry["class_id"]) == None:
        stats["all"]["all"][entry["class_id"]] = {"all": createLeaf()}
    updateEntry(stats["all"]["all"][entry["class_id"]]["all"], entry)
    if stats["all"][entry["area_id"]].get(entry["class_id"]) == None:
        stats["all"][entry["area_id"]][entry["class_id"]] = {"all": createLeaf()}
    updateEntry(stats["all"][entry["area_id"]][entry["class_id"]]["all"], entry)

    if stats["all"]["all"]["all"].get(entry["source_id"]) == None:
        stats["all"]["all"]["all"][entry["source_id"]] = createLeaf()
    updateEntry(stats["all"]["all"]["all"][entry["source_id"]], entry)
    if stats["all"]["all"][entry["class_id"]].get(entry["source_id"]) == None:
        stats["all"]["all"][entry["class_id"]][entry["source_id"]] = createLeaf()
    updateEntry(stats["all"]["all"][entry["class_id"]][entry["source_id"]], entry)
    if stats["all"][entry["area_id"]][entry["class_id"]].get(entry["source_id"]) == None:
        stats["all"][entry["area_id"]][entry["class_id"]][entry["source_id"]] = createLeaf()
    updateEntry(stats["all"][entry["area_id"]][entry["class_id"]][entry["source_id"]], entry)
    if stats["all"][entry["area_id"]]["all"].get(entry["source_id"]) == None:
        stats["all"][entry["area_id"]]["all"][entry["source_id"]] = createLeaf()
    updateEntry(stats["all"][entry["area_id"]]["all"][entry["source_id"]], entry)


dists = {"all": {}} # area_id, ln_mean, classid, []
num_skull_locs = 0
for k,v in complete.items():
    updateFromEntry(v)
    if v.get("map_id") is not None:
        if skull_locs.get(int(v["map_id"])) == None:
            skull_locs[int(v["map_id"])] = []
        skull_locs[int(v["map_id"])].append([v["map_pos"][0], v["map_pos"][1], int(v["source_id"])])
        num_skull_locs+=1

    if dists["all"].get(int(v["class_id"])) == None:
        dists["all"][int(v["class_id"])] = []
    dists["all"][int(v["class_id"])].append(int(v["level"]))

    if dists.get(int(v["area_id"])) == None:
        dists[int(v["area_id"])] = {int(v["class_id"]): []}
    if dists[int(v["area_id"])].get(int(v["class_id"])) == None:
        dists[int(v["area_id"])][int(v["class_id"])] = []
    dists[int(v["area_id"])][int(v["class_id"])].append(int(v["level"]))


for servername,v in stats.items():
    for mapid,v2 in v.items():
        for class_id,v3 in v2.items():
            for sourceid,v4 in v3.items():
                v4["avg_lvl"] = v4["sum_lvl"]/v4["num_entries"]

lognormals = {}
kaplan_meier = {}
kaplan_list = {}
import numpy as np
import surpyval as surv
import math

for mapid,v in dists.items():
    lognormals[mapid] = {}
    for classid,v2 in v.items():
        ln_mean = 0
        total = 0
        ln_std_dev = 0
        for val in v2:
            total+=1
            ln_mean+=math.log(val)
        ln_mean /= total

        for val in v2:
            ln_std_dev += (math.log(val) - ln_mean) * (math.log(val) - ln_mean)
        ln_std_dev /= total

        lognormals[mapid][classid] = [ln_mean, ln_std_dev, total]

        if mapid == "all":
            tr = 60
            x = np.array(v2)
            x = x[(x<tr)]
            model = surv.LogNormal.fit(x=x, tr=tr)
            print(model)
            lognormals[mapid][classid] = [model.params[0], model.params[1], len(v2)]
            model = surv.Turnbull.fit(x=x, tr=tr)
            kaplan_meier[classid] = list(model.R)
            c = 1
            last_val = 0
            kaplan_list[classid] = []
            for i in range(1,61):
                kaplan_list[classid].append(1-model.ff(i)[0])
            # for i in range(len(model.x)):
            #     if c == model.x[i]:
            #         kaplan_list[classid].append(model.R[i])
            #         c += 1
            #     elif c < model.x[i]:
            #         kaplan_list[classid].append(model.R[i])
            #         kaplan_list[classid].append(model.R[i])
            #         c += 1
            # kaplan_list[classid].append(model.R[-1])
            print(model.R, model.x)
            print(len(kaplan_list[classid]), kaplan_list)


iv = {0: {0:.025, 1:.045, 2:.025},1: {0:.045, 1:.1, 2:.045},2: {0:.025, 1:.045, 2:.025}}
heatmap = {}
for mapid, d in skull_locs.items():
    max_intensity = 0
    heatmap[mapid] = {}
    for t in d:
        _x = math.ceil(t[0]/10)
        _y = math.ceil(t[1]/10)
        for xi in range(3):
            for yj in range(3):
                x_in_map = _x - 1 + xi
                y_in_map = _y - 1 + yj
                if heatmap[mapid].get(x_in_map) == None:
                    heatmap[mapid][x_in_map] = {y_in_map:0}
                if heatmap[mapid][x_in_map].get(y_in_map) == None:
                    heatmap[mapid][x_in_map][y_in_map] = 0
                heatmap[mapid][x_in_map][y_in_map] += iv[xi][yj]
                if heatmap[mapid][x_in_map][y_in_map] > max_intensity:
                    max_intensity = heatmap[mapid][x_in_map][y_in_map]
    to_remove = []
    for k,x in heatmap[mapid].items():
        for y,v in x.items():
            heatmap[mapid][k][y]=heatmap[mapid][k][y]/max_intensity
            if heatmap[mapid][k][y] < 0.02:
                to_remove.append((k,y))
    for k in to_remove:
        del heatmap[mapid][k[0]][k[1]]

    count = 0
    for k,v in heatmap[mapid].items():
        for k2,v2 in v.items():
            count += 1

output_str = "precomputed_general_stats = " + luadata.serialize(stats, encoding="utf-8", indent="\t", indent_level=0)
# output_str += "precomputed_skull_locs = " + luadata.serialize(skull_locs, encoding="utf-8", indent="\t", indent_level=0)
output_str += "precomputed_heatmap_intensity = " + luadata.serialize(heatmap, encoding="utf-8", indent="\t", indent_level=0)
output_str += "precomputed_log_normal_params = " + luadata.serialize(lognormals, encoding="utf-8", indent="\t", indent_level=0)
output_str += "precomputed_kaplan_meier = " + luadata.serialize(kaplan_list, encoding="utf-8", indent="\t", indent_level=0)
output_str = output_str.replace("avg_lvl", "[\"avg_lvl\"]")
output_str = output_str.replace("num_entries", "[\"num_entries\"]")
output_str = output_str.replace("sum_lvl", "[\"sum_lvl\"]")
output_str = output_str.replace("all", "[\"all\"]")
f = open("out.lua", "a")
f.write(output_str)
f.close()
