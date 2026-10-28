"""Advantage features for a two-player, two-battlefield Riftbound position.

An observation vector, not an executable rules state or a calibrated score.
Rules basis: official Core Rules, 2026-10-09. See docs/game-state.md.
"""

from enum import IntEnum

import numpy as np


class StateEnum(IntEnum):
    """共93维，索引0-92。P0为己方，P1为对手；BF0/BF1为两个战场。"""

    # 0-14：局面时机、得分和各卡牌区域的数量。
    TURN_PLAYER = 0  # 当前回合属于谁：0=己方，1=对手；不表示此刻谁持有行动权。
    PHASE = 1  # 当前阶段：0准备、1唤醒、2开始、3计分、4引导符文、5抽牌、6主要、7结束、8到期。
    WINDOW = 2  # 当前开放窗口：0=普通开放，1=对决开放（含战斗对决）；不记录未结算的Chain。

    P0_SCORE = 3  # 己方当前累计得分，不是本回合新增分数。
    P1_SCORE = 4  # 对手当前累计得分，不是本回合新增分数。
    P0_DECK_COUNT = 5  # 己方主牌库剩余卡牌张数，不含符文牌库。
    P1_DECK_COUNT = 6  # 对手主牌库剩余卡牌张数，不含符文牌库。
    P0_RUNE_DECK_COUNT = 7  # 己方符文牌库剩余张数，不含已在场上的符文。
    P1_RUNE_DECK_COUNT = 8  # 对手符文牌库剩余张数，不含已在场上的符文。
    P0_HAND_COUNT = 9  # 己方当前手牌张数，不含指定英雄区和盖放区的卡牌。
    P1_HAND_COUNT = 10  # 对手当前手牌张数，不含指定英雄区和盖放区的卡牌。
    P0_TRASH_COUNT = 11  # 己方墓地中的卡牌张数，可参与回收和墓地效果；不是本回合死亡次数。
    P1_TRASH_COUNT = 12  # 对手墓地中的卡牌张数，可参与回收和墓地效果；不是本回合死亡次数。
    P0_CHAMPION_ZONE_COUNT = 13  # 己方指定英雄区中的卡牌张数，可从该区打出；不含手牌或场上英雄。
    P1_CHAMPION_ZONE_COUNT = 14  # 对手指定英雄区中的卡牌张数，可从该区打出；不含手牌或场上英雄。

    # 15-48：当前资源池、场上符文、经验值和装备。
    P0_ENERGY = 15  # 己方资源池中尚未花费的Energy，不含符文尚未产生的资源。
    P1_ENERGY = 16  # 对手资源池中尚未花费的Energy，不含符文尚未产生的资源。
    P0_POWER_FURY = 17  # 己方资源池中未花费的Fury领域Power，不含可回收符文的潜在产出。
    P1_POWER_FURY = 18  # 对手资源池中未花费的Fury领域Power，不含可回收符文的潜在产出。
    P0_POWER_CALM = 19  # 己方资源池中未花费的Calm领域Power，不含可回收符文的潜在产出。
    P1_POWER_CALM = 20  # 对手资源池中未花费的Calm领域Power，不含可回收符文的潜在产出。
    P0_POWER_MIND = 21  # 己方资源池中未花费的Mind领域Power，不含可回收符文的潜在产出。
    P1_POWER_MIND = 22  # 对手资源池中未花费的Mind领域Power，不含可回收符文的潜在产出。
    P0_POWER_BODY = 23  # 己方资源池中未花费的Body领域Power，不含可回收符文的潜在产出。
    P1_POWER_BODY = 24  # 对手资源池中未花费的Body领域Power，不含可回收符文的潜在产出。
    P0_POWER_CHAOS = 25  # 己方资源池中未花费的Chaos领域Power，不含可回收符文的潜在产出。
    P1_POWER_CHAOS = 26  # 对手资源池中未花费的Chaos领域Power，不含可回收符文的潜在产出。
    P0_POWER_ORDER = 27  # 己方资源池中未花费的Order领域Power，不含可回收符文的潜在产出。
    P1_POWER_ORDER = 28  # 对手资源池中未花费的Order领域Power，不含可回收符文的潜在产出。
    P0_POWER_UNIVERSAL = 29  # 己方资源池中未花费的通用Power，可支付任意领域的Power费用。
    P1_POWER_UNIVERSAL = 30  # 对手资源池中未花费的通用Power，可支付任意领域的Power费用。
    P0_RUNES_FURY = 31  # 己方控制的场上Fury领域符文数，含就绪和横置，不含符文牌库。
    P1_RUNES_FURY = 32  # 对手控制的场上Fury领域符文数，含就绪和横置，不含符文牌库。
    P0_RUNES_CALM = 33  # 己方控制的场上Calm领域符文数，含就绪和横置，不含符文牌库。
    P1_RUNES_CALM = 34  # 对手控制的场上Calm领域符文数，含就绪和横置，不含符文牌库。
    P0_RUNES_MIND = 35  # 己方控制的场上Mind领域符文数，含就绪和横置，不含符文牌库。
    P1_RUNES_MIND = 36  # 对手控制的场上Mind领域符文数，含就绪和横置，不含符文牌库。
    P0_RUNES_BODY = 37  # 己方控制的场上Body领域符文数，含就绪和横置，不含符文牌库。
    P1_RUNES_BODY = 38  # 对手控制的场上Body领域符文数，含就绪和横置，不含符文牌库。
    P0_RUNES_CHAOS = 39  # 己方控制的场上Chaos领域符文数，含就绪和横置，不含符文牌库。
    P1_RUNES_CHAOS = 40  # 对手控制的场上Chaos领域符文数，含就绪和横置，不含符文牌库。
    P0_RUNES_ORDER = 41  # 己方控制的场上Order领域符文数，含就绪和横置，不含符文牌库。
    P1_RUNES_ORDER = 42  # 对手控制的场上Order领域符文数，含就绪和横置，不含符文牌库。
    P0_READY_RUNES = 43  # 己方场上受其控制的未横置符文总数，跨全部领域统计。
    P1_READY_RUNES = 44  # 对手场上受其控制的未横置符文总数，跨全部领域统计。
    P0_XP = 45  # 己方当前持有的经验值，可用于Level条件及XP支付。
    P1_XP = 46  # 对手当前持有的经验值，可用于Level条件及XP支付。
    P0_GEAR_COUNT = 47  # 己方控制的场上非单位装备总数，包含附着装备和战场上的装备。
    P1_GEAR_COUNT = 48  # 对手控制的场上非单位装备总数，包含附着装备和战场上的装备。

    # 49-58：双方各自基地中的单位资产、就绪情况和受伤程度。
    P0_BASE_UNITS = 49  # 己方基地内己方单位总数，含就绪、横置和晕眩单位，也含单位衍生物。
    P1_BASE_UNITS = 50  # 对手基地内对手单位总数，含就绪、横置和晕眩单位，也含单位衍生物。
    P0_BASE_MIGHT = 51  # 己方基地内己方所有单位的当前战力之和；单体负值按0，不减标记伤害。
    P1_BASE_MIGHT = 52  # 对手基地内对手所有单位的当前战力之和；单体负值按0，不减标记伤害。
    P0_BASE_READY_UNITS = 53  # 己方基地内未横置的己方单位数量；不排除晕眩，能否行动仍受规则限制。
    P1_BASE_READY_UNITS = 54  # 对手基地内未横置的对手单位数量；不排除晕眩，能否行动仍受规则限制。
    P0_BASE_READY_MIGHT = 55  # 己方基地内未横置的己方单位当前战力之和；单体负值按0，不因晕眩扣除。
    P1_BASE_READY_MIGHT = 56  # 对手基地内未横置的对手单位当前战力之和；单体负值按0，不因晕眩扣除。
    P0_BASE_DAMAGE = 57  # 己方基地内仍在场的己方单位上已标记伤害总和，不从战力中扣除。
    P1_BASE_DAMAGE = 58  # 对手基地内仍在场的对手单位上已标记伤害总和，不从战力中扣除。

    # 59-75：战场0的控制、单位、盖放牌和计分记录。
    BF0_CONTROLLER = 59  # 战场0当前控制者：-1=无人控制，0=己方，1=对手；不是战场拥有者。
    BF0_P0_UNITS = 60  # 战场0内己方单位总数，含就绪、横置和晕眩单位，也含单位衍生物。
    BF0_P1_UNITS = 61  # 战场0内对手单位总数，含就绪、横置和晕眩单位，也含单位衍生物。
    BF0_P0_MIGHT = 62  # 战场0内己方所有单位的当前战力之和；单体负值按0，不减标记伤害。
    BF0_P1_MIGHT = 63  # 战场0内对手所有单位的当前战力之和；单体负值按0，不减标记伤害。
    BF0_P0_READY_UNITS = 64  # 战场0内未横置的己方单位数量；不排除晕眩，能否行动仍受规则限制。
    BF0_P1_READY_UNITS = 65  # 战场0内未横置的对手单位数量；不排除晕眩，能否行动仍受规则限制。
    BF0_P0_READY_MIGHT = 66  # 战场0内未横置的己方单位当前战力之和；单体负值按0，不因晕眩扣除。
    BF0_P1_READY_MIGHT = 67  # 战场0内未横置的对手单位当前战力之和；单体负值按0，不因晕眩扣除。
    BF0_P0_COMBAT_MIGHT = 68  # 战场0内非晕眩己方单位的当前战力之和，含横置单位；未计额外伤害或预防。
    BF0_P1_COMBAT_MIGHT = 69  # 战场0内非晕眩对手单位的当前战力之和，含横置单位；未计额外伤害或预防。
    BF0_P0_DAMAGE = 70  # 战场0内仍在场的己方单位上已标记伤害总和，不从战力中扣除。
    BF0_P1_DAMAGE = 71  # 战场0内仍在场的对手单位上已标记伤害总和，不从战力中扣除。
    BF0_P0_HIDDEN_CARDS = 72  # 战场0关联盖放区中由己方控制的盖放卡数量，不记录卡牌身份。
    BF0_P1_HIDDEN_CARDS = 73  # 战场0关联盖放区中由对手控制的盖放卡数量，不记录卡牌身份。
    BF0_P0_SCORED_THIS_TURN = 74  # 己方本回合是否已对战场0完成Scoring：0否、1是；不等同于获得了1分。
    BF0_P1_SCORED_THIS_TURN = 75  # 对手本回合是否已对战场0完成Scoring：0否、1是；不等同于获得了1分。

    # 76-92：战场1，统计口径与战场0相同。
    BF1_CONTROLLER = 76  # 战场1当前控制者：-1=无人控制，0=己方，1=对手；不是战场拥有者。
    BF1_P0_UNITS = 77  # 战场1内己方单位总数，含就绪、横置和晕眩单位，也含单位衍生物。
    BF1_P1_UNITS = 78  # 战场1内对手单位总数，含就绪、横置和晕眩单位，也含单位衍生物。
    BF1_P0_MIGHT = 79  # 战场1内己方所有单位的当前战力之和；单体负值按0，不减标记伤害。
    BF1_P1_MIGHT = 80  # 战场1内对手所有单位的当前战力之和；单体负值按0，不减标记伤害。
    BF1_P0_READY_UNITS = 81  # 战场1内未横置的己方单位数量；不排除晕眩，能否行动仍受规则限制。
    BF1_P1_READY_UNITS = 82  # 战场1内未横置的对手单位数量；不排除晕眩，能否行动仍受规则限制。
    BF1_P0_READY_MIGHT = 83  # 战场1内未横置的己方单位当前战力之和；单体负值按0，不因晕眩扣除。
    BF1_P1_READY_MIGHT = 84  # 战场1内未横置的对手单位当前战力之和；单体负值按0，不因晕眩扣除。
    BF1_P0_COMBAT_MIGHT = 85  # 战场1内非晕眩己方单位的当前战力之和，含横置单位；未计额外伤害或预防。
    BF1_P1_COMBAT_MIGHT = 86  # 战场1内非晕眩对手单位的当前战力之和，含横置单位；未计额外伤害或预防。
    BF1_P0_DAMAGE = 87  # 战场1内仍在场的己方单位上已标记伤害总和，不从战力中扣除。
    BF1_P1_DAMAGE = 88  # 战场1内仍在场的对手单位上已标记伤害总和，不从战力中扣除。
    BF1_P0_HIDDEN_CARDS = 89  # 战场1关联盖放区中由己方控制的盖放卡数量，不记录卡牌身份。
    BF1_P1_HIDDEN_CARDS = 90  # 战场1关联盖放区中由对手控制的盖放卡数量，不记录卡牌身份。
    BF1_P0_SCORED_THIS_TURN = 91  # 己方本回合是否已对战场1完成Scoring：0否、1是；不等同于获得了1分。
    BF1_P1_SCORED_THIS_TURN = 92  # 对手本回合是否已对战场1完成Scoring：0否、1是；不等同于获得了1分。



