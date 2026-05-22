# 520-memorial 功能增强实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal**: 为 520-memorial 情侣纪念网站添加留言板、照片导出、音乐播放器，并优化大爱心视觉效果

**Architecture**: 在现有 Astro 静态站点基础上，通过 IndexedDB 扩展数据层（留言板），引入 JSZip 实现前端打包导出，恢复已删除的音乐播放器组件，调整 CSS 视觉参数

**Tech Stack**: Astro 5, Tailwind CSS 4, IndexedDB, JSZip

---

### 任务 1: 爱心 opacity 调整

**文件**:
- 修改: `src/components/Hero.astro:13`

- [ ] **Step 1: 调整 opacity**

```astro
<!-- 将 opacity: 0.06 改为 opacity: 0.12 -->
style="... opacity: 0.12; ..."
```

- [ ] **Step 2: 验证效果**

在浏览器中刷新页面，观察大爱心是否更明显（但仍保持背景感，不过于抢眼）

- [ ] **Step 3: 提交**

```bash
git add src/components/Hero.astro
git commit -m "style: 大爱心 opacity 0.06 → 0.12 增强心动效果"
```

---

### 任务 2: 恢复音乐播放器

**文件**:
- 恢复: `src/components/MusicPlayer.astro`
- 修改: `src/config.ts` (添加 musicUrl)
- 修改: `src/pages/index.astro` (引入 MusicPlayer)
- 复制: `夏夜最后的烟火 - 颜人中.mp3` → `public/music/bg.mp3`

- [ ] **Step 1: 复制音乐文件**

```powershell
Copy-Item "D:\编程\520-memorial\夏夜最后的烟火 - 颜人中.mp3" "d:\编程\520-memorial\public\music\bg.mp3"
```

- [ ] **Step 2: 恢复 config.ts 中的 musicUrl**

```typescript
export const config = {
  startDate: "2025-09-28",
  name1: "TT",
  name2: "CC",
  musicUrl: "/music/bg.mp3",
  pageTitle: "TT & CC - Our Love Story",
};
```

- [ ] **Step 3: 恢复 MusicPlayer.astro 组件**

创建文件 `src/components/MusicPlayer.astro`，内容与之前删除的相同（已验证过的版本）：
- 固定右下角播放器
- 旋转唱片 + 歌曲信息 + 播放按钮
- `is:inline` script + ES5 语法
- `DOMContentLoaded` 等待 + 动态设置 `audio.src`
- 点击播放按钮和整体区域切换

- [ ] **Step 4: 在 index.astro 中引入**

```astro
import MusicPlayer from "../components/MusicPlayer.astro";
// 在 BaseLayout 内添加:
<MusicPlayer />
```

- [ ] **Step 5: 浏览器验证**

点击播放按钮，确认音乐正常播放，控制台无错误

- [ ] **Step 6: 提交**

```bash
git add src/components/MusicPlayer.astro src/config.ts src/pages/index.astro public/music/
git commit -m "feat: 恢复音乐播放器组件"
```

---

### 任务 3: 存储层扩展（留言板数据）

**文件**:
- 修改: `src/lib/storage.ts`

- [ ] **Step 1: 扩展 storage.ts**

```typescript
import localforage from "localforage";

// 照片存储（已有）
export const photoStore = localforage.createInstance({
  name: "520-memorial",
  storeName: "photos",
});

// 新增：留言板存储
export const messageStore = localforage.createInstance({
  name: "520-memorial",
  storeName: "messages",
});
```

- [ ] **Step 2: 提交**

```bash
git add src/lib/storage.ts
git commit -m "feat: 存储层添加 messages store"
```

---

### 任务 4: 留言板组件

**文件**:
- 新建: `src/components/MessageBoard.astro`
- 修改: `src/pages/index.astro` (引入 MessageBoard)

- [ ] **Step 1: 创建 MessageBoard.astro**

