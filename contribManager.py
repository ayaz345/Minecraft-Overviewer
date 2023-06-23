#!/usr/bin/env python3

"""The contrib manager is used to help control the contrib scripts
that are shipped with overviewer in Windows packages."""


import ast
import os.path
import sys

scripts = {     # keys are names, values are scripts
    "convertCyrillic":  "cyrillic_convert.py",
    "playerInspect":    "playerInspect.py",
    "testRender":       "testRender.py",
    "pngit":            "png-it.py",
    "gallery":          "gallery.py",
    "regionTrimmer":    "regionTrimmer.py",
    "contributors":     "contributors.py"
}

# you can symlink or hardlink contribManager.py to another name to have it
# automatically find the right script to run.  For example:
# > ln -s contribManager.py pngit.exe
# > chmod +x pngit.exe
# > ./pngit.exe -h


# figure out what script to execute
argv = os.path.basename(sys.argv[0])

if argv[-4:] == ".exe":
    argv = argv[:-4]
if argv[-3:] == ".py":
    argv = argv[:-3]


usage = """Usage:
%s --list-contribs | <script name> <arguments>

Executes a contrib script.

Options:
  --list-contribs           Lists the supported contrib scripts

""" % os.path.basename(sys.argv[0])

if argv in scripts:
    script = scripts[argv]
    sys.argv[0] = script
else:
    if "--list-contribs" in sys.argv:
        for contrib, script in scripts.items():
            with open(os.path.join("contrib", script)) as f:
                d = f.read()
            node = ast.parse(d, script)
            docstring = ast.get_docstring(node)
            docstring = (
                docstring.strip().splitlines()[0]
                if docstring
                else f"(No description found. Add one by adding a docstring to {script}.)"
            )
            print(f"{contrib} : {docstring}")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] in scripts:
        script = scripts[sys.argv[1]]
        sys.argv = [script] + sys.argv[2:]
    else:
        print(usage, file=sys.stderr)
        sys.exit(1)


torun = os.path.join("contrib", script)

if not os.path.exists(torun):
    print(f"Script '{script}' is missing!", file=sys.stderr)
    sys.exit(1)

exec(compile(open(torun, "rb").read(), torun, 'exec'))
