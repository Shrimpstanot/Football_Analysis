# Football Match Analysis System

## Overview
This project is a multi-module program designed to analyze football matches by tracking all players, referees, and the ball. The system overlays each player with an ID, speed, and distance covered, while also tracking the ball with a directional arrow. This project leverages advanced computer vision techniques, including object detection, image clustering, and perspective transformation.

## Features
- **Player & Referee Tracking**: Identifies and tracks all players and referees on the field.
- **Overlay Information**: Displays player ID, speed, and distance covered in real-time.
- **Ball Tracking**: Tracks the ball's movement with a directional arrow.
- **Camera Movement Estimation**: Estimates camera movement to accurately calculate player speed and distance.
- **View and Perspective Transformation**: Adjusts the view to calculate speed and distance in the correct perspective.
- **Interpolation**: Fills in missing bounding boxes to maintain continuous tracking.

![Screenshot](output_videos/screenshot.png)

## Technologies Used
The following modules are used in this project:
- YOLO: AI object detection model
- Kmeans: Pixel segmentation and clustering to detect t-shirt color
- Optical Flow: Measure camera movement
- Perspective Transformation: Represent scene depth and perspective
- Speed and distance calculation per player

## How It Works
1. **Object Detection**: The system uses a custom-trained YOLO model to detect all players, referees, and the ball on the field.
2. **Tracking**: Once detected, objects are tracked frame by frame, with the system calculating speed and distance covered for each player.
3. **Ball Tracking**: The ball is tracked separately, with an arrow indicating its movement.
4. **Data Overlay**: Real-time overlay information, including player IDs, speed, and distance, is displayed on the video.
5. **Camera Movement Estimation**: The system calculates the camera movement to ensure accurate measurements of player statistics.
6. **Perspective Transformation**: The video is transformed to maintain consistent perspective, ensuring accurate distance and speed calculations.

## Installation
1. Clone the repository from GitHub.

2. Install the required dependencies by using the `requirements.txt` file.

## Usage
Run the main script to start analyzing a football match. The output video with overlays will be saved in the `output/` directory.

## Trained Models
- [Trained Yolo v5](https://drive.google.com/file/d/1DC2kCygbBWUKheQ_9cFziCsYVSRw6axK/view?usp=sharing)

## Sample video
-  [Sample input video](https://drive.google.com/file/d/1t6agoqggZKx6thamUuPAIdN_1zR9v9S_/view?usp=sharing)
  
## Future Improvements
- **Enhanced Ball Tracking**: Further refine the logic for more accurate ball tracking.
- **Real-time Analysis**: Develop capabilities for real-time match analysis.
- **Advanced Statistics**: Include more advanced statistics such as player acceleration, team formations, and heat maps.

## Credit
Special thanks to Abdullah Tarek for his amazing tutorial! [His Youtube Channel](https://www.youtube.com/@codeinajiffy)


## License
This project is licensed under the MIT License.
