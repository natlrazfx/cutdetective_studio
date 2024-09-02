# Natalia Raz
# Based on https://github.com/Breakthrough/PySceneDetect

import os
import hiero.core
import hiero.ui
from PySide2 import QtWidgets, QtCore
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector, ThresholdDetector, AdaptiveDetector


class SceneDetectSettings(QtWidgets.QDialog):
    def __init__(self):
        super(SceneDetectSettings, self).__init__()

        self.setWindowTitle("Cut Detective Studio Settings")

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # ContentDetector settings
        self.content_threshold_label = QtWidgets.QLabel("Content Detector Threshold:")
        self.content_threshold = QtWidgets.QSpinBox()
        self.content_threshold.setRange(1, 100)
        self.content_threshold.setValue(60)
        self.content_threshold.setToolTip(
            "Threshold for content-based scene detection.\n"
            "Higher values result in fewer scenes being detected.\n"
            "Example: If set to 60, only significant changes in the content will trigger a scene cut.\n"
            "Range: 1-100. Default: 60."
        )
        layout.addWidget(self.content_threshold_label)
        layout.addWidget(self.content_threshold)

        # ThresholdDetector settings
        self.threshold_value_label = QtWidgets.QLabel("Threshold Detector Value:")
        self.threshold_value = QtWidgets.QSpinBox()
        self.threshold_value.setRange(1, 100)
        self.threshold_value.setValue(100)
        self.threshold_value.setToolTip(
            "Threshold for luma-based scene detection.\n"
            "Higher values mean less sensitivity to changes in brightness.\n"
            "Example: A value of 100 will detect only major brightness changes as scene cuts.\n"
            "Range: 1-100. Default: 100."
        )
        layout.addWidget(self.threshold_value_label)
        layout.addWidget(self.threshold_value)

        self.min_scene_len_label = QtWidgets.QLabel("Minimum Scene Length:")
        self.min_scene_len = QtWidgets.QSpinBox()
        self.min_scene_len.setRange(1, 1000)
        self.min_scene_len.setValue(1000)
        self.min_scene_len.setToolTip(
            "Minimum length of a scene in frames.\n"
            "Increasing this value will reduce the number of detected scenes.\n"
            "Example: If set to 1000, scenes shorter than 1000 frames will not be detected.\n"
            "Range: 1-1000. Default: 1000."
        )
        layout.addWidget(self.min_scene_len_label)
        layout.addWidget(self.min_scene_len)

        # AdaptiveDetector settings
        self.adaptive_threshold_label = QtWidgets.QLabel("Adaptive Detector Threshold:")
        self.adaptive_threshold = QtWidgets.QSpinBox()
        self.adaptive_threshold.setRange(1, 10)
        self.adaptive_threshold.setValue(10)
        self.adaptive_threshold.setToolTip(
            "Threshold for adaptive scene detection.\n"
            "Higher values make the detector less sensitive to gradual changes.\n"
            "Example: A value of 10 will ignore minor changes and focus on significant scene transitions.\n"
            "Range: 1-10. Default: 10."
        )
        layout.addWidget(self.adaptive_threshold_label)
        layout.addWidget(self.adaptive_threshold)

        # Downscale factor
        self.downscale_label = QtWidgets.QLabel("Downscale Factor:")
        self.downscale_factor = QtWidgets.QSpinBox()
        self.downscale_factor.setRange(1, 4)
        self.downscale_factor.setValue(1)
        self.downscale_factor.setToolTip(
            "Factor to downscale the video for faster processing.\n"
            "Example: A value of 2 will process the video at half its original resolution, speeding up detection.\n"
            "Range: 1-4. Default: 1 (no downscaling)."
        )
        layout.addWidget(self.downscale_label)
        layout.addWidget(self.downscale_factor)

        # Frame skip
        self.frame_skip_label = QtWidgets.QLabel("Frame Skip:")
        self.frame_skip = QtWidgets.QSpinBox()
        self.frame_skip.setRange(0, 10)
        self.frame_skip.setValue(0)
        self.frame_skip.setToolTip(
            "Number of frames to skip between each analysis.\n"
            "Example: A value of 2 will analyze every third frame, speeding up detection but possibly missing scenes.\n"
            "Range: 0-10. Default: 0 (no skipping)."
        )
        layout.addWidget(self.frame_skip_label)
        layout.addWidget(self.frame_skip)

        # Buttons
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)


def run_scene_detection_and_cut_in_nukestudio():
    selected_sequence = hiero.ui.activeSequence()

    if selected_sequence is None:
        error_message = QtWidgets.QMessageBox()
        error_message.setIcon(QtWidgets.QMessageBox.Critical)
        error_message.setText("No sequence selected.")
        error_message.setInformativeText("Please select a sequence before running the script.")
        error_message.setWindowTitle("Error")
        error_message.exec_()
        return

    # Check if the sequence contains a video track with clips
    if len(selected_sequence.videoTracks()) == 0 or all(
            len(track.items()) == 0 for track in selected_sequence.videoTracks()):
        error_message = QtWidgets.QMessageBox()
        error_message.setIcon(QtWidgets.QMessageBox.Critical)
        error_message.setText("No video clips found.")
        error_message.setInformativeText(
            "The selected sequence does not contain any video clips. Please add clips to the sequence before running the script.")
        error_message.setWindowTitle("Error")
        error_message.exec_()
        return

    settings_dialog = SceneDetectSettings()
    if settings_dialog.exec_() == QtWidgets.QDialog.Accepted:
        # Retrieve user settings
        content_threshold = settings_dialog.content_threshold.value()
        threshold_value = settings_dialog.threshold_value.value()
        min_scene_len = settings_dialog.min_scene_len.value()
        adaptive_threshold = settings_dialog.adaptive_threshold.value()
        downscale_factor = settings_dialog.downscale_factor.value()
        frame_skip = settings_dialog.frame_skip.value()

        # Get the media source file path
        track_item = selected_sequence.videoTrack(0).items()[0]
        media_source = track_item.source().mediaSource()
        video_path = media_source.fileinfos()[0].filename()

        # Set up VideoManager with downscale factor
        video_manager = VideoManager([video_path])
        video_manager.set_downscale_factor(downscale_factor)

        # Set up SceneManager
        scene_manager = SceneManager()

        # Add detectors with user-defined settings
        scene_manager.add_detector(ContentDetector(threshold=content_threshold))
        scene_manager.add_detector(ThresholdDetector(threshold=threshold_value, min_scene_len=min_scene_len))
        scene_manager.add_detector(AdaptiveDetector(adaptive_threshold=adaptive_threshold))

        # Perform scene detection
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list()
        video_manager.release()

        # Convert scenes to frame numbers
        scene_frames = [scene[0].get_frames() for scene in scene_list]

        # Perform razor cuts at each detected scene frame
        selected_sequence.razorAt(scene_frames)

        # Show completion message
        success_message = QtWidgets.QMessageBox()
        success_message.setIcon(QtWidgets.QMessageBox.Information)
        success_message.setText("Cut Detective Studio Completed")
        success_message.setInformativeText(f"The operation was successful. {len(scene_frames)} shots were created.")
        success_message.setWindowTitle("Operation Completed")
        success_message.exec_()

        print(f"Scene detection and cutting completed for {video_path}. Razor cuts made at frames: {scene_frames}")


# Execute the scene detection and cutting process
run_scene_detection_and_cut_in_nukestudio()

