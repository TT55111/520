# 520-memorial Bug 修复实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复 520-memorial 项目代码审查中发现的 11 个 bug，涵盖代码质量、安全性、工程规范

**Architecture:** 统一 IndexedDB 操作到命名空间化工具函数（`window.Love520`），移除死代码和冗余依赖，修复运行时 bug，清理仓库

**Tech Stack:** Astro 5, Tailwind CSS 4, TypeScript, IndexedDB, JSZip (npm)

**工作目录：** `D:\编程\520-memorial\.worktrees\bugfix`

---

## 文件结构

| 操作 | 文件 | 职责 |
|------|------|------|
| 删除 | `src/lib/storage.ts` | 死代码，功能已内联在组件中 |
| 修改 | `src/lib/db.ts`（新建） | 统一的 IndexedDB 操作封装 |
| 修改 | `src/components/PhotoGallery.astro` | 修复 bug 3/4/6/10，使用 db.ts |
| 修改 | `src/components/MessageBoard.astro` | 修复 bug 4/5，使用 db.ts |
| 修改 | `src/components/PhotoModal.astro` | 配合命名空间调整 |
| 修改 | `src/components/Hero.astro` | 修复 bug 9 |
| 修改 | `src/layouts/BaseLayout.astro` | 移除 CDN script（bug 2） |
| 修改 | `package.json` | 移除 localforage（bug 1） |
| 修改 | `tsconfig.json` | 移除未使用路径别名（bug 11） |
| 修改 | `.gitignore` | 已创建，需补充完善 |
| 删除 | 仓库中的音乐文件和临时文件 | bug 8 |

---

### Task 1: 创建统一的 IndexedDB 工具模块

**Files:**
- 创建: `src/lib/db.ts`
- 删除: `src/lib/storage.ts`

**受影响的已有模块：** PhotoGallery.astro, MessageBoard.astro（后续 Task 会迁移）

- [ ] **Step 1: 创建 `src/lib/db.ts`，封装统一的 IndexedDB 操作**

```typescript
/**
 * 统一的 IndexedDB 操作封装
 * 数据库名：love520，包含 photos 和 messages 两个 objectStore
 * 所有组件通过此模块操作数据库，避免重复的初始化逻辑
 */

// 数据库配置常量
const DB_NAME = "love520";
const DB_VERSION = 1;

// 照片数据结构
export interface PhotoItem {
  id: string;
  dataUrl: string;
  name: string;
  uploadedAt: number;
}

// 留言数据结构
export interface MessageItem {
  id: string;
  author: string;
  content: string;
  createdAt: number;
}

/**
 * 打开/创建数据库
 * onupgradeneeded 中统一创建所有 objectStore
 * 确保首次访问时数据库结构正确初始化
 */
function openDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const db = (e.target as IDBOpenDBRequest).result;
      // 如果 photos store 不存在则创建
      if (!db.objectStoreNames.contains("photos")) {
        db.createObjectStore("photos", { keyPath: "id" });
      }
      // 如果 messages store 不存在则创建
      if (!db.objectStoreNames.contains("messages")) {
        db.createObjectStore("messages", { keyPath: "id" });
      }
    };
    req.onsuccess = (e) => {
      resolve((e.target as IDBOpenDBRequest).result);
    };
    req.onerror = (e) => {
      reject((e.target as IDBOpenDBRequest).error);
    };
  });
}

/**
 * 通用事务执行函数
 * 减少重复的事务创建代码
 */
function withTransaction<T>(
  storeName: string,
  mode: IDBTransactionMode,
  fn: (store: IDBObjectStore) => IDBRequest<T>
): Promise<T> {
  return openDB().then((db) => {
    return new Promise<T>((resolve, reject) => {
      const tx = db.transaction(storeName, mode);
      const store = tx.objectStore(storeName);
      const request = fn(store);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
      tx.oncomplete = () => db.close();
    });
  });
}

// ==================== 照片操作 ====================

/** 保存照片 */
export async function savePhoto(photo: PhotoItem): Promise<void> {
  await withTransaction("photos", "readwrite", (store) => store.put(photo));
}

/** 获取所有照片（按上传时间倒序） */
export async function getAllPhotos(): Promise<PhotoItem[]> {
  const all = await withTransaction<PhotoItem[]>("photos", "readonly", (store) => store.getAll());
  return all.sort((a, b) => b.uploadedAt - a.uploadedAt);
}

/** 删除照片 */
export async function deletePhoto(id: string): Promise<void> {
  await withTransaction("photos", "readwrite", (store) => store.delete(id));
}

// ==================== 留言操作 ====================

/** 保存留言 */
export async function saveMessage(msg: MessageItem): Promise<void> {
  await withTransaction("messages", "readwrite", (store) => store.put(msg));
}

/** 获取所有留言（按创建时间倒序） */
export async function getAllMessages(): Promise<MessageItem[]> {
  const all = await withTransaction<MessageItem[]>("messages", "readonly", (store) => store.getAll());
  return all.sort((a, b) => b.createdAt - a.createdAt);
}

/** 删除留言 */
export async function deleteMessage(id: string): Promise<void> {
  await withTransaction("messages", "readwrite", (store) => store.delete(id));
}

// ==================== 工具函数 ====================

/** 生成唯一 ID */
export function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}
```

