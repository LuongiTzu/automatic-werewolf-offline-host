"""Vote service."""
import uuid
from collections import Counter

from sqlalchemy.orm import Session

from app.models import GamePhase, Player, Room, Vote
from app.services.game_log_service import GameLogService


class VoteService:
    """Validate, store and summarize votes."""

    @staticmethod
    def submit_vote(
        db: Session,
        room: Room,
        voter_player_id: str,
        session_token: str,
        target_player_id: str,
    ) -> dict:
        if room.current_phase != GamePhase.VOTING:
            raise ValueError("Voting is not active")

        voter = db.query(Player).filter(Player.id == voter_player_id, Player.room_id == room.id).first()
        if not voter:
            raise ValueError("Voter not found in this room")
        if voter.session_token != session_token:
            raise PermissionError("Invalid session token")
        if not voter.is_alive:
            raise ValueError("Dead players cannot vote")

        target = db.query(Player).filter(Player.id == target_player_id, Player.room_id == room.id).first()
        if not target:
            raise ValueError("Target player not found in this room")
        if not target.is_alive:
            raise ValueError("Cannot vote for a dead player")

        vote = db.query(Vote).filter(
            Vote.room_id == room.id,
            Vote.day_number == room.day_number,
            Vote.voter_player_id == voter.id,
        ).first()

        if vote:
            vote.target_player_id = target.id
        else:
            vote = Vote(
                id=str(uuid.uuid4()),
                room_id=room.id,
                day_number=room.day_number,
                voter_player_id=voter.id,
                target_player_id=target.id,
            )
            db.add(vote)

        db.commit()
        db.refresh(vote)

        GameLogService.log(
            db,
            room,
            event_type="VOTE_SUBMITTED",
            message=f"{voter.name} voted for {target.name}",
            data={
                "voter_player_id": voter.id,
                "voter_name": voter.name,
                "target_player_id": target.id,
                "target_name": target.name,
            },
        )

        return VoteService.get_vote_summary(db, room)

    @staticmethod
    def get_vote_summary(db: Session, room: Room) -> dict:
        votes = db.query(Vote).filter(
            Vote.room_id == room.id,
            Vote.day_number == room.day_number,
        ).all()
        alive_players = db.query(Player).filter(Player.room_id == room.id, Player.is_alive.is_(True)).all()
        player_map = {p.id: p for p in alive_players}

        counts = Counter(v.target_player_id for v in votes)
        ranking = []
        for player_id, count in counts.most_common():
            player = player_map.get(player_id)
            ranking.append({
                "player_id": player_id,
                "player_name": player.name if player else "Unknown",
                "votes": count,
            })

        return {
            "day_number": room.day_number,
            "total_alive": len(alive_players),
            "total_votes": len(votes),
            "ranking": ranking,
            "voted_player_ids": [v.voter_player_id for v in votes],
        }
