# Build.py --platforms windows ios android
#          --serial XX-XXXX-XXXX-XXXX-XXXX-XXXX
#          --username username
#          --password password
#          --unitypath "C:\Unitypath"
#          --projectpath "C:\Projectpath"
#          --tests
#          --debug

import subprocess
import argparse
import time

parser = argparse.ArgumentParser(description='Triggers build for multiple platforms in unity.')
parser.add_argument('--platforms', nargs='+', help='An optional integer positional argument', required=True)
parser.add_argument('--serial', help='Unity licence serial number.', required=True)
parser.add_argument('--username', help='Your account username.', required=True)
parser.add_argument('--password', help='Your account password.', required=True)
parser.add_argument('--unitypath', help='Unity engine path.', required=True)
parser.add_argument('--projectpath', help='Unity project path.', required=True)
parser.add_argument('--tests', action='store_true', help='Run tests before build.')
parser.add_argument('--debug', action='store_true', help='Run build in debug mode.')
args = parser.parse_args()

if args.tests:
    print("Starting tests...")
    start_time = time.time()
    result = subprocess.run([args.unitypath,
                             "-serial", args.serial,
                             "-username", args.username,
                             "-password", args.password,
                             "-projectPath", args.projectpath,
                             "-logFile", args.projectpath + "\\Build\\log.txt",
                             "-batchmode",
                             "-editorTestsResultFile", args.projectpath + "\\Build\\testresults.xml",
                             "-runEditorTests"])

    if result.returncode != 0:
        raise ValueError('Test failed aborting build.')
    print("Finished successfully in %s seconds." % (time.time() - start_time))

for platform in args.platforms:
    print("Starting %s build..." % platform)
    start_time = time.time()
    result = subprocess.run([args.unitypath,
                             "-serial", args.serial,
                             "-username", args.username,
                             "-password", args.password,
                             "-projectPath", args.projectpath,
                             "-logFile", args.projectpath + "\\Build\\log.txt",
                             "-batchmode",
                             "-quit",
                             "-executeMethod", "Assets.Scripts.Editor.BuildUtils.Build",
                             platform,
                             args.projectpath + "\\Build\\" + platform,
                             'debug' if args.debug else ''])

    if result.returncode != 0:
        raise ValueError('Build failed.')
    print("Finished successfully in %s seconds." % (time.time() - start_time))
