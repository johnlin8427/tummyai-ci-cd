Use the following instructions for your coding agent. Fill in this section with your theme requirements. Be as specific as possible.

# Customizing Themes

The following are details of the app and the theme required for the app. Use these details along with Theme.md to modify the theme of this existing template app.

## Theme Specification

### Application Identity
```yaml
# Application Identity
app_name: "TummyAI"
app_description: "A gastrointestinal health assistant powered by AI"
tagline: "Smart food insights for a happier gut"
domain: "tummyai.me"

# Color Scheme
theme_preset: "forest"

# Typography
heading_font: "Poppins, sans-serif"
body_font: "Inter, sans-serif"
font_cdn:
  - "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
  - "https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap"

# Navigation
navigation_items:
  - name: "Home"
    path: "/"
    icon: "house"
  - name: "Meal History"
    path: "/history"
    icon: "calendar"
  - name: "Health Report"
    path: "/report"
    icon: "info"
  - name: "Chat Assistant"
    path: "/chat"
    icon: "bot"

# Design
design_style: "modern"
border_radius: "0.75rem"
spacing: "standard"
```

Use the instructions in Theme.md to apply the required changes for this app.

---

# Home Page / Landing Page

The following are detailed requirements for the home page / landing page. Use these details along with Component.md to implement the required components in the app.

## Home Page / Landing Page Requirements

### Overview
Create a modern, engaging landing page that allows users to upload photos of their meals and report symptoms.

### Page Sections

#### 1. Upload Section
This section allows the user to:
- Change the time
- Save the current entry
- Upload a photo of their meal
- Report symptoms

##### Save Entry Component
- Display the Save Entry Component as a full width component.
- Add a widget that allows the user to change the time of the meal.
- By default, use the current time.
- Also add a button that allows the user to save the current entry.
- When the user clicks on this button, save the photo and symptoms. Recent meals are displayed on the Meal History Page.
- This button should be aligned on the right.

##### Upload Meal Component
- Display the Upload Meal Component and Report Symptoms Component in a two column grid.
- Add a button that allows the user to upload a photo of their meal.
- Add a preview of the uploaded photo.
- Provide tips to help the user take better photos, such as:
  - Capture the entire meal.
  - Show every ingredient.
  - Use good lighting.
- After a photo is uploaded, call the /food-model/predict POST endpoint to analyze the photo, identify the dish, and generate a list of ingredients.
- Display the detected dish.
- Display the identified ingredients.
- When the user clicks on the Save Entry button, call the /meal-history PUT endpoint to update their meal history. See update_meal_history in meal_history.py. Also, call the /health-report PUT endpoint to update their health report. See update_health_report in health_report.py.
- If the user is new, call the /meal-history POST endpoint to create their meal history. You can find more details at the create_meal_history in meal_history.py. Also, call the /health-report POST endpoint to create their health report. See create_health_report in health_report.py.

##### Report Symptoms Component
- Add a questionnaire that allows the user to report symptoms.
- Instructions: Which of the following symptoms did you experience after this meal? Select all that apply.
- Symptoms (with abbreviated names) include:
  - Abdominal pain or cramps: cramps
  - Excess gas and bloating: bloating
  - Diarrhea: diarrhea
  - Constipation: constipation
  - Sensation of incomplete evacuation: fullness
  - Mucus in stool: mucus
- Use the full names for the symptoms in the questionnaire.
- Allow the user to select multiple options.

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
- Use Poppins for headings, Inter for body text

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
  - Fade-in on scroll (optional, use CSS)
  - Number counters for statistics (animated)

### Component Structure

Create components in `src/components/home/`:
- **UploadSection.jsx** - Main upload section

Update `src/app/page.jsx` to use these components instead of the current placeholder content.

### Functional Requirements

#### Responsive Design
- **Mobile** (< 640px): Single column layout, stacked elements
- **Tablet** (640px - 1024px): 2-column grid
- **Desktop** (> 1024px): 2-column grid

#### Animations (Optional)
- Fade-in animations for sections on scroll
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
- Professional yet friendly
- Action-oriented language
- Benefit-focused messaging
- Clear and concise

