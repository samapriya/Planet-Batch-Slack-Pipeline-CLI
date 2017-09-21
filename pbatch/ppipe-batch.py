#! /usr/bin/env python

import argparse,logging,os,csv,subprocess
from slacker import Slacker
from activate import activate
from asset_downloader import downloader
from cli_metadata import metadata
from cli_space import space
from os.path import expanduser
from cli_aoiupdate import aoiupdate
from cli_aoi2json import aoijson
import getpass
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def planet_key_entry():
    planethome=expanduser("~/.config/planet/")
    if not os.path.exists(planethome):
        os.mkdir(planethome)
    print("Enter your Planet API Key")
    password=getpass.getpass()
    os.chdir(planethome)
    with open("pkey.csv",'w') as completed:
        writer=csv.writer(completed,delimiter=',',lineterminator='\n')
        writer.writerow([password])
def planet_key_from_parser(args):
    planet_key_entry()
def aoijson_from_parser(args):
    aoijson(start=args.start,end=args.end,cloud=args.cloud,inputfile=args.inputfile,geo=args.geo,loc=args.loc)

def activate_from_parser(args):
    activate(indir=args.indir,
             asset=args.asset,
             infile=args.infile)
def aoiupdate_from_parser(args):
    aoiupdate(indir=args.indir,
             days=args.days,
             infile=args.infile)
def space_from_parser(args):
    space(indir=args.indir,
         asset=args.asset,
         infile=args.infile)
def downloader_from_parser(args):
    downloader(indir=args.indir,
             outdir=args.outdir,
             asset=args.asset,
             infile=args.infile)
def metadata_from_parser(args):
    metadata(asset=args.asset,mf=args.mf,mfile=args.mfile,errorlog=args.errorlog)

def slack_key_main():
    slackhome=expanduser("~/.config/slackkey/")
    if not os.path.exists(slackhome):
        os.mkdir(slackhome)
    print("Enter your SlackBot Admin Token")
    password=getpass.getpass()
    os.chdir(slackhome)
    with open("slack_main.csv",'w') as completed:
        writer=csv.writer(completed,delimiter=',',lineterminator='\n')
        writer.writerow([password])
def slack_main_from_parser(args):
    slack_key_main()
    
#Slack Bot Key
def slack_key_bot():
    slackhome=expanduser("~/.config/slackkey/")
    if not os.path.exists(slackhome):
        os.mkdir(slackhome)
    print("Enter your SlackBot Bot Token")
    password=getpass.getpass()
    os.chdir(slackhome)
    with open("slack_key.csv",'w') as completed:
        writer=csv.writer(completed,delimiter=',',lineterminator='\n')
        writer.writerow([password])
def slack_bot_from_parser(args):
    slack_key_bot()
    
#Slack Message Post        
def botupdate(args):
    tkn=expanduser("~/.config/slackkey/slack_key.csv")
    if os.path.isfile(tkn):
        f=open(tkn)
        for row in csv.reader(f):
            tkin=str(row).strip("[']")
            tk=tkin
    else:
        print("Enter your SlackBot Token")
        tk=getpass.getpass()
    if args.channel==None:
        args.channel='#general'
        slack=Slacker(tk)
        slack.chat.post_message(args.channel, args.msg)
    else:
        slack=Slacker(tk)
        slack.chat.post_message(args.channel, args.msg)

#Slack Message Update
def botfile(args):
    tkn=expanduser("~/.config/slackkey/slack_key.csv")
    if os.path.isfile(tkn):
        f=open(tkn)
        for row in csv.reader(f):
            tkin=str(row).strip("[']")
            tk=tkin
    else:
        print("Enter your SlackBot Token")
        tk=getpass.getpass()
    if args.channel==None:
        args.channel='#general'
        slack=Slacker(tk)
        slack.files.upload(args.filepath,channels=args.channel,filename=args.fname,initial_comment=args.cmmt)
    else:
        slack=Slacker(tk)
        slack.files.upload(args.filepath,channels=args.channel,filename=args.fname,initial_comment=args.cmmt)

#Slack Delete all messages and files
def slackdelete():
    tkn=expanduser("~/.config/slackkey/slack_main.csv")
    if os.path.isfile(tkn):
        f=open(tkn)
        for row in csv.reader(f):
            tkin=str(row).strip("[']")
            tk=tkin
    else:
        print("Enter your Slack-Main Token")
        tk=getpass.getpass()
    subprocess.call('slack-cleaner --token '+tk+" --message --channel general --bot --perform --rate 1")
    subprocess.call('slack-cleaner --token '+tk+" --file --channel general --bot --perform --rate 1")
def slackdelete_from_parser(args):
    slackdelete()

