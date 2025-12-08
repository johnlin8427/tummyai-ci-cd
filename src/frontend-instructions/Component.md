# Component - Guidelines

This document provides high-level requirements and implementation guidelines for building an advanced task tracking component for TaskFlow Pro. These instructions are designed for LLM/coding agents to understand what to build and how to follow the template patterns.

---

## Design Specifications

### Visual Design Guidelines
Follow the existing Ocean theme established in the template:

**Color Coding**:
- **Status Colors**:
  - To Do: Gray/muted
  - In Progress: Primary blue
  - Review: Yellow/warning
  - Done: Green/success

- **Priority Colors**:
  - Low: Gray
  - Medium: Blue
  - High: Orange
  - Urgent: Red

**Typography**:
- Headings: Poppins font (already configured)
- Body text: Inter font (already configured)

**Component Styling**:
- Use Ocean theme CSS variables from `globals.css`
- Match existing border radius: 0.75rem
- Follow modern design style with clean lines
- Use consistent spacing and padding

### Required UI Components
Find the required shadcn/ui components (if not already present) and ask to be install

### Component Hierarchy
Come up with a component hierarchy as appropriate for implementing this requirement.

---

## Implementation Guidelines

### Step 1: Create Route Page First
**Following template pattern**: Always create the page route before components

**Create**: `src/app/<feature-name>/page.jsx`
- Replace `<feature-name>` with your component's route name (e.g., `tasks`, `products`, `users`)
- Keep it minimal - just import and render the main component
- Use `'use client'` directive for client-side features
- Follow the pattern used in `src/app/page.jsx`

### Step 2: Create Component Structure
**Following template pattern**: Organize components in feature folders

**Create directory**: `src/components/<feature-name>/`
- Replace `<feature-name>` with your component's folder name

**Create component files**:
Come up with a list of files that would be required to implement this requirement.

### Step 3: Create Data Service Layer
**Following template pattern**: Separate data logic from UI components

**Update**: `src/lib/DataService.js`

This service should handle:
- CRUD operations (Create, Read, Update, Delete)
- localStorage management
- Filter and sort logic
- Statistics calculations
- Export/import functionality


### Step 4: Component Implementation Pattern
**Following template pattern**: Use consistent component structure

Each component should follow this pattern (see existing components):
```jsx
'use client';

// Imports
import { useState } from 'react';
// Import UI components
// Import icons from lucide-react

export default function ComponentName({ props }) {
    // Component States
    const [state, setState] = useState(initialValue);

    // Handlers
    const handleAction = () => {
        // Handle user actions
    };

    // UI View
    return (
        <div>
            {/* Component JSX */}
        </div>
    );
}
```

### Step 5: State Management
Come up with a plan for state management and implement state management

### Step 6: Styling Guidelines
**Follow existing theme patterns**:

- Use Tailwind CSS classes (like other components)
- Reference CSS variables from `globals.css`:
  - `bg-background`, `text-foreground`
  - `bg-primary`, `text-primary`
  - `bg-card`, `border`
  - `bg-muted`, `text-muted-foreground`

- Add custom utility classes to `globals.css` if needed for your specific component requirements

### Step 7: Icons Usage
**Following template pattern**: Use Lucide React icons

Import icons appropriate for your component from `lucide-react`.

Common icons include:
- Plus (add/create)
- Edit (edit/modify)
- Trash2 (delete)
- Search (search)
- Filter (filters)
- Check (complete/confirm)
- X (close/cancel)
- Calendar (dates)
- ChevronDown/ChevronUp (expand/collapse)
- MoreVertical (actions menu)
- Save (save)
- Download/Upload (export/import)

**Pattern**: See how icons are used in `Header.jsx` and other components

### Step 8: Form Handling
**For create/edit form components**:
- Use controlled inputs (useState for form fields)
- Implement validation before submit
- Show error messages below invalid fields
- Disable submit button when form is invalid
- Clear form after successful submit
- Handle both create and edit modes

### Step 9: Responsive Design
**Following template pattern**: Mobile-first responsive

- Use Tailwind responsive classes:
  - `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
  - `hidden md:flex`
  - `flex-col md:flex-row`

- Test on mobile, tablet, and desktop
- Stack elements vertically on mobile
- Hide secondary info on small screens
- Make dialogs full-screen on mobile

### Step 10: Empty States
**Following template pattern**: Helpful empty states

When no items exist, show:
- Icon (centered, relevant to your feature)
- Heading (e.g., "No [items] yet")
- Description (e.g., "Get started by creating your first [item]")
- Primary action button (e.g., "Create [Item]")

Replace `[items]` and `[item]` with your feature's terminology (e.g., tasks, products, users, posts)

**Pattern**: Similar to how other pages handle empty states

### Step 11: Update Navigation
**Following template pattern**: Add to header navigation

**Update**: `src/components/layout/Header.jsx`

Add your feature to the `navItems` array:
```javascript
{ name: '[Feature Name]', path: '/[route]', icon: <[IconName] /> }
```

Example:
- For tasks: `{ name: 'Tasks', path: '/tasks', icon: <CheckSquare /> }`
- For products: `{ name: 'Products', path: '/products', icon: <Package /> }`

Don't forget to import the icon from `lucide-react`

---

## Key Principles to Follow

### 1. Match Existing Patterns
- Study existing components in `src/components/`
- Follow the same file structure
- Use the same naming conventions
- Mirror the code organization pattern

### 2. Use Template Theme
- Reference `src/app/globals.css` for colors
- Use CSS variables, not hardcoded colors
- Maintain consistency with existing pages
- Support both light and dark modes

### 3. Leverage Existing UI Components
- Use components from `src/components/ui/`
- Import Button, Card, Input, etc. that already exist
- Add new shadcn components only when needed
- Don't recreate what's already available

### 4. Keep It Simple
- Start with basic functionality
- Progressive enhancement
- Don't over-engineer
- Focus on user experience

### 5. Mobile-First Approach
- Design for mobile first
- Add desktop enhancements
- Test on all screen sizes
- Ensure touch-friendly interactions

### 6. General Implementation Principles
- Always use JSX for coding
- Do not perform linting or run tests. This will be done by the user externally
- Do not perform any npm or npx installs. Ask the user to perform for you
- Do not run `npm run dev` as the user is already running this externally and testing the app from outside.
---

## Tips for Success

1. **Start Small**: Implement the simplest view first, then progressively add more complex features
2. **Test Incrementally**: Test each component as you build it
3. **Reuse Code**: Look for patterns in existing components to reuse
4. **Stay Consistent**: Match the style and structure of the template
5. **Ask Questions**: If requirements are unclear, ask for clarification

---
