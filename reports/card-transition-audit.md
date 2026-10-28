# 全牌库状态转移验收

本报告覆盖全部印刷记录，使用本地已溯源的实际基础费用，不再使用测试费用假设；场景通过不代表完整对局规则已实现。

```json
{
  "records": 1407,
  "distinct_card_ids": 1407,
  "distinct_card_names": 1103,
  "statuses": {
    "unsupported": 1380,
    "isolated_scenarios_passed": 27
  },
  "reason_counts": {
    "unmapped_text": 1346,
    "unsupported_type": 254,
    "token_lifecycle": 14
  },
  "payment_data_verified": 1143,
  "isolated_play_verified": 27,
  "full_game_verified": 0,
  "scenario_checks": 346,
  "all_cards_verified": false
}
```

## 原因说明

- unmapped_text：完整文本包含未支持的条件、关键词、目标、选择、区域或持续效果，整张卡拒绝生成部分矩阵。
- unsupported_type：传奇、战场、符文等没有普通手牌出牌的生命周期模型。
- token_lifecycle：衍生物需由效果创建／移除，不能按普通卡牌抽取、支付或进入墓地处理。
- missing_power_total / missing_power_glyphs：费用总量或支付符号未认证；不把空值当零，也不按颜色猜符号。
- missing_energy / missing_might：普通可打出牌缺少必要属性。
- isolated_scenarios_passed：使用实际已溯源费用通过孤立场景，完整对局互动仍未实现。
- implementation_failure：场景执行出现意外异常或违反验收性质；原因数量可能重叠。

## 每张牌的状态

