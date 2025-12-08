Use the following instructions for your coding agent. Fill in this section with your theme requirements. Be as specific as possible.

# Customizing Themes

The following are details of the app and the theme required for the app. Use these details along with Theme.md to modify the theme of this existing template app.

## Theme Specification

### Application Identity
```yaml
# Application Identity
app_name: "AgentChat"
app_description: "An intelligent AI chat assistant with multi-model support and conversation history"
tagline: "Your AI Companion for Every Question"
domain: "agentchat.ai"

# Color Scheme
theme_preset: "sunset"  # Using Sunset theme for a warm, engaging feel

# Typography
heading_font: "Space Grotesk, sans-serif"
body_font: "Inter, sans-serif"
font_cdn:
  - "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
  - "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap"

# Navigation
navigation_items:
  - name: "Home"
    path: "/"
    icon: "Home"
  - name: "Chat"
    path: "/chat"
    icon: "MessageSquare"

# Homepage Content
hero:
  title: "Intelligent AI Conversations"
  subtitle: "Experience the power of advanced AI with AgentChat - your intelligent assistant for any task, question, or creative challenge."
  cta_primary: "Start Chatting"
  cta_secondary: "Explore Features"

# Design
design_style: "modern"
border_radius: "0.75rem"
spacing: "standard"
```

Use the instructions in Theme.md to apply the required changes for this app.

---

# Component: AI Chat Interface

The following are detailed requirements of new components in the app. Use these details along with Component.md to implement the required components in the app.

## AI Chat Interface Component Requirements

### Overview
Create a comprehensive AI chat application that allows users to interact with multiple AI models, manage conversation history, support image uploads, and maintain persistent chat sessions. The interface features a dual-mode display: a hero landing view for new conversations and a sidebar layout for active chats.

### Dependencies to Install

Before implementing the component, install the required dependencies:

```bash
npm install react-markdown remark-gfm rehype-raw
```

These dependencies enable markdown rendering for AI responses with support for GitHub Flavored Markdown and raw HTML.

### Functional Requirements

#### Chat Data Model

**Chat Object:**
- **chat_id**: Unique identifier for the conversation (UUID)
- **title**: Chat title (auto-generated from first message, max 50 characters)
- **dts**: Timestamp of chat creation
- **messages**: Array of message objects

**Message Object:**
Each message should include:
- **message_id**: Unique identifier (UUID)
- **role**: One of ['user', 'assistant', 'cnn']
- **content**: Message text content (required)
- **image**: Base64 encoded image data (optional)
- **image_path**: Server path to image (optional)
- **results**: Object containing AI model results (optional)
  - prediction_label: Classification result
  - accuracy: Confidence percentage
- **timestamp**: Message timestamp (ISO format)

#### Data Service Integration

The component should use the existing DataService from `@/lib/DataService` with the following methods:

**Chat Methods:**
- **GetChats(model, limit)**: Fetches recent chat history
  - Parameters:
    - model: Selected AI model type
    - limit: Maximum number of chats to return
  - Returns: Promise resolving to `{ data: Chat[] }`

- **GetChat(model, chat_id)**: Fetches a specific chat by ID
  - Parameters:
    - model: Selected AI model type
    - chat_id: Unique chat identifier
  - Returns: Promise resolving to `{ data: Chat }`

- **StartChatWithLLM(model, message)**: Initiates a new chat conversation
  - Parameters:
    - model: Selected AI model type
    - message: Object containing { content: string, image: string }
  - Returns: Promise resolving to `{ data: Chat }` with chat_id and initial messages

- **ContinueChatWithLLM(model, chat_id, message)**: Appends message to existing chat
  - Parameters:
    - model: Selected AI model type
    - chat_id: Existing chat identifier
    - message: Object containing { content: string, image: string }
  - Returns: Promise resolving to `{ data: Chat }` with updated messages

- **GetChatMessageImage(model, image_path)**: Retrieves image URL from path
  - Parameters:
    - model: Selected AI model type
    - image_path: Server path to image
  - Returns: String URL to image

#### AI Model Support

The application supports multiple AI models selectable via dropdown:
- **llm**: AI Assistant (LLM) - Standard language model
- **llm-cnn**: AI Assistant (LLM + CNN) - Language model with image classification
- **llm-rag**: AI Expert (RAG) - Retrieval-Augmented Generation
- **llm-agent**: AI Expert (Agent) - Agentic AI with tool use

