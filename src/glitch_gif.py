from PIL import Image, ImageSequence
from io import BytesIO
import numpy as np
from src.main import blend_images

def glitch_gif(
    input_path,
    temporal_window=2,
    mode='Manual',
    ratios=None,
    block_size=1
):

    pil_gif = Image.open(input_path)
    frames = [frame.convert("RGB") for frame in ImageSequence.Iterator(pil_gif)]

    frames_np = [np.array(f)[:, :, ::-1] for f in frames]
    total_frames = len(frames_np)

    '''
    num_sources = 2 * temporal_window + 1

    if mode == 'Manual':
      ratios = ratios
    elif mode == 'Random':
      ratios = np.random.rand(num_sources)
    elif mode == 'Centered':
      ratios = np.zeros(num_sources)
      for i in range (1, temporal_window + 1):
        ratios[i - 1] = i
        ratios[num_sources - i] = i
      ratios[temporal_window] = temporal_window + 1
    '''
    
    output_frames = []

    for i in range(total_frames):
        idxs = [min(max(j, 0), total_frames - 1) for j in range(i - temporal_window, i + temporal_window + 1)]
        selected_frames = [frames_np[j] for j in idxs]

        glitched = blend_images(
            images=selected_frames,
            ratios=ratios,
            block_size=block_size
        )
        output_frames.append(Image.fromarray(glitched[:, :, ::-1]))

    output_bytes = BytesIO()
    output_frames[0].save(
            output_bytes,
            format='GIF',
            save_all=True,
            append_images=output_frames[1:] if len(output_frames) > 1 else [],
            duration=pil_gif.info.get("duration", 100),
            loop=0,
            optimize=False
        )
    return output_bytes