# 520-memorial 功能变更设计文档

**日期**: 2026-05-21
**类型**: 功能增删

---

## 一、变更概述

本次变更包含 5 个独立功能模块，均属于在已有项目上增删功能：

| # | 功能 | 类型 | 复杂度 |
|---|------|------|--------|
| 1 | 爱心 opacity 调整 | 样式微调 | 极低 |
| 2 | 音乐播放器恢复 | 恢复已删除组件 | 低 |
| 3 | 留言板（对话模式） | 新增功能 | 中 |
| 4 | 照片 ZIP 导出 | 新增功能 | 中 |
| 5 | 部署到线上 | 推迟到后续 | - |

---

## 二、详细设计

### 2.1 爱心 opacity 调整

**文件**: `src/components/Hero.astro`

**改动**: 将大爱心背景光晕的 `opacity: 0.06` 调整为 `opacity: 0.12`

**原因**: 当前 0.06 太淡，"心动"效果不明显

**风险评估**: 极低（一行 CSS 改动）

---

### 2.2 音乐播放器恢复

**文件**: 
- 恢复 `src/components/MusicPlayer.astro`
- 更新 `src/config.ts` 添加 `musicUrl`
- 更新 `src/pages/index.astro` 引入组件

**音乐文件**: `D:\编程\520-memorial\夏夜最后的烟火 - 颜人中.mp3`
- 文件头 `ID3` 确认是标准 MP3 格式
- 复制到 `public/music/bg.mp3`

**风险评估**: 低（组件之前已实现过，只是恢复）

---

### 2.3 留言板（对话模式）

**新增文件**:
- `src/components/MessageBoard.astro` — 留言板组件

**数据结构** (IndexedDB):
```typescript
interface Message {
  id: string;           // 唯一 ID
  author: "TT" | "CC";  // 作者
  content: string;       // 留言内容
  createdAt: number;     // 创建时间戳
}
```

**UI 设计**:
- 位于照片墙下方
- 标题："写给对方的话"
- 每条留言卡片：
  - 左上角名字标签（"TT" 或 "CC"）
  - TT 的标签用蓝色背景，CC 的标签用粉色背景
  - 留言内容
  - 时间显示（如"3 天前"）
  - 删除按钮（仅自己的留言可删除）
- 底部输入区：
  - 选择作者（TT / CC 单选按钮）
  - 文本输入框
  - 发送按钮

**存储层**: 复用现有 `src/lib/storage.ts`，新增 `messages` store

**风险评估**: 中（新增数据层，需测试 CRUD）

---

### 2.4 照片 ZIP 导出

**新增文件**:
- 无需新增文件，在 `PhotoGallery.astro` 中添加导出按钮

**依赖**: 引入 JSZip 库 (`npm install jszip`)

**功能**:
- 照片墙右上角添加"导出照片"按钮
- 点击后遍历 IndexedDB 中所有照片
- 将每张照片的 dataUrl 转为 Blob，添加到 ZIP
- 文件命名：`photo_001.jpg`, `photo_002.jpg` ...
- 触发浏览器下载 `520-photos.zip`

**风险评估**: 中（依赖第三方库，需测试大文件导出）

---

## 三、影响范围分析

| 已有模块 | 是否受影响 | 说明 |
|----------|------------|------|
| Hero.astro | 是 | opacity 调整 |
| PhotoGallery.astro | 是 | 添加导出按钮 |
| config.ts | 是 | 恢复 musicUrl |
| index.astro | 是 | 引入 MusicPlayer 和 MessageBoard |
| storage.ts | 是 | 新增 messages store |
| FloatingHearts.astro | 否 | 无变更 |
| PhotoModal.astro | 否 | 无变更 |

---

## 四、执行顺序

1. 爱心 opacity 调整（最快，先验证视觉）
2. 音乐播放器恢复（简单，先确认音乐文件可用）
3. 留言板（新增功能，中等复杂度）
4. 照片 ZIP 导出（新增功能，中等复杂度）
5. 部署（推迟）

---

## 五、风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| IndexedDB 存储超限 | 低 | 中 | 留言限制单条 500 字 |
| JSZip 导出大文件崩溃 | 中 | 低 | 限制一次最多导出 100 张 |
| 音乐文件兼容性问题 | 低 | 低 | 已确认 ID3 格式 |
| 留言板 XSS 注入 | 低 | 中 | content 需 HTML 转义 |
