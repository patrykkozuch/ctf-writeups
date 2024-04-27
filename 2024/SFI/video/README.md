# Video

## Table of contents

- [Task](#task)
- [Solution](#solution)
  - [About monitor settings](#about-monitor-settings)
  - [Pro tip - extract all the frames!](#pro-tip---extract-all-frames)
- [Lessons learned](#lessons-learned)


## Task

> Secrets lie concealed in an unclear way in this cryptic video. Do you have what it takes to uncover them?

Attachements: 
- [video](video.mp4)


## Solution

We are given a video with dots blinking around. Nothing really special to watch. 

Things change if we download it and open it locally - then, for a moment (in frame 300) we see the flag in one of the frames.
Quick extraction using any video editing software and we are done.

![frame-0300.png](assets/frame-0300.png)

Flag: **_sfi19_ctf{n73c2n72x}_**

### About monitor settings
Please notice that your monitor settings can play a crucial role here - having settings other than sRGB profile made it much
harder to find the flag.

### Pro Tip - extract all frames!
If you have VLC or another package which uses ffmpeg coded installed, you can easily extract all frames by using:

```
ffmepg -i input.mp4 -c:v png output_frame%04d.png
```



## Lessons learned:
- Have the best contrast possible for tasks like this
- Extract all frames and look at the one by one
- Never trust web preview