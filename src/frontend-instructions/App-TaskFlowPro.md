Use the following instructions for your coding agent. Fill in this section with your theme requirements. Be as specific as possible.

# Customizing Themes

The following are details of the app and the theme required for the app. Use these details along with Theme.md to modify the theme of this existing template app.

## Theme Specification

### Application Identity
```yaml
# Application Identity
app_name: "TaskFlow Pro"
app_description: "A powerful task management application for teams"
tagline: "Organize. Collaborate. Succeed."
domain: "taskflow.pro"

# Color Scheme
theme_preset: "ocean"  # Using Ocean theme

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
    icon: "Home"

# Homepage Content
hero:
  title: "Manage Your Tasks with Ease"
  subtitle: "TaskFlow Pro helps teams collaborate and stay organized with powerful task management tools."
  cta_primary: "Start Free Trial"
  cta_secondary: "See How It Works"

# Design
design_style: "modern"
border_radius: "0.75rem"
spacing: "standard"
```

Use the instructions in Theme.md to apply the required changes for this app.

---

# Example Component: Task Tracking

The following are detailed requirements of new components in the app. Use these details along with Component.md to implement the required components in the app.

## Task Tracking Component Requirements

### Overview
Create an advanced task tracking component that allows users to create, view, edit, and manage tasks with rich features including status tracking, priority levels, due dates, and filtering capabilities.

### Functional Requirements

#### Task Management Features
- Create new tasks with multiple fields
- Edit existing tasks
- Delete tasks (with confirmation)
- Mark tasks as complete/incomplete
- View task details in expanded view

#### Task Data Model
Each task should include:
- **ID**: Unique identifier (auto-generated)
- **Title**: Task name (required, max 100 characters)
- **Description**: Detailed description (optional)
- **Status**: One of [To Do, In Progress, Review, Done]
- **Priority**: One of [Low, Medium, High, Urgent]
- **Due Date**: Target completion date (optional)
- **Created Date**: Auto-generated timestamp
- **Updated Date**: Auto-updated timestamp
- **Tags**: Array of tags (optional)

#### Filtering & Sorting
- Filter by status (all, to do, in progress, review, done)
- Filter by priority (all, low, medium, high, urgent)
- Search across title and description
- Sort by: due date, priority, created date, alphabetical

#### View Modes
- **List View**: Compact list showing key information
- **Card View**: Grid of cards with more details
- **Board View**: Kanban-style board organized by status columns

#### Statistics Dashboard
Show summary statistics:
- Total tasks count
- Tasks by status breakdown
- Tasks by priority breakdown
- Completion rate percentage
- Overdue tasks count

#### Data Persistence
- Store tasks in browser localStorage
- Auto-save on any change
- Provide export/import functionality (JSON format)

#### User Experience
- Responsive design (mobile, tablet, desktop)
- Empty states when no tasks exist
- Loading states for async operations
- Form validation with error messages
- Confirmation dialogs for destructive actions

Use the instructions in Component.md to implement the required changes for this app.
---

# Example Component: Home Page / Landing Page

The following are detailed requirements for the home page / landing page. Use these details along with Component.md to implement the required components in the app.

## Home Page / Landing Page Requirements

### Overview
Create a modern, engaging landing page that introduces TaskFlow Pro to new visitors, highlights key features, demonstrates value propositions, and drives user engagement through clear calls-to-action.

### Page Sections

#### 1. Hero Section
- **Headline**: Bold, attention-grabbing main heading
  - Text: "Master Your Tasks, Amplify Your Productivity"
  - Subheading: "TaskFlow Pro is the all-in-one task management solution trusted by teams worldwide to stay organized and achieve their goals."
- **Call-to-Action Buttons**:
  - Primary: "Get Started Free" (navigate to /tasks)
  - Secondary: "Watch Demo" (scroll to features section)
- **Hero Visual**:
  - Animated mockup or illustration showing the task board
  - Use Ocean theme colors for consistency
- **Design**:
  - Full-width section with gradient background
  - Centered content with max-width container
  - Responsive layout (stack on mobile)

#### 2. Features Section
Highlight the core features with icon cards in a 3-column grid:

