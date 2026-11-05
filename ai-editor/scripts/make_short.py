#!/usr/bin/env python3
"""Tokyo 503 short builder — implements style.md v3.

Usage:
  python3 scripts/make_short.py --images raw/proj/imgs --voice raw/proj/voice.mp3 \
      --title "سؤال يقسم الفانز؟" --out done/proj.mp4 [--music raw/music.mp3] [--fit blur|fill]

Pipeline: Whisper word timings -> one image per sentence (cut on sentence boundaries)
-> Ken Burns + punch-zoom on the payoff -> gold title (0-3 s) + word-by-word captions
-> voice chain (+ optional ducked music) -> loudnorm -14 LUFS -> 1080x1920 H.264.
"""
import argparse, glob, os, subprocess, tempfile, sys
import numpy as np

W, H, FPS = 1080, 1920, 30
GOLD = "&H0042C5F5"  # ASS BGR for #F5C542
WHITE = "&H00FFFFFF"
FONT = "Tajawal ExtraBold"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"command failed: {' '.join(cmd[:6])}...\n{r.stderr[-1500:]}")
    return r


def transcribe(voice, model_size):
    from faster_whisper import WhisperModel
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", voice, "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    m = WhisperModel(model_size, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="ar", word_timestamps=True, vad_filter=True)
    sents = []
    for s in segs:
        words = [(w.start, w.end, w.word.strip()) for w in (s.words or []) if w.word.strip()]
        if words:
            sents.append({"start": words[0][0], "end": words[-1][1], "words": words})
    if not sents:
        sys.exit("no speech detected in voice track")
    return sents


def apply_script(sents, script_text):
    """Replace Whisper's words with the true script, keeping Whisper's timing.
    Script sentences are split on . ! ? ؟ ، and newlines; words are mapped onto the
    spoken timeline proportionally, so a few misheard/merged words don't break sync."""
    import re
    timed = [w for s in sents for w in s["words"]]
    t0, t1 = timed[0][0], timed[-1][1]
    # cumulative speech-time axis built from Whisper word spans
    spans = [(st, en) for st, en, _ in timed]
    lines = [l.strip() for l in re.split(r"[.!?؟\n]+", script_text) if l.strip()]
    words = [(li, w) for li, l in enumerate(lines) for w in l.replace("،", " ").split()]
    n, m = len(words), len(spans)
    out = {}
    for i, (li, w) in enumerate(words):
        a = spans[min(int(i * m / n), m - 1)][0]
        b = spans[min(int((i + 1) * m / n) - 1, m - 1)][1] if i + 1 < n else t1
        out.setdefault(li, []).append((a, max(b, a + 0.12), w))
    return [{"start": ws[0][0], "end": ws[-1][1], "words": ws} for _, ws in sorted(out.items())]


def plan_shots(sents, n_images, total):
    """Give each image a contiguous run of sentences; cut points on sentence starts."""
    n = min(n_images, len(sents))
    bounds = [0.0]
    for k in range(1, n):
        bounds.append(sents[round(k * len(sents) / n)]["start"])
    bounds.append(total)
    return [(bounds[i], bounds[i + 1]) for i in range(n)]


def ass_time(t):
    t = max(t, 0)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def esc(s):
    return s.replace("{", "(").replace("}", ")").replace("\\", "/")


def build_ass(path, sents, title, total):
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,{FONT},78,{GOLD},{WHITE},&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,2,8,70,70,230,-1
Style: Cap,{FONT},96,{WHITE},{WHITE},&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,60,60,640,-1
Style: Sig,{FONT},44,{GOLD},{WHITE},&H00000000,&H00000000,1,0,0,0,100,100,2,0,1,3,0,2,0,0,330,-1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    if title:
        ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(min(3.0, total))},Title,,0,0,0,,{{\\fad(0,250)}}{esc(title)}")
    ev.append(f"Dialogue: 0,{ass_time(0)},{ass_time(total)},Sig,,0,0,0,,Tokyo 503")
    for s in sents:
        ws = s["words"]
        chunks = [ws[i:i + 3] for i in range(0, len(ws), 3)]
        for ci, ch in enumerate(chunks):
            nxt = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else ch[-1][1] + 0.25
            for wi, (st, en, _) in enumerate(ch):
                end = ch[wi + 1][0] if wi + 1 < len(ch) else nxt
                txt = " ".join((f"{{\\c{GOLD}}}{esc(w)}{{\\c{WHITE}}}" if j == wi else esc(w))
                               for j, (_, _, w) in enumerate(ch))
                pop = "{\\fscx108\\fscy108\\t(0,90,\\fscx100\\fscy100)}" if wi == 0 else ""
                ev.append(f"Dialogue: 2,{ass_time(st)},{ass_time(end)},Cap,,0,0,0,,{pop}{txt}")
    open(path, "w", encoding="utf-8").write(hdr + "\n".join(ev) + "\n")


