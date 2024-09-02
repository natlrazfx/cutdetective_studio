# cutdetective_studio
Is a Python script for Nuke Studio that automates the process of scene detection and cutting video sequences into individual shots. This script leverages the PySceneDetect library, which provides powerful tools for detecting scene changes in video files based on content, brightness, and adaptive detection methods.

## How to Use

CutDetective relies on the PySceneDetect library for scene detection. You need to install it using pip:
**pip install --upgrade scenedetect[opencv]**

Select a Sequence.

Execute the Cut Detective Studio script. 

A settings dialog will appear, allowing you to adjust various parameters (optional):
Content Detector Threshold: Adjusts sensitivity to content changes in the video.
Threshold Detector Value: Controls sensitivity to brightness changes.
Minimum Scene Length: Sets the minimum length of detected scenes in frames.
Adaptive Detector Threshold: Fine-tunes detection based on gradual changes.
Downscale Factor: Reduces video resolution for faster processing.
Frame Skip: Determines how many frames to skip between each analysis.

Click "OK" to start the scene detection process. The script will analyze the video, detect scene changes, and automatically cut the sequence into individual shots based on the detected scenes.
Completion:

Once the process is complete, a message will appear informing you of the number of shots created. You can review the cuts in your sequence to ensure they meet your requirements.

**it's recommended to familiarize yourself with the PySceneDetect library. This library provides detailed documentation on how scene detection works and the various parameters available for configuration. Understanding this will help you get the most out of the Cut Detective Studio script and optimize it for your specific workflow.
You can find more information and documentation for PySceneDetect here [PySceneDetect Documentation](https://www.scenedetect.com/download/)**

[![Watch the video](https://img.youtube.com/vi/7zUSFjBkF64/maxresdefault.jpg)](https://youtu.be/7zUSFjBkF64)

## Support and Feedback

If this script saved you some time or you just love what it does, please feel free to share your thoughts and consider supporting my work as I continue my journey

### 💖 GitHub Sponsors
[Become a Sponsor](https://github.com/sponsors/natlrazfx)
### ☕ Buy Me a Coffee
[Buy Me a Coffee](https://www.buymeacoffee.com/natlrazfx)
### 💸 PayPal
[PayPal Me](https://paypal.me/natlrazfx)
### 👾 ByBit
119114169


## Cheers :) 
