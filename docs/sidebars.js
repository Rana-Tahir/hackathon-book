/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  bookSidebar: [
    'index',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1/introduction',
        'module-1/nodes-topics',
        'module-1/services-actions',
        'module-1/urdf-humanoid',
        'module-1/launch-params',
        'module-1/topic-reference',
        'module-1/debugging',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo)',
      items: [
        'module-2/introduction',
        'module-2/gazebo-world',
        'module-2/spawning-humanoid',
        'module-2/sensors',
        'module-2/ros-gz-bridge',
        'module-2/simulation-limits',
        'module-2/debugging',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Perception & Navigation',
      items: [
        'module-3/introduction',
        'module-3/isaac-sim',
        'module-3/object-detection',
        'module-3/visual-slam',
        'module-3/navigation',
        'module-3/sim-to-real',
        'module-3/jetson-deployment',
        'module-3/debugging',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4/introduction',
        'module-4/whisper',
        'module-4/intent-parsing',
        'module-4/safety-filter',
        'module-4/multi-modal',
        'module-4/debugging',
      ],
    },
    {
      type: 'category',
      label: 'Capstone: The Autonomous Humanoid',
      items: [
        'capstone/integration',
        'capstone/testing',
        'capstone/next-steps',
      ],
    },
    {
      type: 'category',
      label: 'Appendix',
      items: [
        'appendix/cloud-alternatives',
        'appendix/glossary',
        'appendix/prerequisites',
      ],
    },
  ],
};

module.exports = sidebars;