**Model Selection:**
- Display model selector in chat input component
- Allow model change before starting new chat
- Disable model changes during active conversation
- Store model preference in URL query parameters
- Update route when model changes

#### Chat Page Layout

**Two Display Modes:**

1. **Hero Mode (No Active Chat):**
   - Display when no chat is selected (no chat_id in URL)
   - Full-screen hero section with gradient background
   - Centered chat input with prominent heading "AI Assistant 🌟"
   - Chat history grid displayed below hero section
   - Responsive padding and spacing

2. **Conversation Mode (Active Chat):**
   - Display when chat_id is present in URL
   - Three-panel layout:
     - **Left Sidebar (280px width)**: Chat history sidebar with scrollable list
     - **Center Panel (flex-1)**: Active chat messages with auto-scroll
     - **Bottom Input**: Fixed chat input bar at bottom of center panel
   - Fixed height layout (100vh - 64px for header)

#### Chat Input Component

**Features:**
- Auto-expanding textarea (min 56px, max 400px height)
- Image upload with preview
  - Camera icon button to trigger file input
  - Accepts image/* formats
  - 5MB file size limit with validation
  - Preview thumbnail (200x200px max, rounded)
  - Remove button (× in top-right corner)
  - Convert to base64 for message submission
- Send button (paper airplane icon)
  - Disabled when no message and no image
  - Visual feedback (opacity, cursor changes)
  - Enabled with primary color when content present
- Model selector dropdown
  - Display current model
  - 4 model options as specified above
  - Disable during active conversation
- Keyboard shortcuts:
  - **Enter**: Submit message
  - **Shift + Enter**: New line in textarea
- Helper text: "Use shift + return for new line"

**Component Props:**
- `onSendMessage`: Callback function when message submitted
- `selectedModel`: Currently selected AI model
- `onModelChange`: Callback when model selection changes
- `disableModelSelect`: Boolean to disable model dropdown (default: false)
- `chat`: Optional current chat object for context

**Styling:**
- Glassmorphic card design with backdrop blur
- Elevated shadow and border
- Padding: p-6
- Responsive layout with flex containers
- Primary color accent for active states

#### Chat Message Display Component

**Message Rendering:**
- Scrollable message container with auto-scroll to bottom
- Each message displays:
  - Avatar icon (User, Bot, or Eye for CNN)
  - Role-specific styling:
    - **User messages**: Primary background, right-aligned, white text
    - **Assistant messages**: Card background, left-aligned, border
    - **CNN messages**: Pink accent for vision model results
  - Message content with markdown support:
    - Use ReactMarkdown component
    - Enable remarkGfm plugin for tables, strikethrough, task lists
    - Enable rehypeRaw for HTML support
    - Apply prose classes for typography
    - Invert prose colors for user messages
  - Image display (if present):
    - Show uploaded image or server image
    - Max width: md (448px)
    - Rounded corners
  - Classification results (if present):
    - Display prediction label and accuracy percentage
  - Timestamp (if present):
    - Format: HH:MM AM/PM
    - Small, semi-transparent text

**Chat Header:**
- Display chat title from chat object
- MessageSquare icon
- Border bottom separator
- Fixed position at top of message area

**Typing Indicator:**
- Show when `isTyping` prop is true
- Three animated dots (bounce animation with staggered delay)
- Centered below last message

**Component Props:**
- `chat`: Chat object with messages array
- `isTyping`: Boolean for typing indicator
- `model`: Current AI model for image URL construction

**Auto-scroll Behavior:**
- Use useRef for chat container
- useEffect hook to scroll on chat/typing changes
- Smooth scroll to bottom of messages

#### Chat History Component

**Display:**
- Grid layout for recent chats:
  - 1 column on mobile (< 768px)
  - 2 columns on tablet (768px - 1024px)
  - 3 columns on desktop (> 1024px)
- Each chat card shows:
  - Chat title (truncated to 2 lines with ellipsis)
  - Relative timestamp (e.g., "2 hours ago", "Yesterday")
  - Hover effect: shadow increase
  - Click: Navigate to chat detail
- Header section:
  - "Your recent chats" heading with History icon
  - "View all" button (right-aligned)
  - Flex layout with space-between

**Component Props:**
- `model`: Current AI model for filtering

**Data Loading:**
- Fetch on component mount using useEffect
- Call DataService.GetChats(model, 20)
- Handle loading and error states
- Display empty array on error

**Navigation:**
- Use Next.js Link component for client-side routing
- Route format: `/chat?model={model}&id={chat_id}`
- Preserve model parameter in navigation

#### Chat History Sidebar Component

**Layout:**
- Fixed width: 280px
- Full height with scroll
- Border-right separator
- Card background

**Header Section:**
- "Chat History" heading with History icon
- "New Chat" button:
  - Primary background
  - Plus icon
  - Navigate to `/chat?model={model}` (no id)
- Flexbox layout with space-between
- Muted background with border-bottom

**Chat List:**
- Scrollable list of recent chats
- Each item displays:
  - Chat title (truncated to 2 lines)
  - Relative timestamp
  - Border-bottom separator
  - Click: Navigate to chat
- Active chat highlighting:
  - Compare current chat_id with prop
  - Apply accent background for active
  - Hover: muted background for others

**Component Props:**
- `chat_id`: Current active chat ID
- `model`: Current AI model

**Data Loading:**
- Fetch chats on mount
- Call DataService.GetChats(model, 20)
- Handle loading and error states

#### Chat Page (Main Route)

**Route:** `/app/chat/page.jsx`

**URL Parameters:**
- `model`: Selected AI model (default: 'llm')
- `id`: Optional chat_id for loading specific chat

**Component State:**
- `chatId`: Current chat identifier
- `hasActiveChat`: Boolean flag for display mode
- `chat`: Current chat object with messages
- `refreshKey`: Force re-render trigger
- `isTyping`: Typing indicator state
- `selectedModel`: Current AI model

**Initialization (useEffect):**
- Parse URL parameters using Next.js `searchParams`
- If chat_id present:
  - Fetch chat data via DataService.GetChat()
  - Set hasActiveChat to true
  - Display conversation mode
- If no chat_id:
  - Clear chat state
  - Set hasActiveChat to false
  - Display hero mode

**Handler Functions:**

1. **newChat(message):**
   - Called when starting new conversation
   - Show typing indicator
   - Create temporary chat with user message for immediate feedback
   - Call DataService.StartChatWithLLM(model, message)
   - Update state with returned chat
   - Navigate to `/chat?model={model}&id={chat_id}`
   - Handle errors: clear state, remove typing indicator

2. **appendChat(message):**
   - Called when continuing conversation
   - Show typing indicator
   - Update temporary UI with user message
   - Call DataService.ContinueChatWithLLM(model, chat_id, message)
   - Update state with returned chat
   - Force refresh of message display
   - Handle errors: clear typing indicator

3. **handleModelChange(newValue):**
   - Update selectedModel state
   - Construct new path with model parameter
   - Preserve chat_id if present
   - Navigate to new path using router.push()

4. **forceRefresh():**
   - Increment refreshKey state
   - Triggers re-render of ChatMessage component

**Component Structure:**
```jsx
<div className="h-screen flex flex-col">
  {!hasActiveChat ? (
    <>
      {/* Hero Section */}
      <section className="hero-with-gradient">
        <ChatInput
          onSendMessage={newChat}
          selectedModel={selectedModel}
          onModelChange={handleModelChange}
        />
      </section>

      {/* Chat History Grid */}
      <ChatHistory model={model} />
    </>
  ) : (
    <div className="flex h-[calc(100vh-64px)]">
      {/* Sidebar */}
      <ChatHistorySidebar chat_id={chat_id} model={model} />

      {/* Main Chat */}
      <div className="flex-1 flex flex-col">
        <ChatMessage
          chat={chat}
          isTyping={isTyping}
          model={model}
          key={refreshKey}
        />
        <ChatInput
          onSendMessage={appendChat}
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
          disableModelSelect={true}
        />
      </div>
    </div>
  )}
