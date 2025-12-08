Use the following instructions for your coding agent. Fill in this section with your component requirements. Be as specific as possible.

# Customizing Themes

The following are details of the app and the theme required for the app. Use these details along with Theme.md to modify the theme of this existing template app.

## Theme Specification

### Application Identity
```yaml
# Application Identity
app_name: "StockAnalyzer Pro"
app_description: "A comprehensive stock market analysis platform with real-time charts and technical indicators"
tagline: "Professional Market Intelligence at Your Fingertips"
domain: "stockanalyzer.pro"

# Color Scheme
theme_preset: "sunset"  # Using Sunset theme for financial/professional feel

# Typography
heading_font: "Roboto, sans-serif"
body_font: "Inter, sans-serif"
font_cdn:
  - "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
  - "https://fonts.googleapis.com/css2?family=Roboto:wght@600;700;900&display=swap"

# Navigation
navigation_items:
  - name: "Home"
    path: "/"
    icon: "Home"
  - name: "Portfolio Dashboard"
    path: "/plots"
    icon: "BarChart3"

# Homepage Content
hero:
  title: "Advanced Stock Market Analytics"
  subtitle: "Track your portfolio, analyze stocks with professional-grade charts, and make informed investment decisions with real-time data and technical indicators."
  cta_primary: "View Portfolio Dashboard"
  cta_secondary: "Learn More"

# Design
design_style: "modern"
border_radius: "0.5rem"
spacing: "standard"
```

Use the instructions in Theme.md to apply the required changes for this app.

---

# Component: Stock Analysis Dashboard

The following are detailed requirements of new components in the app. Use these details along with Component.md to implement the required components in the app.

## Stock Analysis Dashboard Component Requirements

### Overview
Create a comprehensive stock market analysis platform with two main views: a Portfolio Overview showing all tracked stocks with key metrics, and a detailed Stock Dashboard with advanced charting and technical analysis capabilities. The application uses Plotly.js for interactive data visualization.

### Dependencies to Install

Before implementing the component, install the required dependencies:

```bash
npm install plotly.js react-plotly.js
```

### Functional Requirements

#### Portfolio Overview Component

**Data Model - Stock List:**
Each stock in the portfolio should include:
- **Symbol**: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
- **Name**: Company full name
- **Sector**: Industry sector classification
- **Metrics**: Real-time stock metrics (loaded dynamically)

**Stock Metrics Data Model:**
- **Price**: Current stock price (USD)
- **Change**: Dollar change from previous close
- **Change Percent**: Percentage change from previous close
- **Volume**: Trading volume
- **Market Cap**: Total market capitalization
- **52 Week High**: Highest price in past year
- **52 Week Low**: Lowest price in past year
- **P/E Ratio**: Price-to-earnings ratio
- **Dividend Yield**: Annual dividend percentage
- **Beta**: Stock volatility measure

**Portfolio Summary Cards (4 KPI Cards):**
1. **Portfolio Value**
   - Display total market cap of all holdings
   - Show count of total stocks
   - Icon: DollarSign
   - Format large numbers (B for billions, M for millions)

2. **Average Daily Change**
   - Calculate average change percent across all stocks
   - Display with trend indicator (up/down)
   - Color-coded (green for positive, red for negative)
   - Icon: Activity

3. **Top Performers**
   - Count of stocks with positive gains
   - Display in green with TrendingUp icon
   - Show "Stocks with gains today" subtitle

4. **Underperformers**
   - Count of stocks with losses
   - Display in red with TrendingDown icon
   - Show "Stocks with losses today" subtitle

**Stock Holdings Table:**
Display all stocks in a comprehensive table with columns:
- Symbol (with circular avatar showing first 2 letters)
- Company name
- Sector (as badge/pill)
- Current price
- Dollar change (color-coded)
- Percentage change (with trend icon)
- Market capitalization
- P/E ratio
- Analyze button (navigate to detail view)

Table features:
- Hover effects on rows
- Click entire row to view details
- Responsive design with horizontal scroll on mobile
- Alternating row backgrounds

**Sector Distribution Section:**
- Display breakdown by sector
- Show stock count and percentage for each sector
- Progress bars showing proportion
- Calculate dynamically from portfolio holdings

**Performance Summary Section:**
Display key insights:
- Best Performer: Stock with highest gain percentage
- Worst Performer: Stock with lowest change percentage
- Highest P/E Ratio: Stock with highest P/E
- Largest Market Cap: Stock with biggest market cap
- Each shown in styled card with appropriate color coding

