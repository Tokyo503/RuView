#!/usr/bin/env python3
"""QA: re-transcribe a finished short and compare it to the script (herk playbook: 'every word whole').
Usage: qa_transcript.py done/<slug>.mp4 raw/<slug>/script.txt   -> word match %, missing/extra words.
Dialect TTS + Whisper always differ a little; < 70 % means a clipped/garbled line worth listening to."""
import sys, subprocess, re, difflib
import numpy as np
from faster_whisper import WhisperModel
vid, script = sys.argv[1], sys.argv[2]
norm = lambda t: re.sub(r"[ًٌٍَُِّْـ،.؟?!…:]", "", t).replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي").split()
pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", vid, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(a, language="ar", vad_filter=True)
heard = norm(" ".join(s.text for s in segs)); want = norm(open(script, encoding="utf-8").read())
sm = difflib.SequenceMatcher(None, want, heard)
print(f"match {sm.ratio()*100:.0f}%  ({len(want)} script words, {len(heard)} heard)")
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op != "equal":
        print(f"  {op:7} script: {' '.join(want[i1:i2]) or '-':30} heard: {' '.join(heard[j1:j2]) or '-'}")
