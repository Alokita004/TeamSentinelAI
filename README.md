&#x20;🚨 SENTINELAI



\## AI-Powered Disaster Intelligence \& Emergency Response Platform



> Transforming disaster data into intelligent decisions and coordinated action.



SENTINELAI is an AI-powered Disaster Intelligence and Emergency Response Platform designed to help emergency responders make faster, smarter, and data-driven decisions during disasters.



The platform initially focuses on Urban Flood Response, combining disaster intelligence, multi-agent AI, geospatial visualization, knowledge graphs, risk analysis, evacuation planning, resource management, and real-time decision support into a unified command-center platform.



\---



\## 🎯 Problem Statement



During disasters such as urban floods, emergency response teams often work with fragmented and rapidly changing information.



Weather conditions, road blockages, citizen reports, emergency alerts, evacuation routes, shelters, incidents, and available resources may exist across disconnected systems.



This creates major challenges:



\* Delayed decision-making

\* Difficulty identifying high-risk areas

\* Inefficient resource allocation

\* Lack of real-time situational awareness

\* Difficult coordination between response teams

\* Static evacuation plans that cannot adapt to changing conditions



SENTINELAI addresses this problem by converting fragmented disaster information into \*\*actionable AI-driven decisions\*\*.



\---



\## 💡 Our Solution



SENTINELAI creates a centralized AI-powered emergency intelligence layer that can:



\*\*Collect → Analyze → Reason → Predict → Recommend → Act\*\*



The platform combines structured data, knowledge graphs, geospatial intelligence, and multi-agent AI to provide responders with a continuously updated operational picture.



\---



\## 🧠 Multi-Agent AI Architecture



SENTINELAI uses LangGraph to orchestrate specialized AI agents.



\### Specialized Agents



| Agent                 | Responsibility                                                  |

| --------------------- | --------------------------------------------------------------- |

| 🌊 Risk Agent         | Identifies and evaluates high-risk areas                        |

| 🧠 Graph Agent        | Performs relationship-aware reasoning using the knowledge graph |

| 🗺️ Route Agent       | Determines safer evacuation routes                              |

| 🚑 Resource Agent     | Evaluates emergency resource requirements                       |

| 🎯 Decision Agent     | Generates coordinated response recommendations                  |

| 🔔 Notification Agent | Supports emergency alert workflows                              |



These agents collaborate through a stateful LangGraph workflow instead of operating as isolated chatbots.



\---



\## ✨ Key Features



\### 🗺️ Real-Time Disaster Command Center



Interactive dashboard providing:



\* Disaster overview

\* Risk levels

\* Incident monitoring

\* Geographic visualization

\* Active alerts

\* Emergency response status



\### 🌊 Risk Intelligence



Analyzes disaster-related information to identify:



\* High-risk zones

\* Emerging threats

\* Critical incidents

\* Population and infrastructure exposure



\### 🚨 Incident Management



Track and manage:



\* Flood incidents

\* Road blockages

\* Infrastructure issues

\* Citizen reports

\* Emergency situations



\### 🧭 Smart Evacuation



SENTINELAI can recommend safer evacuation strategies based on:



\* Current incidents

\* Risk zones

\* Road conditions

\* Shelter locations

\* Geographic relationships



\### 🚑 Resource Intelligence



Helps emergency teams understand:



\* What resources are available

\* Where resources are required

\* Which incidents require priority

\* How resources can be allocated



\### 🕸️ Knowledge Graph



Neo4j represents relationships between:



\* Locations

\* Incidents

\* Hazards

\* Shelters

\* Resources

\* Evacuation routes

\* Emergency entities



This enables contextual and relationship-aware reasoning.



\### 🤖 AI Emergency Assistant



A conversational AI interface that allows users to ask questions about the disaster situation and receive context-aware recommendations.



\### 👥 Citizen Reporting



Citizens can report incidents and provide information that can contribute to the emergency intelligence pipeline.



\### 🔄 AI Agent Monitoring



Monitor agent execution and workflow progress to provide transparency into the AI decision-making pipeline.



\### 🔔 Emergency Notifications



Supports emergency communication and alert workflows.



\### 📊 Analytics \& Visualization



Provides visual insights through:



\* Interactive maps

\* Risk indicators

\* Charts

\* Incident statistics

\* Resource status

\* Response metrics



\### 🧪 Demo / Simulation Mode



SENTINELAI includes a simulation environment so the complete platform can operate without requiring:



\* Production weather APIs

\* Production traffic APIs

\* External notification systems

\* Production Neo4j

\* External LLM services



This makes the platform reliable for demonstrations while maintaining a production-oriented architecture.



\---



\# 🏗️ System Architecture