- [ ] **Step 2: 删除 `src/lib/storage.ts`**

该文件定义的 localforage 封装从未被使用，PhotoGallery 和 MessageBoard 都直接操作原生 IndexedDB。删除此死代码。

- [ ] **Step 3: 提交**

```bash
git add src/lib/db.ts
git rm src/lib/storage.ts
git commit -m "refactor: 创建统一 IndexedDB 工具模块，删除未使用的 storage.ts"
```

---

### Task 2: 重构 PhotoGallery.astro — 修复 bug 3/4/6/10

**Files:**
- 修改: `src/components/PhotoGallery.astro`

**受影响的已有模块：** 照片上传、预览、删除、导出功能

**Bug 修复清单：**
- Bug 3: `file.name` 只读属性赋值无效 → 用新变量存储截断后的名称
- Bug 4: 全局变量污染 → 收拢到 `window.Love520` 命名空间
- Bug 6: Base64 存储容量风险 → 添加存储容量提示
- Bug 10: innerHTML 拼接 → 改用 DOM API 创建元素

- [ ] **Step 1: 重写 PhotoGallery.astro 的 script 部分**

将整个 `<script is:inline>` 替换为以下内容（保留组件模板部分不变）：

```html
<script is:inline>
(function() {
  // ==================== 命名空间 ====================
  // 所有全局函数收拢到 Love520 命名空间，避免污染 window
  window.Love520 = window.Love520 || {};

  var photos = [];

  // ==================== 工具函数 ====================

  /** HTML 转义：防止 XSS 注入 */
  function escapeHtml(str) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  /** 生成唯一 ID */
  function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2);
  }

  // ==================== IndexedDB 操作 ====================
  // 统一使用 love520 数据库，包含 photos 和 messages 两个 store
  // onupgradeneeded 中确保两个 store 都被创建

  var DB_NAME = "love520";
  var DB_VERSION = 1;

  function openDB(callback) {
    var req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = function(e) {
      var db = e.target.result;
      if (!db.objectStoreNames.contains("photos")) {
        db.createObjectStore("photos", { keyPath: "id" });
      }
      if (!db.objectStoreNames.contains("messages")) {
        db.createObjectStore("messages", { keyPath: "id" });
      }
    };
    req.onsuccess = function(e) {
      callback(e.target.result);
    };
    req.onerror = function(e) {
      console.error("IndexedDB 打开失败:", e.target.error);
    };
  }

  // ==================== 照片 CRUD ====================

  /** 压缩图片：限制最大尺寸 800px，JPEG 质量 0.8 */
  function compressImage(file, callback) {
    var reader = new FileReader();
    reader.onload = function(e) {
      var img = new Image();
      img.onload = function() {
        var canvas = document.createElement("canvas");
        var maxSize = 800;
        var width = img.width;
        var height = img.height;

        if (width > height && width > maxSize) {
          height = (maxSize / width) * height;
          width = maxSize;
        } else if (height > maxSize) {
          width = (maxSize / height) * width;
          height = maxSize;
        }

        canvas.width = width;
        canvas.height = height;
        canvas.getContext("2d").drawImage(img, 0, 0, width, height);
        callback(canvas.toDataURL("image/jpeg", 0.8));
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  /** 保存照片到 IndexedDB */
  function savePhoto(photo, callback) {
    openDB(function(db) {
      var tx = db.transaction("photos", "readwrite");
      tx.objectStore("photos").put(photo);
      tx.oncomplete = function() {
        db.close();
        if (callback) callback();
      };
    });
  }

  /** 获取所有照片（按上传时间倒序） */
  function getAllPhotos(callback) {
    openDB(function(db) {
      var tx = db.transaction("photos", "readonly");
      var store = tx.objectStore("photos");
      var all = [];
      store.openCursor().onsuccess = function(e) {
        var cursor = e.target.result;
        if (cursor) {
          all.push(cursor.value);
          cursor.continue();
        } else {
          all.sort(function(a, b) { return b.uploadedAt - a.uploadedAt; });
          db.close();
          callback(all);
        }
      };
    });
  }

  /** 删除照片 */
  function deletePhotoById(id, callback) {
    openDB(function(db) {
      var tx = db.transaction("photos", "readwrite");
      tx.objectStore("photos").delete(id);
      tx.oncomplete = function() {
        db.close();
        if (callback) callback();
      };
    });
  }

  // ==================== 渲染 ====================

  /** 使用 DOM API 创建照片卡片（修复 Bug 10: innerHTML 拼接风险） */
  function createPhotoCard(p, index) {
    var card = document.createElement("div");
    card.className = "break-inside-avoid mb-3.5 rounded-[16px] overflow-hidden relative cursor-pointer group";
    card.style.cssText = "border: 1px solid rgba(237,107,134,0.08); transition: all 0.3s ease;";

    // 照片图片
    var img = document.createElement("img");
    img.src = p.dataUrl;
    img.alt = p.name;
    img.className = "w-full h-auto block";
    img.loading = "lazy";
    card.appendChild(img);

    // 悬浮操作层
    var overlay = document.createElement("div");
    overlay.className = "absolute inset-0 flex items-end p-4 opacity-0 group-hover:opacity-100 transition-opacity";
    overlay.style.background = "linear-gradient(to top, rgba(44,26,30,0.5) 0%, transparent 50%)";

    var btnGroup = document.createElement("div");
    btnGroup.className = "flex gap-2";

    // 预览按钮
    var previewBtn = document.createElement("button");
    previewBtn.className = "bg-white/90 rounded-full w-10 h-10 flex items-center justify-center hover:scale-110 transition-transform";
    previewBtn.innerHTML = '<svg class="w-4 h-4" style="stroke: #D4507A; stroke-width: 2; fill: none;" viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="3"/></svg>';
    previewBtn.addEventListener("click", function(e) {
      e.stopPropagation();
      window.Love520.previewPhoto(index);
    });

    // 删除按钮
    var deleteBtn = document.createElement("button");
    deleteBtn.className = "bg-white/90 rounded-full w-10 h-10 flex items-center justify-center hover:scale-110 transition-transform";
    deleteBtn.innerHTML = '<svg class="w-4 h-4" style="stroke: #D4507A; stroke-width: 2; fill: none;" viewBox="0 0 24 24"><path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    deleteBtn.addEventListener("click", function(e) {
      e.stopPropagation();
      window.Love520.deletePhoto(index);
    });

    btnGroup.appendChild(previewBtn);
    btnGroup.appendChild(deleteBtn);
    overlay.appendChild(btnGroup);
    card.appendChild(overlay);

    // 悬浮效果
    card.addEventListener("mouseenter", function() {
      card.style.transform = "translateY(-3px)";
      card.style.boxShadow = "0 8px 30px rgba(237,107,134,0.15)";
    });
    card.addEventListener("mouseleave", function() {
      card.style.transform = "";
      card.style.boxShadow = "";
    });

    // 点击预览
    card.addEventListener("click", function() {
      window.Love520.previewPhoto(index);
    });

    return card;
  }

  /** 渲染照片列表 */
  function renderPhotos(photosList) {
    var photoWall = document.getElementById("photo-wall");
    var emptyState = document.getElementById("empty-state");

    if (!photoWall || !emptyState) return;

    if (photosList.length === 0) {
      emptyState.style.display = "block";
      photoWall.innerHTML = "";
      return;
    }

    emptyState.style.display = "none";
    // 清空后用 DOM API 逐个添加
    photoWall.innerHTML = "";
    for (var i = 0; i < photosList.length; i++) {
      photoWall.appendChild(createPhotoCard(photosList[i], i));
    }
  }

  /** 加载照片 */
  function loadPhotos() {
    getAllPhotos(function(list) {
      photos = list;
      renderPhotos(list);
    });
  }

  // ==================== 文件上传 ====================

  /** 处理上传的文件 */
  function handleFiles(files) {
    var MAX_SIZE = 10 * 1024 * 1024; // 10MB
    var MAX_NAME_LEN = 100;
    var remaining = 0;

    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      // 安全校验：只允许图片文件
      if (!file.type || !file.type.startsWith("image/")) {
        continue;
      }
      // 安全校验：文件大小限制
      if (file.size > MAX_SIZE) {
        alert("文件 " + file.name + " 超过 10MB 限制，已跳过");
        continue;
      }

      remaining++;
      (function(file) {
        compressImage(file, function(dataUrl) {
          // Bug 3 修复：file.name 是只读属性，使用新变量存储截断后的名称
          var safeName = file.name.length > MAX_NAME_LEN
            ? file.name.substring(0, MAX_NAME_LEN) + "..."
            : file.name;

          var photo = {
            id: generateId(),
            dataUrl: dataUrl,
            name: safeName,
            uploadedAt: Date.now()
          };

          savePhoto(photo, function() {
            remaining--;
            if (remaining === 0) {
              loadPhotos();
              // Bug 6 修复：上传完成后检查存储容量
              checkStorageQuota();
            }
          });
        });
      })(file);
    }
  }

  // ==================== 存储容量检查（Bug 6） ====================

  /** 检查 IndexedDB 存储使用量，接近上限时提示用户 */
  function checkStorageQuota() {
    if (navigator.storage && navigator.storage.estimate) {
      navigator.storage.estimate().then(function(est) {
        var usedMB = (est.usage / (1024 * 1024)).toFixed(1);
        var quotaMB = (est.quota / (1024 * 1024)).toFixed(0);
        var usagePercent = est.usage / est.quota;

        // 使用超过 80% 时警告
        if (usagePercent > 0.8) {
          console.warn("存储空间使用率超过 80%: " + usedMB + "MB / " + quotaMB + "MB");
          alert("存储空间即将用尽（已用 " + usedMB + "MB / " + quotaMB + "MB），建议导出照片后清理，避免数据丢失。");
        }
      });
    }
  }

  // ==================== 全局函数（命名空间化，修复 Bug 4） ====================

  /** 预览照片 */
  window.Love520.previewPhoto = function(index) {
    if (!photos[index]) return;
    var dataUrl = photos[index].dataUrl;
    var modal = document.getElementById("photo-modal");
    var modalImg = document.getElementById("modal-image");
    var modalContent = modal ? modal.querySelector("div") : null;
    if (modal && modalImg) {
      modalImg.src = dataUrl;
      modal.classList.remove("hidden");
      modal.classList.add("flex", "modal-enter-active");
      if (modalContent) modalContent.classList.add("modal-content-enter-active");
      setTimeout(function() {
        if (modal) modal.classList.remove("modal-enter-active");
        if (modalContent) modalContent.classList.remove("modal-content-enter-active");
      }, 300);
    }
  };

  /** 删除照片 */
  window.Love520.deletePhoto = function(index) {
    if (!photos[index]) return;
    if (confirm("确定要删除这张照片吗？")) {
      deletePhotoById(photos[index].id, function() {
        loadPhotos();
      });
    }
  };

  /** 关闭照片 Modal */
  window.Love520.closePhotoModal = function(e) {
    if (e && e.target !== e.currentTarget) return;
    var modal = document.getElementById("photo-modal");
    var modalContent = modal ? modal.querySelector("div") : null;
    if (modal) {
      modal.classList.add("modal-exit-active");
      if (modalContent) modalContent.classList.add("modal-content-exit-active");
      setTimeout(function() {
        modal.classList.add("hidden");
        modal.classList.remove("flex", "modal-exit-active");
        if (modalContent) modalContent.classList.remove("modal-content-exit-active");
      }, 200);
    }
  };

  /** 导出照片为 ZIP（Bug 2 修复：使用 npm import 替代 CDN） */
  window.Love520.exportPhotos = async function() {
    // 动态 import jszip（从 npm 打包的模块）
    var JSZip;
    try {
      var module = await import("/jszip");
      JSZip = module.default || module;
    } catch (err) {
      // 回退：尝试从全局获取（兼容旧 CDN 加载方式）
      JSZip = window.JSZip;
    }

    if (!JSZip) {
      alert("导出组件加载失败，请刷新页面重试");
      return;
    }

    openDB(function(db) {
      var tx = db.transaction("photos", "readonly");
      var store = tx.objectStore("photos");
      var all = [];
      store.openCursor().onsuccess = function(e) {
        var cursor = e.target.result;
        if (cursor) {
          all.push(cursor.value);
          cursor.continue();
        } else {
          db.close();
          onPhotosLoaded(all, JSZip);
        }
      };
    });
  };

  /** 处理照片数据并生成 ZIP */
  function onPhotosLoaded(photosList, JSZip) {
    if (photosList.length === 0) {
      alert("暂无照片可导出");
      return;
    }

    photosList.sort(function(a, b) { return b.uploadedAt - a.uploadedAt; });

    var zip = new JSZip();
    var folder = zip.folder("520-photos");

    for (var i = 0; i < photosList.length; i++) {
      var p = photosList[i];
      var base64 = p.dataUrl.split(",")[1];
      var filename = "photo_" + String(i + 1).padStart(3, "0") + ".jpg";
      folder.file(filename, base64, { base64: true });
    }

    zip.generateAsync({ type: "blob" }).then(function(content) {
      var a = document.createElement("a");
      a.href = URL.createObjectURL(content);
      a.download = "520-photos-" + photosList.length + ".zip";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(a.href);
    });
  }

  // ==================== 拖拽上传 ====================

  var dropZone = document.getElementById("drop-zone");
  var fileInput = document.getElementById("file-input");

  if (dropZone && fileInput) {
    var dropTextMain = document.getElementById("drop-text-main");
    var dropTextSub = document.getElementById("drop-text-sub");

    dropZone.addEventListener("dragenter", function(e) {
      e.preventDefault();
      dropZone.style.borderColor = "#ED6B86";
      dropZone.style.background = "rgba(237,107,134,0.08)";
      if (dropTextMain) dropTextMain.textContent = "释放以上传";
      if (dropTextSub) dropTextSub.textContent = "松开鼠标完成上传";
    });

    dropZone.addEventListener("dragover", function(e) {
      e.preventDefault();
    });

    dropZone.addEventListener("dragleave", function() {
      dropZone.style.borderColor = "";
      dropZone.style.background = "";
      if (dropTextMain) dropTextMain.textContent = "拖拽照片到这里";
      if (dropTextSub) dropTextSub.textContent = "或点击选择文件";
    });

    dropZone.addEventListener("drop", function(e) {
      e.preventDefault();
      dropZone.style.borderColor = "";
      dropZone.style.background = "";
      if (dropTextMain) dropTextMain.textContent = "拖拽照片到这里";
      if (dropTextSub) dropTextSub.textContent = "或点击选择文件";
      handleFiles(e.dataTransfer.files);
    });

    dropZone.addEventListener("click", function() {
      fileInput.click();
    });

    fileInput.addEventListener("change", function(e) {
      if (e.target.files) {
        handleFiles(e.target.files);
        e.target.value = "";
      }
    });
  }

  // ESC 关闭 Modal
  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") {
      window.Love520.closePhotoModal();
    }
  });

  // 初始加载
  loadPhotos();
})();
</script>
```