```astro
---
/**
 * 留言板组件
 * 对话模式：双方可以互相留言，按时间倒序展示
 * IndexedDB 存储
 */
import { messageStore } from "../lib/storage";

interface Message {
  id: string;
  author: "TT" | "CC";
  content: string;
  createdAt: number;
}
---

<div class="max-w-[720px] mx-auto py-16 px-5" id="message-board">
  <!-- 标题 -->
  <h2 class="text-3xl font-light text-[#2C1A1E] text-center mb-8 tracking-wider" style="font-family: 'Playfair Display', serif;">
    写给对方的话
  </h2>
  
  <!-- 留言列表 -->
  <div id="message-list" class="space-y-4 mb-8 max-h-[400px] overflow-y-auto pr-2">
    <!-- 留言卡片通过 JS 动态渲染 -->
  </div>
  
  <!-- 空状态 -->
  <div id="message-empty" class="text-center py-8">
    <p class="text-[#C4A4AB] text-sm">还没有留言，写下第一句吧 💌</p>
  </div>
  
  <!-- 输入区 -->
  <div class="bg-white/60 rounded-[16px] p-4" style="backdrop-filter: blur(10px); border: 1px solid rgba(237,107,134,0.1);">
    <!-- 作者选择 -->
    <div class="flex gap-3 mb-3">
      <label class="flex items-center gap-2 cursor-pointer">
        <input type="radio" name="author" value="TT" checked class="accent-[#ED6B86]" />
        <span class="text-sm text-[#2C1A1E] font-medium">TT</span>
      </label>
      <label class="flex items-center gap-2 cursor-pointer">
        <input type="radio" name="author" value="CC" class="accent-[#ED6B86]" />
        <span class="text-sm text-[#2C1A1E] font-medium">CC</span>
      </label>
    </div>
    <!-- 输入框 -->
    <div class="flex gap-3">
      <textarea 
        id="message-input" 
        class="flex-1 rounded-[12px] px-4 py-3 text-sm resize-none border border-[#F5A8B8] focus:outline-none focus:border-[#ED6B86]" 
        style="background: rgba(255,255,255,0.8); font-family: 'Noto Serif SC', serif;"
        placeholder="写下你想说的话..."
        maxlength="500"
        rows="2"
      ></textarea>
      <button 
        id="send-btn"
        class="bg-[#ED6B86] text-white rounded-[12px] px-5 py-3 text-sm font-medium hover:bg-[#D4507A] transition-colors self-end"
      >
        发送
      </button>
    </div>
  </div>
</div>

<script is:inline>
  (function() {
    // HTML 转义
    function escapeHtml(str) {
      var div = document.createElement("div");
      div.appendChild(document.createTextNode(str));
      return div.innerHTML;
    }
    
    // 格式化时间
    function formatTime(ts) {
      var now = Date.now();
      var diff = now - ts;
      var minutes = Math.floor(diff / 60000);
      var hours = Math.floor(diff / 3600000);
      var days = Math.floor(diff / 86400000);
      
      if (minutes < 1) return "刚刚";
      if (minutes < 60) return minutes + " 分钟前";
      if (hours < 24) return hours + " 小时前";
      if (days < 30) return days + " 天前";
      
      var date = new Date(ts);
      return date.getFullYear() + "/" + (date.getMonth()+1) + "/" + date.getDate();
    }
    
    // 加载留言
    function loadMessages() {
      var listEl = document.getElementById("message-list");
      var emptyEl = document.getElementById("message-empty");
      if (!listEl || !emptyEl) return;
      
      // 从 IndexedDB 读取
      var dbRequest = indexedDB.open("520-memorial");
      dbRequest.onsuccess = function(e) {
        var db = e.target.result;
        var tx = db.transaction("messages", "readonly");
        var store = tx.objectStore("messages");
        var getAll = store.getAll();
        
        getAll.onsuccess = function() {
          var messages = getAll.result;
          
          if (messages.length === 0) {
            emptyEl.style.display = "block";
            listEl.innerHTML = "";
            return;
          }
          
          emptyEl.style.display = "none";
          
          // 按时间倒序
          messages.sort(function(a, b) { return b.createdAt - a.createdAt; });
          
          var html = "";
          for (var i = 0; i < messages.length; i++) {
            var msg = messages[i];
            var isTT = msg.author === "TT";
            var tagColor = isTT ? "bg-blue-100 text-blue-700" : "bg-pink-100 text-pink-700";
            var safeContent = escapeHtml(msg.content);
            
            html += '<div class="bg-white/60 rounded-[12px] p-4 relative" style="backdrop-filter: blur(8px); border: 1px solid rgba(237,107,134,0.08);">' +
              '<div class="flex items-start gap-3">' +
              '<span class="inline-block px-2 py-0.5 rounded text-xs font-medium ' + tagColor + '">' + escapeHtml(msg.author) + '</span>' +
              '<div class="flex-1">' +
              '<p class="text-[#2C1A1E] text-sm leading-relaxed" style="font-family: \'Noto Serif SC\', serif;">' + safeContent + '</p>' +
              '<p class="text-[#C4A4AB] text-xs mt-2">' + formatTime(msg.createdAt) + '</p>' +
              '</div>' +
              '<button onclick="window.deleteMessage(\'' + msg.id + '\')" class="text-[#C4A4AB] hover:text-[#ED6B86] transition-colors p-1">' +
              '<svg class="w-4 h-4" style="stroke: currentColor; stroke-width: 1.5; fill: none;" viewBox="0 0 24 24">' +
              '<path d="M6 18L18 6M6 6l12 12" stroke-linecap="round"/></svg></button>' +
              '</div></div>';
          }
          listEl.innerHTML = html;
        };
      };
    }
    
    // 删除留言
    window.deleteMessage = function(id) {
      if (!confirm("确定要删除这条留言吗？")) return;
      
      var dbRequest = indexedDB.open("520-memorial");
      dbRequest.onsuccess = function(e) {
        var db = e.target.result;
        var tx = db.transaction("messages", "readwrite");
        var store = tx.objectStore("messages");
        store.delete(id);
        tx.oncomplete = function() {
          loadMessages();
        };
      };
    };
    
    // 发送留言
    var sendBtn = document.getElementById("send-btn");
    var inputEl = document.getElementById("message-input");
    
    if (sendBtn && inputEl) {
      sendBtn.addEventListener("click", function() {
        var content = inputEl.value.trim();
        if (!content) return;
        
        var authorEl = document.querySelector('input[name="author"]:checked');
        var author = authorEl ? authorEl.value : "TT";
        
        var message = {
          id: Date.now().toString(36) + Math.random().toString(36).slice(2),
          author: author,
          content: content,
          createdAt: Date.now()
        };
        
        var dbRequest = indexedDB.open("520-memorial");
        dbRequest.onsuccess = function(e) {
          var db = e.target.result;
          var tx = db.transaction("messages", "readwrite");
          var store = tx.objectStore("messages");
          store.put(message);
          tx.oncomplete = function() {
            inputEl.value = "";
            loadMessages();
          };
        };
      });
    }
    
    // 初始化加载
    loadMessages();
  })();
</script>
```

