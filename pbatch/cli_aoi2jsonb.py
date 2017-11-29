import subprocess,csv
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
                infilename=str(row['pathways'])
                print(infilename)
                if infilename.endswith(".geojson"):
                    filetype="GJSON"
                    start=row['start']
                    end=row['end']
                    cloud=row['cloud']
                    geofile=row['pathways']
                    outdir=row['outdir']
                    subprocess.call("python pbatch.py aoijson --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --inputfile "+'"'+filetype+'"'+" --geo "+'"'+geofile+'"'+" --loc "+'"'+outdir+'"',shell=True)
                elif infilename.endswith(".kml"):
                    filetype="KML"
                    start=row['start']
                    end=row['end']
                    cloud=row['cloud']
                    geofile=row['pathways']
                    outdir=row['outdir']
                    subprocess.call("python pbatch.py aoijson --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --inputfile "+'"'+filetype+'"'+" --geo "+'"'+geofile+'"'+" --loc "+'"'+outdir+'"',shell=True)
                elif infilename.endswith(".shp"):
                    filetype="SHP"
                    start=row['start']
                    end=row['end']
                    cloud=row['cloud']
                    geofile=row['pathways']
                    outdir=row['outdir']
                    subprocess.call("python pbatch.py aoijson --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --inputfile "+'"'+filetype+'"'+" --geo "+'"'+geofile+'"'+" --loc "+'"'+outdir+'"',shell=True)
                elif infilename.endswith(".wkt"):
                    filetype="WKT"
                    start=row['start']
                    end=row['end']
                    cloud=row['cloud']
                    geofile=row['pathways']
                    outdir=row['outdir']
                    subprocess.call("python pbatch.py aoijson --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --inputfile "+'"'+filetype+'"'+" --geo "+'"'+geofile+'"'+" --loc "+'"'+outdir+'"',shell=True)
                else:
                    print "Invalid file type provide {.geojson,.kml,.shp,.wkt}"
