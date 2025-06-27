# System Architecture

## Overview

The Smart Home Energy Management Dashboard is designed as a pet project application which should have real-time capabilities and role-based access control.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  Angular SPA (Frontend)                                        │
│  - Dashboard UI                                                │
│  - Real-time charts                                            │
│  - Role-based components                                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  AWS API Gateway                                               │
│  - Rate limiting                                               │
│  - CORS handling                                               │
│  - Request/Response transformation                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  Python FastAPI (Backend)                                      │
│  - REST API endpoints                                          │
│  - WebSocket connections                                       │
│  - Business logic                                              │
│  - Azure AD integration                                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                 │
├─────────────────────────────────────────────────────────────────┤
│  AWS DynamoDB                                                  │
│  - User profiles                                               │
│  - Energy consumption data                                     │
│  - Alert configurations                                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Integrations                        │
├─────────────────────────────────────────────────────────────────┤
│  Home Assistant API                                            │
│  - Real-time energy data                                       │
│  - Device status                                               │
│  - Historical data                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (Angular)

**Goals:**
- Lazy-loaded modules for performance
- Role-based component rendering
- Real-time data updates via WebSocket
- Responsive design with Angular Material
- State management with services

### Backend (Python FastAPI)

**Goals:**
- Async/await patterns throughout
- Dependency injection for services
- Middleware for authentication
- WebSocket support for real-time updates
- Comprehensive error handling

### Database Design (DynamoDB)

**Tables:**

1. **Users**
   - Partition Key: `user_id`
   - Attributes:azure_oid, email, name, role, created_at

2. **EnergyData**
   - Partition Key: `data_type`
   - Sort Key: `timestamp`
   - Attributes: consumption, cost, source, device_id

4. **Alerts**
   - Partition Key: `alert_type`
   - Sort Key: `alert_id`
   - Attributes: threshold, status, created_at, resolved_at, message

### Authentication & Authorization

**Azure AD Integration:**
- OAuth 2.0 with OpenID Connect
- JWT token validation
- Role-based access control (RBAC)
- Single sign-on (SSO) support

**Roles:**
- **Viewer**: Read-only access to energy data
- **Manager**: Can view data and manage alerts
- **Admin**: Full access to all features
- **Provider**: Access to customer data for energy providers

### Data Flow

1. **Real-time Data Ingestion:**
   ```
   Home Assistant → AWS Lambda → DynamoDB → FastAPI → Angular
   ```

2. **User Authentication:**
   ```
   Angular → Azure AD → FastAPI → DynamoDB (user lookup)
   ```

3. **Dashboard Updates:**
   ```
   DynamoDB → FastAPI → WebSocket → Angular (real-time)
   ```

### Security Considerations

- All API endpoints require authentication
- Role-based access control at API level via Azure AD
- CORS configuration for frontend
- Input validation with Pydantic? possibly
- Rate limiting via API Gateway
- HTTPS enforcement

### Scalability Design

- **Horizontal Scaling**: Stateless API services + Lambdas
- **Database**: DynamoDB auto-scaling
- **CDN**: CloudFront for static assets
- **Load Balancing**: Application Load Balancer

### Monitoring & Observability

- **Logging**: Structured logging with correlation IDs
- **Metrics**: CloudWatch metrics for performance if I can get to it
- **Health Checks**: API health endpoints
- **Error Tracking**: Centralized error handling

## Deployment Architecture???

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CloudFront    │    │   API Gateway   │    │   Application   │
│   (CDN)         │    │   (Load Bal.)   │    │   Load Balancer │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   S3 Bucket     │    │   Lambda        │    │   ECS Fargate?  │
│   (Static)      │    │   (Functions)   │    │   (API)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────────────────────┐
                       │         DynamoDB                │
                       │      (Data Storage)             │
                       └─────────────────────────────────┘
```
