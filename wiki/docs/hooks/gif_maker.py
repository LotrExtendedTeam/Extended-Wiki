import logging
import os
import re
import yaml
import imageio.v2 as imageio
from PIL import Image
from mkdocs.plugins import event_priority

GIF_BLOCK_RE = re.compile(r"```gif\s*(.*?)```", re.DOTALL)

log = logging.getLogger("mkdocs.plugins")

def on_pre_build(config):
    log.info(">>> Gif Maker Processor: Present")

@event_priority(100)
def on_page_markdown(markdown, page, config, files):
    base_frame_dir = "wiki/docs/wiki/img/"  # Base path for frames

    def process_block(match):
        block_content = match.group(1).strip()
        gif_data = yaml.safe_load(block_content)

        frames = gif_data.get("frames", [])
        output_path = gif_data.get("output")
        duration = float(gif_data.get("duration", 0.5)) * 1000

        if not frames or not output_path:
            return f"**GIF generation error:** Missing `frames` or `output`"

        # Prepend base path to frame filenames
        frame_paths = [
            os.path.join(base_frame_dir, f) if not os.path.isabs(f) else f
            for f in frames
        ]
        
        # Ensure output is inside docs/ so it’s copied
        output_abs = os.path.join("wiki/docs/wiki/img/generated/", output_path)
        os.makedirs(os.path.dirname(output_abs), exist_ok=True)

        # Skip if up-to-date
        if os.path.exists(output_abs):
            output_mtime = os.path.getmtime(output_abs)
            if all(os.path.getmtime(frame) <= output_mtime for frame in frame_paths):
                #print(f"[GIF] Skipping, up-to-date: {output_path}")
                return f"generated/{output_path}"

        print(f"[GIF] Generating: {output_path}")
        try:
            # Streaming write (performance gain)
            with imageio.get_writer(output_abs, mode="I", duration=duration, loop=0, disposal=2) as writer:
                for f in frame_paths:
                    try:
                        # Lazy load per frame
                        img = Image.open(f)
                        # Fast path: only convert if needed
                        if img.mode != "RGBA":
                            img = img.convert("RGBA")
                        writer.append_data(img)
                    except Exception as e:
                        log.warning(f"[GIF] Failed reading frame {f}: {e}")
        except Exception as e:
            return f"**GIF generation error:** {e}"
        return f"generated/{output_path}"

    if "```gif" not in markdown:
        return markdown
    return GIF_BLOCK_RE.sub(process_block, markdown)