Use the following instructions for your coding agent. Fill in this section with your theme requirements. Be as specific as possible.

# Customizing Themes

The following are details of the app and the theme required for the app. Use these details along with Theme.md to modify the theme of this existing template app.

## Theme Specification

### Application Identity
```yaml
# Application Identity
app_name: "PropertyFinder"
app_description: "A comprehensive real estate search platform with interactive mapping"
tagline: "Discover Your Dream Home"
domain: "propertyfinder.com"

# Color Scheme
theme_preset: "forest"  # Using Forest theme for a trust-worthy, professional feel

# Typography
heading_font: "Montserrat, sans-serif"
body_font: "Open Sans, sans-serif"
font_cdn:
  - "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600;700&display=swap"
  - "https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&display=swap"

# Navigation
navigation_items:
  - name: "Home"
    path: "/"
    icon: "Home"
  - name: "Find Properties"
    path: "/map"
    icon: "Map"

# Homepage Content
hero:
  title: "Find Your Perfect Property"
  subtitle: "Explore real estate listings on an interactive map with powerful search and filtering tools."
  cta_primary: "Explore Properties"
  cta_secondary: "Learn More"

# Design
design_style: "modern"
border_radius: "0.75rem"
spacing: "standard"
```

Use the instructions in Theme.md to apply the required changes for this app.

---

# Component: Interactive Property Map

The following are detailed requirements of new components in the app. Use these details along with Component.md to implement the required components in the app.

## Interactive Property Map Component Requirements

### Overview
Create a comprehensive property finder component that displays real estate listings on an interactive map with advanced filtering, dual view modes (map and list), and detailed property information. The component integrates Leaflet maps with React to provide a seamless property browsing experience.

### Dependencies to Install

Before implementing the component, install the required dependencies:

```bash
npm install leaflet react-leaflet react-leaflet-cluster
```

Also ensure you add the Leaflet CSS to your global styles or import it in the component.

### Functional Requirements

#### Property Data Model
Each property should include:
- **ID**: Unique identifier (auto-generated with uuid)
- **Title**: Property name/headline (required)
- **Price**: Property price in USD (required)
- **Type**: One of [house, apartment, condo, townhouse]
- **Bedrooms**: Number of bedrooms (integer)
- **Bathrooms**: Number of bathrooms (can be decimal like 2.5)
- **Square Footage**: Property size in square feet (sqft)
- **Location**: Object containing:
  - lat: Latitude coordinate
  - lng: Longitude coordinate
  - address: Street address
  - city: City name
  - state: State abbreviation
  - zip: Zip code
- **Description**: Detailed property description
- **Image URL**: URL to property image
- **Features**: Array of feature strings (e.g., ["Parking", "Pool"])
- **Status**: Property status (e.g., "For Sale")

#### Data Service Integration

The component should use the existing DataService from `@/lib/DataService` with the following method:
- **GetPropertyListings()**: Fetches all property listings
  - Returns: Promise resolving to `{ data: Property[] }`
  - Already includes mock property data

Add mock property data to `src/lib/SampleData.js`:

```javascript
export const mockProperties = [
    {
        id: uuid(),
        title: "Modern Downtown Loft",
        price: 1250000,
        type: "apartment",
        bedrooms: 2,
        bathrooms: 2,
        sqft: 1450,
        location: {
            lat: 37.7879,
            lng: -122.4074,
            address: "123 Market Street",
            city: "San Francisco",
            state: "CA",
            zip: "94103"
        },
        description: "Stunning modern loft in the heart of downtown with floor-to-ceiling windows and city views.",
        imageUrl: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&h=600&fit=crop",
        features: ["Hardwood Floors", "City View", "Walk-in Closet", "Parking"],
        status: "For Sale"
    },
    // Add 10-15 more properties with varying locations in San Francisco area
];
```

Add the following method to DataService if not present:

```javascript
GetPropertyListings: async function () {
    await new Promise(resolve => setTimeout(resolve, 200));
    return Promise.resolve({ data: mockProperties });
},
```

#### Map Integration

**Leaflet Setup:**
- Use dynamic imports for Leaflet components to avoid SSR issues in Next.js
- Configure default map center (San Francisco: [37.7749, -122.4194])
- Set default zoom level to 12
- Fix Leaflet icon paths for Next.js compatibility

**Map Components:**
- MapContainer: Main map wrapper
- TileLayer: OpenStreetMap tiles
- Marker: Property location markers
- Popup: Property detail popups on marker click
- MarkerClusterGroup: Cluster nearby markers for better performance