```text

&#x20;                       ┌──────────────────────────┐

&#x20;                       │       SENTINELAI         │

&#x20;                       │      Web Dashboard       │

&#x20;                       └────────────┬─────────────┘

&#x20;                                    │

&#x20;                                    ▼

&#x20;                       ┌──────────────────────────┐

&#x20;                       │       FastAPI Backend    │

&#x20;                       │      REST API Layer      │

&#x20;                       └────────────┬─────────────┘

&#x20;                                    │

&#x20;                                    ▼

&#x20;                    ┌──────────────────────────────┐

&#x20;                    │     LangGraph Orchestrator    │

&#x20;                    └──────────────┬───────────────┘

&#x20;                                   │

&#x20;             ┌─────────────────────┼─────────────────────┐

&#x20;             │                     │                     │

&#x20;             ▼                     ▼                     ▼

&#x20;       ┌───────────┐         ┌───────────┐        ┌───────────┐

&#x20;       │ Risk      │         │ Route     │        │ Resource  │

&#x20;       │ Agent     │         │ Agent     │        │ Agent     │

&#x20;       └───────────┘         └───────────┘        └───────────┘

&#x20;             │                     │                     │

&#x20;             └─────────────────────┼─────────────────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                          ┌─────────────────┐

&#x20;                          │ Decision Agent  │

&#x20;                          └────────┬────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;             ┌─────────────────────────────────────────┐

&#x20;             │          Intelligence Layer             │

&#x20;             │                                         │

&#x20;             │ PostgreSQL │ Neo4j │ Vector Retrieval   │

&#x20;             └─────────────────────────────────────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                          ┌─────────────────┐

&#x20;                          │ Action / Alert  │

&#x20;                          └─────────────────┘

```



\---



🛠️ Technology Stack



\## Frontend



\* Next.js

\* React

\* TypeScript

\* Tailwind CSS

\* shadcn/ui

\* Zustand

\* React Hook Form

\* Zod

\* React Leaflet

\* Recharts

\* Lucide React



\## Backend



\* Python

\* FastAPI

\* Pydantic

\* REST APIs



\## AI \& Agentic Systems



\* LangGraph

\* LangChain

\* Large Language Models

\* Multi-Agent AI

\* Retrieval-Augmented Generation

\* Stateful Agent Workflows



\## Databases



\* PostgreSQL

\* Neo4j

\* Vector Database / Vector Retrieval



\## DevOps



\* Docker

\* Git

\* GitHub

\* Cloud-ready architecture



\---



\# 🔄 Example Emergency Workflow



```text

Disaster Data

&#x20;    ↓

Incident Detection

&#x20;    ↓

Risk Assessment

&#x20;    ↓

Knowledge Graph Reasoning

&#x20;    ↓

Route \& Resource Analysis

&#x20;    ↓

Multi-Agent Collaboration

&#x20;    ↓

Decision Generation

&#x20;    ↓

Emergency Recommendation

&#x20;    ↓

Notification / Response Action

```



\---



\# 🚀 Getting Started



\## Prerequisites



Make sure you have:



\* Node.js

\* Python 3.10+

\* Git

\* PostgreSQL

\* Neo4j

\* Docker (optional)



\---



\## Clone the Repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd SENTINELAI

```



\---



\## Frontend



```bash

cd frontend

npm install

npm run dev

```



The frontend will normally be available at:



```text

http://localhost:3000

```



\---



\## Backend



Create and activate a Python virtual environment:



\### Windows



```powershell

python -m venv .venv

.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



Start the FastAPI server:



```powershell

uvicorn app.main:app --reload

```



The API will normally be available at:



```text

http://localhost:8000

```



\---



\# 🧪 Demo Mode



SENTINELAI provides simulated disaster data to demonstrate the complete platform without relying on external production services.



Demo Mode can simulate:



\* Flood conditions

\* Risk escalation

\* Road blockages

\* Citizen reports

\* Emergency incidents

\* Shelter availability

\* Resource requirements

\* Agent execution

\* Evacuation recommendations



This ensures the project remains demonstrable even when external APIs or infrastructure are unavailable.



\---



\# 📊 Project Impact



SENTINELAI aims to improve emergency response by providing:



\* ⚡ Faster decision-making

\* 🎯 Better incident prioritization

\* 🗺️ Dynamic evacuation intelligence

\* 🚑 More efficient resource allocation

\* 🧠 Context-aware AI reasoning

\* 📡 Unified disaster situational awareness

\* 🔍 Transparent AI workflows

\* 🤝 Better coordination between emergency stakeholders



\---



\# 🔮 Future Improvements



Future versions of SENTINELAI can include:



\* Real-time government disaster-management integrations

\* Live weather and traffic APIs

\* IoT sensor integration

\* Satellite imagery analysis

\* Drone/CCTV computer vision

\* Flood propagation prediction

\* Population-level risk prediction

\* Automated SMS and emergency notifications

\* Multi-language citizen assistant

\* Mobile application

\* Advanced resource optimization

\* Support for earthquakes, cyclones, wildfires, and industrial disasters

\* Multi-city and multi-agency deployment

\* Human-in-the-loop AI governance

\* Advanced monitoring and AI evaluation



\---



\# 🌍 Vision



The long-term vision of SENTINELAI is to become a general-purpose AI Decision Intelligence platform for disaster preparedness, response, and recovery.



Instead of simply showing responders what is happening, SENTINELAI aims to help them understand:



> What is happening?

> What is likely to happen next?

> What should we prioritize?

> What action should we take?



\---



\# 🏆 Innovation



SENTINELAI is not simply a disaster dashboard or chatbot.



Its core innovation is the combination of:



\*\*Multi-Agent AI + Knowledge Graph + Geospatial Intelligence + Structured Data + Real-Time Decision Support\*\*



This enables SENTINELAI to transform continuously changing disaster information into \*\*actionable emergency intelligence\*\*.







&#x20;👥 Team



Team SentinelAI



Built with a focus on Artificial Intelligence, Agentic Systems, Disaster Intelligence, and Emergency Response.





&#x20;📄 License



This project is developed for educational, research, and innovation purposes.