def render_shot(img, dur, out, zoom, punch_at, fit):
    n = max(1, round(dur * FPS))
    z = f"1+{zoom}*on/{n}"
    if punch_at is not None:  # +10 % punch over 4 frames at the payoff word
        p = round(punch_at * FPS)
        z = f"{z}+if(gte(on,{p}),min((on-{p})/4,1)*0.10,0)"
    zp = f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}"
    grade = "eq=contrast=1.08:saturation=1.08,vignette=PI/6"
    if fit == "blur":  # image centred on a blurred copy of itself (no cropping of the art)
        fc = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"gblur=sigma=40,eq=brightness=-0.12[bg];[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,{zp},{grade}[v]")
    else:
        fc = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,{zp},{grade}[v]"
    run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", img, "-filter_complex", fc, "-map", "[v]",
         "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--music")
    ap.add_argument("--script", help="correct script text (or path to .txt); fixes Whisper's spelling")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fit", choices=["blur", "fill"], default="fill")
    ap.add_argument("--model", default="small")
    a = ap.parse_args()

    imgs = sorted(f for f in glob.glob(os.path.join(a.images, "*"))
                  if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
    if not imgs:
        sys.exit("no images found")
    sents = transcribe(a.voice, a.model)
    if a.script:
        txt = open(a.script, encoding="utf-8").read() if os.path.isfile(a.script) else a.script
        sents = apply_script(sents, txt)
    total = round(sents[-1]["end"] + 0.35, 3)  # stop 0.35 s after the last word
    shots = plan_shots(sents, len(imgs), total)
    payoff_word = sents[-1]["words"][-1][0]
    print(f"{len(sents)} sentences, {len(shots)} shots, {total:.2f}s")

    tmp = tempfile.mkdtemp(prefix="short_")
    with open(f"{tmp}/list.txt", "w") as lst:
        for i, (s, e) in enumerate(shots):
            last = i == len(shots) - 1
            render_shot(imgs[i], e - s, f"{tmp}/{i:02d}.mp4", 0.06, (payoff_word - s) if last else None, a.fit)
            lst.write(f"file '{i:02d}.mp4'\n")
    run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
         "-c", "copy", f"{tmp}/video.mp4"])
    build_ass(f"{tmp}/subs.ass", sents, a.title, total)

    voice = "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"
    if a.music:
        afc = (f"[1:a]atrim=0:{total},asetpts=N/SR/TB,{voice},asplit[v1][v2];"
               f"[2:a]atrim=0:{total + 1},asetpts=N/SR/TB,volume=-16dB,afade=t=out:st={total - 0.6}:d=0.6[m];"
               f"[m][v2]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];"
               f"[v1][md]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=7[a]")
        ins = ["-i", a.voice, "-stream_loop", "-1", "-i", a.music]
    else:
        afc = f"[1:a]atrim=0:{total},asetpts=N/SR/TB,{voice},loudnorm=I=-14:TP=-1.5:LRA=7[a]"
        ins = ["-i", a.voice]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{tmp}/video.mp4", *ins, "-filter_complex",
         # shaping=complex -> HarfBuzz, required for correct Arabic letter forms
         f"[0:v]ass={tmp}/subs.ass:shaping=complex[v];{afc}", "-map", "[v]", "-map", "[a]", "-t", str(total),
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", a.out])
    print("->", a.out)


if __name__ == "__main__":
    main()
