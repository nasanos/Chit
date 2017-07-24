#CHIT

##What It Is
This project, created in Python with Flask, is a simple chat web application with a basic login functionality. It's a product of a period of study and experimentation with the Flask framework and web application development generally.

##Features
* SocketIO utilized in (server-side) Python and (client-side) Javascript for handling of synchronous communications
* Storage of chat messages (via SQLAlchemy, for database-agnostic SQL) for persistent chats
* Fundamental user login system
* Chat conversation selector, for user to have multiple persistent conversations with different users
* Served with Eventlet

##To Do
* Extend login system to include user registration
* Limit users' possible conversations to (editable) friend lists
* Allow more than two users per conversation
* Refine design and layout for mobile