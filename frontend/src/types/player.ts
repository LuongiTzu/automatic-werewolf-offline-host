export interface PlayerInRoom {
  id: string
  name: string
  is_alive: boolean
  is_connected: boolean
  is_ready?: boolean
}

export interface PlayerRole {
  player_id: string
  player_name: string
  room_id: string
  role_code: string
  role_name: string
  side: string
  description?: string
  night_order?: number | null
}

export interface NightTarget {
  id: string
  name: string
  is_alive?: boolean
}

export function roleName(roleCode?: string | null): string {
  const map: Record<string, string> = {
    VILLAGER: 'Dân làng',
    WEREWOLF: 'Ma Sói',
    GUARD: 'Bảo vệ',
    SEER: 'Tiên tri',
    WITCH: 'Phù thủy',
    HUNTER: 'Thợ săn',
    CUPID: 'Cupid',
    OILMAN: 'Kẻ tẩm dầu',
    FOOL: 'Thằng Khờ',
    CURSED_WOLF: 'Sói nguyền',
  }
  return roleCode ? map[roleCode] || roleCode : 'Chưa có'
}

export function sideName(side?: string | null): string {
  const map: Record<string, string> = {
    villager: 'Phe Dân',
    werewolf: 'Phe Sói',
    special: 'Phe thứ ba',
  }
  return side ? map[side] || side : 'Chưa rõ'
}
