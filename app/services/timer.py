import asyncio
from typing import Dict
from .web_sockets import manager
from .game import next_turn

game_timers: Dict[str, asyncio.Task] = {}

async def start_game_timer(room_id: str):
    if room_id in game_timers:
        game_timers[room_id].cancel()

    async def timer():
        seconds = 60
        try:
            await asyncio.sleep(1)
            while seconds > 0:
                await manager.broadcast_to_room(room_id, f"timer: {seconds}")
                await asyncio.sleep(1)
                seconds -= 1
            next_turn(room_id)
            await manager.broadcast_to_room(room_id, "next_turn")
            await start_game_timer(room_id)
        except asyncio.CancelledError:
            pass

    task = asyncio.create_task(timer())
    game_timers[room_id] = task

async def cancel_game_timer(room_id: str):
    if room_id in game_timers:
        game_timers[room_id].cancel()
        del game_timers[room_id]