</div>
```

### Component Structure

Create the following files:

**1. `src/app/chat/page.jsx`** - Main chat route page
- Client component ('use client' directive)
- Import all chat components
- Handle URL parameters and routing
- Manage application state
- Implement handler functions
- Conditional rendering for two modes

**2. `src/components/chat/ChatInput.jsx`** - Message input component
- Client component
- Controlled textarea with auto-resize
- Image upload and preview
- Model selector dropdown
- Send button with validation
- Keyboard event handling

**3. `src/components/chat/ChatMessage.jsx`** - Message display component
- Client component
- Scrollable message container
- Markdown rendering with ReactMarkdown
- Role-based message styling
- Image display support
- Typing indicator animation
- Auto-scroll to bottom

**4. `src/components/chat/ChatHistory.jsx`** - History grid component
- Client component
- Responsive grid layout
- Chat card components
- Relative time formatting
- Navigation handling

**5. `src/components/chat/ChatHistorySidebar.jsx`** - History sidebar component
- Client component
- Scrollable chat list
- Active chat highlighting
- New chat button
- Navigation handling

### Styling & Responsive Design

#### Layout Breakpoints
- **Mobile** (< 640px): Single column, full-width elements
- **Tablet** (640px - 1024px): 2-column grids where applicable
- **Desktop** (> 1024px): 3-column grids, full sidebar layout

#### Color Scheme (Sunset Theme)
- **Primary**: Warm orange/coral tones for CTAs and accents
- **Background**: Gradient backgrounds for hero sections
- **Cards**: bg-card with border for containers
- **Text**: foreground for primary, muted-foreground for secondary
- **Accents**: primary/10 for subtle backgrounds

#### Typography
- **Page Title**: text-4xl to text-6xl, font-bold, gradient-text
- **Section Headings**: text-lg to text-xl, font-semibold
- **Message Content**: text-sm to text-base
- **Helper Text**: text-xs to text-sm, muted-foreground
- Use Space Grotesk for headings, Inter for body text

#### Icons (from lucide-react)
- **User**: User profile for user messages
- **Bot**: AI assistant for bot messages
- **Eye**: Vision model for CNN messages
- **MessageSquare**: Chat/conversation indicator
- **History**: Chat history sections
- **Send**: Submit message button
- **Camera**: Image upload button
- **Plus**: New chat creation

#### Animations
- **Typing Indicator**:
  - Three dots with bounce animation
  - Staggered delay: 0s, 0.2s, 0.4s
  - Smooth transition
- **Auto-scroll**:
  - Smooth scroll behavior
  - Trigger on message changes
- **Hover Effects**:
  - Shadow increase on cards
  - Background color transitions
  - Scale transform for buttons

#### Glassmorphism Effects
- backdrop-blur-lg for input containers
- bg-card/80 for semi-transparent backgrounds
- Shadow-lg for depth
- Border for definition

### User Experience Features

#### Loading States
- Display typing indicator while waiting for AI response
- Temporary message display for immediate feedback
- Smooth transitions between states

#### Error Handling
- Try-catch blocks for all async operations
- Console error logging for debugging
- Graceful fallback: clear state and return to hero mode
- User feedback for failed operations

#### Empty States
- Hero mode displayed when no active chat
- Empty chat history shows empty grid
- Handle missing chat gracefully

#### Keyboard Shortcuts
- **Enter**: Submit message (prevent default)
- **Shift + Enter**: New line in textarea (default behavior)

#### Image Handling
- File size validation (5MB limit)
- File type validation (images only)
- Preview before sending
- Easy removal of selected image
- Base64 encoding for transmission
- Server path handling for received images

#### URL State Management
- Model parameter in URL for bookmarking
- Chat ID parameter for direct chat access
- URL updates on navigation
- Deep linking support

#### Auto-scroll Behavior
- Scroll to bottom on new messages
- Scroll to bottom when typing indicator appears
- Maintain scroll position during typing
- Smooth scroll animation

### Accessibility

- Semantic HTML elements for structure
- Proper ARIA labels for buttons and inputs
- Alt text for images where applicable
- Keyboard navigation support
- Sufficient color contrast ratios
- Focus indicators on interactive elements
- Screen reader friendly text

### Performance Considerations

- Lazy loading of chat history
- Limit history fetch to 20 recent chats
- Efficient re-renders using keys
- Memoization of expensive computations
- Optimized image sizes
- Dynamic imports where beneficial
- Debounced textarea resize

### Message Formatting

#### Markdown Support
The chat supports full markdown rendering with the following features:
- **Headings**: # H1 through ###### H6
- **Bold**: **text** or __text__
- **Italic**: *text* or _text_
- **Lists**: Ordered and unordered
- **Code blocks**: ```language and inline `code`
- **Links**: [text](url)
- **Images**: ![alt](url)
- **Tables**: GitHub Flavored Markdown tables
- **Strikethrough**: ~~text~~
- **Task lists**: - [ ] and - [x]
- **Blockquotes**: > quote
- **Horizontal rules**: ---

