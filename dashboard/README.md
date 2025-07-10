# Dobbs MCP Dashboard

A beautiful, responsive dashboard for controlling the Mathematical Research MCP System.

## Features

- **Dark/Light Mode Toggle**: Easy on the eyes with customizable themes
- **Flexible Layout**: Responsive design with fixed 16:9 aspect ratio center panel
- **Quick Actions**: 
  - Search Perplexity
  - Search File System
  - Save to Obsidian
- **Tab Navigation**: Research, Visualization, Knowledge, and Publish sections
- **Output Monitor**: Toggle between code output, file tree, and debug logs
- **System Resource Monitor**: Real-time CPU, Memory, and Disk usage
- **Visual Status Indicators**: Green/Yellow/Red status for system health
- **Customizable Appearance**: Font size and font family options

## Design

- Dark theme with cyan accents inspired by data visualization dashboards
- Clean, modern interface with shadcn/ui components
- Responsive layout that maintains usability at different screen sizes
- Central 16:9 workspace that never goes below 50% screen size

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Tech Stack

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Radix UI primitives
- Lucide React icons

## Customization

The dashboard uses CSS variables for theming. You can modify the color scheme in `app/globals.css` by adjusting the HSL values for primary, secondary, and accent colors.