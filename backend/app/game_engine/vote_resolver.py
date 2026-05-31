"""Vote resolver."""
from collections import Counter
from sqlalchemy.orm import Session

from app.models import Player, Room, Vote
from app.services.game_log_service import GameLogService


class VoteResolver:
    """Resolve day vote result."""

    @staticmethod
    def resolve_vote(db: Session, room: Room) -> dict:
        votes = db.query(Vote).filter(
            Vote.room_id == room.id,
            Vote.day_number == room.day_number,
        ).all()

        if not votes:
            result = {
                "day_number": room.day_number,
                "eliminated_player": None,
                "is_tie": True,
                "message": "Không ai bỏ phiếu. Không ai bị treo cổ trong lượt này.",
            }
            GameLogService.log(db, room, "VOTE_RESOLVED", result["message"], result)
            return result

        counts = Counter(v.target_player_id for v in votes)
        max_votes = max(counts.values())
        top_targets = [player_id for player_id, count in counts.items() if count == max_votes]

        if len(top_targets) != 1:
            result = {
                "day_number": room.day_number,
                "eliminated_player": None,
                "is_tie": True,
                "message": "Kết quả bỏ phiếu hòa. Không ai bị treo cổ trong lượt này.",
            }
            GameLogService.log(db, room, "VOTE_RESOLVED", result["message"], result)
            return result

        eliminated = db.query(Player).filter(
            Player.room_id == room.id,
            Player.id == top_targets[0],
            Player.is_alive.is_(True),
        ).first()

        if eliminated:
            eliminated.is_alive = False
            db.add(eliminated)
            db.commit()
            db.refresh(eliminated)

        result = {
            "day_number": room.day_number,
            "eliminated_player": {"id": eliminated.id, "name": eliminated.name} if eliminated else None,
            "is_tie": False,
            "message": f"Người bị treo cổ là: {eliminated.name}." if eliminated else "Không ai bị treo cổ.",
        }
        GameLogService.log(db, room, "VOTE_RESOLVED", result["message"], result)
        return result