**User Interactions:**
- Click on stock row to view detailed analysis
- Click "Analyze" button to navigate to stock dashboard
- Loading state while fetching portfolio data
- Real-time metric updates

#### Stock Dashboard Component

**Component States:**
- selectedStock: Currently analyzed stock symbol
- stockData: Historical OHLCV (Open, High, Low, Close, Volume) data
- metrics: Current stock metrics
- movingAverages: SMA and EMA indicators
- technicalIndicators: RSI, MACD, Bollinger Bands
- isLoading: Loading state
- timeRange: Selected time period (30, 90, 180, 365 days)
- isDarkMode: Theme detection for chart colors

**Header Controls:**
- Back button (if navigated from portfolio)
- Stock name and sector display
- Stock selector dropdown (all available stocks)
- Time range selector (1 Month, 3 Months, 6 Months, 1 Year)
- Responsive layout (stack on mobile)

**KPI Cards (4 Cards):**
1. **Current Price**
   - Large price display with 2 decimal places
   - Dollar change today
   - Percentage change with trend indicator
   - Color-coded trend arrow

2. **Market Cap**
   - Formatted market capitalization
   - Trading volume as subtitle
   - BarChart3 icon

3. **P/E Ratio**
   - Price-to-earnings ratio
   - Beta value as subtitle
   - Activity icon

4. **52-Week Range**
   - Display low - high range
   - Dividend yield as subtitle
   - Calendar icon

**Price Action & Volume Charts:**

**Candlestick Chart:**
- Display OHLC data as candlestick chart
- Green candles for price increases
- Red candles for price decreases
- X-axis: Date (formatted)
- Y-axis: Price in USD
- Height: 400px
- No range slider (keep view clean)
- Hover: Show OHLC values
- Interactive zoom and pan

**Volume Chart (below candlestick):**
- Bar chart showing trading volume
- Bars colored by price direction (green if close > open, red otherwise)
- X-axis: Date
- Y-axis: Volume
- Height: 150px
- Synchronized with price chart

**Moving Averages Chart:**
- Line chart showing close price with overlays:
  - Close Price (main line, bold)
  - SMA 20 (Simple Moving Average, dotted line)
  - SMA 50 (Simple Moving Average, dotted line)
- Legend at bottom
- Height: 300px
- Interactive hover showing all values

**Technical Indicators Panel:**

Display in card format:

1. **RSI (Relative Strength Index)**
   - Value with 2 decimals
   - Status: Overbought (>70), Oversold (<30), Neutral
   - Color-coded by status (red/green/default)

2. **MACD (Moving Average Convergence Divergence)**
   - MACD value
   - Signal line value
   - Display both values

3. **Bollinger Bands**
   - Upper band value
   - Middle band (20-day SMA)
   - Lower band value
   - Formatted as currency

4. **Moving Averages Summary**
   - SMA 20, SMA 50
   - EMA 12, EMA 26
   - Displayed in grid format

**Theme-Aware Styling:**
- Detect dark mode using MutationObserver
- Adjust chart colors for theme:
  - Text color (light text in dark mode)
  - Grid color (subtle contrast)
  - Transparent backgrounds
  - Green/red colors remain consistent
- Smooth theme transitions

**Data Loading:**
- Load all data in parallel using Promise.all()
- Show loading spinner during fetch
- Handle errors gracefully
- Reload data when stock or time range changes

**Responsive Design:**
- Full-width container with max-width constraint
- Padding for header spacing (pt-20 for fixed nav)
- Grid layouts collapse on mobile
- Charts resize responsively
- Table scrolls horizontally on small screens

#### Data Service Integration

The components should use DataService from `@/lib/DataService` with the following methods:
GetStockList() - Retrieves list of stocks
GetStockData(symbol, days) - Historical OHLCV data
GetStockMetrics(symbol) - Current stock metrics
GetMovingAverages(symbol) - SMA and EMA indicators
GetTechnicalIndicators(symbol) - RSI, MACD, Bollinger Bands

Make sure to implement them using mock data.

**Stock List:**
```javascript
GetStockList()
```
Returns array of stock objects with symbol, name, and sector.