**Feature 1: Multiple View Modes**
- Icon: LayoutGrid icon
- Title: "Flexible Views"
- Description: "Switch seamlessly between List, Card, and Kanban Board views to match your workflow preference."

**Feature 2: Smart Filtering**
- Icon: Filter icon
- Title: "Advanced Filtering"
- Description: "Find tasks instantly with powerful filters by status, priority, date, and custom search."

**Feature 3: Real-time Statistics**
- Icon: BarChart3 icon
- Title: "Analytics Dashboard"
- Description: "Track your progress with real-time statistics, completion rates, and overdue task alerts."

**Feature 4: Priority Management**
- Icon: AlertCircle icon
- Title: "Priority Levels"
- Description: "Organize tasks by urgency with four priority levels: Low, Medium, High, and Urgent."

**Feature 5: Due Date Tracking**
- Icon: Calendar icon
- Title: "Deadline Management"
- Description: "Never miss a deadline with due date tracking and automatic overdue notifications."

**Feature 6: Data Export/Import**
- Icon: Download icon
- Title: "Backup & Sync"
- Description: "Export and import your tasks in JSON format for easy backup and data portability."

#### 3. How It Works Section
Step-by-step visual guide (3 steps in a horizontal timeline):

**Step 1: Create Tasks**
- Icon: Plus icon
- Title: "Create & Organize"
- Description: "Quickly add tasks with titles, descriptions, tags, and due dates."

**Step 2: Track Progress**
- Icon: TrendingUp icon
- Title: "Monitor Progress"
- Description: "Move tasks through workflows: To Do → In Progress → Review → Done."

**Step 3: Achieve Goals**
- Icon: CheckCircle icon
- Title: "Complete & Celebrate"
- Description: "Watch your completion rate grow as you accomplish your objectives."

#### 4. Statistics Showcase Section
Display impressive metrics in a visually appealing way:
- **Dynamic Counter Cards** (4 cards):
  - "10,000+ Tasks Completed" with CheckCircle icon
  - "500+ Active Users" with Users icon
  - "95% Satisfaction Rate" with Star icon
  - "24/7 Available" with Clock icon

#### 5. Testimonials Section (Optional)
- 2-3 testimonial cards with:
  - User avatar (placeholder)
  - Quote text
  - User name and role
  - Star rating

Sample testimonial:
> "TaskFlow Pro transformed how our team manages projects. The Kanban board view is a game-changer!"
> — Sarah Chen, Product Manager

#### 6. Call-to-Action Banner
- **Background**: Gradient with Ocean theme colors
- **Headline**: "Ready to Take Control of Your Tasks?"
- **Subtext**: "Join thousands of productive individuals and teams using TaskFlow Pro"
- **Button**: "Start Managing Tasks Now" (navigate to /tasks)

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
- Use Poppins for headings, Inter for body text

#### Color Palette (Ocean Theme)
- **Background**: Use gradient backgrounds for hero and CTA sections
- **Accent Colors**: Primary blue (#0EA5E9) for CTAs and highlights
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
- **HeroSection.jsx** - Main hero section
- **FeaturesSection.jsx** - Feature cards grid
- **HowItWorksSection.jsx** - Step-by-step guide
- **StatsSection.jsx** - Statistics showcase
- **TestimonialsSection.jsx** - User testimonials (optional)
- **CTABanner.jsx** - Final call-to-action

Update `src/app/page.jsx` to use these components instead of the current placeholder content.

### Functional Requirements

#### Navigation
- "Get Started Free" buttons should navigate to `/tasks`
- "Watch Demo" should smooth scroll to features section
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
- Professional yet friendly
- Action-oriented language
- Benefit-focused messaging
- Clear and concise

#### Messaging Hierarchy
1. **What**: Task management solution
2. **Who**: For individuals and teams
3. **Why**: Boost productivity and organization
4. **How**: Multiple views, filtering, tracking
5. **Action**: Start using it now

### User Experience Goals
- Visitors should immediately understand what TaskFlow Pro does
- Key features should be quickly scannable
- Multiple conversion points (CTAs) throughout the page
- Mobile-first, responsive experience
- Fast loading times with optimized assets

Use the instructions in Component.md to implement the required changes for this app.
---