#### Prose Styling
- Apply Tailwind prose classes for beautiful typography
- Dark mode support with prose-invert
- Max-width: none for full container width
- Custom styling for code blocks
- Syntax highlighting support

### Testing Scenarios

1. **New Chat Creation**:
   - Start chat from hero mode
   - Verify message submission
   - Check chat_id generation
   - Confirm navigation to chat

2. **Chat Continuation**:
   - Load existing chat
   - Send multiple messages
   - Verify message ordering
   - Check auto-scroll behavior

3. **Model Switching**:
   - Change model in hero mode
   - Verify URL updates
   - Confirm model preserved in navigation
   - Test disabled state during chat

4. **Image Upload**:
   - Select image file
   - Verify preview display
   - Test file size validation
   - Send message with image
   - Remove image before sending

5. **Chat History**:
   - Load history grid
   - Navigate to specific chat
   - Create new chat from sidebar
   - Verify active chat highlighting

6. **Responsive Layout**:
   - Test mobile viewport
   - Test tablet viewport
   - Test desktop viewport
   - Verify layout switches

7. **Markdown Rendering**:
   - Send messages with various markdown
   - Test code blocks
   - Test tables and lists
   - Verify proper styling

8. **Error Handling**:
   - Simulate API failures
   - Verify error states
   - Test recovery behavior