DOMAINS = ("Fury", "Calm", "Mind", "Body", "Chaos", "Order", "Universal")
VICTORY_SCORE = 8  # Fixed 1v1 profile, not a changing advantage feature.
STATE_SIZE = 93  # Vector indices 0-92.
STATE_FIELDS = tuple(StateEnum(index) for index in range(STATE_SIZE))

# Schema metadata only: all changing numeric values are in game_state.vector.
# Allowed values, not extra dimensions. See docs/game-state.md for meanings.
_ENUM_FIELDS = {
    StateEnum.TURN_PLAYER: (0, 1),
    StateEnum.PHASE: tuple(range(9)),
    StateEnum.WINDOW: (0, 1),
    StateEnum.BF0_CONTROLLER: (-1, 0, 1),
    StateEnum.BF1_CONTROLLER: (-1, 0, 1),
}
_FLAGS = tuple(index for index in STATE_FIELDS if index.name.endswith("SCORED_THIS_TURN"))
_DISCRETE = tuple(index for index in STATE_FIELDS
                  if not any(word in index.name for word in ("MIGHT", "DAMAGE", "ENERGY", "POWER")))
_LOCATIONS = ("P0_BASE", "P1_BASE", "BF0_P0", "BF0_P1", "BF1_P0", "BF1_P1")


