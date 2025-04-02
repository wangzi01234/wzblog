document.addEventListener('DOMContentLoaded', function() {
    // 通用更新函数
    function updateDateRange(prefix) {
        const year = parseInt(document.getElementById(`filter-year-${prefix}`).value);
        const month = parseInt(document.getElementById(`filter-month-${prefix}`).value);
        const daySelect = document.getElementById(`filter-day-${prefix}`);
        const daysInMonth = new Date(year, month, 0).getDate();

        // 保留当前选中值
        const currentDay = parseInt(daySelect.value);
        
        // 重新生成选项
        daySelect.innerHTML = '';
        for(let day = 1; day <= daysInMonth; day++) {
            const option = new Option(
                day.toString().padStart(2, '0'),
                day.toString().padStart(2, '0'),
                false,
                day === Math.min(currentDay, daysInMonth) // 保持选中状态
            );
            daySelect.add(option);
        }
    }

    // 为两个选择器绑定事件
    ['start', 'end'].forEach(prefix => {
        document.getElementById(`filter-year-${prefix}`).addEventListener('change', () => {
            updateDateRange(prefix);
            checkDateRange();
        });
        
        document.getElementById(`filter-month-${prefix}`).addEventListener('change', () => {
            updateDateRange(prefix);
            checkDateRange();
        });

        document.getElementById(`filter-day-${prefix}`).addEventListener('change', checkDateRange);
    });

    // 初始化两个选择器
    ['start', 'end'].forEach(updateDateRange);

    // 日期范围检查
    function checkDateRange() {
        const startDate = new Date(
            document.getElementById('filter-year-start').value,
            document.getElementById('filter-month-start').value - 1,
            document.getElementById('filter-day-start').value
        );

        const endDate = new Date(
            document.getElementById('filter-year-end').value,
            document.getElementById('filter-month-end').value - 1,
            document.getElementById('filter-day-end').value
        );

        // 自动修正日期顺序
        if(startDate > endDate) {
            console.log('自动修正日期顺序');
            ['year', 'month', 'day'].forEach(type => {
                const endElement = document.getElementById(`filter-${type}-end`);
                endElement.value = document.getElementById(`filter-${type}-start`).value;
            });
            updateDateRange('end');
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // 状态存储对象
    let filters = {
        category: null,
        tags: new Set(),
        start_date: null,
        end_date: null
    };

    // 分类选择逻辑（互斥）
    document.querySelectorAll('[data-type="category"]').forEach(item => {
        // console.log(item)
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const isSelected = this.classList.contains('selected');
            console.log(isSelected)
            // 移除所有分类选中状态
            document.querySelectorAll('[data-type="category"]').forEach(el => 
                el.classList.remove('selected'));
            
            // 切换当前状态
            if (!isSelected) {
                const isSelected = true
                this.classList.add('selected');
                console.log(isSelected)
                filters.category = this.dataset.value;
            } else {
                filters.category = null;
            }
        });
    });

    // 标签选择逻辑（多选）
    document.querySelectorAll('[data-type="tag"]').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('selected');
            
            const tagValue = this.dataset.value;
            if (this.classList.contains('selected')) {
                filters.tags.add(tagValue);
            } else {
                filters.tags.delete(tagValue);
            }
        });
    });

    // 清空按钮
    document.getElementById('filter-clear').addEventListener('click', function() {
        // 清除选中状态
        document.querySelectorAll('.selected').forEach(el => 
            el.classList.remove('selected'));
        
        // 重置日期选择器
        ['start', 'end'].forEach(prefix => {
            document.getElementById(`filter-year-${prefix}`).value = 
                prefix === 'start' ? 2024 : 2026;
            document.getElementById(`filter-month-${prefix}`).value = 
                prefix === 'start' ? '01' : '12';
            document.getElementById(`filter-day-${prefix}`).value = 
                prefix === 'start' ? '01' : '31';
        });

        // 清空存储
        filters = {
            category: null,
            tags: new Set(),
            start_date: null,
            end_date: null
        };
    });

    // 查询按钮
    document.getElementById('filter-search').addEventListener('click', function() {
        // 获取日期参数
        const getDate = prefix => {
            const year = document.getElementById(`filter-year-${prefix}`).value;
            const month = document.getElementById(`filter-month-${prefix}`).value;
            const day = document.getElementById(`filter-day-${prefix}`).value;
            return `${year}-${month}-${day}`;
        };

        // 构建参数对象（自动过滤空值）
        const params = {
            ...(filters.category && { category: filters.category }), // 仅当有分类时包含
            ...(filters.tags.size > 0 && { tags: Array.from(filters.tags).join(',') }), // 仅当有标签时包含
            start_date: getDate('start'),
            end_date: getDate('end')
        };

        // 构造URL
        const query = new URLSearchParams(params).toString();
        window.location.href = `/filter?${query}`;
    });

});

