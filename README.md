# potree_app
This app will build a potree octree from las, laz, binary ply, xyz or ptx files. This app uses open source [Potree Converter](https://github.com/potree/PotreeConverter/tree/using_laszip) along with the [Potree web renderer](https://github.com/potree/potree).
The pre-built image can be downloaded [here](https://console.cloud.google.com/gcr/images/ml-datalab-datatools-01-pr/GLOBAL/potcon?project=ml-datalab-datatools-01-pr&organizationId=846774596521&gcrImageListsize=30), if using the image, start from step 2 below, otherwise start with step 1.
## To use this image:
###### 1. `./build.sh` to create new image with the latest code after pulling this repo
###### 2. `./start.sh -i /path/to/input/folder -o /path/to/output/folder` note: folders must be given as in and out paths
######      - when starting, potree data already in out will be rendered
######      - if no '-i' or '-o' flags given, defualts will be used (shown below)
######      - webpage should be brought up automatically, when conversion and rendering are complete, refresh the page to see the data
## Adding more data
if you want to add more data to be converted/rendered while the app is running, then add it to the specified in and out folders.
###### 1. Add any ply files into the in path, and any potree data into the out path
###### 2. `./run.sh -c -r` '-c' flag is for converting, '-r' flag is to render, either or both can be used
######      - if new data is rendered then refresh the webpage when it is done to see it in app
## Defaults
If no in or out folder is specified then defaults will be used. this will be $HOME/workspace/tmp for in and $HOME/workspace/out for out. below outlines the expected directory structure in the in and out folders. Note that data can be in root directory or one layer deep inside folders.
###### 1. make a local directory in /home/ with the following structure:
        /workspace
        |-- out
        |   |-- high
        |   |   |-- scan_0
        |   |   |   |-- tmp
        |   |   |   |-- data
        |   |   |   `-- cloud.js
        |   |   |-- scan_1
        |   |   `-- scan_2
        |   `-- scan_1
        `-- tmp
            |-- high
            |   |-- scan_0.ply
            |   |-- scan_1.ply
            |   `-- scan_2.ply
            |-- scan_1.ply
            `--low
                |-- scan_0.ply
                |-- scan_1.ply
                `-- scan_2.ply
###### 2. Notice that ply data can be in folders or in root directory, same for converted data