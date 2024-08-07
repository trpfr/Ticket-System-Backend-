# OpenSource Ticket System - Backend part

$${\color{red}Still}$$ $${\color{red}in}$$ $${\color{red}development}$$ 🚧

## Project Description

OpenSource TicketSystem is a simple and intuitive ticketing system with a basic web interface, developed as a pet project. The backend is written in FastAPI (Python),
and the frontend is developed using VueJS (JavaScript). The project is in the early stages of development and provides essential features for ticket management.

## Core Features

- [x] User Authentication and Registration: Users can register and log in to the system to manage tickets.
- [x] Ticket Creation: Users can create new tickets with all necessary details.
- [x] Ticket Viewing: Ability to view the details of a ticket.
- [x] Ticket Closure: Users can close tickets once the issue is resolved.
- [x] Ticket Assignment: Tickets can be assigned to specific users for resolution.
- [x] Ticket List: View all tickets in the system.
- [x] Ticket Search: Ability to search for tickets by title, creation time, and other fields.

## Planned Features

- [ ] Complete User Interface: Develop a fully functional user interface.
- [ ] Integrations: Integrate with messengers and other systems for ticket creation.
- [ ] Lifecycle Management: Manage the entire lifecycle of a ticket.
- [ ] Notifications: Send notifications about ticket updates via email or messengers.
- [ ] Role-Based Access Control: Introduce role-based access control to manage user permissions and access levels.

## Dependencies

This porject uses:
- FastAPI
- FastAPI Users
- SQLAlchemy
- Uvicorn
- PyDantic
- SQLite

Full list of dependencies is in requirement.txt

## Installation 

1. Clone the repository (use these commands in the terminal):    
   ```git clone https://github.com/piratinskii/Ticket-System-Backend.git```
   
   ```cd Ticket-System-Backend``` 

2. (Optional) Create a virtual environment:   
   ```python -m venv venv```
   
   ```source venv/bin/activate  # On Windows, use `venv\Scripts\activate```

3. Install dependencies:    
   ```pip install -r requirements.txt```

4. Generate SSL key and certificate for the server (better to use singed certificate instead of this step):
   ```python ssl_generator.py``` or ```python3 ssl_generator.py```

## Usage 

Run the server: 

```uvicorn main:app --ssl-keyfile=server.key --ssl-certfile=server.crt```

Check the documentation:
```https://127.0.0.1:8000/docs``` in your browser