- [ ] **Step 2: 更新 PhotoGallery 模板中的导出按钮 onclick**

将 `onclick="window.exportPhotos()"` 改为 `onclick="window.Love520.exportPhotos()"`

- [ ] **Step 3: 提交**

```bash
git add src/components/PhotoGallery.astro
git commit -m "fix: PhotoGallery 修复全局变量污染/文件名只读/容量提示/innerHTML风险"
```

---

### Task 3: 重构 MessageBoard.astro — 修复 bug 4/5

**Files:**
- 修改: `src/components/MessageBoard.astro`

**受影响的已有模块：** 留言发送、删除、显示功能

**Bug 修复清单：**
- Bug 4: 全局变量污染 → 收拢到 `window.Love520` 命名空间
- Bug 5: IndexedDB 初始化缺失 → 使用统一的 openDB 函数

- [ ] **Step 1: 重写 MessageBoard.astro 的 script 部分**

将整个 `<script is:inline>` 替换为以下内容（保留组件模板部分不变）：

```html
<script is:inline>
(function() {
  // 确保命名空间存在
  window.Love520 = window.Love520 || {};

  // ==================== 工具函数 ====================

  /** HTML 转义，防止 XSS 攻击 */
  function escapeHtml(str) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  /** 格式化时间，显示相对时间 */
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
    return date.getFullYear() + "/" + (date.getMonth() + 1) + "/" + date.getDate();
  }

  // ==================== IndexedDB 操作 ====================
  // Bug 5 修复：统一使用 openDB 函数，确保 onupgradeneeded 创建 objectStore

  var DB_NAME = "love520";
  var DB_VERSION = 1;

  function openDB(callback) {
    var req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = function(e) {
      var db = e.target.result;
      if (!db.objectStoreNames.contains("photos")) {
        db.createObjectStore("photos", { keyPath: "id" });
      }
      if (!db.objectStoreNames.contains("messages")) {
        db.createObjectStore("messages", { keyPath: "id" });
      }
    };
    req.onsuccess = function(e) {
      callback(e.target.result);
    };
    req.onerror = function(e) {
      console.error("IndexedDB 打开失败:", e.target.error);
    };
  }

  // ==================== 留言操作 ====================

  /** 加载留言列表 */
  function loadMessages() {
    var listEl = document.getElementById("message-list");
    var emptyEl = document.getElementById("message-empty");
    if (!listEl || !emptyEl) return;

    openDB(function(db) {
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
            '<button data-msg-id="' + escapeHtml(msg.id) + '" class="msg-delete-btn text-[#C4A4AB] hover:text-[#ED6B86] transition-colors p-1">' +
            '<svg class="w-4 h-4" style="stroke: currentColor; stroke-width: 1.5; fill: none;" viewBox="0 0 24 24">' +
            '<path d="M6 18L18 6M6 6l12 12" stroke-linecap="round"/></svg></button>' +
            '</div></div>';
        }
        listEl.innerHTML = html;

        // 使用事件委托绑定删除按钮，避免 inline onclick
        listEl.querySelectorAll(".msg-delete-btn").forEach(function(btn) {
          btn.addEventListener("click", function() {
            var id = btn.getAttribute("data-msg-id");
            if (id) window.Love520.deleteMessage(id);
          });
        });
      };
    });
  }

  // ==================== 全局函数（命名空间化，修复 Bug 4） ====================

  /** 删除留言 */
  window.Love520.deleteMessage = function(id) {
    if (!confirm("确定要删除这条留言吗？")) return;

    openDB(function(db) {
      var tx = db.transaction("messages", "readwrite");
      var store = tx.objectStore("messages");
      store.delete(id);
      tx.oncomplete = function() {
        db.close();
        loadMessages();
      };
    });
  };

  // ==================== 发送留言 ====================

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

      openDB(function(db) {
        var tx = db.transaction("messages", "readwrite");
        var store = tx.objectStore("messages");
        store.put(message);
        tx.oncomplete = function() {
          db.close();
          inputEl.value = "";
          loadMessages();
        };
      });
    });
  }

  // 初始化加载
  loadMessages();
})();
</script>
```

