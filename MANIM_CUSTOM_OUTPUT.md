# Manim Custom Output Path Feature

## Overview
The Manim integration now supports specifying a custom output path for your video files, separate from the construction/support files.

## How to Use in Claude Desktop

### Basic Usage (Default Location)
```
Create a Manim animation of a Mobius transformation
```
This will save the video in the default location: `MathematicalResearch/manim_outputs/media/videos/...`

### Custom Output Path
```
Create a Manim animation of a hyperbolic rotation and save it to Media/Manim/HyperbolicRotation.mp4
```

### Organized by Date
```
Create a Manim animation of a complex function and save it to Media/Manim/2024-01/ComplexFunction.mp4
```

### Organized by Topic
```
Create a Manim animation of a 3D surface plot and save it to Media/Manim/Topology/3DSurface.mp4
```

## Output Structure

When you specify a custom output path:
- The **final MP4** is copied to your specified location (e.g., `Media/Manim/`)
- The **construction files** remain in the default Manim output directory
- The original video is preserved in case you need it

## Example Directory Structure
```
Dropbox/
├── Media/                          # Your clean media folder
│   └── Manim/                      # Just the final videos
│       ├── 2024-01/
│       │   ├── HyperbolicRotation.mp4
│       │   └── MobiusTransformation.mp4
│       ├── Topology/
│       │   └── 3DSurface.mp4
│       └── LinearAlgebra/
│           └── MatrixTransformation.mp4
│
└── MathematicalResearch/           # Working directory
    └── manim_outputs/              # Construction files
        ├── media/
        │   └── videos/
        └── *.py                    # Source files
```

## Benefits
1. **Clean Organization**: Keep final videos separate from construction files
2. **Easy Sharing**: All your videos in one place
3. **Topic-Based Folders**: Organize by subject matter
4. **Date-Based Archives**: Organize by creation date
5. **No Clutter**: Construction files stay in the working directory

## Natural Language Examples

You can use natural language in Claude Desktop:
- "Create a Manim video of eigenvalues and save it in Media/Manim/LinearAlgebra/"
- "Make an animation showing gyrovector addition, output to Media/Manim/Gyrovectors/Addition.mp4"
- "Generate a 3D plot of a complex function, save as Media/Manim/2024-01-11/ComplexPlot.mp4"

## Note
If the custom output path is not specified, videos will be saved in the default Manim output directory as before. This feature is completely optional and backward compatible.