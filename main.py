from utils import read_video, save_video
from trackers import Tracker
import cv2
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
import numpy as np
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedDistance_Estimator

def main():
    #read video
    video_frames = read_video('input_vids/08fd33_4.mp4')

    # initalize tracker
    tracker = Tracker('models/best.pt')
    tracks = tracker.get_obj_tracks(video_frames,
                                    read_from_stub=True,
                                    stub_path='stubs/track_stub.pkl')
    
    # get object positions
    tracker.add_position_to_track(tracks)
    
    # estimate camera movement
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                              read_from_stub=True,
                                                                              stub_path='stubs/camera_movement_stub.pkl')
    camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)

    # View Transformer
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)


    # inetpolate ball positions
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

    # add speed and distance to tracks
    speed_distance_estimator = SpeedDistance_Estimator()
    speed_distance_estimator.add_speed_and_distance_to_tracks(tracks)
    
    # assign players to teams
    team_assigner = TeamAssigner()
    team_assigner.assign(video_frames[0],
                          tracks["players"][0])

    for frame_num, player_track in enumerate(tracks["players"]):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num],
                                                  track["bbox"],
                                                    player_id)
            tracks["players"][frame_num][player_id]["team"] = team
            tracks["players"][frame_num][player_id]["team_color"] = team_assigner.team_colors[team]

    # assign ball to player
    player_ball_assigner = PlayerBallAssigner()
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks["players"]):
        ball_bbox = tracks["ball"][frame_num][1]["bbox"]
        assigned_player = player_ball_assigner.assign_ball_to_player(player_track,
                                                                      ball_bbox)

        if assigned_player != -1:
            tracks["players"][frame_num][assigned_player]["has_ball"] = True        
            team_ball_control.append(tracks["players"][frame_num][assigned_player]["team"])
        else:
            team_ball_control.append(team_ball_control[-1])    

    team_ball_control = np.array(team_ball_control)

    #draw output
    ## draw object tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)
    
    ## draw camera movement
    # output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
    
    ## draw speed and distance
    speed_distance_estimator.draw_speed_distance(output_video_frames, tracks)

    #save video
    save_video(output_video_frames, 'output_vids/output_video.avi')


if __name__ == '__main__':
    main()