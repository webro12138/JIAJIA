import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

dirs = os.listdir(r"/workspaces/JIAJIA/dataset/data/real_data")
for dir in dirs:
    name, extension = os.path.splitext(dir)
    print(extension)
    if(extension == ".fts"):
        if(not os.path.exists(os.path.join("/workspaces/JIAJIA/dataset/data/SLNDatasets", name))):
            os.mkdir(os.path.join("/workspaces/JIAJIA/dataset/data/SLNDatasets", name))
        #os.rename(os.path.join(r"/workspaces/JIAJIA/dataset/data/real_data", name+".wb"), os.path.join("/workspaces/JIAJIA/dataset/data/SLNDatasets", name, "edges.txt"))
        os.rename(os.path.join(r"/workspaces/JIAJIA/dataset/data/real_data", name+".fts"), os.path.join("/workspaces/JIAJIA/dataset/data/SLNDatasets", name, "features.txt"))