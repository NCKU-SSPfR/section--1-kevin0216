import pytest
import httpx

USERNAME = "TestUser"
RESET_URL = f"http://127.0.0.1:8000/api/v1/reset?username={USERNAME}"
LOGIN_URL = f"http://127.0.0.1:8000/api/v1/login"
MOVE_URL = "http://127.0.0.1:8000/api/v1/move"

async def login_request():
    """Simulates a frontend login."""
    
    payload = {"username": USERNAME}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(LOGIN_URL, json=payload)

    assert response.status_code == 200  # Ensure the request was successful

async def reset_request():
    """Reset Game state"""

    async with httpx.AsyncClient() as client:
        response = await client.get(RESET_URL)

    assert response.status_code == 200  # Ensure the request was successful
    game_state = response.json()
    assert game_state["current_position"] == [1, 0]

async def move_request(dir):
    """Simulates a frontend move request."""

    payload = {"username": USERNAME, "direction": dir}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(MOVE_URL, json=payload)

    assert response.status_code == 200  # Ensure the request was successful
    game_state = response.json()
    assert game_state["health"] >= 3
    return game_state
@pytest.mark.asyncio
async def test_integration():
    await login_request()
    await reset_request()
    for _ in range(5):
         game_state = await move_request("down")
    assert game_state["current_position"] == [1,5]

@pytest.mark.asyncio
async def test_solver():
    await login_request()
    await reset_request()

    move_map = [
        "down"*5,
        "right",
        "down",
        "right"*2,
        "up"*4,
        "right"*2,
        "down",
        "right"*2,
        "down",
        "right",
        "down"
    ]
    
    for move in move_map:
        game_state = await move_request(move)

    assert game_state["health"] == 666
