# ML Reasoning Engine - Frontend

Premium Next.js interface for the ML Reasoning System.

## Setup

### 1. Install Dependencies

```bash
cd frotend
pnpm install
```

### 2. Configure API Endpoint

Create `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
pnpm dev
```

Frontend runs at `http://localhost:3000`

## Backend Connection

Ensure the FastAPI backend is running:

```bash
cd ../src
python api.py
```

Backend runs at `http://localhost:8000`

## Features

- Premium minimalist design
- Real-time reasoning problem solving
- Category classification display
- Confidence metrics visualization
- Step-by-step reasoning explanations
- Responsive mobile/desktop layout
- Dark mode support

## Architecture

- **Framework**: Next.js 15 with React 19
- **Styling**: Tailwind CSS 4 with custom design system
- **UI Components**: Radix UI primitives
- **Icons**: Lucide React
- **API Client**: Native fetch with TypeScript types

## Design System

### Colors
- Monochromatic grayscale palette
- Pure black/white with subtle grays
- No unnecessary colors
- High contrast for readability

### Spacing
- Consistent 4/8/12/16/24px grid
- Mobile: 4px base unit
- Desktop: 6px base unit

### Typography
- Font-weight: light (300) for headers
- Font-weight: medium (500) for body
- Uppercase labels with letter-spacing

## API Integration

The frontend connects to `/solve` endpoint:

**Request:**
```typescript
{
  question: string;
  options: string[]; // exactly 5
}
```

**Response:**
```typescript
{
  predicted_answer: number;
  answer_text: string;
  confidence: number;
  reasoning: string;
  category: string;
  category_confidence: number;
  timestamp: string;
}
```

