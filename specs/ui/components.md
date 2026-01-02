# UI Design & Components Spec (Phase II)

## Design System
- **Framework**: Tailwind CSS.
- **Theme**: Clean, minimalist, responsive (Mobile-first).
- **Icons**: Lucide React.
- **Feedback**: Sonner or Toast notifications for actions.

## Core Components

### 1. TaskCard
- **Props**: `task: Task`.
- **States**: View mode, Editing mode.
- **Interactions**:
  - Checkbox to toggle completion.
  - Delete icon with confirmation.
  - Title click to edit.

### 2. TaskList
- **Props**: `tasks: Task[]`.
- **Features**:
  - Empty state graphic/text.
  - Loading skeleton.
  - Animated transitions between filter states.

### 3. AuthForms
- **Login**: Email/Password + Submit.
- **Signup**: Name, Email, Password + Submit.
- **Validation**: Client-side (Zod + React Hook Form).

### 4. Layout
- **Navbar**: App Name, User Avatar (or Login button), Logout menu.
- **Main Container**: Centered, max-width (e.g., `max-w-2xl`).

## Accessibility (A11y)
- Semantic HTML tags.
- Keyboard navigable task list.
- Screen reader friendly error messages.
- High contrast status indicators.
