from sqlalchemy import or_
from models.ticket import Ticket, TicketStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException


async def get_tickets(db: AsyncSession, page: int = 1, per_page: int = 10, user_id: str = None):
    query = select(Ticket)
    if user_id is not None:
        query = query.filter(Ticket.user_id == user_id)
    else:
        # Выводим только те тикеты, которые не назначены ни одному юзеру
        query = query.filter(Ticket.user_id.is_(None))
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    tickets = result.scalars().fetchall()

    if not tickets and page != 1:
        raise HTTPException(status_code=404, detail="Page not found")
    return tickets


async def get_ticket(db: AsyncSession, ticket_id: str):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    return result.scalars().first()


async def search_tickets_by_title(db: AsyncSession, title: str, page: int = 1, per_page: int = 10, user_id: str = None):
    search = "%{}%".format(title)
    query = select(Ticket).filter(Ticket.title.ilike(search))
    if user_id is not None:
        query = query.filter(Ticket.user_id == user_id)
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    tickets = result.scalars().all()

    if not tickets and page != 1:
        raise HTTPException(status_code=404, detail="Page not found")
    return tickets


async def search_tickets_by_time(db: AsyncSession, from_time: int = None, to_time: int = None, page: int = 1,
                                 per_page: int = 10, user_id: str = None):
    query = select(Ticket)

    if from_time:
        query = query.filter(Ticket.creationTime >= from_time)
    if to_time:
        query = query.filter(Ticket.creationTime <= to_time)
    if user_id is not None:
        query = query.filter(Ticket.user_id == user_id)

    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    tickets = result.scalars().all()

    if not tickets and page != 1:
        raise HTTPException(status_code=404, detail="Page not found")
    return tickets


async def search_tickets(db: AsyncSession, search_string: str, page: int = 1, per_page: int = 10, user_id: str = None):
    search = f"%{search_string}%"
    query = select(Ticket).filter(
        or_(
            Ticket.title.ilike(search),
            Ticket.content.ilike(search),
            Ticket.userEmail.ilike(search)
        )
    )
    if user_id is not None:
        query = query.filter(Ticket.user_id == user_id)
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    tickets = result.scalars().all()

    if not tickets and page != 1:
        raise HTTPException(status_code=404, detail="Page not found")
    return tickets


async def assign_ticket(db: AsyncSession, ticket_id: str, user_id: str):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    ticket = result.scalars().first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.user_id = user_id
    ticket.status = TicketStatus.IN_PROGRESS

    await db.commit()

    return ticket


async def close_ticket(db: AsyncSession, ticket_id: str):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    ticket = result.scalars().first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = TicketStatus.CLOSED

    await db.commit()

    return ticket
