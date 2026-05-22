# 520-memorial Bug 修复变更说明

**日期**：2026-05-21
**变更类型**：Bug 修复
**影响范围**：全项目

---

## 变更描述

修复项目代码审查中发现的 11 个 bug，涵盖代码质量、安全性、工程规范三个维度。

## Bug 清单

### CRITICAL（必须修复）

| # | Bug | 涉及文件 | 说明 |
|---|-----|---------|------|
| 1 | `storage.ts` 死代码 + localforage 未使用 | `src/lib/storage.ts`, `package.json` | storage.ts 定义了 localforage 封装但从未被引用，PhotoGallery 和 MessageBoard 直接操作原生 IndexedDB API。localforage 依赖多余 |
| 2 | JSZip CDN + npm 双重引入 | `src/layouts/BaseLayout.astro`, `package.json` | CDN `<script>` 引入不可靠，且与 npm 依赖冗余 |
| 3 | `file.name` 只读属性赋值无效 | `src/components/PhotoGallery.astro` | File 对象的 name 属性是只读的，截断逻辑静默失败 |

### IMPORTANT（强烈建议修复）

| # | Bug | 涉及文件 | 说明 |
|---|-----|---------|------|
| 4 | 全局变量污染 | `PhotoGallery.astro`, `MessageBoard.astro` | previewPhoto、deletePhoto、closePhotoModal、exportPhotos、deleteMessage 直接挂在 window 上，缺乏命名空间 |
| 5 | 留言板 IndexedDB 初始化缺失 | `MessageBoard.astro` | 没有 onupgradeneeded 创建 objectStore，首次访问可能报错 |
| 6 | 照片 Base64 存储容量风险 | `PhotoGallery.astro` | Base64 比二进制大 33%，多张照片容易撑爆 IndexedDB 配额，且无容量提示 |
| 7 | 缺少 `.gitignore` | 项目根目录 | dist/、.astro/、node_modules/ 等可能被提交 |
| 8 | dist/、音乐文件、临时文件入库 | 仓库 | 仓库体积膨胀 + 版权风险 |

### MINOR（可选修复）

| # | Bug | 涉及文件 | 说明 |
|---|-----|---------|------|
| 9 | 计时器 setInterval 无清理 | `Hero.astro` | 页面卸载时未清除定时器 |
| 10 | 照片墙 innerHTML 拼接 | `PhotoGallery.astro` | dataUrl 转义不够全面，建议用 DOM API |
| 11 | tsconfig 路径别名未使用 | `tsconfig.json` | 配置了 @/* 别名但代码中全用相对路径 |

## 受影响的已有模块

- **PhotoGallery.astro**：Bug 1/3/4/6/10 均涉及，改动最大
- **MessageBoard.astro**：Bug 4/5 涉及，需补充 IndexedDB 初始化
- **BaseLayout.astro**：Bug 2 涉及，移除 CDN script
- **Hero.astro**：Bug 9 涉及，添加定时器清理
- **storage.ts**：Bug 1 涉及，删除或重构
- **package.json**：Bug 1/2 涉及，移除 localforage，确认 jszip 依赖
- **tsconfig.json**：Bug 11 涉及
- **项目根目录**：Bug 7/8 涉及，新增 .gitignore，清理文件

## 风险评估

- **低风险**：Bug 7/8/9/11 为纯配置/清理类修改，不影响运行时行为
- **中风险**：Bug 2/3/4/5/10 需修改组件脚本逻辑，需回归验证照片上传/预览/删除/导出、留言发送/删除功能
- **高风险**：Bug 1/6 涉及存储层重构，需确保 IndexedDB 数据兼容性（旧数据不丢失）

## 修复策略

1. **统一 IndexedDB 操作**：删除 storage.ts 死代码，将 PhotoGallery 和 MessageBoard 中的原生 IndexedDB 操作提取为统一的命名空间化工具函数，挂在 `window.Love520` 下
2. **JSZip 改用 npm import**：移除 CDN script，在导出函数中动态 import jszip
3. **file.name 截断**：改用新变量存储截断后的名称
4. **Base64 → Blob 存储**：照片存储改用 Blob 替代 Base64，减少约 33% 存储占用
5. **添加 .gitignore**：排除 dist/、.astro/、node_modules/、音乐文件等
