import sqlite3
import json
import logging
from contextlib import contextmanager
from typing import Optional, Dict, Any
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_PATH = os.environ.get("DB_PATH", "game.db")

@contextmanager
def get_db_connection():
    """Context manager for database connections with proper error handling"""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, isolation_level="EXCLUSIVE")
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            try:
                conn.close()
            except sqlite3.Error as e:
                logger.error(f"Error closing database connection: {e}")

def sanitize_input(value: str) -> str:
    """Sanitize input to prevent SQL injection"""
    return value.replace("'", "''")

def create_user(username: str) -> bool:
    """Create user and initialize game state with proper error handling"""
    username = sanitize_input(username)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO game_state (username, current_level_name, map_size, health, path, current_position)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, "maze-level-1", json.dumps([10, 10]), 3, json.dumps([[1, 0]]), json.dumps([1, 0])))
            conn.commit()
            logger.info(f"User {username} created successfully")
            return True
    except sqlite3.IntegrityError:
        logger.info(f"User {username} already exists")
        return True
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return False

def reset_game_state(username: str) -> bool:
    """Reset game state with proper error handling"""
    username = sanitize_input(username)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM game_state WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result:
                cursor.execute("""
                    UPDATE game_state 
                    SET current_level_name = ?, map_size = ?, health = ?, path = ?, current_position = ?
                    WHERE username = ?
                """, ("maze-level-1", json.dumps([10, 10]), 3, json.dumps([[1, 0]]), json.dumps([1, 0]), username))
                conn.commit()
                logger.info(f"Game state reset for user: {username}")
                return True
            else:
                logger.warning(f"User {username} not found")
                return False
    except Exception as e:
        logger.error(f"Error resetting game state: {e}")
        return False

def get_latest_game_state(username: str) -> Optional[Dict[str, Any]]:
    """Query the latest game state with proper error handling"""
    username = sanitize_input(username)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM game_state WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if result:
                return {
                    "username": result["username"],
                    "current_level_name": result["current_level_name"],
                    "map_size": json.loads(result["map_size"]),
                    "health": result["health"],
                    "path": json.loads(result["path"]),
                    "current_position": json.loads(result["current_position"]),
                    "message": "Load successful",
                    "cookies": [],
                    "status": 1
                }
            logger.warning(f"Game state not found for user: {username}")
            return None
    except Exception as e:
        logger.error(f"Error getting game state: {e}")
        return None
