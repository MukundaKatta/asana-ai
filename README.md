# Asana-AI: AI Yoga Pose Corrector

An intelligent yoga pose analysis and correction system powered by deep learning.
Asana-AI uses a convolutional neural network to detect 17 body keypoints, compares
your pose against a library of 30+ authentic yoga asanas, and generates specific
alignment corrections to deepen your practice safely.

## Features

- **Pose Detection**: CNN-based detector extracting 17 anatomical keypoints from images
- **Asana Library**: 30+ traditional yoga poses with Sanskrit names, correct joint angles, and health benefits
- **Pose Analysis**: Joint angle computation and comparison against reference asanas
- **Alignment Correction**: Specific, actionable feedback to improve form
- **Sequence Builder**: Pre-built sequences (Sun Salutation, Warrior Series, Standing Series)
- **Pranayama Guide**: Breathing patterns synchronized with each pose
- **Practice Reports**: Session summaries with accuracy scores and improvement tracking

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Analyze a yoga pose from an image
asana-ai analyze --image pose.jpg

# Start a guided sequence
asana-ai sequence --name sun-salutation

# Simulate a practice session
asana-ai simulate --asana Virabhadrasana_I --duration 30

# Generate a practice report
asana-ai report --session latest
```

## Architecture

```
src/asana/
  cli.py              # Click CLI interface
  models.py            # Pydantic data models
  simulator.py         # Practice session simulator
  report.py            # Session report generator
  pose/
    detector.py        # YogaPoseDetector CNN (17 keypoints)
    analyzer.py        # AsanaAnalyzer (joint angle comparison)
    corrector.py       # AsanaCorrector (alignment corrections)
  library/
    asanas.py          # AsanaLibrary (30+ yoga poses)
    sequences.py       # SequenceBuilder (Sun Salutation, etc.)
    breathing.py       # PranayamaGuide (breathing patterns)
```

## Requirements

- Python 3.10+
- PyTorch
- NumPy
- Pydantic
- Click
- Rich

## Author

Mukunda Katta

## License

MIT
