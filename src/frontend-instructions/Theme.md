# Theme Transformation Instructions for LLM/Coding Agents

This document provides instructions for transforming the baseline `frontend-template` into a custom-themed application. These instructions are designed to be given to an LLM or coding agent to automatically apply a theme.

---

## Theme Specification Extended

### Color Scheme

Choose ONE of the following or define custom colors:

#### Option A: Predefined Theme
```yaml
theme_preset: "default"  # Options: default, ocean, forest, sunset, midnight, coral, lavender
```

#### Option B: Custom Colors (HSL format)
```yaml
# Light Mode Colors
light_primary: "221 83% 53%"          # Main brand color
light_background: "0 0% 100%"         # Page background
light_foreground: "222 47% 11%"       # Text color
light_accent: "210 40% 96%"           # Accent/hover states

# Dark Mode Colors
dark_primary: "217 91% 60%"           # Main brand color
dark_background: "222 47% 11%"        # Page background
dark_foreground: "210 40% 98%"        # Text color
dark_accent: "217 33% 17%"            # Accent/hover states

# Additional colors (optional)
secondary_color: ""
destructive_color: ""
```

### Typography

```yaml
# Font Families (optional - leave empty to use system fonts)
heading_font: ""        # e.g., "Playfair Display, serif"
body_font: ""          # e.g., "Inter, sans-serif"
mono_font: ""          # e.g., "JetBrains Mono, monospace"

# Font CDN Links (if using custom fonts)
font_cdn: []
# Example:
# - "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
```

### Navigation Structure

```yaml
navigation_items:
  - name: "Home"
    path: "/"
    icon: "Home"          # Lucide icon name
  # Add more navigation items as needed
  # - name: "About"
  #   path: "/about"
  #   icon: "Info"
```

### Homepage Content

```yaml
hero:
  title: "Welcome to Your App"
  subtitle: "This is a minimal starter template. Customize this page to fit your application needs."
  cta_primary: "Get Started"
  cta_secondary: "Learn More"

features:
  enabled: false          # Set to true to show features section
  section_title: ""
  section_description: ""
  items: []
  # Example feature item:
  # - name: "Feature Name"
  #   description: "Feature description"
  #   icon: "Zap"         # Lucide icon name
```

### Design Preferences

```yaml
design_style: "minimal"   # Options: minimal, modern, playful, professional, elegant
border_radius: "0.5rem"   # Border radius for components
spacing: "standard"       # Options: compact, standard, spacious
```

### Assets

```yaml
# Logo files (place in public/assets/)
logo_svg: "logo.svg"
logo_png: "logo.png"
favicon: "logo.svg"

# Additional assets
hero_image: ""            # Optional hero image path
background_pattern: ""    # Optional background pattern
```

---

## Predefined Theme Presets

If using `theme_preset`, here are the available options:

### Ocean Theme
- **Colors**: Blues and teals
- **Vibe**: Professional, trustworthy, calm
- **Use Case**: SaaS, Business apps, Productivity tools

### Forest Theme
- **Colors**: Greens and earth tones
- **Vibe**: Natural, sustainable, growth
- **Use Case**: Environmental apps, Health & wellness, Education

### Sunset Theme
- **Colors**: Oranges, pinks, and warm tones
- **Vibe**: Creative, energetic, friendly
- **Use Case**: Creative tools, Social apps, Entertainment

### Midnight Theme
- **Colors**: Deep blues and purples
- **Vibe**: Sophisticated, premium, tech-forward
- **Use Case**: Developer tools, Analytics, Enterprise

### Coral Theme
- **Colors**: Coral, pink, and warm accents
- **Vibe**: Modern, friendly, approachable
- **Use Case**: E-commerce, Community, Social platforms

### Lavender Theme
- **Colors**: Purples and soft pastels
- **Vibe**: Elegant, creative, calming
- **Use Case**: Design tools, Wellness apps, Lifestyle

---

## Transformation Instructions

> **For LLM/Coding Agents**: Follow these steps to transform the baseline template

### Prerequisites

Before starting, ensure you have:
1. Access to the `frontend-template` directory
2. The theme specification filled out above
3. Ability to read, edit, and create files

### Step 1: Update Application Metadata

**Files to modify:**
- `src/app/layout.jsx`
- `src/components/layout/Header.jsx`
- `src/components/layout/Footer.jsx`
- `package.json`