**Historical Stock Data:**
```javascript
GetStockData(symbol, days)
```
Returns OHLCV data for specified number of days.
Response format:
```javascript
{
  data: [
    {
      date: "2024-01-01",
      open: 150.25,
      high: 152.50,
      low: 149.80,
      close: 151.75,
      volume: 45000000
    },
    // ... more data points
  ]
}
```

**Stock Metrics:**
```javascript
GetStockMetrics(symbol)
```
Returns current stock metrics including price, change, market cap, P/E, etc.

**Moving Averages:**
```javascript
GetMovingAverages(symbol)
```
Returns SMA and EMA values:
```javascript
{
  data: {
    sma20: 150.25,
    sma50: 148.75,
    sma200: 145.50,
    ema12: 151.00,
    ema26: 149.25
  }
}
```

**Technical Indicators:**
```javascript
GetTechnicalIndicators(symbol)
```
Returns RSI, MACD, Bollinger Bands:
```javascript
{
  data: {
    rsi: 65.5,
    macd: 2.35,
    signal: 1.85,
    histogram: 0.50,
    bollingerUpper: 155.50,
    bollingerMiddle: 150.00,
    bollingerLower: 144.50
  }
}
```

### Component Structure

Create the following files:

**1. `src/app/plots/page.jsx`** - Main plots route page
- Client component ('use client' directive)
- Manage view state ('portfolio' or 'detail')
- Manage selected stock state
- Render PortfolioOverview or StockDashboard based on view
- Provide navigation handlers
- Display appropriate header based on view
- Responsive container with padding

**2. `src/components/plots/PortfolioOverview.jsx`** - Portfolio overview component
- Client component
- Accept onSelectStock callback prop
- Load portfolio data for all stocks
- Display summary KPI cards
- Render comprehensive stock table
- Show sector distribution visualization
- Display performance summary insights
- Handle loading and error states
- Format numbers appropriately (B, M, K)

**3. `src/components/plots/StockDashboard.jsx`** - Detailed stock analysis component
- Client component
- Accept initialStock and onBack props
- Dynamic import of Plot from react-plotly.js (no SSR)
- Manage all component states
- Detect and respond to theme changes
- Load all data in parallel
- Render header with controls
- Display KPI cards
- Show candlestick and volume charts
- Display moving averages chart
- Show technical indicators panel
- Handle loading states
- Format numbers and percentages
- Theme-aware chart configurations

**4. `src/components/plots/PlotDisplay.jsx`** (Optional reference component)
- Example component showing basic Plotly usage
- Demonstrates different chart types
- Shows dynamic import pattern
- Can be used as reference for chart configurations

### Plotly Chart Configuration

**Base Layout Configuration:**
```javascript
{
  paper_bgcolor: 'rgba(0,0,0,0)',  // Transparent background
  plot_bgcolor: 'rgba(0,0,0,0)',   // Transparent plot area
  font: {
    color: colors.text,              // Theme-aware text
    family: 'Inter, sans-serif',
    size: 12
  },
  margin: { t: 30, r: 10, b: 40, l: 60 },
  xaxis: {
    gridcolor: colors.grid,          // Theme-aware grid
    color: colors.text,
    showgrid: true
  },
  yaxis: {
    gridcolor: colors.grid,
    color: colors.text,
    showgrid: true
  },
  hovermode: 'x unified'             // Unified hover across traces
}
```

**Color Palette (Theme-Aware):**
```javascript
const colors = {
  text: isDarkMode ? '#e5e7eb' : '#1f2937',
  grid: isDarkMode ? '#374151' : '#e5e7eb',
  paper: 'rgba(0,0,0,0)',
  plot: 'rgba(0,0,0,0)',
  up: '#10b981',      // Green for gains
  down: '#ef4444',    // Red for losses
  volume: isDarkMode ? '#6366f1' : '#8b5cf6'
};
```

**Chart Responsive Configuration:**
```javascript
config={{
  responsive: true,
  displayModeBar: false  // Hide Plotly toolbar for cleaner UI
}}
```

### Styling & Design Specifications

**Layout:**
- Container: max-w-7xl mx-auto
- Padding: pt-20 pb-12 px-4 (top padding for fixed header)
- Section spacing: space-y-6

**Cards:**
- Background: bg-card
- Border: border rounded-lg
- Padding: p-4 to p-6
- Shadow on hover for interactive elements

**Tables:**
- Full width with overflow-x-auto wrapper
- Sticky header with muted background
- Hover effects on rows (bg-accent/50)
- Divide rows with subtle borders

