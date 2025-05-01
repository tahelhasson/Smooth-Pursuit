# # import json
# # import random
# # import numpy as np
# # import subprocess
# # from experiement_base import base
# # import configargparse
# # import pathlib
# # import pylink
# # import os
# # import cv2
# # from math import pi, sin
# # from psychopy import visual, core, event, monitors, gui
# # import time
# # import tempfile
# # from itertools import product
# # import pyautogui
# # import platform
# #
#
#
# import os
# import configargparse
# import pylink
# from psychopy import visual, core, event, monitors
# from experiement_base import base
#
# def parse_args():
#     parser = configargparse.ArgParser(default_config_files=['./configs/polygons_config.txt'])
#
#     parser.add_argument('--results_dir', type=str, default='./edf_outputs')
#     parser.add_argument('--videos_path', type=str, default='./videos')
#     parser.add_argument('--default_name', type=str, default='videoexp')
#     parser.add_argument('--batch', type=int, default=1, help="Video batch number")
#     parser.add_argument('--session', type=int, default=1, help="Session number within the batch")
#     parser.add_argument('--dummy_mode', action='store_true', help='Run in dummy mode (no EyeLink connection)')
#     parser.add_argument('--window_width', type=int, default=1920)
#     parser.add_argument('--window_height', type=int, default=1080)
#     parser.add_argument('--fullscreen', action='store_true')
#     parser.add_argument('--calibration_target', type=str, default='circle')
#     parser.add_argument('--calibration_target_size', type=int, default=24)
#
#     return parser.parse_known_args()
#
# def get_session_videos(args):
#     batch_folder = os.path.join(args.videos_path, f"batch{args.batch}")
#     video_list = sorted([f for f in os.listdir(batch_folder) if f.endswith('.mp4')])
#     return [os.path.join(batch_folder, vid) for vid in video_list]
#
# def run_video_trial(tracker, win, video_path, trial_id, args):
#     tracker.sendMessage(f'TRIALID {trial_id}')
#     tracker.sendMessage('start_trial')
#     tracker.sendMessage(f'VIDEO_FILE {os.path.basename(video_path)}')
#
#     movie = visual.MovieStim3(win, video_path, size=win.size, flipVert=False)
#     tracker.sendMessage('start_phase stimulus')
#
#     while movie.status != visual.FINISHED:
#         movie.draw()
#         win.flip()
#         base.check_for_escape(args)
#
#     tracker.sendMessage('end_phase stimulus')
#     tracker.sendMessage('end_trial')
#     tracker.sendMessage(f'TRIAL_RESULT {pylink.TRIAL_OK}')
#
# def run_experiment(args):
#     win, genv = args.win, args.genv
#     el_tracker = pylink.getEYELINK()
#     el_tracker.setOfflineMode()
#     base.set_calibration_settings(args)
#     pylink.openGraphicsEx(args.genv)
#     base.show_msg(args, "Welcome to the video experiment :)", wait_for_keypress=True)
#
#     if not args.dummy_mode:
#         try:
#             el_tracker.doTrackerSetup()
#         except RuntimeError as err:
#             print('ERROR:', err)
#             el_tracker.exitCalibration()
#
#     session_videos = get_session_videos(args)
#
#     try:
#         el_tracker.startRecording(1, 1, 1, 1)
#     except RuntimeError as error:
#         print("ERROR:", error)
#         base.abort_trial(args)
#         return pylink.TRIAL_ERROR
#
#     core.wait(0.1)
#
#     for i, video_path in enumerate(session_videos):
#         base.check_for_escape(args)
#         trial_id = args.trial_id + i + 1
#         run_video_trial(el_tracker, win, video_path, trial_id, args)
#
#     core.wait(0.25)
#     el_tracker.stopRecording()
#     el_tracker.sendMessage('EXPERIMENT_COMPLETE')
#
#     thanks = visual.TextStim(win, text="Thank you!")
#     thanks.draw()
#     win.flip()
#     core.wait(3)
#     base.terminate_experiment(args)
#
# if __name__ == '__main__':
#     base.config_general_parser()
#     args, _ = parse_args()
#     args.experiment_name = 'videoexp'
#     base.get_edf_filename(args, default=args.default_name)
#     base.get_session_identifier(args)
#     base.connect(args)
#     base.open_edf_file(args)
#     base.record_all_variables(args)
#     args.el_tracker.setOfflineMode()
#     args.el_tracker.sendCommand("calibration_type = HV13")
#     base.setup_screen(args)
#     args.trial_id = 0
#     run_experiment(args)

import os
import configargparse
import pylink
from psychopy import visual, core, event, monitors
from experiement_base import base
from eyelinkparser._eyelinkparser import EyeLinkParser

def parse_asc(path):
    parser = EyeLinkParser(folder=None)
    return parser.parse_file(path)
import pandas as pd
import numpy as np


VELOCITY_THRESHOLD = 30  # deg/s, rough upper limit for smooth pursuit
MIN_DURATION_MS = 100    # minimum duration for pursuit segment


def parse_args():
    parser = configargparse.ArgParser(default_config_files=['./configs/polygons_config.txt'])

    parser.add_argument('--results_dir', type=str, default='./edf_outputs')
    parser.add_argument('--videos_path', type=str, default='./videos')
    parser.add_argument('--default_name', type=str, default='videoexp')
    parser.add_argument('--batch', type=int, default=1, help="Video batch number")
    parser.add_argument('--session', type=int, default=1, help="Session number within the batch")
    parser.add_argument('--dummy_mode', action='store_true', help='Run in dummy mode (no EyeLink connection)')
    parser.add_argument('--window_width', type=int, default=1920)
    parser.add_argument('--window_height', type=int, default=1080)
    parser.add_argument('--fullscreen', action='store_true')
    parser.add_argument('--calibration_target', type=str, default='circle')
    parser.add_argument('--calibration_target_size', type=int, default=24)

    return parser.parse_known_args()

