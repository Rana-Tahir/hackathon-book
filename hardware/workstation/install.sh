#!/usr/bin/env bash
# Physical AI & Humanoid Robotics — Full Stack Installation
# Target: Ubuntu 22.04 LTS (fresh install)
# Run as: bash install.sh
#
# This script installs the complete development environment for the book.
# All commands are copy-paste validated per FR-012 and FR-016.

set -euo pipefail

echo "=== Physical AI & Humanoid Robotics — Environment Setup ==="
echo "Target: Ubuntu 22.04 LTS"
echo ""

# ------------------------------------------------------------------
# Step 1: System prerequisites
# ------------------------------------------------------------------
echo "[1/7] Installing system prerequisites..."
sudo apt update
sudo apt install -y \
  locales \
  software-properties-common \
  curl \
  wget \
  gnupg2 \
  lsb-release \
  git \
  build-essential \
  cmake \
  python3-pip \
  python3-venv \
  ffmpeg

# Set locale (required by ROS 2)
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# ------------------------------------------------------------------
# Step 2: ROS 2 Humble Hawksbill
# ------------------------------------------------------------------
echo "[2/7] Installing ROS 2 Humble..."
sudo add-apt-repository universe -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install -y ros-humble-desktop

# Source ROS 2
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Install colcon build tools
sudo apt install -y python3-colcon-common-extensions

# ------------------------------------------------------------------
# Step 3: Gazebo Fortress + ROS bridge
# ------------------------------------------------------------------
echo "[3/7] Installing Gazebo Fortress..."
sudo apt install -y \
  ros-humble-ros-gz \
  ros-humble-rviz2 \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher \
  ros-humble-xacro

# ------------------------------------------------------------------
# Step 4: Nav2 Navigation Stack
# ------------------------------------------------------------------
echo "[4/7] Installing Nav2..."
sudo apt install -y \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup

# ------------------------------------------------------------------
# Step 5: Python dependencies
# ------------------------------------------------------------------
echo "[5/7] Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install \
  openai-whisper \
  faster-whisper \
  torch \
  transformers

# ------------------------------------------------------------------
# Step 6: Node.js + Docusaurus
# ------------------------------------------------------------------
echo "[6/7] Installing Node.js and Docusaurus..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# ------------------------------------------------------------------
# Step 7: Verification
# ------------------------------------------------------------------
echo "[7/7] Verifying installation..."
echo ""

source /opt/ros/humble/setup.bash

echo "ROS 2:     $(ros2 --version 2>/dev/null || echo 'NOT FOUND')"
echo "Python:    $(python3 --version)"
echo "Gazebo:    $(gz sim --version 2>/dev/null || echo 'NOT FOUND')"
echo "Node.js:   $(node --version)"
echo "npm:       $(npm --version)"
echo "colcon:    $(colcon version-check 2>/dev/null && echo 'OK' || echo 'INSTALLED')"
echo "ffmpeg:    $(ffmpeg -version 2>/dev/null | head -1 || echo 'NOT FOUND')"
echo ""

echo "=== Installation complete ==="
echo ""
echo "MANUAL STEPS REQUIRED:"
echo "1. Install NVIDIA Isaac Sim via Omniverse Launcher"
echo "   https://docs.omniverse.nvidia.com/isaacsim/latest/installation/"
echo "2. Enable ROS 2 Humble bridge in Isaac Sim settings"
echo "3. For Jetson deployment, use NVIDIA SDK Manager to flash JetPack 6.x"
echo ""
echo "Run 'source ~/.bashrc' to activate ROS 2 in your current terminal."
