import streamlit as st
from pathlib import Path


# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="AI Virtual Mouse",
    page_icon="🖱",
    layout="wide"
)


# =====================================
# Header
# =====================================

st.title("🖱 AI Virtual Mouse")

st.markdown("---")


# =====================================
# Project Overview
# =====================================

st.header("Project Overview")

st.write("""
This project uses:

- OpenCV
- MediaPipe Hand Tracking
- Gesture Recognition
- Virtual Mouse Control
- Video Recording
- Frame Capture
- Real-Time Processing
""")


# =====================================
# Supported Gestures
# =====================================

st.header("Supported Gestures")

st.write("👉 Index Finger → Cursor Movement")

st.write("👌 Thumb + Index Finger → Left Click")

st.write("👍 Thumb + Middle Finger → Right Click")

st.write("🤏 Thumb + Ring Finger → Drag")

st.write("✌ Index + Middle Finger → Scroll")


# =====================================
# Project Workflow
# =====================================

st.header("Project Workflow")

st.write("""
### Workflow Steps

1. Capture live webcam feed

2. Preprocess frames
   - Resize
   - Flip
   - Blur

3. Detect hand landmarks using MediaPipe

4. Recognize gestures

5. Perform mouse actions
   - Cursor Movement
   - Left Click
   - Right Click
   - Drag
   - Scroll

6. Save frames

7. Record video

8. Display results in dashboard
""")


# =====================================
# Captured Frames
# =====================================

st.markdown("---")

st.header("📸 Captured Frames")

frame_folder = Path("captured_frames")

frames = []

if frame_folder.exists():

    frames = sorted(
        frame_folder.glob("*.jpg")
    )

    st.success(
        f"Total Frames Saved: {len(frames)}"
    )

    if len(frames) > 0:

        latest_frame = frames[-1]

        st.image(
            str(latest_frame),
            caption="Latest Captured Frame",
            use_container_width=True
        )

    else:

        st.warning(
            "No frames available."
        )

else:

    st.error(
        "captured_frames folder not found."
    )


# =====================================
# Recorded Videos
# =====================================

st.markdown("---")
st.header("🎥 Recorded Videos")
count=0

video_folder = Path("saved_videos")

if video_folder.exists():

    videos = list(video_folder.glob("*.mp4"))

    if videos:

        count+=1

        selected_video = st.selectbox(
            "Select Video",
            [v.name for v in videos]
        )

        video_path = video_folder / selected_video

        st.write("Path:", video_path)
        st.write("Exists:", video_path.exists())
        st.write("Size:", video_path.stat().st_size, "bytes")

        with open(video_path, "rb") as f:
            video_bytes = f.read()


        st.video(video_bytes)

    else:
        st.warning("No videos found.")

else:
    st.error("saved_videos folder not found.")

# =====================================
# Project Statistics
# =====================================

st.markdown("---")

st.header("📊 Project Statistics")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Frames Saved",
        count
    )

with col2:

    st.metric(
        "Videos Recorded",
        len(videos)
    )


# =====================================
# Project Features
# =====================================

st.markdown("---")

st.header("🚀 Features")

st.write("""
✔ Real-Time Hand Tracking

✔ Cursor Control using Index Finger

✔ Left Click Gesture

✔ Right Click Gesture

✔ Drag and Drop Gesture

✔ Scroll Gesture

✔ Frame Saving

✔ Video Recording

✔ Streamlit Dashboard

✔ Modular Project Structure
""")


# =====================================
# Footer
# =====================================

st.markdown("---")

st.success(
    " Virtual Mouse Project Successfully Running"
)

st.info(
    "Run app.py or test_camera_controller.py to control your system mouse using hand gestures."
)

#st.video(r"C:\Users\siva9\OneDrive\Desktop\New\saved_videos\output1 (video-converter.com).mp4")