**Actions:**
1. In `src/app/layout.jsx`:
   - Update `metadata.title` to `{app_name}`
   - Update `metadata.description` to `{app_description}`

2. In `src/components/layout/Header.jsx`:
   - Replace "Your App Name" with `{app_name}` (line 36)
   - Update `navItems` array with items from `{navigation_items}`
   - For each nav item, ensure the correct Lucide icon is imported and used

3. In `src/components/layout/Footer.jsx`:
   - Replace "Your App Name" with `{app_name}` (line 9)

4. In `package.json`:
   - Update `name` field to a kebab-case version of `{app_name}`

### Step 2: Apply Color Scheme

**Files to modify:**
- `src/app/globals.css`

**Actions:**

If using a **predefined theme preset**:
1. Look up the preset colors from the [Theme Preset Colors](#theme-preset-colors) section below
2. Apply those colors to the CSS variables

If using **custom colors**:
1. In `src/app/globals.css`, locate the `:root` section (around line 22)
2. Update the following CSS variables with light mode colors:
   ```css
   --primary: {light_primary};
   --background: {light_background};
   --foreground: {light_foreground};
   --accent: {light_accent};
   ```

3. Locate the `.dark` section (around line 74)
4. Update the following CSS variables with dark mode colors:
   ```css
   --primary: {dark_primary};
   --background: {dark_background};
   --foreground: {dark_foreground};
   --accent: {dark_accent};
   ```

5. If additional colors are specified (secondary, destructive), update those as well

### Step 3: Apply Typography

**Files to modify:**
- `src/app/layout.jsx` (if font CDN links are provided)
- `tailwind.config.js` (if custom fonts are specified)
- `src/app/globals.css`

**Actions:**

1. If `font_cdn` links are provided:
   - In `src/app/layout.jsx`, add `<link>` tags in the `<head>` section:
   ```jsx
   <link href="{font_cdn_url}" rel="stylesheet" />
   ```

2. If custom fonts are specified:
   - In `tailwind.config.js`, update the `theme.extend.fontFamily` section:
   ```javascript
   fontFamily: {
     sans: ['{body_font}'],
     heading: ['{heading_font}'],
     mono: ['{mono_font}']
   }
   ```

3. In `src/app/globals.css`:
   - Update the `body` font-family (line 14) if `body_font` is specified
   - Update `h1, h2, h3, h4, h5, h6` font-family (line 17) if `heading_font` is specified

### Step 4: Update Homepage Content

**Files to modify:**
- `src/app/page.jsx`

**Actions:**

1. Update the hero section:
   - Replace the `<h1>` text with `{hero.title}`
   - Replace the `<p>` text with `{hero.subtitle}`
   - Update button text to `{hero.cta_primary}` and `{hero.cta_secondary}`

2. If `features.enabled` is `true`:
   - Create a features array with the items from `{features.items}`
   - Import necessary Lucide icons for each feature
   - Replace the "Getting Started" card section with a features grid:
   ```jsx
   <section className="py-16 px-4 sm:px-6 lg:px-8">
       <div className="max-w-7xl mx-auto">
           <div className="text-center mb-12">
               <h2 className="text-3xl font-bold mb-4">{features.section_title}</h2>
               <p className="text-muted-foreground text-lg">
                   {features.section_description}
               </p>
           </div>
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
               {/* Feature cards */}
           </div>
       </div>
   </section>
   ```

3. If `features.enabled` is `false`:
   - Keep the existing "Getting Started" card but update text if provided

### Step 5: Apply Design Preferences

**Files to modify:**
- `src/app/globals.css`
- `tailwind.config.js`

**Actions:**

1. Update border radius in `src/app/globals.css`:
   - Change `--radius: 0.5rem;` to `--radius: {border_radius};`

2. If `spacing` is set to "compact" or "spacious":
   - In the homepage and components, adjust padding/margin values:
     - Compact: Reduce py-20 to py-12, py-16 to py-10, gap-6 to gap-4
     - Spacious: Increase py-20 to py-28, py-16 to py-20, gap-6 to gap-8

3. Apply design style adjustments:
   - **Minimal**: Keep clean lines, subtle shadows (current style)
   - **Modern**: Add subtle gradients, increase border radius
   - **Playful**: Increase border radius significantly, add more vibrant colors
   - **Professional**: Use more muted colors, increase whitespace
   - **Elegant**: Add subtle patterns, serif fonts, refined spacing

### Step 6: Update Assets

**Files to modify:**
- Files in `public/assets/`
- `src/app/layout.jsx`

**Actions:**

1. If custom logo files are specified:
   - Ensure `{logo_svg}`, `{logo_png}` are placed in `public/assets/`
   - Update favicon reference in `src/app/layout.jsx` to use `{favicon}`

2. If `hero_image` is provided:
   - Add the hero image to the homepage
   - Update `src/app/page.jsx` to include an image section

3. If `background_pattern` is provided:
   - Add background pattern CSS to `src/app/globals.css`

### Step 7: Create Missing Pages

**Actions:**

For each navigation item (except "Home"):
1. Create a directory: `src/app/{path}/`
2. Create a page file: `src/app/{path}/page.jsx`
3. Add basic page structure:
```jsx
'use client';

export default function {PageName}() {
    return (
        <div className="min-h-screen bg-background">
            <section className="relative py-20 px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl mx-auto">
                    <h1 className="text-4xl font-bold mb-6">{Page Title}</h1>
                    <p className="text-muted-foreground">
                        Content for {page name} goes here.
                    </p>
                </div>
            </section>
        </div>
    );
}
```

### Step 7: Validation Checklist

After transformation, verify:

- [ ] All file paths are correct
- [ ] No syntax errors in modified files
- [ ] All Lucide icons are properly imported
- [ ] Color values are in correct HSL format
- [ ] Font links are valid (if using custom fonts)
- [ ] Navigation links match created pages
- [ ] App name is consistent across all files
- [ ] Theme toggle still works
- [ ] Both light and dark modes look good
- [ ] Responsive design is maintained

## Theme Preset Colors

### Ocean Theme
```yaml
# Light Mode
primary: "199 89% 48%"      # Ocean blue
background: "0 0% 100%"
foreground: "200 20% 10%"
accent: "199 45% 95%"
secondary: "187 71% 45%"    # Teal

# Dark Mode
primary: "199 89% 58%"
background: "200 50% 8%"
foreground: "199 40% 95%"
accent: "200 40% 15%"
secondary: "187 71% 55%"
```

### Forest Theme
```yaml
# Light Mode
primary: "142 76% 36%"      # Forest green
background: "0 0% 100%"
foreground: "142 20% 15%"
accent: "142 45% 95%"
secondary: "84 65% 45%"     # Lime

# Dark Mode
primary: "142 76% 46%"
background: "142 30% 10%"
foreground: "142 40% 95%"
accent: "142 30% 15%"
secondary: "84 65% 55%"
```

### Sunset Theme
```yaml
# Light Mode
primary: "14 90% 53%"       # Sunset orange
background: "0 0% 100%"
foreground: "14 20% 15%"
accent: "14 60% 95%"
secondary: "340 82% 52%"    # Pink

# Dark Mode
primary: "14 90% 63%"
background: "14 30% 10%"
foreground: "14 40% 95%"
accent: "14 40% 15%"
secondary: "340 82% 62%"
```

### Midnight Theme
```yaml
# Light Mode
primary: "251 91% 60%"      # Deep purple
background: "0 0% 100%"
foreground: "251 20% 15%"
accent: "251 45% 95%"
secondary: "217 91% 60%"    # Blue

# Dark Mode
primary: "251 91% 65%"
background: "251 50% 8%"
foreground: "251 40% 95%"
accent: "251 40% 15%"
secondary: "217 91% 65%"
```

### Coral Theme
```yaml
# Light Mode
primary: "350 89% 60%"      # Coral
background: "0 0% 100%"
foreground: "350 20% 15%"
accent: "350 45% 95%"
secondary: "11 83% 61%"     # Peach

# Dark Mode
primary: "350 89% 65%"
background: "350 30% 10%"
foreground: "350 40% 95%"
accent: "350 30% 15%"
secondary: "11 83% 66%"
```

### Lavender Theme
```yaml
# Light Mode
primary: "270 70% 60%"      # Lavender
background: "0 0% 100%"
foreground: "270 20% 15%"
accent: "270 45% 95%"
secondary: "290 60% 65%"    # Purple

# Dark Mode
primary: "270 70% 65%"
background: "270 30% 10%"
foreground: "270 40% 95%"
accent: "270 30% 15%"
secondary: "290 60% 70%"
```

---
