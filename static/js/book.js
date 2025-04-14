// 模拟数据
const mediaData = [
    {
        type: 'book',
        status: 'done',
        title: '百年孤独',
        image: 'https://example.com/book1.jpg',
        score: 4.5,
        link: '/book/123'
    },
    {
        type: 'movie',
        status: 'done',
        title: '肖申克的救赎',
        image: 'https://example.com/movie1.jpg',
        score: 4.8,
        link: '/movie/456'
    },
    // 更多数据...
];

// 初始化
function init() {
    renderMediaItems(filterMedia());
    addEventListeners();
}

// 过滤媒体数据
function filterMedia() {
    const activeType = document.querySelector('.media-nav button.active').dataset.type;
    const activeStatus = document.querySelector('.status-tab.active').dataset.status;
    return mediaData.filter(item => 
        item.type === activeType && 
        item.status === activeStatus
    );
}

// 渲染媒体项
function renderMediaItems(data) {
    const grid = document.getElementById('mediaGrid');
    grid.innerHTML = data.map(item => `
        <div class="media-item">
            <img src="${item.image}" alt="${item.title}" class="media-image" 
                    onclick="window.location.href='${item.link}'">
            <div class="rating">
                <div class="stars">${renderStars(item.score)}</div>
                <div class="score">${item.score.toFixed(1)}</div>
            </div>
            <div class="title" onclick="window.location.href='${item.link}'">${item.title}</div>
        </div>
    `).join('');
}

// 渲染星星
function renderStars(score) {
    const fullStars = Math.floor(score);
    const halfStar = score % 1 >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;
    
    return '★'.repeat(fullStars) + 
            (halfStar ? '½' : '') + 
            '☆'.repeat(emptyStars);
}

// 事件监听
function addEventListeners() {
    // 类型切换
    document.querySelectorAll('.media-nav button').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelector('.media-nav button.active').classList.remove('active');
            btn.classList.add('active');
            renderMediaItems(filterMedia());
        });
    });

    // 状态切换
    document.querySelectorAll('.status-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelector('.status-tab.active').classList.remove('active');
            tab.classList.add('active');
            renderMediaItems(filterMedia());
        });
    });
}

// 初始化
init();