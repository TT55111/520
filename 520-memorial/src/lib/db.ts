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