- [ ] **Step 2: 提交**

```bash
git add src/components/MessageBoard.astro
git commit -m "fix: MessageBoard 修复全局变量污染和 IndexedDB 初始化缺失"
```

---

### Task 4: 修复 PhotoModal.astro — 配合命名空间调整

**Files:**
- 修改: `src/components/PhotoModal.astro`

**受影响的已有模块：** 照片预览 Modal 的关闭功能

- [ ] **Step 1: 更新 PhotoModal 中的 onclick 引用**

将 `onclick="window.closePhotoModal(event)"` 改为 `onclick="window.Love520.closePhotoModal(event)"`
将 `onclick="window.closePhotoModal()"` 改为 `onclick="window.Love520.closePhotoModal()"`

- [ ] **Step 2: 提交**

```bash
git add src/components/PhotoModal.astro
git commit -m "fix: PhotoModal 关闭函数迁移到 Love520 命名空间"
```

---

### Task 5: 修复 BaseLayout.astro — 移除 CDN script（Bug 2）

**Files:**
- 修改: `src/layouts/BaseLayout.astro`

**受影响的已有模块：** 所有页面的 head 部分

- [ ] **Step 1: 移除 JSZip CDN script 标签**

删除这一行：
```html
<script src="https://unpkg.com/jszip@3.10.1/dist/jszip.min.js" defer></script>
```

