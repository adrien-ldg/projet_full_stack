# Readme

This project is a comprehensive Film Management API built with FastAPI, offering a robust platform for managing and exploring movie data. The API provides detailed information about films, their cast members, and related metadata, with features designed for both casual users and film enthusiasts.

## Project Overview

### Key Features
- Complete CRUD operations for films and cast members
- Advanced filtering system for movies based on multiple criteria:
  - Box office performance (gross earnings)
  - Budget ranges
  - Release years
  - Running time
  - MPAA ratings
  - Genres
  - Cast members
- User authentication and authorization system
- Detailed cast information management
- Modern web interface for easy data interaction

### Technical Stack
- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT-based authentication system
- **Documentation**: Automatic OpenAPI/Swagger documentation
- **Frontend**: Server-side rendered templates with Jinja2
- **Styling**: Modern CSS with responsive design

### Data Management
Our database contains comprehensive film information including:
- Title and ranking
- Financial data (gross earnings, budget)
- Release information (year, date)
- Content details (summary, MPAA rating, genres)
- Technical specifications (running time)
- Cast information (actors, directors, writers)
- Media assets (film and cast images)

# Data Structure

## Database Organization
Our PostgreSQL database is structured around three main entities:

### Films Table
The central entity storing movie information with:
- Unique identifiers and ranking
- Core movie details (title, summary)
- Financial metrics (gross earnings, budget)
- Technical information (runtime, MPAA rating)
- Categorization (genres stored as arrays)
- Temporal data (release date, production year)
- Marketing assets (promotional images)

### Cast Table
A related entity managing all cast members with:
- Unique UUID for each cast entry
- Personal information (name, image)
- Role classification (actor, director, writer)
- Character information for actors
- Relationship to films through foreign keys

### Users Table
Manages application users and authentication with:
- Unique identifiers for each user
- Authentication details (email, hashed password)
- Profile information (name)
- Account status (active/disabled)
- Access control information

## Data Relationships
- Each film can have multiple cast members
- Cast members can be associated with multiple films
- Roles are flexible, allowing the same person to be listed as both actor and director
- Users can interact with films and cast data based on their authentication
- All relationships are maintained through proper database constraints

## Data Security
- Sensitive operations require authentication
- Passwords are securely hashed
- Data integrity is enforced through database constraints
- Regular backups ensure data persistence
- Input validation through Pydantic schemas
- JWT-based authentication for secure user sessions

# Architecture

The API is organized into a well-structured modular architecture within the `api` directory. Here's a detailed breakdown of each component:

## Main Application (`main.py`)
- Entry point of the application that initializes the FastAPI instance
- Configures middleware (Prometheus for metrics)
- Sets up static files and Jinja2 templates
- Includes all routers for different endpoints
- Manages database lifecycle through lifespan events

## Models (`/models`)
- Defines SQLAlchemy ORM models for database tables
- `database.py`: Database connection and base configuration
- `post.py`: Contains data models for Films, Cast, and Users
- Handles relationships between different entities

## Routers (`/routers`)
Each router handles specific functionality with its own endpoints:
- `router_film.py`: 
  - CRUD operations for films
  - Advanced filtering and ranking endpoints
  - Supports pagination and complex queries
- `router_cast.py`:
  - Manages cast members (actors, directors, writers)
  - Links cast members to films
  - Supports filtering by name and film
- `router_user.py`:
  - User management endpoints
  - Profile operations
- `router_authentication.py`:
  - Handles login/logout
  - JWT token management
- `other_router.py`:
  - Serves the home page and other general endpoints

## API Endpoints

The API is organized into several routers, each handling specific functionality:

### Film Router (`/films`)
1. **List and Search**
   - `GET /films/`: Get all films with pagination
   - `GET /films/{title}`: Get specific film by title
   - `GET /films/filter/`: Advanced filtering with multiple parameters:
     * Gross earnings range
     * Budget range
     * Running time range
     * Year range
     * Distributor
     * MPAA rating
     * Genres
     * Cast members
   - `GET /films/byrank/`: Get films within specific rank range

