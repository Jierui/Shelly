ffmpeg -re -i testhls.mp4 -vcodec libx264 -acodec aac -f flv rtmp://127.0.0.1:1935/hls/fly
::ffmpeg -re -i testhls.mp4 -vcodec libx264 -an -f flv rtmp://127.0.0.1:1935/hls/fly