JSZip 改为在 PhotoGallery 的导出函数中通过动态 `import()` 加载 npm 包。

- [ ] **Step 2: 提交**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "fix: 移除 JSZip CDN 引入，改用 npm 动态 import"
```

---

### Task 6: 修复 Hero.astro — 计时器清理（Bug 9）

**Files:**
- 修改: `src/components/Hero.astro`

**受影响的已有模块：** 恋爱计时器

- [ ] **Step 1: 添加 setInterval 返回值清理逻辑**

将计时器脚本修改为：

```html
<script is:inline>
  (function() {
    var container = document.getElementById("timer-container");
    if (!container) return;
    var startDateStr = container.getAttribute("data-start-date");
    var startDate = new Date(startDateStr + "T00:00:00").getTime();
    var timerEl = document.getElementById("timer");

    function updateTimer() {
      var now = Date.now();
      var diff = now - startDate;

      if (isNaN(startDate)) {
        timerEl.textContent = "日期解析错误";
        return;
      }

      var days = Math.floor(diff / (1000 * 60 * 60 * 24));
      var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((diff % (1000 * 60)) / 1000);

      if (timerEl) {
        timerEl.textContent = days + "\u5929 " + String(hours).padStart(2, '0') + "\u65f6 " + String(minutes).padStart(2, '0') + "\u5206 " + String(seconds).padStart(2, '0') + "\u79d2";
      }
    }

    updateTimer();
    var timer = setInterval(updateTimer, 1000);

    // Bug 9 修复：页面卸载时清除定时器，避免内存泄漏
    window.addEventListener("beforeunload", function() {
      clearInterval(timer);
    });
  })();