2. **Management**
   - `POST /films/`: Create new film with cast
   - `PUT /films/{title}`: Update existing film
   - `DELETE /films/{title}`: Delete film

### Cast Router (`/cast`)
1. **List and Search**
   - `GET /cast/`: Get all cast members
   - `GET /cast/{id}`: Get specific cast member
   - `GET /cast/cast_name/{name}`: Search cast by name
   - `GET /cast/cast_film/{title}`: Get all cast for specific film

2. **Management**
   - `POST /cast/`: Add new cast member to film
   - `PUT /cast/{id}`: Update cast member
   - `DELETE /cast/{id}`: Remove cast member

### User Router (`/user`)
1. **User Management**
   - `POST /user/`: Create new user account
   - `GET /user/me/`: Get current user profile

### Authentication Router
1. **Session Management**
   - `POST /login/`: User login
   - `POST /logout/`: User logout

### Other Router
   - other function to enhance the user experience 

### Common Features Across Routers
1. **Authentication**
   - All endpoints (except login/register) require authentication
   - Uses `get_current_active_user` dependency

2. **Response Models**
   - Consistent use of Pydantic models
   - Proper status codes for different operations:
     * 201: Resource created
     * 202: Request accepted
     * 401: Unauthorized
     * 404: Not found
     * 409: Conflict

3. **Database Integration**
   - All routes use SQLAlchemy session
   - Proper error handling for database operations

4. **Input Validation**
   - Query parameters validation
   - Request body validation through Pydantic
   - Type checking and conversion

## Services (`/services`)
Business logic layer that separates database operations from route handlers:
- `service_film.py`: Film-related business logic
- `service_cast.py`: Cast management operations
- `service_user.py`: User management logic
- `service_authentication.py`: Authentication and authorization logic
- `oauth2.py`: OAuth2 implementation with JWT
- `hashing.py`: Password hashing utilities
- `auth_token.py`: Token generation and validation

## Services Layer

The services layer acts as the layer of the application, separating the database operations from the route handlers. Each service module is responsible for specific functionality:

### Film Service
- Manages all film-related operations
- Handles complex queries and filters
- Manages film rankings
- Coordinates film and cast relationships
- Implements data validation and error handling
- Handles database transactions for film operations

### Cast Service
- Manages cast member information
- Links cast members to films
- Handles cast member searches
- Provides cast filtering capabilities
- Manages cast member updates and deletions
- Ensures data integrity for cast-film relationships

### Authentication Service
- Implements secure user authentication
- Manages JWT token creation and validation
- Handles session management
- Implements secure cookie handling
- Provides logout functionality
- Manages user sessions and token expiration

### User Service
- Handles user account management
- Implements secure password hashing
- Manages user profiles
- Handles user registration
- Validates user credentials
- Manages user status (active/inactive)

### Common Service Features
1. **Error Handling**
   - Consistent error responses
   - Detailed error messages
   - HTTP status code mapping
   - Database transaction management

2. **Security**
   - Password hashing with bcrypt
   - Secure token management
   - Session validation
   - Input validation and sanitization

3. **Database Operations**
   - Transaction management
   - CRUD operations
   - Relationship handling
   - Query optimization

## Schemas (`/schemas`)
The schemas directory contains Pydantic models that define the structure of our data. We use a pattern of having separate "In" and "Out" schemas for our entities. Here's why:

### Input vs Output Schemas

#### Film Schemas (`FilmIn` vs `FilmOut`)
- **Input Schema (`FilmIn`)**:
  - Used when creating or updating films
  - Contains only the fields that users should be able to provide
  - Has default values for optional fields to simplify data creation
  - Doesn't include auto-generated fields like `rank`
  - Relationships (like cast) are handled through separate endpoints

- **Output Schema (`FilmOut`)**:
  - Used when sending film data to clients
  - Includes additional computed or database-generated fields (like `rank`)
  - Contains nested relationships (includes full `cast` list of all films)
  - Makes certain fields optional to handle partial data
  - Provides a complete view of the film with all its relationships

#### Cast Schemas (`CastIn` vs `CastOut`)
- **Input Schema (`CastIn`)**:
  - Focused on the essential data needed to create a cast entry
  - Simpler structure without relationship data
  - Uses default values for optional fields
  - Doesn't include the associated film data

