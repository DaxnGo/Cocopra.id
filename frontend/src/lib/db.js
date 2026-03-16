import { openDB } from 'idb';

const DB_NAME = 'cocopra-db';
const DB_VERSION = 1;

export const STORES = {
    HARGA: 'pending-harga',
    PEST: 'pending-scans'
};

export async function initDB() {
    return openDB(DB_NAME, DB_VERSION, {
        upgrade(db) {
            // Store untuk antrean harga
            if (!db.objectStoreNames.contains(STORES.HARGA)) {
                db.createObjectStore(STORES.HARGA, { keyPath: 'id', autoIncrement: true });
            }
            // Store untuk antrean pest scan
            if (!db.objectStoreNames.contains(STORES.PEST)) {
                db.createObjectStore(STORES.PEST, { keyPath: 'id', autoIncrement: true });
            }
        },
    });
}

// Helper: Menyimpan request ke Object Store tertentu
export async function saveToQueue(storeName, data) {
    const db = await initDB();
    const tx = db.transaction(storeName, 'readwrite');
    const store = tx.objectStore(storeName);

    // Tambahkan meta data internal
    const payload = {
        ...data,
        _queuedAt: new Date().toISOString(),
        _status: 'pending' // pending, processing, failed
    };

    await store.add(payload);
    await tx.done;
    return true;
}

// Helper: Mengambil semua antrean
export async function getAllFromQueue(storeName) {
    const db = await initDB();
    return db.getAll(storeName);
}

// Helper: Menghapus item dari antrean setelah sukses dikirim
export async function removeFromQueue(storeName, id) {
    const db = await initDB();
    const tx = db.transaction(storeName, 'readwrite');
    await tx.objectStore(storeName).delete(id);
    await tx.done;
}
