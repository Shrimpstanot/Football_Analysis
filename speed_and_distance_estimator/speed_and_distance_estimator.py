import sys
sys.path.append("../")
from utils import measure_distance, get_foot_position
import cv2

class SpeedDistance_Estimator:
    def __init__(self):
        self.frame_window = 5
        self.fps = 24

    def add_speed_and_distance_to_tracks(self, tracks):
        total_distance = {}
        
        for obj, obj_tracks in tracks.items():
            if obj == "ball" or obj == "referee":
                continue
            num_frames = len(obj_tracks)
            for frame_num in range(0, num_frames, self.frame_window):
                last_frame = min(frame_num + self.frame_window, num_frames - 1)

                for track_id, _ in obj_tracks[frame_num].items():
                    if track_id not in obj_tracks[last_frame]:
                        continue

                    start_pos = obj_tracks[frame_num][track_id]["position_transformed"]
                    end_pos = obj_tracks[last_frame][track_id]["position_transformed"]

                    if start_pos is None or end_pos is None:
                        continue

                    distance_covered = measure_distance(start_pos, end_pos)
                    time_taken = (last_frame - frame_num) / self.fps
                    speed = distance_covered / time_taken
                    speed_kmph = speed * 3.6

                    if obj not in total_distance:
                        total_distance[obj] = {}

                    if track_id not in total_distance[obj]:
                        total_distance[obj][track_id] = 0

                    total_distance[obj][track_id] += distance_covered

                    for frame_num_batch in range(frame_num, last_frame):
                        if track_id not in tracks[obj][frame_num_batch]:
                            continue
                        tracks[obj][frame_num_batch][track_id]["speed"] = speed_kmph
                        tracks[obj][frame_num_batch][track_id]["distance"] = total_distance[obj][track_id]

    def draw_speed_distance(self, video_frames, tracks):
        output_video_frames = video_frames.copy()
        for frame_num, frame in enumerate(video_frames):
            for obj, obj_tracks in tracks.items():
                if obj == "ball" or obj == "referee":
                    continue
                for _, track_info in obj_tracks[frame_num].items():
                    if "speed" in track_info:
                        speed = track_info.get("speed", None)
                        distance = track_info.get("distance", None)
                        if speed is not None and distance is not None:
                            continue

                        bbox = track_info["bbox"]
                        position = get_foot_position(bbox)
                        position = list(position)
                        position[1] += 40
                        position = tuple(position)
                        cv2.putText(video_frames, f"Speed: {speed:.2f} kmph", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                        cv2.putText(video_frames, f"Distance: {distance:.2f} m", (position[0], position[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            output_video_frames.append(video_frames)

        return output_video_frames