**Custom Markers:**
- Display property price as custom marker icon
- Use divIcon with styled HTML (primary background, white text, rounded pill shape)
- Format price as currency without decimals

#### Filtering System

Implement three filter categories:

**1. Property Type Filter**
- Options: All Types, House, Apartment, Condo, Townhouse
- Use Select component from shadcn/ui
- Filter properties by exact type match

**2. Price Range Filter**
- Options:
  - All Prices
  - Under $500K
  - $500K - $1M
  - $1M - $2M
  - $2M+
- Use Select component from shadcn/ui
- Filter properties within price range

**3. Minimum Bedrooms Filter**
- Options: Any, 1+, 2+, 3+, 4+
- Use Select component from shadcn/ui
- Filter properties with at least the specified number of bedrooms

**Filter Functionality:**
- Apply filters in real-time (no submit button)
- Use React state to manage filter values
- Use useEffect to reapply filters when any filter changes
- Provide "Reset Filters" button to clear all filters
- Display count of filtered vs total properties

#### View Modes

**Map View:**
- Display properties as markers on interactive map
- Enable scroll wheel zoom
- Show property details in popup when marker is clicked
- Use marker clustering for better performance with many properties
- Map container should be 600px height with rounded borders and shadow

**List View:**
- Display properties in responsive grid layout:
  - 1 column on mobile (< 768px)
  - 2 columns on tablet (768px - 1024px)
  - 3 columns on desktop (> 1024px)
- Show property card with:
  - Property image (full width, 192px height, cover fit)
  - Property title
  - Property type badge
  - Price (large, bold, primary color)
  - Bedrooms, bathrooms, sqft with icons
  - Description (truncated to 2 lines)
  - Full address with map pin icon
- Cards should have hover effects (shadow increase, border color change)

**View Toggle:**
- Provide buttons to switch between Map and List views
- Highlight active view button
- Use Map and List icons from lucide-react

#### Property Display

**Map Popup Content:**
- Property image (250px width, 128px height)
- Property title (semibold, large)
- Price (primary color, bold, XL size, formatted as currency)
- Bedrooms, bathrooms, sqft with icons in horizontal layout
- Full address
- Property type badge

**List Card Content:**
- Property image (full width card header)
- Property title (truncated to 1 line)
- Property type badge
- Price (2XL size, primary color, formatted as currency)
- Bedrooms, bathrooms, sqft with icons
- Description (truncated to 2 lines)
- Address with city (truncated to 1 line)

#### User Experience Features

**Loading States:**
- Show centered loading spinner with "Loading properties..." text
- Display while fetching data from API

**Error States:**
- Show error message if data fetch fails
- Provide "Try Again" button to retry
- Center error message vertically and horizontally

**Empty States:**
- Display when no properties match current filters
- Show home icon
- Message: "No properties found"
- Subtitle: "Try adjusting your filters to see more results"
- Provide "Reset Filters" button

**Results Summary:**
- Display "Showing X of Y properties" above map/list
- Update count based on active filters

#### Styling & Responsive Design

**Layout:**
- Full-width container with max-width constraint
- Padding: pt-20 (for fixed header), pb-12, px-4
- Section gaps: space-y-6

**Filter Card:**
- Three-column grid on desktop
- Single column on mobile
- Each filter has label and select dropdown

**Icons:**
- MapPin: Location markers
- Home: Empty state
- Bed: Bedrooms
- Bath: Bathrooms
- Maximize2: Square footage
- Filter: Filter section
- Map: Map view button
- List: List view button
- Loader2: Loading spinner

**Colors:**
- Use theme primary color for prices, CTAs, and highlights
- Use muted-foreground for secondary text
- Use card background for containers
- Use border color for dividers

**Typography:**
- Page title: text-3xl md:text-4xl, font-bold, primary color
- Property titles: text-lg font-semibold
- Prices: text-xl to text-2xl, font-bold, primary color
- Body text: text-sm to text-base, muted-foreground

#### Component Structure

Create the following files:

**1. `src/app/map/page.jsx`** - Map route page
- Client component ('use client' directive)
- Import and render MapComponent
- Provide page header with title and description
- Use consistent layout with other pages

**2. `src/components/map/MapComponent.jsx`** - Main map component
- Client component ('use client' directive)
- All map logic, filtering, and data fetching
- Manage component state:
  - properties (all properties)
  - filteredProperties (after filters applied)
  - loading state
  - error state
  - viewMode ('map' or 'list')
  - Filter states (propertyType, priceRange, minBedrooms)