Use the instructions in Component.md to implement the required changes for this app.
---

# Component: Home Page / Landing Page

The following are detailed requirements for the home page / landing page. Use these details along with Component.md to implement the required components in the app.

## Home Page / Landing Page Requirements

### Overview
Create an engaging, modern landing page for AgentChat that showcases the AI chat capabilities, highlights key features, explains the different AI models available, and drives users to start conversations. The page should communicate intelligence, versatility, and ease of use.

### Page Sections

#### 1. Hero Section
- **Headline**: Bold, attention-grabbing main heading
  - Text: "Your Intelligent AI Companion"
  - Subheading: "Experience next-generation AI conversations with multiple specialized models. From creative tasks to expert analysis, AgentChat adapts to your needs."
- **Call-to-Action Buttons**:
  - Primary: "Start Chatting Now" (navigate to /chat)
  - Secondary: "Explore AI Models" (scroll to models section)
- **Hero Visual**:
  - Animated chat bubble illustration
  - Gradient background with Sunset theme colors
  - Floating message cards animation (optional)
- **Design**:
  - Full-width section with gradient background
  - Centered content with max-width container
  - Responsive layout (stack on mobile)

#### 2. AI Models Section
Showcase the four available AI models with detailed cards in a 2x2 grid:

**Model 1: AI Assistant (LLM)**
- Icon: MessageSquare icon
- Title: "Standard AI Assistant"
- Model ID: "llm"
- Description: "Powered by advanced language models, perfect for general conversations, creative writing, problem-solving, and everyday questions."
- Key Features:
  - Natural language understanding
  - Creative content generation
  - Code assistance
  - Knowledge synthesis
- Badge: "Most Popular"

**Model 2: AI Assistant (LLM + CNN)**
- Icon: Eye icon
- Title: "Vision-Enhanced AI"
- Model ID: "llm-cnn"
- Description: "Combines language understanding with computer vision capabilities. Upload images for analysis, classification, and visual understanding."
- Key Features:
  - Image classification
  - Visual question answering
  - Multi-modal reasoning
  - Object detection
- Badge: "Image Support"

**Model 3: AI Expert (RAG)**
- Icon: Database icon
- Title: "Knowledge Expert"
- Model ID: "llm-rag"
- Description: "Retrieval-Augmented Generation model that accesses specialized knowledge bases for accurate, source-backed answers."
- Key Features:
  - Document retrieval
  - Fact-checking
  - Source citations
  - Domain expertise
- Badge: "Most Accurate"

**Model 4: AI Expert (Agent)**
- Icon: Cpu icon
- Title: "Agentic AI"
- Model ID: "llm-agent"
- Description: "Advanced AI agent with tool-use capabilities. Performs complex multi-step tasks, searches, calculations, and integrations."
- Key Features:
  - Tool usage
  - Web search
  - API integrations
  - Task automation
- Badge: "Most Powerful"

#### 3. Features Section
Highlight core chat interface features with icon cards in a 3-column grid:

**Feature 1: Multi-Model Support**
- Icon: Layers icon
- Title: "Choose Your AI Model"
- Description: "Switch between specialized AI models tailored for different tasks. From creative writing to expert analysis, select the perfect assistant."

