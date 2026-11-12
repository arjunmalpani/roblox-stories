"""Run the shot renderer in Blender from any machine (same arguments as tools/render.py):
    python tools/blend.py <slug> preview all          middle frame of each shot, 25% res
    python tools/blend.py <slug> still:12.3 14 16     one frame of shot 14 at t=12.3s
    python tools/blend.py <slug> cues                 write audio/cues.json
    python tools/blend.py <slug> final [ids]          every frame, full res (slow: run in the background)
Blender comes from config.json "blender", $BLENDER, PATH or the usual install folders.
Blender's own chatter is hidden; add --verbose to see it."""
import os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit

args = [a for a in sys.argv[1:] if a != "--verbose"]
verbose = "--verbose" in sys.argv
if len(args) < 2:
    sys.exit(__doc__)
b = kit.find_blender()
if not b:
    sys.exit("Blender not found. Install Blender 5.2 or newer, or put its path in config.json as \"blender\".")
cmd = [b, "-b", "--factory-startup", "-P", os.path.join(kit.STUDIO, "tools", "render.py"), "--"] + args
import platform, shutil
if platform.system() == "Linux" and not os.environ.get("DISPLAY") and shutil.which("xvfb-run"):
    cmd = ["xvfb-run", "-a", "-s", "-screen 0 1920x1080x24 +extension GLX +render"] + cmd
NOISE = re.compile(r"(^Blender \d|^Read prefs|^Warning: |^Color management|^Time: |^$)")
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
show_rest = False
for line in p.stdout:
    if ("FAILED" in line or "Traceback" in line or ("Error" in line and "HIPEW" not in line and "HIP dynamic" not in line)):
        show_rest = True
    # Clean up and show frame saves nicely so the user knows it's actively working
    if "Saved:" in line:
        frame_match = re.search(r"(\d{4})\.png", line)
        if frame_match:
            sys.stdout.write(f"  ↳ Rendered frame {frame_match.group(1)}\n")
            sys.stdout.flush()
            continue
    if verbose or show_rest or not NOISE.search(line):
        sys.stdout.write(line); sys.stdout.flush()
sys.exit(p.wait())
