# Planet Batch & Slack Pipeline CLI

### **Talk Slack to Me: Integrating Planet and Slack API for Automation &amp; Batch Notifications**

Yes I agree, the title is longer than usual but to get at the core of what this application could do this was necessary. While the access to data increased as [Planet achieved Mission I (global daily coverage )](https://www.planet.com/pulse/mission-1/) the amount of data and the need to structure them and build efficient pipelines around them also became more critical. While in the past I have written tools which act as pipelines for you to process single areas of interest at the time that could be chained, the need to write something that does a bit more heavy lifting arose. This command line interface(CLI) application was created to handle groups and teams that have multiple areas of interest and multiple input and output buckets and locations to function smoothly. The best part I integrated this to slack so you can be on the move while this task can be on a scheduler and update you when finished.

During the course of this article we will learn a couple of things including setting up a messaging bot for a channel and then using the messaging API to notify of task status and completion. This is part of a tool called the [Planet-Batch-Slack-Pipeline-CLI](https://github.com/samapriya/Planet-Batch-Slack-Pipeline-CLI) that I am releasing today which acts as a load balancer for batch processing Area of Interests AOI(s) using the Planet API. This tool is capable of processing multiple points of interest, while automatically waiting for activation and asset downloading. The keyword throughout this article will be batching and something that is scalable atleast to a large extent within an institutional environment.

The best part, once integrated with Slack&#39;s Messaging API, this sends you a slack message every time a process is completed.

Not only can the tool process all geojson or json(s) in a folder but it can also do the same using a csv list of file path, the asset type you are interested to download and the download location which may vary. This will allow you to create production commands , custom jobs and update the csv file as needed to included additional assets and AOI(s).

**Getting Started with Slack**

This requires you to first create a slack channel within which we will create a slack application allowing a bot to send task notifications. This tool is an extension of the [Planet-GEE-Pipeline-CLI](https://github.com/samapriya/Planet-GEE-Pipeline-CLI) extending only to the Planet side of things and integrating additional tool more streamlined towards downloading and bulk handling of assets.

The first half of this tutorial will thus deal with quickly making a slack channel for your team and then managing components within that. Go to slack&#39;s main page and click on the [sign in page](https://slack.com/signin). And you will get to create a unique channel

The next step we continue with managing the applications that we created by clicking on the Manage apps button

This will take you to the next step where you will be able to build your first shiny new slack app. Click on the Build button

Here all you are doing is specifying the app name and choosing the workspace you want. In case you are logged into more than one workspace you can choose an alternate one.

Once you have created an app you will have options of what the application does and this is where you would select the Bots options since this allows us to add a bot to exchange messages with the app we just created.

Once you click on that the next steps are just confirmation that you are about to add a bot followed by creating a Display name and a default name for the Bot, it can be anything you want so feel free name it _Darth Vader_ :) . You have the option of showing your bot always online which is something I like to do but it is completely optional.

Once you have created the bot you still need to install the application including the new bot you created to your workspace. This is pretty much the last step. Click on the Install App button and choose the Install App to Workspace option.

This will pop up a request asking you for a workspace where you would like to install this app. Note that it might give you a warning that this has not been verified by Slack and that doesn&#39;t matter because you created the app yourself.

The last step of this slack training is to copy the **OAuth Access Token** and the **Bot User OAuth Access Token**. I have filled in some random token numbers to be on the safe side. And you should keep these authorization tokens safe. You can always go back and find them when needed as well. That is it, that is all you need to create and install a new chat bot application in your slack workspace.

The next step we will setup the [Planet-Batch-Slack-Pipeline-CLI](https://github.com/samapriya/Planet-Batch-Slack-Pipeline-CLI) and integrate our previously built slack app for notifications. To setup the prerequisites you need to install the Planet Python API Client and Slack Python API Clients.

- To install the tool you can go to the GitHub page at [Planet-Batch-Slack-Pipeline-CLI](https://github.com/samapriya/Planet-Batch-Slack-Pipeline-CLI). As always two of my favorite operating systems are Windows and Linux, and to install on Linux
git clone https://github.com/samapriya/Planet-Batch-Slack-Pipeline-CLI.git
 cd Planet-Batch-Slack-Pipeline-CLI &amp;&amp; sudo python setup.py install
 pip install -r requirements.txt
- for windows download the zip and after extraction go to the folder containing &quot;setup.py&quot; and open command prompt at that location and type
python setup.py install
 pip install -r requirements.txt

Now call the tool for the first time, by typing in pbatch -h. This will only work if you have python in the system path which you can test for opening up terminal or command prompt and typing python.

Once the requirements have been satisfied the first thing we would setup would be to OAuth Keys we created. The tools consists of a bunch of slack tools as well including capability to just use this tool to send slack messages, attachments and clean up channel as needed.

The two critical setup tools to make Slack ready and integrated are the smain and sbot tools where you will enter the OAuth for the application and OAuth for the bot that you generated earlier. These are then stored into your session for future use, you can call them using

pbatch smain _Use the &quot;_ **OAuth Access Token** _&quot; generated earlier_

pbatch sbot _Use &quot;_ **Bot User OAuth Access Token&quot;** _generated earlier_

Once this is done your bot is now setup to message you when a task is completed. In our case these are tied into individual tools within the batch toolkit we just installed.

**One Batch to Rule Them?**

To be clear these tools were designed based on what I thought was an effective way of looking at data, downloading them and chaining the processes together. They are still a set of individual tools to make sure that one operation is independent of the other and does not break in case of a problem. So a non-monolithic design in some sense to make sure the pieces work. We will go through each of them in the order of use

pbatch planetkey is the obvious one which is your planet API key and will allow you to store this locally to a session.

_The_ **aoijson** _tool is the same tool used in the Planet-EE CLI within the pbatch bundle allows you to bring any existing KML, Zipped Shapefile, GeoJSON, WKT or even Landsat Tiles to a structured geojson file, this is so that the Planet API can read the structured geojson which has additional filters such as cloud cover and range of dates. The tool can then allow you to convert the geojson file to include filters to be used with the Planet Data API._

Let us say we want to convert this [map.geojson](https://filebin.ca/3S3EeDlgNzmj/map.geojson) to a structured aoi.json from _June 1 2017 to June 30th 2017 with 15% cloud cover as our maximum_. We would pass the following command

pbatch.py aoijson --start &quot;2017–06–01&quot; --end &quot;2017–06–30&quot; --cloud &quot;0.15&quot; --inputfile &quot;GJSON&quot; --geo &quot;local path to map.geojson file&quot; --loc &quot;path where aoi.json output file will be created&quot;

**The Batch Approach to Structured JSON(**  **pbatch aoijsonb**** )**

This tool was then rewritten and included in the application to overcome two issues 1) Automatically detect the type of input file I am passing (For now it can automatically handle geojson, kml, shapefile and wkt files). The files are then saved in an output directory with the **filename\_aoi.json . **

The limitation of this is that the same parameters and conditionals are passed to all files in the folder which would be modified in the next iteration of the tool to process these files from a csv list.

**Activate!! but Batch Activate**

This tool was rewritten to provide users with two options to activate their assets. They can either point the tool at a folder and select the item and asset combination or they can specify a CSV file which contains each asset and item type and path to the structured JSON file. A setup would be as simple as

pbatch activate --indir &quot;path to folder with structured json files&quot; --asset &quot;item asset type example: PSOrthoTile analytic&quot;

The csv file need to have headers **pathways | asset**

C:\filepath.json | PSOrthoTile analytic

And guess what this when our slack bot started communicating with us. The read out includes the filename , the asset and item type and the number of item and asset combinations that have been requested for activation

**Load Balance and Download: (Also known as go get a cup of coffee/tea)**

If you have reached here means you are all ready to grab your data which might be activating as we try this out. So we run the downloader tool to batch download these assets and again you can choose to have either a folder or a csv file containing path to the json files, the item asset combination and the output location. A simple setup is thus

pbatch downloader --indir &quot;Pathway to your json file&quot; --asset &quot;PSOrthoTile analytic&quot; --outdir &quot;C:\output-folder&quot;

The csv file need to have headers **pathways | directory |asset**

C:\filepath.json | C:\output folder location | PSOrthoTile analytic

This tool is unique for a few reasons

- This can using the CSV sort to identify different pathways to strctured jsons in different locations, but it can also download different assets for each input file and write to different location each time. Meaning this can be of production value to teams who have different source folders and output buckets where they would want their data to be written.
- The tool also prints information of Number of assets already active, number of assets that could not be activated and the total number of assets. Incase number of assets active do not match those that can be activated it will wait and show you a progressbar before trying again. This is the load balancing for each input file while making sure you don&#39;t have to estimate wait times for large requests.

**Imagine having a university tier license(** [**Investigator or Institutional License**](https://www.planet.com/products/education-and-research/)**) where you manage downloads and users submit requests, this tool will allow you to structure these requests and maintain a status log. **

Last but not the least we get our slack bot reporting back to us with the results. Watch as the number of downloaded assets in folder increases

**Space and Time: And everything in Between**

Two things that keep changing are space (The amount of space needed to store your data) and the time since you may want to look at different time windows . With this in mind an easy way to update you about the total space for the assets you activated I created a tool called pbatch space . A simple setup would be

pbatch space --indir &quot;Input directory with structured json file&quot; --asset &quot;PSOrthoTile analytic&quot;

And it can also consume a csv file where the csv file need to have headers **pathways | asset**

C:\filepath.json | PSOrthoTile analytic

The best part Slack will record the last time you ran this tool because new assets may have activated since you last ran this or new assets may have become available for you to activate.

And now comes time, most often all your data needs can be considered as x number of days from whatever you sent . Meaning I may want to look at 30 days of data from the end date and we don&#39;t want to recreate the structured json files. Turns out we can easily change that using a time delta function and simply rewrite the start date for our json files from which to start looking for data.

Note: Your end date should be current date or later the way the date is now written is date greater than equal to 30 days from today and end date remains constant

A good rule of them to be safe with this tool is to save the end date into the future so for example. The setup maybe

pbatch aoiupdate --indir &quot;directory --days 30

start date &quot; **2017–01–01**&quot; end date &quot; **2017–12–31**&quot;

new start date &quot; **2017–10–26**&quot; new end date &quot; **2017–12–31**&quot;

The slack bot is keeping track of all this and updates us too

There you have it, you now have tools that can help you create more efficient pipelines , talk to a slack bot, load balance and get updates. Additional tools are included in the CLI such as

- **pbatch metadata** which allows you to tabulate metadata and this is for use in conjunction with Google Earth Engine atleast for my workflow.

**Bonus Tools and Goodies**

Well it is near Christmas so why not throw in some extra goodies and bonus tools. So here are a few I built into the Planet-Batch-Slack-Pipeline to allow you to integrate and build around other tools as well as to

**pbatch botupdate** will allow you to send any message to your channel try it type &quot;pbatch botupdate --msg &quot;Hello world&quot;

**pbatch botfile** will allow you send any attachment pictures, codes, json files etc so you can build new tools around it as well. To send a picture for example simply type &quot;pbatch botfile --filepath &quot;Path to file&quot; --fname &quot;name of file&quot;

**pbatch slackdelete** is if your slack channel is too cluttered with logs and you want to delete all of them, feel free to do so. Remember this clears all messages posted by your bot in that channel.

If you find this tool useful and have used it to recreate something or to create better workflow, you can cite it as

-
