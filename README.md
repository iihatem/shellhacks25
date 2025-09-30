# AI Agent Management Platform

A fullstack application that creates and manages AI agents to handle tasks and jobs delegated by users. The platform features a secretary agent that determines task delegation and a hiring manager agent that creates new specialized agents when needed.

## 🏗️ Architecture

- **Backend**: FastAPI (Python) with RESTful APIs
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and shadcn/ui
- **AI Integration**: Ready for OpenAI/LangChain integration
- **Database**: PostgreSQL (configured, not yet implemented)
- **Caching**: Redis (configured, not yet implemented)

## Features

### Current Implementation

- **Dashboard**: Modern UI with agent and task overview
- **Chat Interface**: Interactive chatbot for task delegation
- **Agent Management**: View and manage AI agents in your workspace
- **Task Tracking**: Monitor task status and assignments
- **Responsive Design**: Mobile-friendly interface

### Planned Features

- AI-powered task analysis and delegation
- Dynamic agent creation based on task requirements
- Real-time task updates
- Agent performance analytics
- Multi-user workspaces

## 🛠️ Tech Stack

### Backend

- **FastAPI**: Modern, fast web framework for APIs
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: Database ORM (ready for implementation)
- **Alembic**: Database migrations
- **Redis**: Caching and task queues
- **OpenAI/LangChain**: AI integration

### Frontend

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type safety and better development experience
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality UI components
- **Lucide React**: Beautiful icons

## 📦 Project Structure

```
shellhacks25/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── env.example         # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js App Router
│   │   └── components/     # React components
│   │       ├── Dashboard.tsx
│   │       ├── ChatBot.tsx
│   │       ├── AgentsList.tsx
│   │       └── TasksList.tsx
│   ├── components.json     # shadcn/ui configuration
│   └── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment file:

```bash
cp env.example .env
# Edit .env with your configuration
```

5. Start the FastAPI server:

```bash
python main.py
# Or use uvicorn directly:
# uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 🔌 API Endpoints

### Agents

- `GET /agents` - Get all agents
- `POST /agents` - Create a new agent
- `GET /agents/{agent_id}` - Get specific agent

### Tasks

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task

### Chat

- `POST /chat` - Send message to secretary agent

### Health

- `GET /health` - Health check endpoint

## 🤖 Default Agents

The platform comes with two pre-configured agents:

1. **Executive Secretary** (`secretary-001`)

   - Role: Secretary
   - Capabilities: Task delegation, communication, scheduling
   - Purpose: Main interface for users, handles task analysis and delegation

2. **Hiring Manager** (`hiring-manager-001`)
   - Role: Hiring Manager
   - Capabilities: Agent creation, skill assessment, recruitment
   - Purpose: Creates new specialized agents when existing ones can't handle tasks

## Workflow Example

1. **User** sends a message: "I need to analyze our sales data and create a report"
2. **Secretary Agent** receives the message and analyzes the task
3. **Secretary** checks if any existing agent can handle data analysis and reporting
4. If no suitable agent exists, **Secretary** delegates to **Hiring Manager**
5. **Hiring Manager** creates a new "Data Analyst" agent with required capabilities
6. **New Agent** is assigned the task and begins work

## 🔧 Development

### Adding New Components

The project uses shadcn/ui components. To add new components:

```bash
cd frontend
npx shadcn@latest add [component-name]
```

### Database Setup (Future)

When ready to implement persistent storage:

1. Set up PostgreSQL
2. Update `DATABASE_URL` in `.env`
3. Create database models
4. Run migrations with Alembic

### AI Integration (Future)

To integrate with AI services:

1. Add OpenAI API key to `.env`
2. Implement agent logic in backend
3. Connect to LangChain for advanced workflows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🎉 Acknowledgments

- Built for ShellHacks 2025
- Uses shadcn/ui for beautiful components
- Powered by FastAPI and Next.js