**Icons:**
- Size: h-5 w-5 for standard icons
- Color: text-primary or text-muted-foreground
- Contextual colors for trends (green/red)

**Typography:**
- Page titles: text-3xl md:text-4xl font-bold text-primary
- Card titles: text-lg font-semibold
- KPI values: text-2xl font-bold
- Table text: text-sm
- Muted text: text-muted-foreground

**Color Coding:**
- Positive values: text-green-600 dark:text-green-400
- Negative values: text-red-600 dark:text-red-400
- Primary accent: text-primary
- Secondary text: text-muted-foreground

**Responsive Breakpoints:**
- Mobile: < 768px (single column, stacked elements)
- Tablet: 768px - 1024px (2 columns for grids)
- Desktop: > 1024px (3-4 columns for grids)

### User Experience Features

**Loading States:**
- Centered spinner with Loader2 icon
- Animated spin
- Primary color
- Loading text if appropriate
- Show during all async operations

**Navigation Flow:**
1. User lands on /plots route
2. Sees Portfolio Overview by default
3. Clicks on stock row or Analyze button
4. View switches to Stock Dashboard
5. Back button returns to Portfolio Overview
6. Can change stocks via dropdown in dashboard

**Interactive Features:**
- Stock selector dropdown in dashboard
- Time range selector (1M, 3M, 6M, 1Y)
- Clickable table rows
- Chart zoom and pan (Plotly built-in)
- Hover tooltips on charts
- Back navigation

**Data Presentation:**
- Large numbers formatted (B, M, K suffixes)
- Prices to 2 decimal places
- Percentages to 2 decimal places
- Volume formatted with commas or abbreviations
- Dates formatted consistently
- Color coding for gains/losses

### Technical Implementation Details

#### Dynamic Import for Plotly

To avoid SSR issues in Next.js, use dynamic imports:

```javascript
const Plot = dynamic(() => import('react-plotly.js'), {
  ssr: false,
  loading: () => (
    <div className="flex justify-center p-8">
      <Loader2 className="h-8 w-8 animate-spin text-primary" />
    </div>
  )
});
```

#### Theme Detection

```javascript
useEffect(() => {
  const checkTheme = () => {
    setIsDarkMode(document.documentElement.classList.contains('dark'));
  };
  checkTheme();

  // Watch for theme changes
  const observer = new MutationObserver(checkTheme);
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  });

  return () => observer.disconnect();
}, []);
```

#### Number Formatting Utilities

```javascript
const formatNumber = (num) => {
  if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
  if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
  if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
  return `$${num.toFixed(2)}`;
};

const formatVolume = (num) => {
  if (num >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
  if (num >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
  return `${num.toLocaleString()}`;
};
```

#### Parallel Data Loading

```javascript
const loadStockData = async () => {
  setIsLoading(true);
  try {
    const [stockRes, metricsRes, maRes, tiRes] = await Promise.all([
      DataService.GetStockData(selectedStock, parseInt(timeRange)),
      DataService.GetStockMetrics(selectedStock),
      DataService.GetMovingAverages(selectedStock),
      DataService.GetTechnicalIndicators(selectedStock)
    ]);

    setStockData(stockRes.data);
    setMetrics(metricsRes.data);
    setMovingAverages(maRes.data);
    setTechnicalIndicators(tiRes.data);
  } catch (error) {
    console.error('Error loading stock data:', error);
  } finally {
    setIsLoading(false);
  }
};
```

### Accessibility

- Semantic HTML structure
- Proper heading hierarchy (h1, h2, h3)
- ARIA labels for interactive elements
- Color contrast compliance
- Keyboard navigation support
- Screen reader friendly text
- Focus indicators on interactive elements

### Performance Considerations

- Dynamic imports to reduce bundle size
- Lazy loading of charts
- Memoize expensive calculations
- Efficient re-renders with proper state management
- Parallel data fetching
- Responsive chart resizing
- Optimized chart configurations

### Testing Scenarios

1. **Portfolio Overview:**
   - Verify all stocks load correctly
   - Check KPI calculations are accurate
   - Test sector distribution percentages
   - Verify best/worst performer identification
   - Test row click navigation

2. **Stock Dashboard:**
   - Test stock selector dropdown
   - Verify time range changes update data
   - Check all charts render correctly
   - Verify technical indicators display
   - Test back button functionality
   - Check theme switching updates charts

