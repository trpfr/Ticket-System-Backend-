#  This file contains the routes for the ticket endpoints
import uuid

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.mananger import get_user_manager
from database import get_async_session
from models.ticket import TicketStatus
from models.user import User
from services import ticket as ticket_service
from dto import ticket as ticket_dto

#  This is the router object. It is used to create the routes.
router = APIRouter()

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)


async def async_wrapper(func, *args, **kwargs):
    return await func(*args, **kwargs)


@router.get("/{ticket_id}",
            response_model=ticket_dto.Ticket,
            tags=["ticket"],
            dependencies=[Depends(current_active_user)])
async def get_ticket(ticket_id: str, db: AsyncSession = Depends(get_async_session)):
    """Get a ticket by ID"""
    return await async_wrapper(ticket_service.get_ticket, db=db, ticket_id=ticket_id)


@router.post("/{ticket_id}",
             response_model=ticket_dto.Ticket,
             tags=["ticket"],
             dependencies=[Depends(current_active_user)])
async def assign_ticket(ticket_id: str, user_id: str, db: AsyncSession = Depends(get_async_session)):
    """Assign a ticket to a user"""
    return await async_wrapper(ticket_service.assign_ticket, db=db, ticket_id=ticket_id, user_id=user_id)


@router.patch("/{ticket_id}/close",
              response_model=ticket_dto.Ticket,
              tags=["ticket"],
              dependencies=[Depends(current_active_user)])
async def close_ticket(ticket_id: str, db: AsyncSession = Depends(get_async_session)):
    return await async_wrapper(ticket_service.close_ticket, db=db, ticket_id=ticket_id)


@router.get("/",
            response_model=list[ticket_dto.Ticket],
            tags=["ticket"],
            dependencies=[Depends(current_active_user)])
async def get_tickets(page: int = 1, per_page: int = 10, user_id: str = None,
                      db: AsyncSession = Depends(get_async_session)):
    """Get all tickets"""
    return await async_wrapper(ticket_service.get_tickets, db=db, page=page, per_page=per_page, user_id=user_id)


@router.get("/search_by_title/",
            response_model=list[ticket_dto.Ticket],
            tags=["ticket"],
            dependencies=[Depends(current_active_user)])
async def get_tickets_by_title(search_string: str, page: int = 1, per_page: int = 10, user_id: str = None,
                               db: AsyncSession = Depends(get_async_session)):
    """Search a ticket by title"""
    return await async_wrapper(ticket_service.search_tickets_by_title, db=db, title=search_string, page=page,
                               per_page=per_page, user_id=user_id)


@router.get("/search_by_time/",
            response_model=list[ticket_dto.Ticket],
            tags=["ticket"],
            dependencies=[Depends(current_active_user)])
async def filter_tickets_by_time_route(from_time: int = None, to_time: int = None, page: int = 1, per_page: int = 10,
                                       user_id: str = None, db: AsyncSession = Depends(get_async_session)):
    return await async_wrapper(ticket_service.search_tickets_by_time, db=db, from_time=from_time, to_time=to_time,
                               page=page, per_page=per_page, user_id=user_id)


@router.get("/search_tickets/",
            response_model=list[ticket_dto.Ticket],
            tags=["ticket"],
            dependencies=[Depends(current_active_user)])
async def search_tickets_route(search_string: str, page: int = 1, per_page: int = 10, user_id: str = None,
                               db: AsyncSession = Depends(get_async_session)):
    return await async_wrapper(ticket_service.search_tickets, db=db, search_string=search_string, page=page,
                               per_page=per_page, user_id=user_id)