document.addEventListener('DOMContentLoaded', function() {
    // 移动端断点设置（推荐使用 1024px 作为分界）
  const MOBILE_BREAKPOINT = 1024 
  let isMobileView = window.innerWidth < MOBILE_BREAKPOINT
  
  // 初始化检测
  if (!isMobileView) return
  // 元素获取
  const pagination = document.querySelector('.pagination')
  const loadingIndicator = document.querySelector('.loading-indicator')
  const noMore = document.querySelector('.no-more')
  const postList = document.querySelector('.post-list')

  // 初始化分页状态
  let currentPage = parseInt(pagination.dataset.currentPage)
  let totalPages = parseInt(pagination.dataset.totalPages)
  let isLoading = false
  let hasMore = currentPage < totalPages

  // 事件监听整合（包含节流）
  function initScrollListeners() {
    checkScroll() // 初始检查
    window.addEventListener('scroll', throttle(checkScroll, 200))
    window.addEventListener('resize', throttle(checkScroll, 200))
  }

    // 修改后的滚动检测逻辑
  function checkScroll() {
    if (!hasMore)
      hideLoading()
      showNoMore()
    // 状态锁定检查
    if (isLoading || !hasMore) return
    // 获取精确的滚动位置
    const { scrollTop, scrollHeight, clientHeight } = getAccurateScrollPosition()
    
    // 动态触发阈值（根据容器高度比例计算）
    const triggerThreshold = clientHeight * 0.3 // 剩余30%高度时触发
    const triggerPoint = scrollHeight - triggerThreshold
    
    // 双重位置验证
    const currentPosition = scrollTop + clientHeight
    const isValidScroll = currentPosition >= triggerPoint
    
    // 历史位置比对（防止快速滚动跳过检测点）
    const prevPosition = window._lastScrollPosition || 0
    window._lastScrollPosition = currentPosition
    
    if (isValidScroll || (prevPosition > triggerPoint && currentPosition > triggerPoint)) {
        console.log("触发加载，当前位置:", currentPosition)
        loadMore()
    }
  }

  // 保留原有分页逻辑
  async function loadMore() {
    isLoading = true
    showLoading()
    try {
      const nextPage = currentPage + 1
      const url = buildPageUrl(nextPage)
      const response = await fetch(url)
      if (!response.ok) throw new Error(response.status)
      const html = await response.text()
      const parser = new DOMParser()
      const doc = parser.parseFromString(html, 'text/html')
      // 更新文章列表
      const newContent = doc.querySelector('.post-list').innerHTML
      postList.insertAdjacentHTML('beforeend', newContent)
      // 更新分页信息
      const newPagination = doc.querySelector('.pagination')
      currentPage = parseInt(newPagination.dataset.currentPage)
      totalPages = parseInt(newPagination.dataset.totalPages)
      hasMore = currentPage < totalPages
      // 更新页面标题（可选）
      if (currentPage > 1) {
        document.title = `${document.title.split(' - ')} - 第${currentPage}页`
      }
    } catch (error) {
      console.error('加载失败:', error)
      hasMore = true // 允许重试
    } finally {
      isLoading = false
      hideLoading()
      if (!hasMore) showNoMore()
    }
  }

  // 辅助函数保持原样
  function buildPageUrl(page) {
    const url = new URL(window.location.href)
    const params = new URLSearchParams(url.search)
    params.set('page', page)
    return `${url.pathname}?${params}`
  }

  function showLoading() {
    loadingIndicator.style.display = 'flex' // 修正为英文 block
    noMore.style.display = 'none'
  }

  function hideLoading() {
    loadingIndicator.style.display = 'none'
  }

  function showNoMore() {
    noMore.style.display = 'flex'
  }

// 获取精确滚动位置（兼容不同浏览器）
function getAccurateScrollPosition() {
    return {
      scrollTop: Math.max(
        document.documentElement.scrollTop,
        document.body.scrollTop
      ),
      scrollHeight: Math.max(
        document.documentElement.scrollHeight,
        document.body.scrollHeight
      ),
      clientHeight: window.innerHeight || document.documentElement.clientHeight
    }
  }
  
  // 调整节流函数（使用requestAnimationFrame优化）
  function throttle(fn, delay) {
    let lastCall = 0
    let frameId = null
    
    return function(...args) {
      const now = Date.now()
      const context = this
      
      const execute = () => {
        fn.apply(context, args)
        lastCall = now
      }
      
      if (now - lastCall >= delay) {
        execute()
      } else {
        cancelAnimationFrame(frameId)
        frameId = requestAnimationFrame(execute)
      }
    }
  }

  // 初始化
  initScrollListeners()
})
