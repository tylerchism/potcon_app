import sys
import subprocess
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

try:  # allow running directly or installing as package without distinction
    from runtime_parent import RuntimeParent
except ImportError:
    from .runtime_parent import RuntimeParent


class Runtimejob(RuntimeParent):
    def __init__(self, logname=__file__, workspace=None):
        """ Generic runtimejob package """
        super(Runtimejob, self).__init__(workspace=workspace, logname=logname)

        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='Add -c to convert data from in folder')
        parser.add_argument('-r', action='store_true', help='add -r to render potree data in out folder')
        args = parser.parse_args()
        self.define_paths()
        if args.c:
            self.logger.info("Conversion: Attempting to convert data from in folder...")
            self.convert()
        if args.r:
            self.logger.info("Render: Attempting to render potree data in out folder...")
            self.render()

    def define_paths(self):
        # Define paths
        self.path_tar = self.attachments                          # Path where ply/*.tar files are expected to be
        self.ply_path = self.tmp                                  # Path where files from attachments will be untared to
        self.point_clouds = Path("/opt/potree/pointclouds")       # Path where converted files will be sent for offline tool
        self.templates_dir = Path("/home/script/templates")       # Input for jinja2 template loader
        self.filename = Path("/opt/potree/examples/potcon.html")  # Output for jinja2 html creater

    def convert(self):
        ply_list_1 = self.find_ply()
        ply_list_2 = self.find_ply(level=2)
        if not ply_list_1 and not ply_list_2:
            self.logger.warning("No ply files found to convert")
            return
        if ply_list_1:
            dir_list = [directory for directory in self.point_clouds.iterdir() if 'potree_convert' in str(directory)]
            out_sub = Path("{}/potree_convert_{:03d}".format(self.point_clouds, len(dir_list)))
            out_sub.mkdir(exist_ok=False)
            for file in ply_list_1:
                name = str(file)
                subprocess.run("PotreeConverter {} -o {}/{}".format(name, str(out_sub), file.stem), shell=True)
        if ply_list_2:
            for file in ply_list_2:
                name = str(file)
                out_sub = Path("{}/{}".format(self.point_clouds, file.parents[0].stem))
                out_sub.mkdir(exist_ok=True)
                subprocess.run("PotreeConverter {} -o {}/{}".format(name, str(out_sub), file.stem), shell=True)
    
    def render(self):
        # Jinja2 html template expects 2 variables to create potcon.html that will contain pointcloud data
        paths = [] # list of the paths to all the pointcloud data, potree will render them all at once
        names = [] # the associated name of the particalr pointcloud ex. "medium/scene_0"
        cloud_list_1 = self.find_cloud()
        cloud_list_2 = self.find_cloud(level=2)
        if not cloud_list_1 and not cloud_list_2:
            self.logger.error("Could not find potree data to render")
            return
        if cloud_list_1:
            for item in cloud_list_1:
                paths.append('../pointclouds/{}/cloud.js'.format(item.stem))
                names.append('{}'.format(item.stem))
        if cloud_list_2:
            for item in cloud_list_2:
                paths.append('../pointclouds/{}/{}/cloud.js'.format(item.parents[0].stem, item.stem))
                names.append('{}/{}'.format(item.parents[0].stem, item.stem))
        
        # jinja2 code to take template and create html that contains the pointcloud data:
        env = Environment( loader = FileSystemLoader(self.templates_dir))
        template = env.get_template("index.html")

        with open(self.filename, 'w') as fh:
            fh.write(template.render(
                clouds = zip(paths, names)
            ))

    def find_ply(self, level=1):
        if level == 1:
            return [item for item in self.tmp.iterdir() if item.suffix == '.ply']
        elif level == 2:
            ply_list = []
            for items in self.tmp.glob('*'):
                for item in items.glob('*.ply'):
                    ply_list.append(item)
            return ply_list
        else:
            return False

    def find_cloud(self, level=1):
        if level == 1:
            return [item for item in self.point_clouds.iterdir() if item.is_dir() and 'cloud.js' in [i.name for i in item.iterdir()]]
        elif level == 2:
            cloud_list = []
            for items in [item for item in self.point_clouds.iterdir() if item.is_dir() and 'cloud.js' not in [i.name for i in item.iterdir()]]:
                for item in items.glob('*'):
                    if item.is_dir() and 'cloud.js' in [i.name for i in item.iterdir()]:
                        cloud_list.append(item)
            return cloud_list
        else:
            return False



if __name__ == '__main__':
    workspace = '/home/tchism/workspace'  # point to base location with files subdirectory

    if Path(workspace).exists(): Runtimejob(workspace=workspace)
    else: Runtimejob()  # if path not found, attempt official runtimejob
