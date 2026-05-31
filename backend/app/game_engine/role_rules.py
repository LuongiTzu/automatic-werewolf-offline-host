"""Night role order and role turn helpers."""
from app.game_engine.constants import (
    PUBLIC_ROLE_NAMES,
    ROLE_GUARD,
    ROLE_SEER,
    ROLE_TURN_SECONDS,
    ROLE_WEREWOLF,
    ROLE_WITCH,
)
from app.models import Player

MVP_NIGHT_ORDER = [ROLE_GUARD, ROLE_WEREWOLF, ROLE_WITCH, ROLE_SEER]

ROLE_AUDIO_TEXT = {
    ROLE_GUARD: [
        "Bảo vệ thức dậy.",
        "Bảo vệ hãy chọn một người để bảo vệ trong đêm nay.",
    ],
    ROLE_WEREWOLF: [
        "Ma Sói thức dậy.",
        "Ma Sói hãy nhìn nhau và chọn một người để cắn.",
    ],
    ROLE_WITCH: [
        "Phù thủy thức dậy.",
        "Phù thủy hãy quyết định có dùng bình cứu hoặc bình độc không.",
    ],
    ROLE_SEER: [
        "Tiên tri thức dậy.",
        "Tiên tri hãy chọn một người để soi.",
    ],
}

ROLE_SLEEP_TEXT = {
    ROLE_GUARD: "Bảo vệ đã chọn xong. Bảo vệ đi ngủ.",
    ROLE_WEREWOLF: "Ma Sói đã chọn xong. Ma Sói đi ngủ.",
    ROLE_WITCH: "Phù thủy đã chọn xong. Phù thủy đi ngủ.",
    ROLE_SEER: "Tiên tri đã nhận kết quả. Tiên tri đi ngủ.",
}


def get_existing_alive_night_roles(players: list[Player]) -> list[str]:
    """Return the role order that exists in this room and has at least one alive actor."""
    alive_roles = {p.role_code for p in players if p.is_alive and p.role_code}
    return [role for role in MVP_NIGHT_ORDER if role in alive_roles]


def get_role_turn_seconds(role_code: str) -> int:
    return ROLE_TURN_SECONDS.get(role_code, 20)


def get_role_name(role_code: str) -> str:
    return PUBLIC_ROLE_NAMES.get(role_code, role_code)


def get_role_audio_text(role_code: str) -> str:
    return " ".join(ROLE_AUDIO_TEXT.get(role_code, [f"{get_role_name(role_code)} thức dậy."]))


def get_role_sleep_text(role_code: str) -> str:
    return ROLE_SLEEP_TEXT.get(role_code, f"{get_role_name(role_code)} đi ngủ.")