spacing="                               "
def main(args=None):
    parser = argparse.ArgumentParser(description='Planet Batch Tools and Slack Addons')

    subparsers = parser.add_subparsers()

    parser_pp3 = subparsers.add_parser(' ', help='-------------------------------------------')
    parser_P2 = subparsers.add_parser(' ', help='-----Choose from Planet Batch Tools-----')
    parser_pp4 = subparsers.add_parser(' ', help='-------------------------------------------')

    parser_planet_key = subparsers.add_parser('planetkey', help='Enter your planet API Key')
    parser_planet_key.set_defaults(func=planet_key_from_parser)

    parser_aoijson=subparsers.add_parser('aoijson',help='Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat WRS PathRow file to AreaOfInterest.JSON file with structured query for use with Planet API 1.0')
    parser_aoijson.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijson.add_argument('--inputfile',help='Choose a kml/shapefile/geojson or WKT file for AOI(KML/SHP/GJSON/WKT) or WRS (6 digit RowPath Example: 023042)')
    parser_aoijson.add_argument('--geo', default='./map.geojson',help='map.geojson/aoi.kml/aoi.shp/aoi.wkt file')
    parser_aoijson.add_argument('--loc', help='Location where aoi.json file is to be stored')
    parser_aoijson.set_defaults(func=aoijson_from_parser)
    
    parser_activate = subparsers.add_parser('activate', help='Allows users to batch activate assets using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_activate.add_argument('--indir', help='Input directory with structured json files',default=None)
    parser_activate.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_activate.add_argument('--infile', help='File list with headers pathways:path to json file|asset:asset type|',default=None)
    parser_activate.set_defaults(func=activate_from_parser)

    parser_aoiupdate = subparsers.add_parser('aoiupdate', help='Allows users to batch update assets using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_aoiupdate.add_argument('--indir', help='Choose folder with aoi.json files',default=None)
    parser_aoiupdate.add_argument('--days', help='Choose the number of days before today as new start date for aoi',default=None)
    parser_aoiupdate.add_argument('--infile', help='File list with headers pathways:path to json file',default=None)
    parser_aoiupdate.set_defaults(func=aoiupdate_from_parser)

    parser_space = subparsers.add_parser('space', help='Allows users to batch estimate asset sizes using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_space.add_argument('--indir', help='Input directory with structured json files',default=None)
    parser_space.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_space.add_argument('--infile', help='File list with headers pathways:path to json file|asset:asset type|',default=None)
    parser_space.set_defaults(func=space_from_parser)

    parser_downloader = subparsers.add_parser('downloader', help='Allows users to batch download assets using a directory with json or list of json(Sends updates on Slack if slack key added)')
    parser_downloader.add_argument('--indir', help='Input directory with structured json files',default=None)
    parser_downloader.add_argument('--asset', help='Choose from asset type for example:"PSOrthoTile analytic"|"REOrthoTile analytic"',default=None)
    parser_downloader.add_argument('--outdir', help='Output directory to save the assets',default=None)
    parser_downloader.add_argument('--infile', help='File list with headers pathways:path to json file|directory:output directory|asset:asset type|',default=None)
    parser_downloader.set_defaults(func=downloader_from_parser)

    parser_metadata=subparsers.add_parser('metadata',help='Tool to tabulate and convert all metadata files from Planet|Digital Globe Assets|PGCDEM')
    parser_metadata.add_argument('--asset', help='Choose PS OrthoTile(PSO)|PS OrthoTile DN(PSO_DN)|PS OrthoTile Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band DN(PS4B_DN)|PS3Band Analytic(PS3B)|PS3Band DN(PS3B_DN)|PS3Band Visual(PS3B_V)|RE OrthoTile (REO)|RE OrthoTile Visual(REO_V)|DigitalGlobe MultiSpectral(DGMS)|DigitalGlobe Panchromatic(DGP)|PolarGeospatial CenterDEM Strip(PGCDEM)?')
    parser_metadata.add_argument('--mf', help='Metadata folder?')
    parser_metadata.add_argument('--mfile',help='Metadata filename to be exported along with Path.csv')
    parser_metadata.add_argument('--errorlog',default='./errorlog.csv',help='Errorlog to be exported along with Path.csv')
    parser_metadata.set_defaults(func=metadata_from_parser)
    
    parser_pp1 = subparsers.add_parser(' ', help='-------------------------------------------')
    parser_P = subparsers.add_parser(' ', help='-----Choose from Slack Tools Below-----')
    parser_pp2 = subparsers.add_parser(' ', help='-------------------------------------------')

    parser_slack_key_main = subparsers.add_parser('smain', help='Allows you to save your Slack Main API Token')
    parser_slack_key_main.set_defaults(func=slack_main_from_parser)

    parser_slack_key_bot = subparsers.add_parser('sbot', help='Allows you to save your Slack Bot API Token')
    parser_slack_key_bot.set_defaults(func=slack_bot_from_parser)
    
    parser_botupdate = subparsers.add_parser('botupdate', help='Allows your bot to post messages on slack channel')
    parser_botupdate.add_argument('--channel', help='Slack Bot update channel',default=None)
    parser_botupdate.add_argument('--msg', help='Slack Bot update message',default=None)
    parser_botupdate.set_defaults(func=botupdate)

    parser_botfile = subparsers.add_parser('botfile', help='Allows you to post a file along with comments')
    parser_botfile.add_argument('--channel', help='Slack Bot channel',default=None)
    parser_botfile.add_argument('--filepath', help='Slack Bot file path to upload',default=None)
    parser_botfile.add_argument('--cmmt', help='Slack Bot file comment',default=None)
    parser_botfile.add_argument('--fname', help='Slack Bot filename',default=None)
    parser_botfile.set_defaults(func=botfile)

    parser_slackdelete = subparsers.add_parser('slackdelete', help='Allows users to delete all messages and files posted by bots')
    parser_slackdelete.set_defaults(func=slackdelete_from_parser)




    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
 
#botupdate(msg="This is a long test message")
#botfile(msg="tired",filepath=r"C:\Users\samapriya\Desktop\Tools_Fig\access.jpg",fname="New file",cmmt="Comment at me")
#slackdelete()

