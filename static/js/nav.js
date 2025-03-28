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