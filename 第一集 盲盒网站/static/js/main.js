// Blind Box Display Website - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize based on current page
    const path = window.location.pathname;

    if (path === '/') {
        loadBoxesList();
    } else if (path.startsWith('/box/')) {
        const boxId = path.split('/').pop();
        loadBoxDetail(boxId);
    }
});

// Load all boxes for the index page
async function loadBoxesList() {
    const container = document.getElementById('boxes-container');
    if (!container) return;

    try {
        const response = await fetch('/api/boxes');
        if (!response.ok) throw new Error('Failed to fetch boxes');

        const boxes = await response.json();

        if (boxes.length === 0) {
            container.innerHTML = '<p class="no-data">暂无盲盒商品</p>';
            return;
        }

        container.innerHTML = boxes.map(box => `
            <a href="/box/${box.id}" class="box-card">
                <img src="${box.image_path || '/static/images/placeholder.png'}"
                     alt="${box.name}"
                     class="box-image"
                     onerror="this.src='/static/images/placeholder.png'">
                <h3 class="box-name">${box.name}</h3>
                <p class="box-price">¥${parseFloat(box.price).toFixed(2)}</p>
                ${box.is_secret ? '<span class="secret-badge">隐藏</span>' : ''}
            </a>
        `).join('');

    } catch (error) {
        console.error('Error loading boxes:', error);
        container.innerHTML = '<p class="error">加载失败，请稍后重试</p>';
    }
}

// Load box detail for the detail page
async function loadBoxDetail(boxId) {
    const container = document.getElementById('box-detail');
    if (!container) return;

    try {
        const response = await fetch(`/api/boxes/${boxId}`);
        if (!response.ok) {
            if (response.status === 404) {
                container.innerHTML = '<p class="error">盲盒不存在</p>';
            } else {
                throw new Error('Failed to fetch box');
            }
            return;
        }

        const box = await response.json();

        let descriptionContent;
        if (box.is_secret) {
            descriptionContent = '<div class="secret-placeholder">神秘盲盒</div>';
        } else {
            descriptionContent = `<p class="detail-description">${box.description || '无描述'}</p>`;
        }

        container.innerHTML = `
            <img src="${box.image_path || '/static/images/placeholder.png'}"
                 alt="${box.name}"
                 class="detail-image"
                 onerror="this.src='/static/images/placeholder.png'">
            <h2 class="detail-name">${box.name}</h2>
            <p class="detail-price">¥${parseFloat(box.price).toFixed(2)}</p>
            ${descriptionContent}
            ${box.is_secret ? '<p class="secret-notice">* 此盲盒内容已隐藏</p>' : ''}
        `;

    } catch (error) {
        console.error('Error loading box detail:', error);
        container.innerHTML = '<p class="error">加载失败，请稍后重试</p>';
    }
}