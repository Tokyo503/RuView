#!/usr/bin/env bash
# Reel 1 — built from style.md v2. Music: clip2 track, drop at 9.545 s (130 BPM).
set -euo pipefail
cd "$(dirname "$0")/.."
T=raw/_seg; mkdir -p "$T" done
GRADE="eq=contrast=1.15:saturation=1.1:gamma=0.95,colorbalance=bs=0.05:rh=0.05,vignette=PI/5"
# name|src|src_start|reel_start|reel_end|zoom_amount|extra
SEGS=(
"01|ref4|1.00|0.000|2.635|0.05|"
"02|ref4|4.00|2.635|4.475|0.06|"
"03|ref3|0.30|4.475|6.335|0.05|"
"04|clip3|0.20|6.335|8.175|0.05|"
"05|clip2|0.50|8.175|9.545|0.06|"
"06|ref1|6.00|9.545|10.485|0.12|fade=in:st=0:d=0.25:color=white"
"07|clip2|9.00|10.485|11.395|0.12|"
"08|ref2|6.00|11.395|12.315|0.12|"
"09|clip1|9.20|12.315|12.775|0.14|"
"10|clip2|21.20|12.775|13.235|0.14|"
"11|ref1|9.50|13.235|13.715|0.14|"
"12|clip2|22.00|13.715|14.175|0.14|"
"13|ref4|11.50|14.175|14.625|0.15|"
"14|ref1|12.66|14.625|16.935|0.06|"
)
: > "$T/list.txt"
for s in "${SEGS[@]}"; do
  IFS='|' read -r n src ss a b z extra <<<"$s"
  d=$(python3 -c "print(round($b-$a,3))"); N=$(python3 -c "print(round(($b-$a)*30))")
  vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,"
  vf+="zoompan=z='1+$z*on/$N':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,$GRADE"
  [ -n "$extra" ] && vf+=",$extra"
  ffmpeg -loglevel error -y -ss "$ss" -i "raw/$src.mp4" -t "$d" -an -vf "$vf" -frames:v "$N" \
    -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p "$T/$n.mp4"
  echo "file '$n.mp4'" >> "$T/list.txt"
done
ffmpeg -loglevel error -y -f concat -safe 0 -i "$T/list.txt" -c copy "$T/video.mp4"
DUR=16.935
# Music + riser (filtered noise swelling into the drop at 9.545)
ffmpeg -loglevel error -y -i raw/clip2.mp4 \
  -f lavfi -t 1.6 -i "anoisesrc=color=pink:amplitude=0.5:sample_rate=44100" \
  -filter_complex "[0:a]atrim=0:$DUR,asetpts=N/SR/TB,afade=t=out:st=$(python3 -c "print($DUR-0.3)"):d=0.3[m];\
[1:a]highpass=f=1500,lowpass=f=9000,afade=t=in:d=1.5,volume=0.25,aformat=channel_layouts=stereo,adelay=7945|7945[r];\
[m][r]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map "[a]" -c:a aac -b:a 192k "$T/audio.m4a"
ffmpeg -loglevel error -y -i "$T/video.mp4" -i "$T/audio.m4a" -map 0:v -map 1:a -c:v copy -c:a copy -shortest -movflags +faststart done/reel1.mp4
echo "done/reel1.mp4"