class game_state:
    """One float64 vector of position features, without card/event records.

    Observe after chain resolution and associated cleanups, in an Open state.
    Default values are an empty setup snapshot, never unknown information.
    Direct vector writes are supported; call validate() after a batch of writes.
    """

    __slots__ = ("vector",)

    def __init__(self, vector=None):
        if vector is None:
            self.vector = np.zeros(STATE_SIZE, dtype=np.float64)
            for index, values in _ENUM_FIELDS.items():
                self.vector[index] = values[0]
        else:
            array = np.asarray(vector)
            if array.dtype.kind not in "iuf":
                raise ValueError("State vector must contain real numbers")
            self.vector = np.array(array, dtype=np.float64, copy=True)
        self.validate()

    @staticmethod
    def _index(index):
        return StateEnum(index)

    def __getitem__(self, index: StateEnum) -> float:
        return float(self.vector[self._index(index)])

    def __setitem__(self, index: StateEnum, value: float):
        self.update({index: value})

    def update(self, values: dict[StateEnum, float]):
        """Validate an entire update before changing the current vector."""
        candidate = self.vector.copy()
        for index, value in values.items():
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
                raise ValueError("State values must be real numbers; use 0/1 for flags")
            candidate[self._index(index)] = value
        next_state = type(self)(candidate)
        self.vector[:] = next_state.vector

    def copy(self):
        return type(self)(self.vector)

    def to_vector(self) -> np.ndarray:
        """Return an independent copy for matrix calculations."""
        return self.vector.copy()

    def as_features(self) -> dict[str, float]:
        return {index.name: float(self.vector[index]) for index in STATE_FIELDS}

    def validate(self):
        """Validate observation values, not action legality or effect resolution."""
        vector = self.vector
        if not isinstance(vector, np.ndarray) or vector.shape != (STATE_SIZE,) or vector.dtype != np.float64:
            raise ValueError(f"Expected a float64 vector of shape ({STATE_SIZE},)")
        if not np.isfinite(vector).all():
            raise ValueError("Unknown/nonfinite state values must not be silently replaced by zero")
        if np.any(vector[list(_DISCRETE)] != np.floor(vector[list(_DISCRETE)])):
            raise ValueError("Counts, flags and enum codes must be integers")
        for index in STATE_FIELDS:
            if index in _ENUM_FIELDS:
                if vector[index] not in _ENUM_FIELDS[index]:
                    raise ValueError(f"Invalid {index.name}")
            elif vector[index] < 0:
                raise ValueError(f"{index.name} must be nonnegative")
        if any(vector[index] not in (0, 1) for index in _FLAGS):
            raise ValueError("Scored flags must be 0 or 1")
        for player in (0, 1):
            runes = sum(vector[StateEnum[f"P{player}_RUNES_{domain.upper()}"]] for domain in DOMAINS[:6])
            if vector[StateEnum[f"P{player}_READY_RUNES"]] > runes:
                raise ValueError("Ready runes cannot exceed the runes on board")
        for prefix in _LOCATIONS:
            values = {name: vector[StateEnum[f"{prefix}_{name}"]]
                      for name in ("UNITS", "MIGHT", "READY_UNITS", "READY_MIGHT", "DAMAGE")}
            if values["READY_UNITS"] > values["UNITS"] or values["READY_MIGHT"] > values["MIGHT"]:
                raise ValueError(f"{prefix}: ready quantities cannot exceed totals")
            if values["READY_UNITS"] == 0 and values["READY_MIGHT"] != 0:
                raise ValueError(f"{prefix}: no ready units means no ready Might")
            if values["UNITS"] == 0 and any(values[name] != 0 for name in ("MIGHT", "READY_MIGHT", "DAMAGE")):
                raise ValueError(f"{prefix}: no units means no unit Might or marked damage")
            if prefix.startswith("BF") and vector[StateEnum[f"{prefix}_COMBAT_MIGHT"]] > values["MIGHT"]:
                raise ValueError(f"{prefix}: unstunned Might cannot exceed total Might")