def get_session_videos(args):
    batch_folder = os.path.join(args.videos_path, f"batch{args.batch}")
    video_list = sorted([f for f in os.listdir(batch_folder) if f.endswith('.mp4')])
    return [os.path.join(batch_folder, vid) for vid in video_list]

def run_video_trial(tracker, win, video_path, trial_id, args):
    tracker.sendMessage(f'TRIALID {trial_id}')
    tracker.sendMessage('start_trial')
    tracker.sendMessage(f'VIDEO_FILE {os.path.basename(video_path)}')

    movie = visual.MovieStim3(win, video_path, size=win.size, flipVert=False)
    tracker.sendMessage('start_phase stimulus')

    while movie.status != visual.FINISHED:
        movie.draw()
        win.flip()
        base.check_for_escape(args)

    tracker.sendMessage('end_phase stimulus')
    tracker.sendMessage('end_trial')
    tracker.sendMessage(f'TRIAL_RESULT {pylink.TRIAL_OK}')

def detect_pursuit_segments(t, x, y, threshold=VELOCITY_THRESHOLD, min_duration=MIN_DURATION_MS):
    t = np.array(t)
    x = np.array(x)
    y = np.array(y)
    if len(t) < 2:
        return []

    dt = np.diff(t)
    dx = np.diff(x)
    dy = np.diff(y)

    velocity = np.sqrt(dx**2 + dy**2) / (dt / 1000.0)  # px/s

    segments = []
    in_segment = False
    start_idx = 0

    for i, v in enumerate(velocity):
        if v < threshold:
            if not in_segment:
                in_segment = True
                start_idx = i
        else:
            if in_segment:
                end_idx = i
                duration = t[end_idx] - t[start_idx]
                if duration >= min_duration:
                    segments.append((t[start_idx], t[end_idx], duration))
                in_segment = False

    if in_segment:
        end_idx = len(t) - 1
        duration = t[end_idx] - t[start_idx]
        if duration >= min_duration:
            segments.append((t[start_idx], t[end_idx], duration))

    return segments

def run_experiment(args):
    win, genv = args.win, args.genv
    el_tracker = pylink.getEYELINK()
    el_tracker.setOfflineMode()
    base.set_calibration_settings(args)
    pylink.openGraphicsEx(args.genv)
    base.show_msg(args, "Welcome to the video experiment :)", wait_for_keypress=True)

    if not args.dummy_mode:
        try:
            el_tracker.doTrackerSetup()
        except RuntimeError as err:
            print('ERROR:', err)
            el_tracker.exitCalibration()

    session_videos = get_session_videos(args)

    try:
        el_tracker.startRecording(1, 1, 1, 1)
    except RuntimeError as error:
        print("ERROR:", error)
        base.abort_trial(args)
        return pylink.TRIAL_ERROR

    core.wait(0.1)

    for i, video_path in enumerate(session_videos):
        base.check_for_escape(args)
        trial_id = args.trial_id + i + 1
        run_video_trial(el_tracker, win, video_path, trial_id, args)
        break

    core.wait(0.25)
    el_tracker.stopRecording()
    el_tracker.sendMessage('EXPERIMENT_COMPLETE')

    thanks = visual.TextStim(win, text="Thank you!")
    thanks.draw()
    win.flip()
    core.wait(3)
    base.terminate_experiment(args)

    # ---- Step 2 & 3: Convert, Parse, Analyze ----
    asc_path = os.path.join(args.session_folder, args.edf_filename + '.asc')
    if os.path.exists(asc_path):
        dm = parse_asc(asc_path)

        summary = []
        pursuits = []
        for trial in dm.unique('TRIAL_INDEX'):
            trial_dm = dm.select(f'TRIAL_INDEX == {trial}')
            fix = trial_dm.select('EYEEVENT == "EFIX"')
            sacc = trial_dm.select('EYEEVENT == "ESACC"')
            raw = trial_dm.select('EYEEVENT == ""')

            summary.append({
                'trial': trial,
                'n_fixations': len(fix),
                'n_saccades': len(sacc),
                'n_samples': len(raw)
            })

            t = raw.TIME.tolist()
            x = raw.XPOS.tolist()
            y = raw.YPOS.tolist()
            segments = detect_pursuit_segments(t, x, y)

            for onset, offset, duration in segments:
                pursuits.append({
                    'trial': trial,
                    'start_time': onset,
                    'end_time': offset,
                    'duration_ms': duration
                })

        pd.DataFrame(summary).to_csv(os.path.join(args.results_dir, args.edf_filename + '_trial_summary.csv'), index=False)
        pd.DataFrame(pursuits).to_csv(os.path.join(args.session_folder, args.edf_filename + '_pursuits.csv'), index=False)
        print("Saved fixation/saccade summary and smooth pursuit segments.")
    else:
        print("ASC file not found. Skipping analysis.")

if __name__ == '__main__':
    base.config_general_parser()
    args, _ = parse_args()
    args.experiment_name = 'videoexp'
    base.get_edf_filename(args, default=args.default_name)
    base.get_session_identifier(args)
    base.connect(args)
    args.edf_path = os.path.join(args.session_folder, args.edf_filename + '.EDF')
    base.open_edf_file(args)
    base.record_all_variables(args)
    args.el_tracker.setOfflineMode()
    args.el_tracker.sendCommand("calibration_type = HV13")
    base.setup_screen(args)
    args.trial_id = 0
    run_experiment(args)
