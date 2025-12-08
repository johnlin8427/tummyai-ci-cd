# App Building Template

A minimal frontend starter template built with React & Next.js. This template provides a clean foundation for quickly starting new applications.

## Getting Started

### 1. Copy the Template

Copy the `frontend-template` directory to start your new project:

### 2. Start App Container

* Go into the frontend folder
Open a terminal and go to the location where `frontend-template` was copied to

* Build & Run Container
```bash
sh docker-shell.sh
```

### 3. Install Dependencies

```bash
npm install
```

### 4. Run Development Server

```bash
npm run dev
```

Your app will be running at [http://localhost:3001](http://localhost:3001)


## Project Structure

```
frontend-template/
├── src/
│   ├── app/
│   │   ├── layout.jsx          # Root layout with header/footer
│   │   ├── page.jsx             # Homepage
│   │   ├── globals.css          # Global styles and design tokens
│   │   └── not-found.jsx        # 404 page
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.jsx       # Main navigation
│   │   │   ├── Footer.jsx       # Footer component
│   │   │   └── ThemeToggle.jsx  # Dark mode toggle
│   │   └── ui/                  # shadcn/ui components
│   │       ├── button.jsx
│   │       ├── card.jsx
│   │       ├── input.jsx
│   │       └── ...
│   └── lib/
│       ├── Common.js            # Utility functions
│       ├── DataService.js       # API service layer
│       ├── SampleData.js        # Mock data for testing
│       └── utils.js             # shadcn/ui utilities
├── public/
│   └── assets/                  # Static assets (logos, images)
├── components.json              # shadcn/ui configuration
├── tailwind.config.js           # Tailwind configuration
├── next.config.js               # Next.js configuration
├── package.json                 # Dependencies
├── Dockerfile                   # Production Docker image
└── Dockerfile.dev               # Development Docker image
```

## Example Apps

### 1: Task Flow Pro
Look in [App-TaskFlowPro.md](App-TaskFlowPro.md)

### 2: Property Finder
Look in [App-PropertyFinder.md](App-PropertyFinder.md)

### 3: Stock Analyzer
Look in [App-StockAnalyzer.md](App-StockAnalyzer.md)

### 4: Agent Chat
Look in [App-AgentChat.md](App-AgentChat.md)