#### Messaging Hierarchy
1. **What**: Gastrointestinal health assistant
2. **Who**: For individuals
3. **Why**: Manage irritable bowel syndrome (IBS)
4. **How**: Tracking meals and symptoms
5. **Action**: Start using it now

### User Experience Goals
- Visitors should upload meals and report symptoms
- Key features should be quickly scannable
- Mobile-first, responsive experience
- Fast loading times with optimized assets

Use the instructions in Component.md to implement the required changes for this app.

---

# Meal History Page

The following are detailed requirements for the meal history page. Use these details along with Component.md to implement the required components in the app.

## Meal History Page Requirements

### Overview
Create a modern, engaging landing page that allows users to view their recent meals.

### Page Sections

#### 1. Recent Meals Section
Display recent meals as preview cards. Add a button in the top right corner that allows the user to switch between list and grid view.

##### View Meal History Component
- Display preview cards of recent meals.
- For each preview card, display:
  - Uploaded photo
  - Time and date
  - Detected dish
  - Identified ingredients
  - Abbreviated symptoms
- Allow the user to click on a preview card and open a popup with more detailed information.
- For the detailed popup, display:
  - Uploaded photo
  - Time and date
  - Detected dish
  - Identified ingredients
  - Symptoms
- Call the /meal-history GET endpoint to get details. See get_meal_history in meal_history.py.

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
- Use Poppins for headings, Inter for body text

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
  - Fade-in on scroll (optional, use CSS)
  - Number counters for statistics (animated)

### Component Structure

Create components in `src/components/history/`:
- **RecentMealsSection.jsx** - Meal history section

Update `src/app/page.jsx` to use these components instead of the current placeholder content.

### Functional Requirements

#### Responsive Design
- **Mobile** (< 640px): Single column layout, stacked elements
- **Tablet** (640px - 1024px): 2-column grid
- **Desktop** (> 1024px): 2-column grid

#### Animations (Optional)
- Fade-in animations for sections on scroll
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
- Professional yet friendly
- Action-oriented language
- Benefit-focused messaging
- Clear and concise

#### Messaging Hierarchy
1. **What**: Gastrointestinal health assistant
2. **Who**: For individuals
3. **Why**: Manage irritable bowel syndrome (IBS)
4. **How**: Tracking meals and symptoms
5. **Action**: Start using it now

### User Experience Goals
- Visitors should view their recent meals
- Key features should be quickly scannable
- Mobile-first, responsive experience
- Fast loading times with optimized assets

Use the instructions in Component.md to implement the required changes for this app.

---

## Health Report Page Requirements

The following are detailed requirements for the health report page. Use these details along with Component.md to implement the required components in the app.

## Health Report Page Requirements

### Overview
Create a modern, engaging health report page that allows users to view their personalized insights

### Page Sections

#### 1. Foods to Watch Section

##### View Health Report Component
- Call the /health-report GET endpoint to get details. See get_health_report in health_report.py.
- Display the results.

#### 2. Symptom Trends Section

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
- Use Poppins for headings, Inter for body text

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
  - Fade-in on scroll (optional, use CSS)
  - Number counters for statistics (animated)

### Component Structure

Create components in `src/components/history/`:
- **RecentMealsSection.jsx** - Meal history section

Update `src/app/page.jsx` to use these components instead of the current placeholder content.

### Functional Requirements

#### Responsive Design
- **Mobile** (< 640px): Single column layout, stacked elements
- **Tablet** (640px - 1024px): 2-column grid
- **Desktop** (> 1024px): 2-column grid

#### Animations (Optional)
- Fade-in animations for sections on scroll
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
- Professional yet friendly
- Action-oriented language
- Benefit-focused messaging
- Clear and concise

#### Messaging Hierarchy
1. **What**: Gastrointestinal health assistant
2. **Who**: For individuals
3. **Why**: Manage irritable bowel syndrome (IBS)
4. **How**: Tracking meals and symptoms
5. **Action**: Start using it now

### User Experience Goals
- Visitors should view their recent meals
- Key features should be quickly scannable
- Mobile-first, responsive experience
- Fast loading times with optimized assets

Use the instructions in Component.md to implement the required changes for this app.

---

## Chat Assistant Page Requirements

#### 1. Chat Assistant Section

---
