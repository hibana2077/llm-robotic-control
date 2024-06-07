<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2024-06-07 16:57:38
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2024-06-07 16:59:31
 * @FilePath: \llm-robotic-control\src\lab\plot\template_2\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# Detailed Sequential Instruction Prompt

```python
template = ChatPromptTemplate.from_messages([
    ('system', "You are an AI Assistant tasked with helping the user operate a robotic arm. Your role is to provide precise and sequential guidance."),
    ('system', "When the user issues a command, your response should lay out the step-by-step actions necessary to execute it using the RoboticArmOperation tool. Ensure each step is clear and actionable."),
])
```

「Detailed Sequential Instruction Prompt」這個提示模板的特點是專注於提供精確且有序的操作指導。以下是它的幾個關鍵特點：

1. **精確性**: 此模板強調指令的精確性，要求AI助理在解釋每個步驟時必須非常具體，確保用戶可以清晰地執行每個操作。

2. **步驟性**: 透過分解任務到具體的步驟，此模板使得操作流程變得更加清楚與可追踪。這種方法適合複雜的操作，幫助避免任何可能的錯誤或遺漏。

3. **有序性**: 這種提示風格注重步驀間的邏輯順序，確保用戶按照正確的順序執行操作，從而提高操作的效率和安全性。

總之，「Detailed Sequential Instruction Prompt」是專為需要細致操作指導的情景設計，適合在需要高度控制和精確操作的技術或工業應用中使用。