**Feature 2: Image Understanding**
- Icon: Image icon
- Title: "Upload & Analyze Images"
- Description: "Send images in your conversations for visual analysis, classification, and understanding with vision-enabled models."

**Feature 3: Markdown Rendering**
- Icon: FileText icon
- Title: "Rich Text Formatting"
- Description: "AI responses support full markdown with code blocks, tables, lists, and formatting for easy-to-read answers."

**Feature 4: Persistent History**
- Icon: History icon
- Title: "Never Lose a Conversation"
- Description: "All your chats are automatically saved. Resume conversations anytime from your chat history."

**Feature 5: Real-time Responses**
- Icon: Zap icon
- Title: "Lightning Fast"
- Description: "Get instant AI responses with typing indicators and smooth, real-time conversation flow."

**Feature 6: Mobile Responsive**
- Icon: Smartphone icon
- Title: "Chat Anywhere"
- Description: "Fully responsive design optimized for seamless conversations on mobile, tablet, and desktop devices."

#### 4. How It Works Section
Step-by-step visual guide (3 steps in a horizontal timeline):

**Step 1: Choose Your Model**
- Icon: MousePointer icon
- Title: "Select AI Model"
- Description: "Pick from four specialized AI models based on your task: general assistant, vision AI, knowledge expert, or agentic AI."

**Step 2: Start Conversation**
- Icon: MessageCircle icon
- Title: "Type or Upload"
- Description: "Send your message or upload an image. The AI understands natural language and can analyze visual content."

**Step 3: Get Intelligent Answers**
- Icon: Sparkles icon
- Title: "Receive AI Response"
- Description: "Get detailed, well-formatted responses instantly. Continue the conversation as the AI remembers context."

#### 5. Use Cases Section
Display practical applications in a visually appealing way (2x3 grid):

**Use Case Cards:**
1. **Creative Writing**
   - Icon: PenTool icon
   - Description: "Generate stories, poems, and creative content"

2. **Code Assistance**
   - Icon: Code icon
   - Description: "Get help with programming and debugging"

3. **Image Analysis**
   - Icon: ScanSearch icon
   - Description: "Classify and understand visual content"

4. **Research & Learning**
   - Icon: GraduationCap icon
   - Description: "Explore topics with source-backed answers"

5. **Problem Solving**
   - Icon: Lightbulb icon
   - Description: "Work through complex challenges step-by-step"

6. **Task Automation**
   - Icon: Workflow icon
   - Description: "Automate multi-step tasks with AI agents"

#### 6. Statistics Showcase Section
Display impressive metrics in a visually appealing way:
- **Dynamic Counter Cards** (4 cards):
  - "4 AI Models" with Layers icon
  - "Unlimited Conversations" with Infinity icon
  - "100% Free to Use" with Gift icon
  - "24/7 Availability" with Clock icon

#### 7. Call-to-Action Banner
- **Background**: Gradient with Sunset theme colors
- **Headline**: "Ready to Experience Intelligent AI?"
- **Subtext**: "Start your first conversation now and discover the power of multi-model AI assistance"
- **Button**: "Launch AgentChat" (navigate to /chat)
- **Additional Text**: "No sign-up required • Free forever • Instant access"

#### 8. Footer Section
- Already exists in template, but ensure it includes:
  - App name and tagline
  - Copyright information
  - Quick links (Chat, Home)

### Design Specifications

#### Layout & Spacing
- **Max Width**: 1280px for content sections
- **Section Padding**: py-16 to py-24 (responsive)
- **Section Gaps**: Adequate whitespace between sections (space-y-16)
- **Container**: Centered with px-4 sm:px-6 lg:px-8

#### Typography
- **Hero Headline**: text-4xl sm:text-5xl lg:text-6xl font-bold
- **Section Headings**: text-3xl sm:text-4xl font-bold
- **Subsection Headings**: text-2xl font-semibold
- **Feature Titles**: text-xl font-semibold
- **Body Text**: text-base sm:text-lg text-muted-foreground
- Use Space Grotesk for headings, Inter for body text

#### Color Palette (Sunset Theme)
- **Background**: Gradient backgrounds for hero and CTA sections
- **Accent Colors**: Warm orange/coral for CTAs and highlights
- **Feature Cards**: bg-card with border
- **Icons**: text-primary or themed colors
- **Badges**: Different colors for each (blue, pink, green, purple)

