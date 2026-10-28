"""Prepare the documented API before R3; no runtime or test changes."""
from pathlib import Path
import hashlib,re
root=Path(__file__).resolve().parents[1];d=root/'docs';p=d/'basic-operators-api.md'
s=p.read_text(encoding='utf-8');archive=d/'basic-operators-api-v2.1.md'
if archive.exists():raise ValueError('Archive exists; inspect before rerun')
archive.write_bytes(p.read_bytes())
s=s.replace('# 基本算子 API 参考 V2.1','# 基本算子 API 参考 V3',1)
s=s.replace('版本：2026-10-28。共73个正式函数；[V2接口](basic-operators-api-v2.md)仅供迁移对照。','版本：2026-10-28。共71个正式函数；[V2.1接口](basic-operators-api-v2.1.md)仅供迁移对照。函数数量不等于不同游戏动作的数量。',1)
a=s.index('### `exhaust` 横置');b=s.index('### `buff` 给予增益',a)
s=s[:a]+'''### `orient` 改变活跃／横置朝向

```python
orient(objects: Selection[Orientable], state: str, *, simultaneous: bool = True,
       actor: Player = CONTROLLER) -> Result[list[Orientable]]
```

- state闭集为ready、exhausted。接受Unit/Gear/Rune/Legend；仅返回实际改变朝向的对象。
- ready模式产生READY事件；exhausted模式产生EXHAUST事件，分别适用对应替代、限制和触发；不能使用一个通用“状态改变”事件抹平二者。
- 已处于目标朝向不重复成功。进入场上的朝向使用play.entry或modify_entry；本函数只改变已存在对象的朝向。
- simultaneous及actor的意义与原ready／exhaust相同；作为费用时仍须完整支付，不把尽可能执行的效果冒充支付。

```python
ops.orient(selected_units, "ready")
ops.orient(selected_runes, "exhausted")
```

''' +s[b:]
a=s.index('### `empower` 强化');b=s.index('### `modify_might` 调整、设至或交换战力',a)
s=s[:a]+'''### `change_empowerment` 强化／解除一层强化

```python
change_empowerment(objects: Selection[Permanent | Legend], mode: str, *,
                   actor: Player = CONTROLLER) -> Result[list[Permanent | Legend]]
```

- mode闭集为empower、disempower；每次至多对各对象增加／移除一层，返回实际完成该模式动作的对象。
- empower模式保留EMPOWER动作身份：默认二元状态，已强化不再次成功；明确可叠层的对象检查自己的上限。
- disempower模式保留DISEMPOWER动作身份：未强化不变化；多层时只移除一层，不直接设成未强化。
- 模式分别适用成本、限制、替代和触发。判断成功使用实际返回对象，不以模式请求推定已发生；不改动规则所定义的强化期限。

```python
ops.change_empowerment(selected_units, "empower")
ops.change_empowerment(selected_units, "disempower")
```

''' +s[b:]
s=s.replace('BUFF / EMPOWER / EXHAUST / READY / XP','BUFF / EMPOWER / DISEMPOWER / EXHAUST / READY / XP')
s+='''
## 14. V2.1入口迁移

| V2.1入口 | V3正式调用 | 必须保留 |
| --- | --- | --- |
| ready(objects, ...) | orient(objects, "ready", ...) | READY事件与实际横置→活跃结果 |
| exhaust(objects, ...) | orient(objects, "exhausted", ...) | EXHAUST事件与实际活跃→横置结果 |
| empower(objects) | change_empowerment(objects, "empower") | 默认二元、特例叠层上限、EMPOWER事件 |
| disempower(objects) | change_empowerment(objects, "disempower") | 仅移除一层、DISEMPOWER事件 |

这四个旧函数名不属于V3正式API；成本类型中的具名动作、关键词和事件仍保留原本游戏身份。其余V2.1签名保持。
'''
p.write_text(s,encoding='utf-8')
names=re.findall(r'^### `([a-z_]+)`',s,re.M)
assert len(names)==len(set(names))==71
print('API V3 functions=71 sha256='+hashlib.sha256(p.read_bytes()).hexdigest())
