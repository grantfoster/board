# board

A pet project energy management system that monitors home energy consumption with role-based access control and real-time data.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Angular UI    │    │   Python API    │    │   AWS Services  │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Infra)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Azure AD      │    │   DynamoDB      │    │   Lambda        │
│   (Auth)        │    │   (Data)        │    │   (Processing)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Tech Stack

- **Frontend**: Angular 20 (with Zone.js)
- **Backend**: Python FastAPI
- **Authentication**: Azure AD with role-based access control
- **Database**: AWS DynamoDB
- **Infrastructure**: AWS Lambda, API Gateway, Fargate
- **Data Source**: My current Home Assistant API integration

## 📁 Project Structure

```
smart-energy-dashboard/
├── frontend/                 # Angular application
├── backend/                  # Python FastAPI server
├── infrastructure/           # AWS infrastructure as code
├── shared/                   # Shared types and utilities
├── docs/                     # Documentation
├── scripts/                  # Build and deployment scripts
└── README.md
```

## 🎯 Goals

- **Real-time Energy Monitoring**: Live dashboard with current consumption
- **Role-based Access**: Different views for homeowners, family members, and energy providers
- **Historical Analytics**: Trend analysis and consumption patterns
- **Smart Alerts**: Notifications for unusual energy usage, based on arbitrary limits perhaps?
- **Multi-tenant**: Support for multiple users (possibly multipe homes)

## 🛠️ Quick Start

### Prerequisites
- Node.js 24+
- Python 3.12+
- AWS CLI configured
- Azure AD tenant access

### Development Setup

TBD

## 🔐 Authentication

The system should use Azure AD for authentication - roles could be:
- **Viewer**: Can view energy data and basic analytics
- **Manager**: Can view data and manage alerts
- **Admin**: Full access to all features and settings
- **Provider**: Energy provider access for customer data

## 📊 Data Flow

1. Home Assistant provides real-time energy data
2. AWS Lambda processes and stores data in DynamoDB
3. Python API serves data to Angular frontend
4. Azure AD handles authentication and authorization
5. Real-time updates via WebSocket connections

## 🚀 Deployment

See `infrastructure/` directory for AWS deployment configurations and `scripts/` for deployment automation.

## 📝 Dev Timeline

- **Day 1**: Project setup and architecture ✅
    - Setup FastAPI
    - Setup Angular
    - Notes on architecture and plan
- **Day 2**: Backend foundation
    - OAuth and Azure AD (Entra)
    - JWTs
- **Day 3**: Angular foundation
    - SSO login/protect routes
    - Dash with device list
- **Day 4**: Role-based access control
    - Protect API endpoints by role/handle insufficient perms
    - Same for UI
- **Day 5**: Data integration & AWS services
    - Setup DynamoDB
    - Setup Lambdas
    - Simple API Gateway
    - Cloudfront for anything static
    - Load balance?
    - s3s?
- **Day 6**: Dashboard & visualization
    - Find library for charts
    - Make them look good, adjust API as needed
- **Day 7**: Alert system & notifications
- **Day 8**: Polish & Unit test 
