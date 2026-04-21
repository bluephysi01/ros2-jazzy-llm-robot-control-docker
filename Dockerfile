FROM bluephysi01/ros2_jazzy_pinky:latest

SHELL ["/bin/bash", "-c"]

COPY ./src /home/root/ros2_pinky_ws/src

WORKDIR /home/root/ros2_pinky_ws

RUN source /opt/ros/jazzy/setup.bash && colcon build --symlink-install

RUN grep -qF "source /home/root/ros2_pinky_ws/install/setup.bash" ~/.bashrc || \
    echo "source /home/root/ros2_pinky_ws/install/setup.bash" >> ~/.bashrc
