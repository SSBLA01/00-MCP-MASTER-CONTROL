#!/usr/bin/env python
"""Create actual Manim demo video"""

import os
import subprocess
from pathlib import Path

# Create Manim script directly
manim_code = '''from manim import *

class MobiusTransformation(Scene):
    def construct(self):
        # Title
        title = Text("Möbius Transformation", font_size=48)
        subtitle = Text("in the Poincaré Disk", font_size=36)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Create unit disk
        disk = Circle(radius=3, color=BLUE, stroke_width=3)
        disk_label = MathTex(r"|z| < 1").next_to(disk, UP)
        
        self.play(Create(disk), Write(disk_label))
        self.wait()
        
        # Show Möbius formula
        formula = MathTex(
            r"f(z) = \\frac{az + b}{cz + d}",
            font_size=60
        ).to_edge(UP)
        
        condition = MathTex(r"ad - bc \\neq 0", font_size=40)
        condition.next_to(formula, DOWN)
        
        self.play(Write(formula))
        self.play(Write(condition))
        self.wait(2)
        
        # Create grid inside disk
        grid = NumberPlane(
            x_range=[-3, 3, 0.5],
            y_range=[-3, 3, 0.5],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        
        # Mask to show only inside disk
        mask = Circle(radius=3, color=BLACK, fill_opacity=1)
        mask.set_stroke(width=0)
        
        self.play(Create(grid))
        self.wait()
        
        # Apply Möbius transformation
        def mobius_transform(point):
            x, y, z = point
            z_complex = complex(x, y)
            
            # Simple Möbius: rotation and scaling
            # f(z) = (z + 0.5) / (0.5z + 1)
            if abs(0.5 * z_complex + 1) > 0.01:
                w = (z_complex + 0.5) / (0.5 * z_complex + 1)
                return np.array([w.real, w.imag, 0])
            else:
                return point
        
        # Animate transformation
        self.play(
            grid.animate.apply_function(mobius_transform),
            run_time=3
        )
        self.wait(2)
        
        # Final message
        final_text = Text(
            "Möbius transformations preserve the hyperbolic metric",
            font_size=24
        ).to_edge(DOWN)
        
        self.play(Write(final_text))
        self.wait(2)
'''

# Save the script
output_dir = Path("/Users/scottbroock/Dropbox/MathematicalResearch/manim_outputs")
output_dir.mkdir(parents=True, exist_ok=True)

script_path = output_dir / "mobius_demo.py"
with open(script_path, 'w') as f:
    f.write(manim_code)

print(f"Created Manim script: {script_path}")

# Try to render it with Manim
video_path = output_dir / "MobiusTransformation.mp4"

print("\nAttempting to render video...")
print("Note: This requires Manim to be properly installed with all dependencies")

# Check if manim is available
try:
    result = subprocess.run(['manim', '--version'], capture_output=True, text=True)
    print(f"Manim version: {result.stdout}")
    
    # Try to render
    cmd = [
        'manim', '-ql', '-o', 'MobiusTransformation.mp4',
        str(script_path), 'MobiusTransformation'
    ]
    
    print(f"\nRunning: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(output_dir))
    
    if result.returncode == 0:
        print(f"\n✅ Video successfully created!")
        print(f"Location: {video_path}")
        
        # Check if file exists
        if video_path.exists():
            size = video_path.stat().st_size / 1024 / 1024  # MB
            print(f"File size: {size:.2f} MB")
    else:
        print(f"\n❌ Manim rendering failed:")
        print(result.stderr)
        
except FileNotFoundError:
    print("\n❌ Manim is not installed or not in PATH")
    print("The script has been created but cannot be rendered without Manim")

print(f"\n📝 Script location: {script_path}")
print("You can manually render it with: manim -ql mobius_demo.py MobiusTransformation")