</script>
```

- [ ] **Step 2: 提交**

```bash
git add src/components/Hero.astro
git commit -m "fix: 计时器添加 beforeunload 清理，避免内存泄漏"
```

---

### Task 7: 清理 package.json — 移除 localforage 依赖（Bug 1）

**Files:**
- 修改: `package.json`

**受影响的已有模块：** 依赖管理

- [ ] **Step 1: 从 package.json 中移除 localforage**

将 dependencies 中的 `"localforage": "^1.10.0"` 删除。jszip 保留（导出功能需要）。

- [ ] **Step 2: 安装依赖更新 lock 文件**

```bash
npm install
```

- [ ] **Step 3: 提交**

```bash
git add package.json package-lock.json
git commit -m "chore: 移除未使用的 localforage 依赖"
```

---

### Task 8: 修复 tsconfig.json — 移除未使用路径别名（Bug 11）

**Files:**
- 修改: `tsconfig.json`

**受影响的已有模块：** TypeScript 配置

- [ ] **Step 1: 移除未使用的 paths 配置**

将 tsconfig.json 修改为：

```json
{
  "extends": "astro/tsconfigs/strict"
}
```

移除 `baseUrl` 和 `paths`，因为代码中全部使用相对路径，别名从未使用。

- [ ] **Step 2: 提交**

```bash
git add tsconfig.json
git commit -m "chore: 移除 tsconfig.json 中未使用的路径别名配置"
```

---

### Task 9: 清理仓库文件（Bug 8）

**Files:**
- 删除: `夏夜最后的烟火 - 颜人中.mp3`
- 删除: `夏夜最后的烟火 - 颜人中.mp3#459088908.320mp3.zip`
- 删除: `test-verify.py`
- 删除: `final-design-preview.html`