3. **Data Integration:**
   - Verify DataService calls
   - Test loading states
   - Simulate API errors
   - Check data formatting

4. **Responsive Design:**
   - Test on mobile devices
   - Verify tablet layout
   - Check desktop multi-column grids
   - Test table horizontal scroll

5. **Theme Support:**
   - Toggle between light and dark mode
   - Verify chart colors adapt
   - Check text contrast
   - Verify all UI elements visible

Use the instructions in Component.md to implement the required changes for this app.

---

# Component: Home Page / Landing Page

The following are detailed requirements for the home page / landing page. Use these details along with Component.md to implement the required components in the app.

## Home Page / Landing Page Requirements

### Overview
Create a professional, engaging landing page for StockAnalyzer Pro that showcases the platform's capabilities, highlights key features for investors and traders, and drives users to explore the portfolio dashboard.

### Page Sections

#### 1. Hero Section
- **Headline**: Bold, attention-grabbing main heading
  - Text: "Professional Stock Market Analytics for Smart Investors"
  - Subheading: "Track your portfolio, analyze market trends, and make data-driven investment decisions with real-time charts, technical indicators, and comprehensive market intelligence."
- **Call-to-Action Buttons**:
  - Primary: "View Portfolio Dashboard" (navigate to /plots)
  - Secondary: "Explore Features" (scroll to features section)
- **Hero Visual**:
  - Animated chart or graph visualization
  - Use Sunset theme colors for consistency
  - Show sample stock chart or dashboard preview
- **Design**:
  - Full-width section with gradient background
  - Centered content with max-width container
  - Responsive layout (stack on mobile)

#### 2. Features Section
Highlight the core features with icon cards in a 3-column grid:

**Feature 1: Portfolio Overview**
- Icon: PieChart icon
- Title: "Comprehensive Portfolio Tracking"
- Description: "Monitor all your stock holdings in one place with real-time metrics, performance summaries, and sector distribution analysis."

**Feature 2: Advanced Charting**
- Icon: BarChart3 icon
- Title: "Professional-Grade Charts"
- Description: "Analyze stocks with interactive candlestick charts, volume analysis, and customizable time ranges powered by Plotly."

**Feature 3: Technical Indicators**
- Icon: Activity icon
- Title: "Technical Analysis Tools"
- Description: "Access RSI, MACD, Bollinger Bands, and moving averages to identify trends and trading opportunities."

**Feature 4: Real-time Data**
- Icon: TrendingUp icon
- Title: "Live Market Data"
- Description: "Stay updated with real-time stock prices, market cap, P/E ratios, and daily changes across your portfolio."

**Feature 5: Performance Insights**
- Icon: Target icon
- Title: "Performance Analytics"
- Description: "Track top performers, identify underperformers, and analyze sector allocation to optimize your investment strategy."

**Feature 6: Multi-Stock Comparison**
- Icon: Layers icon
- Title: "Compare Multiple Stocks"
- Description: "Easily switch between stocks, compare metrics, and analyze different companies within your portfolio."

#### 3. How It Works Section
Step-by-step visual guide (3 steps in a horizontal timeline):

**Step 1: View Your Portfolio**
- Icon: Eye icon
- Title: "Access Dashboard"
- Description: "View your complete portfolio with key metrics, performance summaries, and market insights at a glance."

**Step 2: Analyze Stocks**
- Icon: Search icon
- Title: "Deep Dive Analysis"
- Description: "Click on any stock to access detailed charts, technical indicators, and historical performance data."

**Step 3: Make Informed Decisions**
- Icon: CheckCircle icon
- Title: "Trade with Confidence"
- Description: "Use professional analytics and real-time data to make informed investment decisions and optimize returns."

#### 4. Statistics Showcase Section
Display impressive metrics in a visually appealing way:
- **Dynamic Counter Cards** (4 cards):
  - "8 Major Stocks Tracked" with BarChart3 icon
  - "Real-time Updates" with Zap icon
  - "Multiple Timeframes" with Calendar icon
  - "Professional Indicators" with Activity icon

#### 5. Key Metrics Highlight Section
Showcase what users can track:
- **4 Metric Cards**:
  - Market Price - "Track real-time stock prices and daily changes"
  - Market Cap - "Monitor company valuations and trading volumes"
  - P/E Ratios - "Analyze valuation metrics and beta coefficients"
  - Technical Indicators - "RSI, MACD, Bollinger Bands, and moving averages"

