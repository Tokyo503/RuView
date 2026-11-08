---
name: "Beat Synced Reel"
description: "Cut a music-driven, no-voice reel (anime/AI-art edits) with every cut on the beat and the peak on the drop: tease → build → peak → payoff, one white flash, Ken Burns, riser into the drop, -14 LUFS. Use for montage/edit reels without narration."
---

# Beat Synced Reel

Template: `ai-editor/scripts/edit_reel1.sh` (a 14-shot segment table).

## Steps
1. Pick the music track. Beats: `npx hyperframes beats track.wav --json` (`beatTimes`, `bpm`).
2. Find the drop, i.e. the half-second where loudness jumps:
   ```bash
   ffmpeg -loglevel error -y -i track.mp4 -vn -ac 1 -ar 44100 t.wav && python3 -c "
   import wave,struct,math;w=wave.open('t.wav');n=w.getnframes();d=struct.unpack('<%dh'%n,w.readframes(n));s=22050
   print(' '.join('%.1f:%d'%(i/2,20*math.log10(math.sqrt(sum(x*x for x in d[i*s:(i+1)*s])/s)/32768+1e-9)) for i in range(n//s)))"
   ```
   Put the peak section start exactly on the beat nearest the jump.
3. Fill the `SEGS` table `name|src|src_start|reel_start|reel_end|zoom|extra`, with every boundary on a beat time:
   - tease 0–~2.6 s (1 slow shot, zoom 0.05), build 1.8 s shots (4 beats), peak 0.45–0.9 s shots (1–2 beats, zoom 0.12–0.15), payoff 2–3.5 s close-up, no fade (loops).
   - `fade=in:st=0:d=0.25:color=white` on the first peak shot only.
4. Source clips: skip each source's TikTok outro (find the scene cut before the end). The last shot must end before it.
5. Run the script, check the contact sheet and the last 2.5 s, confirm loudness about -14 LUFS.

## Ownership
Reels cut from other creators' videos (watermarked) are for practice only. Tell the user not to post them as their own.