- **Output Schema (`CastOut`)**:
  - Includes the complete film relationship
  - Provides more context by including related film information
  - Used when returning detailed cast information
  - Better handles optional fields for display purposes

### Why This Separation?

1. **Data Control**:
   - Input schemas limit what users can send to the API
   - Output schemas provide richer, more complete data back to users
   - This separation helps prevent unwanted data manipulation

2. **Relationship Handling**:
   - Input: Keeps relationships simple (using IDs or separate requests)
   - Output: Includes full relationship data for better data consumption

3. **Validation Logic**:
   - Input: Stricter validation for data creation/updates
   - Output: More flexible structure for displaying data

4. **Security**:
   - Input: Prevents users from setting sensitive or computed fields
   - Output: Includes additional fields that are safe to expose

5. **User Experience**:
   - Input: Simpler structure makes it easier to create/update data
   - Output: Richer data structure provides complete information in a single response

This separation of concerns helps maintain a clean, secure, and user-friendly API while ensuring data integrity and proper validation.

## Static Files (`/static`)
- CSS stylesheets for frontend styling
- JavaScript files for client-side functionality
- Images and other media assets
- Organized by type (css, js, images)

## Templates (`/templates`)
- Jinja2 HTML templates for server-side rendering
- Includes base templates and page-specific templates
- Supports template inheritance and reusable components

## Security Features
### Authentication System
The API implements a robust authentication system using JWT (JSON Web Tokens) with secure cookie-based storage:

#### Login Process
1. **User Authentication**:
   - Users provide email and password via the `/login` endpoint
   - Credentials are validated against the database
   - Passwords are verified using bcrypt hashing

2. **Token Management**:
   - Upon successful login, a JWT token is generated
   - Token contains user email in its payload
   - Token is signed using HS256 algorithm with a secure key

3. **Cookie Security**:
   - Token is stored in an HTTP-only cookie named "authentication"
   - Cookie settings:
     - `httponly`: True (prevents JavaScript access)
     - `secure`: True (only sent over HTTPS)
     - `samesite`: "strict" (prevents CSRF attacks)
     - `max_age`: 12 hours (automatic expiration)

#### Session Management
1. **Active Session Check**:
   - System prevents multiple concurrent logins
   - Checks for existing authentication cookie
   - Returns appropriate error if session already exists

2. **Access Control**:
   - Protected endpoints require valid authentication
   - Token is automatically validated on each request
   - Invalid or expired tokens trigger 401 Unauthorized responses

3. **User Status Verification**:
   - System checks if user account is active
   - Disabled accounts cannot access protected resources
   - Automatic validation through `get_current_active_user`

#### Logout Process
1. **Session Termination**:
   - `/logout` endpoint handles session ending
   - Authentication cookie is deleted
   - Server validates session existence before logout

### Libraries and Dependencies
- **FastAPI Security**: Provides OAuth2 password flow
- **Passlib**: Handles password hashing with bcrypt
- **PyJWT**: Manages JWT token creation and validation
- **Pydantic**: Ensures type safety in security schemas

### Protected Resources
All sensitive operations require authentication:
- Film management (create, update, delete)
- Cast management (create, update, delete)
- User profile access
- Data modification endpoints

### Security Best Practices
1. **Password Protection**:
   - Passwords never stored in plain text
   - Bcrypt hashing with salt
   - Secure password verification

2. **Token Security**:
   - Short-lived tokens (12-hour expiration)
   - Secure token storage in HTTP-only cookies
   - Protected against XSS and CSRF attacks

3. **Error Handling**:
   - Secure error messages
   - Proper HTTP status codes
   - Validation of all user inputs

## API Features
- RESTful endpoints following HTTP standards
- Comprehensive CRUD operations
- Advanced filtering and search capabilities
- Pagination support
- Error handling with appropriate status codes
- API documentation with OpenAPI/Swagger

This architecture ensures:
- Separation of concerns
- Maintainable and scalable codebase
- Secure and efficient data handling
- Clear organization of business logic
- Easy testing and debugging