#### Interactive Elements
- **Buttons**:
  - Hover effects with scale (1.05) and shadow
  - Smooth transitions (transition-all duration-200)
  - Primary: solid background, secondary: outline
- **Cards**:
  - Hover: lift effect (shadow-lg increase)
  - Rounded corners (0.75rem)
  - Border on hover color change
- **Animations**:
  - Fade-in on scroll (optional)
  - Floating animation for hero visuals
  - Number counters for statistics (animated)

#### AI Model Cards Styling
- Large cards in 2x2 grid on desktop
- Single column on mobile
- Each card contains:
  - Large icon (primary color)
  - Model title (text-2xl font-bold)
  - Model ID badge (text-xs, monospace font)
  - Description (text-base)
  - Key features list (checkmarks with primary color)
  - Special badge (top-right corner)
- Hover effect: border color changes to primary
- Click: Navigate to `/chat?model={model_id}`

### Component Structure

Create components in `src/components/home/`:
- **HeroSection.jsx** - Main hero section with CTAs
- **AIModelsSection.jsx** - Four AI model cards
- **FeaturesSection.jsx** - Feature cards grid
- **HowItWorksSection.jsx** - Step-by-step guide
- **UseCasesSection.jsx** - Use case cards grid
- **StatsSection.jsx** - Statistics showcase
- **CTABanner.jsx** - Final call-to-action

Update `src/app/page.jsx` to use these components instead of the current placeholder content.

### Functional Requirements

#### Navigation
- "Start Chatting Now" and "Launch AgentChat" buttons navigate to `/chat`
- "Explore AI Models" smooth scrolls to models section
- AI model cards navigate to `/chat?model={model_id}`
- All navigation should use Next.js router for client-side transitions

#### Responsive Design
- **Mobile** (< 640px): Single column layout, stacked elements
- **Tablet** (640px - 1024px): 2-column grid for features, model cards
- **Desktop** (> 1024px): 3-column grid for features, 2x2 for models

#### Animations (Optional)
- Fade-in animations for sections on scroll (use Intersection Observer)
- Number counter animation for statistics (count up effect)
- Smooth scroll behavior for anchor links
- Button hover and active states with transforms
- Floating animation for hero visual elements

#### Accessibility
- Proper heading hierarchy (h1, h2, h3, h4)
- Alt text for all images/icons
- Sufficient color contrast (WCAG AA)
- Keyboard navigation support
- Focus visible states
- Screen reader friendly labels
- Skip to content link

### Content Strategy

#### Tone & Voice
- Intelligent yet approachable
- Technical but not overwhelming
- Confident and innovative
- User-focused benefits

#### Messaging Hierarchy
1. **What**: AI chat assistant with multiple models
2. **Who**: For anyone needing AI assistance
3. **Why**: Specialized models for different tasks
4. **How**: Simple chat interface with powerful features
5. **Action**: Start chatting now

#### Key Differentiators
- Four specialized AI models vs single model
- Image support with vision models
- Agentic capabilities with tool use
- RAG for accurate, sourced answers
- Persistent conversation history
- Free and unlimited access

### User Experience Goals
- Visitors immediately understand AgentChat's unique value
- Clear differentiation between AI models
- Easy to get started (one click to chat)
- Features are scannable and benefit-focused
- Multiple conversion points throughout page
- Mobile-first, responsive experience
- Fast loading with optimized assets
- Engaging visual design with Sunset theme

### Special Considerations

#### AI Model Selection
- Each model card should be clickable
- Navigate to chat with pre-selected model
- Clear visual feedback on hover
- Badges highlight unique capabilities

#### Gradient Backgrounds
- Use Sunset theme colors (warm oranges, corals, yellows)
- Subtle gradients that don't overwhelm content
- Consistent gradient direction (usually diagonal)
- Lower opacity overlays for readability

#### Icon Usage
- Consistent icon style (lucide-react library)
- Appropriate size for context (h-6 w-6 to h-12 w-12)
- Primary color for emphasis
- Muted colors for secondary elements

#### Badge System
- "Most Popular" - Blue badge
- "Image Support" - Pink badge
- "Most Accurate" - Green badge
- "Most Powerful" - Purple badge
- Small, pill-shaped with rounded corners
- Positioned in top-right of cards

Use the instructions in Component.md to implement the required changes for this app.
---
