import subprocess
import time
import progressbar,os,csv
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def downloader(indir=None,outdir=None,asset=None,infile=None):
    if infile==None:
        aoicount=[]
        dirc=[]
        sizeup=[]
        for filename in os.listdir(indir):

            if filename.endswith('.json'):
                print(' ')
                print("Using Directory sort & processing "+str(filename)+' Asset type '+str(asset))
                aoi=os.path.join(indir,filename)
                activate= subprocess.check_output("python download.py --query "+'"'+aoi+'" '+"--check "+asset+'"')
                item=int((str(activate).split('...')[1].split(' available')[0]))#Count number of items
                remain=int(activate.count("active"))-1
                err=int(activate.count("Could not"))
                #splitting output by line
                print('Number of Items '+str(item))
                print("Number of assets active "+str(remain))
                print("Number of assets could not activate "+str(err))

                while int(remain)+int(err)<int(item):
                    print("Active Items: "+str(remain)+" of Total Items: "+str(item))
                    bar = progressbar.ProgressBar()
                    for z in bar(range(60)):
                        time.sleep(1)
                    check= subprocess.check_output("python download.py --query "+'"'+aoi+'" '+"--check "+asset+'"')
                    remain=int(check.count("active"))-1
                sizeinit=len(os.walk(outdir).next()[2])
                neg=("python download.py --query "+'"'+aoi+'" '+"--download "+'"'+outdir+'" '+asset+'"')
                print("Starting to Download assets for "+str(os.path.basename(aoi)))
                subprocess.call(neg)
                sizefinal=len(os.walk(outdir).next()[2])
                totaldown=int(sizefinal)-int(sizeinit)
                combined='Using '+str(os.path.basename(aoi))+' downloaded '+str(totaldown)+' '+str(asset)
                aoicount.append(str(combined))
                dirc.append((outdir))
            sz=list(set(dirc))
            for elem in sz:
                pathsize='Base Folder :'+str(os.path.basename(elem))+' has '+str(len(os.walk(elem).next()[2]))+' assets'
                sizeup.append(pathsize)
            #print(', '.join(sizeup))
        #print(', '.join(aoicount))
        subprocess.call("python slack_notifier.py botupdate --msg "+'"'+'\n '.join(aoicount)+'"')
        subprocess.call("python slack_notifier.py botupdate --msg "+'"'+'____________________________________________________________________'+'"')
        subprocess.call("python slack_notifier.py botupdate --msg "+'"'+'\n'.join(sizeup)+'"')

    else:
        with open(infile) as csvFile:
            reader = csv.DictReader(csvFile)
            aoicount=[]
            dirc=[]
            sizeup=[]
            for row in reader:
                aoi=str(row["pathways"])
                outdir=str(row["directory"])
                asset=str(row["asset"])
                print(' ')
                print("Using CSV file & processing "+str(os.path.basename(aoi))+' Asset type '+str(asset))
                activate= subprocess.check_output("python download.py --query "+'"'+aoi+'" '+"--check "+asset+'"')
                item=int((str(activate).split('...')[1].split(' available')[0]))#Count number of items
                remain=int(activate.count("active"))-1
                err=int(activate.count("Could not"))
                print('Number of Items '+str(item))
                print("Number of assets active "+str(remain))
                print("Number of assets could not activate "+str(err))

                while int(remain)+int(err)<int(item):
                    print("Active Items: "+str(remain)+" of Total Items: "+str(item))
                    bar = progressbar.ProgressBar()
                    for z in bar(range(60)):
                        time.sleep(1)
                    check= subprocess.check_output("python download.py --query "+'"'+aoi+'" '+"--check "+asset+'"')
                    remain=int(check.count("active"))-1
                sizeinit=len(os.walk(outdir).next()[2])
                neg=("python download.py --query "+'"'+aoi+'" '+"--download "+'"'+outdir+'" '+asset+'"')
                print("Starting to Download assets for "+str(os.path.basename(aoi)))
                subprocess.call(neg)
                sizefinal=len(os.walk(outdir).next()[2])
                totaldown=int(sizefinal)-int(sizeinit)
                combined='Using '+str(os.path.basename(aoi))+' downloaded '+str(totaldown)+' '+str(asset)
                aoicount.append(str(combined))
                dirc.append((outdir))
            sz=list(set(dirc))
            for elem in sz:
                pathsize='Base Folder :'+str(os.path.basename(elem))+' has '+str(len(os.walk(elem).next()[2]))+' assets'
                sizeup.append(pathsize)
            #print(', '.join(sizeup))
        #print(', '.join(aoicount))
        subprocess.call("python slack_notifier.py botupdate --msg "+'"'+'\n '.join(aoicount)+'"')
        subprocess.call("python slack_notifier.py botupdate --msg "+'"'+'____________________________________________________________________'+'"')
        subprocess.call("python slack_notifier.py botupdate --msg "+'"'+'\n'.join(sizeup)+'"')
