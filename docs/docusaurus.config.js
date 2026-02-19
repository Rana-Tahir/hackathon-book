// @ts-check
const {themes} = require('prism-react-renderer');
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.vsDark;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Embodied Intelligence in the Physical World',
  favicon: 'img/favicon.ico',
  url: 'https://physical-ai-book.vercel.app',
  baseUrl: '/',
  organizationName: 'physical-ai-book',
  projectName: 'physical-ai-book',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  customFields: {
    chatbotApiUrl: process.env.CHATBOT_API_URL || 'http://localhost:8000',
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  themes: ['@docusaurus/theme-live-codeblock'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '.',
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
          exclude: [
            'node_modules/**',
            'build/**',
            'src/**',
            '.docusaurus/**',
            'package.json',
            'package-lock.json',
            'docusaurus.config.js',
            'sidebars.js',
            'babel.config.js',
            'README.md',
            'demo-script.md',
            'vercel.json',
          ],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      metadata: [
        { name: 'description', content: 'Build, simulate, and deploy autonomous humanoid robots with ROS 2, Gazebo, NVIDIA Isaac, and LLM-driven control.' },
        { name: 'keywords', content: 'physical AI, humanoid robotics, ROS 2, Gazebo Fortress, NVIDIA Isaac, Nav2, VLA, simulation' },
      ],
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'bookSidebar',
            position: 'left',
            label: 'Book',
          },
        ],
      },
      footer: {
        style: 'dark',
        copyright: `Physical AI & Humanoid Robotics — Embodied Intelligence in the Physical World`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['bash', 'python', 'yaml', 'markup', 'json', 'docker'],
      },
      liveCodeBlock: {
        playgroundPosition: 'bottom',
      },
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
    }),
};

module.exports = config;
