<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2024-06-01 17:49:33
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2024-06-01 18:21:49
 * @FilePath: \llm-robotic-control\todo\index.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# TODO

## LLM model return json 格式

### 直接模式

直接返回舵機轉動角度

```json
{
    "servo1": 90,
    "servo2": 90,
    "servo3": 90,
    "servo4": 90,
    "servo5": 90,
    "servo6": 90
}
```

- 這個方案可能需要把舵機分布一併告知 LLM model

#### 修改後

選用此方案

#### 格式

```json
{
    "goal": "Take nearest red box",
    "tasks":[
        {
            "action":{
                "servo1": 90,
                "servo2": 90,
                "servo3": 90,
                "servo4": 90,
                "servo5": 90,
                "servo6": 90
            },
            "check_point": "description of check point 1"
        },
        {
            "action":{
                "servo1": 90,
                "servo2": 90,
                "servo3": 90,
                "servo4": 90,
                "servo5": 90,
                "servo6": 90
            },
            "check_point": "description of check point 2"
        }
    ]
}
```

### 間接模式

返回動作名稱，動作已經被預先設定好

```json
{
    "action": "stand",
    "power": 10,
    "seconds": 1
}
```