**受影响的已有模块：** 无（纯清理）

- [ ] **Step 1: 从 git 追踪中删除这些文件**

```bash
git rm "夏夜最后的烟火 - 颜人中.mp3"
git rm "夏夜最后的烟火 - 颜人中.mp3#459088908.320mp3.zip"
git rm test-verify.py
git rm final-design-preview.html
```

注意：`.gitignore` 中已有 `*.mp3`、`*.mp3.*`、`test-verify.py`、`final-design-preview.html` 规则，删除后不会再被追踪。

- [ ] **Step 2: 提交**

```bash
git commit -m "chore: 清理仓库中的音乐文件和临时文件"
```

---

### Task 10: 数据库迁移兼容性处理

**Files:**
- 修改: `src/lib/db.ts`（如需要）

**受影响的已有模块：** 旧数据兼容性

**说明：** 旧版 PhotoGallery 使用 `love520_photos` 数据库名，新版统一为 `love520`。需要处理数据迁移。

- [ ] **Step 1: 在 PhotoGallery 的 script 中添加旧数据库迁移逻辑**

在 PhotoGallery.astro 的 IIFE 开头添加迁移函数：

```javascript
/**
 * 数据库迁移：将旧版 love520_photos 数据库中的照片迁移到新版 love520 数据库
 * 迁移完成后删除旧数据库，避免数据丢失
 */
function migrateOldDB() {
  var oldDBName = "love520_photos";
  var req = indexedDB.open(oldDBName);

  req.onupgradeneeded = function(e) {
    // 旧数据库不存在，无需迁移
    e.target.transaction.abort();
    indexedDB.deleteDatabase(oldDBName);
  };

  req.onsuccess = function(e) {
    var oldDB = e.target.result;
    // 检查旧数据库中是否有 photos store
    if (!oldDB.objectStoreNames.contains("photos")) {
      oldDB.close();
      indexedDB.deleteDatabase(oldDBName);
      return;
    }

    var tx = oldDB.transaction("photos", "readonly");
    var store = tx.objectStore("photos");
    var all = [];
    store.openCursor().onsuccess = function(ev) {
      var cursor = ev.target.result;
      if (cursor) {
        all.push(cursor.value);
        cursor.continue();
      } else {
        oldDB.close();
        if (all.length === 0) {
          indexedDB.deleteDatabase(oldDBName);
          return;
        }
        // 将旧数据写入新数据库
        openDB(function(newDB) {
          var newTx = newDB.transaction("photos", "readwrite");
          var newStore = newTx.objectStore("photos");
          for (var i = 0; i < all.length; i++) {
            newStore.put(all[i]);
          }
          newTx.oncomplete = function() {
            newDB.close();
            indexedDB.deleteDatabase(oldDBName);
            console.log("已迁移 " + all.length + " 张照片到新数据库");
            loadPhotos(); // 重新加载
          };
        });
      }
    };
  };

  req.onerror = function() {
    // 旧数据库不存在或无法打开，忽略
  };
}

// 页面加载时尝试迁移
migrateOldDB();
```

- [ ] **Step 2: 提交**

```bash
git add src/components/PhotoGallery.astro
git commit -m "fix: 添加旧数据库迁移逻辑，确保照片数据不丢失"
```

---

## 自检清单

- [x] Bug 1 (storage.ts 死代码): Task 1 删除 + Task 7 移除依赖
- [x] Bug 2 (JSZip 双重引入): Task 2 动态 import + Task 5 移除 CDN
- [x] Bug 3 (file.name 只读): Task 2 使用 safeName 变量
- [x] Bug 4 (全局变量污染): Task 2/3/4 收拢到 Love520 命名空间
- [x] Bug 5 (留言板 IndexedDB 初始化): Task 3 统一 openDB 函数
- [x] Bug 6 (Base64 容量风险): Task 2 添加 checkStorageQuota
- [x] Bug 7 (.gitignore): 已在阶段 02 创建
- [x] Bug 8 (仓库文件清理): Task 9
- [x] Bug 9 (setInterval 清理): Task 6
- [x] Bug 10 (innerHTML 拼接): Task 2 改用 DOM API
- [x] Bug 11 (路径别名): Task 8
