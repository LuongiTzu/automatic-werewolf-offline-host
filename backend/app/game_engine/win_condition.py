"""Win condition resolver for MVP."""
from sqlalchemy.orm import Session

from app.game_engine.constants import ROLE_WEREWOLF, WINNER_VILLAGERS, WINNER_WEREWOLVES
from app.models import Player, Room, RoomStatus, GamePhase


class WinCondition:
    """MVP win rules: Villagers vs Werewolves."""

    @staticmethod
    def check_game_over(db: Session, room: Room) -> str | None:
        alive_players = db.query(Player).filter(
            Player.room_id == room.id,
            Player.is_alive.is_(True),
        ).all()

        werewolves = [p for p in alive_players if p.role_code == ROLE_WEREWOLF or p.side == "werewolf"]
        villagers = [p for p in alive_players if p not in werewolves]

        if len(werewolves) == 0:
            return WINNER_VILLAGERS

        if len(werewolves) >= len(villagers):
            return WINNER_WEREWOLVES

        return None

    @staticmethod
    def apply_game_over_if_needed(db: Session, room: Room) -> str | None:
        winner = WinCondition.check_game_over(db, room)
        if not winner:
            return None

        room.status = RoomStatus.ENDED
        room.current_phase = GamePhase.ENDED
        room.is_game_over = True
        room.winner = winner
        room.current_role_turn = None
        room.phase_ends_at = None
        room.current_audio_text = (
            "Trò chơi kết thúc. Phe Dân Làng chiến thắng."
            if winner == WINNER_VILLAGERS
            else "Trò chơi kết thúc. Phe Ma Sói chiến thắng."
        )
        db.add(room)
        db.commit()
        db.refresh(room)
        return winner