| 卡牌 ID | 名称 | 状态 | 原因 |
| --- | --- | --- | --- |
| OGN-001 | Blazing Scorcher | unsupported | unmapped_text |
| OGN-002 | Brazen Buccaneer | unsupported | unmapped_text |
| OGN-003 | Chemtech Enforcer | unsupported | unmapped_text |
| OGN-004 | Cleave | unsupported | unmapped_text |
| OGN-005 | Disintegrate | unsupported | unmapped_text |
| OGN-006 | Flame Chompers | unsupported | unmapped_text |
| OGN-007 | Fury Rune | unsupported | unsupported_type |
| OGN-007A | Fury Rune | unsupported | unsupported_type |
| OGN-008 | Get Excited! | unsupported | unmapped_text |
| OGN-009 | Hextech Ray | isolated_scenarios_passed |  |
| OGN-010 | Legion Rearguard | unsupported | unmapped_text |
| OGN-011 | Magma Wurm | unsupported | unmapped_text |
| OGN-012 | Noxus Hopeful | isolated_scenarios_passed |  |
| OGN-013 | Pouty Poro | unsupported | unmapped_text |
| OGN-014 | Sky Splitter | unsupported | unmapped_text |
| OGN-015 | Captain Farron | unsupported | unmapped_text |
| OGN-016 | Dangerous Duo | unsupported | unmapped_text |
| OGN-017 | Iron Ballista | unsupported | unmapped_text |
| OGN-018 | Noxus Saboteur | unsupported | unmapped_text |
| OGN-019 | Raging Soul | unsupported | unmapped_text |
| OGN-020 | Scrapyard Champion | unsupported | unmapped_text |
| OGN-021 | Sun Disc | unsupported | unmapped_text |
| OGN-022 | Thermo Beam | unsupported | unmapped_text |
| OGN-023 | Unlicensed Armory | unsupported | unmapped_text |
| OGN-024 | Void Seeker | isolated_scenarios_passed |  |
| OGN-025 | Blind Fury | unsupported | unmapped_text |
| OGN-026 | Brynhir Thundersong | unsupported | unmapped_text |
| OGN-027 | Darius, Trifarian | unsupported | unmapped_text |
| OGN-027A | Darius, Trifarian | unsupported | unmapped_text |
| OGN-028 | Draven, Showboat | unsupported | unmapped_text |
| OGN-029 | Falling Star | isolated_scenarios_passed |  |
| OGN-030 | Jinx, Demolitionist | unsupported | unmapped_text |
| OGN-030A | Jinx, Demolitionist | unsupported | unmapped_text |
| OGN-031 | Raging Firebrand | unsupported | unmapped_text |
| OGN-032 | Ravenborn Tome | unsupported | unmapped_text |
| OGN-033 | Shakedown | unsupported | unmapped_text |
| OGN-034 | Tryndamere, Barbarian | unsupported | unmapped_text |
| OGN-035 | Vayne, Hunter | unsupported | unmapped_text |
| OGN-036 | Vi, Destructive | unsupported | unmapped_text |
| OGN-037 | Immortal Phoenix | unsupported | unmapped_text |
| OGN-038 | Kadregrin the Infernal | unsupported | unmapped_text |
| OGN-039 | Kai'Sa, Survivor | unsupported | unmapped_text |
| OGN-039A | Kai'Sa, Survivor | unsupported | unmapped_text |
| OGN-040 | Seal of Rage | unsupported | unmapped_text |
| OGN-041 | Volibear, Furious | unsupported | unmapped_text |
| OGN-041A | Volibear, Furious | unsupported | unmapped_text |
| OGN-042 | Calm Rune | unsupported | unsupported_type |
| OGN-042A | Calm Rune | unsupported | unsupported_type |
| OGN-043 | Charm | unsupported | unmapped_text |
| OGN-044 | Clockwork Keeper | unsupported | unmapped_text |
| OGN-045 | Defy | unsupported | unmapped_text |
| OGN-046 | En Garde | unsupported | unmapped_text |
| OGN-047 | Find Your Center | unsupported | unmapped_text |
| OGN-048 | Meditation | unsupported | unmapped_text |
| OGN-049 | Playful Phantom | isolated_scenarios_passed |  |
| OGN-050 | Rune Prison | unsupported | unmapped_text |
| OGN-051 | Solari Shieldbearer | unsupported | unmapped_text |
| OGN-052 | Stalwart Poro | unsupported | unmapped_text |
| OGN-053 | Stand United | unsupported | unmapped_text |
| OGN-054 | Sunlit Guardian | unsupported | unmapped_text |
| OGN-055 | Wielder of Water | unsupported | unmapped_text |
| OGN-056 | Adaptatron | unsupported | unmapped_text |
| OGN-057 | Block | unsupported | unmapped_text |
| OGN-058 | Discipline | isolated_scenarios_passed |  |
| OGN-059 | Eclipse Herald | unsupported | unmapped_text |
| OGN-060 | Mask of Foresight | unsupported | unmapped_text |
| OGN-061 | Poro Herder | unsupported | unmapped_text |
| OGN-062 | Reinforce | unsupported | unmapped_text |
| OGN-063 | Spirit's Refuge | unsupported | unmapped_text |
| OGN-064 | Wind Wall | unsupported | unmapped_text |
| OGN-065 | Wizened Elder | unsupported | unmapped_text |
| OGN-066 | Ahri, Alluring | unsupported | unmapped_text |
| OGN-066A | Ahri, Alluring | unsupported | unmapped_text |
| OGN-067 | Blitzcrank, Impassive | unsupported | unmapped_text |
| OGN-068 | Caitlyn, Patrolling | unsupported | unmapped_text |
| OGN-069 | Last Stand | unsupported | unmapped_text |
| OGN-070 | Mageseeker Warden | unsupported | unmapped_text |
| OGN-071 | Party Favors | unsupported | unmapped_text |
| OGN-072 | Solari Shrine | unsupported | unmapped_text |
| OGN-073 | Sona, Harmonious | unsupported | unmapped_text |
| OGN-074 | Taric, Protector | unsupported | unmapped_text |
| OGN-075 | Tasty Faefolk | unsupported | unmapped_text |
| OGN-076 | Yasuo, Remorseful | unsupported | unmapped_text |
| OGN-076A | Yasuo, Remorseful | unsupported | unmapped_text |
| OGN-077 | Zhonya's Hourglass | unsupported | unmapped_text |
| OGN-078 | Lee Sin, Ascetic | unsupported | unmapped_text |
| OGN-078A | Lee Sin, Ascetic | unsupported | unmapped_text |
| OGN-079 | Leona, Zealot | unsupported | unmapped_text |
| OGN-079A | Leona, Zealot | unsupported | unmapped_text |
| OGN-080 | Mystic Reversal | unsupported | unmapped_text |
| OGN-081 | Seal of Focus | unsupported | unmapped_text |
| OGN-082 | Whiteflame Protector | isolated_scenarios_passed |  |
| OGN-083 | Consult the Past | unsupported | unmapped_text |
| OGN-084 | Eager Apprentice | unsupported | unmapped_text |
| OGN-085 | Falling Comet | isolated_scenarios_passed |  |
| OGN-086 | Jeweled Colossus | unsupported | unmapped_text |
| OGN-087 | Lecturing Yordle | unsupported | unmapped_text |
| OGN-088 | Mega-Mech | isolated_scenarios_passed |  |
| OGN-089 | Mind Rune | unsupported | unsupported_type |
| OGN-089A | Mind Rune | unsupported | unsupported_type |
| OGN-090 | Orb of Regret | unsupported | unmapped_text |
| OGN-091 | Pit Crew | unsupported | unmapped_text |
| OGN-092 | Riptide Rex | unsupported | unmapped_text |
| OGN-093 | Smoke Screen | unsupported | unmapped_text |
| OGN-094 | Sprite Call | unsupported | unmapped_text |
| OGN-095 | Stupefy | unsupported | unmapped_text |
| OGN-096 | Watchful Sentry | unsupported | unmapped_text |
| OGN-097 | Blastcone Fae | unsupported | unmapped_text |
| OGN-098 | Energy Conduit | unsupported | unmapped_text |
| OGN-099 | Garbage Grabber | unsupported | unmapped_text |
| OGN-100 | Gemcraft Seer | unsupported | unmapped_text |
| OGN-101 | Mushroom Pouch | unsupported | unmapped_text |
| OGN-102 | Portal Rescue | unsupported | unmapped_text |
| OGN-103 | Ravenbloom Student | unsupported | unmapped_text |
| OGN-104 | Retreat | unsupported | unmapped_text |
| OGN-105 | Singularity | unsupported | unmapped_text |
| OGN-106 | Sprite Mother | unsupported | unmapped_text |
| OGN-107 | Ava Achiever | unsupported | unmapped_text |
| OGN-108 | Convergent Mutation | unsupported | unmapped_text |
| OGN-109 | Dr. Mundo, Expert | unsupported | unmapped_text |
| OGN-110 | Ekko, Recurrent | unsupported | unmapped_text |
| OGN-111 | Heimerdinger, Inventor | unsupported | unmapped_text |
| OGN-112 | Kai'Sa, Evolutionary | unsupported | unmapped_text |
| OGN-112A | Kai'Sa, Evolutionary | unsupported | unmapped_text |
| OGN-113 | Malzahar, Fanatic | unsupported | unmapped_text |
| OGN-114 | Progress Day | isolated_scenarios_passed |  |
| OGN-115 | Promising Future | unsupported | unmapped_text |
| OGN-116 | Thousand-Tailed Watcher | unsupported | unmapped_text |
| OGN-117 | Viktor, Innovator | unsupported | unmapped_text |
| OGN-117A | Viktor, Innovator | unsupported | unmapped_text |
| OGN-118 | Wraith of Echoes | unsupported | unmapped_text |
| OGN-119 | Ahri, Inquisitive | unsupported | unmapped_text |
| OGN-119A | Ahri, Inquisitive | unsupported | unmapped_text |
| OGN-120 | Seal of Insight | unsupported | unmapped_text |
| OGN-121 | Teemo, Strategist | unsupported | unmapped_text |
| OGN-121A | Teemo, Strategist | unsupported | unmapped_text |
| OGN-122 | Time Warp | unsupported | unmapped_text |
| OGN-123 | Unchecked Power | unsupported | unmapped_text |
| OGN-124 | Arena Bar | unsupported | unmapped_text |
| OGN-125 | Bilgewater Bully | unsupported | unmapped_text |
| OGN-126 | Body Rune | unsupported | unsupported_type |
| OGN-126A | Body Rune | unsupported | unsupported_type |
| OGN-127 | Cannon Barrage | unsupported | unmapped_text |
| OGN-128 | Challenge | unsupported | unmapped_text |
| OGN-129 | Confront | unsupported | unmapped_text |
| OGN-130 | Crackshot Corsair | unsupported | unmapped_text |
| OGN-131 | Dune Drake | unsupported | unmapped_text |
| OGN-132 | First Mate | unsupported | unmapped_text |
| OGN-133 | Flurry of Blades | unsupported | unmapped_text |
| OGN-134 | Mobilize | unsupported | unmapped_text |
| OGN-135 | Pakaa Cub | unsupported | unmapped_text |
| OGN-136 | Pit Rookie | unsupported | unmapped_text |
| OGN-137 | Stormclaw Ursine | unsupported | unmapped_text |
| OGN-138 | Catalyst of Aeons | unsupported | unmapped_text |
| OGN-139 | Cithria of Cloudfield | unsupported | unmapped_text |
| OGN-140 | Herald of Scales | unsupported | unmapped_text |
| OGN-141 | Kinkou Monk | unsupported | unmapped_text |
| OGN-142 | Mountain Drake | isolated_scenarios_passed |  |
| OGN-143 | Pirate's Haven | unsupported | unmapped_text |
| OGN-144 | Spoils of War | unsupported | unmapped_text |
| OGN-145 | Unyielding Spirit | unsupported | unmapped_text |
| OGN-146 | Wallop | unsupported | unmapped_text |
| OGN-147 | Wildclaw Shaman | unsupported | unmapped_text |
| OGN-148 | Anivia, Primal | unsupported | unmapped_text |
| OGN-149 | Carnivorous Snapvine | unsupported | unmapped_text |
| OGN-150 | Kraken Hunter | unsupported | unmapped_text |
| OGN-151 | Lee Sin, Centered | unsupported | unmapped_text |
| OGN-151A | Lee Sin, Centered | unsupported | unmapped_text |
| OGN-152 | Mistfall | unsupported | unmapped_text |
| OGN-153 | Overt Operation | unsupported | unmapped_text |
| OGN-154 | Primal Strength | isolated_scenarios_passed |  |
| OGN-155 | Qiyana, Victorious | unsupported | unmapped_text |
| OGN-156 | Sabotage | unsupported | unmapped_text |
| OGN-157 | Udyr, Wildman | unsupported | unmapped_text |
| OGN-158 | Volibear, Imposing | unsupported | unmapped_text |
| OGN-158A | Volibear, Imposing | unsupported | unmapped_text |
| OGN-159 | Warwick, Hunter | unsupported | unmapped_text |
| OGN-160 | Dazzling Aurora | unsupported | unmapped_text |
| OGN-161 | Deadbloom Predator | unsupported | unmapped_text |
| OGN-162 | Miss Fortune, Captain | unsupported | unmapped_text |
| OGN-162A | Miss Fortune, Captain | unsupported | unmapped_text |
| OGN-163 | Seal of Strength | unsupported | unmapped_text |
| OGN-164 | Sett, Brawler | unsupported | unmapped_text |
| OGN-164A | Sett, Brawler | unsupported | unmapped_text |
| OGN-165 | Cemetery Attendant | unsupported | unmapped_text |
| OGN-166 | Chaos Rune | unsupported | unsupported_type |
| OGN-166A | Chaos Rune | unsupported | unsupported_type |
| OGN-167 | Ember Monk | unsupported | unmapped_text |
| OGN-168 | Fight or Flight | unsupported | unmapped_text |
| OGN-169 | Gust | unsupported | unmapped_text |
| OGN-170 | Morbid Return | unsupported | unmapped_text |
| OGN-171 | Mystic Poro | unsupported | unmapped_text |
| OGN-172 | Rebuke | unsupported | unmapped_text |
| OGN-173 | Ride the Wind | unsupported | unmapped_text |
| OGN-174 | Sai Scout | unsupported | unmapped_text |
| OGN-175 | Shipyard Skulker | isolated_scenarios_passed |  |
| OGN-176 | Sneaky Deckhand | unsupported | unmapped_text |
| OGN-177 | Stealthy Pursuer | unsupported | unmapped_text |
| OGN-178 | Undercover Agent | unsupported | unmapped_text |
| OGN-179 | Acceptable Losses | unsupported | unmapped_text |
| OGN-180 | Fading Memories | unsupported | unmapped_text |
| OGN-181 | Pack of Wonders | unsupported | unmapped_text |
| OGN-182 | Scrapheap | unsupported | unmapped_text |
| OGN-183 | Stacked Deck | unsupported | unmapped_text |
| OGN-184 | The Syren | unsupported | unmapped_text |
| OGN-185 | Traveling Merchant | unsupported | unmapped_text |
| OGN-186 | Treasure Trove | unsupported | unmapped_text |
| OGN-187 | Whirlwind | unsupported | unmapped_text |
| OGN-188 | Zaunite Bouncer | unsupported | unmapped_text |
| OGN-189 | Kayn, Unleashed | unsupported | unmapped_text |
| OGN-190 | Kog'Maw, Caustic | unsupported | unmapped_text |
| OGN-191 | Maddened Marauder | unsupported | unmapped_text |
| OGN-192 | Mindsplitter | unsupported | unmapped_text |
| OGN-193 | Miss Fortune, Buccaneer | unsupported | unmapped_text |
| OGN-193A | Miss Fortune, Buccaneer | unsupported | unmapped_text |
| OGN-194 | Nocturne, Horrifying | unsupported | unmapped_text |
| OGN-195 | Rhasa the Sunderer | isolated_scenarios_passed |  |
| OGN-196 | Soulgorger | unsupported | unmapped_text |
| OGN-197 | Teemo, Scout | unsupported | unmapped_text |
| OGN-197A | Teemo, Scout | unsupported | unmapped_text |
| OGN-198 | The Harrowing | unsupported | unmapped_text |
| OGN-199 | Tideturner | unsupported | unmapped_text |
| OGN-200 | Twisted Fate, Gambler | unsupported | unmapped_text |
| OGN-201 | Invert Timelines | unsupported | unmapped_text |
| OGN-202 | Jinx, Rebel | unsupported | unmapped_text |
| OGN-202A | Jinx, Rebel | unsupported | unmapped_text |
| OGN-203 | Possession | unsupported | unmapped_text |
| OGN-204 | Seal of Discord | unsupported | unmapped_text |
| OGN-205 | Yasuo, Windrider | unsupported | unmapped_text |
| OGN-205A | Yasuo, Windrider | unsupported | unmapped_text |
| OGN-206 | Back to Back | unsupported | unmapped_text |
| OGN-207 | Call to Glory | unsupported | unmapped_text |
| OGN-208 | Cruel Patron | unsupported | unmapped_text |
| OGN-209 | Cull the Weak | unsupported | unmapped_text |
| OGN-210 | Daring Poro | unsupported | unmapped_text |
| OGN-211 | Faithful Manufactor | unsupported | unmapped_text |
| OGN-212 | Forge of the Future | unsupported | unmapped_text |
| OGN-213 | Hidden Blade | unsupported | unmapped_text |
| OGN-214 | Order Rune | unsupported | unsupported_type |
| OGN-214A | Order Rune | unsupported | unsupported_type |
| OGN-215 | Petty Officer | unsupported | unmapped_text |
| OGN-216 | Soaring Scout | unsupported | unmapped_text |
| OGN-217 | Trifarian Gloryseeker | unsupported | unmapped_text |
| OGN-218 | Vanguard Captain | unsupported | unmapped_text |
| OGN-219 | Vanguard Sergeant | isolated_scenarios_passed |  |
| OGN-220 | Facebreaker | unsupported | unmapped_text |
| OGN-221 | Imperial Decree | unsupported | unmapped_text |
| OGN-222 | Noxian Drummer | unsupported | unmapped_text |
| OGN-223 | Peak Guardian | unsupported | unmapped_text |
| OGN-224 | Salvage | unsupported | unmapped_text |
| OGN-225 | Solari Chief | unsupported | unmapped_text |
| OGN-226 | Spectral Matron | unsupported | unmapped_text |
| OGN-227 | Symbol of the Solari | unsupported | unmapped_text |
| OGN-228 | Vanguard Helm | unsupported | unmapped_text |
| OGN-229 | Vengeance | isolated_scenarios_passed |  |
| OGN-230 | Albus Ferros | unsupported | unmapped_text |
| OGN-231 | Commander Ledros | unsupported | unmapped_text |
| OGN-232 | Fiora, Victorious | unsupported | unmapped_text |
| OGN-233 | Grand Strategem | unsupported | unmapped_text |
| OGN-234 | Harnessed Dragon | unsupported | unmapped_text |
| OGN-235 | Karma, Channeler | unsupported | unmapped_text |
| OGN-236 | Karthus, Eternal | unsupported | unmapped_text |
| OGN-237 | King's Edict | unsupported | unmapped_text |
| OGN-238 | Leona, Determined | unsupported | unmapped_text |
| OGN-238A | Leona, Determined | unsupported | unmapped_text |
| OGN-239 | Machine Evangel | unsupported | unmapped_text |
| OGN-240 | Sett, Kingpin | unsupported | unmapped_text |
| OGN-240A | Sett, Kingpin | unsupported | unmapped_text |
| OGN-241 | Shen, Kinkou | unsupported | unmapped_text |
| OGN-242 | Baited Hook | unsupported | unmapped_text |
| OGN-243 | Darius, Executioner | unsupported | unmapped_text |
| OGN-243A | Darius, Executioner | unsupported | unmapped_text |
| OGN-244 | Divine Judgment | unsupported | unmapped_text |
| OGN-245 | Seal of Unity | unsupported | unmapped_text |
| OGN-246 | Viktor, Leader | unsupported | unmapped_text |
| OGN-246A | Viktor, Leader | unsupported | unmapped_text |
| OGN-247 | Daughter of the Void | unsupported | unsupported_type; unmapped_text |
| OGN-248 | Icathian Rain, Kai'Sa | isolated_scenarios_passed |  |
| OGN-249 | Relentless Storm | unsupported | unsupported_type; unmapped_text |
| OGN-250 | Stormbringer, Volibear | unsupported | unmapped_text |
| OGN-251 | Loose Cannon | unsupported | unsupported_type; unmapped_text |
| OGN-252 | Super Mega Death Rocket!, Jinx | unsupported | unmapped_text |
| OGN-253 | Hand of Noxus | unsupported | unsupported_type; unmapped_text |
| OGN-254 | Noxian Guillotine, Darius | unsupported | unmapped_text |
| OGN-255 | Nine-Tailed Fox | unsupported | unsupported_type; unmapped_text |
| OGN-256 | Fox-Fire, Ahri | unsupported | unmapped_text |
| OGN-257 | Blind Monk | unsupported | unsupported_type; unmapped_text |
| OGN-258 | Dragon's Rage, Lee Sin | unsupported | unmapped_text |
| OGN-259 | Unforgiven | unsupported | unsupported_type; unmapped_text |
| OGN-260 | Last Breath, Yasuo | unsupported | unmapped_text |
| OGN-261 | Radiant Dawn | unsupported | unsupported_type; unmapped_text |
| OGN-262 | Zenith Blade, Leona | unsupported | unmapped_text |
| OGN-263 | Swift Scout | unsupported | unsupported_type; unmapped_text |
| OGN-264 | Guerilla Warfare, Teemo | unsupported | unmapped_text |
| OGN-265 | Herald of the Arcane | unsupported | unsupported_type; unmapped_text |
| OGN-266 | Siphon Power, Viktor | unsupported | unmapped_text |
| OGN-267 | Bounty Hunter | unsupported | unsupported_type; unmapped_text |
| OGN-268 | Bullet Time, Miss Fortune | unsupported | unmapped_text |
| OGN-269 | The Boss | unsupported | unsupported_type; unmapped_text |
| OGN-270 | Showstopper, Sett | unsupported | unmapped_text |
| OGN-271 | Recruit (DE) | unsupported | token_lifecycle |
| OGN-272 | Recruit (NX) | unsupported | token_lifecycle |
| OGN-273 | Recruit (ZN) | unsupported | token_lifecycle |
| OGN-274 | Sprite | unsupported | unmapped_text; token_lifecycle |
| OGN-275 | Altar to Unity | unsupported | unsupported_type; unmapped_text |
| OGN-276 | Aspirant's Climb | unsupported | unsupported_type; unmapped_text |
| OGN-277 | Back-Alley Bar | unsupported | unsupported_type; unmapped_text |
| OGN-278 | Bandle Tree | unsupported | unsupported_type; unmapped_text |
| OGN-279 | Fortified Position | unsupported | unsupported_type; unmapped_text |
| OGN-280 | Grove of the God-Willow | unsupported | unsupported_type; unmapped_text |
| OGN-281 | Hallowed Tomb | unsupported | unsupported_type; unmapped_text |
| OGN-282 | Monastery of Hirana | unsupported | unsupported_type; unmapped_text |
| OGN-283 | Navori Fighting Pit | unsupported | unsupported_type; unmapped_text |
| OGN-284 | Obelisk of Power | unsupported | unsupported_type; unmapped_text |
| OGN-285 | Reaver's Row | unsupported | unsupported_type; unmapped_text |
| OGN-286 | Reckoner's Arena | unsupported | unsupported_type; unmapped_text |
| OGN-287 | Sigil of the Storm | unsupported | unsupported_type; unmapped_text |
| OGN-288 | Startipped Peak | unsupported | unsupported_type; unmapped_text |
| OGN-289 | Targon's Peak | unsupported | unsupported_type; unmapped_text |
| OGN-290 | The Arena's Greatest | unsupported | unsupported_type; unmapped_text |
| OGN-291 | The Candlelit Sanctum | unsupported | unsupported_type; unmapped_text |
| OGN-292 | The Dreaming Tree | unsupported | unsupported_type; unmapped_text |
| OGN-293 | The Grand Plaza | unsupported | unsupported_type; unmapped_text |
| OGN-294 | Trifarian War Camp | unsupported | unsupported_type; unmapped_text |
| OGN-295 | Vilemaw's Lair | unsupported | unsupported_type; unmapped_text |
| OGN-296 | Void Gate | unsupported | unsupported_type; unmapped_text |
| OGN-297 | Windswept Hillock | unsupported | unsupported_type; unmapped_text |
| OGN-298 | Zaun Warrens | unsupported | unsupported_type; unmapped_text |
| OGN-299 | Daughter of the Void | unsupported | unsupported_type; unmapped_text |
| OGN-299-STAR | Daughter of the Void | unsupported | unsupported_type; unmapped_text |
| OGN-300 | Relentless Storm | unsupported | unsupported_type; unmapped_text |
| OGN-300-STAR | Relentless Storm | unsupported | unsupported_type; unmapped_text |
| OGN-301 | Loose Cannon | unsupported | unsupported_type; unmapped_text |
| OGN-301-STAR | Loose Cannon | unsupported | unsupported_type; unmapped_text |
| OGN-302 | Hand of Noxus | unsupported | unsupported_type; unmapped_text |
| OGN-302-STAR | Hand of Noxus | unsupported | unsupported_type; unmapped_text |
| OGN-303 | Nine-Tailed Fox | unsupported | unsupported_type; unmapped_text |
| OGN-303-STAR | Nine-Tailed Fox | unsupported | unsupported_type; unmapped_text |
| OGN-304 | Blind Monk | unsupported | unsupported_type; unmapped_text |
| OGN-304-STAR | Blind Monk | unsupported | unsupported_type; unmapped_text |
| OGN-305 | Unforgiven | unsupported | unsupported_type; unmapped_text |
| OGN-305-STAR | Unforgiven | unsupported | unsupported_type; unmapped_text |
| OGN-306 | Radiant Dawn | unsupported | unsupported_type; unmapped_text |
| OGN-306-STAR | Radiant Dawn | unsupported | unsupported_type; unmapped_text |
| OGN-307 | Swift Scout | unsupported | unsupported_type; unmapped_text |
| OGN-307-STAR | Swift Scout | unsupported | unsupported_type; unmapped_text |
| OGN-308 | Herald of the Arcane | unsupported | unsupported_type; unmapped_text |
| OGN-308-STAR | Herald of the Arcane | unsupported | unsupported_type; unmapped_text |
| OGN-309 | Bounty Hunter | unsupported | unsupported_type; unmapped_text |
| OGN-309-STAR | Bounty Hunter | unsupported | unsupported_type; unmapped_text |
| OGN-310 | The Boss | unsupported | unsupported_type; unmapped_text |
| OGN-310-STAR | The Boss | unsupported | unsupported_type; unmapped_text |
| OGS-001 | Annie, Fiery | unsupported | unmapped_text |
| OGS-002 | Firestorm | unsupported | unmapped_text |
| OGS-003 | Incinerate | isolated_scenarios_passed |  |
| OGS-004 | Master Yi, Meditative | unsupported | unmapped_text |
| OGS-005 | Zephyr Sage | unsupported | unmapped_text |
| OGS-006 | Lux, Illuminated | unsupported | unmapped_text |
| OGS-007 | Garen, Rugged | unsupported | unmapped_text |
| OGS-008 | Gentlemen's Duel | unsupported | unmapped_text |
| OGS-009 | Master Yi, Honed | unsupported | unmapped_text |
| OGS-010 | Annie, Stubborn | unsupported | unmapped_text |
| OGS-011 | Flash | unsupported | unmapped_text |
| OGS-012 | Blast of Power | isolated_scenarios_passed |  |
| OGS-013 | Garen, Commander | unsupported | unmapped_text |
| OGS-014 | Lux, Crownguard | unsupported | unmapped_text |
| OGS-015 | Recruit the Vanguard | unsupported | unmapped_text |
| OGS-016 | Vanguard Attendant | unsupported | unmapped_text |
| OGS-017 | Dark Child, Starter | unsupported | unsupported_type; unmapped_text |
| OGS-018 | Tibbers, Annie | unsupported | unmapped_text |
| OGS-019 | Wuju Bladesman, Starter | unsupported | unsupported_type; unmapped_text |
| OGS-020 | Highlander, Yi | unsupported | unmapped_text |
| OGS-021 | Lady of Luminosity, Starter | unsupported | unsupported_type; unmapped_text |
| OGS-022 | Final Spark, Lux | isolated_scenarios_passed |  |
| OGS-023 | Might of Demacia, Starter | unsupported | unsupported_type; unmapped_text |
| OGS-024 | Decisive Strike, Garen | unsupported | unmapped_text |
| RAD-001 | Amateur Demolitionist | unsupported | unmapped_text |
| RAD-002 | Banner of Conquest | unsupported | unmapped_text |
| RAD-003 | Bilgewater Tracker | unsupported | unmapped_text |
| RAD-004 | Brawl | unsupported | unmapped_text |
| RAD-005 | Lingering Animus | unsupported | unmapped_text |
| RAD-006 | Scorched Earth | unsupported | unmapped_text |
| RAD-007 | Rally for War | unsupported | unmapped_text |
| RAD-008 | War Scout | unsupported | unmapped_text |
| RAD-009 | Antagonistic Apparatus | unsupported | unmapped_text |
| RAD-010 | Forbidden Technique | unsupported | unmapped_text |
| RAD-011 | Incorrigible Construct | unsupported | unmapped_text |
| RAD-012 | Runeblade Anvil | unsupported | unmapped_text |
| RAD-013 | Lost to the Sands | unsupported | unmapped_text |
| RAD-014 | Shimmering Swimmer | unsupported | unmapped_text |
| RAD-015 | Akali, Brash | unsupported | unmapped_text |
| RAD-016 | Coalesced Energy | unsupported | unmapped_text |
| RAD-017 | Detonation Amplifier | unsupported | unmapped_text |
| RAD-018 | Drakehound Packmaster | unsupported | unmapped_text |
| RAD-019 | Firebrand Raider | unsupported | unmapped_text |
| RAD-020 | Mordekaiser, Twice Slain | unsupported | unmapped_text |
| RAD-020A | Mordekaiser, Twice Slain | unsupported | unmapped_text |
| RAD-021 | Ekko, Revolutionary | unsupported | unmapped_text |
| RAD-021A | Ekko, Revolutionary | unsupported | unmapped_text |
| RAD-022 | Whirling Twirligig | unsupported | unmapped_text |
| RAD-023 | Ziggs, Short-Fused | unsupported | unmapped_text |
| RAD-023A | Ziggs, Short-Fused | unsupported | unmapped_text |
| RAD-024 | Blossoming Dreamroot | unsupported | unmapped_text |
| RAD-025 | Consult the Heavens | unsupported | unmapped_text |
| RAD-026 | Entrenched Boar | unsupported | unmapped_text |
| RAD-027 | Iridescent Avian | unsupported | unmapped_text |
| RAD-028 | Ki Burst | unsupported | unmapped_text |
| RAD-029 | Life from Stone | unsupported | unmapped_text |
| RAD-030 | Sanctum Conservator | unsupported | unmapped_text |
| RAD-031 | Stoic Ferryman | unsupported | unmapped_text |
| RAD-032 | Battle Preparations | unsupported | unmapped_text |
| RAD-033 | Command: Attack | unsupported | unmapped_text |
| RAD-034 | Hunker Down | unsupported | unmapped_text |
| RAD-035 | Invigorating Bloom | unsupported | unmapped_text |
| RAD-036 | Storm Raptor | unsupported | unmapped_text |
| RAD-037 | Watchful Curator | unsupported | unmapped_text |
| RAD-038 | Ahri, Confident | unsupported | unmapped_text |
| RAD-039 | Ephemeral Ward | unsupported | unmapped_text |
| RAD-040 | Heartening Soul | unsupported | unmapped_text |
| RAD-041 | Hush | unsupported | unmapped_text |
| RAD-042 | Orianna, Exquisite | unsupported | unmapped_text |
| RAD-042A | Orianna, Exquisite | unsupported | unmapped_text |
| RAD-043 | Riven, Broken Blade | unsupported | unmapped_text |
| RAD-043A | Riven, Broken Blade | unsupported | unmapped_text |
| RAD-044 | Hunting Blind | unsupported | unmapped_text |
| RAD-045 | K'Sante, Dauntless | unsupported | unmapped_text |
| RAD-045A | K'Sante, Dauntless | unsupported | unmapped_text |
| RAD-046 | Resplendent Rostrum | unsupported | unmapped_text |
| RAD-047 | Fanfare | unsupported | unmapped_text |
| RAD-048 | High Note | unsupported | unmapped_text |
| RAD-049 | Industrious Mechsmith | unsupported | unmapped_text |
| RAD-050 | Mysterious Chronomancer | unsupported | unmapped_text |
| RAD-051 | Parallel Convergence | unsupported | unmapped_text |
| RAD-052 | Resource Extractor | unsupported | unmapped_text |
| RAD-053 | Strigian Oracle | unsupported | unmapped_text |
| RAD-054 | Trinket Peddler | unsupported | unmapped_text |
| RAD-055 | Clanging Sentry | unsupported | unmapped_text |
| RAD-056 | Improvised Projectile | unsupported | unmapped_text |
| RAD-057 | Piltovan Guidebot | unsupported | unmapped_text |
| RAD-058 | Riptide Mage | unsupported | unmapped_text |
| RAD-059 | Supernova | isolated_scenarios_passed |  |
| RAD-060 | The Empyrean | unsupported | unmapped_text |
| RAD-061 | Ekko, Ingenious | unsupported | unmapped_text |
| RAD-061A | Ekko, Ingenious | unsupported | unmapped_text |
| RAD-062 | Gravity Field | unsupported | unmapped_text |
| RAD-063 | Kai'Sa, Rebel | unsupported | unmapped_text |
| RAD-064 | Scrutinizing Scope | unsupported | unmapped_text |
| RAD-065 | Seraphine, Inspiring | unsupported | unmapped_text |
| RAD-065A | Seraphine, Inspiring | unsupported | unmapped_text |
| RAD-066 | Spirit of the Forge | unsupported | unmapped_text |
| RAD-067 | Clocktower Guardian | unsupported | unmapped_text |
| RAD-068 | Orianna, Mechanical Marvel | unsupported | unmapped_text |
| RAD-068A | Orianna, Mechanical Marvel | unsupported | unmapped_text |
| RAD-069 | Zero Point Inflection | unsupported | unmapped_text |
| RAD-070 | Hold 'Em | unsupported | unmapped_text |
| RAD-071 | Nazuman Ntofo | unsupported | unmapped_text |
| RAD-072 | Overloaded Traveler | unsupported | unmapped_text |
| RAD-073 | Pillaged Armory | unsupported | unmapped_text |
| RAD-074 | Raving Witness | unsupported | unmapped_text |
| RAD-075 | Skystrike Squadron | unsupported | unmapped_text |
| RAD-076 | Sneaky Zeebles | unsupported | unmapped_text |
| RAD-077 | Wrath of the Freljord | unsupported | unmapped_text |
| RAD-078 | Armored Tusker | unsupported | unmapped_text |
| RAD-079 | Avalanche | unsupported | unmapped_text |
| RAD-080 | Bloodscent Swarm | unsupported | unmapped_text |
| RAD-081 | Elnuk Herd | unsupported | unmapped_text |
| RAD-082 | Primordial Roar | unsupported | unmapped_text |
| RAD-083 | Stalwart Goatherd | unsupported | unmapped_text |
| RAD-084 | Cataclysm | unsupported | unmapped_text |
| RAD-085 | Graves, Blasting Through | unsupported | unmapped_text |
| RAD-086 | K'Sante, Courageous | unsupported | unmapped_text |
| RAD-086A | K'Sante, Courageous | unsupported | unmapped_text |
| RAD-087 | Portable Portal | unsupported | unmapped_text |
| RAD-088 | Staunch Survivor | unsupported | unmapped_text |
| RAD-089 | Titanic Shrine | unsupported | unmapped_text |
| RAD-090 | Evelynn, Consuming | unsupported | unmapped_text |
| RAD-090A | Evelynn, Consuming | unsupported | unmapped_text |
| RAD-091 | Jarvan IV, Martial Paragon | unsupported | unmapped_text |
| RAD-091A | Jarvan IV, Martial Paragon | unsupported | unmapped_text |
| RAD-092 | Seraphic Wyvern | unsupported | unmapped_text |
| RAD-093 | Disposal Expert | unsupported | unmapped_text |
| RAD-094 | Explosimian | unsupported | unmapped_text |
| RAD-095 | Momentary Companion | unsupported | unmapped_text |
| RAD-096 | Satchel Charge | unsupported | unmapped_text |
| RAD-097 | Siren of the Shallows | unsupported | unmapped_text |
| RAD-098 | Siren's Song | unsupported | unmapped_text |
| RAD-099 | Suave Negotiator | unsupported | unmapped_text |
| RAD-100 | The Waters' Wage | unsupported | unmapped_text |
| RAD-101 | An Offer You Can't Refuse | unsupported | unmapped_text |
| RAD-102 | Demon Shade | unsupported | unmapped_text |
| RAD-103 | Gutter Guardian | unsupported | unmapped_text |
| RAD-104 | Pitiless Stalker | unsupported | unmapped_text |
| RAD-105 | Reckless Innovator | unsupported | unmapped_text |
| RAD-106 | The Good Stuff | unsupported | unmapped_text |
| RAD-107 | Bedeviling Stranger | unsupported | unmapped_text |
| RAD-108 | Bushwhack Trap | unsupported | unmapped_text |
| RAD-109 | Evelynn, In Control | unsupported | unmapped_text |
| RAD-109A | Evelynn, In Control | unsupported | unmapped_text |
| RAD-110 | Lulu, Whimsical | unsupported | unmapped_text |
| RAD-111 | Mechanical Bandit | unsupported | unmapped_text |
| RAD-112 | Ziggs, Explosive | unsupported | unmapped_text |
| RAD-112A | Ziggs, Explosive | unsupported | unmapped_text |
| RAD-113 | Angler Wyrm | unsupported | unmapped_text |
| RAD-114 | Riven, Deserter | unsupported | unmapped_text |
| RAD-114A | Riven, Deserter | unsupported | unmapped_text |
| RAD-115 | Transpositionist | unsupported | unmapped_text |
| RAD-116 | Concert Poster | unsupported | unmapped_text |
| RAD-117 | For Demacia! | unsupported | unmapped_text |
| RAD-118 | Herald of the Emperor | unsupported | unmapped_text |
| RAD-119 | Hunting Dog | unsupported | unmapped_text |
| RAD-120 | Meticulous Restorationist | unsupported | unmapped_text |
| RAD-121 | One-Two Punch | unsupported | unmapped_text |
| RAD-122 | Party Crasher | unsupported | unmapped_text |
| RAD-123 | Protector's Shield | unsupported | unmapped_text |
| RAD-124 | Burn Away | unsupported | unmapped_text |
| RAD-125 | Dune Devourer | unsupported | unmapped_text |
| RAD-126 | Mournful Spirit | unsupported | unmapped_text |
| RAD-127 | Rousing Display | unsupported | unmapped_text |
| RAD-128 | Steadfast Outrider | unsupported | unmapped_text |
| RAD-129 | Trifarian Captain | unsupported | unmapped_text |
| RAD-130 | Battlefield Armorer | unsupported | unmapped_text |
| RAD-131 | Demacian Illuminators | unsupported | unmapped_text |
| RAD-132 | Heimerdinger, Academy Instructor | unsupported | unmapped_text |
| RAD-133 | Jarvan IV, Royal Heir | unsupported | unmapped_text |
| RAD-133A | Jarvan IV, Royal Heir | unsupported | unmapped_text |
| RAD-134 | Raucous Anthem | unsupported | unmapped_text |
| RAD-135 | Remember the Fallen | unsupported | unmapped_text |
| RAD-136 | Dockside Lock-Up | unsupported | unmapped_text |
| RAD-137 | Mordekaiser, Dominating | unsupported | unmapped_text |
| RAD-137A | Mordekaiser, Dominating | unsupported | unmapped_text |
| RAD-138 | Seraphine, Not Alone | unsupported | unmapped_text |
| RAD-138A | Seraphine, Not Alone | unsupported | unmapped_text |
| RAD-139 | Boy Who Shattered Time | unsupported | unsupported_type; unmapped_text |
| RAD-140 | Chronobreak | unsupported | unmapped_text |
| RAD-141 | Hexplosives Expert | unsupported | unsupported_type; unmapped_text |
| RAD-142 | Hexplosive Minefield | unsupported | unmapped_text |
| RAD-143 | Iron Revenant | unsupported | unsupported_type; unmapped_text |
| RAD-144 | Realm of Death | unsupported | unmapped_text |
| RAD-145 | Lady of Clockwork | unsupported | unsupported_type; unmapped_text |
| RAD-146 | The Ball | unsupported | unmapped_text |
| RAD-147 | Pride of Nazumah | unsupported | unsupported_type; unmapped_text |
| RAD-148 | Ntofo Strikes | unsupported | unmapped_text |
| RAD-149 | The Exile | unsupported | unsupported_type; unmapped_text |
| RAD-150 | Blade of the Exile | unsupported | unmapped_text |
| RAD-151 | Starry-Eyed Songstress | unsupported | unsupported_type; unmapped_text |
| RAD-152 | Encore | unsupported | unmapped_text |
| RAD-153 | Agony's Embrace | unsupported | unsupported_type; unmapped_text |
| RAD-154 | Last Caress | unsupported | unmapped_text |
| RAD-155 | Exemplar of Demacia | unsupported | unsupported_type; unmapped_text |
| RAD-156 | Demacian Standard | unsupported | unmapped_text |
| RAD-157 | Bandle Scouts' Academy | unsupported | unsupported_type; unmapped_text |
| RAD-158 | Black Market | unsupported | unsupported_type; unmapped_text |
| RAD-159 | Black Rose Sanctum | unsupported | unsupported_type; unmapped_text |
| RAD-160 | Cosmic Vista | unsupported | unsupported_type; unmapped_text |
| RAD-161 | Durand Memorial | unsupported | unsupported_type; unmapped_text |
| RAD-162 | Firelights' Hideout | unsupported | unsupported_type; unmapped_text |
| RAD-163 | Hunters' Circle | unsupported | unsupported_type; unmapped_text |
| RAD-164 | Packed Amphitheater | unsupported | unsupported_type; unmapped_text |
| RAD-165 | Rakelstake | unsupported | unsupported_type; unmapped_text |
| RAD-166 | Ruined Monastery | unsupported | unsupported_type; unmapped_text |
| RAD-167 | Neeko, Blending In | unsupported | unmapped_text |
| RAD-168 | Boy Who Shattered Time | unsupported | unsupported_type; unmapped_text |
| RAD-169 | Hexplosives Expert | unsupported | unsupported_type; unmapped_text |
| RAD-170 | Iron Revenant | unsupported | unsupported_type; unmapped_text |
| RAD-171 | Lady of Clockwork | unsupported | unsupported_type; unmapped_text |
| RAD-172 | Pride of Nazumah | unsupported | unsupported_type; unmapped_text |
| RAD-173 | The Exile | unsupported | unsupported_type; unmapped_text |
| RAD-174 | Starry-Eyed Songstress | unsupported | unsupported_type; unmapped_text |
| RAD-175 | Agony's Embrace | unsupported | unsupported_type; unmapped_text |
| RAD-176 | Exemplar of Demacia | unsupported | unsupported_type; unmapped_text |
| RAD-177 | Ekko, Revolutionary | unsupported | unmapped_text |
| RAD-178 | K'Sante, Courageous | unsupported | unmapped_text |
| RAD-179 | Aphelios, Exalted | unsupported | unmapped_text |
| RAD-180 | Ezreal, Dashing | unsupported | unmapped_text |
| RAD-181 | Yone, Blademaster | unsupported | unmapped_text |
| RAD-182 | Kayn, Unleashed | unsupported | unmapped_text |
| RAD-183 | Sett, Kingpin | unsupported | unmapped_text |
| RAD-184 | Packed Amphitheater | unsupported | unsupported_type; unmapped_text |
| RAD-R01 | Fury Rune | unsupported | unsupported_type |
| RAD-R01A | Fury Rune | unsupported | unsupported_type |
| RAD-R02 | Calm Rune | unsupported | unsupported_type |
| RAD-R02A | Calm Rune | unsupported | unsupported_type |
| RAD-R03 | Mind Rune | unsupported | unsupported_type |
| RAD-R03A | Mind Rune | unsupported | unsupported_type |
| RAD-R04 | Body Rune | unsupported | unsupported_type |
| RAD-R04A | Body Rune | unsupported | unsupported_type |
| RAD-R05 | Chaos Rune | unsupported | unsupported_type |
| RAD-R05A | Chaos Rune | unsupported | unsupported_type |
| RAD-R06 | Order Rune | unsupported | unsupported_type |
| RAD-R06A | Order Rune | unsupported | unsupported_type |
| RAD-SP1 | Ahri, Confident | unsupported | unmapped_text |
| RAD-SP2 | Akali, Brash | unsupported | unmapped_text |
| RAD-SP3 | Evelynn, In Control | unsupported | unmapped_text |
| RAD-SP4 | Kai'Sa, Rebel | unsupported | unmapped_text |
| RAD-SP5 | Seraphine, Not Alone | unsupported | unmapped_text |
| SFD-001 | Against the Odds | unsupported | unmapped_text |
| SFD-002 | Armed Assailant | unsupported | unmapped_text |
| SFD-003 | Blood Rush | unsupported | unmapped_text |
| SFD-004 | Bushwhack | unsupported | unmapped_text |
| SFD-005 | Detonate | unsupported | unmapped_text |
| SFD-006 | Eager Drakehound | unsupported | unmapped_text |
| SFD-007 | Gem Jammer | unsupported | unmapped_text |
| SFD-008 | Sentinel Adept | unsupported | unmapped_text |
| SFD-009 | Serrated Dirk | unsupported | unmapped_text |
| SFD-010 | Void Drone | unsupported | unmapped_text |
| SFD-011 | Angle Shot | unsupported | unmapped_text |
| SFD-012 | Battering Ram | unsupported | unmapped_text |
| SFD-013 | Blast Corps Cadet | unsupported | unmapped_text |
| SFD-014 | Minotaur Reckoner | unsupported | unmapped_text |
| SFD-015 | Perched Grimwyrm | unsupported | unmapped_text |
| SFD-016 | Recurve Bow | unsupported | unmapped_text |
| SFD-017 | Sudden Storm | unsupported | unmapped_text |
| SFD-018 | Void Hatchling | unsupported | unmapped_text |
| SFD-019 | Assembly Rig | unsupported | unmapped_text |
| SFD-020 | Draven, Vanquisher | unsupported | unmapped_text |
| SFD-020A | Draven, Vanquisher | unsupported | unmapped_text |
| SFD-021 | Ferrous Forerunner | unsupported | unmapped_text |
| SFD-022 | Long Sword | unsupported | unmapped_text |
| SFD-023 | Piercing Light | unsupported | unmapped_text |
| SFD-024 | Rell, Magnetic | unsupported | unmapped_text |
| SFD-025 | Rengar, Pouncing | unsupported | unmapped_text |
| SFD-026 | Rumble, Hotheaded | unsupported | unmapped_text |
| SFD-026A | Rumble, Hotheaded | unsupported | unmapped_text |
| SFD-027 | Dunebreaker | unsupported | unmapped_text |
| SFD-028 | Lucian, Gunslinger | unsupported | unmapped_text |
| SFD-028A | Lucian, Gunslinger | unsupported | unmapped_text |
| SFD-029 | Rek'Sai, Breacher | unsupported | unmapped_text |
| SFD-029A | Rek'Sai, Breacher | unsupported | unmapped_text |
| SFD-030 | Skyfall of Areion | unsupported | unmapped_text |
| SFD-031 | Desert's Call | unsupported | unmapped_text |
| SFD-032 | Disarming Rake | unsupported | unmapped_text |
| SFD-033 | Doran's Shield | unsupported | unmapped_text |
| SFD-034 | Feral Strength | unsupported | unmapped_text |
| SFD-035 | Guardian of the Passage | unsupported | unmapped_text |
| SFD-036 | Lonely Poro | unsupported | unmapped_text |
| SFD-037 | Navori Scout | unsupported | unmapped_text |
| SFD-038 | Ribbon Dancer | unsupported | unmapped_text |
| SFD-039 | Royal Entourage | unsupported | unmapped_text |
| SFD-040 | Thwonk! | unsupported | unmapped_text |
| SFD-041 | Apprentice Smith | unsupported | unmapped_text |
| SFD-042 | Brutalizer | unsupported | unmapped_text |
| SFD-043 | Emperor's Divide | unsupported | unmapped_text |
| SFD-044 | Legion Quartermaster | unsupported | unmapped_text |
| SFD-045 | Not So Fast | unsupported | unmapped_text |
| SFD-046 | Poro Snax | unsupported | unmapped_text |
| SFD-047 | Simian Ancestor | unsupported | unmapped_text |
| SFD-048 | Stellacorn Herder | unsupported | unmapped_text |
| SFD-049 | Aphelios, Exalted | unsupported | unmapped_text |
| SFD-050 | Azir, Ascendant | unsupported | unmapped_text |
| SFD-050A | Azir, Ascendant | unsupported | unmapped_text |
| SFD-051 | Guardian Angel | unsupported | unmapped_text |
| SFD-052 | Heart of Dark Ice | unsupported | unmapped_text |
| SFD-053 | Janna, Savior | unsupported | unmapped_text |
| SFD-054A | Jax, Unmatched | unsupported | unmapped_text |
| SFD-055 | Needlessly Large Yordle | unsupported | unmapped_text |
| SFD-056 | Sterak's Gage | unsupported | unmapped_text |
| SFD-057 | Irelia, Fervent | unsupported | unmapped_text |
| SFD-057A | Irelia, Fervent | unsupported | unmapped_text |
| SFD-058 | Ornn, Blacksmith | unsupported | unmapped_text |
| SFD-058A | Ornn, Blacksmith | unsupported | unmapped_text |
| SFD-059 | Svellsongur | unsupported | unmapped_text |
| SFD-060 | Tianna Crownguard | unsupported | unmapped_text |
| SFD-061 | Aspiring Engineer | unsupported | unmapped_text |
| SFD-062 | Bubble Bot | unsupported | unmapped_text |
| SFD-063 | Chemtech Cask | unsupported | unmapped_text |
| SFD-064 | Cloth Armor | unsupported | unmapped_text |
| SFD-065 | Forecaster | unsupported | unmapped_text |
| SFD-066 | Frigid Touch | unsupported | unmapped_text |
| SFD-067 | Frostcoat Cub | unsupported | unmapped_text |
| SFD-068 | Gearhead | unsupported | unmapped_text |
| SFD-069 | Plundering Poro | unsupported | unmapped_text |
| SFD-070 | Wages of Pain | unsupported | unmapped_text |
| SFD-071 | Breakneck Mech | unsupported | unmapped_text |
| SFD-072 | Dropboarder | unsupported | unmapped_text |
| SFD-073 | Experimental Hexplate | unsupported | unmapped_text |
| SFD-074 | Pickpocket | unsupported | unmapped_text |
| SFD-075 | Prize of Progress | unsupported | unmapped_text |
| SFD-076 | Production Surge | unsupported | unmapped_text |
| SFD-077 | Rocket Barrage | unsupported | unmapped_text |
| SFD-078 | Temporal Portal | unsupported | unmapped_text |
| SFD-079 | Bard, Mercurial | unsupported | unmapped_text |
| SFD-080 | Bellows Breath | unsupported | unmapped_text |
| SFD-081 | Card Sharp | unsupported | unmapped_text |
| SFD-082 | Ezreal, Dashing | unsupported | unmapped_text |
| SFD-082A | Ezreal, Dashing | unsupported | unmapped_text |
| SFD-083 | Hextech Anomaly | unsupported | unmapped_text |
| SFD-084 | Jayce, Man of Progress | unsupported | unmapped_text |
| SFD-085 | Ornn, Forge God | unsupported | unmapped_text |
| SFD-085A | Ornn, Forge God | unsupported | unmapped_text |
| SFD-086 | World Atlas | unsupported | unmapped_text |
| SFD-087 | Premonition | isolated_scenarios_passed |  |
| SFD-088 | Renata Glasc, Mastermind | unsupported | unmapped_text |
| SFD-088A | Renata Glasc, Mastermind | unsupported | unmapped_text |
| SFD-089 | Rumble, Scrapper | unsupported | unmapped_text |
| SFD-089A | Rumble, Scrapper | unsupported | unmapped_text |
| SFD-090 | The Zero Drive | unsupported | unmapped_text |
| SFD-091 | Buhru Captain | unsupported | unmapped_text |
| SFD-092 | Combat Chef | unsupported | unmapped_text |
| SFD-093 | Dauntless Vanguard | unsupported | unmapped_text |
| SFD-094 | Direwing | unsupported | unmapped_text |
| SFD-095 | Doran's Blade | unsupported | unmapped_text |
| SFD-096 | Laurent Bladekeeper | unsupported | unmapped_text |
| SFD-097 | Punch First | isolated_scenarios_passed |  |
| SFD-098 | Sea Monkey | unsupported | unmapped_text |
| SFD-099 | Veteran Poro | unsupported | unmapped_text |
| SFD-100 | Yordle Explorer | unsupported | unmapped_text |
| SFD-101 | Fae Dragon | unsupported | unmapped_text |
| SFD-102 | Hexdrinker | unsupported | unmapped_text |
| SFD-103 | Jaull-Fish | unsupported | unmapped_text |
| SFD-104 | Petricite Monument | unsupported | unmapped_text |
| SFD-105 | Ruin Runner | unsupported | unmapped_text |
| SFD-106 | Show of Strength | unsupported | unmapped_text |
| SFD-107 | Strike Down | unsupported | unmapped_text |
| SFD-108 | Warmog's Armor | unsupported | unmapped_text |
| SFD-109 | Akshan, Mischievous | unsupported | unmapped_text |
| SFD-110 | Fiora, Peerless | unsupported | unmapped_text |
| SFD-110A | Fiora, Peerless | unsupported | unmapped_text |
| SFD-111 | Here to Help | unsupported | unmapped_text |
| SFD-112 | Kato the Arm | unsupported | unmapped_text |
| SFD-113 | Lucian, Merciless | unsupported | unmapped_text |
| SFD-113A | Lucian, Merciless | unsupported | unmapped_text |
| SFD-114 | Marching Orders | unsupported | unmapped_text |
| SFD-115 | Trinity Force | unsupported | unmapped_text |
| SFD-116 | Yone, Blademaster | unsupported | unmapped_text |
| SFD-117 | Ancient Henge | unsupported | unmapped_text |
| SFD-118 | Boneshiver | unsupported | unmapped_text |
| SFD-119 | Jax, Unrelenting | unsupported | unmapped_text |
| SFD-119A | Jax, Unrelenting | unsupported | unmapped_text |
| SFD-120 | Sivir, Ambitious | unsupported | unmapped_text |
| SFD-120A | Sivir, Ambitious | unsupported | unmapped_text |
| SFD-121 | Black Market Broker | unsupported | unmapped_text |
| SFD-122 | Called Shot | unsupported | unmapped_text |
| SFD-123 | Corrupt Enforcer | unsupported | unmapped_text |
| SFD-124 | Doran's Ring | unsupported | unmapped_text |
| SFD-125 | Fae Porter | unsupported | unmapped_text |
| SFD-126 | Loyal Pup | unsupported | unmapped_text |
| SFD-127 | Master Bingwen | unsupported | unmapped_text |
| SFD-128 | Overzealous Fan | unsupported | unmapped_text |
| SFD-129 | Temptation | unsupported | unmapped_text |
| SFD-130 | Treasure Hunter | unsupported | unmapped_text |
| SFD-131 | Ancient Warmonger | unsupported | unmapped_text |
| SFD-132 | Beast Below | unsupported | unmapped_text |
| SFD-133 | Boots of Swiftness | unsupported | unmapped_text |
| SFD-134 | Cull | unsupported | unmapped_text |
| SFD-135 | Factory Recall | unsupported | unmapped_text |
| SFD-136 | Hard Bargain | unsupported | unmapped_text |
| SFD-137 | Harpoon Squad | unsupported | unmapped_text |
| SFD-138 | Windsinger | unsupported | unmapped_text |
| SFD-139 | Edge of Night | unsupported | unmapped_text |
| SFD-140 | Fizz, Trickster | unsupported | unmapped_text |
| SFD-141 | Irelia, Graceful | unsupported | unmapped_text |
| SFD-141A | Irelia, Graceful | unsupported | unmapped_text |
| SFD-142 | Jae Medarda | unsupported | unmapped_text |
| SFD-143 | Sivir, Mercenary | unsupported | unmapped_text |
| SFD-143A | Sivir, Mercenary | unsupported | unmapped_text |
| SFD-144 | Spirit Wheel | unsupported | unmapped_text |
| SFD-145 | Switcheroo | unsupported | unmapped_text |
| SFD-146 | Vex, Cheerless | unsupported | unmapped_text |
| SFD-147 | Downwell | unsupported | unmapped_text |
| SFD-148 | Draven, Audacious | unsupported | unmapped_text |
| SFD-148A | Draven, Audacious | unsupported | unmapped_text |
| SFD-149 | Ezreal, Prodigy | unsupported | unmapped_text |
| SFD-149A | Ezreal, Prodigy | unsupported | unmapped_text |
| SFD-150 | Last Rites | unsupported | unmapped_text |
| SFD-151 | Bonds of Strength | unsupported | unmapped_text |
| SFD-152 | Eminent Benefactor | unsupported | unmapped_text |
| SFD-153 | Eye of the Herald | unsupported | unmapped_text |
| SFD-154 | Guards! | unsupported | unmapped_text |
| SFD-155 | Honest Broker | unsupported | unmapped_text |
| SFD-156 | Laurent Duelist | unsupported | unmapped_text |
| SFD-157 | Royal Guard | unsupported | unmapped_text |
| SFD-158 | Sandshifter | unsupported | unmapped_text |
| SFD-159 | Trusty Ramhound | unsupported | unmapped_text |
| SFD-160 | Zaun Punk | unsupported | unmapped_text |
| SFD-161 | B.F. Sword | unsupported | unmapped_text |
| SFD-162 | Blood Money | unsupported | unmapped_text |
| SFD-163 | Deathgrip | unsupported | unmapped_text |
| SFD-164 | Drag Under | unsupported | unmapped_text |
| SFD-165 | Glasc Mixologist | unsupported | unmapped_text |
| SFD-166 | Rally the Troops | unsupported | unmapped_text |
| SFD-167 | Unsung Hero | unsupported | unmapped_text |
| SFD-168 | Vanguard Armory | unsupported | unmapped_text |
| SFD-169 | Altar of Memories | unsupported | unmapped_text |
| SFD-170 | Rek'Sai, Swarm Queen | unsupported | unmapped_text |
| SFD-170A | Rek'Sai, Swarm Queen | unsupported | unmapped_text |
| SFD-171 | Renata Glasc, Industrialist | unsupported | unmapped_text |
| SFD-171A | Renata Glasc, Industrialist | unsupported | unmapped_text |
| SFD-172 | Sacred Shears | unsupported | unmapped_text |
| SFD-173 | Soraka, Wanderer | unsupported | unmapped_text |
| SFD-174 | Trove Golem | unsupported | unmapped_text |
| SFD-175 | Undertitan | unsupported | unmapped_text |
| SFD-176 | Xin Zhao, Vigilant | unsupported | unmapped_text |
| SFD-177 | Azir, Sovereign | unsupported | unmapped_text |
| SFD-177A | Azir, Sovereign | unsupported | unmapped_text |
| SFD-178 | Blade of the Ruined King | unsupported | unmapped_text |
| SFD-179 | Corinna Veraza | unsupported | unmapped_text |
| SFD-180 | Fiora, Worthy | unsupported | unmapped_text |
| SFD-180A | Fiora, Worthy | unsupported | unmapped_text |
| SFD-181 | Mechanized Menace | unsupported | unsupported_type; unmapped_text |
| SFD-182 | Danger Zone | unsupported | unmapped_text |
| SFD-183 | Purifier | unsupported | unsupported_type; unmapped_text |
| SFD-184 | Relentless Pursuit | unsupported | unmapped_text |
| SFD-185 | Glorious Executioner | unsupported | unsupported_type; unmapped_text |
| SFD-186 | Spinning Axe | unsupported | unmapped_text |
| SFD-187 | Void Burrower | unsupported | unsupported_type; unmapped_text |
| SFD-188 | Void Rush | unsupported | unmapped_text |
| SFD-189 | Fire Below the Mountain | unsupported | unsupported_type; unmapped_text |
| SFD-190 | Forgefire Cape | unsupported | unmapped_text |
| SFD-191 | Rabadon's Deathcrown | unsupported | unmapped_text |
| SFD-192 | Shurelya's Requiem | unsupported | unmapped_text |
| SFD-193 | Grandmaster at Arms | unsupported | unsupported_type; unmapped_text |
| SFD-194 | Counter Strike | unsupported | unmapped_text |
| SFD-195 | Blade Dancer | unsupported | unsupported_type; unmapped_text |
| SFD-196 | Defiant Dance | unsupported | unmapped_text |
| SFD-197 | Emperor of the Sands | unsupported | unsupported_type; unmapped_text |
| SFD-198 | Arise! | unsupported | unmapped_text |
| SFD-199 | Prodigal Explorer | unsupported | unsupported_type; unmapped_text |
| SFD-200 | Arcane Shift | unsupported | unmapped_text |
| SFD-201 | Chem-Baroness | unsupported | unsupported_type; unmapped_text |
| SFD-202 | Hostile Takeover | unsupported | unmapped_text |
| SFD-203 | Battle Mistress | unsupported | unsupported_type; unmapped_text |
| SFD-204 | On the Hunt | unsupported | unmapped_text |
| SFD-205 | Grand Duelist | unsupported | unsupported_type; unmapped_text |
| SFD-206 | Riposte | unsupported | unmapped_text |
| SFD-207 | Emperor's Dais | unsupported | unsupported_type; unmapped_text |
| SFD-208 | Forge of the Fluft | unsupported | unsupported_type; unmapped_text |
| SFD-209 | Forgotten Monument | unsupported | unsupported_type; unmapped_text |
| SFD-210 | Hall of Legends | unsupported | unsupported_type; unmapped_text |
| SFD-211 | Marai Spire | unsupported | unsupported_type; unmapped_text |
| SFD-212 | Minefield | unsupported | unsupported_type; unmapped_text |
| SFD-213 | Ornn's Forge | unsupported | unsupported_type; unmapped_text |
| SFD-214 | Power Nexus | unsupported | unsupported_type; unmapped_text |
| SFD-215 | Ravenbloom Conservatory | unsupported | unsupported_type; unmapped_text |
| SFD-216 | Rockfall Path | unsupported | unsupported_type; unmapped_text |
| SFD-217 | Seat of Power | unsupported | unsupported_type; unmapped_text |
| SFD-218 | Sunken Temple | unsupported | unsupported_type; unmapped_text |
| SFD-219 | The Papertree | unsupported | unsupported_type; unmapped_text |
| SFD-220 | Treasure Hoard | unsupported | unsupported_type; unmapped_text |
| SFD-221 | Veiled Temple | unsupported | unsupported_type; unmapped_text |
| SFD-222 | Seal of Rage | unsupported | unmapped_text |
| SFD-223 | Vayne, Hunter | unsupported | unmapped_text |
| SFD-223-STAR | Vayne, Hunter | unsupported | unmapped_text |
| SFD-224 | Aphelios, Exalted | unsupported | unmapped_text |
| SFD-224-STAR | Aphelios, Exalted | unsupported | unmapped_text |
| SFD-225 | Irelia, Fervent | unsupported | unmapped_text |
| SFD-225-STAR | Irelia, Fervent | unsupported | unmapped_text |
| SFD-226 | Seal of Focus | unsupported | unmapped_text |
| SFD-227 | Ahri, Inquisitive | unsupported | unmapped_text |
| SFD-227-STAR | Ahri, Inquisitive | unsupported | unmapped_text |
| SFD-228 | Bard, Mercurial | unsupported | unmapped_text |
| SFD-228-STAR | Bard, Mercurial | unsupported | unmapped_text |
| SFD-229 | Seal of Insight | unsupported | unmapped_text |
| SFD-230 | Teemo, Strategist | unsupported | unmapped_text |
| SFD-230-STAR | Teemo, Strategist | unsupported | unmapped_text |
| SFD-231 | Seal of Strength | unsupported | unmapped_text |
| SFD-232 | Sett, Brawler | unsupported | unmapped_text |
| SFD-232-STAR | Sett, Brawler | unsupported | unmapped_text |
| SFD-233 | Yone, Blademaster | unsupported | unmapped_text |
| SFD-233-STAR | Yone, Blademaster | unsupported | unmapped_text |
| SFD-234 | Seal of Discord | unsupported | unmapped_text |
| SFD-235 | Yasuo, Windrider | unsupported | unmapped_text |
| SFD-235-STAR | Yasuo, Windrider | unsupported | unmapped_text |
| SFD-236 | Darius, Executioner | unsupported | unmapped_text |
| SFD-236-STAR | Darius, Executioner | unsupported | unmapped_text |
| SFD-237 | Karma, Channeler | unsupported | unmapped_text |
| SFD-237-STAR | Karma, Channeler | unsupported | unmapped_text |
| SFD-238 | Seal of Unity | unsupported | unmapped_text |
| SFD-239 | Soraka, Wanderer | unsupported | unmapped_text |
| SFD-239-STAR | Soraka, Wanderer | unsupported | unmapped_text |
| SFD-240 | Mechanized Menace | unsupported | unsupported_type; unmapped_text |
| SFD-241 | Purifier | unsupported | unsupported_type; unmapped_text |
| SFD-242 | Glorious Executioner | unsupported | unsupported_type; unmapped_text |
| SFD-243 | Void Burrower | unsupported | unsupported_type; unmapped_text |
| SFD-244 | Fire Below the Mountain | unsupported | unsupported_type; unmapped_text |
| SFD-245 | Grandmaster at Arms | unsupported | unsupported_type; unmapped_text |
| SFD-246 | Blade Dancer | unsupported | unsupported_type; unmapped_text |
| SFD-247 | Emperor of the Sands | unsupported | unsupported_type; unmapped_text |
| SFD-248 | Prodigal Explorer | unsupported | unsupported_type; unmapped_text |
| SFD-249 | Chem-Baroness | unsupported | unsupported_type; unmapped_text |
| SFD-250 | Battle Mistress | unsupported | unsupported_type; unmapped_text |
| SFD-251 | Grand Duelist | unsupported | unsupported_type; unmapped_text |
| SFD-T03 | Gold | unsupported | unmapped_text; token_lifecycle |
| UNL-001 | Arena Kingpin | unsupported | unmapped_text |
| UNL-002 | Inferna | unsupported | unmapped_text |
| UNL-003 | Mischievous Marai | unsupported | unmapped_text |
| UNL-004 | Prepared Neophyte | unsupported | unmapped_text |
| UNL-005 | Revna the Lorekeeper | unsupported | unmapped_text |
| UNL-006 | Sharkling | unsupported | unmapped_text |
| UNL-007 | Smite | unsupported | unmapped_text |
| UNL-008 | Towering Pairofant | unsupported | unmapped_text |
| UNL-009 | Upstage Comedy | unsupported | unmapped_text |
| UNL-010 | Vault Breaker | unsupported | unmapped_text |
| UNL-011 | Fresh Beans | unsupported | unmapped_text |
| UNL-012 | Lord Broadmane | unsupported | unmapped_text |
| UNL-013 | Lotus Trap | unsupported | unmapped_text |
| UNL-014 | Monster Harpoon | unsupported | unmapped_text |
| UNL-015 | Right of Conquest | unsupported | unmapped_text |
| UNL-016 | Scorchclaw | unsupported | unmapped_text |
| UNL-017 | Square Up | unsupported | unmapped_text |
| UNL-018 | Yeti Brawler | unsupported | unmapped_text |
| UNL-019 | Blighted Battleaxe | unsupported | unmapped_text |
| UNL-020 | Dancing Grenade | unsupported | unmapped_text |
| UNL-021 | Grim Apothecary | unsupported | unmapped_text |
| UNL-022 | Jhin, Murderous Artist | unsupported | unmapped_text |
| UNL-022A | Jhin, Murderous Artist | unsupported | unmapped_text |
| UNL-023 | Katarina, Reckless | unsupported | unmapped_text |
| UNL-024 | Rengar, Unseen | unsupported | unmapped_text |
| UNL-024A | Rengar, Unseen | unsupported | unmapped_text |
| UNL-025 | Undying Legion | unsupported | unmapped_text |
| UNL-026 | Xerath, Freed | unsupported | unmapped_text |
| UNL-027 | Inviolus Vox | unsupported | unmapped_text |
| UNL-028 | Pyke, Dockside Butcher | unsupported | unmapped_text |
| UNL-028A | Pyke, Dockside Butcher | unsupported | unmapped_text |
| UNL-029 | Red Brambleback | unsupported | unmapped_text |
| UNL-029A | Red Brambleback | unsupported | unmapped_text |
| UNL-030 | Vi, Hotheaded | unsupported | unmapped_text |
| UNL-030A | Vi, Hotheaded | unsupported | unmapped_text |
| UNL-031 | Combat Experience | unsupported | unmapped_text |
| UNL-032 | Double Trouble | unsupported | unmapped_text |
| UNL-033 | Frisky Hunter | unsupported | unmapped_text |
| UNL-034 | Herald of Spring | unsupported | unmapped_text |
| UNL-035 | Monch | unsupported | unmapped_text |
| UNL-036 | Mutated Mouser | unsupported | unmapped_text |
| UNL-037 | Shadow Watcher | unsupported | unmapped_text |
| UNL-038 | Skyward Strike | unsupported | unmapped_text |
| UNL-039 | Soul Sword | unsupported | unmapped_text |
| UNL-040 | Wuju Apprentice | unsupported | unmapped_text |
| UNL-041 | Allay, Eager Admirer | unsupported | unmapped_text |
| UNL-042 | Back Off | unsupported | unmapped_text |
| UNL-043 | Enthusiastic Promoter | unsupported | unmapped_text |
| UNL-044 | Flurry of Feathers | unsupported | unmapped_text |
| UNL-045 | Forgotten Signpost | unsupported | unmapped_text |
| UNL-046 | Friendship | unsupported | unmapped_text |
| UNL-047 | Mosstomper | unsupported | unmapped_text |
| UNL-048 | Trevor Snoozebottom | unsupported | unmapped_text |
| UNL-049 | Honeyfruit | unsupported | unmapped_text |
| UNL-050 | Iascylla | unsupported | unmapped_text |
| UNL-051 | Ivern, Nurturer | unsupported | unmapped_text |
| UNL-051A | Ivern, Nurturer | unsupported | unmapped_text |
| UNL-052 | Nami, Headstrong | unsupported | unmapped_text |
| UNL-053 | Scuttle Crab | unsupported | unmapped_text |
| UNL-054 | Tricksy Tentacles | unsupported | unmapped_text |
| UNL-055 | Vex, Mocking | unsupported | unmapped_text |
| UNL-055A | Vex, Mocking | unsupported | unmapped_text |
| UNL-056 | Yuumi, Magical Cat | unsupported | unmapped_text |
| UNL-057 | Alpha Wildclaw | unsupported | unmapped_text |
| UNL-058 | Lillia, Protector of Dreams | unsupported | unmapped_text |
| UNL-058A | Lillia, Protector of Dreams | unsupported | unmapped_text |
| UNL-059 | Master Yi, Unstoppable | unsupported | unmapped_text |
| UNL-059A | Master Yi, Unstoppable | unsupported | unmapped_text |
| UNL-060 | Vilemaw | unsupported | unmapped_text |
| UNL-060A | Vilemaw | unsupported | unmapped_text |
| UNL-061 | Downstage Dramatics | unsupported | unmapped_text |
| UNL-062 | Dramatic Visionary | unsupported | unmapped_text |
| UNL-063 | Eclipse | unsupported | unmapped_text |
| UNL-064 | Fate Weaver | unsupported | unmapped_text |
| UNL-065 | Icevale Archer | unsupported | unmapped_text |
| UNL-066 | Moonlight Affliction | unsupported | unmapped_text |
| UNL-067 | Ruined Rex | unsupported | unmapped_text |
| UNL-068 | Spectral Centaur | unsupported | unmapped_text |
| UNL-069 | Sprite Burst | unsupported | unmapped_text |
| UNL-070 | Turn to Dust | unsupported | unmapped_text |
| UNL-071 | Chakram Dancer | unsupported | unmapped_text |
| UNL-072 | Crescent Strike | unsupported | unmapped_text |
| UNL-073 | Deadly Flourish | unsupported | unmapped_text |
| UNL-074 | Frigid Jewel | unsupported | unmapped_text |
| UNL-075 | Gustwalker | unsupported | unmapped_text |
| UNL-076 | Petal Pixie | unsupported | unmapped_text |
| UNL-077 | Soul Shepherd | unsupported | unmapped_text |
| UNL-078 | Sprite Fountain | unsupported | unmapped_text |
| UNL-079 | Diana, Lunari | unsupported | unmapped_text |
| UNL-079A | Diana, Lunari | unsupported | unmapped_text |
| UNL-080 | Hwei, Brooding Painter | unsupported | unmapped_text |
| UNL-081 | Keeper of Masks | unsupported | unmapped_text |
| UNL-082 | Lillia, Fae Fawn | unsupported | unmapped_text |
| UNL-082A | Lillia, Fae Fawn | unsupported | unmapped_text |
| UNL-083 | Smoke and Mirrors | unsupported | unmapped_text |
| UNL-084 | Sprite Queen | unsupported | unmapped_text |
| UNL-085 | Sumpworks Map | unsupported | unmapped_text |
| UNL-086 | Zilean, Time Mage | unsupported | unmapped_text |
| UNL-087 | Blue Sentinel | unsupported | unmapped_text |
| UNL-087A | Blue Sentinel | unsupported | unmapped_text |
| UNL-088 | Gutter Palace | unsupported | unmapped_text |
| UNL-089 | Jhin, Meticulous Killer | unsupported | unmapped_text |
| UNL-089A | Jhin, Meticulous Killer | unsupported | unmapped_text |
| UNL-090 | LeBlanc, Everywhere at Once | unsupported | unmapped_text |
| UNL-090A | LeBlanc, Everywhere at Once | unsupported | unmapped_text |
| UNL-091 | Concentrate | unsupported | unmapped_text |
| UNL-092 | Demacian Diplomat | isolated_scenarios_passed |  |
| UNL-093 | Dragonsoul Sage | unsupported | unmapped_text |
| UNL-094 | Gemhand Hunter | unsupported | unmapped_text |
| UNL-095 | Grim Resolve | unsupported | unmapped_text |
| UNL-096 | Hunter's Machete | unsupported | unmapped_text |
| UNL-097 | Kinkou Initiate | isolated_scenarios_passed |  |
| UNL-098 | Targonian Visionary | unsupported | unmapped_text |
| UNL-099 | Towering Combatant | unsupported | unmapped_text |
| UNL-100 | Voracious Gromp | unsupported | unmapped_text |
| UNL-101 | Call to Battle | unsupported | unmapped_text |
| UNL-102 | Crowd Favorite | unsupported | unmapped_text |
| UNL-103 | Disposal Order | unsupported | unmapped_text |
| UNL-104 | Gentle Gemdragon | unsupported | unmapped_text |
| UNL-105 | Imposing Challenger | unsupported | unmapped_text |
| UNL-106 | Repulse | unsupported | unmapped_text |
| UNL-107 | Stare Down | unsupported | unmapped_text |
| UNL-108 | Wily Newtfish | unsupported | unmapped_text |
| UNL-109 | Blood Rose | unsupported | unmapped_text |
| UNL-110 | Clash of Giants | unsupported | unmapped_text |
| UNL-111 | Determined Sentry | unsupported | unmapped_text |
| UNL-112 | Irresistible Faefolk | unsupported | unmapped_text |
| UNL-113 | Master Yi, Tempered | unsupported | unmapped_text |
| UNL-113A | Master Yi, Tempered | unsupported | unmapped_text |
| UNL-114 | Nidalee, Cat Form | unsupported | unmapped_text |
| UNL-115 | Nilah, Joyful Ascetic | unsupported | unmapped_text |
| UNL-116 | Poppy, Paragon | unsupported | unmapped_text |
| UNL-116A | Poppy, Paragon | unsupported | unmapped_text |
| UNL-117 | Arachnoid Horror | unsupported | unmapped_text |
| UNL-118 | Elder Dragon | unsupported | unmapped_text |
| UNL-118A | Elder Dragon | unsupported | unmapped_text |
| UNL-119 | Kha'Zix, Evolving Hunter | unsupported | unmapped_text |
| UNL-119A | Kha'Zix, Evolving Hunter | unsupported | unmapped_text |
| UNL-120 | Rengar, Trophy Hunter | unsupported | unmapped_text |
| UNL-120A | Rengar, Trophy Hunter | unsupported | unmapped_text |
| UNL-121 | Bewitching Spirit | unsupported | unmapped_text |
| UNL-122 | Crescent Guardian | unsupported | unmapped_text |
| UNL-123 | Evershade Stalker | unsupported | unmapped_text |
| UNL-124 | Isolate | unsupported | unmapped_text |
| UNL-125 | Lunar Boon | unsupported | unmapped_text |
| UNL-126 | Megatusk | unsupported | unmapped_text |
| UNL-127 | Mister Root | unsupported | unmapped_text |
| UNL-128 | Star-Crossed | unsupported | unmapped_text |
| UNL-129 | Vicious Snapjaws | unsupported | unmapped_text |
| UNL-130 | Walking Roost | unsupported | unmapped_text |
| UNL-131 | Abandon | unsupported | unmapped_text |
| UNL-132 | Angler Beast | unsupported | unmapped_text |
| UNL-133 | Blast Cone | unsupported | unmapped_text |
| UNL-134 | Existential Dread | unsupported | unmapped_text |
| UNL-135 | Insightful Investigator | unsupported | unmapped_text |
| UNL-136 | Scryer's Bloom | unsupported | unmapped_text |
| UNL-137 | Sinister Poro | unsupported | unmapped_text |
| UNL-138 | The List | unsupported | unmapped_text |
| UNL-139 | Bone Skewer | unsupported | unmapped_text |
| UNL-140 | Conscription | unsupported | unmapped_text |
| UNL-141 | Evelynn, Entrancing | unsupported | unmapped_text |
| UNL-142 | Heedless Resurrection | unsupported | unmapped_text |
| UNL-143 | Kha'Zix, Mutating Horror | unsupported | unmapped_text |
| UNL-143A | Kha'Zix, Mutating Horror | unsupported | unmapped_text |
| UNL-144 | Maduli the Gatekeeper | unsupported | unmapped_text |
| UNL-145 | Pyke, Returned | unsupported | unmapped_text |
| UNL-145A | Pyke, Returned | unsupported | unmapped_text |
| UNL-146 | Syndra, Transcendent | unsupported | unmapped_text |
| UNL-147 | Baron Nashor | unsupported | unmapped_text |
| UNL-147A | Baron Nashor | unsupported | unmapped_text |
| UNL-148 | Cursed Sarcophagus | unsupported | unmapped_text |
| UNL-149 | Diana, No Longer Human | unsupported | unmapped_text |
| UNL-149A | Diana, No Longer Human | unsupported | unmapped_text |
| UNL-150 | Vex, Apathetic | unsupported | unmapped_text |
| UNL-150A | Vex, Apathetic | unsupported | unmapped_text |
| UNL-151 | Bandle Soldier | unsupported | unmapped_text |
| UNL-152 | Black Rose Dignitary | unsupported | unmapped_text |
| UNL-153 | Carrion Dredger | unsupported | unmapped_text |
| UNL-154 | Crimson Pigeons | unsupported | unmapped_text |
| UNL-155 | Heroic Charge | unsupported | unmapped_text |
| UNL-156 | Loyal Poro | unsupported | unmapped_text |
| UNL-157 | Scrutinizing Sergeant | unsupported | unmapped_text |
| UNL-158 | Shepherd's Heirloom | unsupported | unmapped_text |
| UNL-159 | Soul Harvest | unsupported | unmapped_text |
| UNL-160 | Ultrasoft Poro | unsupported | unmapped_text |
| UNL-161 | Divining Shells | unsupported | unmapped_text |
| UNL-162 | Enthralling Protector | unsupported | unmapped_text |
| UNL-163 | Mageseeker Investigator | unsupported | unmapped_text |
| UNL-164 | Safety Inspector | unsupported | unmapped_text |
| UNL-165 | Shadow's Call | unsupported | unmapped_text |
| UNL-166 | Stalking Wolf | unsupported | unmapped_text |
| UNL-167 | Starhound | unsupported | unmapped_text |
| UNL-168 | Undying Loyalty | unsupported | unmapped_text |
| UNL-169 | Ashe, Focused | unsupported | unmapped_text |
| UNL-170 | Atakhan | unsupported | unmapped_text |
| UNL-171 | Galio, Indefatigable | unsupported | unmapped_text |
| UNL-172 | LeBlanc, Fragmented | unsupported | unmapped_text |
| UNL-172A | LeBlanc, Fragmented | unsupported | unmapped_text |
| UNL-173 | Sacrifice | unsupported | unmapped_text |
| UNL-174 | Shard of Undoing | unsupported | unmapped_text |
| UNL-175 | Tactical Retreat | unsupported | unmapped_text |
| UNL-176 | Vi, Peacekeeper | unsupported | unmapped_text |
| UNL-176A | Vi, Peacekeeper | unsupported | unmapped_text |
| UNL-177 | Ivern, Friend to All | unsupported | unmapped_text |
| UNL-177A | Ivern, Friend to All | unsupported | unmapped_text |
| UNL-178 | Poppy, Defender of the Meek | unsupported | unmapped_text |
| UNL-178A | Poppy, Defender of the Meek | unsupported | unmapped_text |
| UNL-179 | Rift Herald | unsupported | unmapped_text |
| UNL-179A | Rift Herald | unsupported | unmapped_text |
| UNL-180 | The Ruination | unsupported | unmapped_text |
| UNL-181 | Virtuoso | unsupported | unsupported_type; unmapped_text |
| UNL-182 | Curtain Call | unsupported | unmapped_text |
| UNL-183 | Pridestalker | unsupported | unsupported_type; unmapped_text |
| UNL-184 | Thrill of the Hunt | unsupported | unmapped_text |
| UNL-185 | Bloodharbor Ripper | unsupported | unsupported_type; unmapped_text |
| UNL-186 | Death from Below | unsupported | unmapped_text |
| UNL-187 | Piltover Enforcer | unsupported | unsupported_type; unmapped_text |
| UNL-188 | Hextech Gauntlets | unsupported | unmapped_text |
| UNL-189 | Bashful Bloom | unsupported | unsupported_type; unmapped_text |
| UNL-190 | Lilting Lullaby | unsupported | unmapped_text |
| UNL-191 | Wuju Master | unsupported | unsupported_type; unmapped_text |
| UNL-192 | Alpha Strike | unsupported | unmapped_text |
| UNL-193 | Gloomist | unsupported | unsupported_type; unmapped_text |
| UNL-194 | Shadow | unsupported | unmapped_text |
| UNL-195 | Green Father | unsupported | unsupported_type; unmapped_text |
| UNL-196 | Daisy! | unsupported | unmapped_text |
| UNL-197 | Scorn of the Moon | unsupported | unsupported_type; unmapped_text |
| UNL-198 | Moonfall | unsupported | unmapped_text |
| UNL-199 | Deceiver | unsupported | unsupported_type; unmapped_text |
| UNL-200 | Mirror Image | unsupported | unmapped_text |
| UNL-201 | Voidreaver | unsupported | unsupported_type; unmapped_text |
| UNL-202 | Void Assault | unsupported | unmapped_text |
| UNL-203 | Keeper of the Hammer | unsupported | unsupported_type; unmapped_text |
| UNL-204 | Keeper's Verdict | unsupported | unmapped_text |
| UNL-205 | Abandoned Hall | unsupported | unsupported_type; unmapped_text |
| UNL-206 | Altar of Blood | unsupported | unsupported_type; unmapped_text |
| UNL-207 | Amateur Recital | unsupported | unsupported_type; unmapped_text |
| UNL-208 | Black Flame Altar | unsupported | unsupported_type; unmapped_text |
| UNL-209 | Dusk Rose Lab | unsupported | unsupported_type; unmapped_text |
| UNL-210 | Forbidding Waste | unsupported | unsupported_type; unmapped_text |
| UNL-211 | Forgotten Library | unsupported | unsupported_type; unmapped_text |
| UNL-212 | Frozen Fortress | unsupported | unsupported_type; unmapped_text |
| UNL-213 | Gardens of Becoming | unsupported | unsupported_type; unmapped_text |
| UNL-214 | Ripper's Bay | unsupported | unsupported_type; unmapped_text |
| UNL-215 | Star Spring | unsupported | unsupported_type; unmapped_text |
| UNL-216 | The Academy | unsupported | unsupported_type; unmapped_text |
| UNL-217 | Trapping Grounds | unsupported | unsupported_type; unmapped_text |
| UNL-218 | Valley of Idols | unsupported | unsupported_type; unmapped_text |
| UNL-219 | Vaults of Helia | unsupported | unsupported_type; unmapped_text |
| UNL-220 | Pouty Poro | unsupported | unmapped_text |
| UNL-221 | Lonely Poro | unsupported | unmapped_text |
| UNL-222 | Plundering Poro | unsupported | unmapped_text |
| UNL-223 | Veteran Poro | unsupported | unmapped_text |
| UNL-224 | Mystic Poro | unsupported | unmapped_text |
| UNL-225 | Daring Poro | unsupported | unmapped_text |
| UNL-226 | Virtuoso | unsupported | unsupported_type; unmapped_text |
| UNL-226-STAR | Virtuoso | unsupported | unsupported_type; unmapped_text |
| UNL-227 | Pridestalker | unsupported | unsupported_type; unmapped_text |
| UNL-227-STAR | Pridestalker | unsupported | unsupported_type; unmapped_text |
| UNL-228 | Bloodharbor Ripper | unsupported | unsupported_type; unmapped_text |
| UNL-228-STAR | Bloodharbor Ripper | unsupported | unsupported_type; unmapped_text |
| UNL-229 | Piltover Enforcer | unsupported | unsupported_type; unmapped_text |
| UNL-229-STAR | Piltover Enforcer | unsupported | unsupported_type; unmapped_text |
| UNL-230 | Bashful Bloom | unsupported | unsupported_type; unmapped_text |
| UNL-230-STAR | Bashful Bloom | unsupported | unsupported_type; unmapped_text |
| UNL-231 | Wuju Master | unsupported | unsupported_type; unmapped_text |
| UNL-231-STAR | Wuju Master | unsupported | unsupported_type; unmapped_text |
| UNL-232 | Gloomist | unsupported | unsupported_type; unmapped_text |
| UNL-232-STAR | Gloomist | unsupported | unsupported_type; unmapped_text |
| UNL-233 | Green Father | unsupported | unsupported_type; unmapped_text |
| UNL-233-STAR | Green Father | unsupported | unsupported_type; unmapped_text |
| UNL-234 | Scorn of the Moon | unsupported | unsupported_type; unmapped_text |
| UNL-234-STAR | Scorn of the Moon | unsupported | unsupported_type; unmapped_text |
| UNL-235 | Deceiver | unsupported | unsupported_type; unmapped_text |
| UNL-235-STAR | Deceiver | unsupported | unsupported_type; unmapped_text |
| UNL-236 | Voidreaver | unsupported | unsupported_type; unmapped_text |
| UNL-236-STAR | Voidreaver | unsupported | unsupported_type; unmapped_text |
| UNL-237 | Keeper of the Hammer | unsupported | unsupported_type; unmapped_text |
| UNL-237-STAR | Keeper of the Hammer | unsupported | unsupported_type; unmapped_text |
| UNL-238 | Baron Nashor | unsupported | unmapped_text |
| UNL-T01 | Baron Pit | unsupported | unsupported_type; unmapped_text; token_lifecycle |
| UNL-T02 | Bird | unsupported | unmapped_text; token_lifecycle |
| UNL-T03 | Brush | unsupported | unsupported_type; unmapped_text; token_lifecycle |
| UNL-T04 | Buff | unsupported | unsupported_type; unmapped_text; token_lifecycle |
| UNL-T05 | Gold | unsupported | unmapped_text; token_lifecycle |
| UNL-T06 | Reflection | unsupported | unmapped_text; token_lifecycle |
| UNL-T07 | Sprite | unsupported | unmapped_text; token_lifecycle |
| UNL-T08 | XP Tracker | unsupported | unsupported_type; unmapped_text; token_lifecycle |
| VEN-001 | Baccai Sandspinner | unsupported | unmapped_text |
| VEN-002 | Blade Twirler | unsupported | unmapped_text |
| VEN-003 | Brittle Steel | unsupported | unmapped_text |
| VEN-004 | Dune Surfer | unsupported | unmapped_text |
| VEN-005 | Forsaken Baccai | unsupported | unmapped_text |
| VEN-006 | Oasis Raider | unsupported | unmapped_text |
| VEN-007 | Punching Poro | unsupported | unmapped_text |
| VEN-008 | Ruthless Strike | unsupported | unmapped_text |
| VEN-009 | Baccai Reaper | unsupported | unmapped_text |
| VEN-010 | Consuming Curse | unsupported | unmapped_text |
| VEN-011 | Pendulum Blade | unsupported | unmapped_text |
| VEN-012 | Perfect Execution | unsupported | unmapped_text |
| VEN-013 | Shadow Assassin | unsupported | unmapped_text |
| VEN-014 | Shadow Fiend | unsupported | unmapped_text |
| VEN-015 | Decree of Rage | unsupported | unmapped_text |
| VEN-016 | Eclipse Dragon | unsupported | unmapped_text |
| VEN-017 | Morgana, Vindictive | unsupported | unmapped_text |
| VEN-018 | Rage Amplifier | unsupported | unmapped_text |
| VEN-019 | Renekton, Rage Fueled | unsupported | unmapped_text |
| VEN-019A | Renekton, Rage Fueled | unsupported | unmapped_text |
| VEN-020 | Twilight Reveler | unsupported | unmapped_text |
| VEN-021 | Akali, Deadly Weapon | unsupported | unmapped_text |
| VEN-021A | Akali, Deadly Weapon | unsupported | unmapped_text |
| VEN-022 | Endless Riches | unsupported | unmapped_text |
| VEN-023 | Zed, From the Shadows | unsupported | unmapped_text |
| VEN-023A | Zed, From the Shadows | unsupported | unmapped_text |
| VEN-024 | Affectionate Poro | unsupported | unmapped_text |
| VEN-025 | Esteemed Hierophant | unsupported | unmapped_text |
| VEN-026 | Field Musicians | isolated_scenarios_passed |  |
| VEN-027 | Hand Hammer | unsupported | unmapped_text |
| VEN-028 | Mournful Witness | unsupported | unmapped_text |
| VEN-029 | Ol' Poro | unsupported | unmapped_text |
| VEN-030 | Serene Ascetic | unsupported | unmapped_text |
| VEN-031 | Twilight Shroud | unsupported | unmapped_text |
| VEN-032 | Frostcoat Mother | unsupported | unmapped_text |
| VEN-033 | Pakaa Protector | unsupported | unmapped_text |
| VEN-034 | Resonating Strike | unsupported | unmapped_text |
| VEN-035 | Sanction | unsupported | unmapped_text |
| VEN-036 | Sandstone Chimera | unsupported | unmapped_text |
| VEN-037 | Tomb-Raider Barbara | unsupported | unmapped_text |
| VEN-038 | Akali, Silent | unsupported | unmapped_text |
| VEN-038A | Akali, Silent | unsupported | unmapped_text |
| VEN-039 | Crumbling Sands | unsupported | unmapped_text |
| VEN-040 | Decree of Focus | unsupported | unmapped_text |
| VEN-041 | Riven, Shattered | unsupported | unmapped_text |
| VEN-042 | Shen, Scourge of Shadows | unsupported | unmapped_text |
| VEN-042A | Shen, Scourge of Shadows | unsupported | unmapped_text |
| VEN-043 | Steel Paws | unsupported | unmapped_text |
| VEN-044 | Astral Heron | unsupported | unmapped_text |
| VEN-045 | Helm of Suppression | unsupported | unmapped_text |
| VEN-046 | Nasus, Ascended | unsupported | unmapped_text |
| VEN-046A | Nasus, Ascended | unsupported | unmapped_text |
| VEN-047 | Apprentice Mage | unsupported | unmapped_text |
| VEN-048 | Cloud Drake | isolated_scenarios_passed |  |
| VEN-049 | Dredge Up | unsupported | unmapped_text |
| VEN-050 | Grumpy Rockbear | unsupported | unmapped_text |
| VEN-051 | Iterative Design | unsupported | unmapped_text |
| VEN-052 | Mesmerize | unsupported | unmapped_text |
| VEN-053 | Otterpus | unsupported | unmapped_text |
| VEN-054 | Questionable Tome | unsupported | unmapped_text |
| VEN-055 | Applied Researchers | unsupported | unmapped_text |
| VEN-056 | Clairvoyance | unsupported | unmapped_text |
| VEN-057 | Covert Informant | unsupported | unmapped_text |
| VEN-058 | Patched Porobot | unsupported | unmapped_text |
| VEN-059 | Shock Blast | unsupported | unmapped_text |
| VEN-060 | Sky Crusier | unsupported | unmapped_text |
| VEN-061 | Decree of Insight | unsupported | unmapped_text |
| VEN-062 | Hextech Formula | unsupported | unmapped_text |
| VEN-063 | Nasus, Guardian of Knowledge | unsupported | unmapped_text |
| VEN-063A | Nasus, Guardian of Knowledge | unsupported | unmapped_text |
| VEN-064 | Plaza Guardian | unsupported | unmapped_text |
| VEN-065 | Swain, Visionary | unsupported | unmapped_text |
| VEN-066 | Temporal Breach | unsupported | unmapped_text |
| VEN-067 | Bottled Constellation | unsupported | unmapped_text |
| VEN-068 | Jayce, Brilliant Inventor | unsupported | unmapped_text |
| VEN-068A | Jayce, Brilliant Inventor | unsupported | unmapped_text |
| VEN-069 | Mel, Newly Awakened | unsupported | unmapped_text |
| VEN-069A | Mel, Newly Awakened | unsupported | unmapped_text |
| VEN-070 | Brutal Hunter | unsupported | unmapped_text |
| VEN-071 | Fretful Feline | unsupported | unmapped_text |
| VEN-072 | Guttural Roar | unsupported | unmapped_text |
| VEN-073 | Jagged Cutlass | unsupported | unmapped_text |
| VEN-074 | Legion Marauder | unsupported | unmapped_text |
| VEN-075 | Platewyrm Egg | unsupported | unmapped_text |
| VEN-076 | Repair Specialist | unsupported | unmapped_text |
| VEN-077 | Tools of Empire | unsupported | unmapped_text |
| VEN-078 | Baccai Witherclaw | unsupported | unmapped_text |
| VEN-079 | Dame the Despoiler | unsupported | unmapped_text |
| VEN-080 | Noxian Demolitionist | unsupported | unmapped_text |
| VEN-081 | Onslaught | unsupported | unmapped_text |
| VEN-082 | Profiteer | unsupported | unmapped_text |
| VEN-083 | Rampage | unsupported | unmapped_text |
| VEN-084 | Ambessa, The Wolf | unsupported | unmapped_text |
| VEN-084A | Ambessa, The Wolf | unsupported | unmapped_text |
| VEN-085 | Decree of Strength | unsupported | unmapped_text |
| VEN-086 | Gangplank, Naval | unsupported | unmapped_text |
| VEN-087 | Hextech Disc | unsupported | unmapped_text |
| VEN-088 | Jayce, Hammer in Hand | unsupported | unmapped_text |
| VEN-088A | Jayce, Hammer in Hand | unsupported | unmapped_text |
| VEN-089 | Wild Claw | unsupported | unmapped_text |
| VEN-090 | Cataclysmic Duel | unsupported | unmapped_text |
| VEN-091 | Corrupted Dragon | unsupported | unmapped_text |
| VEN-092 | Renekton, Brute | unsupported | unmapped_text |
| VEN-092A | Renekton, Brute | unsupported | unmapped_text |
| VEN-093 | Kinkou Lifeblade | unsupported | unmapped_text |
| VEN-094 | Mask Mother | unsupported | unmapped_text |
| VEN-095 | Shadow Order Disciple | unsupported | unmapped_text |
| VEN-096 | Shadowblade Lurker | unsupported | unmapped_text |
| VEN-097 | Spiderling | unsupported | unmapped_text |
| VEN-098 | Stargazer | unsupported | unmapped_text |
| VEN-099 | Tornado Warrior | unsupported | unmapped_text |
| VEN-100 | Up from the Deep | unsupported | unmapped_text |
| VEN-101 | Gust Monk | unsupported | unmapped_text |
| VEN-102 | Ravenbloom Prefect | unsupported | unmapped_text |
| VEN-103 | Shadows of the Past | unsupported | unmapped_text |
| VEN-104 | Tail-Cloaked Matriarch | unsupported | unmapped_text |
| VEN-105 | Twilight Step | unsupported | unmapped_text |
| VEN-106 | Wind and Ghosts | unsupported | unmapped_text |
| VEN-107 | Decree of Discord | unsupported | unmapped_text |
| VEN-108 | Forgotten Relic | unsupported | unmapped_text |
| VEN-109 | Illaoi, Prophet of the Great Kraken | unsupported | unmapped_text |
| VEN-110 | Mel, Defiant Soul | unsupported | unmapped_text |
| VEN-110A | Mel, Defiant Soul | unsupported | unmapped_text |
| VEN-111 | Minah Swiftfoot | unsupported | unmapped_text |
| VEN-112 | Zed, Without a Sound | unsupported | unmapped_text |
| VEN-112A | Zed, Without a Sound | unsupported | unmapped_text |
| VEN-113 | Kennen, Storm of Shuriken | unsupported | unmapped_text |
| VEN-113A | Kennen, Storm of Shuriken | unsupported | unmapped_text |
| VEN-114 | Kharox | unsupported | unmapped_text |
| VEN-115 | Ocean Drake | unsupported | unmapped_text |
| VEN-116 | Dragon Form | unsupported | unmapped_text |
| VEN-117 | Disciple of Shen | unsupported | unmapped_text |
| VEN-118 | Horns of the Dragon | unsupported | unmapped_text |
| VEN-119 | Keeper of Law | unsupported | unmapped_text |
| VEN-120 | Masa, Crashing Thunder | unsupported | unmapped_text |
| VEN-121 | Reluctant Leader | unsupported | unmapped_text |
| VEN-122 | Solari Sunhawk | unsupported | unmapped_text |
| VEN-123 | Soulspinner | unsupported | unmapped_text |
| VEN-124 | Escaped Grayback | unsupported | unmapped_text |
| VEN-125 | Hungry Wolf | unsupported | unmapped_text |
| VEN-126 | Ki Barrier | unsupported | unmapped_text |
| VEN-127 | Lacerate | unsupported | unmapped_text |
| VEN-128 | Noxian Emissary | unsupported | unmapped_text |
| VEN-129 | Sacred Protector | unsupported | unmapped_text |
| VEN-130 | Aurok General | unsupported | unmapped_text |
| VEN-131 | Decree of Unity | unsupported | unmapped_text |
| VEN-132 | Fallen Feline | unsupported | unmapped_text |
| VEN-133 | Glowstone | unsupported | unmapped_text |
| VEN-134 | Kayle, Justified | unsupported | unmapped_text |
| VEN-135 | Kennen, Keeper of Balance | unsupported | unmapped_text |
| VEN-135A | Kennen, Keeper of Balance | unsupported | unmapped_text |
| VEN-136 | Ambessa, Respected and Feared | unsupported | unmapped_text |
| VEN-136A | Ambessa, Respected and Feared | unsupported | unmapped_text |
| VEN-137 | Shady Spectacles | unsupported | unmapped_text |
| VEN-138 | Shen, Leader of the Kinkou Order | unsupported | unmapped_text |
| VEN-138A | Shen, Leader of the Kinkou Order | unsupported | unmapped_text |
| VEN-139 | Rogue Assassin | unsupported | unsupported_type; unmapped_text |
| VEN-140 | Shuriken Flip | unsupported | unmapped_text |
| VEN-141 | Butcher of the Sands | unsupported | unsupported_type; unmapped_text |
| VEN-142 | Dominus | unsupported | unmapped_text |
| VEN-143 | Master of Shadows | unsupported | unsupported_type; unmapped_text |
| VEN-144 | Death Mark | unsupported | unmapped_text |
| VEN-145 | Curator of the Sands | unsupported | unsupported_type; unmapped_text |
| VEN-146 | Siphoning Strike | unsupported | unmapped_text |
| VEN-147 | Eye of Twilight | unsupported | unsupported_type; unmapped_text |
| VEN-148 | Shadow Dash | unsupported | unmapped_text |
| VEN-149 | Defender of Tomorrow | unsupported | unsupported_type; unmapped_text |
| VEN-150 | Acceleration Gate | unsupported | unmapped_text |
| VEN-151 | Soul's Reflection | unsupported | unsupported_type; unmapped_text |
| VEN-152 | Rebuttal | unsupported | unmapped_text |
| VEN-153 | Matriarch of War | unsupported | unsupported_type; unmapped_text |
| VEN-154 | Public Execution | unsupported | unmapped_text |
| VEN-155 | Heart of the Tempest | unsupported | unsupported_type; unmapped_text |
| VEN-156 | Lightning Rush | unsupported | unmapped_text |
| VEN-157 | Dragon Roost | unsupported | unsupported_type; unmapped_text |
| VEN-158 | Heisho, Shell of the World | unsupported | unsupported_type; unmapped_text |
| VEN-159 | Kinkou Temple | unsupported | unsupported_type; unmapped_text |
| VEN-160 | Mystic Vortex | unsupported | unsupported_type; unmapped_text |
| VEN-161 | Piltovan Forge | unsupported | unsupported_type; unmapped_text |
| VEN-162 | Protective Sands | unsupported | unsupported_type; unmapped_text |
| VEN-163 | Risen Altar | unsupported | unsupported_type; unmapped_text |
| VEN-164 | Sandswept Tomb | unsupported | unsupported_type; unmapped_text |
| VEN-165 | Shadow Temple | unsupported | unsupported_type; unmapped_text |
| VEN-166 | Threshold of the Gray | unsupported | unsupported_type; unmapped_text |
| VEN-167 | Vi, Destructive | unsupported | unmapped_text |
| VEN-168 | Jinx, Demolitionist | unsupported | unmapped_text |
| VEN-169 | Zed, From the Shadows | unsupported | unmapped_text |
| VEN-170 | Shen, Scourge of Shadows | unsupported | unmapped_text |
| VEN-171 | Riven, Shattered | unsupported | unmapped_text |
| VEN-172 | Draven, Showboat | unsupported | unmapped_text |
| VEN-173 | Swain, Visionary | unsupported | unmapped_text |
| VEN-174 | Irelia, Fervent | unsupported | unmapped_text |
| VEN-175 | Jayce, Man of Progress | unsupported | unmapped_text |
| VEN-176 | Viktor, Innovator | unsupported | unmapped_text |
| VEN-177 | Renekton, Brute | unsupported | unmapped_text |
| VEN-178 | Nasus, Guardian of Knowledge | unsupported | unmapped_text |
| VEN-179 | Rengar, Trophy Hunter | unsupported | unmapped_text |
| VEN-180 | Kha'Zix, Evolving Hunter | unsupported | unmapped_text |
| VEN-181 | Gangplank, Naval | unsupported | unmapped_text |
| VEN-182 | Illaoi, Prophet of the Great Kraken | unsupported | unmapped_text |
| VEN-183 | Diana, No Longer Human | unsupported | unmapped_text |
| VEN-184 | Leona, Determined | unsupported | unmapped_text |
| VEN-185 | Kayle, Justified | unsupported | unmapped_text |
| VEN-186 | Morgana, Vindictive | unsupported | unmapped_text |
| VEN-187 | Ambessa, Respected and Feared | unsupported | unmapped_text |
| VEN-188 | Mel, Defiant Soul | unsupported | unmapped_text |
| VEN-189 | Rogue Assassin | unsupported | unsupported_type; unmapped_text |
| VEN-189-STAR | Rogue Assassin | unsupported | unsupported_type; unmapped_text |
| VEN-190 | Butcher of the Sands | unsupported | unsupported_type; unmapped_text |
| VEN-190-STAR | Butcher of the Sands | unsupported | unsupported_type; unmapped_text |
| VEN-191 | Master of Shadows | unsupported | unsupported_type; unmapped_text |
| VEN-191-STAR | Master of Shadows | unsupported | unsupported_type; unmapped_text |
| VEN-192 | Curator of the Sands | unsupported | unsupported_type; unmapped_text |
| VEN-192-STAR | Curator of the Sands | unsupported | unsupported_type; unmapped_text |
| VEN-193 | Eye of Twilight | unsupported | unsupported_type; unmapped_text |
| VEN-193-STAR | Eye of Twilight | unsupported | unsupported_type; unmapped_text |
| VEN-194 | Defender of Tomorrow | unsupported | unsupported_type; unmapped_text |
| VEN-194-STAR | Defender of Tomorrow | unsupported | unsupported_type; unmapped_text |
| VEN-195 | Soul's Reflection | unsupported | unsupported_type; unmapped_text |
| VEN-195-STAR | Soul's Reflection | unsupported | unsupported_type; unmapped_text |
| VEN-196 | Matriarch of War | unsupported | unsupported_type; unmapped_text |
| VEN-196-STAR | Matriarch of War | unsupported | unsupported_type; unmapped_text |
| VEN-197 | Heart of the Tempest | unsupported | unsupported_type; unmapped_text |
| VEN-197-STAR | Heart of the Tempest | unsupported | unsupported_type; unmapped_text |
| VEN-R01 | Fury Rune | unsupported | unsupported_type |
| VEN-R02 | Calm Rune | unsupported | unsupported_type |
| VEN-R03 | Mind Rune | unsupported | unsupported_type |
| VEN-R04 | Body Rune | unsupported | unsupported_type |
| VEN-R05 | Chaos Rune | unsupported | unsupported_type |
| VEN-R06 | Order Rune | unsupported | unsupported_type |
| VEN-SP1 | Kai'Sa, Survivor | unsupported | unmapped_text |
| VEN-SP2 | Sona, Harmonious | unsupported | unmapped_text |
| VEN-SP3 | Ahri, Inquisitive | unsupported | unmapped_text |
| VEN-SP4 | Sett, Brawler | unsupported | unmapped_text |
| VEN-SP5 | Ezreal, Prodigy | unsupported | unmapped_text |
| VEN-SP6 | Lux, Crownguard | unsupported | unmapped_text |
| VEN-T04 | Recruit | unsupported | token_lifecycle |
