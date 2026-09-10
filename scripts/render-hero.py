"""Encode a seamless 15s camera-motion film from three campaign stills."""
import pathlib,subprocess,json,concurrent.futures
R=pathlib.Path(__file__).resolve().parents[1];A=R/'theme/assets';OUT=R/'deliverables';OUT.mkdir(exist_ok=True)
def render(mobile=False):
 width,height=(720,1280) if mobile else (1600,900);filters=[]
 for i in range(3):
  # Oversample to keep subpixel camera movement smooth. Mobile crops toward the model.
  base="scale=-2:2400,crop=1350:2400:(iw-ow)*0.85:0" if mobile else "scale=3600:2026:force_original_aspect_ratio=increase,crop=3600:2026:(iw-ow)/2:(ih-oh)/2"
  zoom=("1.025-0.02*on/143" if i==1 else "1.005+0.02*on/143") if mobile else ("1.06-0.035*on/143" if i==1 else "1.015+0.035*on/143")
  vertical=0.1 if mobile else 0.45
  filters.append(f"[{i}:v]{base},zoompan=z='{zoom}':x='(iw-iw/zoom)*0.65':y='(ih-ih/zoom)*{vertical}':d=144:s={width}x{height}:fps=24,format=yuv420p,setsar=1,settb=AVTB[v{i}]")
 filters+=['[v0]split=2[a][d]','[a][v1]xfade=transition=fade:duration=1:offset=5[ab]','[ab][v2]xfade=transition=fade:duration=1:offset=10[abc]','[abc][d]xfade=transition=fade:duration=1:offset=15[loop]','[loop]trim=start=1:end=16,setpts=PTS-STARTPTS[out]']
 filename='essaint-hero-mobile.mp4' if mobile else 'essaint-hero-desktop.mp4'
 command=['ffmpeg','-y','-hide_banner','-loglevel','error']
 for i in range(1,4):command+=['-i',str(A/f'campaign-0{i}.png')]
 command+=['-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[out]','-an','-c:v','libx264','-preset','medium','-crf','24','-maxrate','2200k' if not mobile else '1300k','-bufsize','4400k' if not mobile else '2600k','-pix_fmt','yuv420p','-movflags','+faststart','-threads','3',str(A/filename)]
 subprocess.run(command,check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(A/filename)],text=True));video=probe['streams'][0]
 assert (video['width'],video['height'])==(width,height);assert abs(float(probe['format']['duration'])-15)<0.1;assert len(probe['streams'])==1;assert (A/filename).stat().st_size<10_000_000
 return {'file':filename,'width':width,'height':height,'duration':probe['format']['duration'],'bytes':(A/filename).stat().st_size,'audio':False}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(render,[False,True]))
(OUT/'video-specification.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