- [ ] **Step 2: 在 index.astro 中引入**

```astro
import MessageBoard from "../components/MessageBoard.astro";
// 在 PhotoModal 后添加:
<MessageBoard />
```

- [ ] **Step 3: 浏览器验证**
  1. 选择 TT，写一条留言，点击发送，确认显示
  2. 选择 CC，写一条留言，确认标签颜色不同（蓝色 vs 粉色）
  3. 点击删除按钮，确认删除成功
  4. 留言超过 500 字时无法输入（maxlength 限制）

- [ ] **Step 4: 提交**

```bash
git add src/components/MessageBoard.astro src/pages/index.astro
git commit -m "feat: 新增留言板组件（对话模式）"
```

---

### 任务 5: 照片 ZIP 导出

**文件**:
- 修改: `src/components/PhotoGallery.astro`
- 依赖: `npm install jszip`

- [ ] **Step 1: 安装 JSZip**

```bash
npm install jszip
```

- [ ] **Step 2: 在 PhotoGallery.astro 中添加导出按钮和逻辑**

在标题右侧添加导出按钮：
```astro
<!-- 在 <h2>Our Moments</h2> 后添加 -->
<button id="export-btn" class="ml-3 px-3 py-1.5 rounded-full text-xs font-medium transition-colors hover:scale-105" style="background: rgba(237,107,134,0.1); color: #ED6B86; border: 1px solid rgba(237,107,134,0.2);" onclick="window.exportPhotos()">
  <svg class="w-3.5 h-3.5 inline mr-1" style="stroke: currentColor; stroke-width: 2; fill: none;" viewBox="0 0 24 24">
    <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1M12 12V4m0 0l-4 4m4-4l4 4" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  导出照片
</button>
```

在 script 中添加导出函数：
```javascript
window.exportPhotos = function() {
  var dbRequest = indexedDB.open("520-memorial");
  dbRequest.onsuccess = function(e) {
    var db = e.target.result;
    var tx = db.transaction("photos", "readonly");
    var store = tx.objectStore("photos");
    var getAll = store.getAll();
    
    getAll.onsuccess = function() {
      var photos = getAll.result;
      if (photos.length === 0) {
        alert("暂无照片可导出");
        return;
      }
      
      // 使用 JSZip 打包
      var JSZip = window.JSZip;
      var zip = new JSZip();
      var folder = zip.folder("520-photos");
      
      var count = 0;
      for (var i = 0; i < photos.length; i++) {
        var p = photos[i];
        var dataUrl = p.dataUrl;
        // dataUrl 格式: "data:image/jpeg;base64,..."
        var base64 = dataUrl.split(",")[1];
        var filename = "photo_" + String(i + 1).padStart(3, "0") + ".jpg";
        folder.file(filename, base64, {base64: true});
        count++;
      }
      
      zip.generateAsync({type: "blob"}).then(function(content) {
        // 触发下载
        var a = document.createElement("a");
        a.href = URL.createObjectURL(content);
        a.download = "520-photos-" + photos.length + "张.zip";
        a.click();
        URL.revokeObjectURL(a.href);
      });
    };
  };
};
```

- [ ] **Step 3: 在页面中引入 JSZip CDN**

在 `src/layouts/BaseLayout.astro` 的 `<head>` 中添加：
```html
<script src="https://unpkg.com/jszip@3.10.1/dist/jszip.min.js" defer></script>
```

- [ ] **Step 4: 浏览器验证**
  1. 上传 2-3 张照片
  2. 点击"导出照片"按钮
  3. 确认浏览器下载了 ZIP 文件
  4. 解压 ZIP，确认照片正常

- [ ] **Step 5: 提交**

```bash
git add src/components/PhotoGallery.astro src/layouts/BaseLayout.astro package.json package-lock.json
git commit -m "feat: 添加照片 ZIP 导出功能"
```

---

## 执行顺序

1. 任务 1 → 2 → 3 → 4 → 5（按此顺序）
2. 每完成一个任务后立即验证
3. 任务间无依赖阻塞，但建议按序执行以保持一致性

## 回归测试

每完成一个任务后，验证以下核心功能未受影响：
- 计时器正常显示
- 爱心背景正常
- 照片上传/预览/删除正常