- Handle dynamic imports for Leaflet components
- Fix Leaflet icon paths in useEffect
- Implement all filtering logic
- Render both map and list views
- Handle loading, error, and empty states

### Technical Implementation Details

#### Next.js Compatibility

**Dynamic Imports:**
```javascript
const MapContainer = dynamic(
    () => import('react-leaflet').then((mod) => mod.MapContainer),
    { ssr: false }
);
// Repeat for TileLayer, Marker, Popup, and MarkerClusterGroup
```

**Leaflet Icon Fix:**
```javascript
useEffect(() => {
    if (typeof window !== 'undefined') {
        const L = require('leaflet');
        delete L.Icon.Default.prototype._getIconUrl;
        L.Icon.Default.mergeOptions({
            iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
            iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
        });
    }
}, []);
```

#### Global CSS

Add Leaflet CSS to `src/app/globals.css`:

```css
/* Leaflet CSS */
@import 'leaflet/dist/leaflet.css';
@import 'react-leaflet-cluster/lib/assets/MarkerCluster.css';
@import 'react-leaflet-cluster/lib/assets/MarkerCluster.Default.css';

/* Custom marker styles */
.custom-marker {
  background: transparent !important;
  border: none !important;
}
```

#### Price Formatting

```javascript
const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
    }).format(price);
};
```

#### Filter Logic

```javascript
const applyFilters = () => {
    let filtered = [...properties];

    // Filter by property type
    if (propertyType !== 'all') {
        filtered = filtered.filter(p => p.type === propertyType);
    }

    // Filter by price range
    if (priceRange !== 'all') {
        const [min, max] = priceRange.split('-').map(Number);
        filtered = filtered.filter(p => {
            if (max) {
                return p.price >= min && p.price <= max;
            }
            return p.price >= min;
        });
    }

    // Filter by minimum bedrooms
    if (minBedrooms !== 'all') {
        filtered = filtered.filter(p => p.bedrooms >= Number(minBedrooms));
    }

    setFilteredProperties(filtered);
};
```

### Accessibility

- Use semantic HTML elements
- Provide proper labels for all form controls
- Include alt text for property images
- Ensure sufficient color contrast
- Support keyboard navigation
- Use ARIA labels where appropriate

### Performance Considerations

- Use dynamic imports to reduce initial bundle size
- Implement marker clustering to handle many properties
- Optimize images with appropriate sizing
- Memoize expensive computations
- Lazy load map tiles

### Testing Scenarios

1. **Data Loading**: Verify properties load correctly on mount
2. **Filtering**: Test each filter individually and in combination
3. **View Toggle**: Ensure smooth transition between map and list views
4. **Marker Interaction**: Click markers to see popups with correct data
5. **Responsive Design**: Test on mobile, tablet, and desktop viewports
6. **Error Handling**: Simulate API failures to verify error states
7. **Empty States**: Apply filters that return no results
8. **Reset Filters**: Verify all filters clear when reset button is clicked

Use the instructions in Component.md to implement the required changes for this app.
---

# Component: Home Page / Landing Page

The following are detailed requirements for the home page / landing page. Use these details along with Component.md to implement the required components in the app.

## Home Page / Landing Page Requirements

### Overview
Create an engaging landing page for PropertyFinder that showcases the value proposition, highlights key features, and drives users to explore property listings. The page should communicate trust, professionalism, and ease of use.

### Page Sections

#### 1. Hero Section
- **Headline**: Bold, attention-grabbing main heading
  - Text: "Find Your Dream Home with Ease"
  - Subheading: "Search thousands of real estate listings on an interactive map. Filter by location, price, property type, and more to find your perfect property."
- **Call-to-Action Buttons**:
  - Primary: "Explore Properties" (navigate to /map)
  - Secondary: "Learn More" (scroll to features section)
- **Hero Visual**:
  - Background gradient or property image overlay
  - Use Forest theme colors for consistency
- **Design**:
  - Full-width section with gradient background
  - Centered content with max-width container
  - Responsive layout (stack on mobile)

#### 2. Features Section
Highlight the core features with icon cards in a 3-column grid:

**Feature 1: Interactive Map**
- Icon: Map icon
- Title: "Interactive Property Map"
- Description: "Explore listings on a dynamic map with marker clustering, custom price labels, and detailed popups for each property."

**Feature 2: Advanced Filtering**
- Icon: Filter icon
- Title: "Smart Filtering System"
- Description: "Filter properties by type, price range, and bedrooms to quickly find listings that match your exact criteria."

