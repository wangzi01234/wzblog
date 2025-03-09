// 日历导航事件委托
document.addEventListener('click', (e) => {
  const target = e.target.closest('[data-action]');
  if (!target) return;

  switch (target.dataset.action) {
    case 'year-prev':
      CalendarManager.changeYear(-1);
      break;
    case 'year-next':
      CalendarManager.changeYear(1);
      break;
    case 'month-prev':
      CalendarManager.changeMonth(-1);
      break;
    case 'month-next':
      CalendarManager.changeMonth(1);
      break;
  }
});

const config = window.appConfig || {};

// 公共方法
window.CalendarManager = {
  changeMonth(offset) {
    let currentMonth = config.month;
    let currentYear = config.year;

    currentMonth += offset;
    if (currentMonth > 12) {
      currentMonth = 1;
      currentYear++;
    } else if (currentMonth < 1) {
      currentMonth = 12;
      currentYear--;
    }
    this.updateCalendar(currentYear, currentMonth);
  },

  changeYear(offset) {
    this.updateCalendar(
      config.year + offset,
      config.month
    );
  },
  updateCalendar(year, month) {
    const baseDate = `${year}-${String(month).padStart(2, '0')}-01`;
    this.selectDate(baseDate);
  },
  selectDate(dateStr) {
    const url = config.planUrl.replace('DATE', encodeURIComponent(dateStr));
    window.location.href = url;
  },
}


// 通过tbody监听点击事件
document.querySelector('tbody').addEventListener('click', function(e) {
  const td = e.target.closest('td');
  // 判断是否为有效日期单元格
  if (td && !td.classList.contains('prev-month')) {
    const selectedDate = td.dataset.date;
    CalendarManager.selectDate(selectedDate); // 调用日期选择函数
  }
});