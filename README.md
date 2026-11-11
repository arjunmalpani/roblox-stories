# 🎬 Roblox Story Kit & Colab Cloud Renderer

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arjunmalpani/roblox-stories/blob/main/render_in_colab.ipynb)

A complete automated studio for high-retention Roblox-style 3D animated story videos (9:16 vertical shorts, 60–120s) with expressive characters, fast camera moves, captions, sound effects, and music.

---

## ⚡ Cloud GPU Rendering via Google Colab

Render videos using free Google Colab cloud GPUs (T4 / L4) without placing load on your local PC:

1. Click the **Open In Colab** badge above.
2. Select **Runtime** > **Change runtime type** > **T4 GPU**.
3. Run the cells in `render_in_colab.ipynb` to:
   - Download headless Blender 5.2 (Linux)
   - Render all frames with GPU acceleration
   - Mix voiceover, cues, sound effects, and music
   - Download the finished `final.mp4` directly to your computer!

---

## 📁 Project Structure

```text
roblox-stories/
├── assets/                 # Textures, expressions, and faces
├── music/                  # Background music track
├── rbx/                    # 3D character rigs, sets, and animation engine
├── sfx/                    # Sound effects library
├── tools/                  # Pipeline scripts (blend, voice, finish, mix)
├── videos/
│   ├── hiccup_shrink/      # "In this world, hiccups make you shrink"
│   ├── sneeze_teleport/    # "In this world, sneezing teleports you"
│   └── laugh_float/        # "In this world, laughing makes you float"
└── render_in_colab.ipynb   # 1-click cloud renderer notebook
```