#### 6. Call-to-Action Banner
- **Background**: Gradient with Sunset theme colors
- **Headline**: "Ready to Elevate Your Investment Strategy?"
- **Subtext**: "Access professional-grade stock analysis tools and real-time market data today"
- **Button**: "Open Portfolio Dashboard" (navigate to /plots)

#### 7. Footer Section
- Already exists in template, but ensure it includes:
  - App name and tagline
  - Copyright information
  - Links (if applicable)

### Design Specifications

#### Layout & Spacing
- **Max Width**: 1280px for content sections
- **Section Padding**: py-16 to py-24 (responsive)
- **Section Gaps**: Adequate whitespace between sections
- **Container**: Centered with px-4 sm:px-6 lg:px-8

#### Typography
- **Hero Headline**: text-4xl sm:text-5xl lg:text-6xl font-bold
- **Section Headings**: text-3xl sm:text-4xl font-bold
- **Feature Titles**: text-xl font-semibold
- **Body Text**: text-base sm:text-lg text-muted-foreground
- Use Roboto for headings, Inter for body text

#### Color Palette (Sunset Theme)
- **Background**: Use gradient backgrounds for hero and CTA sections
- **Accent Colors**: Primary sunset colors for CTAs and highlights
- **Feature Cards**: bg-card with border
- **Icons**: text-primary or themed colors
- **Financial Colors**: Green for positive, red for negative (traditional finance colors)

#### Interactive Elements
- **Buttons**:
  - Hover effects with scale and shadow
  - Smooth transitions
  - Primary button with gradient or solid sunset color
- **Cards**:
  - Hover: lift effect (shadow increase)
  - Rounded corners (0.5rem)
- **Animations**:
  - Fade-in on scroll (optional)
  - Smooth scroll behavior
  - Number counters (animated)

### Component Structure

Create components in `src/components/home/`:
- **HeroSection.jsx** - Main hero section
- **FeaturesSection.jsx** - Feature cards grid
- **HowItWorksSection.jsx** - Step-by-step guide
- **StatsSection.jsx** - Statistics showcase
- **MetricsHighlight.jsx** - Key metrics available
- **CTABanner.jsx** - Final call-to-action

Update `src/app/page.jsx` to use these components instead of the current placeholder content.

### Functional Requirements

#### Navigation
- "View Portfolio Dashboard" and "Open Portfolio Dashboard" buttons should navigate to `/plots`
- "Explore Features" should smooth scroll to features section
- All navigation should be smooth and responsive

#### Responsive Design
- **Mobile** (< 640px): Single column layout, stacked elements
- **Tablet** (640px - 1024px): 2-column grid for features
- **Desktop** (> 1024px): 3-column grid for features

#### Animations (Optional)
- Fade-in animations for sections on scroll
- Number counter animation for statistics
- Smooth scroll behavior
- Button hover and active states
- Chart animation in hero section

#### Accessibility
- Proper heading hierarchy (h1, h2, h3)
- Alt text for all images/icons
- Sufficient color contrast
- Keyboard navigation support
- Screen reader friendly
- Focus indicators

### Content Strategy

#### Tone & Voice
- Professional and authoritative
- Data-driven and analytical
- Trustworthy and reliable
- Action-oriented

#### Messaging Hierarchy
1. **What**: Professional stock analysis platform
2. **Who**: For investors, traders, and portfolio managers
3. **Why**: Make informed, data-driven investment decisions
4. **How**: Real-time data, charts, and technical indicators
5. **Action**: Start analyzing your portfolio now

### User Experience Goals
- Visitors should immediately understand StockAnalyzer Pro's value
- Convey professionalism and reliability
- Highlight data-driven decision making
- Multiple conversion points (CTAs) throughout the page
- Mobile-first, responsive experience
- Fast loading times with optimized assets
- Visual representations of stock charts/data

### Visual Enhancements

**Chart/Graph Visuals:**
- Consider adding sample mini charts in feature cards
- Show preview of candlestick chart in hero
- Use chart-related icons consistently
- Color code gains/losses in examples

**Trust Indicators:**
- Emphasize real-time data
- Highlight professional-grade tools
- Show variety of technical indicators
- Demonstrate comprehensive analysis

Use the instructions in Component.md to implement the required changes for this app.
---
