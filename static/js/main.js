document.querySelector('.nav-toggle').addEventListener('click', function(e) {
  e.stopPropagation(); // 阻止事件冒泡
  const menu = document.querySelector('.nav-menu');
  menu.classList.toggle('active'); // 使用class切换代替直接修改style
});

// 点击页面其他区域关闭菜单
document.addEventListener('click', function() {
  const menu = document.querySelector('.nav-menu');
  menu.classList.remove('active');
});