**Feature 3: Dual View Modes**
- Icon: LayoutGrid icon
- Title: "Map & List Views"
- Description: "Toggle between map view for geographic search and list view for detailed property comparisons."

**Feature 4: Real-time Results**
- Icon: Zap icon
- Title: "Instant Results"
- Description: "See filtered results update in real-time as you adjust your search criteria without page reloads."

**Feature 5: Detailed Property Info**
- Icon: Home icon
- Title: "Comprehensive Details"
- Description: "View property photos, descriptions, features, pricing, and location information all in one place."

**Feature 6: Mobile Responsive**
- Icon: Smartphone icon
- Title: "Mobile Friendly"
- Description: "Search for properties on any device with a fully responsive design optimized for mobile, tablet, and desktop."

#### 3. How It Works Section
Step-by-step visual guide (3 steps in a horizontal timeline):

**Step 1: Browse Properties**
- Icon: Search icon
- Title: "Explore Listings"
- Description: "View all available properties on an interactive map or browse through the list view."

**Step 2: Apply Filters**
- Icon: Sliders icon
- Title: "Refine Your Search"
- Description: "Use filters to narrow down results by property type, price range, and number of bedrooms."

**Step 3: View Details**
- Icon: Eye icon
- Title: "Find Your Match"
- Description: "Click on properties to see detailed information, photos, and location details."

#### 4. Statistics Showcase Section
Display impressive metrics in a visually appealing way:
- **Dynamic Counter Cards** (4 cards):
  - "1,000+ Active Listings" with Home icon
  - "50+ Neighborhoods" with MapPin icon
  - "100% Free to Use" with Heart icon
  - "Updated Daily" with RefreshCw icon

#### 5. Property Types Section
Showcase different property types available:
- **4 Property Type Cards**:
  - Houses - "Single family homes with yards and privacy"
  - Apartments - "Urban living in multi-unit buildings"
  - Condos - "Owned units with shared amenities"
  - Townhouses - "Multi-story homes with shared walls"
- Each card should have an icon, title, description, and property count

#### 6. Call-to-Action Banner
- **Background**: Gradient with Forest theme colors
- **Headline**: "Ready to Find Your Perfect Property?"
- **Subtext**: "Start exploring thousands of listings on our interactive map today"
- **Button**: "Start Searching Now" (navigate to /map)

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
- Use Montserrat for headings, Open Sans for body text

#### Color Palette (Forest Theme)
- **Background**: Use gradient backgrounds for hero and CTA sections
- **Accent Colors**: Primary green for CTAs and highlights
- **Feature Cards**: bg-card with border
- **Icons**: text-primary or themed colors

#### Interactive Elements
- **Buttons**:
  - Hover effects with scale and shadow
  - Smooth transitions
- **Cards**:
  - Hover: lift effect (shadow increase)
  - Rounded corners (0.75rem)
- **Animations**:
  - Fade-in on scroll (optional)
  - Smooth scroll behavior

### Component Structure

Create components in `src/components/home/`:
- **HeroSection.jsx** - Main hero section
- **FeaturesSection.jsx** - Feature cards grid
- **HowItWorksSection.jsx** - Step-by-step guide
- **StatsSection.jsx** - Statistics showcase
- **PropertyTypesSection.jsx** - Property type cards
- **CTABanner.jsx** - Final call-to-action

Update `src/app/page.jsx` to use these components instead of the current placeholder content.

### Functional Requirements

#### Navigation
- "Explore Properties" and "Start Searching Now" buttons should navigate to `/map`
- "Learn More" should smooth scroll to features section
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

#### Accessibility
- Proper heading hierarchy (h1, h2, h3)
- Alt text for all images/icons
- Sufficient color contrast
- Keyboard navigation support
- Screen reader friendly

### Content Strategy

#### Tone & Voice
- Professional and trustworthy
- Clear and concise
- Benefit-focused messaging
- Welcoming and helpful

#### Messaging Hierarchy
1. **What**: Real estate property search platform
2. **Who**: For home buyers and renters
3. **Why**: Easy, visual, comprehensive property search
4. **How**: Interactive map with advanced filtering
5. **Action**: Start exploring properties now

### User Experience Goals
- Visitors should immediately understand PropertyFinder's value
- Key features should be quickly scannable
- Multiple conversion points (CTAs) throughout the page
- Mobile-first, responsive experience
- Fast loading times with optimized assets

Use the instructions in Component.md to implement the required changes for this app.
---
