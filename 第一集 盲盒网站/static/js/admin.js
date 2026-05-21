// Blind Box Display Website - Admin JavaScript

// Session check for all admin pages
async function checkAdminSession() {
    try {
        const response = await fetch('/api/admin/check', { credentials: 'include' });
        if (!response.ok) {
            window.location.href = '/admin/login';
            return false;
        }
        const data = await response.json();
        if (!data.logged_in) {
            window.location.href = '/admin/login';
            return false;
        }
        return true;
    } catch (err) {
        window.location.href = '/admin/login';
        return false;
    }
}

// Admin logout function
async function adminLogout() {
    if (!confirm('确定要退出登录吗？')) return;
    try {
        const response = await fetch('/api/admin/logout', {
            method: 'POST',
            credentials: 'include'
        });
        if (response.ok) {
            window.location.href = '/admin/login';
        }
    } catch (err) {
        window.location.href = '/admin/login';
    }
}

// Load boxes with pagination
async function loadBoxesForAdmin(page = 1, itemsPerPage = 10) {
    try {
        const response = await fetch('/api/boxes');
        const boxes = await response.json();
        return boxes;
    } catch (err) {
        console.error('Failed to load boxes:', err);
        return [];
    }
}

// Delete box with confirmation
async function deleteBoxConfirm(id) {
    if (!confirm('确定要删除这个盲盒吗？此操作无法撤销。')) return;
    try {
        const response = await fetch(`/api/boxes/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        const data = await response.json();
        if (data.success) {
            return true;
        } else {
            alert('删除失败：' + (data.error || '未知错误'));
            return false;
        }
    } catch (err) {
        alert('网络错误，请稍后重试');
        return false;
    }
}

// Image upload handler
async function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            credentials: 'include',
            body: formData
        });
        const data = await response.json();

        if (data.image_path) {
            return { success: true, image_path: data.image_path };
        } else {
            return { success: false, error: data.error || '上传失败' };
        }
    } catch (err) {
        return { success: false, error: '上传失败，请稍后重试' };
    }
}

// Form submission for box create/update
async function submitBoxForm(formData, isEdit = false, boxId = null) {
    const url = isEdit ? `/api/boxes/${boxId}` : '/api/boxes';
    const method = isEdit ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(formData)
        });
        const result = await response.json();

        if (result.box || result.success) {
            return { success: true };
        } else {
            return { success: false, error: result.error || '保存失败' };
        }
    } catch (err) {
        return { success: false, error: '网络错误，请稍后重试' };
    }
}

// Initialize admin page
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;

    // Attach logout handler if form exists
    const logoutForm = document.getElementById('logout-form');
    if (logoutForm) {
        logoutForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await adminLogout();
        });
    }
});