/**
 * 照片存储封装 - 使用 localforage (IndexedDB 封装库)
 * 提供照片的增删查功能
 */
import localforage from "localforage";

// 初始化存储实例
const photoStore = localforage.createInstance({
  name: "love520",
  storeName: "photos",
});

/**
 * 照片数据结构
 */
export interface PhotoItem {
  id: string;        // 唯一 ID
  dataUrl: string;   // Base64 图片数据
  name: string;      // 文件名
  uploadedAt: number; // 上传时间戳
}

/**
 * 保存照片到 IndexedDB
 * @param photo - 照片对象
 */
export async function savePhoto(photo: PhotoItem): Promise<void> {
  await photoStore.setItem(photo.id, photo);
}

/**
 * 获取所有照片（按上传时间倒序）
 */
export async function getAllPhotos(): Promise<PhotoItem[]> {
  const photos: PhotoItem[] = [];
  await photoStore.iterate((value: PhotoItem) => {
    photos.push(value);
  });
  // 按上传时间倒序排列
  return photos.sort((a, b) => b.uploadedAt - a.uploadedAt);
}

/**
 * 删除照片
 * @param id - 照片 ID
 */
export async function deletePhoto(id: string): Promise<void> {
  await photoStore.removeItem(id);
}

/**
 * 生成唯一 ID
 */
export function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

// 留言板存储
export const messageStore = localforage.createInstance({
  name: "love520",
  storeName: "messages",
});
