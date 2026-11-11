"""Fish Audio TTS tool for Roblox Stories:
    python tools/fish.py tts <slug>    videos/<slug>/script.txt -> videos/<slug>/audio/raw.mp3
    python tools/fish.py check        check API key and voice model access

Key: FISH_API_KEY environment variable or in .env
Model/Voice: config.json 'fish_audio_model_id' (e.g. d4014f074be14859b458d399e76daa72)
"""
import json, os, re, sys, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit

API_URL = "https://api.fish.audio/v1/tts"


def get_api_key():
    key = os.environ.get("FISH_API_KEY", "").strip()
    if not key:
        env_path = os.path.join(kit.STUDIO, ".env")
        if os.path.exists(env_path):
            for line in open(env_path, encoding="utf-8"):
                m = re.match(r"\s*FISH_API_KEY\s*=\s*['\"]?([^'\"\s]+)", line)
                if m:
                    key = m.group(1)
    return key


def get_model_id():
    cfg = kit.cfg()
    return cfg.get("fish_audio_model_id", "d4014f074be14859b458d399e76daa72")


def script_text(slug):
    p = os.path.join(kit.STUDIO, "videos", slug, "script.txt")
    lines = [l.strip() for l in open(p, encoding="utf-8") if l.strip() and not l.lstrip().startswith("#")]
    return " ".join(lines)


def generate_tts(text, model_id, out_path):
    key = get_api_key()
    if not key:
        sys.exit("Error: FISH_API_KEY not found in environment or .env file.")

    payload = {
        "text": text,
        "reference_id": model_id,
        "format": "mp3"
    }

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            audio_data = resp.read()
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(audio_data)
            return len(audio_data)
    except urllib.error.HTTPError as e:
        sys.exit(f"Fish Audio error {e.code}: {e.read().decode('utf-8', 'replace')}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)

    action = sys.argv[1]
    model_id = get_model_id()

    if action == "check":
        key = get_api_key()
        if not key:
            sys.exit("Error: FISH_API_KEY not found.")
        print(f"Testing Fish Audio with model {model_id}...")
        try:
            generate_tts("Testing connection.", model_id, os.path.join(kit.STUDIO, "tools", ".test.mp3"))
            if os.path.exists(os.path.join(kit.STUDIO, "tools", ".test.mp3")):
                os.remove(os.path.join(kit.STUDIO, "tools", ".test.mp3"))
            print(f"Fish Audio connection OK! Model '{model_id}' is valid and ready.")
        except Exception as e:
            sys.exit(f"Fish Audio check failed: {e}")

    elif action == "tts":
        slug = sys.argv[2]
        text = script_text(slug)
        out_path = os.path.join(kit.STUDIO, "videos", slug, "audio", "raw.mp3")
        print(f"Generating Fish Audio voiceover for '{slug}' ({len(text)} characters) with model '{model_id}'...")
        size = generate_tts(text, model_id, out_path)
        print(f"Success! Saved raw audio: {out_path} ({size} bytes)")


if __name__ == "__main__":
    main()
