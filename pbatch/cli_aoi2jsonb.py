import subprocess
import os

def aoijsonb(indir=None,infile=None,start=None,end=None,cloud=None,outdir=None):
    if infile==None:
        folder=indir
        for files in os.listdir(indir):
            ext=os.path.splitext(files)[1]
            if ext==".geojson":
                filetype="GJSON"
                subprocess.call("python pbatch.py aoijson --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --inputfile "+'"'+filetype+'"'+" --geo "+'"'+os.path.join(folder,files)+'"'+" --loc "+'"'+outdir+'"',shell=True)
            elif ext==".kml":
                filetype="KML"
                subprocess.call("python pbatch.py aoijson --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --inputfile "+'"'+filetype+'"'+" --geo "+'"'+os.path.join(folder,files)+'"'+" --loc "+'"'+outdir+'"',shell=True)
            elif ext==".shp":
                filetype="SHP"
                subprocess.call("python pbatch.py aoijson --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --inputfile "+'"'+filetype+'"'+" --geo "+'"'+os.path.join(folder,files)+'"'+" --loc "+'"'+outdir+'"',shell=True)
            elif ext==".wkt":
                filetype="WKT"
                subprocess.call("python pbatch.py aoijson --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --inputfile "+'"'+filetype+'"'+" --geo "+'"'+os.path.join(folder,files)+'"'+" --loc "+'"'+outdir+'"',shell=True)
            else:
                print "Invalid file type provide {.geojson,.kml,.shp,.wkt}"
    else:
        with open(infile) as csvFile:
            reader=csv.DictReader(csvFile)
            for row in reader:
                infilename=str(row['filepath'])
                print(infilename)


